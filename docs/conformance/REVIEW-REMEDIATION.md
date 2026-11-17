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

## Discussion-draft merge gate

- [x] Add draft CI for JSON parsing, synthetic state-model/cohort checks and pinned fixture traceability. Earlier head `761f3a8` passed both workflows; those receipts are historical, not validation of subsequent edits.
- [ ] Verify exact-head draft CI and independent technical review of the final proposal and synthetic checks.
- [ ] Obtain explicit merge authorization for the discussion draft.

Keep the RFC non-normative and all proposed real scenario outcomes `NOT_RUN`. Synthetic results are bookkeeping checks, not implementation qualification. Merging a discussion draft does not authorize upstream redistribution or representation as an adopted standard.

## Future implementation qualification (not a discussion-draft merge prerequisite)

- [ ] Add full JSON Schema validation, complete negative-control matrix and independent semantic evidence checks.
- [ ] Build and run owned-sink, deterministic race, replay, crash/reconciliation, two-tenant identity, policy-version and bypass/evidence negative fixtures.
- [x] Pin the current Governance Lab canonical vector by Git blob SHA and assert all seven fixture IDs in the synthetic contract test.
- [ ] Execute real Governance Lab vectors against an independent implementation.
- [ ] Update workflow actions to verified Node-24-compatible immutable revisions and deliberately pin the runner image; verify against an actual workflow run.
- [ ] Obtain a separate human security-semantics review and independent non-Anthesis implementation/interoperability review before claiming qualification.

## Upstream contribution gate

- [ ] Resolve ownership, third-party provenance, recipient governance and rights-holder-approved path-based SPDX/license split. See [license decision gate](CONTRIBUTION-LICENSE-GATE.md).
- [ ] Obtain human authorization before upstream redistribution or OpenSSF outreach.

Publication CI success is not conformance success. No LF/OpenSSF adoption or sponsorship is implied.
