# Governance Lab CLI

The Anthesis Governance Lab CLI is a deliberately small deterministic evaluator for testing public governance contracts without requiring the full Anthesis runtime.

It is distributed as a compiled `anthesis-lab` binary and consumed by [`ryjen/anthesis-governance-lab`](https://github.com/ryjen/anthesis-governance-lab).

## Public proof surfaces

The CLI participates in two executable proof surfaces; Governance Lab adds a third cataloged demonstration surface around it.

| Surface | Count | Primary command |
|---|---:|---|
| Canonical governance contract | 7 scenarios | `anthesis-lab test --repo . --format json` |
| General Governance Lab catalog | 9 packs / 27 scenarios | `bash scripts/aggregate-demo-packs.sh` in Governance Lab |
| Inference-integrity contract | 24 scenarios | `anthesis-lab inference-integrity --repo . --format json` |

The 24 inference-integrity cases are **not** part of the 27 general demonstration scenarios.

## What it proves

The public evaluator provides a concrete way to verify that Anthesis can:

- allow explicitly permitted declarations;
- hold approval-gated declarations before an effect executor acts;
- deny prohibited declarations;
- deny unregistered runtime identities through an engine guard;
- identify stable decision provenance, rule, and reason;
- fail closed on malformed, unsupported, unsafe, or unregistered inputs;
- emit reproducible report and evidence contracts;
- evaluate recorded provider-neutral inference evidence against explicit verification classes and policy postures;
- detect controlled expectation drift rather than accepting fixture expectations as computed outcomes.

It does **not** prove production sandboxing, credential isolation, distributed enforcement, live provider replay, containment, universal non-bypassability, or resistance to a hostile administrator.

## Current commands

Inspect the evaluator identity and supported contracts:

```bash
anthesis-lab version --format json
```

Run the seven canonical governance scenarios:

```bash
anthesis-lab test --repo . --format json
```

Run the 24 inference-integrity scenarios:

```bash
anthesis-lab inference-integrity --repo . --format json
```

Governance Lab also exercises individual declarations, evidence verification, demo-pack aggregation, controlled expectation mismatches, and output formats through its repository scripts.

## Expected report contracts

Canonical governance reports use:

```text
anthesis.test-report/v1
```

Inference-integrity reports use:

```text
anthesis.inference-integrity-report/v1alpha1
```

A successful inference-integrity run reports 24 total, 24 passed, and 0 failed. The executable validation also reruns the suite to require byte-identical JSON and mutates one copied expectation to require exit code `7` with exactly one failed scenario.

## Signed immutable acquisition

Governance Lab does not trust an arbitrary binary from a mutable URL. Its pinned release metadata identifies one reviewed Anthesis source revision and one public release transaction.

The acquisition path verifies:

1. the expected public release repository and source-derived tag;
2. Sigstore producer identity, workflow ref, workflow SHA, and GitHub Actions OIDC issuer;
3. archive and packaged-binary SHA-256 digests;
4. published checksum assets;
5. provenance source and distribution identity;
6. archive member allowlisting;
7. CLI name and version;
8. the exact supported public contract set;
9. repository-contained installation.

Any mismatch fails closed before scenario execution.

## Supported public contract set

The promoted evaluator currently identifies these contracts:

```text
anthesis.policy/v1
anthesis.lab-profile/v1
anthesis.scenario/v1
anthesis.decision/v1
anthesis.request-binding/v1
anthesis.evaluation-request/v1
anthesis.evidence-bundle/v1
anthesis.evidence-bundle-verification/v1
```

The exact binary version and release identity remain pinned by Governance Lab rather than duplicated here as a mutable documentation promise.

## Public contract

The community repository publishes selected versioned schemas, semantics, fixtures, and release artifacts required to inspect the public claims, including:

- policy, runtime-profile, scenario, decision, request-binding, evaluation-request, and evidence contracts;
- deterministic normalization and matching semantics;
- default-deny and fail-closed requirements;
- canonical policy and runtime fixtures;
- seven canonical governance vectors;
- inference-integrity fixture contracts and report semantics exposed by the promoted evaluator;
- exact policy/evidence digest fixtures and validators where applicable.

Version 1 governance scenarios declare exactly one attempted effect. Natural-language goals are descriptive only and never grant authority.

The canonical runtime profile explicitly lists permitted runtime identities. Unregistered runtimes are denied by an engine guard rather than silently accepted.

## Private implementation boundary

The private Anthesis repository may retain evaluator source, parser and canonicalization hardening, optimization, defensive implementation details, binary hardening, and release-signing infrastructure.

Hidden implementation checks may only deny. Every authorization must remain attributable to the public policy/default semantics that produced it.

## Trust model

The CLI is a reference evaluator for controlled public validation:

- evaluation never executes the attempted file, command, network, merge, deployment, release, or administration effect;
- inference-integrity evaluation uses recorded synthetic evidence rather than live provider traffic;
- policy defaults to deny;
- invalid YAML, duplicate keys, unsupported values, unsafe paths, and unknown runtimes fail closed;
- expected outcomes are assertions, not evaluator inputs;
- evidence can be checksum-verified and, where specified, independently verified;
- obfuscation is IP friction, not a security boundary.

For the executable operator procedure, use the Governance Lab repository's full-verification and inference-integrity runbooks. The normative Governance Lab specification remains under `specs/governance-lab/` in this repository.
