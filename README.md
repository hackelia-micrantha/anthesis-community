---
category: Overview
publish: false
summary: >
  Full Anthesis overview, architecture, governance, and testing guidance.
---

# Project Anthesis

> *Anthesis* — the phase in which a flower is fully open and capable of function.

**Project Anthesis** is an agentic software delivery system designed to ensure autonomous actions occur **only when context is complete, risk is understood, and authority is explicit**.

Anthesis treats AI execution as a *governed state transition*, not a default behavior.

***

## Core Principles

1. **Governed Autonomy**  
   Agents may act independently, but never without policy, context, and traceability.

2. **Human Authority First**  
   Humans remain the final arbiters through approvals, overrides, and ownership.

3. **Deterministic Execution**  
   Every agent run is reproducible: same inputs, same context, same outcome.

4. **Auditability by Design**  
   All actions, approvals, and artifacts are recorded with immutable metadata.

5. **Living Architecture**  
   Specifications, prompts, and policies evolve continuously as first-class artifacts.

***

## System Overview

Project Anthesis coordinates a team of specialized agents across the full Software Development Lifecycle (SDLC):

- Requirements
- Analysis & Design
- Implementation
- Testing
- CI/CD & Maintenance

The system is composed of four primary pillars:

1. **Git Repository** — Source of truth for all artifacts
2. **Phloem (MCP Server)** — Orchestration, policy enforcement, and audit layer
3. **n8n** — Workflow automation, approvals, notifications
4. **LLM** — LLM inference and embeddings

All services run within a secure private network and communicate through explicit APIs.

## Architecture at a Glance

```ascii
Git Repo ──▶ Phloem (MCP) ──▶ LLM
   ▲            │            │
   │            ▼            │
Human        SQLite      Embeddings
Editors      (Audit + Vectors)
   │            ▲
   ▼            │
  n8n ◀─────────┘
```

***

## Repository Structure

```tree
anthesis/
├── agents/            # Agent role definitions
├── prompts/           # Prompt templates
├── instructions/      # Shared rules and conventions
├── specs/             # Formal specifications (APIs, schemas, UX)
├── requirements/      # Product and system requirements
├── architecture/      # ADRs and system design docs
├── inflorescence/     # Multi-agent coordination graphs
├── calyx/             # Approval policies and risk rules
├── meristem/          # RFCs and living documents
├── services/          # MCP server(s) and workers (phloem, xylem)
├── tooling/           # Anthesis CLI and supporting tooling
├── plugins/           # Plugin manifests, scripts, and outputs
├── config/            # Runtime configuration (phloem, xylem, plugins, AI)
├── docs/              # Planning, drafts, diagrams, usage examples
├── web/               # Static web artifacts
├── cicd/              # CI/CD definitions
├── observability/     # Logs, metrics, traces
├── n8n/               # Workflow automation assets
├── tasks/             # Task tracking and work items
└── trees/             # Repository trees and inventories
```

Planning guidance:

- See `docs/planning/README.md` for why Anthesis prefers planning docs and when
  to use planning docs vs task-only updates.

***

## The Anthesis Lifecycle

Every autonomous action follows a controlled lifecycle:

1. **Pre-Bloom** — Artifact change or event detected
2. **Context Assembly** — Relevant artifacts retrieved via embeddings
3. **Calyx Gate** — Policy and risk evaluation
4. **Approval** — Human or automated authorization
5. **Anthesis** — Agent executes with full context
6. **Dormancy** — Completion, rollback, or safe halt

This lifecycle ensures that autonomy is *earned*, not assumed.

***

## Usage Example

See `docs/usage_example.md` for a concrete SDLC walkthrough using Anthesis.

***

## Approvals & Governance

Anthesis supports multiple approval surfaces:

- Slack (one-click approve/reject)
- Email (signed links)
- GitHub / GitLab Pull Requests

Approval requirements vary by artifact type and risk classification.

All approvals are recorded with:

- Commit hash
- Timestamp
- Reviewer identity
- Policy version

***

## Human-in-the-Loop by Default

Humans may:

- Edit the repository directly
- Trigger agentic workflows via commits
- Override or halt agents at any stage
- Replay or audit any past execution

Anthesis is designed so that **manual and autonomous workflows coexist** without conflict.

***

## Security Model

- Private networking via Tailscale
- Short-lived credentials
- Principle of least privilege
- Full execution audit trail
- Secrets isolated from prompts and artifacts

Trust is never implicit.

***

## Status

Project Anthesis is under active development.

Key components:

- RFC-driven architecture
- Local-first execution
- Policy-governed autonomy

Expect rapid iteration.

***

## Testing

Phloem (MCP) tests live in `services/phloem/tests`. Run them from the repo root:

```bash
python -m pip install -e .
python -m pytest services/phloem/tests
```

If you update migrations or Alembic configuration while running Phloem via Docker, restart the container (`docker compose down` then `docker compose up phloem`) so the new migration state is picked up.

To run the Xylem locally:

```bash
docker compose up phloem xylem 
```

Dispatch flow notes:

- Async/deferred runs are queued and published to Xylem.
- The xylem claims executions (`/v1/executions/{id}/claim`) before dispatching.
- Healthchecks: Phloem on `${ANTHESIS_PORT:-8088}`, xylem on `8099`.
- Diagram: `docs/diagrams/dfd_execution_dispatch.md`.
- Exchange-based fan-out can be configured in `config/xylem.yaml`; env vars may override.
