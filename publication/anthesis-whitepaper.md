---
title: "Anthesis: Governed Execution for Agentic Systems"
order: 0
category: "Overview"
summary: "A concise public whitepaper describing the Anthesis governance boundary, integration model, proof paths, and trust assumptions."
status: "Draft"
pdf_title: "Anthesis: Governed Execution for Agentic Systems"
pdf_footer: "All rights reserved © Micrantha 2026"
pdf_outline_title: "Anthesis Whitepaper"
---

# Anthesis Whitepaper

## Version and authorship

**Version 0.3.0 - 2026-07-27 - Ryan Jennings**

This release refocuses the public whitepaper on governed effects, integration assurance, and executable proof paths. Earlier revisions remain available through version control.

## 1. Executive summary

Anthesis is the governance boundary between an agent's intent and its externally observable effects.

It evaluates consequential actions against explicit policy, authority, approvals, capabilities, and evidence requirements before those actions cross a real-world boundary. The result is a structured decision that a surrounding tool, gateway, credential boundary, validator, or runtime can enforce.

Anthesis is designed to compose with existing agent frameworks and execution environments. It is not a general-purpose agent orchestrator, model runtime, memory database, project-management system, or compliance dashboard.

Its central invariant is:

> Every governed externally observable effect is authorized, constrained, attributable, and auditable through Anthesis.

The strength of that claim depends on the integration preventing bypass. Prompts, conventions, and cooperative wrappers are useful ergonomics, but they are not enforcement guarantees by themselves.

## 2. The problem

Agentic systems can acquire practical authority through tool registries, credentials, network access, delegated specialists, filesystem access, and automated loops. Without a clear governance boundary, authority may be implicit, difficult to review, and hard to reconstruct after an incident.

A useful governance system must answer four questions before a consequential effect occurs:

1. **What is being requested?**
2. **Who or what has authority to request it?**
3. **Which policy, approval, capability, and evidence requirements apply?**
4. **What prevents execution outside the approved boundary?**

Anthesis addresses the decision and evidence parts of this boundary. Enforcement is completed by the selected integration: a restricted tool surface, gateway, downstream capability validator, credential boundary, sandbox, or combination of controls.

## 3. Governed effects

Reasoning may remain internal. Effects must cross a governance boundary.

Governed effects may include:

- specialist or sub-agent delegation;
- tool and MCP invocation;
- memory or context access;
- filesystem and repository mutation;
- shell or process execution;
- network and API calls;
- external communication;
- approval-gated actions;
- deployment, release, or administrative operations;
- artifact publication and durable state mutation.

Not every effect needs the same policy or approval level. Low-risk actions may be permitted under an existing policy grant. Higher-risk actions may require exact human approval, narrower capabilities, stronger evidence, or a safe halt.

## 4. Responsibility boundaries

Anthesis is part of a broader proof and execution ecosystem with deliberately separate responsibilities.

| Component | Responsibility |
| --- | --- |
| **Anthesis** | Policy authority, deterministic decision contracts, approval requirements, capability constraints, evidence semantics, and provenance. |
| **Anthesis Governance Lab** | Independent deterministic conformance, scenario packs, aggregate reports, and public walkthroughs against the Anthesis evaluator contract. |
| **Dubnium** | Reproducible local-first agentic runtime, gateway, bounded tools, execution, and runtime evidence for a reference integration. |

Governance Lab is not the deployable governance product and is not in the runtime critical path. It evaluates declared scenarios and does not execute their declared effects.

Dubnium is not the policy authority. It demonstrates how an execution environment can consume Anthesis decisions, enforce exact approvals, run bounded actions, and return evidence.

## 5. Governed effect flow

A typical governed action follows this shape:

```text
Agent or supervisor request
  -> normalize the proposed effect
  -> Anthesis policy and authority evaluation
      -> allow with constraints
      -> exact approval required
      -> deny or safe halt
  -> integration enforcement boundary
  -> bounded execution
  -> evidence and outcome return
  -> audit, evaluation, and recovery as applicable
```

Five concerns must remain distinct:

| Concern | Responsibility |
| --- | --- |
| **Decision integration** | Anthesis normalizes and evaluates a proposed externally observable effect. |
| **Enforcement integration** | A tool, gateway, credential boundary, downstream validator, or runtime prevents an unauthorized effect. |
| **Evidence integration** | Execution identity, material activity, outcome, and validation evidence return to the governed record. |
| **Reference validation** | Governance Lab independently validates public Anthesis contracts and deterministic decisions. |
| **Reference execution** | Dubnium demonstrates bounded execution using the public Anthesis decision boundary. |

A policy decision without enforcement can still be bypassed. Enforcement without evidence may block some misuse but remain difficult to inspect or audit. A complete governed path needs all three operational concerns: decision, enforcement, and evidence.

## 6. Integration and enforcement model

Anthesis supports six canonical integration modes:

1. **Tool wrapper / invoke**
2. **MCP mediation**
3. **Gateway / sidecar**
4. **Capability tokens**
5. **SDK wrapper**
6. **Sandboxed runtime**

The modes describe integration mechanisms. They do not carry a fixed guarantee level by name alone.

### 6.1 Enforcement location

Enforcement may live at one or more locations:

- **Application** — an SDK or application wrapper controls how effects are requested.
- **Tool surface** — a tool registry or MCP facade controls the agent-facing capability surface.
- **Infrastructure** — a gateway, sidecar, credential boundary, network control, or downstream validator controls access to effects.
- **Runtime** — a sandbox controls filesystem, network, process, credential, and tool access.

### 6.2 Assurance classification

The resulting assurance depends on the surrounding bypass controls:

- **Advisory** — Anthesis recommends or records a decision, but direct effect paths remain available.
- **Moderate** — agents are configured to use Anthesis paths, but additional bypass paths may remain.
- **Strong** — registries, credentials, network controls, gateways, or downstream validators prevent most direct bypass.
- **Runtime-enforced** — the runtime prevents direct effects outside governed paths.

The same nominal mode may fall into different classifications. MCP mediation with raw credentials and unrestricted network access may be moderate. MCP mediation combined with credential isolation and egress controls may be strong.

### 6.3 Integration matrix

| Mode | Enforcement location | Required bypass control | Typical assurance |
| --- | --- | --- | --- |
| **Tool wrapper / invoke** | Tool surface | Raw tools must not remain available to the agent | Moderate to strong |
| **MCP mediation** | Tool surface | Raw downstream MCP servers, credentials, and direct service paths must be unavailable or constrained | Moderate to strong |
| **Gateway / sidecar** | Infrastructure | Downstream services must be unreachable except through the gateway | Strong |
| **Capability tokens** | Infrastructure or downstream tool | Downstream effects must reject missing, expired, altered, or out-of-scope grants | Strong |
| **SDK wrapper** | Application | Direct clients and raw credentials must not remain an uncontrolled path | Advisory to moderate |
| **Sandboxed runtime** | Runtime | Filesystem, network, process, credentials, and tools must be unavailable outside governed paths | Runtime-enforced when complete |

For each deployment, the implementer should identify:

- the agent-facing surface;
- the location of Anthesis policy authority;
- the credential owner;
- the executor;
- the exact bypass-prevention mechanism;
- the evidence return path;
- material trust assumptions and residual direct-effect paths.

Detailed Questions, Alternatives, Recommendations, and Tradeoffs analyses remain in the product integration documentation rather than being duplicated here.

## 7. Composition patterns

Production and higher-assurance deployments will often combine modes.

### SDK wrapper plus credential isolation

The SDK provides a simple application interface, while raw service credentials are held by a gateway or broker. The wrapper alone is not the guarantee; credential ownership and downstream access control prevent bypass.

### MCP mediation plus egress control

The agent sees only the Anthesis MCP facade. Network policy prevents direct access to downstream services, and credentials are unavailable to the model-facing process. This can raise an otherwise cooperative integration to strong assurance.

### Gateway plus capability validation

Anthesis issues an action-bound capability after policy evaluation. The gateway and downstream service reject requests without a valid grant. Evidence links the decision, capability, executor, and outcome.

### Sandboxed runtime plus gateway and scoped capabilities

A sandbox prevents direct filesystem, network, process, and credential access. External effects pass through a governed gateway and require scoped grants. This provides the strongest reference pattern, with greater operational complexity.

### Tool wrapper plus evidence callback

For a low-risk local trial, a restricted tool registry may expose only Anthesis-scoped actions and return material evidence after execution. This is useful for adoption testing but should not be represented as universally non-bypassable without environmental controls.

## 8. Public proof paths

### 8.1 Runnable now: Governance Lab

The public evaluator and Anthesis Governance Lab provide an independently runnable deterministic proof surface:

- immutable evaluator acquisition and checksum verification;
- deterministic scenario packs;
- allow, approval-required, policy-deny, and engine-guard outcomes;
- aggregate reports and stakeholder walkthroughs;
- no requirement for a GPU, live model, private source repository, production credentials, or hosted service.

Governance Lab proves public contract behavior. It does not execute declared file, network, deployment, merge, release, or administrative effects, and it does not prove production non-bypassability by itself.

### 8.2 Reference integration: Dubnium

Dubnium demonstrates a bounded governed-agent execution path:

```text
Human task
  -> exact structured action request
  -> Anthesis decision
  -> action-bound approval when required
  -> bounded Dubnium executor
  -> visible outcome and sanitized evidence
```

This is a reference composition showing decision, approval, execution, and evidence responsibilities. It is not a claim that every Anthesis deployment has equivalent runtime enforcement.

### 8.3 In development

Active work includes broader production enforcement profiles and stronger live evidence, replay, independent verification, containment, recovery, and inference-integrity controls.

Deterministic inference-integrity fixtures and scenario evaluations must not be described as complete live prevention of model-weight or covert-channel exfiltration.

## 9. Security and trust boundaries

Anthesis is fail-closed at the decision boundary when required policy, identity, approval, capability, or evidence inputs are missing or invalid. Deployment assurance still depends on the enforcing environment.

A security review should test at least these conditions:

- direct tool or API invocation without Anthesis;
- use of raw credentials outside the governed path;
- expired, altered, replayed, or out-of-scope capabilities;
- approval reuse against a different action, target, or payload;
- direct network, filesystem, process, or repository effects;
- missing or contradictory execution identity;
- evidence mutation or replacement after execution;
- fallback to an unregistered runtime, model route, verifier, or tool;
- failure to return material outcome and validation evidence.

The system should state residual bypass assumptions explicitly. A prompt instruction to “always call Anthesis first” is not equivalent to registry restriction, credential isolation, downstream validation, or sandbox enforcement.

## 10. Adoption path

A practical evaluation can proceed in three stages:

1. **Validate the contract.** Run Governance Lab and inspect deterministic decisions, reasons, rules, and reports.
2. **Integrate one bounded effect.** Select a low-risk action, identify its bypass paths, choose an integration mode, and require evidence return.
3. **Strengthen enforcement.** Add credential isolation, gateway controls, downstream capability validation, egress restriction, or sandboxing according to the risk.

A trial is successful when an evaluator can explain:

- what Anthesis decided and why;
- what prevented the effect from bypassing the decision;
- who or what executed the action;
- which approval or capability authorized it;
- what evidence proves the material outcome;
- what trust assumptions and residual risks remain.

## 11. Scope and non-goals

Anthesis does not automatically make an agentic system secure merely by being called. It does not guarantee deterministic model output, universal replay, complete compliance, or non-bypassability without an enforcing integration.

The public whitepaper is explanatory. Accepted RFCs, schemas, policy contracts, and evaluator contracts remain the normative sources for implementation behavior.

## 12. Conclusion

Anthesis makes agent authority explicit at the point where intent becomes effect.

Its value is not only that it can return an allow, approval-required, or deny decision. Its value is that existing agentic systems can bind those decisions to enforcement controls and evidence records that remain reviewable after execution.

The governing question for every integration is therefore: **What prevents the agent from producing this effect without crossing Anthesis?**
