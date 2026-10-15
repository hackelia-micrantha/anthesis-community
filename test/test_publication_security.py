"""Regression tests for the public Anthesis publication boundary."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_publication_security.py"
SPEC = importlib.util.spec_from_file_location("anthesis_publication_security", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class PublicationSecurityTests(unittest.TestCase):
    def test_block_sensitive_paths_allow_intended_public_artifacts(self):
        bad = [
            "test/certs/dev-key.pem", "test/certs/dev.pem", "docs/private.key",
            "web/.env", "web/.env.production", "web/.dev.vars",
            "web/.dev.vars.production", "runtime/secrets.yaml",
            "keys/id_ed25519", "backup/credentials.json", "data/users.db",
        ]
        good = [
            "web/anthesis.pdf", "web/index.html", "specs/governance-lab/policy.schema.json",
            "examples/.env.example", ".dev.vars.example", "web/theme.css",
        ]
        for path in bad:
            with self.subTest(blocked=path):
                self.assertTrue(guard.sensitive_path(Path(path)))
        for path in good:
            with self.subTest(allowed=path):
                self.assertFalse(guard.sensitive_path(Path(path)))

    def test_detects_private_key_marker_across_stream_chunks(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            file = root / "site.txt"
            marker = b"-----BEGIN " + b"OPENSSH PRIVATE KEY-----"
            file.write_bytes(b"a" * (guard.READ_CHUNK_BYTES - 4) + marker)
            self.assertEqual(
                guard.inspect(root, [Path("site.txt")]),
                [("site.txt", "private-key PEM marker")],
            )

    def test_detects_marker_in_nonstandard_extension(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "fixture.foo").write_bytes(
                b"header\n" + b"-----BEGIN " + b"PRIVATE KEY-----\nsynthetic"
            )
            self.assertEqual(len(guard.inspect(root, [Path("fixture.foo")])), 1)

    def test_fails_closed_on_symlinks_and_missing_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "file").write_text("allowed content")
            (root / "link").symlink_to(root / "file")
            findings = guard.inspect(root, [Path("file"), Path("link"), Path("missing")])
            self.assertEqual(
                findings,
                [("link", "publication symlink"), ("missing", "missing or invalid file")],
            )

    def test_does_not_follow_parent_escape(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            findings = guard.inspect(root, [Path("../elsewhere")])
            self.assertEqual(findings, [("../elsewhere", "unsafe relative path")])

    def test_web_only_scans_web_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "web").mkdir()
            (root / "web" / "index.html").write_text("<title>Anthesis</title>")
            (root / "private").mkdir()
            (root / "private" / "secret.key").write_text("synthetic")
            self.assertEqual(guard.web_files(root), [Path("web/index.html")])
            self.assertEqual(guard.inspect(root, guard.web_files(root)), [])


if __name__ == "__main__":
    unittest.main()
