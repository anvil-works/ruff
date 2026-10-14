"""Anvil decorator validation through the real CLI, including deliberate improvements."""

from __future__ import annotations

import json
import unittest

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "native handle checks")
class HandleValidation(unittest.TestCase):
    setUp = harness.ValidateIntegration.setUp
    write = harness.ValidateIntegration.write
    validate = harness.ValidateIntegration.validate

    def test_component_event_validation_keeps_inherited_events_and_reports_typos(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: panel\n  type: ColumnPanel\n  components:\n"
            "  - name: submit\n    type: Button\n"
            "- name: label\n  type: Label\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom anvil import handle as on\n"
            "from ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('submit', 'click')\n"
            "    @on('submit', 'show')\n"
            "    @on('label', 'hide')\n"
            "    @on('', 'refreshing_data_bindings')\n"
            "    @on('label', 'click')\n"
            "    @on('', 'click')\n"
            "    def clicked(self, **event_args):\n        pass\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        warnings = data.get("warnings", []) + data.get("issues", [])
        self.assertEqual(len(warnings), 2, events)
        warning = warnings[0]
        self.assertEqual(warning["rule"], "reportAnvilInvalidEvent")
        self.assertIn("Label has no event 'click'", warning["message"])
        self.assertEqual(warning["file"], str(file))
        self.assertEqual(warning["line"], 9)
        self.assertIn("Page has no event 'click'", warnings[1]["message"])
        self.assertEqual(warnings[1]["line"], 10)

    def test_custom_component_events_are_read_from_yaml(self):
        self.write(
            "client_code/Card/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\n"
            "events:\n- name: changed\n  parameters: []\n",
        )
        self.write(
            "client_code/Card/__init__.py",
            "from ._anvil_designer import CardTemplate\n"
            "class Card(CardTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: card\n  type: form:Card\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('card', 'changed')\n"
            "    @anvil.handle('card', 'show')\n"
            "    @anvil.handle('card', 'x-user-event')\n"
            "    @anvil.handle('card', 'click')\n"
            "    def changed(self, **event_args):\n        pass\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        data = events[-1]["data"]
        issues = data.get("warnings", []) + data.get("issues", [])
        self.assertEqual(len(issues), 1, events)
        self.assertEqual(issues[0]["rule"], "reportAnvilInvalidEvent")
        self.assertIn("has no event 'click'", issues[0]["message"])

    def test_handle_diagnostic_severity_and_selective_suppression(self):
        self.write(
            "client_code/Page.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: label\n  type: Label\n",
        )
        file = self.write(
            "client_code/Page.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('missing', 'click')  # pyright: ignore[reportAnvilUnknownComponent]\n"
            "    @anvil.handle('label', 'click')\n"
            "    def clicked(self, **event_args):\n        pass\n",
        )
        config = self.write(
            "pyrightconfig.json",
            json.dumps({"reportAnvilInvalidEvent": "error"}),
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issues = events[-1]["data"].get("issues", [])
        self.assertEqual(len(issues), 1, events)
        self.assertEqual(issues[0]["rule"], "reportAnvilInvalidEvent")
        self.assertEqual(issues[0]["severity"], "error")
        config.write_text(json.dumps({"reportAnvilInvalidEvent": "none"}))
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("issues"), events)
        self.assertFalse(events[-1]["data"].get("warnings"), events)

    def test_lookalike_decorators_and_dynamic_names_are_not_rejected(self):
        self.write(
            "client_code/Page.yaml",
            "container:\n  type: ColumnPanel\ncomponents: []\n",
        )
        file = self.write(
            "client_code/Page.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "def handle(component: str, event: str):\n"
            "    return anvil.handle('', 'show')\n"
            "component = ''\n"
            "class Page(PageTemplate):\n"
            "    @handle('missing', 'not_an_event')\n"
            "    @anvil.handle(component, 'show')\n"
            "    @anvil.handle('', 'x-user-event')\n"
            "    def shown(self, **event_args):\n        pass\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("issues"), events)
        self.assertFalse(events[-1]["data"].get("warnings"), events)

    def test_event_catalog_matches_current_runtime_for_canvas_grid_and_textarea(self):
        self.write(
            "client_code/Page.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: canvas\n  type: Canvas\n"
            "- name: grid\n  type: DataGrid\n"
            "- name: input\n  type: TextArea\n",
        )
        file = self.write(
            "client_code/Page.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('canvas', 'reset')\n"
            "    @anvil.handle('grid', 'page_changed')\n"
            "    @anvil.handle('input', 'pressed_enter')\n"
            "    def handle(self, **event_args):\n        pass\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        warnings = events[-1]["data"].get("warnings", [])
        self.assertEqual(len(warnings), 1, events)
        self.assertIn("TextArea has no event 'pressed_enter'", warnings[0]["message"])

    def test_layout_is_a_valid_decorator_target_with_its_declared_events(self):
        self.write(
            "client_code/Layout/form_template.yaml",
            "container:\n  type: ColumnPanel\nslots:\n  default: {}\n"
            "events:\n- name: changed\n  parameters: []\n",
        )
        self.write(
            "client_code/Layout/__init__.py",
            "from ._anvil_designer import LayoutTemplate\n"
            "class Layout(LayoutTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page.yaml",
            "layout:\n  type: form:Layout\ncomponents_by_slot:\n  default:\n"
            "  - name: submit\n    type: Button\n",
        )
        file = self.write(
            "client_code/Page.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('layout', 'changed')\n"
            "    @anvil.handle('submit', 'click')\n"
            "    def changed(self, **event_args):\n        pass\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("issues"), events)
        self.assertFalse(events[-1]["data"].get("warnings"), events)


if __name__ == "__main__":
    unittest.main()
