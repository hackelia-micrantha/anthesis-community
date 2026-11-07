# Independent desk-review remediation — PR #48

**Source:** independent technical desk review of head `c104b45c67e067e823cff74f6d97a94c7002c312` (6 November 2026). **This is a tracking record, not an independent implementation, security certification or reviewer sign-off.**

## Addressed in draft documentation

- [x] Separate decision, admission, mediated dispatch, target effect and claim-scoped verification.
- [x] Add `not_observed`, `unchanged`, `partially_committed`; remove overloaded process `failed` from effect state.
- [x] Represent denied-but-committed bypass and unobserved dispatch as valid security-failure records.
- [x] Forbid direct admission from `approval_required`, `escalate` and `indeterminate` without bound terminal resolution.
- [x] Bind positive/negative scenarios to one qualification cohort with explicit mutation rules.
- [x] Add mandatory evidence substitution (`AUTH-010` / `AUTH-010-D`), policy freshness (`AUTH-004`) and bypass inventory (`AUTH-009`) where applicable.
- [x] Make replay and crash recovery separately qualified extensions.
- [x] Narrow Governance Lab `06` and `07` reuse to conceptual analogies and document the missing independent effect harness.
- [x] Add **draft** JSON Schemas for manifests and result records; no claim of execution or complete semantic validation.

## Still open — not markable complete by documentation alone

- [x] Add a draft PR workflow for JSON parsing and synthetic state-model/cohort/qualification tests; **workflow execution not yet verified**. These are not complete JSON Schema validation or independent conformance tests.
- [ ] Run and verify exact-head CI; add a full JSON Schema validator, complete negative-control matrix and independent semantic evidence checks.
- [ ] Build and **run** owned-sink, deterministic race, replay, crash/reconciliation, two-tenant identity, policy-version and bypass/evidence negative fixtures.
- [x] Pin the current Governance Lab canonical vector by Git blob SHA and assert all seven fixture IDs in the synthetic contract test.
- [ ] Run fixture traceability CI and execute real Governance Lab vectors against an independent implementation.
- [ ] Update workflow actions to verified Node-24-compatible immutable revisions and deliberately pin the runner image; verify against an actual workflow run.
- [ ] Resolve ownership, third-party provenance, recipient governance and **rights-holder-approved** path-based SPDX/license split. Candidate: Apache-2.0 for software/executable fixtures, CC-BY-4.0 for explanatory docs, Community-Spec-1.0 for an adopted formal specification **only if recipient governance chooses it**.
- [ ] Obtain a separate human security-semantics review and an independent non-Anthesis implementation/interoperability review.
- [ ] Obtain human authorization before upstream redistribution or OpenSSF outreach.

## Release gate

Publication CI success is not conformance success. Until the open items have independently verifiable receipts, keep PR #48 **draft**, keep all proposed scenario outcomes `NOT_RUN`, and describe the RFC as **discussion-ready but not qualification-ready**. No LF/OpenSSF adoption or sponsorship is implied.
