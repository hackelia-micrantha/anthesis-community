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


def construct_mapping(
    loader: StrictLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError("mapping keys must be strings")
        if key in mapping:
            raise ValueError(f"duplicate mapping key: {key}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
)


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
    # Fixtures contain only RFC 8785-compatible strings, booleans, nulls,
    # arrays, and objects. This serialization is byte-equivalent to JCS for
    # the contract fixtures because they contain no numeric values.
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def glob_regex(pattern: str) -> re.Pattern[str]:
    out = ["^"]
    index = 0
    while index < len(pattern):
        char = pattern[index]
        if char == "*":
            if index + 1 < len(pattern) and pattern[index + 1] == "*":
                out.append(".*")
                index += 2
            else:
                out.append("[^/]*")
                index += 1
        elif char == "?":
            out.append("[^/]")
            index += 1
        else:
            out.append(re.escape(char))
            index += 1
    out.append("$")
    return re.compile("".join(out))


def command_matches(declared: str, attempted: str) -> bool:
    return attempted == declared or attempted.startswith(declared + " ")


def rule_matches(
    rule: dict[str, Any], attempt: dict[str, Any], scenario: dict[str, Any]
) -> bool:
    if attempt["action"] not in rule["actions"]:
        return False
    if "paths" in rule and not any(
        glob_regex(pattern).fullmatch(attempt.get("path", ""))
        for pattern in rule["paths"]
    ):
        return False
    if "commands" in rule and not any(
        command_matches(command, attempt.get("command", ""))
        for command in rule["commands"]
    ):
        return False
    if "roles" in rule and scenario["actor"]["role"] not in rule["roles"]:
        return False
    if "runtimes" in rule and scenario["runtime"]["id"] not in rule["runtimes"]:
        return False
    return True


def evaluate(
    policy: dict[str, Any], profile: dict[str, Any], scenario: dict[str, Any]
) -> dict[str, Any]:
    runtime = scenario["runtime"]["id"]
    if runtime not in profile["allowed_runtimes"]:
        return {
            "decision": "deny",
            "source": "engine_guard",
            "reason": "unknown_runtime",
        }

    attempt = scenario["attempts"][0]
    for rule in policy["rules"]:
        if rule_matches(rule, attempt, scenario):
            return {
                "decision": rule["effect"],
                "source": "policy_rule",
                "rule_id": rule["id"],
                "reason": rule["reason"],
            }

    return {
        "decision": policy["default"],
        "source": "policy_default",
        "rule_id": "default",
        "reason": "policy_default",
    }


def normalized_effect(scenario: dict[str, Any]) -> dict[str, Any]:
    attempt = scenario["attempts"][0]
    return {
        "action": attempt["action"],
        "resource": {"path": attempt["path"]} if "path" in attempt else None,
        "command": attempt.get("command"),
        "actor": scenario["actor"],
        "runtime": scenario["runtime"],
    }


def compare_fields(
    actual: dict[str, Any],
    expected: dict[str, Any],
    fields: tuple[str, ...],
    label: str,
) -> list[str]:
    errors: list[str] = []
    for field in fields:
        if actual.get(field) != expected.get(field):
            errors.append(
                f"{label}: expected {field}={expected.get(field)!r}, "
                f"got {actual.get(field)!r}"
            )
    return errors


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
    errors += schema_errors(
        profile, "runtime-profile.schema.json", "local.runtime-profile.yaml"
    )
    errors += schema_errors(
        decision_example, "decision.schema.json", "allow.decision.json"
    )
    errors += schema_errors(
        evidence_example, "evidence.schema.json", "allow.evidence.json"
    )

    scenarios = vectors.get("scenarios", []) if isinstance(vectors, dict) else []
    if vectors.get("version") != "anthesis.conformance/v1" or len(scenarios) != 7:
        errors.append("conformance-vectors.yaml must contain exactly seven v1 scenarios")

    policy_digest = canonical_digest(policy)
    if policy_digest != vectors.get("expected_policy_digest"):
        errors.append(
            "policy digest mismatch: expected "
            f"{vectors.get('expected_policy_digest')}, got {policy_digest}"
        )

    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        label = f"conformance-vectors.yaml:scenarios[{index}]"
        scenario_errors = schema_errors(scenario, "scenario.schema.json", label)
        errors += scenario_errors

        scenario_id = scenario.get("id")
        if scenario_id in seen:
            errors.append(f"duplicate scenario id: {scenario_id}")
        if isinstance(scenario_id, str):
            seen.add(scenario_id)

        if scenario_errors:
            continue

        actual = evaluate(policy, profile, scenario)
        expected = scenario["expected"]
        errors += compare_fields(
            actual,
            expected,
            ("decision", "source", "reason", "rule_id"),
            str(scenario_id),
        )

        available_evidence = {
            "scenario_id",
            "decision",
            "decision_source",
            "policy_digest",
            "reason",
            "effect",
            "engine",
            "configured_runtime",
        }
        if actual["source"] != "engine_guard":
            available_evidence.add("policy_rule_id")
        missing = set(expected["evidence"]) - available_evidence
        if missing:
            errors.append(
                f"{scenario_id}: unavailable expected evidence fields: {sorted(missing)}"
            )

    if {scenario_id[:3] for scenario_id in seen} != {
        f"0{index}-" for index in range(1, 8)
    }:
        errors.append("conformance vectors must include scenarios 01 through 07")

    scenario_one = next(
        (
            scenario
            for scenario in scenarios
            if scenario.get("id") == "01-allowed-docs-edit"
        ),
        None,
    )
    if scenario_one is None:
        errors.append("missing canonical scenario 01 fixture")
    else:
        result_one = evaluate(policy, profile, scenario_one)
        canonical_common = {
            "scenario_id": scenario_one["id"],
            "decision": result_one["decision"],
            "decision_source": result_one["source"],
            "policy": policy["name"],
            "policy_digest": policy_digest,
            "canonicalization": "rfc8785-json",
            "policy_rule_id": result_one.get("rule_id"),
            "reason": result_one["reason"],
            "effect": normalized_effect(scenario_one),
        }
        errors += compare_fields(
            decision_example,
            canonical_common,
            (
                "scenario_id",
                "decision",
                "decision_source",
                "policy",
                "policy_digest",
                "canonicalization",
                "policy_rule_id",
                "reason",
                "effect",
            ),
            "allow.decision.json",
        )
        errors += compare_fields(
            evidence_example,
            canonical_common,
            (
                "scenario_id",
                "decision",
                "decision_source",
                "policy",
                "policy_digest",
                "canonicalization",
                "policy_rule_id",
                "reason",
                "effect",
            ),
            "allow.evidence.json",
        )

        if evidence_example.get("previous_record_digest") is not None:
            errors.append(
                "allow.evidence.json: first evidence record must have "
                "previous_record_digest=null"
            )
        evidence_without_digest = {
            key: value
            for key, value in evidence_example.items()
            if key != "record_digest"
        }
        computed_record_digest = canonical_digest(evidence_without_digest)
        if evidence_example.get("record_digest") != computed_record_digest:
            errors.append(
                "allow.evidence.json: record digest mismatch: expected "
                f"{computed_record_digest}, got {evidence_example.get('record_digest')}"
            )

    if errors:
        print("Governance lab contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(scenarios)} scenarios, policy/runtime schemas, "
        f"decision/evidence fixtures, policy digest {policy_digest}, and "
        f"evidence digest {evidence_example['record_digest']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
