# Anthesis Product Overview

Anthesis is a deterministic governance boundary for agentic systems and lifecycle loops.

Core invariant:

> Every externally observable agentic effect is authorized, constrained, attributable, and auditable through Anthesis.

Reasoning can remain internal. Effects must cross a governance boundary that the surrounding execution environment can make authoritative.

Externally observable effects include tool invocation, specialist delegation, memory/context access, filesystem mutation, shell/process execution, network/API calls, repository writes, external communication, approval-gated actions, artifact publication, and long-term state mutation.

## Supervisor / Specialist Model

```text
AI control plane
  -> supervisor agent
    -> Anthesis governance boundary
      -> envelope / policy decision / capability / approval
        -> specialist agents
          -> governed tools, memory, services, APIs
            -> evidence / evaluation / audit
```

Supervisor agents orchestrate. Specialist agents execute bounded work. Anthesis governs the effects.

## Public Proof Model

The current public materials keep three proof surfaces separate:

| Surface | Count | Purpose |
|---|---:|---|
| Canonical Governance Lab contract | 7 scenarios | Stable deterministic governance conformance. |
| General Governance Lab catalog | 9 packs / 27 scenarios | Broader synthetic governed-action coverage. |
| Inference-integrity contract | 24 scenarios | Deterministic evaluation of recorded provider-neutral inference evidence. |

The 24 inference-integrity cases are separate from the 27 general demo scenarios.

Governance Lab proves deterministic evaluator behavior and reproducible public evidence. It does not execute declared production effects or prove that arbitrary runtimes cannot bypass Anthesis.

Dubnium provides a bounded reference execution environment for demonstrating how an Anthesis decision can be made authoritative at a runtime/tool boundary. It is a reference composition, not a universal deployment guarantee.

## Integration Strength

Anthesis can be integrated through tool wrappers, MCP mediation, gateways/sidecars, downstream capability tokens, SDK wrappers, or sandboxed runtimes. Assurance depends on which direct effect paths remain available.

The governing question is:

> What prevents the agent from producing this effect without crossing Anthesis?

## What Anthesis Is Not

Anthesis is not primarily an agent framework, LLM runtime, memory database, generic orchestration system, scanner, dashboard, or compliance portal. It is the control surface for governed agentic effects.

## Read Next

- `docs/product/envelope.md`
- `docs/product/trial-criteria.md`
- `docs/product/integrations/README.md`
- `docs/product/governance-lab-cli.md`
- `https://github.com/ryjen/anthesis-governance-lab`
