# Security Policy

Anthesis is a governance-oriented project for human and agent execution in software delivery workflows. Security review is central to the project.

## Reporting Security Issues

Do not disclose security-sensitive findings in public issues if they include operationally useful detail.

For now, report security concerns to the project maintainer directly through the contact channels listed on the public Anthesis or Micrantha pages.

## Areas of Interest

Security review is especially welcome for:

- MCP and tool invocation boundaries
- approval bypass risks
- actor identity and impersonation risks
- evidence integrity
- runtime trace evidence handling
- prompt, response, and retrieval data exposure
- secrets and environment handling
- replay and rollback semantics
- CI and GitHub Actions enforcement
- policy versioning and drift

## Runtime Trace Evidence

Runtime traces can contain sensitive execution details. Contributions involving trace evidence should consider:

- redaction before persistence
- minimal retention by default
- digest binding for evidence artifacts
- clear separation between debug traces and audit evidence
- access control for stored trace artifacts

## Governance Principle

Security controls should preserve Anthesis' central guarantee:

```text
No significant human or agent action should be treated as governed unless it is bound to actor identity, policy, approval state, repo context, and reviewable evidence.
```
