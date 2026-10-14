"""Schema string-key compatibility through the real validate command."""

from __future__ import annotations

import json
import unittest

import test_validate as harness


@unittest.skipUnless(harness.NATIVE, "native schema names")
class ColumnNames(unittest.TestCase):
    write = harness.ValidateIntegration.write
    validate = harness.ValidateIntegration.validate

    def setUp(self):
        harness.ValidateIntegration.setUp(self)
        config = self.app / "anvil.yaml"
        schema = {
            "people": {
                "columns": [
                    {"name": name, "type": "string"}
                    for name in ("full name", "class", 'quote"name', "café", "name")
                ]
            }
        }
        config.write_text(
            config.read_text() + "db_schema: " + json.dumps(schema) + "\n"
        )

    def test_string_keys_keep_types_across_reads_writes_queries_and_buffered_changes(
        self,
    ):
        file = self.write(
            "server_code/People.py",
            "from anvil.tables import app_tables\n"
            "row = app_tables.people.add_row(**{'full name': 'Ada', 'class': 'VIP'})\n"
            "row.update(**{'full name': 'Grace'})\n"
            "row['café'] = 'Paris'\n"
            "name: str = row['full name']\n"
            "quoted: str = row['quote\"name']\n"
            "normal: str = row.name\n"
            "changes = row.buffered_changes\n"
            "if changes is not None:\n    buffered: str = changes['full name']\n"
            "for person in app_tables.people.search(**{'full name': 'Ada'}):\n"
            "    title: str = person['class']\n"
            "found = app_tables.people.get(**{'full name': 'Ada'})\n"
            "if found is not None:\n    title: str = found['full name']\n",
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 0, (result.stdout, result.stderr))
        self.assertFalse(events[-1]["data"].get("issues"), events)
        file.write_text(
            file.read_text().replace(
                "name: str = row['full name']", "name: int = row['full name']"
            )
        )
        result, events = self.validate(file)
        self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
        issues = events[-1]["data"].get("issues", [])
        self.assertEqual(len(issues), 1, events)
        self.assertEqual(issues[0]["rule"], "invalid-assignment")

    def test_string_key_writes_reject_wrong_types_in_client_and_server(self):
        for environment in ("client", "server"):
            with self.subTest(environment=environment):
                file = self.write(
                    f"{environment}_code/People.py",
                    "from anvil.tables import app_tables\n"
                    "app_tables.people.add_row(**{'full name': 123})\n"
                    "row = app_tables.people.add_row()\n"
                    "row.update(**{'class': 123})\n",
                )
                result, events = self.validate(file)
                self.assertEqual(result.returncode, 1, (result.stdout, result.stderr))
                issues = events[-1]["data"].get("issues", [])
                self.assertEqual(len(issues), 2, events)
                self.assertTrue(
                    all(issue["rule"] == "invalid-argument-type" for issue in issues),
                    events,
                )
