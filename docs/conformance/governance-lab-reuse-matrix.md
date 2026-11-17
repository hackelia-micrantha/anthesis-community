# Governance Lab reuse and coverage gaps for proposed agent authorization conformance

**Status:** discussion-stage traceability only · 2026-11-06  
**Upstream baseline:** [Governance Lab contract](../../specs/governance-lab/README.md), [canonical vectors](../../specs/governance-lab/conformance-vectors.yaml) and [bounded reference trial](../product/try-anthesis.md).

This matrix documents what existing public material could seed a new suite. A matching policy decision **does not** establish runtime mediation, state invariance, revocation fencing, or receipt provenance. No row is evidence of passing the proposed RFC.

| Proposed case | Candidate existing public fixture or trial | Reusable contract | Gap and next fixture |
| --- | --- | --- | --- |
| AUTH-001 / AUTH-001-D | `01-allowed-docs-edit`; bounded reference-trial allowed write | Decision allow and scoped file.write; constrained writer trial | Independent sink receipt and cross-implementation positive execution |
| AUTH-002 / AUTH-002-D | `06-fail-unknown-runtime` | **Weak conceptual analogy only:** unknown runtime rejection is not authenticated actor/tenant impersonation | Trusted actor/tenant provenance and explicit cross-actor confused-deputy attempt |
| AUTH-003 / AUTH-003-D | `02-block-ci-change`, `04-block-secret-access`; reference-trial out-of-scope path | Scope / policy-rule decisions, some constrained-path denial | Exact effect digest/argument swap and actual sink non-mutation under substitution |
| AUTH-004 / AUTH-004-D | Canonical policy digest and rule-order semantics | Decision bound to an identified policy bundle | Two policy generations and mid-flight stale-policy denial at effect time |
| AUTH-005 | No canonical v1 authority epoch fixture | None asserted | Owned effect-sink epoch revocation and stale admission |
| AUTH-006 | Request-binding/evidence public contracts | Request correlation and digest modeling, not idempotency enforcement | Atomic duplicate-effect admission with bounded idempotency window |
| AUTH-007 | No canonical concurrency fence fixture | None asserted | Controlled two-order revocation/effect linearization at owned sink |
| AUTH-008 | No canonical crash-recovery effect fixture | None asserted | Indeterminate durable state and no blind replay after crash |
| AUTH-009 | Reference trial raw writer not registered | Concrete bypass denial within intentionally restricted registry | Independent runtime alternate path and credentials inventory; proof on actual effect state |
| AUTH-010 | `07-block-evidence-tamper`; promoted bundle verification | **Weak conceptual analogy only:** evidence-path write protection is not detached receipt authenticity, substitution or semantic verification | Signed/mismatched receipt subject, source, observation and false-claim negative controls |

## Decision-only projection constraints

`AUTH-001-D` through `AUTH-004-D`, plus `AUTH-010-D` (decision-evidence substitution), compare deterministic decisions for corresponding stimuli. The canonical Governance Lab `decision=deny` or `approval_required` outcome cannot be converted into proof of a denied *external* side effect. In particular, the existing `02-block-ci-change` fixture is **approval required**, not hard denial; its relevance to AUTH-003 is policy-scope modeling, not an exact expected-answer match.

The current canonical set contains seven scenarios (`01` through `07`), including allow, approval-required and deny. `AUTH-002` and `AUTH-010` require new independent fixtures; neither `06` nor `07` is a passing seed for the target predicate. Existing evidence and contract verification are useful test infrastructure, but do not automatically implement the proposed `-D` inputs or any owned-sink tests.

## Promotion protocol

1. Reference actual canonical fixture IDs and semantic expectations. Keep existing accepted contracts unchanged.
2. Create **new** synthetic fixtures when trust boundaries or required observations differ.
3. Pin fixture/contract revision and record behavior under a defined profile version.
4. Run negative controls against independent effect observations, not only evaluator output.
5. Publish `NOT_RUN` for all proposed scenarios until a real, verified test receipt is available.
6. Obtain license and rights review before copying any vectors into an external LF-hosted repository.

## External collaboration

This mapping is advisory input to OpenSSF/SAF-MCP discussion, not an adopted standard or a claim of Linux Foundation affiliation. The conformance suite must admit independent policy engines and enforcement mechanisms.

## Execution harness requirements (not yet implemented)

A runnable qualification harness needs a transactional owned-sink emulator with independently readable snapshots and epoch fencing; a barrier-controlled revoke/commit coordinator (both orderings, no sleep-based assertions); a duplicate dispatcher and bounded idempotency window; named crash failpoints and reconciliation; two actor/two tenant trusted identity fixtures; two policy generations; a raw credential/network/filesystem/tool bypass inventory; and detached receipt/source/target mismatch and false-but-signed-claim controls. Every fixture must bind a qualification cohort, declared mutation, fixture digest and observation authority. These are **acceptance criteria for future executable fixtures**, not tests this documentation has run.
