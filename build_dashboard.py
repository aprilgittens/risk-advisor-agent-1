from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_RESULTS = BASE_DIR / "prompt_cache_results.json"
DEFAULT_TEMPLATE = BASE_DIR / "prompt_cache_dashboard.template.html"
DEFAULT_OUTPUT = BASE_DIR / "prompt_cache_dashboard.html"
DATA_PLACEHOLDER = "__PROMPT_CACHE_DATA__"


def validate_results(document: Mapping[str, Any]) -> None:
    if document.get("schema_version") != 1:
        raise ValueError("Dashboard requires results schema version 1.")
    for field in ("run", "pricing_usd_per_million_tokens", "items", "summary"):
        if field not in document:
            raise ValueError(f"Results are missing required field '{field}'.")
    if not isinstance(document["items"], list):
        raise ValueError("Results field 'items' must be a list.")


def serialize_for_script(document: Mapping[str, Any]) -> str:
    return (
        json.dumps(document, separators=(",", ":"), ensure_ascii=True)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def build_dashboard(
    results_path: Path = DEFAULT_RESULTS,
    output_path: Path = DEFAULT_OUTPUT,
    template_path: Path = DEFAULT_TEMPLATE,
) -> Path:
    document = json.loads(results_path.read_text(encoding="utf-8"))
    validate_results(document)
    template = template_path.read_text(encoding="utf-8")
    if template.count(DATA_PLACEHOLDER) != 1:
        raise ValueError("Dashboard template must contain one data placeholder.")
    output_path.write_text(
        template.replace(DATA_PLACEHOLDER, serialize_for_script(document)),
        encoding="utf-8",
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a self-contained prompt-cache savings dashboard."
    )
    parser.add_argument("results", type=Path, nargs="?", default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    built_path = build_dashboard(
        arguments.results,
        arguments.output,
        arguments.template,
    )
    print(f"Dashboard: {built_path}")