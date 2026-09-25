# Anthesis

![Status](https://img.shields.io/badge/status-active%20development-2ea44f)
![Governance](https://img.shields.io/badge/governance-deterministic%20policy-1f6feb)
![Execution](https://img.shields.io/badge/execution-governed-6f42c1)
![Security](https://img.shields.io/badge/security-docs%20available-8250df)
![License](https://img.shields.io/badge/core-closed%20source%20%7C%20public%20contracts-5a5a5a)

> *Anthesis* — the phase in which a flower is fully open and capable of function.

Anthesis is a **portable, self-hostable governance solution for data sovereignty in agentic AI**. It lets resource owners define and evaluate policies for how agents may access, modify, and transmit their code, data, and connected systems.

Data sovereignty is the goal; deterministic exact-effect authorization is the mechanism. Anthesis does not host a model, replace an agent runtime, or independently guarantee data residency. The selected tool, gateway, capability validator, or isolated runtime must enforce Anthesis decisions, and all other data paths must be controlled.

**Running an agentic system that could serve as an Anthesis trial?** Anthesis is actively looking for real agent workflows to exercise the governance boundary and provide implementation feedback. See [How to help Anthesis](#how-to-help-anthesis).

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

## Try Anthesis

For the shortest executable path, use [`docs/product/try-anthesis.md`](docs/product/try-anthesis.md).

The reference trial evaluates one exact repository mutation, executes it only through a constrained Anthesis-controlled tool wrapper, then deliberately attempts both a raw writer bypass and an out-of-scope write. Both negative paths must be hard-denied with repository state unchanged.

It is intentionally explicit about what creates the enforcement claim: the simulated agent registry exposes only the governed writer and no shell, filesystem, Git, network, raw provider tool, or raw credential path. The walkthrough does not mistake deterministic evaluation for universal sandboxing.

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
- **Dubnium** — personal self-hosted AI system and bounded reference execution environment; it consumes Anthesis decisions rather than defining policy authority. It is not required to run Anthesis or currently a generally available distribution; a future public release is possible.
- **Anthesis Community** — public contracts, specifications, release artifacts, product documentation, website, project brief, and whitepaper distribution.

## How to help Anthesis

Anthesis is looking for external scrutiny and real integration pressure more than undirected feature work. In particular, it is seeking **existing agentic systems for bounded trial runs** so the project can measure integration effort, identify bypass paths, expose missing policy/evidence semantics, and gather operator feedback from systems that were not designed around Anthesis.

- **Agentic-system trial partners** — bring an existing coding agent, supervisor/specialist system, MCP/tool workflow, automation platform, or other agentic runtime and select one low-risk consequential action for a bounded Anthesis integration trial. Useful feedback includes integration friction, unexpected authority paths, policy-model gaps, approval UX, evidence quality, and operational overhead.
- **Security and governance reviewers** — challenge authorization, approval binding, capability scope, evidence semantics, provenance, replay, bypass resistance, and failure-closed behavior.
- **Design partners and adopters** — bring concrete agentic workflows where data sovereignty, local/self-hosted operation, privileged tools, approvals, or audit evidence matter.
- **Integration contributors** — help define and validate adapters, gateways, capability validation, MCP/tool mediation, runtime enforcement profiles, and interoperability with existing agent platforms.
- **Governance Lab and conformance contributors** — add safe synthetic scenarios, adversarial cases, independent reproductions, documentation, and implementation-neutral contract feedback.
- **Strategic partners** — help test product direction, applied research, distribution, sustainability, and production adoption while preserving the separation between public proof surfaces and private implementation.

A trial does not need to prove that Anthesis is a fit. Negative results, awkward integration points, unacceptable overhead, and bypasses that cannot be closed are useful findings. Trial feedback should be reduced to reusable requirements or safe synthetic cases before public publication; environment-specific or confidential details can stay private.

For a trial conversation, contact [services@micrantha.com](mailto:services@micrantha.com?subject=Anthesis%20agentic%20system%20trial) with a short description of the agentic system, the effect you want to govern, and the main trust boundary you want to test.

The core Anthesis implementation remains closed source. Public contribution is intentionally focused on contracts, specifications, documentation, release/proof artifacts, integrations, conformance, and reproducible review. See [CONTRIBUTING.md](CONTRIBUTING.md) for the public contribution boundary. Micrantha-wide strategic-partner and co-founder interests are described in the [organization collaboration overview](https://github.com/hackelia-micrantha/.github/blob/main/profile/README.md#looking-for-collaborators).

## Current maturity

**Runnable now:** signed public evaluator acquisition, Governance Lab canonical/general/inference fixtures, deterministic reports, evidence bundles, and stakeholder walkthroughs.

**Reference integration:** bounded governed-agent execution through the personal Dubnium system with approval binding and runtime evidence. Dubnium is a personal-system use case, not a requirement for using Anthesis or a generally available release.

**In development:** broader production enforcement profiles and stronger live inference-integrity capture, replay, independent verification, containment, and recovery.

## Read next

- [`Try Anthesis`](docs/product/try-anthesis.md)
- [Documentation maintenance contract](docs/documentation-maintenance.md) — maintainer validation and public/private authority boundaries
- [Anthesis website](https://anthesis.micrantha.com/)
- [Project brief](https://anthesis.micrantha.com/project-brief.html)
- [Governance Lab](https://github.com/ryjen/anthesis-governance-lab)
- [`docs/product/overview.md`](docs/product/overview.md)
- [`docs/product/where-anthesis-fits.md`](docs/product/where-anthesis-fits.md) — local-first data-sovereignty use cases and platform responsibilities
- [`docs/product/trial-criteria.md`](docs/product/trial-criteria.md)
- [`docs/product/integrations/README.md`](docs/product/integrations/README.md)
- [`docs/product/governance-lab-cli.md`](docs/product/governance-lab-cli.md)
- [Anthesis whitepaper](https://anthesis.micrantha.com/anthesis.pdf)

## License and implementation boundary

The core Anthesis implementation remains closed source and all rights reserved unless separately licensed. This community repository intentionally publishes selected contracts, specifications, documentation, release artifacts, and validation surfaces so external reviewers can inspect and reproduce the public governance claims without access to private implementation details.
