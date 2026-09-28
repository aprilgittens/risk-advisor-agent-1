import json
import tempfile
import unittest
from pathlib import Path

from build_dashboard import (
    DEFAULT_TEMPLATE,
    build_dashboard,
    serialize_for_script,
    validate_results,
)


class DashboardBuilderTests(unittest.TestCase):
    def test_rejects_missing_schema_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "pricing"):
            validate_results(
                {"schema_version": 1, "run": {}, "items": [], "summary": {}}
            )

    def test_escapes_script_closing_markup(self) -> None:
        serialized = serialize_for_script({"prompt": "</script><strong>unsafe</strong>"})

        self.assertNotIn("<", serialized)
        self.assertIn("\\u003c/script\\u003e", serialized)

    def test_builds_single_file_with_embedded_data(self) -> None:
        document = {
            "schema_version": 1,
            "run": {"model": "test-model"},
            "pricing_usd_per_million_tokens": {},
            "items": [],
            "summary": {},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results = root / "results.json"
            template = root / "template.html"
            output = root / "dashboard.html"
            results.write_text(json.dumps(document), encoding="utf-8")
            template.write_text(
                "<script>const DATA=__PROMPT_CACHE_DATA__;</script>",
                encoding="utf-8",
            )

            build_dashboard(results, output, template)

            rendered = output.read_text(encoding="utf-8")
            self.assertIn('"model":"test-model"', rendered)
            self.assertNotIn("__PROMPT_CACHE_DATA__", rendered)

    def test_template_uses_requested_request_columns(self) -> None:
        template = DEFAULT_TEMPLATE.read_text(encoding="utf-8")

        self.assertIn('data-sort="input">Total input', template)
        self.assertIn('data-sort="standard_input">Standard input', template)
        self.assertNotIn('data-sort="category">Category', template)
        self.assertNotIn("Savings by category", template)
        self.assertNotIn("Savings by difficulty", template)


if __name__ == "__main__":
    unittest.main()