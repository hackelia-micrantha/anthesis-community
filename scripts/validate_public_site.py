#!/usr/bin/env python3
"""Validate the static Anthesis public-site content contract."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPO_ROOT / "web"
INDEX_PATH = WEB_ROOT / "index.html"
BRIEF_PATH = WEB_ROOT / "project-brief.html"
APP_PATH = WEB_ROOT / "app.js"
PROOF_CSS_PATH = WEB_ROOT / "proof.css"

INTEGRATION_MODES = (
    "Tool wrapper / invoke",
    "MCP mediation",
    "Gateway / sidecar",
    "Capability tokens",
    "SDK wrapper",
    "Sandboxed runtime",
)

MATURITY_LABELS = (
    "Runnable now",
    "Reference integration",
    "In development",
)

PROOF_MARKERS = (
    "7 canonical governance scenarios",
    "9 packs / 27 scenarios",
    "24 inference-integrity scenarios",
)


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[str] = []
        self.main_depth = 0
        self.main_sections = 0
        self.text_parts: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        attributes = dict(attrs)
        element_id = attributes.get("id")
        if element_id:
            self.ids.append(element_id)

        for name in ("href", "src"):
            value = attributes.get(name)
            if value:
                self.references.append(value)

        if tag == "main":
            self.main_depth += 1
        elif tag == "section" and self.main_depth == 1:
            self.main_sections += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "main":
            self.main_depth -= 1

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text:
            self.text_parts.append(text)

    @property
    def text(self) -> str:
        return " ".join(self.text_parts)


def parse_document(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_local_references(path: Path, parser: DocumentParser) -> None:
    ids = set(parser.ids)
    require(len(ids) == len(parser.ids), f"duplicate id in {path}: {parser.ids}")

    for reference in parser.references:
        parsed = urlsplit(reference)
        if parsed.scheme or parsed.netloc or reference.startswith("mailto:"):
            continue
        if reference.startswith("#"):
            require(reference[1:] in ids, f"missing anchor {reference} in {path}")
            continue

        relative_path = parsed.path
        if not relative_path:
            continue
        target = (path.parent / relative_path).resolve()
        require(
            target == WEB_ROOT.resolve() or WEB_ROOT.resolve() in target.parents,
            f"local reference escapes web root in {path}: {reference}",
        )
        require(target.exists(), f"missing local asset in {path}: {reference}")

        if parsed.fragment and target.suffix == ".html":
            target_parser = parse_document(target)
            require(
                parsed.fragment in set(target_parser.ids),
                f"missing anchor #{parsed.fragment} in {target}",
            )


def require_public_proof_model(text: str, surface: str) -> None:
    for marker in PROOF_MARKERS:
        require(marker in text, f"{surface} proof model missing: {marker}")
    require(
        "24 inference-integrity" in text and "27" in text and "separate" in text,
        f"{surface} does not distinguish the 24-case and 27-case surfaces",
    )


def validate_homepage(parser: DocumentParser) -> None:
    text = parser.text
    refs = " ".join(parser.references)
    require(parser.main_sections == 9, "homepage must contain nine main sections plus the hero")
    require("Portable, self-hostable data sovereignty for agentic AI" in text,
            "sovereignty hero eyebrow missing")
    require(
        "Your agents. Your rules." in text,
        "authorization and human authority headline missing",
    )
    require("Keep control where your data lives." in text,
            "data sovereignty band missing")
    require("Run an authorized write. Attempt a bypass." in text, "reference trial heading missing")
    require("Keep your data under your authority, from a laptop to a self-hosted system." in text,
            "local-first use cases missing")
    require("Ollama" in text and "MacBook" in text and "turnkey" in text,
            "local target use case or readiness disclosure missing")
    require("how agents access, modify, and transmit" in text,
            "data sovereignty must cover agent access, modification, and transfer")
    require("does not guarantee local data handling" in text,
            "sovereignty claims must acknowledge runtime and data-path limits")
    require("Enforcing adapter" in text and "Source of truth" in text,
            "model-to-effect authorization path missing")
    require("Where Anthesis fits alongside other AI platforms." in text,
            "platform responsibility map missing")
    for platform in ("Bedrock", "SageMaker", "Copilot Studio", "UiPath", "Power Platform"):
        require(platform in text, f"platform comparison missing: {platform}")
    require("Data sovereignty is an end-to-end property" in text,
            "data-sovereignty boundary missing")
    require("docs/product/where-anthesis-fits.md" in refs,
            "use-case and platform responsibility document missing")
    require("Try Anthesis" in text, "reference trial primary action missing")
    require("docs/product/try-anthesis.md" in refs, "public trial walkthrough link missing")
    require("anthesis-community" in refs, "GitHub community navigation link missing")
    require("Challenge the governance boundary with real requirements." in text,
            "collaboration section missing")
    require("CONTRIBUTING.md" in refs, "public contribution guide link missing")
    require("looking-for-collaborators" in refs,
            "Micrantha collaboration overview link missing")
    require("disposable Git repository" in text, "reference trial scope missing")
    require("not universal agent containment" in text, "reference trial trust boundary missing")
    require("Governance Lab" in text and "Dubnium" in text, "proof paths missing")
    require("Personal AI system" in text and "not a generally available product" in text,
            "Dubnium personal-use-case and availability distinction missing")
    require("not in the runtime critical path" in text, "Governance Lab runtime boundary missing")
    require("does not define policy authority" in text, "Dubnium policy boundary missing")
    require("What prevents the agent" in text, "central bypass question missing")
    require("full-verification.md" in refs, "full verification link missing")
    require("inference-integrity-demo.md" in refs, "inference runbook link missing")
    require_public_proof_model(text, "homepage")
    for label in MATURITY_LABELS:
        require(label in text, f"homepage maturity label missing: {label}")


def validate_project_brief(parser: DocumentParser) -> None:
    text = parser.text
    refs = " ".join(parser.references)
    require(parser.main_sections == 5, "project brief must have five focused sections")
    require(
        "Portable, self-hostable governance for data sovereignty in agentic AI." in text,
        "plain-language project definition missing",
    )
    require("does not make an AI model's reasoning deterministic" in text,
            "deterministic-decision distinction missing")
    require("the surrounding tool, gateway, credential boundary, or runtime" in text,
            "runtime enforcement distinction missing")
    require("hard-denied with repository state unchanged" in text,
            "reference trial blocked-bypass evidence missing")
    require("What success looks like" in text,
            "design-partner evaluation goals missing")
    require("personal self-hosted AI system" in text and "public release may follow later" in text,
            "project brief must distinguish Dubnium personal system from a public release")
    require("Product goal:" in text and "Evaluation request:" in text,
            "design-partner invitation missing")
    for goal in ("Authorization:", "Bypass resistance:", "Attribution:", "Human approval:", "Adoption:"):
        require(goal in text, f"project brief outcome missing: {goal}")
    require("docs/product/try-anthesis.md" in refs,
            "reference trial entry point missing")
    require("docs/product/integrations/README.md" in refs,
            "integration detail link missing")
    require("docs/product/trial-criteria.md" in refs,
            "trial criteria link missing")
    require("full-verification.md" in refs,
            "public proof verification link missing")
    require("anthesis-community" in refs,
            "community link missing")
    for label in MATURITY_LABELS:
        require(label in text, f"project brief maturity label missing: {label}")


def validate_supporting_assets(
    index_parser: DocumentParser,
    brief_parser: DocumentParser,
) -> None:
    require(PROOF_CSS_PATH.exists(), "governed-agent proof stylesheet missing")
    require((WEB_ROOT / "site-theme.css").exists(), "shared policy-site theme missing")
    app_text = APP_PATH.read_text(encoding="utf-8")
    css_text = PROOF_CSS_PATH.read_text(encoding="utf-8")

    for path, parser in (
        (INDEX_PATH, index_parser),
        (BRIEF_PATH, brief_parser),
    ):
        require("proof.css" in parser.references, f"proof stylesheet is not linked in {path}")
        require("app.js" in parser.references, f"application script is not linked in {path}")

    require("site-theme.css" in index_parser.references, "homepage must link shared theme")
    require("site-theme.css" in brief_parser.references, "project brief must link shared theme")
    require("proofStylesheet" not in app_text, "proof stylesheet must not depend on JavaScript injection")
    require(
        "document.documentElement.classList.add('js')" in app_text,
        "JavaScript enhancement marker must be set only after app.js loads",
    )
    require(".reveal {" in css_text, "no-script reveal fallback missing")
    require(".js .reveal" in css_text, "JavaScript-only reveal enhancement missing")
    require("@media (prefers-reduced-motion: reduce)" in css_text, "reduced-motion fallback missing")
    require("@media (max-width: 900px)" in css_text, "mobile proof layout missing")
    require("overflow-x: auto" in css_text, "responsive table overflow missing")
    require("@media print" in css_text, "project brief print rules missing")


def main() -> int:
    for path in (INDEX_PATH, BRIEF_PATH, APP_PATH, PROOF_CSS_PATH):
        require(path.exists(), f"required public-site file missing: {path}")

    index_parser = parse_document(INDEX_PATH)
    brief_parser = parse_document(BRIEF_PATH)

    validate_homepage(index_parser)
    validate_project_brief(brief_parser)
    validate_local_references(INDEX_PATH, index_parser)
    validate_local_references(BRIEF_PATH, brief_parser)
    validate_supporting_assets(index_parser, brief_parser)

    print("public site content contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
