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
- detect controlled expectation drift rather than accepting fixture expectations as computed outcomes;
- generate and verify portable evidence bundles without treating evidence as execution authority.

It does **not** prove production sandboxing, credential isolation, distributed enforcement, live provider replay, containment, universal non-bypassability, or resistance to a hostile administrator.

## Current commands

Inspect evaluator identity and the exact advertised public contract set:

```bash
anthesis-lab version --format json
```

Evaluate one declared scenario without executing its effect:

```bash
anthesis-lab evaluate --repo . --scenario .anthesis/scenarios/01-allowed-docs-edit.yaml --format json
```

Run the seven canonical governance scenarios:

```bash
anthesis-lab test --repo . --format json
```

Run the 24 inference-integrity scenarios:

```bash
anthesis-lab inference-integrity --repo . --format json
```

Generate a deterministic portable completed-run evidence bundle:

```bash
anthesis-lab generate-bundle \
  --run <completed-run-directory> \
  --output <bundle-directory> \
  --bundle-id <bundle-id> \
  --run-id <run-id> \
  --format json
```

Verify a portable evidence bundle offline:

```bash
anthesis-lab verify --bundle <bundle-directory> --format json
```

The promoted evaluator also exposes `gateway-eligibility` for projecting trusted Dubnium gateway metadata into conservative verification eligibility. That integration command is not one of the 7 / 27 / 24 proof counts and does not grant runtime authority.

Governance Lab additionally exercises evidence generation, demo-pack aggregation, controlled expectation mismatches, deterministic repeatability, and output formats through its repository scripts.

## Expected report contracts

Canonical governance reports use:

```text
anthesis.test-report/v1
```

Inference-integrity reports use:

```text
anthesis.inference-integrity-report/v1alpha1
```

Portable evidence-bundle verification reports use:

```text
anthesis.evidence-bundle-verification/v1
```

A successful inference-integrity run reports 24 total, 24 passed, and 0 failed. The executable validation reruns the suite to require byte-identical JSON and mutates one copied expectation to require exit code `7` with exactly one failed scenario.

Evidence-bundle verification returns exit code `0` when the declared bundle is internally consistent, `7` for verification findings, `3` for invalid/unsafe input, `8` for unsupported contract versions, and `10` for internal failures. Successful verification validates evidence; it does not authorize or replay an effect.

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
8. the exact evaluator-advertised public contract identifier set;
9. repository-contained installation.

Any mismatch fails closed before scenario execution.

## Promoted public contract identifiers

The promoted evaluator currently advertises exactly these eight implementation-neutral public contracts:

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

All eight now have machine-readable schemas and published semantics under `specs/governance-lab/`. The bounded compatibility supplement is [`specs/governance-lab/PROMOTED-CONTRACTS.md`](../../specs/governance-lab/PROMOTED-CONTRACTS.md).

The promoted v1 request-binding field is `input_digest`. Historical internal spelling such as `action_input_digest` is not part of the public v1 contract and is rejected by compatibility validation.

The original `anthesis.evidence/v1` and `anthesis.conformance/v1` artifacts remain public specification/conformance records but are not part of the evaluator's exact eight-identifier version-advertised compatibility set.

A future evaluator release must not advertise a new identifier as an implementation-neutral public contract unless the corresponding externally observable schema and semantics are published here.

## Public contract

The community repository publishes the versioned contracts needed to independently inspect the promoted evaluator's public claims, including:

- policy, runtime-profile, scenario, decision, request-binding, and evaluation-request schemas;
- portable evidence-bundle and evidence-bundle-verification schemas;
- deterministic normalization, matching, canonicalization, and digest semantics;
- default-deny and fail-closed requirements;
- canonical policy/runtime fixtures and seven governance vectors;
- representative evaluation-request, bundle, and verification examples;
- compatibility validation requiring every promoted public identifier to have a published schema;
- a guard against obsolete request-binding field spelling;
- inference-integrity fixture/report semantics in the Governance Lab proof surface.

Version 1 governance scenarios declare exactly one attempted effect. Natural-language goals are descriptive only and never grant authority.

The canonical runtime profile explicitly lists permitted runtime identities. Unregistered runtimes are denied by an engine guard rather than silently accepted.

Evidence bundles preserve and verify recorded material. Evidence, successful verification, prior execution, topology, or replay material cannot mint or widen invocation authority.

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
- portable evidence bundles are checksum-bound and independently verifiable offline;
- verification validates evidence consistency but cannot authorize execution;
- obfuscation is IP friction, not a security boundary.

For the executable operator procedure, use the Governance Lab repository's full-verification and inference-integrity runbooks. The normative Governance Lab specification and promoted compatibility supplement remain under `specs/governance-lab/` in this repository.
