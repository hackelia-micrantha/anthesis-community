#!/usr/bin/env python3
"""Validate the static Anthesis public-site content contract."""

from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = REPO_ROOT / "web"
INDEX_PATH = WEB_ROOT / "index.html"
BRIEF_PATH = WEB_ROOT / "project-brief.html"
APP_PATH = WEB_ROOT / "app.js"
PROOF_CSS_PATH = WEB_ROOT / "proof.css"
WHITEPAPER_PATH = WEB_ROOT / "anthesis.pdf"
WHITEPAPER_MANIFEST_PATH = WEB_ROOT / "anthesis.pdf.manifest.json"

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

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def validate_homepage(parser: DocumentParser) -> None:
    text = parser.text
    require(parser.main_sections == 5, "homepage must contain five main sections plus the hero")
    require("Governed execution for agentic systems" in text, "canonical hero eyebrow missing")
    require(
        "Let agents act without giving them invisible authority." in text,
        "canonical outcome headline missing",
    )
    require("Run the deterministic demo" in text, "Governance Lab primary action missing")
    require("View the governed-agent integration" in text, "Dubnium primary action missing")
    require("Governance Lab" in text and "Dubnium" in text, "proof paths missing")
    require("not in the runtime critical path" in text, "Governance Lab runtime boundary missing")
    require("does not define policy authority" in text, "Dubnium policy boundary missing")
    require("What prevents the agent" in text, "central bypass question missing")
    require("27 scenarios" not in text, "unsynchronized scenario count must be omitted")
    for label in MATURITY_LABELS:
        require(label in text, f"homepage maturity label missing: {label}")


def validate_project_brief(parser: DocumentParser) -> None:
    text = parser.text
    require(
        "governance boundary between an agent's intent and its externally observable effects" in text,
        "canonical project-brief positioning missing",
    )
    for mode in INTEGRATION_MODES:
        require(mode in text, f"project brief integration mode missing: {mode}")
    for label in MATURITY_LABELS:
        require(label in text, f"project brief maturity label missing: {label}")
    require("Enforcement location and assurance are separate dimensions." in text, "assurance distinction missing")
    require("27 scenarios" not in text, "unsynchronized scenario count must be omitted")


def validate_supporting_assets(
    index_parser: DocumentParser,
    brief_parser: DocumentParser,
) -> None:
    require(PROOF_CSS_PATH.exists(), "governed-agent proof stylesheet missing")
    app_text = APP_PATH.read_text(encoding="utf-8")
    css_text = PROOF_CSS_PATH.read_text(encoding="utf-8")

    for path, parser in (
        (INDEX_PATH, index_parser),
        (BRIEF_PATH, brief_parser),
    ):
        require("proof.css" in parser.references, f"proof stylesheet is not linked in {path}")
        require("app.js" in parser.references, f"application script is not linked in {path}")

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


def validate_whitepaper_artifact() -> None:
    require(WHITEPAPER_PATH.read_bytes().startswith(b"%PDF-"), "whitepaper is not a PDF")
    require(WHITEPAPER_PATH.stat().st_size > 10_000, "whitepaper is unexpectedly small")

    metadata = json.loads(WHITEPAPER_MANIFEST_PATH.read_text(encoding="utf-8"))
    require(metadata.get("schema_version") == 1, "whitepaper manifest schema must be 1")
    require(metadata.get("artifact") == WHITEPAPER_PATH.name, "whitepaper artifact name mismatch")
    require(
        metadata.get("artifact_sha256") == sha256(WHITEPAPER_PATH),
        "whitepaper artifact digest mismatch",
    )
    require(
        isinstance(metadata.get("source_commit"), str)
        and COMMIT_PATTERN.fullmatch(metadata["source_commit"]) is not None,
        "whitepaper source commit must be a full lowercase Git SHA",
    )
    require(
        metadata.get("manifest") == "docs/anthesis/overview/whitepaper-manifest.json",
        "whitepaper source manifest path mismatch",
    )
    require(
        isinstance(metadata.get("manifest_sha256"), str)
        and SHA256_PATTERN.fullmatch(metadata["manifest_sha256"]) is not None,
        "whitepaper source manifest digest is malformed",
    )

    sources = metadata.get("sources")
    require(isinstance(sources, list) and len(sources) == 1, "whitepaper must declare one curated source")
    source = sources[0]
    require(
        isinstance(source, dict)
        and source.get("path") == "docs/anthesis/overview/anthesis-whitepaper.md",
        "whitepaper curated source path mismatch",
    )
    require(
        isinstance(source.get("sha256"), str)
        and SHA256_PATTERN.fullmatch(source["sha256"]) is not None,
        "whitepaper curated source digest is malformed",
    )


def main() -> int:
    for path in (
        INDEX_PATH,
        BRIEF_PATH,
        APP_PATH,
        PROOF_CSS_PATH,
        WHITEPAPER_PATH,
        WHITEPAPER_MANIFEST_PATH,
    ):
        require(path.exists(), f"required public-site file missing: {path}")

    index_parser = parse_document(INDEX_PATH)
    brief_parser = parse_document(BRIEF_PATH)

    validate_homepage(index_parser)
    validate_project_brief(brief_parser)
    validate_local_references(INDEX_PATH, index_parser)
    validate_local_references(BRIEF_PATH, brief_parser)
    validate_supporting_assets(index_parser, brief_parser)
    validate_whitepaper_artifact()

    print("public site content contract validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
