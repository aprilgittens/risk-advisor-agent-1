# Prompt Cache Savings Dashboard

This workspace measures prompt-cache usage for the 50 Northwind Traders
evaluation prompts and produces a self-contained cost dashboard.

## Prerequisites

1. Activate the existing virtual environment.
2. Sign in with the Azure CLI account that can access the Foundry project.
3. Configure these values in `.env`:

```text
FOUNDRY_PROJECT_ENDPOINT=...
FOUNDRY_MODEL=gpt-5.6-sol-1
VECTOR_STORE_ID=...
```

## Pricing assumptions

Rates are in USD per one million tokens:

| Token type | Rate |
| --- | ---: |
| Standard input | $5.00 |
| Cache write | $6.25 |
| Cache read | $0.50 |
| Output | $30.00 |

The no-cache baseline is derived from the same measured response. All input
tokens are repriced at the standard input rate while output usage remains
unchanged. This isolates the billing effect of caching without making a
second, variable model request.

## Run the evaluation

Run a three-prompt smoke test into separate artifacts:

```powershell
python evaluate_prompt_cache.py --limit 3 --reset `
  --output prompt_cache_results.smoke.json `
  --dashboard prompt_cache_dashboard.smoke.html
```

Run all 50 prompts:

```powershell
python evaluate_prompt_cache.py --reset
```

The configured cache lifetime is 30 minutes. A run or resumed run that crosses
that window can record additional cache writes. Those misses are retained as
measured behavior and can temporarily reduce net savings.

Results are saved after every request. If a run is interrupted, repeat the
command without `--reset`; completed prompt IDs are skipped and failed items
are retried. Each new run gets a unique cache key so it can measure the initial
cache-write premium. A resumed run keeps that same key.

The generated files are:

- `prompt_cache_results.json`: measured usage, per-request costs, and groups.
- `prompt_cache_dashboard.html`: portable dashboard with all data embedded.

Model response bodies are intentionally omitted from the results.

## Rebuild the dashboard

Regenerate the HTML from saved results without calling the model:

```powershell
python build_dashboard.py prompt_cache_results.json
```

Open `prompt_cache_dashboard.html` directly in a browser. It has no server,
CDN, or frontend build dependency.

## Tests

```powershell
python -m unittest discover -s tests -v
```