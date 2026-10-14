"""Exercise the proof through the real anvil-cli validation command."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
PYRIGHT = ROOT.parent / "anvil-pyright"
CLI = ROOT.parent / "anvil-cli" / "dist" / "cli.js"
ADAPTER = Path(
    os.environ.get(
        "ANVIL_TY_TEST_EXECUTABLE", ROOT / "anvil/native/target/debug/anvil-ty-native"
    )
).resolve(strict=True)
# Probe capability rather than the filename: relocated/renamed native executables
# must run the same acceptance suite. The earlier adapter requires explicit selection.
VERSION = subprocess.check_output([str(ADAPTER), "--version"], text=True).strip()
NATIVE = VERSION.startswith("anvil-ty native")
if not VERSION.startswith("anvil-ty"):
    raise RuntimeError(f"expected an Anvil ty checker, got {VERSION!r}")


class ValidateIntegration(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.app = Path(self.temp.name)
        self.write(
            "anvil.yaml",
            "name: Ty proof\npackage_name: TyProof\nruntime_options:\n  version: 2\n  client_version: '3'\n  server_version: python3-full\n",
        )
        self.write(
            "client_code/Helpers.py", "def title() -> str:\n    return 'Ready'\n"
        )
        self.write(
            "server_code/Server.py",
            "import anvil.server\n\n@anvil.server.callable\ndef title() -> str:\n    return 'Ready'\n",
        )

    def write(self, name, content):
        target = self.app / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def validate(self, target=None, backend=None):
        executable = backend or ADAPTER
        probe = subprocess.run(
            [str(executable), "--version"], check=False, text=True, capture_output=True
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        prefix = "anvil-pyright" if backend else "anvil-ty"
        self.assertTrue(probe.stdout.startswith(prefix), probe.stdout)
        result = subprocess.run(
            ["node", str(CLI), "--json", "validate", str(target or self.app)],
            check=False,
            env={
                **os.environ,
                "ANVIL_PYRIGHT": str(executable),
                "ANVIL_PYRIGHT_ROOT": str(PYRIGHT),
            },
            text=True,
            capture_output=True,
        )
        events = [
            json.loads(line) for line in result.stdout.splitlines() if line.strip()
        ]
        return result, events

    @unittest.skipUnless(NATIVE, "native shared API contracts")
    def test_environment_constant_selects_client_reexport(self):
        self.write(
            "client_code/Implementation/__init__.py",
            "import anvil\n"
            "if anvil.is_server_side():\n    from .server import schedule\n"
            "else:\n    from .client import schedule\n",
        )
        self.write(
            "client_code/Implementation/server.py",
            "def schedule(callback, ms):\n    return 1\n",
        )
        self.write(
            "client_code/Implementation/client.py",
            "from anvil.js.window import setTimeout as schedule\n",
        )
        client = self.write(
            "client_code/Probe.py",
            "from typing import Literal\nimport anvil\n"
            "from .Implementation import schedule\n"
            "client_side: Literal[False] = anvil.is_server_side()\n"
            "schedule(lambda: None)\n",
        )
        server = self.write(
            "server_code/Probe.py",
            "from typing import Literal\nimport anvil\n"
            "server_side: Literal[True] = anvil.is_server_side()\n",
        )
        for path in (client, server):
            result, events = self.validate(path)
            self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        server.write_text(server.read_text().replace("Literal[True]", "Literal[False]"))
        result, events = self.validate(server)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertEqual(
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            ["invalid-assignment"],
        )

    @unittest.skipUnless(NATIVE, "native shared API contracts")
    def test_storage_methods_keep_value_and_nullable_result_checks(self):
        code = (
            "from anvil.js.window import sessionStorage\n"
            "value: str | None = sessionStorage.getItem('key')\n"
            "sessionStorage.setItem('key', 'value')\n"
            "sessionStorage.removeItem('key')\n"
        )
        path = self.write("client_code/Storage.py", code)
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        path.write_text(
            code + "sessionStorage.setItem('key', 42)\n"
            "wrong: str = sessionStorage.getItem('key')\n"
        )
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertCountEqual(
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            ["invalid-argument-type", "invalid-assignment"],
        )

    @unittest.skipUnless(NATIVE, "native API stub override")
    def test_agent_host_api_stubs_override_bundled_stubs_and_refresh(self):
        client = self.write(
            "client_code/Probe.py",
            "import anvil\nvalue: int = anvil.stub_probe()\n",
        )
        server = self.write(
            "server_code/Probe.py",
            "import anvil\nvalue: str = anvil.stub_probe()\n",
        )
        self.write(
            "client_code/Form1/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: probe\n  type: Label\n",
        )
        self.write(
            "client_code/Form1/__init__.py",
            "from ._anvil_designer import Form1Template\n"
            "class Form1(Form1Template):\n"
            "    def configure(self):\n        self.probe.stub_only = 'Ready'\n",
        )
        with tempfile.TemporaryDirectory(prefix="agent host stubs ") as directory:
            stubs = Path(directory)
            shutil.copytree(ROOT / "anvil/api-stubs", stubs, dirs_exist_ok=True)
            client_api = stubs / "client/anvil/__init__.pyi"
            server_api = stubs / "server/anvil/__init__.pyi"
            client_base = client_api.read_text().replace(
                "class Label(Component):\n",
                "class Label(Component):\n    stub_only: str\n",
            )
            server_base = server_api.read_text()
            client_api.write_text(client_base + "\ndef stub_probe() -> int: ...\n")
            server_api.write_text(server_base + "\ndef stub_probe() -> str: ...\n")
            with patch.dict(
                os.environ,
                {"ANVIL_API_STUBS_PATH": directory, "ANVIL_AGENT_HOST": "1"},
            ):
                result, events = self.validate()
                self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))

                # New host stubs must take effect without a checker version change.
                client_api.write_text(client_base + "\ndef stub_probe() -> str: ...\n")
                server_api.write_text(server_base + "\ndef stub_probe() -> int: ...\n")
                result, events = self.validate()
                self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
                self.assertCountEqual(
                    [
                        (issue["file"], issue["rule"])
                        for file in events[-1]["data"]["files"]
                        for issue in file.get("issues", [])
                    ],
                    [
                        (str(client), "invalid-assignment"),
                        (str(server), "invalid-assignment"),
                    ],
                    events,
                )

    def test_valid_anvil_app_uses_ty_through_cli(self):
        # Anvil API stubs and generated designer stubs must reach the real checker.
        self.write(
            "client_code/Form1/form_template.yaml",
            "custom_component: false\ncontainer:\n  type: ColumnPanel\n  components:\n  - name: label_2\n    type: Label\ncomponents:\n- name: label_1\n  type: Label\n",
        )
        self.write(
            "client_code/Form1/__init__.py",
            "from ._anvil_designer import Form1Template\nfrom ..Helpers import title\n\nclass Form1(Form1Template):\n    def __init__(self, **properties):\n        self.init_components(**properties)\n        self.label_1.text = title()\n        self.label_2.text = title()\n",
        )
        before = {
            p.relative_to(self.app): p.read_bytes()
            for p in self.app.rglob("*")
            if p.is_file()
        }
        result, events = self.validate()
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertTrue(events)
        after = {
            p.relative_to(self.app): p.read_bytes()
            for p in self.app.rglob("*")
            if p.is_file()
        }
        self.assertEqual(
            before, after, "validation must not materialize stubs in the source app"
        )

    def test_type_error_preserves_original_file_and_utf16_range(self):
        file = self.write(
            "server_code/Broken.py", "marker = '😀'; count: int = 'wrong'\n"
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issue = events[-1]["data"]["issues"][0]
        self.assertEqual(issue["file"], str(file))
        self.assertEqual(issue["rule"], "invalid-assignment")
        self.assertEqual(
            (issue["line"], issue["column"], issue["endLine"], issue["endColumn"]),
            (1, 29, 1, 36),
        )

    def test_generated_component_attributes_are_checked(self):
        self.write(
            "client_code/Form1/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: label_1\n  type: Label\n",
        )
        file = self.write(
            "client_code/Form1/__init__.py",
            "from ._anvil_designer import Form1Template\n\nclass Form1(Form1Template):\n    def __init__(self, **properties):\n        self.init_components(**properties)\n        self.label_1.text = 42\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertTrue(
            any(
                issue.get("file") == str(file)
                and issue.get("rule") == "invalid-assignment"
                for issue in events[-1]["data"]["issues"]
            ),
            events,
        )

    def test_file_target_ignores_unrelated_sibling_errors(self):
        file = self.write("server_code/Good.py", "answer: int = 42\n")
        self.write("server_code/Broken.py", "answer: int = 'wrong'\n")
        result, _events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))

    def test_syntax_error_at_end_of_file_has_a_source_range(self):
        file = self.write("server_code/Broken.py", "def broken(\n")
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issues = events[-1]["data"]["issues"]
        self.assertTrue(
            any(issue.get("file") == str(file) and "line" in issue for issue in issues),
            issues,
        )

    def test_client_cannot_import_a_server_module(self):
        file = self.write("client_code/Broken.py", "from .Server import title\n")
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issues = events[-1]["data"]["issues"]
        self.assertTrue(
            any(issue.get("rule") == "unresolved-import" for issue in issues), issues
        )

    @unittest.skipUnless(NATIVE, "native proof boundary")
    def test_native_accepts_module_forms_when_another_file_is_targeted(self):
        self.write(
            "client_code/Form1.yaml",
            "container:\n  type: ColumnPanel\ncomponents: []\n",
        )
        self.write(
            "client_code/Form1.py",
            "from ._anvil_designer import Form1Template\nclass Form1(Form1Template):\n    pass\n",
        )
        result, events = self.validate(self.app / "client_code/Helpers.py")
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertTrue(events[-1]["success"])

    @unittest.skipUnless(NATIVE, "native proof boundary")
    def test_native_accepts_spaced_column_names_when_another_file_is_targeted(
        self,
    ):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text() + "db_schema:\n  people:\n    columns:\n"
            "    - name: full name\n      type: string\n"
        )
        result, events = self.validate(self.app / "client_code/Helpers.py")
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertTrue(events[-1]["success"], events)


if __name__ == "__main__":
    unittest.main()
