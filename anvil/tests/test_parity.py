"""Differential acceptance cases through the real CLI, using Pyright as oracle."""

from __future__ import annotations

import json
import os
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "native parity")
class ValidateParity(unittest.TestCase):
    setUp = harness.ValidateIntegration.setUp
    write = harness.ValidateIntegration.write
    validate = harness.ValidateIntegration.validate

    def cache_widgets(self):
        dependency = {
            "app_id": "dep-app",
            "version": {"branch": "master"},
            "resolution_hints": {"package_name": "Widgets"},
        }
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text() + "dependencies: " + json.dumps([dependency]) + "\n"
        )
        self.write(".anvil/deps/Widgets/anvil.yaml", "package_name: Widgets\n")
        self.write(
            ".anvil/deps/manifest.json",
            json.dumps(
                {
                    "version": 3,
                    "includeDocs": False,
                    "source_dependencies": [dependency],
                    "resolved_dependencies": [
                        {"app_id": "dep-app", "commit_id": "cached"}
                    ],
                    "cached_dependencies": [
                        {
                            "app_id": "dep-app",
                            "commit_id": "cached",
                            "package_name": "Widgets",
                        }
                    ],
                }
            ),
        )

    def compare(self, target, rule, severity, count, *, difference=None):
        outcomes = []
        record = {
            "comparison": "known-difference"
            if difference
            else "semantic"
            if isinstance(rule, tuple)
            else "exact",
            "target": str(target.relative_to(self.app)),
            "files": {
                str(path.relative_to(self.app, walk_up=True)): path.read_text()
                for path in sorted(Path(self.temp.name).rglob("*"))
                if path.is_file()
            },
            "outputs": [],
        }
        if difference:
            self.assertIsInstance(count, tuple)
            record["difference"] = difference
        if not hasattr(self, "evidence"):
            self.evidence = []
        self.evidence.append(record)
        for backend in (harness.PYRIGHT / "packages/pyright/index.js", None):
            result, events = self.validate(target, backend=backend)
            # Retain the public CLI result for reproducible differential reports.
            normalized = json.loads(json.dumps(events).replace(str(self.app), "<app>"))
            for event in normalized:
                event.pop("timestamp", None)
            record["outputs"].append(
                {
                    "backend": "pyright" if backend else "native",
                    "exit_code": result.returncode,
                    "events": normalized,
                    "stderr": result.stderr.replace(str(self.app), "<app>"),
                }
            )
            data = events[-1]["data"]
            issues = data.get("issues", []) + data.get("warnings", [])
            for file_result in data.get("files", []):
                issues.extend(file_result.get("issues", []))
                issues.extend(file_result.get("warnings", []))
            expected_rule = (
                rule[0 if backend else 1] if isinstance(rule, tuple) else rule
            )
            matching = [issue for issue in issues if issue.get("rule") == expected_rule]
            expected_count = (
                count[0 if backend else 1] if isinstance(count, tuple) else count
            )
            self.assertEqual(len(matching), expected_count, (backend, issues))
            self.assertTrue(all(issue["severity"] == severity for issue in matching))
            self.assertEqual(len(issues), expected_count, (backend, issues))
            outcomes.append((result.returncode, matching))
        if difference:
            for (exit_code, _), expected_count in zip(outcomes, count, strict=True):
                self.assertEqual(
                    exit_code, 1 if severity == "error" and expected_count else 0
                )
            return
        if isinstance(rule, tuple):
            # Generic checker wording/rule names differ. Protect the same failure,
            # severity, original file and source line; preserve full ranges in evidence.
            self.assertEqual(outcomes[0][0], outcomes[1][0])
            for left, right in zip(outcomes[0][1], outcomes[1][1], strict=True):
                self.assertEqual(
                    (left["file"], left["line"], left["severity"]),
                    (right["file"], right["line"], right["severity"]),
                )
        else:
            self.assertEqual(outcomes[0], outcomes[1])

    def test_skulpt_imports_include_dotted_from_and_nested_imports(self):
        file = self.write(
            "client_code/Runtime.py",
            "import math, subprocess as process\n"
            "from pathlib import Path\n"
            "def later():\n    import os.path\n",
        )
        self.compare(file, "reportAnvilUnsupportedSkulptImport", "error", 3)

    def test_slot_clear_accepts_no_arguments(self):
        file = self.write(
            "client_code/Slots.py",
            "import anvil\n"
            "slot = anvil.Slot(anvil.ColumnPanel(), 0)\n"
            "slot.add_component(anvil.Label(text='Ready'))\n"
            "slot.clear()\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(file.read_text().replace("slot.clear()", "slot.clear(42)"))
        self.compare(
            file, ("reportCallIssue", "too-many-positional-arguments"), "error", 1
        )

    def test_slot_get_components_returns_components(self):
        file = self.write(
            "client_code/SlotChildren.py",
            "import anvil\n"
            "slot = anvil.Slot(anvil.ColumnPanel(), 0)\n"
            "children: list[anvil.Component] = slot.get_components()\n"
            "for child in children:\n    child.remove_from_parent()\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(
            file.read_text()
            .replace("list[anvil.Component]", "list[str]")
            .replace("for child in children:\n    child.remove_from_parent()\n", "")
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_link_inherits_column_panel_constructor_and_container_methods(self):
        file = self.write(
            "client_code/Links.py",
            "import anvil\n"
            "link = anvil.Link(text='Open', spacing_above='none', spacing_below='small')\n"
            "panel: anvil.ColumnPanel = link\n"
            "link.add_component(anvil.Label(text='Child'))\n"
            "children: list[anvil.Component] = link.get_components()\n"
            "link.clear()\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(file.read_text().replace("'small'", "'invalid'"))
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_legacy_component_spacing_accepts_none(self):
        file = self.write(
            "client_code/Spacing.py",
            "import anvil\n"
            "panel = anvil.ColumnPanel(spacing_above=None, spacing_below=None)\n"
            "label = anvil.Label(spacing_above=None, spacing_below=None)\n"
            "link = anvil.Link(spacing_above=None, spacing_below=None)\n"
            "panel.spacing_above = None\n"
            "panel.add_component(label)\n"
            "panel.add_component(link)\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(
            file.read_text().replace(
                "panel.spacing_above = None", "panel.spacing_above = 42"
            )
        )
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )

    def test_history_locations_and_browser_navigation_are_typed(self):
        file = self.write(
            "client_code/Navigation.py",
            "from anvil.history import Location, history, hash_history\n"
            "location = Location(path='/books', search='page=1', hash='title', state={'id': 1})\n"
            "path: str = location.path\n"
            "query: dict[str, str] = location.search_params\n"
            "url: str = Location.from_url('/books', state={}).get_url(full=True)\n"
            "def changed(*, action: str, location: Location, delta: int | None) -> None:\n"
            "    pass\n"
            "unsubscribe = history.listen(changed)\n"
            "history.push(location)\n"
            "history.replace(location)\n"
            "href: str = history.create_href(location)\n"
            "current: Location = history.location\n"
            "history.go()\n"
            "hash_history.go(-1)\n"
            "unsubscribe()\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(
            file.read_text().replace("history.push(location)", "history.push('wrong')")
        )
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)
        server = self.write(
            "server_code/Navigation.py",
            "from anvil.history import Location, history\n"
            "location = Location('/books', 'page=1')\n"
            "url: str = location.get_url(full=True)\n"
            "other: Location = Location.from_url('/books', {'id': 1})\n",
        )
        self.compare(server, None, "error", 0)
        server.write_text(server.read_text() + "history.go(-1)\n")
        self.compare(
            server, ("reportAttributeAccessIssue", "unresolved-attribute"), "error", 1
        )

    def test_custom_exception_registration_and_client_startup_data_are_available(self):
        code = (
            "from anvil.server import AnvilWrappedError, _register_exception_type\n"
            "class Redirect(AnvilWrappedError):\n    pass\n"
            "_register_exception_type('app.Redirect', Redirect)\n"
            "error = Redirect('Moving')\n"
        )
        for environment in ("client", "server"):
            file = self.write(f"{environment}_code/Exceptions.py", code)
            self.compare(file, None, "error", 0)
            file.write_text(
                code.replace(
                    "_register_exception_type('app.Redirect', Redirect)",
                    "_register_exception_type('app.Redirect', 'wrong')",
                )
            )
            self.compare(
                file, ("reportArgumentType", "invalid-argument-type"), "error", 1
            )
        client = self.write(
            "client_code/Startup.py",
            "from anvil.server import startup_data\n"
            "cache = startup_data.get('cache', {}) if startup_data is not None else {}\n",
        )
        self.compare(client, None, "error", 0)

        server = self.write(
            "server_code/Startup.py",
            "import anvil.server\nvalue = anvil.server.startup_data\n",
        )
        self.compare(
            server, ("reportAttributeAccessIssue", "unresolved-attribute"), "error", 1
        )

    def test_app_responder_is_available_only_on_server(self):
        file = self.write(
            "server_code/Responses.py",
            "from anvil.server import AppResponder\n"
            "responder = AppResponder(data={'cache': {}}, meta={'title': 'Books'})\n"
            "response = responder.load_app()\n"
            "form_response = responder.load_form('Books', category='fiction')\n"
            "module_response = responder.load_module('startup')\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(file.read_text().replace("AppResponder(data=", "AppResponder("))
        self.compare(
            file, ("reportCallIssue", "too-many-positional-arguments"), "error", 1
        )
        client = self.write(
            "client_code/Responses.py",
            "import anvil.server\nresponse = anvil.server.AppResponder()\n",
        )
        self.compare(
            client, ("reportAttributeAccessIssue", "unresolved-attribute"), "error", 1
        )

    def test_anonymous_template_components_preserve_named_children_and_events(self):
        self.write(
            "client_code/Form1/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: $component_1\n  type: ColumnPanel\n  components:\n"
            "  - name: label_1\n    type: Label\n",
        )
        file = self.write(
            "client_code/Form1/__init__.py",
            "import anvil\nfrom ._anvil_designer import Form1Template\n"
            "class Form1(Form1Template):\n"
            "    def __init__(self, **properties):\n"
            "        self.init_components(**properties)\n"
            "        self.label_1.text = 'Ready'\n"
            "    @anvil.handle('$component_1', 'show')\n"
            "    def shown(self, **event_args):\n        pass\n",
        )
        self.compare(file, None, "error", 0)
        file.write_text(file.read_text().replace("'Ready'", "42"))
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )

    def test_server_calls_check_names_without_rejecting_dynamic_or_known_calls(self):
        file = self.write(
            "client_code/Calls.py",
            "import anvil.server\nfrom anvil import server\n"
            "anvil.server.call('title')\n"
            "name = 'uplink_function'\nserver.call(name)\n"
            "marker = '😀'; anvil.server.call('missing')\n"
            "server.call_s('missing_sync')\n",
        )
        self.compare(file, "reportAnvilUnknownCallable", "warning", 2)

    def test_background_tasks_and_named_callables_are_registered(self):
        self.write(
            "server_code/Tasks.py",
            "import anvil.server\n"
            "@anvil.server.callable(name='public_name')\ndef internal_name() -> str:\n    return 'ok'\n"
            "@anvil.server.background_task\ndef rebuild() -> None:\n    pass\n",
        )
        file = self.write(
            "server_code/Caller.py",
            "import anvil.server\nfrom anvil import server\n"
            "anvil.server.call('public_name')\n"
            "server.launch_background_task('rebuild')\n"
            "server.launch_background_task('missing_task')\n",
        )
        self.compare(file, "reportAnvilUnknownBackgroundTask", "warning", 1)

    def test_local_decorator_named_callable_is_not_an_anvil_registration(self):
        file = self.write(
            "server_code/Decorators.py",
            "from typing import Callable, TypeVar\n"
            "_F = TypeVar('_F', bound=Callable[..., object])\n"
            "def callable(fn: _F) -> _F:\n    return fn\n"
            "@callable\ndef local_only() -> str:\n    return 'ok'\n",
        )
        self.compare(file, "reportAnvilFalseCallableDecorator", "warning", 1)

    def test_false_decorator_rule_can_be_promoted_to_error(self):
        self.write(
            "pyrightconfig.json",
            '{"reportAnvilFalseCallableDecorator": "error"}',
        )
        file = self.write(
            "server_code/Configured.py",
            "from typing import Callable, TypeVar\n"
            "_F = TypeVar('_F', bound=Callable[..., object])\n"
            "def callable(fn: _F) -> _F:\n    return fn\n"
            "@callable\ndef local_only() -> str:\n    return 'ok'\n",
        )
        self.compare(file, "reportAnvilFalseCallableDecorator", "error", 1)

    def test_jsonc_configuration_can_disable_false_decorator_warnings(self):
        self.write(
            "pyrightconfig.json",
            "// Config files permit comments and trailing commas.\n"
            '{"reportAnvilFalseCallableDecorator": false,}\n',
        )
        file = self.write(
            "server_code/Configured.py",
            "from typing import Callable, TypeVar\n"
            "_F = TypeVar('_F', bound=Callable[..., object])\n"
            "def callable(fn: _F) -> _F:\n    return fn\n"
            "@callable\ndef local_only() -> str:\n    return 'ok'\n",
        )
        self.compare(file, "reportAnvilFalseCallableDecorator", "warning", 0)

    def test_supported_imports_local_names_and_stub_imports_remain_valid(self):
        self.write("client_code/os.py", "token = 'ok'\n")
        self.write("client_code/os.pyi", "import subprocess\ntoken: str\n")
        client = self.write(
            "client_code/Allowed.py",
            "import math, signal, types, urllib.request\nfrom .os import token\n",
        )
        server = self.write(
            "server_code/Allowed.py", "import subprocess\nfrom pathlib import Path\n"
        )
        for file in (client, server):
            with self.subTest(file=file):
                self.compare(file, "reportAnvilUnsupportedSkulptImport", "error", 0)

    def test_client_extra_paths_cannot_import_server_modules(self):
        self.write("pyrightconfig.json", '{"extraPaths": ["server_code", "libraries"]}')
        self.write(
            "server_code/Secret.py", "def private() -> str:\n    return 'secret'\n"
        )
        self.write("libraries/Public.py", "def public() -> str:\n    return 'public'\n")
        client = self.write(
            "client_code/Paths.py",
            "from Public import public\nvalue: str = public()\n",
        )
        self.compare(client, None, "error", 0)
        client.write_text("from Secret import private\nvalue: str = private()\n")
        self.compare(
            client,
            ("reportMissingImports", "reportAnvilImportRestriction"),
            "error",
            1,
        )
        server = self.write(
            "server_code/Paths.py",
            "from Secret import private\nvalue: str = private()\n",
        )
        self.compare(server, None, "error", 0)

        self.write("pyrightconfig.json", '{"extraPaths": [".", "libraries"]}')
        client.write_text(
            "from server_code import Secret\nvalue: str = Secret.private()\n"
        )
        self.compare(
            client,
            "reportAnvilImportRestriction",
            "error",
            (0, 1),
            difference="Pyright misses server ownership through a namespace from-import",
        )

    def test_real_aliased_decorators_are_not_reported_as_false_registrations(self):
        file = self.write(
            "server_code/Aliases.py",
            "import anvil.server\nfrom anvil.server import callable as rpc\n"
            "@rpc('alias_name')\ndef internal_name() -> str:\n    return 'ok'\n",
        )
        self.compare(file, "reportAnvilFalseCallableDecorator", "warning", 0)
        file.write_text(file.read_text() + "anvil.server.call('alias_name')\n")
        self.compare(
            file,
            "reportAnvilUnknownCallable",
            "warning",
            (1, 0),
            difference="Pyright misses positional callable names through an imported decorator alias",
        )

    def test_yaml_module_and_package_forms_share_designer_namespace(self):
        for name in ("Home", "SubForm", "OtherForm"):
            is_package = name == "Home"
            template = (
                f"client_code/Home/{'form_template' if is_package else name}.yaml"
            )
            self.write(
                template,
                "container:\n  type: ColumnPanel\ncomponents:\n- name: button_1\n  type: Button\n",
            )
            self.write(
                f"client_code/Home/{'__init__' if is_package else name}.py",
                f"from ._anvil_designer import {name}Template\n"
                f"class {name}({name}Template):\n"
                "    def configure(self) -> None:\n        self.button_1.text = 'Ready'\n",
            )
        file = self.write(
            "client_code/UseForms.py",
            "from .Home import Home\nfrom .Home.SubForm import SubForm\n"
            "from .Home.OtherForm import OtherForm\n"
            "for form in (Home(), SubForm(), OtherForm()):\n"
            "    form.configure()\n    form.button_1.text = 'Ready'\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)

    def test_named_html_fragments_reject_dom_only_attributes(self):
        self.write(
            "client_code/Page/form_template.html",
            '<main><button anvil:name="submit">Submit</button></main>',
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        self.submit.text = 'Ready'\n",
        )
        self.compare(
            file, ("reportAttributeAccessIssue", "unresolved-attribute"), "error", 1
        )

    def test_named_plain_html_fragments_are_htmlcomponents(self):
        self.write(
            "client_code/Page/form_template.html",
            '<main anvil:name="ignored_root"><button anvil:name="submit" '
            'anvil:on-dom:click="self.clicked">Submit</button></main>',
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def clicked(self, event) -> None:\n        self.submit.classes.add('active')\n"
            "        self.submit.html = 'Ready'\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)

    def test_html_dom_nodes_keep_tag_specific_types_per_form(self):
        for name, body, assignment in (
            (
                "Inputs",
                '<input anvil:dom-node="email_input">',
                'self.dom_nodes["email_input"].value = "hello@example.com"',
            ),
            (
                "Buttons",
                '<button anvil:dom-node="submit-button">Submit</button>',
                'self.dom_nodes["submit-button"].textContent = "Working"',
            ),
        ):
            self.write(
                f"client_code/Forms/{name}.html",
                f'<anvil-form container="HtmlComponent">{body}</anvil-form>',
            )
            self.write(
                f"client_code/Forms/{name}.py",
                f"from ._anvil_designer import {name}Template\n"
                f"class {name}({name}Template):\n"
                f"    def configure(self) -> None:\n        {assignment}\n",
            )
        for name in ("Inputs", "Buttons"):
            with self.subTest(form=name):
                self.compare(
                    self.app / f"client_code/Forms/{name}.py",
                    "reportMissingImports",
                    "error",
                    0,
                )

    def test_html_dom_nodes_reject_unknown_keys(self):
        self.write(
            "client_code/Page/form_template.html",
            '<anvil-form container="HtmlComponent"><input anvil:dom-node="email_input"></anvil-form>',
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            '    def configure(self) -> None:\n        self.dom_nodes["missing"]\n',
        )
        self.compare(file, ("reportGeneralTypeIssues", "invalid-key"), "error", 1)

    def test_html_dom_nodes_propagate_element_property_types(self):
        self.write(
            "client_code/Page/form_template.html",
            '<anvil-form container="HtmlComponent"><input anvil:dom-node="email_input"></anvil-form>',
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            '    def configure(self) -> None:\n        value: int = self.dom_nodes["email_input"].value\n',
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_legacy_yaml_htmltemplate_dom_nodes_use_anvil_name(self):
        self.write(
            "client_code/Legacy/form_template.yaml",
            "container:\n  type: HtmlTemplate\n  properties:\n"
            '    html: |-\n      <input anvil-name="email_input">\ncomponents: []\n',
        )
        file = self.write(
            "client_code/Legacy/__init__.py",
            "from ._anvil_designer import LegacyTemplate\nclass Legacy(LegacyTemplate):\n"
            '    def configure(self) -> None:\n        self.dom_nodes["email_input"].value = "hello@example.com"\n',
        )
        self.compare(file, "reportMissingImports", "error", 0)

    def test_html_package_and_module_forms_expose_builtin_components(self):
        for name, template, code in (
            ("Page", "Page/form_template.html", "Page/__init__.py"),
            ("Footer", "Footer.html", "Footer.py"),
        ):
            self.write(
                f"client_code/{template}",
                '<anvil-form container="ColumnPanel"><section>'
                '<anvil-component type="Button" name="html_button"></anvil-component>'
                "</section></anvil-form>",
            )
            self.write(
                f"client_code/{code}",
                f"from ._anvil_designer import {name}Template\n"
                f"class {name}({name}Template):\n"
                "    def configure(self) -> None:\n        self.html_button.text = 'Ready'\n",
            )
        file = self.write(
            "client_code/UseHtml.py",
            "from .Page import Page\nfrom .Footer import Footer\n"
            "Page().configure()\nFooter().configure()\n"
            "Page().html_button.text = 'Ready'\nFooter().html_button.text = 'Ready'\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)

    def test_html_frontmatter_custom_properties_and_constructor_are_typed(self):
        self.write(
            "client_code/Widget/form_template.html",
            "---\ncustom_component: true\nproperties:\n"
            "- name: theme\n  type: enum\n  options: [light, dark]\n"
            "- name: enabled\n  type: boolean\n---\n"
            '<anvil-form container="ColumnPanel"></anvil-form>',
        )
        file = self.write(
            "client_code/Widget/__init__.py",
            "from ._anvil_designer import WidgetTemplate\nclass Widget(WidgetTemplate):\n"
            "    def configure(self) -> None:\n        self.theme = 'dark'\n        self.enabled = True\n"
            "widget = Widget(theme='light', enabled=True)\nwidget.configure()\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)

    def test_custom_property_constructor_rejects_values_outside_enum(self):
        self.write(
            "client_code/Widget/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\nproperties:\n"
            "- name: theme\n  type: enum\n  options: [light, dark]\n",
        )
        file = self.write(
            "client_code/Widget/__init__.py",
            "from ._anvil_designer import WidgetTemplate\nclass Widget(WidgetTemplate):\n    pass\n"
            "widget = Widget(theme='unknown')\n",
        )
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_local_custom_components_preserve_property_types(self):
        self.write(
            "client_code/Widgets/ThemeSelector/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\nproperties:\n"
            "- name: theme\n  type: enum\n  options: [light, dark]\n",
        )
        self.write(
            "client_code/Widgets/ThemeSelector/__init__.py",
            "from ._anvil_designer import ThemeSelectorTemplate\n"
            "class ThemeSelector(ThemeSelectorTemplate):\n    pass\n",
        )
        for name, kind in (
            ("Page", "TyProof.Widgets.ThemeSelector"),
            ("Legacy", "form:Widgets.ThemeSelector"),
        ):
            self.write(
                f"client_code/{name}/form_template.yaml",
                f"container:\n  type: ColumnPanel\ncomponents:\n- name: selector\n  type: {kind}\n",
            )
            file = self.write(
                f"client_code/{name}/__init__.py",
                f"from ._anvil_designer import {name}Template\nclass {name}({name}Template):\n"
                "    def configure(self) -> None:\n        self.selector.theme = 'dark'\n",
            )
            with self.subTest(reference=kind):
                self.compare(file, "reportMissingImports", "error", 0)
                file.write_text(file.read_text().replace("'dark'", "'sepia'"))
                self.compare(
                    file,
                    ("reportAttributeAccessIssue", "invalid-assignment"),
                    "error",
                    1,
                )

    def test_unknown_handle_component_warns_even_when_baseline_cli_misses_it(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: submit\n  type: Button\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    @anvil.handle('missing', 'click')\n"
            "    def clicked(self, **event_args):\n        pass\n",
        )
        # Source-level tests pre-generate designer stubs before binding. The real
        # one-shot CLI currently emits no warning for this invalid component.
        self.compare(
            file,
            "reportAnvilUnknownComponent",
            "warning",
            (0, 1),
            difference="Native validate checks decorator component names before binding; the baseline CLI misses this check.",
        )

    def test_existing_html_fixture_outside_parent_ignore_configuration(self):
        fixture = (
            harness.PYRIGHT
            / "packages/pyright-internal/src/tests/benchmarkData/anvil_memory_app"
        )
        # The original checkout's pyproject.toml ignores packages/, masking this
        # fixture's errors. Copy the actual app outside that inherited config.
        for path in sorted(fixture.rglob("*")):
            if path.is_file():
                self.write(str(path.relative_to(fixture)), path.read_text())
        for name in ("Form1", "Form3"):
            with self.subTest(form=name):
                self.compare(
                    self.app / f"client_code/{name}/__init__.py",
                    ("reportAttributeAccessIssue", "unresolved-attribute"),
                    "error",
                    3,
                )

    def test_bound_event_handlers_accept_common_signatures_and_direct_calls(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: button_1\n  type: Button\n  event_bindings:\n    click: button_1_click\n"
            "- name: button_2\n  type: Button\n  event_bindings:\n    click: button_2_click\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def button_1_click(self, sender, **event_args) -> str:\n        return 'done'\n"
            "    def button_2_click(self, **event_args):\n        pass\n"
            "    def configure(self) -> None:\n        self.button_2_click()\n"
            "Page().configure()\n",
        )
        self.compare(file, "reportIncompatibleMethodOverride", "error", 0)

    def test_bound_event_methods_still_check_concrete_user_arguments(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: button_1\n  type: Button\n  event_bindings:\n    click: button_1_click\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def button_1_click(self, sender: anvil.Button, **event_args):\n        pass\n"
            "    def configure(self) -> None:\n        self.button_1_click(sender='wrong')\n",
        )
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_bound_event_handler_missing_implementation_prevents_instantiation(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: button_1\n  type: Button\n  event_bindings:\n    click: button_1_click\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n    pass\n"
            "Page()\n",
        )
        self.compare(file, ("reportAbstractUsage", "call-non-callable"), "error", 1)

    def test_html_component_event_bindings_resolve_handlers(self):
        self.write(
            "client_code/Page/form_template.html",
            '<anvil-form container="ColumnPanel"><anvil-component type="Button" '
            'name="submit" on:click="self.submit_click"></anvil-component></anvil-form>',
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def submit_click(self, sender, **event_args):\n        self.submit.text = 'Ready'\n"
            "Page()\n",
        )
        self.compare(file, "reportIncompatibleMethodOverride", "error", 0)

    def test_yaml_data_bindings_support_item_and_refresh(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: title\n  type: Label\n"
            "  data_bindings:\n  - property: text\n    code: self.item['title']\n    writeback: false\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        self.item = {'title': 'Ready'}\n"
            "        self.refresh_data_bindings()\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)

    def test_custom_item_property_keeps_its_declared_type(self):
        self.write(
            "client_code/Page/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\nproperties:\n"
            "- name: item\n  type: string\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        self.item = 123\n",
        )
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )

    def test_html_data_binding_prefixes_support_refresh(self):
        for name, body in (
            (
                "Input",
                '<anvil-component type="TextBox" name="field" bind:text="self.item[\'name\']" writeback:text="self.item[\'name\']"></anvil-component>',
            ),
            (
                "Fragment",
                '<section anvil:name="content" anvil:bind:html="self.item[\'body\']"></section>',
            ),
        ):
            self.write(
                f"client_code/{name}.html",
                f'<anvil-form container="ColumnPanel">{body}</anvil-form>',
            )
            file = self.write(
                f"client_code/{name}.py",
                f"from ._anvil_designer import {name}Template\nclass {name}({name}Template):\n"
                "    def configure(self) -> None:\n        self.item = {'name': 'Ready', 'body': 'Hello'}\n"
                "        self.refresh_data_bindings()\n",
            )
            with self.subTest(form=name):
                self.compare(file, "reportAttributeAccessIssue", "error", 0)

    def test_custom_event_parameters_and_sender_are_checked(self):
        self.write(
            "client_code/Widget/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\nevents:\n"
            "- name: changed\n  parameters:\n  - name: value\n",
        )
        file = self.write(
            "client_code/Widget/__init__.py",
            "from ._anvil_designer import WidgetTemplate\nclass Widget(WidgetTemplate):\n"
            "    def configure(self) -> None:\n"
            "        self.changed(sender=self, event_name='changed', value=123)\n",
        )
        self.compare(file, "reportArgumentType", "error", 0)
        file.write_text(file.read_text().replace("sender=self", "sender='wrong'"))
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_custom_event_methods_accept_sender_and_keep_concrete_call_checking(self):
        self.write(
            "client_code/Widget/form_template.yaml",
            "custom_component: true\ncontainer:\n  type: ColumnPanel\nevents:\n"
            "- name: row_click\n",
        )
        file = self.write(
            "client_code/Widget/__init__.py",
            "import anvil\nfrom ._anvil_designer import WidgetTemplate\n"
            "class Widget(WidgetTemplate):\n"
            "    def row_click(self, sender: anvil.Button, **event_args) -> str:\n"
            "        self.raise_event('row_click', **event_args)\n"
            "        return 'done'\n"
            "    def configure(self):\n"
            "        self.row_click(sender=anvil.Button())\n"
            "Widget().configure()\n",
        )
        self.compare(
            file,
            ("reportIncompatibleMethodOverride", "invalid-method-override"),
            "error",
            (1, 0),
            difference="Untyped custom-event declarations permit ordinary sender/event_args callback methods; the baseline's strict generated method rejects them.",
        )
        # Suppress the baseline's known override error to compare the independent
        # concrete-call check. The valid control above uses default settings.
        self.write("pyrightconfig.json", '{"reportIncompatibleMethodOverride": "none"}')
        file.write_text(
            file.read_text().replace("sender=anvil.Button()", "sender='wrong'")
        )
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_layout_slots_and_properties_are_typed(self):
        self.write(
            "client_code/Layout/form_template.yaml",
            "container:\n  type: ColumnPanel\nslots:\n  default: {}\nproperties:\n"
            "- name: title\n  type: string\n",
        )
        file = self.write(
            "client_code/Layout/__init__.py",
            "import anvil\nfrom ._anvil_designer import LayoutTemplate\nclass Layout(LayoutTemplate):\n"
            "    def configure(self) -> None:\n        self.title = 'Ready'\n"
            "        self.slots['default'].add_component(anvil.Label(text='Hello'))\n"
            "Layout(title='Welcome').configure()\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)
        file.write_text(
            file.read_text().replace("anvil.Label(text='Hello')", "'wrong'")
        )
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_yaml_forms_with_layouts_expose_layout_and_slotted_components(self):
        self.write(
            "client_code/Layout/form_template.yaml",
            "container:\n  type: ColumnPanel\nslots:\n  default: {}\nproperties:\n"
            "- name: title\n  type: string\n",
        )
        self.write(
            "client_code/Layout/__init__.py",
            "from ._anvil_designer import LayoutTemplate\nclass Layout(LayoutTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "layout:\n  type: form:Layout\ncomponents_by_slot:\n  default:\n"
            "  - name: submit\n    type: Button\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        self.layout.title = 'Ready'\n"
            "        self.submit.text = 'Submit'\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)
        file.write_text(
            file.read_text().replace(
                "self.layout.title = 'Ready'", "self.layout.title = 123"
            )
        )
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )

    def test_yaml_layout_event_handlers_require_an_implementation(self):
        self.write(
            "client_code/Layout/form_template.yaml", "container:\n  type: ColumnPanel\n"
        )
        self.write(
            "client_code/Layout/__init__.py",
            "from ._anvil_designer import LayoutTemplate\nclass Layout(LayoutTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "layout:\n  type: form:Layout\n  form_event_bindings:\n    show: layout_show\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n    pass\nPage()\n",
        )
        self.compare(file, ("reportAbstractUsage", "call-non-callable"), "error", 1)
        file.write_text(
            file.read_text().replace(
                "    pass", "    def layout_show(self, **event_args):\n        pass"
            )
        )
        self.compare(file, "reportIncompatibleMethodOverride", "error", 0)

    def test_html_layout_form_events_require_handlers(self):
        self.write(
            "client_code/Layout/form_template.yaml", "container:\n  type: ColumnPanel\n"
        )
        self.write(
            "client_code/Layout/__init__.py",
            "from ._anvil_designer import LayoutTemplate\nclass Layout(LayoutTemplate):\n    pass\n",
        )
        template = self.write(
            "client_code/Page/form_template.html",
            '<anvil-form layout="TyProof.Layout" on:show="self.form_show"></anvil-form>',
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n    pass\nPage()\n",
        )
        self.compare(file, ("reportAbstractUsage", "call-non-callable"), "error", 1)
        file.write_text(
            file.read_text().replace(
                "    pass", "    def form_show(self, **event_args):\n        pass"
            )
        )
        self.compare(file, "reportIncompatibleMethodOverride", "error", 0)
        template.write_text(
            '<anvil-form layout="TyProof.Layout" on:layout:show="self.layout_show"></anvil-form>'
        )
        self.compare(file, "reportAbstractUsage", "error", 0)

    def test_html_layouts_and_slots_preserve_layout_property_types(self):
        self.write(
            "client_code/Layout/form_template.html",
            "---\nproperties:\n- name: title\n  type: string\n---\n"
            '<anvil-form container="ColumnPanel"><anvil-slot name="default"></anvil-slot></anvil-form>',
        )
        self.write(
            "client_code/Layout/__init__.py",
            "from ._anvil_designer import LayoutTemplate\nclass Layout(LayoutTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page/form_template.html",
            '<anvil-form layout="TyProof.Layout"><anvil-block slot="default">'
            '<anvil-component type="Button" name="submit"></anvil-component>'
            "</anvil-block></anvil-form>",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        self.layout.title = 'Ready'\n"
            "        self.layout.slots['default'].add_component(anvil.Label())\n"
            "        self.submit.text = 'Submit'\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)

    def test_schema_rows_and_table_queries_propagate_column_types(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    python_name: people\n    columns:\n"
            "    - name: name\n      type: string\n    - name: age\n      type: number\n"
        )
        file = self.write(
            "server_code/People.py",
            "from anvil.tables import app_tables\n"
            "row = app_tables.people.add_row(name='Ada', age=37)\n"
            "title: str = row['name']\nrow.update(name='Grace')\n"
            "for person in app_tables.people.search(name='Ada'):\n    label: str = person['name']\n"
            "found = app_tables.people.get(name='Ada')\n"
            "if found is not None:\n    other: str = found['name']\n",
        )
        self.compare(file, "reportArgumentType", "error", 0)
        file.write_text(file.read_text().replace("title: str", "title: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_table_writes_check_declared_column_types_in_both_environments(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        for environment in ("client", "server"):
            file = self.write(
                f"{environment}_code/People.py",
                "from anvil.tables import app_tables\napp_tables.people.add_row(name=123)\n",
            )
            with self.subTest(environment=environment):
                self.compare(
                    file, ("reportArgumentType", "invalid-argument-type"), "error", 1
                )

    def test_linked_tables_use_target_python_names_and_typed_iterators(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  Teams:\n    python_name: groups\n    columns:\n"
            "    - name: title\n      type: string\n  People:\n    python_name: people\n    columns:\n"
            "    - name: team\n      type: link_single\n      target: Teams\n"
            "    - name: teams\n      type: link_multiple\n      target: Teams\n"
        )
        file = self.write(
            "server_code/Links.py",
            "from anvil.tables import app_tables\n"
            "person = app_tables.people.add_row(team=app_tables.groups.add_row(title='Anvil'), teams=app_tables.groups.search())\n"
            "title: str = person['team']['title']\n"
            "for team in person['teams']:\n    label: str = team['title']\n",
        )
        self.compare(file, "reportAssignmentType", "error", 0)
        file.write_text(file.read_text().replace("title: str", "title: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_form_item_table_rows_preserve_schema_types(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\nitem_type:\n  table_name: people\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from anvil.tables import app_tables\nfrom ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        self.item = app_tables.people.add_row(name='Ada')\n"
            "        title: str = self.item['name']\n",
        )
        self.compare(file, "reportAssignmentType", "error", 0)
        file.write_text(file.read_text().replace("title: str", "title: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_users_service_returns_typed_optional_user_rows(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "services:\n- source: /runtime/services/anvil/users.yml\n"
            "  server_config:\n    user_table: Accounts\n"
            "db_schema:\n  Accounts:\n    python_name: users\n    columns:\n"
            "    - name: email\n      type: string\n"
        )
        for environment in ("client", "server"):
            file = self.write(
                f"{environment}_code/Account.py",
                "import anvil.users\nuser = anvil.users.get_user()\n"
                "if user is not None:\n    email: str = user['email']\n",
            )
            with self.subTest(environment=environment):
                self.compare(file, "reportAssignmentType", "error", 0)
                file.write_text(file.read_text().replace("email: str", "email: int"))
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                )

    def test_google_drive_app_files_keep_mime_specific_types(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text() + "services:\n- source: /runtime/services/google.yml\n"
            "  client_config:\n    app_files:\n"
            "    - {id: sheet-id, python_name: workbook, mimeType: application/vnd.google-apps.spreadsheet}\n"
            "    - {id: folder-id, python_name: documents, mimeType: application/vnd.google-apps.folder}\n"
            "    - {id: file-id, python_name: readme, mimeType: text/plain}\n"
        )
        for environment in ("client", "server"):
            file = self.write(
                f"{environment}_code/Files.py",
                "from anvil.google.drive import app_files, Folder, File\n"
                "from anvil.google.sheets import Spreadsheet\n"
                "sheet: Spreadsheet = app_files.workbook\nfolder: Folder = app_files.documents\n"
                "readme: File = app_files.readme\n",
            )
            with self.subTest(environment=environment):
                self.compare(file, "reportAssignmentType", "error", 0)
                file.write_text(
                    file.read_text().replace(
                        "sheet: Spreadsheet = app_files.workbook",
                        "sheet: Spreadsheet = app_files.documents",
                    )
                )
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                )

    def test_table_model_subclasses_supply_methods_on_fetched_rows(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        file = self.write(
            "server_code/Models.py",
            "from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attrs=True):\n"
            "    def greeting(self) -> str:\n        return self.name\n"
            "person = app_tables.people.add_row(name='Ada')\n"
            "title: str = person.greeting()\n"
            "found = app_tables.people.get(name='Ada')\n"
            "if found is not None:\n    other: str = found.greeting()\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)
        file.write_text(file.read_text().replace("title: str", "title: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_row_models_are_scoped_to_client_and_server_environments(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        for environment, model, kind, result in (
            ("client", "ClientPerson", "str", "'Ready'"),
            ("server", "ServerPerson", "int", "42"),
        ):
            self.write(
                f"{environment}_code/{model}.py",
                "from anvil.tables import app_tables\n"
                f"class {model}(app_tables.people.Row, attrs=True):\n"
                f"    def greeting(self) -> {kind}:\n        return {result}\n",
            )
        for environment, model, kind in (
            ("client", "ClientPerson", "str"),
            ("server", "ServerPerson", "int"),
        ):
            file = self.write(
                f"{environment}_code/UseModel.py",
                f"from .{model} import {model}\nfrom anvil.tables import app_tables\n"
                f"value: {kind} = app_tables.people.add_row(name='Ada').greeting()\n",
            )
            with self.subTest(environment=environment):
                self.compare(file, "reportAssignmentType", "error", 0)
                file.write_text(
                    file.read_text().replace(
                        f"value: {kind}", f"value: {'int' if kind == 'str' else 'str'}"
                    )
                )
                self.compare(
                    file,
                    ("reportAssignmentType", "invalid-assignment"),
                    "error",
                    (0, 1) if environment == "server" else 1,
                    difference="With both client and server row models, the baseline accepts an incompatible server result assignment; native preserves the server model's declared return type."
                    if environment == "server"
                    else None,
                )

    def test_users_service_preserves_user_model_methods(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "services:\n- source: /runtime/services/anvil/users.yml\n"
            "db_schema:\n  users:\n    columns:\n    - name: email\n      type: string\n"
        )
        file = self.write(
            "server_code/Models.py",
            "import anvil.users\nfrom anvil.tables import app_tables\n"
            "class User(app_tables.users.Row, attrs=True):\n"
            "    def display_name(self) -> str:\n        return self.email\n"
            "user = anvil.users.get_user()\nif user is not None:\n    name: str = user.display_name()\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)
        file.write_text(file.read_text().replace("name: str", "name: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_server_overlay_does_not_import_a_hidden_client_row_model(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        self.write(
            "client_code/Models.py",
            "from anvil.tables import app_tables\n"
            "class Person(app_tables.people.Row, attrs=True):\n"
            "    def greeting(self) -> str:\n        return self.name\n",
        )
        self.write("server_code/Models.py", "marker = 42\n")
        file = self.write(
            "server_code/UseModel.py",
            "from .Models import marker\nfrom anvil.tables import app_tables\n"
            "value: int = app_tables.people.add_row(name='Ada')['name']\n",
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)
        file.write_text(file.read_text().replace("value: int", "value: str"))
        self.compare(file, "reportAssignmentType", "error", 0)

    def test_form_items_preserve_client_row_model_methods(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    columns:\n    - name: name\n      type: string\n"
        )
        self.write(
            "client_code/Models.py",
            "from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attrs=True):\n"
            "    def greeting(self) -> str:\n        return self.name\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\nitem_type:\n  table_name: people\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ..Models import Person\nfrom ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n"
            "    def configure(self) -> None:\n        title: str = self.item.greeting()\n",
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)
        file.write_text(file.read_text().replace("title: str", "title: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_whole_app_combines_forms_tables_and_server_code(self):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "db_schema:\n  people:\n    title: People\n    client: full\n    server: full\n    columns:\n    - name: name\n      type: string\n"
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\nitem_type:\n  table_name: people\n  table_id: 1\ncomponents:\n- name: submit\n  type: Button\n  event_bindings: {click: submit_click}\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n    def configure(self) -> None:\n        title: str = self.item['name']\n        self.submit.text = 'Ready'\n    def submit_click(self, **event_args) -> None:\n        self.refresh_data_bindings()\n",
        )
        self.write(
            "client_code/Main.py",
            "from .Page import Page\npage = Page()\npage.configure()\n",
        )
        self.write(
            "server_code/UseTables.py",
            "from anvil.tables import app_tables\nrow = app_tables.people.add_row(name='Ada')\nname: str = row['name']\n",
        )
        self.compare(self.app, "reportAssignmentType", "error", 0)
        file.write_text(file.read_text().replace("title: str", "title: int"))
        self.compare(
            self.app, ("reportAssignmentType", "invalid-assignment"), "error", 1
        )

    def test_missing_dependency_keeps_cli_cache_warning_without_blocking_validation(
        self,
    ):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text()
            + "dependencies:\n- app_id: missing-app\n  version: {branch: master}\n"
        )
        self.compare(
            self.app / "client_code/Helpers.py",
            "reportAnvilDependencyCache",
            "warning",
            1,
        )

    def test_cached_dependency_client_namespace_preserves_declared_types(self):
        self.cache_widgets()
        self.write(
            ".anvil/deps/Widgets/client_code/Helpers.py",
            "def title() -> str:\n    return 'Widget'\n",
        )
        file = self.write(
            "client_code/UseDependency.py",
            "from Widgets.Helpers import title\nlabel: str = title()\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text(file.read_text().replace("label: str", "label: int"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_cached_dependency_server_overlays_client_and_registers_callables(self):
        self.cache_widgets()
        self.write(
            ".anvil/deps/Widgets/client_code/Shared.py",
            "def value() -> str:\n    return 'Widget'\n",
        )
        self.write(
            ".anvil/deps/Widgets/client_code/Fallback.py",
            "def title() -> str:\n    return 'Client fallback'\n",
        )
        self.write(
            ".anvil/deps/Widgets/server_code/Shared.py",
            "import anvil.server\n@anvil.server.callable\ndef dependency_value() -> int:\n    return 42\ndef value() -> int:\n    return dependency_value()\n",
        )
        file = self.write(
            "server_code/UseDependency.py",
            "import anvil.server\nfrom Widgets.Shared import value\nfrom Widgets.Fallback import title\nnumber: int = value()\nlabel: str = title()\nanvil.server.call('dependency_value')\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text(file.read_text().replace("number: int", "number: str"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_app_and_dependency_module_collisions_preserve_class_identity_per_environment(
        self,
    ):
        self.cache_widgets()
        for environment, local_type, local_value, dependency_type, dependency_value in (
            ("client", "int", "42", "str", "'Dependency'"),
            ("server", "bool", "True", "float", "2.5"),
        ):
            self.write(
                f"{environment}_code/Shared.py",
                f"class Widget:\n    value: {local_type} = {local_value}\n",
            )
            self.write(
                f".anvil/deps/Widgets/{environment}_code/Shared.py",
                f"class Widget:\n    value: {dependency_type} = {dependency_value}\n",
            )
        for environment, local_type, dependency_type in (
            ("client", "int", "str"),
            ("server", "bool", "float"),
        ):
            with self.subTest(environment=environment):
                file = self.write(
                    f"{environment}_code/UseWidgets.py",
                    "from Widgets.Shared import Widget\n"
                    "from TyProof.Shared import Widget as LocalWidget\n"
                    "local: LocalWidget = LocalWidget()\n"
                    "dependency: Widget = Widget()\n"
                    f"local_value: {local_type} = local.value\n"
                    f"dependency_value: {dependency_type} = dependency.value\n",
                )
                self.compare(file, "reportAssignmentType", "error", 0)
                file.write_text(
                    file.read_text().replace(
                        "local: LocalWidget = LocalWidget()",
                        "local: LocalWidget = Widget()",
                    )
                )
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                )

    def test_cached_dependency_form_designer_types_reach_importers(self):
        self.cache_widgets()
        self.write(
            ".anvil/deps/Widgets/client_code/Card/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: label\n  type: Label\n",
        )
        self.write(
            ".anvil/deps/Widgets/client_code/Card/__init__.py",
            "from ._anvil_designer import CardTemplate\nclass Card(CardTemplate):\n    pass\n",
        )
        file = self.write(
            "client_code/UseDependency.py",
            "from Widgets.Card import Card\ncard = Card()\ncard.label.text = 'Ready'\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text(file.read_text().replace("'Ready'", "42"))
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )

    def test_dependency_form_references_keep_component_types_in_app_designers(self):
        self.cache_widgets()
        self.write(
            ".anvil/deps/Widgets/client_code/Card/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: label\n  type: Label\n",
        )
        self.write(
            ".anvil/deps/Widgets/client_code/Card/__init__.py",
            "from ._anvil_designer import CardTemplate\nclass Card(CardTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: card\n  type: form:dep-app:Card\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "from ._anvil_designer import PageTemplate\nclass Page(PageTemplate):\n    def configure(self) -> None:\n        self.card.label.text = 'Ready'\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text(file.read_text().replace("'Ready'", "42"))
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )

    def test_dependency_custom_events_are_validated_from_cached_form_metadata(self):
        self.cache_widgets()
        self.write(
            ".anvil/deps/Widgets/client_code/Card/form_template.yaml",
            "container:\n  type: ColumnPanel\nevents:\n- name: changed\n  parameters: []\n",
        )
        self.write(
            ".anvil/deps/Widgets/client_code/Card/__init__.py",
            "from ._anvil_designer import CardTemplate\nclass Card(CardTemplate):\n    pass\n",
        )
        self.write(
            "client_code/Page/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n- name: card\n  type: form:dep-app:Card\n",
        )
        file = self.write(
            "client_code/Page/__init__.py",
            "import anvil\nfrom ._anvil_designer import PageTemplate\n"
            "class Page(PageTemplate):\n"
            "    @anvil.handle('card', 'changed')\n"
            "    @anvil.handle('card', 'x-undeclared')\n"
            "    def changed(self, **event_args):\n        pass\n",
        )
        self.compare(file, "reportAnvilInvalidEvent", "warning", 0)
        file.write_text(file.read_text().replace("'changed')", "'click')"))
        self.compare(
            file,
            "reportAnvilInvalidEvent",
            "warning",
            (0, 1),
            difference="Native validate checks cached custom-component event metadata; the baseline CLI misses this check.",
        )

    def test_bare_client_imports_report_runtime_restriction_with_exact_ranges(self):
        file = self.write(
            "client_code/Imports.py",
            "marker = '😀'; from Helpers import title\ndef later():\n    import Helpers\n",
        )
        self.compare(file, "reportAnvilImportRestriction", "error", 2)

    def test_relative_and_package_imports_work_in_client_and_server(self):
        for environment in ("client", "server"):
            file = self.write(
                f"{environment}_code/Imports.py",
                "from TyProof.Helpers import title\nfrom .Helpers import title as relative_title\nlabel: str = title()\nother: str = relative_title()\n"
                + (
                    "from Helpers import title as bare_title\nserver_label: str = bare_title()\n"
                    if environment == "server"
                    else ""
                ),
            )
            with self.subTest(environment=environment):
                self.compare(file, "reportAnvilImportRestriction", "error", 0)
                file.write_text(
                    file.read_text().replace(
                        "label: str = title()", "label: int = title()"
                    )
                )
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                )

    def test_checkout_directory_imports_are_rejected_in_both_environments(self):
        for environment in ("client", "server"):
            file = self.write(
                f"{environment}_code/Imports.py",
                "from client_code.Helpers import title\n",
            )
            with self.subTest(environment=environment):
                self.compare(file, "reportAnvilImportRestriction", "error", 1)

    def test_assignment_diagnostic_configuration_controls_severity_and_exit(self):
        config = self.write("pyrightconfig.json", '{"reportAssignmentType": "none"}')
        file = self.write("server_code/Configured.py", "count: int = 'wrong'\n")
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 0)
        config.write_text('{"reportAssignmentType": "warning"}')
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "warning", 1)

    def test_dependency_hints_reserve_cache_entries_before_legacy_fallback(self):
        legacy = {"app_id": "legacy-app", "version": {"branch": "master"}}
        hinted = {
            "app_id": "widget-app",
            "version": {"branch": "master"},
            "resolution_hints": {"package_name": "Widgets"},
        }
        declarations = [legacy, hinted]
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text() + "dependencies: " + json.dumps(declarations) + "\n"
        )
        for directory, package, kind, value in (
            ("A", "Widgets", "str", "'Ready'"),
            ("Z", "Legacy", "int", "42"),
        ):
            self.write(
                f".anvil/deps/{directory}/anvil.yaml", f"package_name: {package}\n"
            )
            self.write(
                f".anvil/deps/{directory}/client_code/Helpers.py",
                f"def value() -> {kind}:\n    return {value}\n",
            )
        # The CLI manifest confirms freshness; checker discovery uses anvil.yaml in each cache directory.
        manifest = {
            "version": 3,
            "includeDocs": False,
            "source_dependencies": declarations,
            "resolved_dependencies": [
                {"app_id": "legacy-app", "commit_id": "cached"},
                {"app_id": "widget-app", "commit_id": "cached"},
            ],
            "cached_dependencies": [
                {"app_id": "legacy-app", "commit_id": "cached", "package_name": "Z"},
                {"app_id": "widget-app", "commit_id": "cached", "package_name": "A"},
            ],
        }
        self.write(".anvil/deps/manifest.json", json.dumps(manifest))
        file = self.write(
            "client_code/UseDependencies.py",
            "from Widgets.Helpers import value as widget_value\nfrom Legacy.Helpers import value as legacy_value\nlabel: str = widget_value()\nnumber: int = legacy_value()\n",
        )
        for hint in ("Widgets", "A"):
            hinted["resolution_hints"]["package_name"] = hint
            config.write_text(
                config.read_text().split("dependencies:")[0]
                + "dependencies: "
                + json.dumps(declarations)
                + "\n"
            )
            manifest["source_dependencies"] = declarations
            self.write(".anvil/deps/manifest.json", json.dumps(manifest))
            with self.subTest(hint=hint):
                self.compare(file, "reportMissingImports", "error", 0)

    def test_type_ignore_suppresses_runtime_checks_without_unused_ignore_warning(self):
        file = self.write(
            "client_code/Ignored.py",
            "import subprocess  # type: ignore\nimport anvil.server\nanvil.server.call('missing')  # type: ignore\n",
        )
        self.compare(file, "reportAnvilUnsupportedSkulptImport", "error", 0)

    def test_pyright_ignore_is_rule_specific_for_generic_and_runtime_diagnostics(self):
        file = self.write(
            "client_code/Ignored.py",
            "import subprocess  # pyright: ignore[reportAnvilUnsupportedSkulptImport]\ncount: int = 'wrong'  # pyright: ignore[reportAssignmentType]\nimport anvil.server\nanvil.server.call('missing')  # pyright: ignore[reportAssignmentType]\n",
        )
        self.compare(file, "reportAnvilUnknownCallable", "warning", 1)

    def test_unused_type_ignore_uses_baseline_default_and_explicit_configuration(self):
        file = self.write("server_code/Ignored.py", "count: int = 42  # type: ignore\n")
        self.compare(
            file,
            ("reportUnnecessaryTypeIgnoreComment", "unused-type-ignore-comment"),
            "warning",
            0,
        )
        self.write(
            "pyrightconfig.json", '{"reportUnnecessaryTypeIgnoreComment": "warning"}'
        )
        self.compare(
            file,
            ("reportUnnecessaryTypeIgnoreComment", "unused-type-ignore-comment"),
            "warning",
            1,
        )

    def test_missing_import_diagnostic_configuration_and_inline_suppression(self):
        config = self.write("pyrightconfig.json", '{"reportMissingImports": false}')
        file = self.write("server_code/Imports.py", "import no_such_anvil_dependency\n")
        self.compare(file, ("reportMissingImports", "unresolved-import"), "error", 0)
        config.write_text('{"reportMissingImports": "warning"}')
        self.compare(file, ("reportMissingImports", "unresolved-import"), "warning", 1)
        file.write_text(
            file.read_text().rstrip() + "  # pyright: ignore[reportMissingImports]\n"
        )
        self.compare(file, ("reportMissingImports", "unresolved-import"), "warning", 0)

    def test_jsonc_configuration_inheritance_resolves_relative_paths_and_child_overrides(
        self,
    ):
        self.write(
            "config/root.json", '// Shared policy\n{"reportAssignmentType": "none",}\n'
        )
        self.write(
            "config/base.json",
            '{"extends": "root.json", "reportMissingImports": false}',
        )
        config = self.write("pyrightconfig.json", '{"extends": "config/base.json"}')
        file = self.write(
            "server_code/Configured.py",
            "import no_such_anvil_dependency\ncount: int = 'wrong'\n",
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 0)
        config.write_text(
            '{"extends": "config/base.json", "reportAssignmentType": "warning"}'
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "warning", 1)

    def test_directory_target_reports_its_files_and_ignores_other_environments(self):
        file = self.write("client_code/Selected/Broken.py", "count: int = 'wrong'\n")
        self.write("client_code/Elsewhere.py", "other: int = 'wrong'\n")
        self.write("server_code/Broken.py", "other: int = 'wrong'\n")
        self.compare(
            file.parent, ("reportAssignmentType", "invalid-assignment"), "error", 1
        )
        file.write_text("count: int = 42\n")
        self.compare(file.parent, "reportAssignmentType", "error", 0)

    def test_file_level_type_ignore_suppresses_later_runtime_checks(self):
        file = self.write(
            "client_code/Ignored.py",
            "# type: ignore\nimport subprocess\nimport anvil.server\nanvil.server.call('missing')\n",
        )
        self.compare(file, "reportAnvilUnsupportedSkulptImport", "error", 0)

    def test_type_ignore_can_be_disabled_without_disabling_pyright_ignore(self):
        self.write("pyrightconfig.json", '{"enableTypeIgnoreComments": false}')
        client = self.write(
            "client_code/Ignored.py", "import subprocess  # type: ignore\n"
        )
        self.compare(client, "reportAnvilUnsupportedSkulptImport", "error", 1)
        server = self.write(
            "server_code/Ignored.py", "count: int = 'wrong'  # type: ignore\n"
        )
        self.compare(server, ("reportAssignmentType", "invalid-assignment"), "error", 1)
        server.write_text(
            server.read_text().replace(
                "type: ignore", "pyright: ignore[reportAssignmentType]"
            )
        )
        self.compare(server, ("reportAssignmentType", "invalid-assignment"), "error", 0)

    def test_argument_and_return_diagnostic_settings_remain_independent(self):
        self.write(
            "pyrightconfig.json",
            '{"reportArgumentType": "none", "reportReturnType": "warning"}',
        )
        file = self.write(
            "server_code/Configured.py",
            "def number(text: str) -> int:\n    return text\nnumber(42)\n",
        )
        self.compare(file, ("reportReturnType", "invalid-return-type"), "warning", 1)

    def test_off_mode_preserves_runtime_import_checks_and_explicit_rule_overrides(self):
        config = self.write("pyrightconfig.json", '{"typeCheckingMode": "off"}')
        file = self.write("server_code/Configured.py", "count: int = 'wrong'\n")
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 0)
        calls = self.write(
            "client_code/Calls.py",
            "import anvil.server\nanvil.server.call('missing')\n",
        )
        self.compare(calls, "reportAnvilUnknownCallable", "warning", 0)
        imports = self.write("client_code/Imports.py", "import subprocess\n")
        self.compare(imports, "reportAnvilUnsupportedSkulptImport", "error", 1)
        config.write_text(
            '{"typeCheckingMode": "off", "reportAssignmentType": "error"}'
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_ignored_source_keeps_imported_types_but_emits_no_diagnostics(self):
        self.write("pyrightconfig.json", '{"ignore": ["server_code/Broken.py"]}')
        ignored = self.write(
            "server_code/Broken.py", "def title() -> str:\n    return 42\n"
        )
        self.compare(ignored, "reportReturnType", "error", 0)
        file = self.write(
            "server_code/UseIgnored.py",
            "from .Broken import title\nlabel: str = title()\n",
        )
        self.compare(file, "reportAssignmentType", "error", 0)
        file.write_text(file.read_text().replace("label: str", "label: int"))
        self.compare(
            file,
            ("reportAssignmentType", "invalid-assignment"),
            "error",
            (0, 1),
            difference="The baseline accepts an incompatible result from an unselected server module; native preserves the function's declared return type even when the defining file is ignored. The baseline also misses the assignment without ignore configured.",
        )
        self.write("pyrightconfig.json", "{}")
        self.compare(
            file,
            ("reportAssignmentType", "invalid-assignment"),
            "error",
            (0, 1),
            difference="Without ignore configured, the baseline still accepts the incompatible result from the unselected server module; native preserves the declared return type.",
        )

    def test_inherited_ignore_globs_cover_nested_sources_and_runtime_diagnostics(self):
        self.write("config/base.json", '{"ignore": ["../client_code/Legacy/**"]}')
        self.write("pyrightconfig.json", '{"extends": "config/base.json"}')
        for path in ("Old.py", "Nested/Old.py"):
            self.write(
                f"client_code/Legacy/{path}",
                "import subprocess\ncount: int = 'wrong'\n",
            )
        self.compare(self.app, "reportAnvilUnsupportedSkulptImport", "error", 0)
        self.write("client_code/Active.py", "import subprocess\n")
        self.compare(self.app, "reportAnvilUnsupportedSkulptImport", "error", 1)

    def test_excluded_sources_are_not_checked_for_file_or_whole_app_targets(self):
        self.write("pyrightconfig.json", '{"exclude": ["server_code/Broken.py"]}')
        file = self.write("server_code/Broken.py", "count: int = 'wrong'\n")
        for target in (file, self.app):
            with self.subTest(target=target):
                self.compare(target, "reportAssignmentType", "error", 0)

    def test_include_selects_whole_app_sources_but_explicit_file_targets_override_it(
        self,
    ):
        self.write("pyrightconfig.json", '{"include": ["client_code"]}')
        file = self.write("server_code/Broken.py", "count: int = 'wrong'\n")
        self.compare(self.app, "reportAssignmentType", "error", 0)
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_pyproject_tool_sections_configure_validation_and_json_takes_precedence(
        self,
    ):
        file = self.write("server_code/Configured.py", "value: int = 'wrong'\n")
        config = self.write("pyproject.toml", "")
        for section in ("anvil-pyright", "basedpyright", "pyright"):
            with self.subTest(section=section):
                config.write_text(
                    f'[tool.{section}]\nreportAssignmentType = "warning"\n'
                )
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "warning", 1
                )
        self.write("pyrightconfig.json", '{"reportAssignmentType": "none"}')
        self.compare(file, "reportAssignmentType", "error", 0)

    def test_ancestor_pyproject_is_found_through_unrelated_project_metadata(self):
        config = (self.app / "anvil.yaml").read_text()
        self.write(
            "pyproject.toml",
            '[tool.anvil-pyright]\nreportAssignmentType = "warning"\n'
            'ignore = ["App/server_code/Ignored.py"]\n',
        )
        self.app = self.app / "App"
        self.write("anvil.yaml", config)
        local = self.write("pyproject.toml", '[project]\nname = "unrelated"\n')
        file = self.write("server_code/Configured.py", "value: int = 'wrong'\n")
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "warning", 1)
        ignored = self.write("server_code/Ignored.py", "value: int = 'wrong'\n")
        self.compare(ignored, "reportAssignmentType", "error", 0)
        local.unlink()
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "warning", 1)

    def test_mixed_json_toml_inheritance_preserves_declaring_directory(self):
        self.write(
            "config/base.toml",
            '[tool.anvil-pyright]\nreportAssignmentType = "warning"\n'
            'reportReturnType = "none"\nignore = ["../server_code/Ignored.py"]\n',
        )
        self.write("pyrightconfig.json", '{"extends": "config/base.toml"}')
        file = self.write(
            "server_code/Configured.py",
            "def title() -> int:\n    return 'wrong'\nvalue: int = 'wrong'\n",
        )
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "warning", 1)
        ignored = self.write("server_code/Ignored.py", "value: int = 'wrong'\n")
        self.compare(ignored, "reportAssignmentType", "error", 0)
        (self.app / "pyrightconfig.json").unlink()
        self.write("config/base.json", '{"reportAssignmentType": "none"}')
        self.write(
            "pyproject.toml",
            '[tool.anvil-pyright]\nextends = "config/base.json"\n'
            'reportReturnType = "none"\n',
        )
        self.compare(file, "reportAssignmentType", "error", 0)

    def test_attribute_diagnostic_settings_and_rule_specific_ignore(self):
        source = "class Thing:\n    pass\nthing = Thing()\nthing.missing\n"
        file = self.write("server_code/Attributes.py", source)
        config = self.write(
            "pyrightconfig.json", '{"reportAttributeAccessIssue": "none"}'
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)
        config.write_text('{"reportAttributeAccessIssue": "warning"}')
        self.compare(
            file, ("reportAttributeAccessIssue", "unresolved-attribute"), "warning", 1
        )
        file.write_text(
            source.replace(
                "thing.missing",
                "thing.missing  # pyright: ignore[reportAttributeAccessIssue]",
            )
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)

    def test_call_binding_rules_share_configuration_and_specific_ignore(self):
        source = "def title(text: str) -> str:\n    return text\n"
        config = self.write("pyrightconfig.json", "{}")
        for call, rule in (
            ("title()", "missing-argument"),
            ("title('a', 'b')", "too-many-positional-arguments"),
            ("title(text='a', other=42)", "unknown-argument"),
        ):
            with self.subTest(call=call):
                file = self.write("server_code/Calls.py", source + call + "\n")
                config.write_text('{"reportCallIssue": "none"}')
                self.compare(file, "reportCallIssue", "error", 0)
                config.write_text('{"reportCallIssue": "warning"}')
                self.compare(file, ("reportCallIssue", rule), "warning", 1)
                file.write_text(
                    source + call + "  # pyright: ignore[reportCallIssue]\n"
                )
                self.compare(file, "reportCallIssue", "error", 0)

    def test_undefined_names_honor_configuration_and_specific_ignore(self):
        file = self.write("server_code/Names.py", "print(missing_name)\n")
        config = self.write("pyrightconfig.json", '{"reportUndefinedVariable": "none"}')
        self.compare(file, "reportUndefinedVariable", "error", 0)
        config.write_text('{"reportUndefinedVariable": "warning"}')
        self.compare(
            file, ("reportUndefinedVariable", "unresolved-reference"), "warning", 1
        )
        file.write_text(
            "print(missing_name)  # pyright: ignore[reportUndefinedVariable]\n"
        )
        self.compare(file, "reportUndefinedVariable", "error", 0)

    def test_stdlib_typing_wins_absolute_imports_but_relative_shim_remains_available(
        self,
    ):
        self.write(
            "client_code/typing.py",
            "class Callable:\n    pass\ndef marker() -> str:\n    return 'ready'\n",
        )
        file = self.write(
            "client_code/Typed.py",
            "from typing import Callable\nfrom . import typing as runtime_typing\n"
            "def apply(fn: Callable[[str], str]) -> str:\n"
            "    return fn(runtime_typing.marker())\n",
        )
        self.compare(file, "reportArgumentType", "error", 0)
        file.write_text(
            file.read_text().replace("fn(runtime_typing.marker())", "fn(123)")
        )
        self.compare(file, ("reportArgumentType", "invalid-argument-type"), "error", 1)

    def test_stdlib_modules_and_packages_preserve_relative_app_access(self):
        for name, statement in (
            ("math.py", "import math\nvalue: float = math.sqrt(4)\n"),
            (
                "collections/__init__.py",
                "from collections import deque\nqueue: deque[str] = deque(['ready'])\n",
            ),
        ):
            with self.subTest(module=name):
                self.write(
                    f"client_code/{name}", "def marker() -> str:\n    return 'ready'\n"
                )
                module = name.split("/")[0].removesuffix(".py")
                file = self.write(
                    "client_code/Standard.py",
                    statement
                    + f"from . import {module} as local\nlabel: str = local.marker()\n",
                )
                self.compare(file, "reportAnvilImportRestriction", "error", 0)
        self.write("client_code/annotationlib.py", "title: str = 'ready'\n")
        file = self.write("client_code/Future.py", "import annotationlib\n")
        # annotationlib is not stdlib for the proof's Python 3.10 target.
        self.compare(file, "reportAnvilImportRestriction", "error", 1)

    def test_attribute_assignment_configuration_is_independent_of_variable_assignments(
        self,
    ):
        attribute = self.write(
            "server_code/AttributeWrite.py",
            "class Thing:\n    value: str\nthing = Thing()\nthing.value = 123\n",
        )
        variable = self.write("server_code/VariableWrite.py", "value: str = 123\n")
        config = self.write(
            "pyrightconfig.json",
            '{"reportAssignmentType": "none", "reportAttributeAccessIssue": "warning"}',
        )
        self.compare(
            attribute,
            ("reportAttributeAccessIssue", "invalid-assignment"),
            "warning",
            1,
        )
        self.compare(variable, "reportAssignmentType", "error", 0)
        config.write_text(
            '{"reportAssignmentType": "warning", "reportAttributeAccessIssue": "none"}'
        )
        self.compare(attribute, "reportAttributeAccessIssue", "error", 0)
        self.compare(
            variable, ("reportAssignmentType", "invalid-assignment"), "warning", 1
        )
        config.write_text(
            '{"typeCheckingMode": "off", "reportAssignmentType": "error"}'
        )
        self.compare(attribute, "reportAttributeAccessIssue", "error", 0)
        self.compare(
            variable, ("reportAssignmentType", "invalid-assignment"), "error", 1
        )
        config.write_text(
            '{"typeCheckingMode": "off", "reportAttributeAccessIssue": "error"}'
        )
        self.compare(
            attribute, ("reportAttributeAccessIssue", "invalid-assignment"), "error", 1
        )
        self.compare(variable, "reportAssignmentType", "error", 0)
        attribute.write_text(
            attribute.read_text().replace(
                "thing.value = 123",
                "thing.value = 123  # pyright: ignore[reportAttributeAccessIssue]",
            )
        )
        self.compare(attribute, "reportAttributeAccessIssue", "error", 0)

    def test_anvil_property_assignment_uses_attribute_policy(self):
        file = self.write(
            "client_code/PropertyWrite.py",
            "import anvil\nlabel = anvil.Label()\nlabel.text = 123\n",
        )
        self.write(
            "pyrightconfig.json",
            '{"reportAssignmentType": "none", "reportAttributeAccessIssue": "warning"}',
        )
        self.compare(
            file, ("reportAttributeAccessIssue", "invalid-assignment"), "warning", 1
        )
        file.write_text(
            file.read_text().replace(
                "label.text = 123",
                "label.text = 123  # pyright: ignore[reportAttributeAccessIssue]",
            )
        )
        self.compare(file, "reportAttributeAccessIssue", "error", 0)

    def test_legacy_schema_arrays_use_baseline_generic_tables_without_blocking_python(
        self,
    ):
        config = self.app / "anvil.yaml"
        config.write_text(
            config.read_text() + "db_schema:\n- name: tasks\n  python_name: tasks\n"
            "  columns:\n    col1:\n      name: title\n      type: string\n"
        )
        file = self.write(
            "server_code/Legacy.py",
            "from anvil.tables import app_tables\n"
            "row = app_tables.tasks.add_row(title='ready')\nlabel: int = row['title']\n",
        )
        # Current anvil-pyright ignores array schemas; no generated column types.
        # The CLI's independent YAML validation still rejects this legacy format.
        self.compare(file, "reportAssignmentType", "error", 0)
        file.write_text(file.read_text() + "count: int = 'wrong'\n")
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_abstract_classes_and_plain_calls_keep_independent_policies(self):
        plain = self.write("server_code/PlainCall.py", "count = 42\ncount()\n")
        abstract = self.write(
            "server_code/Abstract.py",
            "from abc import ABC, abstractmethod\nclass Abstract(ABC):\n"
            "    @abstractmethod\n    def title(self) -> str: ...\nAbstract()\n",
        )
        config = self.write(
            "pyrightconfig.json",
            '{"reportCallIssue": "none", "reportAbstractUsage": "error"}',
        )
        self.compare(plain, "reportCallIssue", "error", 0)
        self.compare(abstract, ("reportAbstractUsage", "call-non-callable"), "error", 1)
        config.write_text(
            '{"reportCallIssue": "warning", "reportAbstractUsage": "none"}'
        )
        self.compare(plain, ("reportCallIssue", "call-non-callable"), "warning", 1)
        self.compare(abstract, "reportAbstractUsage", "error", 0)
        config.write_text('{"typeCheckingMode": "off", "reportAbstractUsage": "error"}')
        self.compare(plain, "reportCallIssue", "error", 0)
        self.compare(abstract, ("reportAbstractUsage", "call-non-callable"), "error", 1)

    def test_python_user_site_resolves_library_types_and_respects_disable_flag(self):
        userbase = self.app / "user-base"
        with patch.dict(os.environ, {"PYTHONUSERBASE": str(userbase)}):
            user_site = Path(
                subprocess.check_output(
                    ["python3", "-c", "import site; print(site.getusersitepackages())"],
                    text=True,
                ).strip()
            )
            self.write(
                str(user_site.relative_to(self.app) / "__anvil_ty_user_library.py"),
                "def title() -> str:\n    return 'Ready'\n",
            )
            file = self.write(
                "server_code/UserLibrary.py",
                "from __anvil_ty_user_library import title\nvalue: str = title()\n",
            )
            self.compare(file, "reportMissingImports", "error", 0)
            self.evidence[-1]["environment"] = {"PYTHONUSERBASE": "<app>/user-base"}
            file.write_text(
                "from __anvil_ty_user_library import title\nvalue: int = title()\n"
            )
            self.compare(
                file, ("reportAssignmentType", "invalid-assignment"), "error", 1
            )
            self.evidence[-1]["environment"] = {"PYTHONUSERBASE": "<app>/user-base"}
            file.write_text("from __anvil_ty_user_library import title\n")
            with patch.dict(os.environ, {"PYTHONNOUSERSITE": "1"}):
                self.compare(
                    file, ("reportMissingImports", "unresolved-import"), "error", 1
                )
                self.evidence[-1]["environment"] = {
                    "PYTHONUSERBASE": "<app>/user-base",
                    "PYTHONNOUSERSITE": "1",
                }
            self.write(
                "envs/isolated/pyvenv.cfg",
                "home = /unused\ninclude-system-site-packages = false\nversion = 3.10.0\n",
            )
            self.write("envs/isolated/lib/python3.10/site-packages/marker", "")
            self.write("pyrightconfig.json", '{"venvPath": "envs", "venv": "isolated"}')
            self.compare(
                file, ("reportMissingImports", "unresolved-import"), "error", 1
            )
            self.evidence[-1]["environment"] = {"PYTHONUSERBASE": "<app>/user-base"}

    def test_pythonpath_resolves_ambient_library_types(self):
        self.write(
            "ambient/acme/__init__.py", "def title() -> str:\n    return 'Ready'\n"
        )
        file = self.write(
            "server_code/Ambient.py", "from acme import title\nvalue: str = title()\n"
        )
        with patch.dict(os.environ, {"PYTHONPATH": str(self.app / "ambient")}):
            self.compare(file, "reportMissingImports", "error", 0)
            self.evidence[-1]["environment"] = {"PYTHONPATH": "<app>/ambient"}
            file.write_text("from acme import title\nvalue: int = title()\n")
            self.compare(
                file, ("reportAssignmentType", "invalid-assignment"), "error", 1
            )
            self.evidence[-1]["environment"] = {"PYTHONPATH": "<app>/ambient"}

    def test_inherited_extra_paths_resolve_library_types(self):
        self.write(
            "shared/acme/__init__.py", "def title() -> str:\n    return 'Ready'\n"
        )
        self.write("config/base.json", '{"extraPaths": ["../shared"]}')
        self.write("pyrightconfig.json", '{"extends": "config/base.json"}')
        file = self.write(
            "server_code/External.py", "from acme import title\nvalue: str = title()\n"
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text("from acme import title\nvalue: int = title()\n")
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_configured_python_environment_resolves_server_library_types(self):
        self.write(
            "envs/custom/pyvenv.cfg",
            "home = /unused\ninclude-system-site-packages = false\nversion = 3.10.0\n",
        )
        library = self.write(
            "envs/custom/lib/python3.10/site-packages/acme/__init__.py",
            "def title() -> str:\n    return 'Ready'\n",
        )
        self.write("envs/custom/lib/python3.10/site-packages/acme/py.typed", "")
        self.write("pyrightconfig.json", '{"venvPath": "envs", "venv": "custom"}')
        file = self.write(
            "server_code/Library.py", "from acme import title\nvalue: str = title()\n"
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text("from acme import title\nvalue: int = title()\n")
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)
        self.assertEqual(
            library.read_text(), "def title() -> str:\n    return 'Ready'\n"
        )

    def test_project_stubs_resolve_and_preserve_declared_types(self):
        for folder, config in (
            ("typings", {}),
            ("shared/stubs", {"stubPath": "shared/stubs"}),
        ):
            with self.subTest(folder=folder):
                self.write("pyrightconfig.json", json.dumps(config))
                self.write(f"{folder}/acme/__init__.pyi", "def title() -> str: ...\n")
                file = self.write(
                    "server_code/External.py",
                    "from acme import title\nvalue: str = title()\n",
                )
                self.compare(
                    file,
                    ("reportMissingModuleSource", "unresolved-import"),
                    "warning",
                    (1, 0),
                    difference="Pyright warns when a project stub has no runtime source. ty accepts the stub; runtime availability warnings are outside the migration contract.",
                )
                file.write_text(
                    "from acme import title  # pyright: ignore[reportMissingModuleSource]\nvalue: int = title()\n"
                )
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                )
                # An explicit stubPath must replace the default, not search both.
                if config:
                    self.write("typings/acme/__init__.pyi", "def title() -> int: ...\n")
                    self.compare(
                        file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                    )

    def test_pyright_optional_only_settings_do_not_suppress_native_type_errors(self):
        cases = (
            (
                "def show(value: str | None) -> None:\n    print(value.upper())\n",
                "reportOptionalMemberAccess",
                "unresolved-attribute",
            ),
            (
                "from typing import Callable\ndef show(value: Callable[[], str] | None) -> None:\n    print(value())\n",
                "reportOptionalCall",
                "call-non-callable",
            ),
            (
                "def show(value: list[str] | None) -> None:\n    print(value[0])\n",
                "reportOptionalSubscript",
                "not-subscriptable",
            ),
            (
                "def show(value: list[str] | None) -> None:\n    for item in value:\n        print(item)\n",
                "reportOptionalIterable",
                "not-iterable",
            ),
        )
        for source, optional_rule, native_rule in cases:
            with self.subTest(rule=optional_rule):
                file = self.write("server_code/Optional.py", source)
                self.write("pyrightconfig.json", json.dumps({optional_rule: "none"}))
                self.compare(
                    file,
                    (optional_rule, native_rule),
                    "error",
                    (0, 1),
                    difference="Pyright's optional-only rule settings are outside the migration contract. Native validation retains ty's type error; the ordinary mapped rule configures the whole ty diagnostic category.",
                )

    def test_parameter_default_errors_use_argument_policy_and_ignore(self):
        file = self.write(
            "server_code/Defaults.py",
            "def title(text: str = 123) -> str:\n    return text\n",
        )
        config = self.write("pyrightconfig.json", '{"reportArgumentType": "none"}')
        self.compare(file, "reportArgumentType", "error", 0)
        config.write_text('{"reportArgumentType": "warning"}')
        self.compare(
            file, ("reportArgumentType", "invalid-parameter-default"), "warning", 1
        )
        file.write_text(
            file.read_text().replace(
                "-> str:", "-> str:  # pyright: ignore[reportArgumentType]"
            )
        )
        self.compare(file, "reportArgumentType", "error", 0)

    def test_package_local_absolute_import_fallback_keeps_types_and_runtime_restrictions(
        self,
    ):
        for package, kind, value, wrong in (
            ("Text", "str", "'ready'", "int"),
            ("Number", "int", "42", "str"),
        ):
            self.write(f"client_code/{package}/__init__.py", "")
            self.write(
                f"client_code/{package}/Local.py",
                f"class Value:\n    text: {kind} = {value}\n",
            )
            file = self.write(
                f"client_code/{package}/Use.py",
                f"from Local import Value\nvalue = Value()\ntext: {kind} = value.text\n",
            )
            with self.subTest(package=package):
                self.compare(file, "reportAnvilImportRestriction", "error", 1)
                file.write_text(
                    file.read_text().replace(
                        "from Local import Value",
                        "from Local import Value  # pyright: ignore[reportAnvilImportRestriction]",
                    )
                )
                self.compare(file, "reportAnvilImportRestriction", "error", 0)
                file.write_text(
                    file.read_text().replace(f"text: {kind}", f"text: {wrong}")
                )
                self.compare(
                    file, ("reportAssignmentType", "invalid-assignment"), "error", 1
                )

    def test_bare_and_relative_imports_preserve_the_same_class_identity(self):
        self.write("client_code/Shared.py", "class Value:\n    pass\n")
        file = self.write(
            "client_code/Nominal.py",
            "from Shared import Value  # pyright: ignore[reportAnvilImportRestriction]\n"
            "from .Shared import Value as RelativeValue\nvalue: RelativeValue = Value()\n",
        )
        self.compare(file, "reportAssignmentType", "error", 0)

    def test_bare_imports_retain_private_and_non_star_exports(self):
        self.write(
            "client_code/Exports.py",
            "__all__ = []\nclass _Private:\n    pass\nclass Public:\n    pass\n"
            "_count: int = 42\n",
        )
        file = self.write(
            "client_code/Use.py",
            "from Exports import Public, _Private, _count  # pyright: ignore[reportAnvilImportRestriction]\n"
            "from .Exports import Public as Canonical, _Private as Private\n"
            "value: Canonical = Public()\nprivate: Private = _Private()\n"
            "count: int = _count\n",
        )
        self.compare(file, "reportMissingImports", "error", 0)
        file.write_text(file.read_text().replace("count: int", "count: str"))
        self.compare(file, ("reportAssignmentType", "invalid-assignment"), "error", 1)

    def test_bare_star_imports_respect_the_original_all_list(self):
        self.write(
            "client_code/Exports.py",
            "__all__ = ['Shown']\nclass Shown:\n    pass\nclass Hidden:\n    pass\n",
        )
        file = self.write(
            "client_code/Use.py",
            "from Exports import *  # pyright: ignore[reportAnvilImportRestriction]\n"
            "from .Exports import Shown as Canonical\nvalue: Canonical = Shown()\n",
        )
        self.compare(file, "reportAssignmentType", "error", 0)
        file.write_text(file.read_text() + "hidden = Hidden()\n")
        self.compare(
            file, ("reportUndefinedVariable", "unresolved-reference"), "error", 1
        )

    def test_operator_errors_remain_visible_with_default_policy(self):
        for expression, rule in (
            ("count + 1", "reportOptionalOperand"),
            ("count + 'a'", "reportOperatorIssue"),
            ("-count", "reportOptionalOperand"),
            ("count < 1", "reportOptionalOperand"),
        ):
            with self.subTest(expression=expression):
                file = self.write(
                    "server_code/Operators.py",
                    f"def show(count: int | None) -> None:\n    print({expression})\n",
                )
                self.compare(file, (rule, "unsupported-operator"), "error", 1)

    def test_method_override_settings_and_specific_ignore(self):
        source = (
            "class Base:\n    def title(self, text: str) -> str:\n        return text\n"
            "class Child(Base):\n    def title(self, text: str) -> int:\n        return 42\n"
        )
        file = self.write("server_code/Override.py", source)
        config = self.write(
            "pyrightconfig.json", '{"reportIncompatibleMethodOverride": "none"}'
        )
        self.compare(file, "reportIncompatibleMethodOverride", "error", 0)

        config.write_text('{"reportIncompatibleMethodOverride": "warning"}')
        self.compare(
            file,
            ("reportIncompatibleMethodOverride", "invalid-method-override"),
            "warning",
            1,
        )
        config.write_text(
            '{"typeCheckingMode": "off", "reportIncompatibleMethodOverride": "error"}'
        )
        self.compare(
            file,
            ("reportIncompatibleMethodOverride", "invalid-method-override"),
            "error",
            1,
        )
        file.write_text(
            source.replace(
                "-> int:",
                "-> int:  # pyright: ignore[reportIncompatibleMethodOverride]",
            )
        )
        self.compare(file, "reportIncompatibleMethodOverride", "error", 0)

    def test_optional_only_settings_leave_mixed_union_errors_visible(self):
        cases = (
            (
                "class Thing:\n    pass\ndef show(value: Thing | None) -> None:\n    print(value.missing)\n",
                "reportOptionalMemberAccess",
                "reportAttributeAccessIssue",
                "unresolved-attribute",
            ),
            (
                "from typing import Callable\ndef show(value: Callable[[], str] | int | None) -> None:\n    print(value())\n",
                "reportOptionalCall",
                "reportCallIssue",
                "call-non-callable",
            ),
            (
                "def show(value: list[str] | int | None) -> None:\n    print(value[0])\n",
                "reportOptionalSubscript",
                "reportIndexIssue",
                "not-subscriptable",
            ),
            (
                "def show(value: list[str] | int | None) -> None:\n    for item in value:\n        print(item)\n",
                "reportOptionalIterable",
                "reportGeneralTypeIssues",
                "not-iterable",
            ),
        )
        for source, optional_rule, ordinary_rule, native_rule in cases:
            with self.subTest(rule=optional_rule):
                file = self.write("server_code/Mixed.py", source)
                self.write("pyrightconfig.json", json.dumps({optional_rule: "none"}))
                counts = (
                    (1, 2)
                    if native_rule in {"call-non-callable", "not-subscriptable"}
                    else (1, 1)
                )
                self.compare(
                    file,
                    (ordinary_rule, native_rule),
                    "error",
                    counts,
                    difference="Optional-only Pyright settings are not applied to ty diagnostics. Native validation reports invalid receivers using ty's own grouping, retaining the unrelated union error.",
                )


if __name__ == "__main__":
    unittest.main()
