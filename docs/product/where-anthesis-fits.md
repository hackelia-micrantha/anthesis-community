# Where Anthesis fits: portable governance for agent actions

**Product boundary:** Anthesis accepts a normalized proposed effect, evaluates deterministic policy and current authority, expresses approval obligations, and produces a versioned decision and attributable evidence. An external adapter/runtime must enforce the decision at the effect boundary. Anthesis is not a model host, agent orchestrator, filesystem sandbox, or automatic data-residency guarantee.

This document describes architectural use cases and desired integrations, **not** a list of shipped adapters. See [Try Anthesis](try-anthesis.md) for the current executable public reference and [Integration modes](integrations/README.md) for claims and bypass assumptions.

## Mental model

```text
model / agent client
  -> proposed exact action
  -> Anthesis policy + authority + approval decision
  -> enforcing adapter / capability boundary
  -> source of truth (repository, service, database)
  -> attributable outcome and evidence
```

The model may suggest a tool call, but the client or agent runtime executes the call. Routing a request through Anthesis is not enough: the protected resource must be unreachable through any equivalent unmediated path within the claimed enforcement boundary.

## Use case 1: local coding agent on a developer laptop

**Goal:** Allow useful source-code modifications while denying or requiring approval for more sensitive operations, without requiring Dubnium or an external governance service.

A developer might run a model via Ollama on a MacBook while an agent client requests filesystem, shell, Git, or network operations. With a suitable Anthesis-aware agent adapter and appropriately constrained executor, the developer could apply a project policy such as:

- permit selected reads and writes within the working tree;
- require exact-action approval before editing CI configuration, changing dependencies, or pushing a branch;
- deny access to secrets and unapproved destinations;
- record the policy revision, selected action, approval, outcome, and remaining bypass assumptions.

**Integration status:** This is a target workflow. The public reference trial instead exercises an exact repository write using a simulated agent and a constrained tool registry over a disposable Git repository. It does not demonstrate a turnkey MacBook/Ollama agent adapter, a universal host sandbox, or protection against the host user/administrator.

**Enforcement dependency:** Unrestricted direct shell, raw filesystem access, alternate MCP servers, network clients, or inherited credentials can bypass tool-level policy. An OS-specific sandbox or equivalent capability boundary is required before making stronger containment claims. Executable names and permitted commands alone do not bound child processes or arbitrary script execution; symlinks and path replacement also need explicit treatment.

## Use case 2: self-hosted execution with Dubnium

**Goal:** Apply consistent authority to a supervisor/specialist runtime operated on infrastructure under the owner's control.

Dubnium owns inference/runtime execution, process and network restrictions, tool and credential placement, and runtime evidence. Anthesis owns authorization semantics; it consumes the normalized requested effect and returns the decision and obligations. Dubnium is a reference integration, not an Anthesis dependency or policy authority.

See the [public Dubnium governed-agent integration guide](https://github.com/hackelia-micrantha/dubnium-community/blob/main/docs/governed-agent-integration.md).

## Use case 3: existing external agent or business workflow

**Goal:** Govern one consequential operation without replacing an existing agent or process orchestrator.

Choose a concrete effect such as writing a repository file, publishing an artifact, modifying a production configuration, or sending data externally. Add an adapter at an actual enforcement point, enumerate alternate effect paths, and test allow, deny, approval-required, changed-target, stale-approval, and raw-bypass cases. Keep the original platform's identity, policy, and security controls in place.

The [Warden external trial](https://github.com/hackelia-micrantha/anthesis-community/issues/25) is a proposed example, not evidence of successful general interoperability.

## Platform responsibility map

This is a **layer and integration comparison**, not a ranking or a statement that vendor-native governance is absent.

| System | Main role | Relationship to Anthesis |
| --- | --- | --- |
| [Ollama](https://docs.ollama.com/capabilities/tool-calling) | Local model serving and model-generated tool calls. | An agent client or tool executor must integrate Anthesis to govern an effect; model inference by itself does not enforce tool authorization. |
| Anthesis | Exact-effect authorization, approval obligations, decision/evidence semantics. | Portable policy authority; requires a mediated execution boundary. |
| [Dubnium](https://github.com/hackelia-micrantha/dubnium-community/blob/main/docs/governed-agent-integration.md) | Operator-controlled AI runtime and tool execution. | Reference consumer of Anthesis, not part of the core. |
| [Amazon Bedrock / AgentCore](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy-core-concepts.html) | Managed model/agent infrastructure with native gateway policy controls. | Some governance responsibilities overlap; an independent policy contract is useful only when a concrete need and a real enforcement integration are identified. |
| [Amazon SageMaker AI](https://docs.aws.amazon.com/sagemaker/latest/dg/train-model.html) | Model training, ML development, and deployment. | Potential model-lifecycle provider governed at selected operations; not an agent-effect authorization layer by itself. |
| [Microsoft Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/fundamentals-what-is-copilot-studio) | Agent and workflow design/management. | Has native controls; any Anthesis integration must mediate a specific supported effect and respect existing policy boundaries. |
| [UiPath / Maestro](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/overview) | Agent, robot, and human process orchestration. | Existing process governance may be sufficient; an Anthesis adapter could add an independent cross-runtime decision for a specific operation. |
| [Microsoft Power Platform](https://learn.microsoft.com/en-us/power-platform/) | Business apps, workflow automation, agents, and data integration. | Possible source and destination of governed effects, with platform identity, connector, and data controls still in force. |

**Data sovereignty requires more than local authorization.** Local model serving does not establish that an agent client, logging service, remote connector, backup, telemetry exporter, or tool never transmits protected content. Anthesis can specify a handling policy; the runtime and infrastructure must enforce it at actual data and effect boundaries. Policy labels on generated outputs are not a complete substitute for information-flow controls.

## Current proof versus target integrations

| Surface | What can be demonstrated | What must not be inferred |
| --- | --- | --- |
| [Governance Lab](https://github.com/ryjen/anthesis-governance-lab) | Repeatable evaluator contracts and recorded-evidence checks. | Execution of declared production effects, universal sandboxing, or arbitrary runtime non-bypassability. |
| [Public reference trial](try-anthesis.md) | An exact authorized repository write through a constrained tool registry; raw and out-of-scope attempts are blocked in that reference composition. | A released general-purpose Ollama adapter, containment of a hostile local user, or denial of alternate tool paths in other runtimes. |
| [Dubnium integration](https://github.com/hackelia-micrantha/dubnium-community/blob/main/docs/governed-agent-integration.md) | A separate reference composition for governed execution. | A dependency on Dubnium or guarantees about every installation. |
| Other platforms | Candidate integration surfaces or externally evaluated experiments. | Shipped adapters, equivalent native policy guarantees, or proven cross-provider enforceability. |

## Adoption and evaluation

1. Start with the [public reference trial](try-anthesis.md).
2. Select one real, low-risk consequential action in an existing workflow.
3. Enumerate the agent's direct resource, shell, network, tool, and credential paths.
4. Choose and enforce one [integration boundary](integrations/README.md), then test equivalent raw bypasses and changed/stale authorization.
5. Record setup cost, false denies, latency, execution evidence, usability, and residual paths using the [trial criteria](trial-criteria.md).

The durable core should remain independently usable as a CLI with stable stdin/stdout contracts. Optional runtime, MCP, and OS adapters should compose around it. The product's current implementation/release work is tracked in [core architecture issue #237](https://github.com/hackelia-micrantha/anthesis/issues/237), [Rust CLI issue #241](https://github.com/hackelia-micrantha/anthesis/issues/241), and [distribution issue #173](https://github.com/hackelia-micrantha/anthesis/issues/173).
