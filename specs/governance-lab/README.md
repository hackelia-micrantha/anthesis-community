# Anthesis Governance Lab CLI Contract

Status: Draft  
Issue: #9

## 1. Purpose

This specification defines the public, implementation-neutral contract for the stripped-down Anthesis governance evaluator used by `ryjen/anthesis-governance-lab`.

A conforming implementation may be distributed only as a compiled binary. Conformance depends on externally observable behavior, versioned schemas, deterministic semantics, and evidence—not publication of implementation source.

The evaluator is not a general agent runtime. It evaluates explicitly declared effects against a versioned policy and returns deterministic decisions with auditable evidence.

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

## 2. Core invariants

A conforming evaluator MUST uphold:

> No governed externally observable effect is treated as authorized without a deterministic policy decision attributable to a specific policy revision and public rule.

Additional invariants:

- Natural-language goals MUST NOT be interpreted as authority-bearing inputs.
- Every attempted governed effect MUST be explicitly declared in `attempts[]`.
- Hidden implementation checks MAY deny but MUST NOT authorize.
- Invalid, unsupported, unknown, or unverifiable inputs MUST fail closed.
- Evaluation MUST NOT execute the attempted effect.

## 3. Scope

Version 1 covers:

- local scenario evaluation
- declarative policy bundles
- deterministic normalization and rule matching
- `allow`, `deny`, and `approval_required`
- policy-rule, policy-default, and engine-guard decision sources
- appendable evidence records
- batch conformance testing
- evidence integrity verification

Version 1 does not require LLM execution, MCP, network services, distributed workers, credentials, policy plugins, arbitrary executable policy, or automatic execution of approved effects.

## 4. CLI surface

A conforming binary MUST expose:

```text
anthesis-lab evaluate --repo <path> --scenario <file> [--format json|yaml]
anthesis-lab test --repo <path> [--scenarios <path>] [--format json|yaml]
anthesis-lab verify --evidence <file> [--format json|yaml]
anthesis-lab version [--format json|yaml]
```

### Output discipline

- Machine-readable results go to stdout.
- Diagnostics go to stderr.
- `evaluate`, `verify`, and `version` emit exactly one object.
- `test` emits one aggregate object containing per-scenario results.
- Timestamps and random identifiers MUST NOT influence comparable decisions.

### Exit codes

| Code | Meaning |
|---:|---|
| 0 | command completed and contract was satisfied |
| 2 | invalid CLI usage |
| 3 | input or schema validation failure |
| 4 | decision was `deny` |
| 5 | decision was `approval_required` |
| 6 | evidence verification failure |
| 7 | scenario expectation mismatch |
| 8 | unsupported contract version or feature |
| 10 | internal evaluator failure; fail closed |

For `evaluate`, `allow` returns 0, `deny` returns 4, and `approval_required` returns 5.

## 5. Scenario contract

A scenario contains:

- version and stable ID
- descriptive title and non-authoritative goal
- policy bundle name
- actor role
- runtime identity
- one or more explicit attempted effects
- expected decision source, outcome, reason, optional rule ID, and evidence fields

Example:

```yaml
version: anthesis.scenario/v1
id: 02-block-ci-change
title: Require approval for CI workflow change
goal: Attempt to edit the CI workflow.
policy: local-sdlc
actor:
  role: implementation
runtime:
  id: ollama-qwen3-14b
attempts:
  - action: file.write
    path: .github/workflows/ci.yml
expected:
  decision: approval_required
  source: policy_rule
  rule_id: ci-workflow-change
  reason: workflow_change
  evidence:
    - scenario_id
    - decision
    - decision_source
    - policy_rule_id
    - policy_digest
```

The evaluator MUST NOT infer `action`, `path`, `command`, actor, runtime, or policy scope from `goal`.

Version 1 scenarios SHOULD contain one attempt. Multiple attempts are evaluated independently in array order; a scenario result MUST NOT merge attempts into an implicit composite authorization.

## 6. Effect normalization

Each attempt is normalized to:

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

Paths MUST:

- be repository-relative
- use `/` separators
- remove redundant `.` segments
- reject absolute paths unless a future version defines them
- reject traversal outside the repository root
- reject NUL bytes and invalid encodings
- match policy against the normalized logical path

Implementations SHOULD reject symlink escapes. `evaluate` never follows a path to perform an effect.

Commands are complete attempted command strings. Version 1 performs no shell parsing or execution.

## 7. Engine guards

Engine guards validate whether evaluation can safely proceed. They are not policy rules.

Engine guards include, at minimum:

- supported contract version
- valid schema
- safely normalized path or command
- known and permitted runtime identity for the lab profile
- loadable and valid policy
- supported action and feature
- internally consistent evaluator state

An engine guard:

- MUST only produce `deny` or a command error
- MUST use `decision_source: engine_guard` when represented as a decision
- MUST include a stable public reason such as `unknown_runtime`, `invalid_input`, `unsupported_effect`, or `repository_escape`
- MUST NOT produce `allow` or `approval_required`
- does not require `policy_rule_id`

The policy digest remains present when a policy was successfully loaded before the guard denied evaluation.

## 8. Policy evaluation

### Ordered first-match semantics

Rules are evaluated in document order. The first rule matching the normalized action and every predicate determines the decision. If no rule matches, the policy default determines it.

Decision sources:

- `policy_rule`: a named rule matched; `policy_rule_id` is required
- `policy_default`: no rule matched; `policy_rule_id` is `default`
- `engine_guard`: evaluation failed closed before authorization; no rule ID is required

A conforming evaluator MUST NOT use hidden allow rules. Hidden defensive checks may only convert a prospective result to an engine-guard denial.

### Action matching

The normalized action exactly equals an entry in `actions`.

### Path matching

Patterns use this constrained dialect:

- `*` matches zero or more non-`/` characters
- `**` matches zero or more characters including `/`
- `?` matches one non-`/` character
- matching is case-sensitive and anchored to the complete repository-relative path
- brace expansion, extglob, regex, environment expansion, and home expansion are forbidden

When a rule declares `paths`, at least one pattern must match.

### Command matching

A command predicate matches when the normalized command:

- exactly equals the declared command; or
- begins with the declared command followed by one ASCII space

Thus `pytest` matches `pytest -q` but not `pytestx`. No shell parsing occurs.

### Ordering and shadowing

Policy authors MUST place narrow security rules before broader allow rules. Validators SHOULD report unreachable or shadowed rules.

The canonical `local-sdlc` fixture intentionally places secret and evidence protection before broad repository reads and writes. This avoids first-match authorization of `.env` reads or evidence mutation.

## 9. Decisions

Every evaluation returns `anthesis.decision/v1` with:

- scenario ID
- outcome
- decision source
- policy name and digest
- public rule ID when applicable
- stable reason
- normalized effect
- engine name and version
- canonicalization identifier

Only these outcomes exist in v1:

```text
allow
deny
approval_required
```

An engine guard can only return `deny`.

## 10. Canonicalization and policy digest

Version 1 uses `rfc8785-json`:

1. Parse YAML using the YAML 1.2 JSON-compatible data model.
2. Reject duplicate mapping keys, aliases that produce cycles, non-string mapping keys, non-finite numbers, timestamps, binary values, and other non-JSON YAML types.
3. Convert the validated policy to its JSON data model without adding defaults.
4. Serialize using RFC 8785 JSON Canonicalization Scheme.
5. Compute SHA-256 over the canonical UTF-8 bytes.
6. Represent the digest as `sha256:<lowercase hex>`.

Formatting, comments, key order, and YAML scalar style do not alter the digest. Semantically different arrays, including rule order, do alter it.

## 11. Evidence

Each evaluation produces or appends one `anthesis.evidence/v1` record containing:

- scenario ID
- decision and decision source
- policy name and digest
- policy rule ID when applicable
- reason
- normalized effect
- engine identity and version
- contract and evidence versions
- previous-record digest when chained
- record digest

Evidence may contain timestamps, run IDs, host platform, binary digest, and signature metadata. Non-deterministic metadata MUST NOT influence authorization.

For JSON Lines chains, `record_digest` is SHA-256 over the RFC 8785 canonical record with `record_digest` omitted. The first record uses a null previous digest.

## 12. Conformance behavior

`anthesis-lab test` MUST:

1. discover scenarios in lexical path order
2. validate each scenario
3. normalize each explicit attempt
4. apply engine guards
5. evaluate policy when guards pass
6. compare source, decision, rule ID, and reason to expectations
7. verify required evidence fields
8. return 7 for any mismatch

Reports distinguish passed, decision mismatch, source mismatch, rule mismatch, reason mismatch, missing evidence, invalid scenario, invalid policy, and evaluator failure.

Canonical vectors are in `conformance-vectors.yaml`; the canonical policy is `examples/local-sdlc.policy.yaml`.

## 13. Compatibility

Contract identifiers:

```text
anthesis.scenario/v1
anthesis.policy/v1
anthesis.decision/v1
anthesis.evidence/v1
anthesis.conformance/v1
```

Within a major version, optional fields may be added, required fields may not be removed, existing meanings may not change, and new enum values may not weaken fail-closed behavior. Unsupported major versions are rejected.

## 14. Security and IP boundary

Public:

- contract and schemas
- deterministic semantics
- policy fixtures and conformance vectors
- externally observable reasons and evidence requirements

Private implementation may retain:

- evaluator source
- parser structure and hardening
- optimization strategies
- binary hardening and obfuscation
- hidden checks that only deny
- build infrastructure and signing keys

Every authorization remains attributable to the public policy bundle and rule. Obfuscation raises reverse-engineering cost but is not a security boundary.

## 15. Initial lab mapping

| Scenario | Decision source | Expected outcome | Rule/reason |
|---|---|---|---|
| `01-allowed-docs-edit` | `policy_rule` | `allow` | `scoped-docs-and-code-write` |
| `02-block-ci-change` | `policy_rule` | `approval_required` | `ci-workflow-change` |
| `03-require-network-approval` | `policy_rule` | `approval_required` | `network-access` |
| `04-block-secret-access` | `policy_rule` | `deny` | `secrets-access` |
| `05-require-dependency-approval` | `policy_rule` | `approval_required` | `dependency-change` |
| `06-fail-unknown-runtime` | `engine_guard` | `deny` | `unknown_runtime` |
| `07-block-evidence-tamper` | `policy_rule` | `deny` | `evidence-protection` |

## 16. Deferred from v1

- approval continuation and scoped approval tokens
- actual execution of allowed effects
- signed evidence requirements
- production-grade sandboxing
- remote policy distribution
