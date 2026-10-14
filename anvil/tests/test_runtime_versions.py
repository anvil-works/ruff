"""Server runtime metadata must not change the client's Python target."""

from __future__ import annotations

import unittest
from unittest.mock import patch

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "native runtime selection")
class RuntimeVersions(unittest.TestCase):
    setUp = harness.ValidateIntegration.setUp
    write = harness.ValidateIntegration.write
    validate = harness.ValidateIntegration.validate

    def test_server_image_selects_python_without_changing_client(self):
        code = "value = int('3')\nvalue.is_integer()\n"
        server = self.write("server_code/Version.py", code)
        client = self.write("client_code/Version.py", code)
        for image, valid in (
            ("python310-minimal", False),
            ("python310-standard", False),
            ("python310-datascience", False),
            ("python310-machine-learning", False),
            ("python312", True),
            ("python313", True),
            ("python314", True),
        ):
            with self.subTest(image=image):
                self.write(
                    "anvil.yaml",
                    "name: Ty proof\npackage_name: TyProof\nruntime_options:\n"
                    "  version: 2\n  client_version: '3'\n"
                    "  server_version: python3-full\n  server_spec:\n"
                    f"    base: {image}\n",
                )
                result, events = self.validate(server)
                self.assertEqual(result.returncode, 0 if valid else 1, events)
                if not valid:
                    self.assertEqual(
                        [i["rule"] for i in events[-1]["data"]["issues"]],
                        ["unresolved-attribute"],
                    )
        result, events = self.validate(client)
        self.assertEqual(result.returncode, 1, events)
        self.assertEqual(
            [i["rule"] for i in events[-1]["data"]["issues"]],
            ["unresolved-attribute"],
        )

    def test_custom_image_uses_explicit_version_and_rejects_missing_version(self):
        self.write(
            "anvil.yaml",
            "name: Ty proof\npackage_name: TyProof\nruntime_options:\n"
            "  version: 2\n  client_version: '3'\n"
            "  server_version: python3-full\n  server_spec:\n"
            "    base: company-python\n",
        )
        server = self.write(
            "server_code/Version.py", "value = int('3')\nvalue.is_integer()\n"
        )
        result, events = self.validate(server)
        self.assertEqual(result.returncode, 1, events)
        self.assertIn("pythonVersion", result.stdout)
        self.write("pyrightconfig.json", '{"pythonVersion": "3.13"}')
        result, events = self.validate(server)
        self.assertEqual(result.returncode, 0, events)
        server.write_text(server.read_text() + "wrong: str = 42\n")
        result, events = self.validate(server)
        self.assertEqual(result.returncode, 1, events)
        self.assertEqual(
            [i["rule"] for i in events[-1]["data"]["issues"]],
            ["invalid-assignment"],
        )

    def test_modern_server_syntax_does_not_require_host_python(self):
        self.write(
            "anvil.yaml",
            "name: Ty proof\npackage_name: TyProof\nruntime_options:\n"
            "  version: 2\n  client_version: '3'\n"
            "  server_version: python3-full\n  server_spec:\n    base: python312\n",
        )
        source = self.write(
            "server_code/Version.py",
            "type Values = list[int]\nvalues: Values = [1, 2]\n",
        )
        with patch.dict(harness.os.environ, {"ANVIL_PYTHON": "/unavailable/python"}):
            result, events = self.validate(source)
        self.assertEqual(result.returncode, 0, events)
        source.write_text("type Values = list[int]\nvalues: Values = ['wrong']\n")
        result, events = self.validate(source)
        self.assertEqual(result.returncode, 1, events)
        self.assertEqual(
            [i["rule"] for i in events[-1]["data"]["issues"]],
            ["invalid-assignment"],
        )
