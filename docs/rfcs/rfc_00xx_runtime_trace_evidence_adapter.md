# RFC-00XX: Runtime Trace Evidence Adapter

- Status: Draft
- Area: Evidence, Observability, Governance
- Related: Anthesis execution envelopes, approval gates, audit records, replayability, agent/tool execution

## Summary

Anthesis should support runtime trace evidence as an optional evidence source for governed human and agent execution.

This RFC defines a minimal adapter contract for attaching GenAI runtime traces, including traces produced by tools such as Monocle, to Anthesis execution envelopes. The goal is to let Anthesis consume runtime observability data without becoming an observability framework itself.

## Motivation

Anthesis is Git-native and governance-first. It anchors policy, prompts, tasks, RFCs, approvals, and execution state to version-controlled artifacts and reviewable workflow transitions.

Agent execution also produces runtime behavior that is not fully represented by Git alone:

- model calls
- tool calls
- retrieval steps
- agent handoffs
- prompt and response metadata
- failures, retries, and fallback paths
- latency, token, and provider behavior

Runtime traces can help explain what actually happened during execution. They are useful for debugging, replay analysis, audit review, and drift detection.

Tools such as Monocle can produce GenAI-aware traces and export them through OpenTelemetry-compatible or artifact-oriented paths. Anthesis should be able to bind those traces to its own governance records.

## Design Principle

Anthesis owns governance semantics.

Trace systems own runtime instrumentation.

The adapter binds runtime trace artifacts to Anthesis evidence requirements.

```text
Anthesis does not need to become Monocle.
Monocle does not need to become Git-native governance.
The integration point is evidence binding.
```

## Goals

- Define a generic `runtime_trace` evidence type.
- Allow Monocle traces to be attached as a first supported adapter shape.
- Bind trace evidence to Git-native context.
- Bind trace evidence to Anthesis execution envelopes.
- Preserve redaction, retention, and integrity requirements.
- Keep runtime tracing optional and replaceable.

## Non-Goals

- Standardize all GenAI tracing.
- Replace OpenTelemetry.
- Require Monocle as a core Anthesis dependency.
- Build an observability backend.
- Store all prompt, response, or tool payloads by default.
- Treat runtime traces as sufficient governance records on their own.

## Evidence Contract

A runtime trace evidence record should include at minimum:

```yaml
trace_evidence:
  type: runtime_trace
  provider: monocle
  trace_id: "trace-123"
  artifact_uri: "evidence/traces/trace-123.json"
  captured_at: "2026-06-14T00:00:00Z"
  digest:
    algorithm: sha256
    value: "..."

  git:
    repository: "hackelia-micrantha/anthesis-community"
    branch: "feature/example"
    commit: "abc123"
    pull_request: 42

  anthesis:
    envelope_id: "env-123"
    actor_id: "agent:worker-xylem"
    policy_version: "policy-2026-06-14"
    approval_state: "approved"
    risk_tier: "review-required"

  controls:
    redaction_profile: "default-agent-trace-redaction"
    retention_class: "project-evidence"
    integrity_mode: "digest-bound-artifact"
```

The `provider` field is intentionally separate from `type`. Monocle is one possible provider. Other future providers could include raw OpenTelemetry exports, custom Anthesis workers, CI-side trace emitters, or vendor-specific trace systems.

## Required Bindings

Runtime trace evidence is not considered review-grade Anthesis evidence unless it is bound to:

- execution envelope ID
- actor identity
- repository identity
- commit SHA
- policy version
- approval state
- artifact digest
- redaction profile
- retention class

This binding prevents traces from becoming detached debug logs with unclear provenance.

## Trace Artifact Handling

Trace artifacts may be stored in one of several locations:

- committed evidence fixtures for tests and examples
- CI artifacts
- object storage
- local development evidence directories
- OpenTelemetry collector destinations
- external observability systems

Anthesis should avoid requiring one storage backend at the RFC level.

The envelope should store enough metadata to locate, verify, and classify the trace artifact.

## Redaction Requirements

Runtime traces can contain sensitive information, including prompts, model responses, retrieved context, tool arguments, URLs, file paths, user data, and internal architecture details.

An adapter must support an explicit redaction profile. The profile should define what is retained, hashed, summarized, or removed.

Recommended default posture:

```yaml
redaction_profile:
  prompts: summarize_or_hash
  responses: summarize_or_hash
  tool_arguments: allowlist_fields
  retrieved_documents: metadata_only
  sensitive_values: remove
  environment: allowlist_fields
```

## Retention Requirements

Trace retention should follow risk and evidence class:

| Retention class | Intended use | Suggested handling |
| --- | --- | --- |
| `debug` | Local troubleshooting | Short-lived, non-authoritative |
| `ci-evidence` | CI validation | Retained with CI artifacts |
| `project-evidence` | Review and replay | Bound to envelope and digest |
| `audit-evidence` | Compliance/security review | Stronger retention and access controls |

The adapter must not silently upgrade debug traces into audit evidence without classification and redaction.

## Integrity

At minimum, Anthesis should record a digest of the trace artifact.

For higher-risk workflows, Anthesis may require signed artifact manifests, append-only evidence logs, signed envelope records, CI attestation, object storage immutability, or repository-bound evidence manifests.

This RFC does not require one integrity mechanism, but it requires the trace evidence record to state which mechanism was used.

## Validation

An Anthesis implementation should validate:

- required fields are present
- referenced commit exists
- envelope ID exists
- actor ID is known or explicitly external
- policy version is resolvable
- approval state is valid for the risk tier
- artifact digest matches the stored artifact, where accessible
- redaction profile is known
- retention class is allowed for the workflow

## Failure Modes

| Failure | Required behavior |
| --- | --- |
| Trace missing | Mark evidence incomplete unless trace is optional |
| Trace digest mismatch | Fail validation for review-grade evidence |
| Unknown actor | Require explicit external actor classification |
| Unknown policy version | Fail governance binding |
| Overexposed sensitive data | Quarantine or reject according to policy |
| External trace backend unavailable | Preserve envelope metadata and mark retrieval unavailable |

## Security Considerations

Runtime trace evidence increases visibility but also increases data exposure risk.

Threats include prompt or retrieved-context leakage, tool argument leakage, accidental sensitive-value capture, trace tampering, detached traces being reused out of context, incomplete traces being treated as full audit records, and provider lock-in through provider-specific trace semantics.

Anthesis should treat traces as sensitive evidence artifacts, not generic logs.

## Monocle Adapter Notes

Monocle is a useful initial adapter candidate because it focuses on GenAI application and agent instrumentation and can emit trace-like records suitable for analysis.

Anthesis should not depend directly on Monocle-specific internals. Instead, it should define a provider mapping:

```yaml
provider_mapping:
  provider: monocle
  trace_id: $.trace_id
  spans: $.spans
  model_calls: $.spans[?type == "model"]
  tool_calls: $.spans[?type == "tool"]
  retrieval_calls: $.spans[?type == "retrieval"]
```

The exact field paths should be implementation-specific and tested against real exported traces.

## Open Questions

- What Monocle export format should Anthesis treat as the first supported artifact shape?
- Should Anthesis store trace summaries in Git and full traces outside Git?
- Which fields should be mandatory for audit-grade trace evidence?
- Should trace redaction happen before export, during ingestion, or both?
- Should runtime trace validation run in CI, pre-PR, post-merge, or all three?
- How should Anthesis represent partial traces or failed instrumentation?

## Recommendation

Adopt `runtime_trace` as a generic optional evidence type.

Use Monocle as the first planning target for a GenAI runtime trace provider, but keep Anthesis provider-neutral.

The important boundary is:

```text
Trace evidence explains runtime behavior.
Anthesis governance explains why the behavior was allowed, reviewed, and preserved.
```
