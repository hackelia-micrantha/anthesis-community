#!/usr/bin/env python3
"""Validate governance-lab schemas and canonical conformance fixtures."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "governance-lab"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate(instance: object, schema_path: Path, label: str) -> list[str]:
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = []
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label}:{location}: {error.message}")
    return errors


def main() -> int:
    errors: list[str] = []

    vectors = load_yaml(SPEC / "conformance-vectors.yaml")
    if not isinstance(vectors, dict) or vectors.get("version") != "anthesis.conformance/v1":
        errors.append("conformance-vectors.yaml:<root>: unsupported or missing version")
        scenarios = []
    else:
        scenarios = vectors.get("scenarios", [])

    if not isinstance(scenarios, list) or len(scenarios) != 7:
        errors.append("conformance-vectors.yaml:scenarios: expected exactly seven scenarios")
        scenarios = scenarios if isinstance(scenarios, list) else []

    seen_ids: set[str] = set()
    for index, scenario in enumerate(scenarios):
        errors.extend(
            validate(
                scenario,
                SPEC / "scenario.schema.json",
                f"conformance-vectors.yaml:scenarios[{index}]",
            )
        )
        if isinstance(scenario, dict):
            scenario_id = scenario.get("id")
            if isinstance(scenario_id, str):
                if scenario_id in seen_ids:
                    errors.append(f"duplicate scenario id: {scenario_id}")
                seen_ids.add(scenario_id)

    policy = load_yaml(SPEC / "examples" / "local-sdlc.policy.yaml")
    errors.extend(validate(policy, SPEC / "policy.schema.json", "local-sdlc.policy.yaml"))

    expected_ids = {f"0{i}-" for i in range(1, 8)}
    if len(seen_ids) == 7 and not all(any(item.startswith(prefix) for item in seen_ids) for prefix in expected_ids):
        errors.append("conformance vectors must include scenarios 01 through 07")

    if errors:
        print("Governance lab contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(scenarios)} scenarios and one policy fixture.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
