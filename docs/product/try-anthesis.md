# Try Anthesis

Use this path when you want to answer one concrete question quickly:

> Can a consequential agentic effect be allowed through an Anthesis-controlled boundary while an equivalent raw bypass is hard-denied?

The reference trial uses the public [Anthesis Governance Lab](https://github.com/ryjen/anthesis-governance-lab). It combines the signed `anthesis-lab` evaluator with a deliberately small tool-wrapper runtime harness and a disposable Git repository.

## Run the reference trial

Clone the Governance Lab, then from its repository root:

```bash
bash scripts/acquire-anthesis-lab.sh
bash scripts/run-reference-trial.sh
```

Inspect the actual repository mutation and its evidence:

```bash
git -C .anthesis/reference-trial diff -- docs/onboarding.md
jq . .anthesis/reference-trial/decision.json
jq . .anthesis/reference-trial/reference-trial.json
```

The evaluator acquisition is pinned and verifies the published release identity, provenance, Sigstore material, archive/checksum integrity, binary identity, version, and public contract set before use.

## What happens

```text
reference supervisor
  -> anthesis-lab evaluates exact file.write request
  -> runtime exposes only anthesis.repo_write
  -> exact action/path checked
  -> disposable Git repository mutated
  -> decision + outcome evidence recorded

raw bypass
  -> raw.repo_write
  -> runtime registry lookup
  -> HARD DENIAL: tool_not_registered
  -> repository state unchanged
```

The governed effect is the canonical `file.write` to `docs/onboarding.md`. The trial creates a baseline Git commit, performs the authorized mutation, and leaves an inspectable diff.

It then performs two negative checks:

1. `raw.repo_write` attempts the same mutation and is rejected because that tool is not registered.
2. The registered `anthesis.repo_write` attempts `.github/workflows/ci.yml` and is rejected because the path is outside the evaluator-authorized effect.

Both denials are checked to leave repository state unchanged.

## Enforcement boundary

**Integration mode:** tool wrapper / constrained runtime registry.

**Enforcement point:** the reference runtime's tool registry plus exact-effect dispatcher.

The simulated agent-visible registry exposes only `anthesis.repo_write` for this effect. It exposes no raw repository writer, shell, filesystem, Git, network, or provider credential path. The dispatcher also requires the requested action and path to match the exact `anthesis.decision/v1` effect before mutation.

That runtime restriction is what makes the demonstrated raw bypass impossible **inside this reference composition**. The denial is therefore a runtime block, not merely an advisory evaluator result.

## What the output tells you

`.anthesis/reference-trial/reference-trial.json` is a non-normative evaluator record. It identifies:

- integration mode and enforcement point;
- exact governed action and path;
- reference supervisor/specialist plus evaluator runtime identity;
- policy decision, source, rule, reason, policy digest, and request binding;
- a lifecycle/Envelope correlation reference;
- before/after content hashes and Git diff digest;
- bypass attempts, hard-denial reasons, and state-unchanged checks;
- the exact runtime restriction and residual trusted components.

The Envelope correlation reference carries workflow context only; it is not an authority grant. See [Anthesis Envelope](envelope.md).

This reference path uses an `allow` decision, so approval and capability fields are intentionally null. Trials of approval-gated or capability-bound effects must bind those artifacts to the exact effect rather than inferring authority from this example.

## What this does not prove

The local harness does not claim containment against a hostile local OS user or administrator. It also does not prove that arbitrary agent code remains non-bypassable if it is given shell, filesystem, Git, network, raw MCP/provider access, or raw credentials.

Those are residual trust boundaries. Giving the simulated agent any such direct effect path invalidates the reference composition's non-bypassability claim.

A production trial must establish the equivalent restriction in its real runtime using tool/MCP registry control, credential placement, gateways, downstream capability validation, sandboxing, or another explicit enforcement mechanism.

## Evaluate a real workflow next

Do not stop at the reference harness. Apply the same questions to a real consequential workflow and score the six [trial criteria](trial-criteria.md):

- enforceability;
- attribution;
- least privilege;
- human approval;
- auditability;
- bypass resistance.

For integration-specific bypass assumptions, use [Integration Modes](integrations/README.md). For the deterministic evaluator's public/non-public proof boundary, use [Governance Lab CLI](governance-lab-cli.md).

The goal is not to show that Anthesis can return a decision. The goal is to establish that the selected runtime boundary makes the decision authoritative for the effect you care about.
