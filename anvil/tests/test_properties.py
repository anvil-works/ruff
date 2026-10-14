"""Python-owned properties use Python contracts, not designer input formats."""

from __future__ import annotations

import unittest

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "native property preparation")
class OwnedProperties(unittest.TestCase):
    setUp = harness.ValidateIntegration.setUp
    write = harness.ValidateIntegration.write
    validate = harness.ValidateIntegration.validate

    def test_theme_role_metadata_accepts_role_values_and_checks_invalid_values(self):
        # The designer type applies to any property name, not only built-in `role`.
        self.write(
            "client_code/Choices/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: HtmlTemplate\n"
            "properties:\n- {name: appearance, type: themeRole}\n",
        )
        code = (
            "from ._anvil_designer import ChoicesTemplate\n"
            "class Choices(ChoicesTemplate):\n    pass\n"
            "component = Choices(appearance='outlined')\n"
            "component.appearance = ['outlined', 'compact']\n"
            "component.appearance = None\n"
            "component.init_components(appearance=['compact'])\n"
        )
        path = self.write("client_code/Choices/__init__.py", code)
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        path.write_text(
            code + "component.appearance = 42\n"
            "Choices(appearance=42)\n"
            "component.init_components(appearance=[42])\n"
        )
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertCountEqual(
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            ["invalid-assignment", "invalid-argument-type", "invalid-argument-type"],
            events,
        )

    def test_typed_property_keeps_richer_values_and_rejects_invalid_values(self):
        self.write(
            "client_code/Choices/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: HtmlTemplate\n"
            "properties:\n- {name: role, type: string}\n"
            "- {name: caption, type: string}\n",
        )
        code = (
            "from ._anvil_designer import ChoicesTemplate\n"
            "Roles = str | list[str] | None\n"
            "class Choices(ChoicesTemplate):\n"
            "    def __init__(self, role: Roles = None):\n"
            "        self._role = role\n"
            "        self.init_components(role=self._role)\n"
            "    @property\n    def role(self) -> Roles:\n"
            "        return self._role\n"
            "    @role.setter\n    def role(self, value: Roles) -> None:\n"
            "        self._role = value\n"
            "component = Choices(role=['one', 'two'])\n"
            "component.role = ['two', 'three']\n"
            "component.caption = 'Ready'\n"
        )
        path = self.write("client_code/Choices/__init__.py", code)
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("warnings"), events)
        path.write_text(
            code + "component.role = 42\ncomponent.caption = 42\nChoices(role=42)\n"
        )
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertCountEqual(
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            ["invalid-assignment", "invalid-assignment", "invalid-argument-type"],
            events,
        )

    def test_unannotated_property_keeps_normal_permissive_checking(self):
        self.write(
            "client_code/Choices/form_template.html",
            "---\ncustom_component: true\nproperties:\n"
            "- {name: role, type: string}\n---\n"
            '<anvil-form container="HtmlTemplate"></anvil-form>',
        )
        path = self.write(
            "client_code/Choices/__init__.py",
            "from ._anvil_designer import ChoicesTemplate\n"
            "class Choices(ChoicesTemplate):\n"
            "    @property\n    def role(self):\n        return []\n"
            "    @role.setter\n    def role(self, value):\n        pass\n"
            "component = Choices(role=['one', 'two'])\n"
            "component.role = 42\nunchecked: int = component.role\n",
        )
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("warnings"), events)

    def test_real_base_property_override_is_still_checked(self):
        self.write(
            "client_code/Choices/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: HtmlTemplate\n"
            "properties:\n- {name: role, type: string}\n",
        )
        path = self.write(
            "client_code/Choices/__init__.py",
            "from ._anvil_designer import ChoicesTemplate\n"
            "class Choices(ChoicesTemplate):\n"
            "    @property\n    def role(self) -> int:\n        return 42\n",
        )
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertIn(
            "invalid-property-type-override",
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            events,
        )
