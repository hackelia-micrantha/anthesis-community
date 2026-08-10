# Promoted Governance Lab contracts

Status: Accepted compatibility surface  
Tracks: #19

This document defines the implementation-neutral contract identifiers advertised by the currently promoted `anthesis-lab` evaluator. It supplements the original Governance Lab v1 specification without exposing private evaluator implementation details.

## Advertised contract set

The promoted evaluator reports exactly these eight public contract identifiers:

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

Each identifier above MUST have a machine-readable schema in this directory. An evaluator release MUST NOT advertise a new identifier as a public compatibility contract unless its externally observable schema and semantics are published here.

The original `anthesis.evidence/v1` and `anthesis.conformance/v1` records remain public specification artifacts but are not part of this evaluator version-advertised set.

## Request binding and evaluation request

`anthesis.request-binding/v1` binds integrator-owned context to one normalized Anthesis evaluation request without placing unrestricted payloads or secrets in policy or decision records.

The v1 request binding uses:

- `canonicalization: rfc8785-json`;
- `algorithm: sha256`;
- `input_digest`;
- `plan_digest`;
- `source_digest`;
- `dependency_state_digest`.

All digests use lowercase `sha256:<64 hex characters>`. The digest values are identity claims supplied by the integrator; they do not prove the represented content is safe, truthful, or semantically complete.

`anthesis.evaluation-request/v1` contains exactly:

- `version`;
- `scenario_id`;
- `policy`;
- the normalized `effect`;
- the unbound `request_binding`.

Anthesis canonicalizes that typed request and computes the `request_digest` returned in the bound request-binding member of `anthesis.decision/v1`. Changing any bound field changes request identity. Unknown members, unsupported versions, unsupported algorithms, and malformed digests fail closed.

The promoted v1 field name is **`input_digest`**. The historical implementation spelling `action_input_digest` is not part of this public v1 contract.

## Evidence bundle

`anthesis.evidence-bundle/v1` is a portable completed-run manifest. It binds retained files by relative path, role, exact byte size, and lowercase SHA-256 digest.

A bundle declares:

- one `bundle_id` and `run_id`;
- an RFC-0054 replayability class: `none`, `bounded`, or `strong`;
- a comparison strategy: `strict`, `semantic`, `governance`, or `non_replayable`;
- one declared decision path;
- one declared report path;
- sorted portable entries;
- typed links between retained files.

A completed-run bundle must identify a decision entry and report entry and include a `reports_on` link from the report to the exact decision digest. Bundle declarations do not upgrade the retained evidence floor and do not mint invocation authority.

Portable bundle paths are repository-like relative paths. Implementations must reject path escape and unsafe or symlinked bundle entries before trusting file contents.

## Evidence-bundle verification

`anthesis.evidence-bundle-verification/v1` is the machine-readable result of offline bundle verification.

A report contains:

- `passed`;
- the bundle contract version and identity;
- replayability and comparison declarations copied from the manifest;
- counts of verified entries and links;
- zero or more findings.

The v1 finding codes are:

```text
missing_file
not_regular_file
size_mismatch
digest_mismatch
substituted_report
broken_linkage
```

A successful verification has `passed: true` and no findings. Integrity failures return the same report with `passed: false` and exit code `7`. Invalid manifests, unsafe paths, and symlinked entries are invalid input. Unsupported versions are unsupported input. Internal output or verifier failures remain internal failures.

Offline verification establishes internal consistency against the supplied manifest. It does **not** prove who produced the manifest, authorize an effect, re-evaluate policy, replay an effect, contact a live runtime, or establish release authenticity.

## CLI relationship

The promoted evaluator exposes the bundle verification surface as:

```text
anthesis-lab verify --bundle <directory> [--format json|yaml]
```

The evaluator also exposes `generate-bundle` for deterministic bundle generation. Generation and verification are evidence operations only; neither can mint or widen execution authority.

The canonical Governance Lab consumer pins a specific signed evaluator revision and validates the exact advertised contract set before execution. Release producer identity, Sigstore verification, checksums, and provenance remain distribution concerns separate from these payload schemas.

## Compatibility

Within a major contract version:

- required fields must not be removed;
- authorization-relevant meanings must not change;
- enum values with security meaning must not be silently reinterpreted;
- unsupported major versions fail closed;
- new public contract identifiers require a published schema and semantics before they are treated as implementation-neutral compatibility promises.
