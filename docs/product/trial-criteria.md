# Trial Criteria

An Anthesis trial should answer one practical question:

> Does the selected integration make consequential agentic effects authorized, constrained, attributable, auditable, and difficult to bypass in the way the trial claims?

The public Governance Lab is useful for validating deterministic evaluator behavior, but a production-oriented trial must also evaluate the surrounding enforcement boundary.

## Six assurance dimensions

### 1. Enforceability

- No governed effect occurs without the selected Anthesis authorization boundary.
- The trial identifies the concrete enforcement point: tool registry, MCP mediation, gateway, downstream capability validator, credential boundary, sandbox, or equivalent.
- Advisory integrations are labeled advisory rather than presented as non-bypassable enforcement.

### 2. Attribution

Every governed action should be attributable to the relevant:

- supervisor and/or specialist;
- runtime identity;
- tool or service;
- policy decision and reason;
- capability or grant;
- human approval when required;
- timestamp and execution envelope;
- resulting evidence and outcome.

### 3. Least privilege

- Capabilities are narrowly scoped to the requested effect.
- Out-of-scope paths, tools, services, arguments, credentials, or time windows are denied.
- Approval does not silently broaden the original capability.

### 4. Human approval

- Actions requiring approval remain blocked before approval.
- Approval is bound to the exact requested scope rather than a generic future permission.
- Rejected, expired, altered, or replayed approval material does not authorize execution.

### 5. Auditability

- Decisions, approvals, execution, and outcomes produce sufficient evidence to reconstruct what happened.
- Evidence identifies the verification level honestly; deterministic replay is not claimed when only semantic or governance-level verification is available.
- Material evidence mutation or re-verification does not erase the original record.

### 6. Bypass resistance

- Direct effect paths are enumerated and tested for the selected integration mode.
- Residual bypass paths and trusted components are documented explicitly.
- A successful trial distinguishes between evaluator correctness and runtime non-bypassability.

## Required trial checks

1. Every governed action has a policy decision before the selected effect boundary permits execution.
2. Allowed, approval-required, and denied outcomes are attributable to stable policy/default/engine semantics.
3. Least-privilege constraints deny deliberately out-of-scope variants of otherwise permitted actions.
4. Approval-required effects cannot execute before exact approval and cannot exceed approved scope afterward.
5. Evidence is sufficient to associate the request, decision, executor, approval/capability, and resulting outcome.
6. At least one controlled drift or tamper case fails closed or produces the documented mismatch signal.
7. Bypass assumptions are tested rather than only stated where the integration environment permits meaningful verification.

## Bypass assumptions to state

- **Tool wrapper:** the agent registry exposes only `anthesis.invoke` or Anthesis-scoped wrappers for governed effects.
- **MCP mediation:** the client registry does not expose raw downstream MCP servers or equivalent direct service paths.
- **Gateway / sidecar:** downstream network/API access is blocked or rejected except through the governed gateway.
- **Capability tokens:** downstream tools reject calls without valid Anthesis-issued grants and validate scope, expiry, replay, and integrity.
- **SDK wrapper:** direct clients and raw credentials are blocked, constrained, or the mode is explicitly labeled advisory.
- **Sandboxed runtime:** filesystem, network, process, credential, and tool effects are unavailable outside governed paths.

## Relationship to Governance Lab

Governance Lab currently exposes three separate public proof surfaces:

- **7 canonical governance scenarios** for stable public conformance;
- **9 packs / 27 general demo scenarios** for broader synthetic governed-action coverage;
- **24 inference-integrity scenarios** for deterministic evaluation of recorded provider-neutral inference evidence.

These establish evaluator and fixture behavior. They do not by themselves establish that a deployed runtime cannot bypass Anthesis. A live trial should therefore score the six assurance dimensions above in the actual target workflow.
