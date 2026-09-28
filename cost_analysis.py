from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping


TOKENS_PER_MILLION = 1_000_000


@dataclass(frozen=True)
class Pricing:
    standard_input: float = 5.00
    cache_write: float = 6.25
    cache_read: float = 0.50
    output: float = 30.00

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def _token_count(usage: Mapping[str, Any], field: str) -> int:
    value = usage.get(field, 0)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Usage field '{field}' must be numeric.")
    if value < 0 or int(value) != value:
        raise ValueError(f"Usage field '{field}' must be a non-negative integer.")
    return int(value)


def normalize_usage(usage: Mapping[str, Any]) -> dict[str, int]:
    if "input_token_count" not in usage or "output_token_count" not in usage:
        raise ValueError(
            "Usage must include input_token_count and output_token_count."
        )

    total_input = _token_count(usage, "input_token_count")
    output = _token_count(usage, "output_token_count")
    cache_write = _token_count(
        usage,
        "cache_creation_input_token_count",
    )
    cache_read = _token_count(usage, "cache_read_input_token_count")
    standard_input = total_input - cache_write - cache_read

    if standard_input < 0:
        raise ValueError(
            "Cache write and read tokens cannot exceed total input tokens."
        )

    return {
        "input": total_input,
        "standard_input": standard_input,
        "cache_write": cache_write,
        "cache_read": cache_read,
        "output": output,
    }


def calculate_request_cost(
    usage: Mapping[str, Any],
    pricing: Pricing = Pricing(),
) -> dict[str, Any]:
    tokens = normalize_usage(usage)
    cached_cost = (
        tokens["standard_input"] * pricing.standard_input
        + tokens["cache_write"] * pricing.cache_write
        + tokens["cache_read"] * pricing.cache_read
        + tokens["output"] * pricing.output
    ) / TOKENS_PER_MILLION
    baseline_cost = (
        tokens["input"] * pricing.standard_input
        + tokens["output"] * pricing.output
    ) / TOKENS_PER_MILLION
    savings = baseline_cost - cached_cost
    savings_percent = (
        savings / baseline_cost * 100 if baseline_cost else 0.0
    )
    cache_read_rate = (
        tokens["cache_read"] / tokens["input"] * 100
        if tokens["input"]
        else 0.0
    )

    return {
        "tokens": tokens,
        "costs": {
            "with_cache": cached_cost,
            "without_cache": baseline_cost,
            "savings": savings,
            "savings_percent": savings_percent,
        },
        "cache_read_rate_percent": cache_read_rate,
    }


def aggregate_results(items: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    successful = [item for item in items if item.get("status") == "completed"]
    token_fields = (
        "input",
        "standard_input",
        "cache_write",
        "cache_read",
        "output",
    )
    totals: dict[str, Any] = {
        "requests": len(successful),
        "tokens": {field: 0 for field in token_fields},
        "costs": {
            "with_cache": 0.0,
            "without_cache": 0.0,
            "savings": 0.0,
            "savings_percent": 0.0,
        },
        "cache_read_rate_percent": 0.0,
    }

    for item in successful:
        analysis = item["analysis"]
        for field in token_fields:
            totals["tokens"][field] += analysis["tokens"][field]
        for field in ("with_cache", "without_cache", "savings"):
            totals["costs"][field] += analysis["costs"][field]

    baseline = totals["costs"]["without_cache"]
    totals["costs"]["savings_percent"] = (
        totals["costs"]["savings"] / baseline * 100 if baseline else 0.0
    )
    total_input = totals["tokens"]["input"]
    totals["cache_read_rate_percent"] = (
        totals["tokens"]["cache_read"] / total_input * 100
        if total_input
        else 0.0
    )
    return totals


def group_results(
    items: Iterable[Mapping[str, Any]],
    field: str,
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[Mapping[str, Any]]] = {}
    for item in items:
        groups.setdefault(str(item.get(field, "unknown")), []).append(item)
    return {
        name: aggregate_results(group_items)
        for name, group_items in sorted(groups.items())
    }