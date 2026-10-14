"""A release must contain every platform at the same version and source."""

from __future__ import annotations

import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from collect_release import collect

WRAPPER = json.loads(
    (Path(__file__).resolve().parents[1] / "npm/package.json").read_text()
)


def archive(path, files):
    with tarfile.open(path, "w:gz") as tar:
        for name, value in files.items():
            data = json.dumps(value).encode()
            entry = tarfile.TarInfo("package/" + name)
            entry.size = len(data)
            tar.addfile(entry, io.BytesIO(data))


class CollectRelease(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        self.snapshot = {
            "revision": "a" * 40,
            "patch": "",
            "native_files": {"src/main.rs": "example hash"},
        }
        archive(self.inputs / "wrapper.tgz", {"package.json": WRAPPER})
        for number, name in enumerate(WRAPPER["optionalDependencies"]):
            archive(
                self.inputs / f"platform-{number}.tgz",
                {
                    "package.json": {"name": name, "version": WRAPPER["version"]},
                    "manifest.json": {
                        "source_snapshot_at_packaging": self.snapshot,
                        "files": {},
                    },
                },
            )

    def test_complete_release_records_six_archives_and_deduplicates_wrapper(self):
        archive(self.inputs / "second-wrapper.tgz", {"package.json": WRAPPER})
        output = self.root / "release"
        result = collect(self.inputs, output)
        self.assertEqual(len(result["packages"]), 6)
        self.assertEqual(result["source_revision"], "a" * 40)
        self.assertEqual(len(list(output.glob("*.tgz"))), 6)
        self.assertEqual(len((output / "SHA256SUMS").read_text().splitlines()), 6)

    def test_missing_platform_is_rejected_before_writing_output(self):
        (self.inputs / "platform-4.tgz").unlink()
        output = self.root / "release"
        with self.assertRaisesRegex(ValueError, "missing"):
            collect(self.inputs, output)
        self.assertFalse(output.exists())

    def test_corrupted_bundle_is_rejected_before_writing_output(self):
        name = next(iter(WRAPPER["optionalDependencies"]))
        archive(
            self.inputs / "platform-0.tgz",
            {
                "package.json": {"name": name, "version": WRAPPER["version"]},
                "manifest.json": {
                    "source_snapshot_at_packaging": self.snapshot,
                    "files": {"README.md": "incorrect digest"},
                },
                "README.md": "damaged content",
            },
        )
        output = self.root / "release"
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            collect(self.inputs, output)
        self.assertFalse(output.exists())

    def test_different_source_or_version_is_rejected(self):
        name = next(iter(WRAPPER["optionalDependencies"]))
        for version, snapshot in [
            ("0.1.0-canary.99", self.snapshot),
            (WRAPPER["version"], {**self.snapshot, "revision": "c" * 40}),
            (WRAPPER["version"], {**self.snapshot, "patch": "uncommitted change"}),
        ]:
            with self.subTest(version=version, snapshot=snapshot):
                archive(
                    self.inputs / "platform-0.tgz",
                    {
                        "package.json": {"name": name, "version": version},
                        "manifest.json": {
                            "source_snapshot_at_packaging": snapshot,
                            "files": {},
                        },
                    },
                )
                with self.assertRaisesRegex(ValueError, "version|source"):
                    collect(self.inputs, self.root / "release")
