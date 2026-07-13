# Trial Criteria

A trial should prove the core invariant:

> Every externally observable agentic effect is authorized, constrained, attributable, and auditable through Anthesis.

## Required Checks

1. No governed effect occurs without Anthesis authorization.
2. Every governed action has a policy decision.
3. Every governed action is attributable to supervisor, specialist, tool, capability, approval, timestamp, envelope, and evidence.
4. Capabilities are least privilege and deny out-of-scope actions.
5. Human approval gates block actions before approval and permit only approved scope after approval.
6. Decisions and effects are replayable or auditable from envelope/evidence records.
7. Bypass assumptions are explicit for the selected integration mode.

## Bypass Assumptions To State

- Tool wrapper: agent registry exposes only `anthesis.invoke` or Anthesis-scoped wrappers.
- MCP mediation: MCP client registry exposes only Anthesis.
- Gateway/sidecar: downstream network/API access is blocked except through Anthesis.
- Capability tokens: downstream tools reject calls without Anthesis-issued grants.
- SDK wrapper: direct clients and raw credentials are blocked or the mode is explicitly advisory.
- Sandboxed runtime: filesystem, network, process, and credential effects are blocked except through Anthesis-controlled paths.
