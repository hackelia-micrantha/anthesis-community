#!/usr/bin/env python3
"""Fail closed on credential files and private-key material before public release.

Checks the current tracked tree or the deployed web/ tree. This is not a
historical Git scan or a general-purpose credential detector. Never print
file contents or discovered secret values.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

PRIVATE_KEY = re.compile(
    rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----"
)
BLOCKED_SUFFIXES = frozenset({
    ".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".sqlite", ".db",
})
BLOCKED_NAMES = frozenset({
    "id_rsa", "id_ed25519", "id_ecdsa", "credentials.json", "secrets.yaml",
})
EXAMPLE_SUFFIXES = (".example", ".sample", ".template")
READ_CHUNK_BYTES = 65536
MARKER_OVERLAP_BYTES = 100


def sensitive_path(relative: Path) -> bool:
    name = relative.name.lower()
    if name in BLOCKED_NAMES or relative.suffix.lower() in BLOCKED_SUFFIXES:
        return True
    if name == ".env" or name == ".dev.vars":
        return True
    return (
        (name.startswith(".env.") or name.startswith(".dev.vars."))
        and not name.endswith(EXAMPLE_SUFFIXES)
    )


def contains_private_key(path: Path) -> bool:
    overlap = b""
    with path.open("rb") as stream:
        while chunk := stream.read(READ_CHUNK_BYTES):
            combined = overlap + chunk
            if PRIVATE_KEY.search(combined):
                return True
            overlap = combined[-MARKER_OVERLAP_BYTES:]
    return False


def tracked_files(root: Path) -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "-z"],
        check=True, capture_output=True,
    )
    return [
        Path(os.fsdecode(part)) for part in result.stdout.split(b"\0") if part
    ]


def web_files(root: Path) -> list[Path]:
    web = root / "web"
    if web.is_symlink() or not web.is_dir():
        raise ValueError("web directory missing or symlinked")
    return [path.relative_to(root) for path in web.rglob("*") if not path.is_dir()]


def inspect(root: Path, files: list[Path]) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for rel in sorted(files):
        display = rel.as_posix()
        if rel.is_absolute() or ".." in rel.parts:
            findings.append((display, "unsafe relative path"))
            continue
        path = root / rel
        if path.is_symlink():
            findings.append((display, "publication symlink"))
        elif not path.is_file():
            findings.append((display, "missing or invalid file"))
        elif sensitive_path(rel):
            findings.append((display, "credential-like file path"))
        elif contains_private_key(path):
            findings.append((display, "private-key PEM marker"))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--tracked", action="store_true")
    mode.add_argument("--web", action="store_true")
    args = parser.parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    try:
        files = tracked_files(root) if args.tracked else web_files(root)
        findings = inspect(root, files)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"publication-gate: inspection failed ({type(error).__name__})", file=sys.stderr)
        return 2
    if findings:
        for name, reason in findings:
            # Avoid control characters from unusual tracked filenames in logs.
            display = name.encode("unicode_escape").decode("ascii")
            print(f"publication-gate: blocked {display}: {reason}", file=sys.stderr)
        return 1
    print("publication-gate: tracked source passed" if args.tracked else
          "publication-gate: public web passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
