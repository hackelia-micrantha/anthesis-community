# Contributing to Anthesis Community

Anthesis Community publishes the public contracts, specifications, documentation, release/proof artifacts, and validation surfaces that can be reviewed independently of the closed core implementation.

Contributions are welcome when they strengthen those public surfaces without crossing the implementation or disclosure boundary.

## Useful contributions

High-value contributions include:

- security and governance review of authorization, approvals, capabilities, evidence, provenance, replay, and bypass assumptions;
- implementation-neutral contract and specification feedback;
- safe synthetic Governance Lab or conformance scenarios;
- integration requirements and adapter/gateway design feedback;
- documentation corrections, threat-model gaps, usability issues, and reproducibility findings;
- independent reproduction of public claims and release artifacts;
- interoperability findings from existing agent, MCP, tool, gateway, or runtime environments.

## Agentic-system trial program

Anthesis is actively looking for existing agentic systems that can participate in bounded trial runs.

A useful trial starts with one real but low-risk consequential effect in an existing system—for example a repository mutation, privileged tool call, deployment step, external API action, or data-transfer decision. The goal is not to retrofit an entire platform. It is to learn whether Anthesis can govern one meaningful effect without hiding bypass paths or imposing unacceptable operational friction.

Useful trial systems include coding agents, supervisor/specialist architectures, MCP-based tool systems, autonomous developer workflows, local/self-hosted agents, CI/release agents, and other systems where an agent can produce externally observable effects.

Trial feedback should capture:

- integration effort and architectural changes required;
- direct or alternate authority paths discovered during bypass analysis;
- policy or capability concepts that do not map cleanly to the host system;
- approval and operator-experience friction;
- evidence that is missing, ambiguous, excessive, or hard to verify;
- runtime overhead and operational complexity;
- failure modes, false assumptions, and cases where Anthesis is not a good fit.

Negative results are first-class feedback. A trial that shows the integration is too invasive, cannot close an important bypass, or needs a different contract is useful evidence.

For a trial involving non-public architecture or environment details, contact **services@micrantha.com** with the subject **Anthesis agentic system trial** before sharing sensitive material.

## Design-partner feedback

Real-world integration feedback is particularly useful when it can be reduced to reusable requirements or safe synthetic examples.

Good topics include:

- which agentic effects must be governed;
- what data must remain local or under a specific authority boundary;
- where raw credentials, filesystem, shell, network, or provider access could bypass policy;
- which actions require human approval;
- what evidence must be retained or independently verified;
- how an existing platform could enforce Anthesis decisions.

Do not place confidential employer/customer information, credentials, private repository content, production topology, logs, incidents, proprietary source, or non-public policy in a public issue or pull request.

## Public / private implementation boundary

The core Anthesis implementation remains closed source and all rights reserved unless separately licensed. A contribution to this repository does not grant access to the private core, production systems, private roadmap, credentials, or operational data.

Public work should remain independently useful and reviewable without private implementation details.

## Contribution workflow

1. Start with a focused issue or discussion-sized problem statement when the change affects a contract, security property, or integration boundary.
2. State the problem, trust assumptions, expected behavior, and negative cases.
3. Use synthetic fixtures and examples.
4. Keep changes narrowly scoped and include reproducible validation where practical.
5. Update related documentation and proof/conformance material when a public claim changes.
6. Expect security-sensitive or authority-changing work to require deeper review before merge.

Documentation-only corrections can usually go directly to a pull request when they do not change normative behavior.

## Security-sensitive findings

Do not publish secrets, exploitable private-system details, or sensitive operational evidence in a public issue. For a vulnerability that cannot be safely disclosed publicly, use Micrantha's published security contact at **security@micrantha.com**.

## Strategic collaboration

For design partnerships, product/integration collaboration, infrastructure support, sponsorship, or Micrantha-wide strategic and co-founder conversations, see the [Micrantha collaboration overview](https://github.com/hackelia-micrantha/.github/blob/main/profile/README.md#looking-for-collaborators).

Public participation never requires a commercial relationship and does not imply endorsement, roadmap priority, certification, procurement, or access to private implementation.
