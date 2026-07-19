#!/usr/bin/env python3
"""Validate schemas, strict YAML, digests, and governance-lab decisions."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "governance-lab"


class StrictLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("mapping keys must be strings")
        if key in mapping:
            raise ValueError(f"duplicate mapping key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def assert_json_model(value: Any, stack: set[int] | None = None) -> None:
    stack = stack or set()
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite numbers are not allowed")
        return
    if isinstance(value, (list, dict)):
        marker = id(value)
        if marker in stack:
            raise ValueError("cyclic YAML aliases are not allowed")
        stack.add(marker)
        items = value.values() if isinstance(value, dict) else value
        if isinstance(value, dict) and not all(isinstance(k, str) for k in value):
            raise ValueError("mapping keys must be strings")
        for item in items:
            assert_json_model(item, stack)
        stack.remove(marker)
        return
    raise ValueError(f"non-JSON YAML value is not allowed: {type(value).__name__}")


def load_yaml(path: Path) -> Any:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=StrictLoader)
    assert_json_model(value)
    return value


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(instance: Any, schema_name: str, label: str) -> list[str]:
    validator = Draft202012Validator(load_json(SPEC / schema_name))
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label}:{location}: {error.message}")
    return errors


def canonical_digest(value: Any) -> str:
    # Fixtures contain only RFC 8785-compatible strings, booleans, nulls, arrays,
    # and objects. This serialization is therefore byte-equivalent to JCS.
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def glob_regex(pattern: str) -> re.Pattern[str]:
    out = ["^"]
    i = 0
    while i < len(pattern):
        char = pattern[i]
        if char == "*":
            if i + 1 < len(pattern) and pattern[i + 1] == "*":
                out.append(".*")
                i += 2
            else:
                out.append("[^/]*")
                i += 1
        elif char == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(char))
            i += 1
    out.append("$")
    return re.compile("".join(out))


def command_matches(declared: str, attempted: str) -> bool:
    return attempted == declared or attempted.startswith(declared + " ")


def rule_matches(rule: dict[str, Any], attempt: dict[str, Any], scenario: dict[str, Any]) -> bool:
    if attempt["action"] not in rule["actions"]:
        return False
    if "paths" in rule and not any(glob_regex(p).fullmatch(attempt.get("path", "")) for p in rule["paths"]):
        return False
    if "commands" in rule and not any(command_matches(c, attempt.get("command", "")) for c in rule["commands"]):
        return False
    if "roles" in rule and scenario["actor"]["role"] not in rule["roles"]:
        return False
    if "runtimes" in rule and scenario["runtime"]["id"] not in rule["runtimes"]:
        return False
    return True


def evaluate(policy: dict[str, Any], profile: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    runtime = scenario["runtime"]["id"]
    if runtime not in profile["allowed_runtimes"]:
        return {"decision": "deny", "source": "engine_guard", "reason": "unknown_runtime"}
    attempt = scenario["attempts"][0]
    for rule in policy["rules"]:
        if rule_matches(rule, attempt, scenario):
            return {
                "decision": rule["effect"],
                "source": "policy_rule",
                "rule_id": rule["id"],
                "reason": rule["reason"],
            }
    return {"decision": policy["default"], "source": "policy_default", "rule_id": "default", "reason": "policy_default"}


def main() -> int:
    errors: list[str] = []
    try:
        vectors = load_yaml(SPEC / "conformance-vectors.yaml")
        policy = load_yaml(SPEC / "examples" / "local-sdlc.policy.yaml")
        profile = load_yaml(SPEC / "examples" / "local.runtime-profile.yaml")
        decision_example = load_json(SPEC / "examples" / "allow.decision.json")
        evidence_example = load_json(SPEC / "examples" / "allow.evidence.json")
    except Exception as exc:
        print(f"Governance lab contract validation failed: {exc}", file=sys.stderr)
        return 1

    errors += schema_errors(policy, "policy.schema.json", "local-sdlc.policy.yaml")
    errors += schema_errors(profile, "runtime-profile.schema.json", "local.runtime-profile.yaml")
    errors += schema_errors(decision_example, "decision.schema.json", "allow.decision.json")
    errors += schema_errors(evidence_example, "evidence.schema.json", "allow.evidence.json")

    scenarios = vectors.get("scenarios", []) if isinstance(vectors, dict) else []
    if vectors.get("version") != "anthesis.conformance/v1" or len(scenarios) != 7:
        errors.append("conformance-vectors.yaml must contain exactly seven v1 scenarios")

    digest = canonical_digest(policy)
    if digest != vectors.get("expected_policy_digest"):
        errors.append(f"policy digest mismatch: expected {vectors.get('expected_policy_digest')}, got {digest}")

    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"conformance-vectors.yaml:scenarios[{index}]"
        errors += schema_errors(scenario, "scenario.schema.json", label)
        scenario_id = scenario.get("id")
        if scenario_id in seen:
            errors.append(f"duplicate scenario id: {scenario_id}")
        seen.add(scenario_id)
        if not errors:
            actual = evaluate(policy, profile, scenario)
            expected = scenario["expected"]
            for field in ("decision", "source", "reason", "rule_id"):
                if actual.get(field) != expected.get(field):
                    errors.append(f"{scenario_id}: expected {field}={expected.get(field)!r}, got {actual.get(field)!r}")
            available_evidence = {"scenario_id", "decision", "decision_source", "policy_digest", "reason", "effect", "engine", "configured_runtime"}
            if actual["source"] != "engine_guard":
                available_evidence.add("policy_rule_id")
            missing = set(expected["evidence"]) - available_evidence
            if missing:
                errors.append(f"{scenario_id}: unavailable expected evidence fields: {sorted(missing)}")

    if {sid[:3] for sid in seen} != {f"0{i}-" for i in range(1, 8)}:
        errors.append("conformance vectors must include scenarios 01 through 07")

    if errors:
        print("Governance lab contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(scenarios)} scenarios, policy/runtime schemas, decisions, evidence, and digest {digest}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
