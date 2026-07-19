# Anthesis Governance Lab CLI Contract

Status: Draft

Issue: #9

## 1. Purpose

This specification defines the public, implementation-neutral contract for a stripped-down Anthesis governance evaluator used by `ryjen/anthesis-governance-lab`.

A conforming implementation may be distributed only as a compiled binary. Conformance depends on externally observable behavior, schemas, deterministic semantics, and evidence—not on publication of implementation source.

The implementation is not a general agent runtime. It evaluates declared effects against a versioned policy and produces one deterministic decision plus auditable evidence.

## 2. Normative language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

## 3. Core invariant

A conforming evaluator MUST uphold:

> No governed externally observable effect is treated as authorized without a deterministic policy decision attributable to a specific policy revision and rule.

## 4. Scope

Version 1 covers:

- local scenario evaluation
- declarative policy bundles
- deterministic rule matching
- `allow`, `deny`, and `approval_required` outcomes
- appendable evidence records
- batch conformance testing
- evidence integrity verification

Version 1 does not require:

- LLM execution
- MCP transport
- network services
- distributed workers
- credential handling
- production authorization guarantees
- policy plugins or executable policy code
- automatic execution of approved effects

## 5. CLI surface

A conforming binary MUST expose the program name `anthesis-lab` and these commands:

```text
anthesis-lab evaluate --repo <path> --scenario <file> [--format json|yaml]
anthesis-lab test --repo <path> [--scenarios <path>] [--format json|yaml]
anthesis-lab verify --evidence <file> [--format json|yaml]
anthesis-lab version [--format json|yaml]
```

### 5.1 Output discipline

- Successful machine-readable output MUST be written to stdout.
- Diagnostics MUST be written to stderr.
- JSON output MUST contain exactly one JSON object for `evaluate`, `verify`, and `version`.
- JSON output for `test` MUST contain one aggregate object with per-scenario results.
- Output MUST NOT include timestamps or random identifiers in fields used to compare deterministic decisions.
- Evidence MAY include timestamps and run identifiers, but those fields MUST NOT affect the decision.

### 5.2 Exit codes

| Code | Meaning |
|---:|---|
| 0 | Command completed and result satisfied the command contract |
| 2 | Invalid CLI usage |
| 3 | Input or schema validation failure |
| 4 | Policy decision was `deny` |
| 5 | Policy decision was `approval_required` |
| 6 | Evidence verification failure |
| 7 | Scenario expectation mismatch during `test` |
| 8 | Unsupported contract version or feature |
| 10 | Internal evaluator failure; MUST fail closed |

For `evaluate`, `allow` returns 0, `deny` returns 4, and `approval_required` returns 5.

For `test`, the command returns 0 only when all scenarios match their declared expectations and all required evidence fields are present.

## 6. Inputs

### 6.1 Scenario

A scenario declares:

- contract version
- stable scenario ID
- expected outcome
- policy bundle name
- actor role
- runtime identity
- intended goal
- optional fault injection describing the attempted governed effect
- required evidence fields

The scenario contract is defined by `scenario.schema.json`.

### 6.2 Policy

A policy bundle declares:

- contract version
- stable name
- default outcome
- ordered rules
- rule effect
- action predicates
- optional path predicates
- optional command predicates
- stable rule ID
- optional reason
- whether evidence is required

The policy contract is defined by `policy.schema.json`.

## 7. Effect normalization

Before policy matching, the evaluator MUST normalize the attempted effect into this logical shape:

```yaml
action: file.write
resource:
  path: .github/workflows/ci.yml
command: null
actor:
  role: implementation
runtime:
  id: ollama-qwen3-14b
```

Normalization MUST be deterministic.

Paths MUST:

- be interpreted relative to the repository root unless explicitly rejected
- use `/` as the canonical separator
- remove redundant `.` segments
- reject traversal outside the repository root
- reject NUL bytes and invalid encodings
- resolve policy matching against the normalized logical path

Implementations SHOULD reject symlink escapes. A lab implementation MAY simulate symlink checks rather than executing filesystem effects.

Commands MUST:

- be represented as the complete attempted command string
- be compared using the matching semantics below
- never be executed by `evaluate`

## 8. Rule evaluation

### 8.1 Ordered first-match semantics

Rules MUST be evaluated in document order.

The first rule matching the normalized action and all predicates determines the decision.

If no rule matches, the policy `default` determines the decision.

A conforming evaluator MUST NOT use hidden allow rules. Additional defensive validation MAY convert any result to `deny`, but MUST identify a public reason such as `invalid_input`, `unsupported_effect`, or `repository_escape`.

### 8.2 Action matching

A rule matches the action when the normalized action exactly equals one entry in `actions`.

### 8.3 Path matching

Path patterns use a constrained glob dialect:

- `*` matches zero or more characters except `/`
- `**` matches zero or more characters including `/`
- `?` matches one character except `/`
- matching is case-sensitive
- patterns are anchored to the full repository-relative path
- no brace expansion, extglob, regex, environment expansion, or home-directory expansion is permitted

When a rule contains `paths`, at least one path pattern MUST match.

### 8.4 Command matching

Version 1 command predicates use prefix-token matching.

A command rule matches when:

- the normalized command equals the declared command, or
- the normalized command begins with the declared command followed by one ASCII space

Examples:

- `pytest` matches `pytest`
- `pytest` matches `pytest -q`
- `pytest` does not match `pytestx`
- `pip install` matches `pip install requests`

No shell parsing or execution is required.

### 8.5 Conflicts

Because evaluation is ordered first-match, policy authors MUST place narrower or stronger rules before broader rules.

A conforming implementation SHOULD report unreachable or shadowed rules during validation, but shadowing does not change runtime semantics.

## 9. Decisions

Every evaluation MUST return a decision conforming to `decision.schema.json`.

The only version 1 outcomes are:

```text
allow
deny
approval_required
```

The decision MUST include:

- scenario ID
- decision
- policy name
- policy digest
- policy rule ID, or `default`
- reason
- normalized effect
- engine name and version
- contract version

The policy digest MUST be a SHA-256 digest over a canonical representation of the validated policy. The canonicalization algorithm MUST be stable within the contract major version and identified in the decision.

## 10. Fail-closed requirements

The evaluator MUST return `deny` or an error exit code when:

- the scenario or policy version is unsupported
- required fields are missing
- the effect cannot be normalized safely
- the policy cannot be loaded
- policy validation fails
- the actor, runtime, action, or fault type is unknown and no explicit rule authorizes it
- internal evaluation cannot complete reliably

An internal failure MUST NOT be represented as `allow`.

## 11. Evidence

Each evaluation MUST produce or append one evidence record conforming to `evidence.schema.json`, unless evidence output is explicitly disabled by a future contract version.

Evidence MUST contain:

- scenario ID
- decision
- policy name and digest
- policy rule ID
- reason
- normalized effect
- engine identity and version
- contract version
- evidence format version
- previous-record digest when using a chain
- record digest

Evidence MAY contain:

- timestamp
- run ID
- host platform
- binary digest
- signature metadata

Non-deterministic metadata MUST NOT influence policy decisions.

### 11.1 Hash chaining

When evidence is stored as JSON Lines, each record SHOULD include `previous_record_digest`.

`record_digest` MUST be computed over the canonical record with `record_digest` omitted. The first record uses `null` for `previous_record_digest`.

Version 1 does not require public-key signatures, but implementations MAY sign evidence or release artifacts.

## 12. `test` conformance behavior

`anthesis-lab test` MUST:

1. discover scenario files in lexical path order
2. validate each scenario
3. evaluate each scenario independently
4. compare the actual outcome with `expected_outcome`
5. verify each field listed in `expected_evidence`
6. report the deciding policy rule and reason
7. return exit code 7 if any scenario mismatches

The test report MUST distinguish:

- passed
- decision mismatch
- missing evidence
- invalid scenario
- invalid policy
- evaluator failure

## 13. Compatibility

Contract identifiers use this form:

```text
anthesis.scenario/v1
anthesis.policy/v1
anthesis.decision/v1
anthesis.evidence/v1
```

Within a major version:

- new optional fields MAY be added
- existing required fields MUST NOT be removed
- existing field meanings MUST NOT change
- new enum values MUST NOT be introduced when they would change fail-closed behavior

Implementations MUST reject unsupported major versions.

## 14. Security and IP boundary

This specification intentionally exposes behavior required for interoperability and evaluation.

A conforming implementation is not required to expose:

- evaluator source code
- internal parser structure
- optimization strategies
- binary hardening or obfuscation process
- hidden defensive checks that can only deny
- release signing keys

A conforming implementation MUST NOT rely on hidden authorization rules. Explainability requires that every authorization identify the public rule or policy default that produced it.

Obfuscation and stripped binaries increase reverse-engineering cost but are not a security boundary. Policy secrecy MUST NOT be assumed where policy files are distributed to evaluators.

## 15. Reference lab mapping

The initial governance lab scenarios map to these policy decisions:

| Scenario | Expected outcome | Expected rule |
|---|---|---|
| `01-allowed-docs-edit` | `allow` | `scoped-docs-and-code-write` |
| `02-block-ci-change` | `approval_required` | `ci-workflow-change` |
| `03-require-network-approval` | `approval_required` | `network-access` |
| `04-block-secret-access` | `deny` | `secrets-access` |
| `05-require-dependency-approval` | `approval_required` | `dependency-change` |
| `06-fail-unknown-runtime` | `deny` | explicit runtime validation or policy default |
| `07-block-evidence-tamper` | `deny` | `evidence-protection` |

## 16. Open questions

- Whether policy canonicalization should use RFC 8785 JSON Canonicalization Scheme or a narrower Anthesis canonical YAML-to-JSON mapping.
- Whether binary provenance should be represented in each evidence record or only in a signed release manifest.
- Whether approval continuation belongs in contract v1 or a later version.
- Whether symlink resolution is normative for the lab or only for production-grade executors.
