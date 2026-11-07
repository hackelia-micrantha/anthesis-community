#!/usr/bin/env python3
"""Draft conformance contract self-tests; synthetic fixtures, not implementation certification."""
import hashlib
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/conformance/schema"
MANIFEST = json.loads((BASE / "profile-manifest.schema.json").read_text())
RESULT = json.loads((BASE / "scenario-result.schema.json").read_text())
SETS = {clause["if"]["properties"]["profile"]["const"]: clause["then"]["properties"]["required_scenarios"]["const"] for clause in MANIFEST["allOf"]}
DIGEST = "sha256:" + "0" * 64


def validate_record(r):
    """Semantic checks layered on top of candidate JSON schema; no third-party dependencies."""
    for k in RESULT["required"]:
        if k not in r:
            raise ValueError("missing " + k)
    for k, v in r.items():
        if k not in RESULT["properties"]:
            raise ValueError("unknown " + k)
        p = RESULT["properties"][k]
        if "enum" in p and v not in p["enum"]:
            raise ValueError("invalid " + k)
        if "const" in p and v != p["const"]:
            raise ValueError("invalid " + k)
    if r["profile"] == "decision-only":
        if not r["scenario_id"].endswith("-D") or r["dispatch_state"] != "not_observed" or r["effect_state"] != "not_observed":
            raise ValueError("decision-only must not claim effect observation")
    elif r["scenario_id"].endswith("-D"):
        raise ValueError("decision projection in execution profile")
    if not re.fullmatch(r"AUTH-0(?:0[1-9]|10)(?:-D)?", r["scenario_id"]):
        raise ValueError("unknown scenario")
    if not isinstance(r["verification"], list) or not isinstance(r["effect_observation_refs"], list):
        raise ValueError("invalid evidence collection")
    for v in r["verification"]:
        if not isinstance(v, dict) or not all(v.get(k) for k in ("claim", "status", "verifier", "trust_policy_digest", "evidence_refs")):
            raise ValueError("unbound verification")
        if v["status"] not in ("valid", "invalid", "insufficient", "not_evaluated"):
            raise ValueError("unknown verification status")
    if r["scenario_result"] == "PASS":
        if r["admission_result"] == "admit" and r["decision_result"] != "allow":
            raise ValueError("unresolved or denied admission")
        if r["effect_state"] in ("committed", "partially_committed") and r["admission_result"] == "deny":
            raise ValueError("forbidden effect")
        if r["profile"] != "decision-only":
            if r["effect_state"] in ("not_observed", "unknown") or not r["effect_observation_refs"]:
                raise ValueError("no independent effect observation")
            if not any(v["status"] == "valid" and v["claim"].startswith("effect_") for v in r["verification"]):
                raise ValueError("no effect verification")
    return True


def qualification(profile, records):
    if profile not in SETS:
        return "NOT_QUALIFIED"
    required = {"AUTH-" + x for x in SETS[profile]}
    if len(records) != len({r["scenario_id"] for r in records}):
        return "NOT_QUALIFIED"
    cohort_keys = ("implementation_digest", "profile_manifest_digest", "trust_policy_digest", "authority_configuration_digest", "environment_digest")
    cohort = None
    for r in records:
        try:
            validate_record(r)
        except (ValueError, TypeError):
            return "NOT_QUALIFIED"
        current = tuple(r[k] for k in cohort_keys)
        if cohort is None:
            cohort = current
        if cohort != current:
            return "NOT_QUALIFIED"
    return "QUALIFIED" if all(any(r["scenario_id"] == sid and r["scenario_result"] == "PASS" for r in records) for sid in required) else "NOT_QUALIFIED"


def record(profile, sid, result="PASS", effect=None):
    decision_only = profile == "decision-only"
    effect = effect or ("not_observed" if decision_only else "unchanged")
    return dict(profile=profile, profile_version="agent-tool-auth-conformance/profile-v0", scenario_id=sid,
        scenario_result=result, implementation_digest=DIGEST, profile_manifest_digest=DIGEST,
        trust_policy_digest=DIGEST, authority_configuration_digest=DIGEST, environment_digest=DIGEST,
        fixture_digest=DIGEST, source_revision="test-revision", request_digest=DIGEST,
        operation_digest=DIGEST, target_digest=DIGEST, trusted_actor_ref="actor-A",
        identity_source="test-broker", observation_authority="test-observer",
        decision_result="allow" if sid.endswith("001") or sid.endswith("001-D") else "deny",
        admission_result="not_evaluated" if decision_only else ("admit" if sid == "AUTH-001" else "deny"),
        dispatch_state="not_observed" if decision_only else ("dispatched" if sid == "AUTH-001" else "not_dispatched"),
        effect_state="committed" if sid == "AUTH-001" else effect,
        effect_observation_refs=[] if decision_only else ["snapshot"],
        verification=[dict(claim="decision_binding" if decision_only else "effect_unchanged",status="valid",verifier="test-observer",trust_policy_digest=DIGEST,evidence_refs=["snapshot"])])


class ContractTests(unittest.TestCase):
    def test_manifest_exact_sets(self):
        self.assertEqual(len(SETS), 3)
        self.assertIn("AUTH-010-D", ["AUTH-" + x for x in SETS["decision-only"]])
        self.assertIn("AUTH-009", ["AUTH-" + x for x in SETS["owned-effect-sink"]])

    def test_qualifying_synthetic_cohorts(self):
        for profile, ids in SETS.items():
            records = [record(profile, "AUTH-" + x) for x in ids]
            self.assertEqual(qualification(profile, records), "QUALIFIED")
            records[0]["trust_policy_digest"] = "sha256:changed"
            self.assertEqual(qualification(profile, records), "NOT_QUALIFIED")

    def test_deny_all_positive_control(self):
        p = "mediated-dispatch"
        records = [record(p, "AUTH-" + x) for x in SETS[p]]
        records[0]["scenario_result"] = "FAIL"
        self.assertEqual(qualification(p, records), "NOT_QUALIFIED")

    def test_missing_and_inconclusive_required(self):
        p = "decision-only"
        rs = [record(p, "AUTH-" + x) for x in SETS[p]]
        self.assertEqual(qualification(p, rs[:-1]), "NOT_QUALIFIED")
        rs[-1]["scenario_result"] = "INCONCLUSIVE"
        self.assertEqual(qualification(p, rs), "NOT_QUALIFIED")
        rs[-1]["scenario_result"] = "NOT_APPLICABLE"
        self.assertEqual(qualification(p, rs), "NOT_QUALIFIED")

    def test_bypass_record_is_representable_but_not_pass(self):
        r = record("owned-effect-sink", "AUTH-009")
        r["effect_state"] = "committed"
        with self.assertRaises(ValueError):
            validate_record(r)
        r["scenario_result"] = "FAIL"
        self.assertTrue(validate_record(r))

    def test_nonterminal_admission_never_passes(self):
        r = record("mediated-dispatch", "AUTH-001")
        r["decision_result"] = "approval_required"
        with self.assertRaises(ValueError):
            validate_record(r)

    def test_no_false_pass_without_observer(self):
        r = record("mediated-dispatch", "AUTH-001")
        r["effect_observation_refs"] = []
        with self.assertRaises(ValueError):
            validate_record(r)

    def test_fixture_traceability_pinned(self):
        path = ROOT / "specs/governance-lab/conformance-vectors.yaml"
        raw = path.read_bytes()
        pinned = (BASE / "governance-lab-pin.json")
        expected = json.loads(pinned.read_text())
        self.assertEqual(hashlib.sha256(raw).hexdigest(), expected["sha256"])
        for fid in expected["fixture_ids"]:
            self.assertIn("id: " + fid, raw.decode())
        self.assertEqual(len(re.findall(r"(?m)^    id: ", raw.decode())), len(expected["fixture_ids"]))


if __name__ == "__main__":
    unittest.main()
