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
    if not re.fullmatch(r"AUTH-(?:00[1-9]|010)(?:-D)?", r["scenario_id"]):
        raise ValueError("unknown scenario")
    if not isinstance(r["verification"], list) or not isinstance(r["effect_observation_refs"], list):
        raise ValueError("invalid evidence collection")
    if not all(isinstance(ref, str) and ref for ref in r["effect_observation_refs"]):
        raise ValueError("invalid effect observation reference")
    for v in r["verification"]:
        if not isinstance(v, dict) or not all(v.get(k) for k in ("claim", "status", "verifier", "trust_policy_digest", "evidence_refs")):
            raise ValueError("unbound verification")
        if v["status"] not in ("valid", "invalid", "insufficient", "not_evaluated"):
            raise ValueError("unknown verification status")
        if not isinstance(v["evidence_refs"], list) or not all(
            isinstance(ref, str) and ref for ref in v["evidence_refs"]
        ):
            raise ValueError("invalid verification reference")
    if r["scenario_result"] == "PASS":
        # Only count claims bound to the declared observer and trust policy.
        def verified(claim, observation_refs=None):
            return any(
                v["status"] == "valid" and v["claim"] == claim
                and v["verifier"] == r["observation_authority"]
                and v["trust_policy_digest"] == r["trust_policy_digest"]
                and (observation_refs is None or all(ref in v["evidence_refs"] for ref in observation_refs))
                for v in r["verification"]
            )

        # These scenarios require hard denial before dispatch, not merely a
        # self-reported PASS. Decision projections do not assert effects.
        if r["scenario_id"] in ("AUTH-002", "AUTH-003", "AUTH-004", "AUTH-002-D", "AUTH-003-D", "AUTH-004-D"):
            if r["decision_result"] != "deny":
                raise ValueError("negative decision must deny")
            if r["profile"] != "decision-only" and (
                r["admission_result"] != "deny"
                or r["dispatch_state"] != "not_dispatched"
                or r["effect_state"] != "unchanged"
            ):
                raise ValueError("negative control must deny before effect")
        if r["scenario_id"] == "AUTH-005" and (
            r["admission_result"] != "deny" or r["effect_state"] != "unchanged"
        ):
            raise ValueError("stale authority must deny at sink")
        if r["scenario_id"] == "AUTH-009" and (
            r["admission_result"] == "admit"
            or r["dispatch_state"] != "not_dispatched"
            or r["effect_state"] != "unchanged"
        ):
            raise ValueError("bypass control must block effect")

        if r["scenario_id"] in ("AUTH-001", "AUTH-001-D"):
            if r["decision_result"] != "allow":
                raise ValueError("positive control must allow")
            if r["profile"] != "decision-only" and (
                r["admission_result"] != "admit"
                or r["dispatch_state"] != "dispatched"
                or r["effect_state"] != "committed"
            ):
                raise ValueError("positive control must commit the allowed effect")
        if r["admission_result"] == "admit" and r["decision_result"] != "allow":
            raise ValueError("unresolved or denied admission")
        if r["effect_state"] in ("committed", "partially_committed") and r["admission_result"] == "deny":
            raise ValueError("forbidden effect")
        if r["profile"] == "decision-only":
            if not verified("decision_binding"):
                raise ValueError("no bound decision verification")
        else:
            if r["effect_state"] in ("not_observed", "unknown") or not r["effect_observation_refs"]:
                raise ValueError("no independent effect observation")
            if not verified("effect_" + r["effect_state"], r["effect_observation_refs"]):
                raise ValueError("no matching bound effect verification")
    return True


def qualification(profile, records):
    if profile not in SETS:
        return "NOT_QUALIFIED"
    required = set(SETS[profile])
    if any(not isinstance(r, dict) or "scenario_id" not in r for r in records):
        return "NOT_QUALIFIED"
    if len(records) != len({r["scenario_id"] for r in records}):
        return "NOT_QUALIFIED"
    cohort_keys = ("implementation_digest", "profile_manifest_digest", "trust_policy_digest", "authority_configuration_digest", "environment_digest")
    cohort = None
    for r in records:
        if r.get("profile") != profile:
            return "NOT_QUALIFIED"
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
        verification=[dict(claim="decision_binding" if decision_only else ("effect_committed" if sid == "AUTH-001" else "effect_unchanged"),status="valid",verifier="test-observer",trust_policy_digest=DIGEST,evidence_refs=["snapshot"])])


class ContractTests(unittest.TestCase):
    def test_valid_scenario_ids(self):
        for sid in ("AUTH-001", "AUTH-010", "AUTH-010-D"):
            self.assertTrue(validate_record(record("decision-only" if sid.endswith("-D") else "mediated-dispatch", sid)))
        with self.assertRaises(ValueError):
            validate_record(record("mediated-dispatch", "AUTH-0001"))

    def test_manifest_exact_sets(self):
        self.assertEqual(len(SETS), 3)
        self.assertIn("AUTH-010-D", SETS["decision-only"])
        self.assertIn("AUTH-009", SETS["owned-effect-sink"])

    def test_qualifying_synthetic_cohorts(self):
        for profile, ids in SETS.items():
            records = [record(profile, x) for x in ids]
            self.assertEqual(qualification(profile, records), "QUALIFIED")
            records[0]["trust_policy_digest"] = "sha256:changed"
            self.assertEqual(qualification(profile, records), "NOT_QUALIFIED")

    def test_deny_all_positive_control(self):
        p = "mediated-dispatch"
        records = [record(p, x) for x in SETS[p]]
        records[0]["scenario_result"] = "FAIL"
        self.assertEqual(qualification(p, records), "NOT_QUALIFIED")

    def test_pass_label_does_not_qualify_deny_all_or_wrong_profile(self):
        for profile, ids in SETS.items():
            with self.subTest(profile=profile):
                records = [record(profile, sid) for sid in ids]
                records[0]["decision_result"] = "deny"
                if profile != "decision-only":
                    records[0].update(admission_result="deny", dispatch_state="not_dispatched", effect_state="unchanged")
                    records[0]["verification"][0]["claim"] = "effect_unchanged"
                self.assertEqual(qualification(profile, records), "NOT_QUALIFIED")
        p = "mediated-dispatch"
        records = [record("owned-effect-sink", sid) for sid in SETS[p]]
        self.assertEqual(qualification(p, records), "NOT_QUALIFIED")

    def test_negative_controls_reject_false_pass(self):
        for profile, ids in SETS.items():
            for sid in ids:
                if sid not in ("AUTH-002", "AUTH-003", "AUTH-004", "AUTH-002-D", "AUTH-003-D", "AUTH-004-D", "AUTH-005", "AUTH-009"):
                    continue
                with self.subTest(profile=profile, sid=sid):
                    records = [record(profile, x) for x in ids]
                    r = next(r for r in records if r["scenario_id"] == sid)
                    r["decision_result"] = "allow"
                    if profile != "decision-only":
                        r.update(admission_result="admit", dispatch_state="dispatched", effect_state="committed")
                        r["verification"][0]["claim"] = "effect_committed"
                    self.assertEqual(qualification(profile, records), "NOT_QUALIFIED")
                    r["scenario_result"] = "FAIL"
                    self.assertTrue(validate_record(r))

    def test_effect_claim_must_match_observation_and_binding(self):
        p = "mediated-dispatch"
        for field, value in (
            ("claim", "effect_committed"),
            ("claim", "effect_arbitrary"),
            ("status", "invalid"),
            ("verifier", "different-observer"),
            ("trust_policy_digest", "sha256:other"),
            ("evidence_refs", ["different-snapshot"]),
            ("evidence_refs", "snapshot"),
        ):
            with self.subTest(field=field, value=value):
                records = [record(p, x) for x in SETS[p]]
                r = next(r for r in records if r["scenario_id"] == "AUTH-002")
                r["verification"][0][field] = value
                self.assertEqual(qualification(p, records), "NOT_QUALIFIED")

    def test_decision_projection_requires_bound_verification(self):
        p = "decision-only"
        for sid in SETS[p]:
            for evidence in (
                [],
                [dict(claim="decision_binding", status="invalid", verifier="test-observer",
                      trust_policy_digest=DIGEST, evidence_refs=["snapshot"])],
                [dict(claim="effect_unchanged", status="valid", verifier="test-observer",
                      trust_policy_digest=DIGEST, evidence_refs=["snapshot"])],
                [dict(claim="decision_binding", status="valid", verifier="different-observer",
                      trust_policy_digest=DIGEST, evidence_refs=["snapshot"])],
            ):
                with self.subTest(sid=sid, evidence=evidence):
                    records = [record(p, x) for x in SETS[p]]
                    next(r for r in records if r["scenario_id"] == sid)["verification"] = evidence
                    self.assertEqual(qualification(p, records), "NOT_QUALIFIED")

    def test_missing_and_inconclusive_required(self):
        p = "decision-only"
        rs = [record(p, x) for x in SETS[p]]
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
        self.assertEqual(hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest(), expected["git_blob_sha1"])
        for fid in expected["fixture_ids"]:
            self.assertIn("id: " + fid, raw.decode())
        self.assertEqual(len(re.findall(r"(?m)^    id: ", raw.decode())), len(expected["fixture_ids"]))


if __name__ == "__main__":
    unittest.main()
