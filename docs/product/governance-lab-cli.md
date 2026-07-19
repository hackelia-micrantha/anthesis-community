# Governance Lab CLI

The Anthesis Governance Lab CLI is a deliberately small deterministic evaluator for testing governance behavior without requiring the full Anthesis runtime.

It is intended to be distributed as a compiled, stripped binary and consumed by `ryjen/anthesis-governance-lab`.

## What it proves

The CLI provides a concrete way to test whether Anthesis can:

- allow explicitly safe work
- deny explicitly unsafe work
- stop approval-gated work before execution
- identify the exact public policy rule and reason
- fail closed on malformed, unsupported, or unregistered inputs
- emit verifiable evidence

It does not prove production-grade sandboxing, credential isolation, distributed enforcement, or resistance to a hostile administrator.

## Commands

```bash
anthesis-lab evaluate --repo . --scenario .anthesis/scenarios/02-block-ci-change.yaml
anthesis-lab test --repo .
anthesis-lab verify --evidence .anthesis/evidence/run.jsonl
anthesis-lab version
```

## Public contract

The community repository publishes:

- versioned scenario, policy, runtime-profile, decision, and evidence schemas
- deterministic normalization and matching semantics
- default-deny and fail-closed requirements
- canonical policy and runtime fixtures
- seven semantic conformance vectors
- an exact policy digest vector
- a validator that checks schema shape and expected decisions

Version 1 scenarios declare exactly one attempted effect. Natural-language goals are descriptive only and never grant authority.

The canonical runtime profile explicitly lists permitted runtime identities. Unregistered runtimes are denied by an engine guard rather than silently accepted.

## Private implementation boundary

The private Anthesis repository may retain:

- evaluator source
- parser and canonicalization hardening
- optimization and defensive implementation details
- binary hardening and obfuscation
- release signing infrastructure and keys

Hidden implementation checks may only deny. Every authorization must identify the public rule or default that produced it.

## Trust model

The CLI is a reference evaluator for a controlled local lab:

- evaluation never executes the attempted command, network request, or file effect
- policy defaults to deny
- deny and approval rules precede broad allow rules
- invalid YAML, duplicate keys, unsupported values, unsafe paths, and unknown runtimes fail closed
- evidence may be hash-chained and independently verified
- obfuscation is IP friction, not a security boundary

The normative specification is in `specs/governance-lab/README.md`.
