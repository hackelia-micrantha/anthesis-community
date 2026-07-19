# Anthesis Governance Lab CLI Contract

Status: Accepted  
Issue: #9

## 1. Purpose

This specification defines the public, implementation-neutral contract for the stripped-down Anthesis governance evaluator consumed by `ryjen/anthesis-governance-lab`.

A conforming implementation may be distributed only as a compiled binary. Conformance depends on externally observable behavior, schemas, deterministic semantics, conformance vectors, and evidence—not publication of implementation source.

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

## 2. Core invariants

> No governed externally observable effect is treated as authorized without a deterministic policy decision attributable to a specific policy revision and public rule.

A conforming evaluator MUST also enforce:

- Natural-language goals are descriptive and MUST NOT carry authority.
- Every attempted effect is explicitly declared.
- Hidden implementation checks MAY deny but MUST NOT authorize.
- Invalid, unsupported, unknown, or unverifiable inputs fail closed.
- Evaluation does not execute the attempted effect.
- Version 1 policies use `default: deny`.

## 3. CLI

```text
anthesis-lab evaluate --repo <path> --scenario <file> [--format json|yaml]
anthesis-lab test --repo <path> [--scenarios <path>] [--format json|yaml]
anthesis-lab verify --evidence <file> [--format json|yaml]
anthesis-lab version [--format json|yaml]
```

Machine-readable results go to stdout. Diagnostics go to stderr.

| Code | Meaning |
|---:|---|
| 0 | command completed and contract was satisfied |
| 2 | invalid CLI usage |
| 3 | input or schema validation failure |
| 4 | decision was `deny` |
| 5 | decision was `approval_required` |
| 6 | evidence verification failure |
| 7 | scenario expectation mismatch |
| 8 | unsupported version or feature |
| 10 | internal failure; fail closed |

## 4. Scenario contract

Version 1 scenarios contain exactly one attempted effect. This avoids ambiguous aggregation, evidence, and exit-code semantics.

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

The evaluator MUST NOT infer the action, path, command, actor, runtime, or policy scope from `goal`.

Attempt shapes are closed:

- `file.read`, `file.write`, and `file.delete` require `path` and forbid `command`.
- `command.run` and `network.request` require `command` and forbid `path`.
- action-only operations accept neither path nor command.
- unknown shapes fail schema validation or an engine guard.

## 5. Runtime profile

Runtime authority is declared by `anthesis.lab-profile/v1` rather than hidden implementation configuration.

```yaml
version: anthesis.lab-profile/v1
name: local
allowed_runtimes:
  - ollama-qwen3-14b
```

A runtime absent from `allowed_runtimes` produces:

```yaml
decision: deny
decision_source: engine_guard
reason: unknown_runtime
```

A runtime profile is public conformance input. Implementations MUST NOT silently add runtimes that can authorize effects.

## 6. Normalization

A file attempt normalizes to:

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

Paths MUST be repository-relative, use `/`, remove redundant `.` segments, reject absolute paths and repository escape, reject NUL bytes and invalid encodings, and match policy against the normalized logical path. Implementations SHOULD reject symlink escapes.

Commands are complete attempted strings. Version 1 performs no shell parsing or execution.

## 7. Engine guards

Engine guards validate supported versions, schema validity, safe normalization, runtime registration, policy loading, supported effects, and evaluator integrity.

An engine guard:

- can only produce `deny` or a command error
- uses `decision_source: engine_guard`
- uses a stable public reason such as `unknown_runtime`, `invalid_input`, `unsupported_effect`, or `repository_escape`
- MUST NOT include `policy_rule_id`
- MUST NOT produce `allow` or `approval_required`

## 8. Policy evaluation

Version 1 policy bundles MUST declare `default: deny` and every rule MUST declare a stable `reason`.

Rules are evaluated in document order. The first rule matching the action and every declared predicate determines the decision. If no rule matches, the policy default produces `deny`, `decision_source: policy_default`, `policy_rule_id: default`, and reason `policy_default`.

Decision sources are:

- `policy_rule`: named public rule matched
- `policy_default`: no rule matched
- `engine_guard`: evaluation failed closed before authorization

Hidden allow rules are forbidden.

### Matching

Action matching is exact.

Path patterns use a constrained dialect:

- `*` matches zero or more non-`/` characters
- `**` matches zero or more characters including `/`
- `?` matches one non-`/` character
- matching is case-sensitive and anchored to the complete path
- brace expansion, extglob, regex, environment expansion, and home expansion are forbidden

A command matches when it equals the declared command or begins with that command followed by one ASCII space. Thus `pytest` matches `pytest -q` but not `pytestx`.

Narrow deny and approval rules MUST precede broader allow rules. The canonical policy places secret and evidence protection before repository reads and writes.

## 9. Canonicalization and digests

Version 1 uses `rfc8785-json`:

1. Parse YAML using a JSON-compatible model.
2. Reject duplicate keys, non-string mapping keys, cyclic aliases, timestamps, binary values, non-finite numbers, and other non-JSON YAML values.
3. Validate the object without injecting schema defaults.
4. Serialize using RFC 8785 JSON Canonicalization Scheme.
5. Compute SHA-256 over canonical UTF-8 bytes.
6. Encode as `sha256:<lowercase hex>`.

The canonical policy fixture digest is pinned in `conformance-vectors.yaml`. Formatting and mapping order do not affect it; rule array order does.

The community validator uses deterministic JSON serialization that is byte-equivalent to RFC 8785 for the current non-numeric fixtures. Production implementations MUST use complete RFC 8785 canonicalization for the full accepted input model.

## 10. Decisions and evidence

Decisions conform to `anthesis.decision/v1` and include scenario, outcome, decision source, policy and digest, canonicalization, reason, normalized effect, engine identity, and the public rule ID when applicable.

Evidence conforms to `anthesis.evidence/v1`. It contains the same authorization facts plus previous-record and record digests. JSON Lines evidence SHOULD be hash-chained. `record_digest` is computed over the canonical record with `record_digest` omitted.

Engine-guard evidence MAY include `configured_runtime`, but MUST omit `policy_rule_id`.

## 11. Conformance

`anthesis-lab test` discovers scenarios in lexical path order, validates each input, evaluates it independently, compares decision/source/rule/reason, verifies expected evidence fields, and returns 7 on any mismatch.

The community validation workflow MUST check more than schema shape. It validates:

- strict YAML restrictions
- policy, runtime-profile, scenario, decision, and evidence schemas
- exact policy digest
- exact evidence-record digest
- first-record chain initialization with `previous_record_digest: null`
- decision and evidence fixture consistency with canonical scenario 01
- all seven canonical policy outcomes
- decision sources, rule IDs, and reasons
- required evidence availability

The canonical vectors are normative interoperability tests.

## 12. Compatibility and IP boundary

Contract identifiers are:

```text
anthesis.scenario/v1
anthesis.policy/v1
anthesis.lab-profile/v1
anthesis.decision/v1
anthesis.evidence/v1
anthesis.conformance/v1
```

Within a major version, optional fields may be added, required fields may not be removed, and meanings or authorization-relevant enum values may not change. Unsupported major versions are rejected.

The public repository exposes contracts, schemas, semantics, examples, and conformance vectors. It does not require publication of evaluator source, parser internals, optimization, binary hardening, obfuscation, signing keys, or deny-only defensive implementation details.

Every authorization must remain attributable to a public rule. Obfuscation increases reverse-engineering cost but is not a security boundary.
