import unittest

from cost_analysis import (
    Pricing,
    aggregate_results,
    calculate_request_cost,
    normalize_usage,
)


class CostAnalysisTests(unittest.TestCase):
    def test_calculates_observed_cached_read_payload(self) -> None:
        usage = {
            "input_token_count": 11_414,
            "output_token_count": 317,
            "cache_creation_input_token_count": 0,
            "cache_read_input_token_count": 4_002,
        }

        result = calculate_request_cost(usage)

        self.assertEqual(result["tokens"]["standard_input"], 7_412)
        self.assertAlmostEqual(result["costs"]["with_cache"], 0.048571)
        self.assertAlmostEqual(result["costs"]["without_cache"], 0.06658)
        self.assertAlmostEqual(result["costs"]["savings"], 0.018009)

    def test_cache_write_can_cost_more_than_baseline(self) -> None:
        result = calculate_request_cost(
            {
                "input_token_count": 5_000,
                "output_token_count": 100,
                "cache_creation_input_token_count": 4_000,
                "cache_read_input_token_count": 0,
            }
        )

        self.assertLess(result["costs"]["savings"], 0)

    def test_rejects_cache_buckets_larger_than_input(self) -> None:
        with self.assertRaisesRegex(ValueError, "cannot exceed"):
            normalize_usage(
                {
                    "input_token_count": 100,
                    "output_token_count": 10,
                    "cache_creation_input_token_count": 80,
                    "cache_read_input_token_count": 30,
                }
            )

    def test_aggregate_excludes_failed_items(self) -> None:
        completed = {
            "status": "completed",
            "analysis": calculate_request_cost(
                {
                    "input_token_count": 1_000,
                    "output_token_count": 100,
                    "cache_read_input_token_count": 800,
                },
                Pricing(),
            ),
        }
        failed = {"status": "failed", "error": "provider error"}

        totals = aggregate_results([completed, failed])

        self.assertEqual(totals["requests"], 1)
        self.assertEqual(totals["tokens"]["cache_read"], 800)
        self.assertAlmostEqual(totals["cache_read_rate_percent"], 80.0)

    def test_aggregate_handles_all_failed_items(self) -> None:
        totals = aggregate_results(
            [
                {"status": "failed", "error": "first"},
                {"status": "failed", "error": "second"},
            ]
        )

        self.assertEqual(totals["requests"], 0)
        self.assertEqual(totals["tokens"]["input"], 0)
        self.assertEqual(totals["costs"]["savings"], 0.0)


if __name__ == "__main__":
    unittest.main()