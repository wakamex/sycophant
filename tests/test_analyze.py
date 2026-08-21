import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "analyze.py"
SPEC = importlib.util.spec_from_file_location("analyze", MODULE_PATH)
ANALYZE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYZE)


class PublishedResultsTest(unittest.TestCase):
    def test_three_axis_headlines(self):
        result = ANALYZE.analyze_three_axis()

        self.assertEqual(result["complete_comparisons"], 110)
        self.assertEqual(result["mean_absolute_span"], 6.18)
        self.assertEqual(result["absolute_span_ge_10"], 29)
        self.assertEqual(result["absolute_span_ge_20"], 13)
        self.assertEqual(result["user_aligned_flips"], 6)
        self.assertEqual(result["anti_aligned_flips"], 0)
        self.assertEqual(result["strong_60_40_flips"], 5)

    def test_lmca_headlines(self):
        result = ANALYZE.analyze_lmca()

        self.assertEqual(result["scores"], 45)
        self.assertEqual(result["routes"]["gpt"]["mean_span"], 35.0)
        self.assertEqual(result["routes"]["deepseek"]["mean_span"], 33.6)
        self.assertEqual(result["routes"]["gemini-pro"]["mean_span"], 11.0)
        self.assertEqual(result["qualifying_routes"], ["deepseek", "gpt"])
        self.assertTrue(result["outreach_rule_met"])


if __name__ == "__main__":
    unittest.main()
