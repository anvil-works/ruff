"""Exercise design-component typing through the real validate command."""

from __future__ import annotations

import unittest

from test_validate import NATIVE, ValidateIntegration


@unittest.skipUnless(NATIVE, "native design-component typing")
class DesignComponent(ValidateIntegration):
    def test_design_component_preserves_class_and_inherited_property_checks(self):
        code = (
            "import anvil\n"
            "from anvil.designer import get_design_component\n"
            "BaseLink = get_design_component(anvil.Link)\n"
            "class Anchor(BaseLink):\n"
            "    def configure(self):\n"
            "        self.text = 'Ready'\n"
            "        self.clear()\n"
            "        self.raise_event('click')\n"
            "Anchor().configure()\n"
        )
        path = self.write("client_code/DynamicBase.py", code)
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("warnings"), events)
        path.write_text(code.replace("self.text = 'Ready'", "self.text = 42"))
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertEqual(
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            ["invalid-assignment"],
            events,
        )

        path.write_text(
            "import anvil\nfrom anvil.designer import get_design_component\n"
            "get_design_component(anvil.Link())\n"
        )
        result, events = self.validate(path)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertEqual(
            [issue["rule"] for issue in events[-1]["data"]["issues"]],
            ["invalid-argument-type"],
            events,
        )


if __name__ == "__main__":
    unittest.main()
