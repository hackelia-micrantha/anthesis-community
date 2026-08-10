#!/usr/bin/env python3
"""Validate the complete public contract set advertised by the promoted evaluator."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "specs" / "governance-lab"
EXAMPLES = SPEC / "examples"
PROMOTED_SPEC = SPEC / "PROMOTED-CONTRACTS.md"

PROMOTED_CONTRACTS = {
    "anthesis.policy/v1": "policy.schema.json",
    "anthesis.lab-profile/v1": "runtime-profile.schema.json",
    "anthesis.scenario/v1": "scenario.schema.json",
    "anthesis.decision/v1": "decision.schema.json",
    "anthesis.request-binding/v1": "request-binding.schema.json",
    "anthesis.evaluation-request/v1": "evaluation-request.schema.json",
    "anthesis.evidence-bundle/v1": "evidence-bundle.schema.json",
    "anthesis.evidence-bundle-verification/v1": "evidence-bundle-verification.schema.json",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def contains_const(value: Any, expected: str) -> bool:
    if isinstance(value, dict):
        if value.get("const") == expected:
            return True
        return any(contains_const(item, expected) for item in value.values())
    if isinstance(value, list):
        return any(contains_const(item, expected) for item in value)
    return False


def validation_errors(
    instance: Any, validator: Draft202012Validator, label: str
) -> list[str]:
    errors: list[str] = []
    for error in sorted(validator.iter_errors(instance), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        errors.append(f"{label}:{location}: {error.message}")
    return errors


def main() -> int:
    errors: list[str] = []
    validators: dict[str, Draft202012Validator] = {}

    promoted_spec = PROMOTED_SPEC.read_text(encoding="utf-8")
    for contract_id, schema_name in PROMOTED_CONTRACTS.items():
        schema_path = SPEC / schema_name
        if not schema_path.is_file():
            errors.append(f"missing schema for promoted contract {contract_id}: {schema_name}")
            continue
        try:
            schema = load_json(schema_path)
            Draft202012Validator.check_schema(schema)
            validators[contract_id] = Draft202012Validator(schema)
        except Exception as exc:
            errors.append(f"invalid schema {schema_name}: {exc}")
            continue
        if not contains_const(schema, contract_id):
            errors.append(f"{schema_name} does not define promoted identifier {contract_id}")
        if contract_id not in promoted_spec:
            errors.append(
                f"PROMOTED-CONTRACTS.md does not document promoted identifier {contract_id}"
            )

    required = set(PROMOTED_CONTRACTS)
    if set(validators) != required:
        missing = sorted(required - set(validators))
        if missing:
            errors.append(f"promoted contract validators unavailable: {missing}")

    if not errors:
        evaluation_request = load_json(EXAMPLES / "evaluation-request.json")
        bundle = load_json(EXAMPLES / "evidence-bundle.manifest.json")
        verification = load_json(EXAMPLES / "evidence-bundle-verification.json")
        decision = load_json(EXAMPLES / "allow.decision.json")

        errors += validation_errors(
            evaluation_request,
            validators["anthesis.evaluation-request/v1"],
            "evaluation-request.json",
        )
        errors += validation_errors(
            evaluation_request["request_binding"],
            validators["anthesis.request-binding/v1"],
            "evaluation-request.json:request_binding",
        )
        errors += validation_errors(
            bundle,
            validators["anthesis.evidence-bundle/v1"],
            "evidence-bundle.manifest.json",
        )
        errors += validation_errors(
            verification,
            validators["anthesis.evidence-bundle-verification/v1"],
            "evidence-bundle-verification.json",
        )

        if evaluation_request["scenario_id"] != decision["scenario_id"]:
            errors.append("evaluation request scenario_id must match allow.decision.json")
        if evaluation_request["policy"] != decision["policy"]:
            errors.append("evaluation request policy must match allow.decision.json")
        if evaluation_request["effect"] != decision["effect"]:
            errors.append("evaluation request effect must match allow.decision.json")
        if evaluation_request["request_binding"] != {
            key: value
            for key, value in decision["request_binding"].items()
            if key != "request_digest"
        }:
            errors.append("evaluation request binding must match the bound decision inputs")

        entries = {entry["path"]: entry for entry in bundle["entries"]}
        decision_entry = entries.get(bundle["decision_path"])
        report_entry = entries.get(bundle["report_path"])
        if not decision_entry or decision_entry.get("role") != "decision":
            errors.append("evidence bundle decision_path must identify a decision entry")
        if not report_entry or report_entry.get("role") != "report":
            errors.append("evidence bundle report_path must identify a report entry")
        reports_on = [
            link
            for link in bundle["links"]
            if link["relation"] == "reports_on"
            and link["source_path"] == bundle["report_path"]
            and link["target_path"] == bundle["decision_path"]
        ]
        if len(reports_on) != 1:
            errors.append("evidence bundle must contain one report-to-decision reports_on link")
        elif decision_entry and reports_on[0]["target_sha256"] != decision_entry["sha256"]:
            errors.append("reports_on target digest must match the decision entry digest")

        for field in (
            "bundle_id",
            "run_id",
            "replayability_class",
            "comparison_strategy",
        ):
            if verification[field] != bundle[field]:
                errors.append(f"verification {field} must match the bundle manifest")
        if verification["verified_entries"] != len(bundle["entries"]):
            errors.append("verification example must report every bundle entry verified")
        if verification["verified_links"] != len(bundle["links"]):
            errors.append("verification example must report every bundle link verified")
        if not verification["passed"] or verification["findings"]:
            errors.append("successful verification example must pass with no findings")

        obsolete = copy.deepcopy(evaluation_request["request_binding"])
        obsolete["action_input_digest"] = obsolete.pop("input_digest")
        if validators["anthesis.request-binding/v1"].is_valid(obsolete):
            errors.append(
                "request-binding schema must reject obsolete action_input_digest spelling"
            )

    if errors:
        print("Promoted governance contract validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        "Validated 8 promoted contract schemas, evaluation-request identity, "
        "evidence-bundle linkage, verification output, and request-binding compatibility."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
