"""Installed native packages on each release platform, without a source checkout."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


@unittest.skipUnless(
    os.environ.get("ANVIL_RELEASE_PACKAGES"), "release archives not selected"
)
class InstalledRelease(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.installation = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.installation.cleanup)
        original = Path(cls.installation.name) / "original"
        archives = sorted(
            Path(os.environ["ANVIL_RELEASE_PACKAGES"]).resolve().glob("*.tgz")
        )
        if len(archives) != 2:
            raise AssertionError(
                f"expected wrapper and one platform archive: {archives}"
            )
        subprocess.run(
            [
                shutil.which("npm"),
                "install",
                "--offline",
                "--ignore-scripts",
                "--no-audit",
                "--no-fund",
                "--prefix",
                str(original),
                *map(str, archives),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.installed = (
            Path(cls.installation.name) / "relocated installation with spaces"
        )
        shutil.move(original, cls.installed)
        cls.executable = subprocess.check_output(
            ["node", "-p", "require('@anvil-works/anvil-ty').executablePath"],
            cwd=cls.installed,
            text=True,
        ).strip()
        if not Path(cls.executable).resolve().is_relative_to(cls.installed.resolve()):
            raise AssertionError(
                f"checker resolved outside installation: {cls.executable}"
            )

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="anvil release app ")
        self.addCleanup(self.temp.cleanup)
        self.app = Path(self.temp.name)
        self.write(
            "anvil.yaml",
            "name: Release test\npackage_name: ReleaseTest\n"
            "runtime_options:\n  version: 2\n  client_version: '3'\n"
            "  server_version: python3-full\n"
            "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n",
        )

    def write(self, relative, text):
        path = self.app / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def validate(self, expected_status=0, target=None):
        before = {
            path: path.read_bytes() for path in self.app.rglob("*") if path.is_file()
        }
        result = subprocess.run(
            [
                self.executable,
                "--outputjson",
                "--level",
                "warning",
                "--project",
                str(self.app),
                *([str(target)] if target else []),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode, expected_status, (result.stdout, result.stderr)
        )
        self.assertEqual(before, {path: path.read_bytes() for path in before})
        return json.loads(result.stdout)["generalDiagnostics"]

    def test_nested_forms_row_models_and_custom_events(self):
        self.write("client_code/nested/__init__.py", "")
        self.write("client_code/nested/helpers.py", "class Payload: pass\n")
        self.write(
            "client_code/nested/Card/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\n"
            "events:\n- name: changed\n  parameters: []\n",
        )
        self.write(
            "client_code/nested/Card/__init__.py",
            "from ._anvil_designer import CardTemplate\n"
            "class Card(CardTemplate): pass\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: card\n  type: form:nested.Card\n",
        )
        page = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('card', 'changed')\n"
            "    def changed(self, **event_args): pass\n",
        )
        self.write("server_code/nested/__init__.py", "")
        self.write(
            "server_code/nested/models.py",
            "from anvil.tables import app_tables\n"
            "class Person(app_tables.people.Row, attrs=True):\n"
            "    def greeting(self) -> str: return self.name\n",
        )
        self.write(
            "server_code/Use.py",
            "from .nested.models import Person\nfrom anvil.tables import app_tables\n"
            "from nested.helpers import Payload\n"
            "person = app_tables.people.add_row(name='Ada')\n"
            "message: str = person.greeting()\npayload: Payload = Payload()\n",
        )
        self.assertEqual(self.validate(), [])
        page.write_text(
            page.read_text().replace("'changed'", "'typo'"), encoding="utf-8"
        )
        diagnostics = self.validate(target=page)
        self.assertEqual(
            [item["rule"] for item in diagnostics], ["reportAnvilInvalidEvent"]
        )

    def test_invalid_assignment_keeps_original_path_and_utf16_range(self):
        file = self.write(
            "server_code/Broken.py", "marker = '😀'; count: int = 'wrong'\n"
        )
        diagnostics = self.validate(1, file)
        self.assertEqual(len(diagnostics), 1)
        self.assertEqual(diagnostics[0]["rule"], "invalid-assignment")
        self.assertEqual(diagnostics[0]["file"], str(file))
        self.assertEqual(
            diagnostics[0]["range"],
            {
                "start": {"line": 0, "character": 28},
                "end": {"line": 0, "character": 35},
            },
        )

    def test_client_cannot_import_server_source(self):
        self.write("pyrightconfig.json", '{"extraPaths": ["server_code"]}')
        self.write("server_code/Secret.py", "value: str = 'server'\n")
        client = self.write("client_code/Use.py", "import Secret\n")
        diagnostics = self.validate(1, client)
        self.assertEqual(
            [item["rule"] for item in diagnostics], ["reportAnvilImportRestriction"]
        )


if __name__ == "__main__":
    unittest.main()
