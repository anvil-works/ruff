"""Inspect the actual Linux npm archive's installation restrictions."""

from __future__ import annotations

import json
import os
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import package


class PackageMetadata(unittest.TestCase):
    def test_linux_archive_selects_glibc_only(self):
        binary = Path(os.environ["ANVIL_TY_TEST_EXECUTABLE"])
        with tempfile.TemporaryDirectory() as directory, patch(
            "package.platform.system", return_value="Linux"
        ), patch("package.platform.machine", return_value="x86_64"):
            result = package.package(binary, Path(directory) / "bundle")
            archive = result["npm_packages"][0]["archive"]
            with tarfile.open(archive) as tar:
                metadata = json.load(tar.extractfile("package/package.json"))
            self.assertEqual(metadata["os"], ["linux"])
            self.assertEqual(metadata["cpu"], ["x64"])
            self.assertEqual(metadata["libc"], ["glibc"])
            self.assertEqual(
                metadata["repository"]["url"],
                "https://github.com/anvil-works/ruff.git",
            )
            manifest = json.loads(
                (Path(directory) / "bundle/manifest.json").read_text()
            )
            self.assertIn(
                "anvil/native/src/main.rs",
                manifest["source_snapshot_at_packaging"]["native_files"],
            )
            self.assertIn("share/anvil-typeshed/SOURCE.json", manifest["files"])
            self.assertIn("revision", manifest["source_snapshot_at_packaging"])
            self.assertNotIn("ruff_source", manifest["source_snapshot_at_packaging"])
