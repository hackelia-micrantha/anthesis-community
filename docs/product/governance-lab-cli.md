# Governance Lab CLI

The Anthesis Governance Lab CLI is a deliberately small evaluator for testing deterministic governance behavior without requiring the full Anthesis runtime.

It is intended to be distributed as a compiled, stripped binary and consumed by `ryjen/anthesis-governance-lab`.

## What it proves

The CLI gives an evaluator a concrete way to test whether Anthesis can:

- allow explicitly safe work
- deny explicitly unsafe work
- stop approval-gated work before execution
- identify the exact policy rule and reason
- fail closed on malformed or unsupported input
- emit evidence that can be checked after the run

It does not prove production-grade sandboxing, credential isolation, distributed enforcement, or resistance to a hostile administrator.

## Commands

```bash
anthesis-lab evaluate --repo . --scenario .anthesis/scenarios/02-block-ci-change.yaml
anthesis-lab test --repo .
anthesis-lab verify --evidence .anthesis/evidence/run.jsonl
anthesis-lab version
```

## Distribution boundary

The public community repository contains:

- the CLI contract
- versioned schemas
- deterministic matching semantics
- conformance requirements
- sample inputs and outputs

The private Anthesis repository may contain:

- source implementation
- binary hardening and obfuscation
- release workflows
- parser hardening
- additional deny-only defensive checks

The implementation may remain closed while still conforming to the public contract. Every authorization must nevertheless identify the public policy rule that produced it.

## Trust model

The CLI is a reference evaluator for a controlled local lab.

For the first version:

- policy is local and declarative
- scenarios describe attempted effects
- evaluation does not execute commands or network requests
- filesystem effects may be simulated or constrained to a temporary worktree
- invalid or unknown inputs fail closed
- binary obfuscation is treated as IP friction, not a security boundary

The normative specification is in `specs/governance-lab/README.md`.
