"""Relocated native bundles through the real anvil validate command."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import unittest

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "native bundle")
class Packaging(unittest.TestCase):
    write = harness.ValidateIntegration.write
    setUp = harness.ValidateIntegration.setUp

    def test_relocated_bundle_checks_forms_and_preserves_diagnostics_without_checkout(
        self,
    ):
        artifacts = self.app.parent / (self.app.name + " artifacts")
        artifacts.mkdir()
        self.addCleanup(shutil.rmtree, artifacts)
        original = artifacts / "original bundle"
        result = subprocess.run(
            [
                sys.executable,
                str(harness.ROOT / "anvil/package.py"),
                "--binary",
                str(harness.ADAPTER),
                "--output",
                str(original),
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        packaged = json.loads(result.stdout)
        npm_archives = [item["archive"] for item in packaged["npm_packages"]]
        installed = artifacts / "npm installation with spaces"
        result = subprocess.run(
            [
                "npm",
                "install",
                "--offline",
                "--ignore-scripts",
                "--no-audit",
                "--no-fund",
                "--prefix",
                str(installed),
                *npm_archives,
            ],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        installed_executable = subprocess.check_output(
            ["node", "-p", "require('@anvil-works/anvil-ty').executablePath"],
            cwd=installed,
            text=True,
        ).strip()
        self.assertTrue(
            os.path.commonpath([installed_executable, str(installed.resolve())])
            == str(installed.resolve()),
            installed_executable,
        )
        manifest = json.loads((original / "manifest.json").read_text())
        npm = json.loads((original / "package.json").read_text())
        node_platform = subprocess.check_output(
            ["node", "-p", "process.platform + '-' + process.arch"], text=True
        ).strip()
        self.assertEqual(npm["name"], f"@anvil-works/anvil-ty-{node_platform}")
        self.assertEqual(
            npm["version"],
            json.loads((harness.ROOT / "anvil/npm/package.json").read_text())[
                "version"
            ],
        )
        snapshot = manifest["source_snapshot_at_packaging"]
        self.assertNotIn("anvil_pyright_revision", snapshot)
        self.assertIn("anvil_api_stubs", snapshot)
        authoritative = harness.ROOT.parent / "anvil/doc/dist/stubs"
        for source in authoritative.rglob("*.pyi"):
            bundled = (
                original / "share/anvil-typeshed" / source.relative_to(authoritative)
            )
            self.assertEqual(bundled.read_bytes(), source.read_bytes())
        engine = manifest["source_snapshot_at_packaging"]
        patch = subprocess.check_output(
            ["git", "-C", str(harness.ROOT), "diff", "HEAD", "--binary"],
            text=True,
        )
        self.assertEqual(engine["patch"], patch)
        self.assertEqual(
            engine["patch_sha256"], hashlib.sha256(patch.encode()).hexdigest()
        )
        with tarfile.open(original.with_name(original.name + ".tar.gz")) as archive:
            archive.extractall(artifacts / "extracted", filter="data")
        shutil.rmtree(original)
        bundle = artifacts / "relocated bundle with spaces"
        (artifacts / "extracted" / original.name).rename(bundle)
        executable = bundle / "bin" / "anvil-ty-native"
        self.write(
            "client_code/Form1/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: label_1\n  type: Label\n",
        )
        form = self.write(
            "client_code/Form1/__init__.py",
            "from ._anvil_designer import Form1Template\n"
            "class Form1(Form1Template):\n"
            "    def __init__(self, **properties):\n"
            "        self.init_components(**properties)\n"
            "        self.label_1.text = 'Ready'\n",
        )
        environment = {
            **os.environ,
            "ANVIL_PYRIGHT_ROOT": str(self.app / "unavailable checkout"),
        }
        environment.pop("ANVIL_PYRIGHT", None)
        environment.pop("ANVIL_API_STUBS_PATH", None)
        environment.pop("ANVIL_AGENT_HOST", None)

        def validate(target, checker=executable):
            before = {
                p.relative_to(self.app): p.read_bytes()
                for p in self.app.rglob("*")
                if p.is_file()
            }
            result = subprocess.run(
                ["node", str(harness.CLI), "--json", "validate", str(target)],
                check=False,
                env={**environment, "ANVIL_TY": str(checker)},
                text=True,
                capture_output=True,
            )
            after = {
                p.relative_to(self.app): p.read_bytes()
                for p in self.app.rglob("*")
                if p.is_file()
            }
            self.assertEqual(before, after, "validation must not write to the app")
            events = [
                json.loads(line) for line in result.stdout.splitlines() if line.strip()
            ]
            return result, events

        result, events = validate(self.app)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("issues"), events)
        result, events = validate(self.app, installed_executable)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))

        form.write_text(form.read_text().replace("'Ready'", "42"))
        result, events = validate(form)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issues = events[-1]["data"]["issues"]
        self.assertEqual(len(issues), 1, events)
        self.assertEqual(
            (issues[0]["file"], issues[0]["rule"]), (str(form), "invalid-assignment")
        )
        result, events = validate(form, installed_executable)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertEqual(events[-1]["data"]["issues"], issues)

        file = self.write(
            "server_code/Broken.py", "marker = '😀'; count: int = 'wrong'\n"
        )
        result, events = validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issue = events[-1]["data"]["issues"][0]
        self.assertEqual(
            (issue["file"], issue["rule"]), (str(file), "invalid-assignment")
        )
        self.assertEqual(
            (issue["line"], issue["column"], issue["endLine"], issue["endColumn"]),
            (1, 29, 1, 36),
        )
