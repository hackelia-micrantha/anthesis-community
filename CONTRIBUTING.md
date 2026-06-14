# Contributing

Anthesis is currently in active development. Public collaboration is focused on documentation, specifications, review, threat modeling, and design feedback.

## Useful Contribution Areas

Good contribution areas include:

- RFC review
- terminology cleanup
- threat model review
- governance model feedback
- evidence and replay model feedback
- MCP/tool-control surface analysis
- GenAI trace evidence integration notes
- examples and diagrams

## Current Boundary

This repository is public for review and discussion, but not all Anthesis implementation work is necessarily open for external contribution yet.

Before opening implementation-heavy changes, prefer opening an issue or discussion describing the proposed change and its governance impact.

## Review Expectations

Helpful reviews should identify:

- conceptual drift
- duplicated concepts
- missing links between RFCs
- security or privacy gaps
- unclear MVP boundaries
- unclear actor, approval, or evidence semantics
- places where Anthesis is taking ownership of something better handled by an adapter or external system

## Design Posture

Anthesis should stay focused on governed execution.

It should avoid absorbing adjacent systems wholesale. Agent frameworks, tracing systems, CI systems, queues, and observability backends should usually remain integrations behind clear contracts.

## Security-Sensitive Contributions

For security-sensitive findings, avoid posting exploitable details in public issues. Use the repository security policy when available, or contact the maintainer directly.
