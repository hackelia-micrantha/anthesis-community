# Anthesis

![Status](https://img.shields.io/badge/status-active%20development-2ea44f)
![Governance](https://img.shields.io/badge/governance-deterministic%20policy-1f6feb)
![Execution](https://img.shields.io/badge/execution-governed-6f42c1)
![Security](https://img.shields.io/badge/security-docs%20available-8250df)
![License](https://img.shields.io/badge/core-closed%20source%20%7C%20public%20contracts-5a5a5a)

> *Anthesis* — the phase in which a flower is fully open and capable of function.

Anthesis is a **deterministic governance boundary for agentic systems**.

Its core invariant is:

> Every externally observable agentic effect is authorized, constrained, attributable, and auditable through Anthesis.

Reasoning can remain internal. Consequential effects must cross a governance boundary whose decision can be enforced by the surrounding tool surface, gateway, credential boundary, downstream validator, capability system, or runtime.

## What Anthesis governs

Externally observable effects can include:

- tool invocation and specialist delegation;
- memory and context access;
- filesystem and process mutation;
- network and API calls;
- repository writes, merges, releases, and deployment actions;
- external communication;
- approval-gated operations;
- artifact publication and long-term state mutation.

Anthesis does **not** attempt to be an agent framework, LLM runtime, memory database, generic orchestrator, scanner, dashboard, or compliance portal. It is the control surface for governed agentic effects.

## Supervisor / specialist model

A common integration pattern is:

```text
AI control plane
  -> supervisor agent
    -> Anthesis governance boundary
      -> policy decision / capability / approval
        -> specialist agents
          -> governed tools, memory, services, APIs
            -> evidence / outcome
```

Supervisors orchestrate. Specialists execute bounded work. Anthesis governs the effects and records the authority required to produce them.

## Public proof surfaces

Anthesis keeps evaluation, demonstration coverage, and runtime enforcement deliberately separate.

| Surface | Current public proof | Purpose |
|---|---:|---|
| Canonical Governance Lab contract | **7 scenarios** | Stable deterministic policy outcomes, including allow, approval-required, policy deny, and engine-guard deny. |
| General Governance Lab catalog | **9 packs / 27 scenarios** | Broader synthetic SDLC and operational declarations across documentation, source, CI/release, dependencies, secrets, tools, runtimes, administration, and adversarial cases. |
| Inference-integrity contract | **24 scenarios** | Deterministic evaluation of recorded provider-neutral evidence for identity, seed/token integrity, routing, verifier trust, topology, re-verification, operating modes, and recovery. |

The **24 inference-integrity cases are separate from the 27 general demo scenarios**.

Run the public lab at [`ryjen/anthesis-governance-lab`](https://github.com/ryjen/anthesis-governance-lab). Start with its operator or full-verification runbook rather than assuming the three counts describe one suite.

### What Governance Lab proves

Governance Lab proves that a pinned public evaluator can reproducibly evaluate declared attempts and recorded evidence against pinned contracts, and that controlled expectation drift is detected.

It does **not** execute the declared effects, persist production approvals, invoke live model providers, prove universal replay, execute containment, or prove that an external runtime cannot bypass Anthesis.

## Enforcement and integration modes

Integration strength depends on what prevents the agent from producing an effect without crossing Anthesis.

| Mode | Core bypass question | Typical strength |
|---|---|---|
| Tool wrapper / `invoke` | Does the agent registry expose only Anthesis-controlled tools? | Moderate to strong |
| MCP mediation | Are raw downstream MCP servers and credentials unavailable or constrained? | Moderate to strong |
| Gateway / sidecar | Are downstream effects unreachable except through the gateway? | Strong |
| Capability tokens | Do downstream tools reject missing, expired, altered, replayed, or out-of-scope grants? | Strong |
| SDK wrapper | Can code still use direct clients or raw credentials? | Advisory to moderate |
| Sandboxed runtime | Does the runtime prevent direct filesystem, network, process, credential, and tool effects? | Runtime-enforced when complete |

Prompts and conventions are not enforcement guarantees. Strong assurance comes from control of registries, credentials, network paths, downstream validation, capabilities, or the runtime itself.

See [`docs/product/integrations/README.md`](docs/product/integrations/README.md).

## Trial criteria

A useful Anthesis trial should evaluate six practical dimensions:

1. **Enforceability** — governed effects cannot occur without the selected governance boundary.
2. **Attribution** — decisions and effects identify the responsible actor, runtime, tool, capability, approval, envelope, and evidence.
3. **Least privilege** — capabilities are narrowly scoped and deny out-of-scope actions.
4. **Human approval** — actions requiring approval remain blocked until the exact approved scope is granted.
5. **Auditability** — decisions, approvals, effects, and evidence can be reconstructed or replayed at the appropriate verification level.
6. **Bypass resistance** — residual direct paths and trust assumptions are explicit and tested for the selected integration mode.

See [`docs/product/trial-criteria.md`](docs/product/trial-criteria.md).

## Public evaluator

The public Governance Lab uses a signed, immutable `anthesis-lab` release distributed through this repository. The lab verifies producer identity, Sigstore bundles, provenance, checksums, archive contents, binary identity, version, and supported contracts before execution.

The current evaluator exposes separate commands for the canonical governance contract and inference-integrity contract. See [`docs/product/governance-lab-cli.md`](docs/product/governance-lab-cli.md) and the Governance Lab repository for the pinned executable workflow.

## Project relationships

- **Anthesis** — policy authority, deterministic evaluator semantics, approvals, capabilities, evidence semantics, and provenance.
- **Anthesis Governance Lab** — independent public conformance and demonstration fixtures; not part of the runtime critical path.
- **Dubnium** — bounded reference execution environment and live-runtime integration surface; it consumes Anthesis decisions rather than defining policy authority.
- **Anthesis Community** — public contracts, specifications, release artifacts, product documentation, website, project brief, and whitepaper distribution.

## Current maturity

**Runnable now:** signed public evaluator acquisition, Governance Lab canonical/general/inference fixtures, deterministic reports, evidence bundles, and stakeholder walkthroughs.

**Reference integration:** bounded governed-agent execution through Dubnium with approval binding and runtime evidence.

**In development:** broader production enforcement profiles and stronger live inference-integrity capture, replay, independent verification, containment, and recovery.

## Read next

- [Anthesis website](https://anthesis.micrantha.com/)
- [Project brief](https://anthesis.micrantha.com/project-brief.html)
- [Governance Lab](https://github.com/ryjen/anthesis-governance-lab)
- [`docs/product/overview.md`](docs/product/overview.md)
- [`docs/product/trial-criteria.md`](docs/product/trial-criteria.md)
- [`docs/product/integrations/README.md`](docs/product/integrations/README.md)
- [`docs/product/governance-lab-cli.md`](docs/product/governance-lab-cli.md)
- [Anthesis whitepaper](https://anthesis.micrantha.com/anthesis.pdf)

## License and implementation boundary

The core Anthesis implementation remains closed source and all rights reserved unless separately licensed. This community repository intentionally publishes selected contracts, specifications, documentation, release artifacts, and validation surfaces so external reviewers can inspect and reproduce the public governance claims without access to private implementation details.
