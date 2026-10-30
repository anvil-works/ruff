"""Anvil-specific diagnostics through the real validate CLI."""

from __future__ import annotations

import json
import os
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "shared native Anvil diagnostics")
class RuntimeDiagnostics(unittest.TestCase):
    setUp = harness.ValidateIntegration.setUp
    write = harness.ValidateIntegration.write
    validate = harness.ValidateIntegration.validate

    def test_client_runtime_modules_follow_the_selected_stub_bundle(self):
        stubs = self.app / "stub-overrides"
        for environment in ("client", "server"):
            shutil.copytree(
                harness.ROOT / "anvil/api-stubs" / environment, stubs / environment
            )
        metadata = stubs / "client-runtime.json"
        metadata.write_text(json.dumps({"modules": ["locale"]}))
        client = self.write(
            "client_code/Imports.py", "from locale import LC_TIME, setlocale\n"
        )
        server = self.write("server_code/Imports.py", "import os\n")
        with patch.dict(os.environ, {"ANVIL_API_STUBS_PATH": str(stubs)}):
            result, events = self.validate(client)
            self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
            client.write_text("import math\n")
            result, events = self.validate(client)
            self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
            self.assertEqual(
                events[-1]["data"]["issues"][0]["rule"],
                "reportAnvilUnsupportedSkulptImport",
            )
            result, events = self.validate(server)
            self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
            # Older override directories still use the checker's bundled runtime data.
            metadata.unlink()
            result, events = self.validate(client)
            self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))

    def test_malformed_client_runtime_metadata_does_not_use_bundled_defaults(self):
        stubs = self.app / "stub-overrides"
        stubs.mkdir()
        (stubs / "client-runtime.json").write_text('{"modules": "locale"}')
        client = self.write("client_code/Imports.py", "import math\n")
        with patch.dict(os.environ, {"ANVIL_API_STUBS_PATH": str(stubs)}):
            result, events = self.validate(client)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertIn("Invalid client runtime metadata", result.stdout)

    def test_client_syntax_policy_preserves_supported_fstrings(self):
        fixtures = json.loads(
            Path(__file__).with_name("client-syntax.json").read_text()
        )
        for fixture in fixtures:
            with self.subTest(name=fixture["name"]):
                file = self.write("client_code/Syntax.py", fixture["source"])
                result, events = self.validate(file)
                self.assertIn(result.returncode, (0, 1), (result.stdout, result.stderr))
                data = events[-1]["data"]
                issues = data.get("issues", []) + data.get("warnings", [])
                syntax = [
                    issue
                    for issue in issues
                    if issue["rule"]
                    in ("invalid-syntax", "reportAnvilUnsupportedSkulptSyntax")
                ]
                self.assertEqual(
                    sorted(issue["line"] - 1 for issue in syntax), fixture["lines"]
                )

    def test_client_syntax_warnings_preserve_server_support(self):
        source = 'async def fetch():\n    return 42\nvalue = 42\ntext = f"{value=}"\n'
        client = self.write("client_code/Syntax.py", source)
        server = self.write("server_code/Syntax.py", source)
        result, events = self.validate(client)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        issues = data.get("issues", []) + data.get("warnings", [])
        unsupported = [
            issue
            for issue in issues
            if issue["rule"] == "reportAnvilUnsupportedSkulptSyntax"
        ]
        self.assertEqual([issue["line"] for issue in unsupported], [1, 4])
        result, events = self.validate(server)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertEqual(client.read_text(), source)
        self.assertEqual(server.read_text(), source)

    def test_row_model_keywords_follow_the_runtime_signature(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "\ndb_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        source = (
            "from anvil.tables import app_tables\n"
            "class Person(app_tables.people.Row, attr=True, client_writable=True, surprise=True):\n"
            "    pass\n"
        )
        for directory in ("client_code", "server_code"):
            with self.subTest(directory=directory):
                file = self.write(f"{directory}/Models.py", source)
                result, events = self.validate(file)
                self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
                issues = events[-1]["data"]["issues"]
                self.assertEqual(
                    [issue["rule"] for issue in issues],
                    ["unknown-argument", "unknown-argument"],
                )
                file.write_text(
                    source.replace(
                        "attr=True, client_writable=True, surprise=True",
                        "attrs=True, client_writable=True, metaclass=type",
                    )
                )
                result, events = self.validate(file)
                self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))

    def test_portable_class_placement_resolves_aliases(self):
        source = "from anvil.server import portable_class as portable\n@portable\nclass Example:\n    pass\n"
        self.write("client_code/Portable.py", source)
        server = self.write("server_code/Portable.py", source)
        form = self.write(
            "client_code/Home/__init__.py", source.replace("Example", "Home")
        )
        self.write(
            "client_code/Home/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents: []\n",
        )
        self.write(
            "server_code/Ordinary.py",
            "def portable(cls): return cls\n@portable\nclass Example:\n    pass\n",
        )
        result, events = self.validate()
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        issues = [
            issue
            for file in data["files"]
            for issue in file.get("issues", []) + file.get("warnings", [])
        ]
        placement = [
            issue
            for issue in issues
            if issue["rule"] == "reportAnvilPortableClassPlacement"
        ]
        self.assertEqual(
            {issue["file"] for issue in placement}, {str(server), str(form)}
        )
        self.assertEqual([issue["line"] for issue in placement], [2, 2])

    def test_registration_collisions_include_unselected_modules(self):
        # A checkout's name does not decide whether a source is a Server Module.
        relocated = self.app / "checkout" / "server_code"
        relocated.mkdir(parents=True)
        for source in self.app.iterdir():
            if source.name != "checkout":
                source.rename(relocated / source.name)
        self.app = relocated
        prefix = (
            "from anvil.server import callable as expose, background_task as task\n"
        )
        first = self.write(
            "server_code/First.py",
            prefix
            + '@expose("shared")\ndef first(): pass\n@task("nightly")\ndef first_task(): pass\n',
        )
        second = self.write(
            "server_code/Second.py",
            prefix
            + '@expose("shared")\ndef second(): pass\n@task("nightly")\ndef second_task(): pass\n',
        )
        self.write(
            "server_code/Unused.py",
            prefix
            + 'def factory():\n    @expose("shared")\n    def inner(): pass\n    return inner\n',
        )
        self.write(
            "client_code/Shared.py",
            prefix
            + '@expose("shared")\ndef shared(): pass\n@task("nightly")\ndef shared_task(): pass\n',
        )
        result, events = self.validate(first)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        issues = data.get("issues", []) + data.get("warnings", [])
        self.assertEqual(
            [issue["rule"] for issue in issues],
            ["reportAnvilDuplicateCallable", "reportAnvilDuplicateBackgroundTask"],
        )
        self.assertIn("shared", issues[0]["message"])
        self.assertIn("nightly", issues[1]["message"])
        second.write_text(
            second.read_text()
            .replace('"shared"', '"other"')
            .replace('"nightly"', '"morning"')
        )
        result, events = self.validate(first)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        self.assertEqual(data.get("issues", []) + data.get("warnings", []), [])

    def test_show_handler_navigation_uses_yaml_and_decorator_metadata(self):
        template = self.write(
            "client_code/Home/form_template.yaml",
            "class_name: pkg.Welcome\ncontainer:\n  type: ColumnPanel\n  event_bindings: {show: overridden}\n"
            "  components:\n  - {name: label, type: Label, event_bindings: {show: from_yaml}}\n"
            "components_by_slot:\n  body:\n  - {name: slot_label, type: Label, event_bindings: {show: slotted}}\n",
        )
        file = self.write(
            "client_code/Home/__init__.py",
            (
                "from anvil import open_form as navigate, handle as on\n"
                "from ._anvil_designer import WelcomeTemplate\n"
                "class Welcome(WelcomeTemplate):\n    def from_yaml(self, **event_args):\n        navigate('Home')\n"
                "    @on('', 'show')\n    def decorated(self, **event_args):\n        navigate('Home')\n"
                "    def overridden(self, **event_args):\n        navigate('Home')\n"
                "    def slotted(self, **event_args):\n        navigate('Home')\n"
                "    def click(self, **event_args):\n        navigate('Home')\n"
                "class Other:\n    def from_yaml(self):\n        navigate('Home')\n"
            ),
        )
        for expected in ([5, 8, 12], [8]):
            result, events = self.validate(file)
            self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
            data = events[-1]["data"]
            issues = data.get("issues", []) + data.get("warnings", [])
            self.assertEqual(
                [
                    issue["line"]
                    for issue in issues
                    if issue["rule"] == "reportAnvilOpenFormInShow"
                ],
                expected,
            )
            template.write_text(
                "class_name: pkg.Welcome\ncontainer:\n  type: ColumnPanel\ncomponents: []\n"
            )

    def test_class_body_and_dynamic_registrations_remain_known_to_call_validation(self):
        self.write(
            "server_code/Registered.py",
            'import anvil.server\nclass Service:\n    @staticmethod\n    @anvil.server.callable("shared")\n    def run(): pass\nNAME = "dynamic"\n@anvil.server.callable(NAME)\ndef dynamic(): pass\n',
        )
        file = self.write(
            "client_code/Caller.py",
            'import anvil.server\nanvil.server.call("shared")\nanvil.server.call("dynamic")\n',
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        self.assertEqual(data.get("issues", []) + data.get("warnings", []), [])
