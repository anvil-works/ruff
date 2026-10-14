"""Keep validation useful when an individual form cannot be prepared."""

from __future__ import annotations

import unittest

from test_validate import NATIVE, ValidateIntegration


@unittest.skipUnless(NATIVE, "native preparation boundary")
class FormPreparationFailures(ValidateIntegration):
    def test_invalid_form_does_not_stop_other_python_checks(self):
        template = self.write(
            "client_code/Broken/form_template.html",
            '---\n---\n<anvil-component type="MissingPackage.Nope" '
            'name="missing_component"></anvil-component>\n',
        )
        broken = self.write(
            "client_code/Broken/__init__.py",
            "from ._anvil_designer import BrokenTemplate\n"
            "class Broken(BrokenTemplate):\n"
            "    def configure(self):\n"
            "        self.init_components()\n"
            "        count: int = 'wrong'\n",
        )
        self.write(
            "client_code/Good/form_template.yaml",
            "container:\n  type: ColumnPanel\ncomponents:\n"
            "- name: label_1\n  type: Label\n",
        )
        good = self.write(
            "client_code/Good/__init__.py",
            "from ._anvil_designer import GoodTemplate\n"
            "class Good(GoodTemplate):\n"
            "    def configure(self):\n        self.label_1.text = 42\n",
        )
        server = self.write("server_code/Other.py", "count: int = 'wrong'\n")

        result, events = self.validate()
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        files = events[-1]["data"]["files"]
        issues = [issue for file in files for issue in file.get("issues", [])]
        preparation = [
            issue for issue in issues if issue.get("rule") == "invalid-form-template"
        ]
        self.assertEqual(len(preparation), 1, events)
        # The CLI attaches checker diagnostics to Python files, so identify the
        # template in the message and attach the failure to its owning form.
        self.assertEqual(preparation[0]["file"], str(broken))
        self.assertIn(str(template), preparation[0]["message"])
        self.assertIn("MissingPackage.Nope", preparation[0]["message"])
        self.assertEqual(
            {
                issue["file"]
                for issue in issues
                if issue.get("rule") == "invalid-assignment"
            },
            {str(broken), str(good), str(server)},
            events,
        )
        self.assertFalse(
            any(issue.get("rule") == "unresolved-import" for issue in issues), events
        )

        # File targeting remains local even though all designer modules are
        # prepared. Selecting the bad form still reports its preparation failure.
        good.write_text(good.read_text().replace("text = 42", "text = 'Ready'"))
        result, events = self.validate(good)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        result, events = self.validate(broken)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        self.assertEqual(
            {issue["rule"] for issue in events[-1]["data"]["issues"]},
            {"invalid-form-template", "invalid-assignment"},
            events,
        )


if __name__ == "__main__":
    unittest.main()
