# Anthesis Product Overview

Anthesis is a deterministic governance gate for agentic architectures and lifecycle loops.

Core invariant:

> Every externally observable agentic effect is authorized, constrained, attributable, and auditable through Anthesis.

Reasoning can remain internal. Effects must cross a governance boundary.

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

## What Anthesis Is Not

Anthesis is not primarily an agent framework, LLM runtime, memory database, generic orchestration system, scanner, dashboard, or compliance portal. It is the control surface for governed agentic effects.

## Read Next

- `docs/product/envelope.md`
- `docs/product/trial-criteria.md`
- `docs/product/integrations/README.md`
