from __future__ import annotations

import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from agent import CACHE_OPTIONS, MODEL_DEPLOYMENT, run_question
from agent_framework.foundry import FoundryChatOptions
from cost_analysis import (
    Pricing,
    aggregate_results,
    calculate_request_cost,
    group_results,
)


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_INPUT = BASE_DIR / "northwind_traders_model_router_eval_50.jsonl"
DEFAULT_OUTPUT = BASE_DIR / "prompt_cache_results.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_prompts(path: Path) -> list[dict[str, str]]:
    prompts: list[dict[str, str]] = []
    with path.open(encoding="utf-8") as source:
        for line_number, line in enumerate(source, start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            missing = {
                field
                for field in ("id", "prompt", "category", "difficulty")
                if not record.get(field)
            }
            if missing:
                fields = ", ".join(sorted(missing))
                raise ValueError(f"Line {line_number} is missing: {fields}.")
            prompts.append(record)
    return prompts


def new_results_document(source: Path, pricing: Pricing) -> dict[str, Any]:
    base_cache_key = CACHE_OPTIONS.get("prompt_cache_key", "prompt-cache")
    return {
        "schema_version": 1,
        "run": {
            "model": MODEL_DEPLOYMENT,
            "source": source.name,
            "cache_key": f"{base_cache_key}-{uuid4().hex[:12]}",
            "started_at": utc_now(),
            "updated_at": utc_now(),
            "status": "partial",
            "completed": 0,
            "failed": 0,
        },
        "pricing_usd_per_million_tokens": pricing.to_dict(),
        "items": [],
        "summary": aggregate_results([]),
        "groups": {"category": {}, "difficulty": {}},
    }


def load_results(
    path: Path,
    source: Path,
    pricing: Pricing,
    reset: bool,
) -> dict[str, Any]:
    if reset or not path.exists():
        return new_results_document(source, pricing)

    document = json.loads(path.read_text(encoding="utf-8"))
    if document.get("schema_version") != 1:
        raise ValueError("Unsupported results schema version.")
    if document.get("run", {}).get("source") != source.name:
        raise ValueError("Existing results were created from a different source file.")
    if document.get("pricing_usd_per_million_tokens") != pricing.to_dict():
        raise ValueError("Existing results use different pricing; pass --reset to restart.")
    return document


def refresh_summary(
    document: dict[str, Any],
    expected_prompts: int,
) -> None:
    items = document["items"]
    completed = sum(item.get("status") == "completed" for item in items)
    failed = sum(item.get("status") == "failed" for item in items)
    document["summary"] = aggregate_results(items)
    document["groups"] = {
        "category": group_results(items, "category"),
        "difficulty": group_results(items, "difficulty"),
    }
    document["run"].update(
        {
            "updated_at": utc_now(),
            "status": "completed" if completed == expected_prompts else "partial",
            "completed": completed,
            "failed": failed,
        }
    )


def save_results(
    document: dict[str, Any],
    path: Path,
    expected_prompts: int,
) -> None:
    refresh_summary(document, expected_prompts)
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    temporary_path.write_text(
        json.dumps(document, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(path)


def replace_item(items: list[dict[str, Any]], item: dict[str, Any]) -> None:
    for index, existing in enumerate(items):
        if existing.get("id") == item["id"]:
            items[index] = item
            return
    items.append(item)


async def evaluate(args: argparse.Namespace) -> None:
    pricing = Pricing()
    prompts = read_prompts(args.input)
    selected_prompts = prompts[: args.limit] if args.limit else prompts
    document = load_results(args.output, args.input, pricing, args.reset)
    completed_ids = {
        item["id"]
        for item in document["items"]
        if item.get("status") == "completed"
    }
    run_options: FoundryChatOptions = {
        **CACHE_OPTIONS,
        "prompt_cache_key": document["run"]["cache_key"],
    }

    for position, prompt in enumerate(selected_prompts, start=1):
        if prompt["id"] in completed_ids:
            print(f"[{position}/{len(selected_prompts)}] {prompt['id']}: already completed")
            continue

        print(f"[{position}/{len(selected_prompts)}] {prompt['id']}: running")
        item: dict[str, Any] = {
            "id": prompt["id"],
            "prompt": prompt["prompt"],
            "category": prompt["category"],
            "difficulty": prompt["difficulty"],
            "measured_at": utc_now(),
        }
        try:
            _, usage = await run_question(prompt["prompt"], run_options)
            item.update(
                {
                    "status": "completed",
                    "usage": usage,
                    "analysis": calculate_request_cost(usage, pricing),
                }
            )
            print(
                f"  cache read: {item['analysis']['tokens']['cache_read']:,} tokens; "
                f"savings: ${item['analysis']['costs']['savings']:.6f}"
            )
        except Exception as error:
            item.update({"status": "failed", "error": str(error)})
            print(f"  failed: {error}")

        replace_item(document["items"], item)
        save_results(document, args.output, len(prompts))

        if args.dashboard:
            from build_dashboard import build_dashboard

            build_dashboard(args.output, args.dashboard)

        if position < len(selected_prompts) and args.delay:
            await asyncio.sleep(args.delay)

    save_results(document, args.output, len(prompts))
    print(f"Results: {args.output}")
    if args.dashboard:
        print(f"Dashboard: {args.dashboard}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure prompt-cache usage and generate cost results."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--dashboard",
        type=Path,
        default=BASE_DIR / "prompt_cache_dashboard.html",
    )
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=2.0)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Discard existing results and start a new run.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    asyncio.run(evaluate(parse_args()))