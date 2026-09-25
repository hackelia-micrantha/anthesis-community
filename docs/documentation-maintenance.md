# Documentation maintenance contract

**Adoption:** Micrantha shared `documentation-sync` default, unchanged.

This repository does not maintain a local copy of the shared skill. The organization contract in `hackelia-micrantha/.github/skills/documentation-sync/SKILL.md` applies unless this file explicitly narrows a project-specific boundary.

## Authority

- `hackelia-micrantha/anthesis` remains authoritative for the private Anthesis implementation, policy/evaluator semantics, security architecture, and implementation maturity.
- `hackelia-micrantha/anthesis-community` owns public contracts, specifications, release artifacts, product documentation, website source, project brief, whitepaper distribution, and public claim wording.
- `ryjen/anthesis-governance-lab` is an independent registered conformance/testbed consumer. Its scenarios and run evidence do not become Anthesis implementation authority.
- Dubnium is a bounded reference execution environment and use case. Private Dubnium host state is not a source for public Anthesis capability claims.

Public/community visibility does not grant implementation authority and does not permit private source, operational details, or inaccessible internal links to be projected here.

## Maintained public surfaces

- root `README.md`;
- `docs/product/` product, integration, trial, and evaluator guidance;
- `specs/` implementation-neutral published contracts;
- `web/` public site, project brief, security policy, sitemap, whitepaper, and related static assets;
- public evaluator/release material intentionally projected into this repository.

Generated or released artifacts must be updated through their owning build/publication contract rather than hand-edited as independent source.

## Validation

Use the narrowest applicable check first.

### Public site source and browser behavior

```bash
python scripts/validate_public_site.py
cd test
npm ci --no-audit --no-fund
npx playwright install --with-deps chromium
npm run test:e2e
```

The repository `Public Site` GitHub workflow is the exact PR/push evidence surface for this path. Source validation and Chromium browser tests are independent checks and should not be collapsed.

### Governance Lab public contracts

```bash
python scripts/validate_governance_lab_contract.py
python scripts/validate_promoted_governance_contracts.py
```

The `Governance Lab Contract` workflow is the repository-owned CI evidence for these validators. Python dependency installation remains defined by that workflow.

### Whitepaper

`web/anthesis.pdf` and `web/anthesis.pdf.manifest.json` are validated together by the `Whitepaper integrity` workflow. The manifest binds the PDF digest, private-source revision reference, document metadata, and source/build-input digests. Do not replace that publication trace with prose assertions.

## Deployment boundary

`web/` is the intended public deploy payload and `wrangler.toml` defines the Cloudflare static-assets project. Deterministic live deployment identity/fingerprint, deployment owner, and artifact-set parity remain tracked by repository issue #18.

A documentation edit or successful source CI run does **not** authorize deployment and does not prove which revision is currently live. Do not mark a landing page or whitepaper deployment current until #18-style source/fingerprint evidence supports it.

## Claim rules

- Keep deterministic Governance Lab evaluation separate from runtime effect enforcement.
- Keep the canonical 7-scenario contract, 9-pack/27-scenario general catalog, and 24-case inference-integrity contract separately labeled.
- Do not describe a reference integration as universal non-bypassable enforcement.
- Data sovereignty is an end-to-end deployment property; self-hosting or Anthesis policy evaluation alone does not establish residency, jurisdiction, or confinement.
- Release/install claims require exact release/artifact evidence; source availability or passing documentation CI is insufficient.

## Local specialization

No additional project-local `documentation-sync` specialization is currently required. Add one only when Anthesis Community develops a repeatable documentation rule that materially narrows or extends the shared contract. Ordinary project facts belong in their canonical product/specification sources rather than in a duplicated skill.

## Recurrence

Prefer event-driven review after public contract changes, evaluator/release promotion, public/private topology changes, deployment changes, or material capability/maturity changes. Periodic read-only reconciliation may supplement those triggers. Any unattended mutation, publication, or deployment requires separate authority.
