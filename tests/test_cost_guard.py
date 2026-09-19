import os
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
try:
    import openai  # noqa: F401
except ModuleNotFoundError:
    openai_stub = ModuleType("openai")
    openai_stub.OpenAI = object
    sys.modules["openai"] = openai_stub
import gpt_integration as gpt


class FakeCompletions:
    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))]
        )


class FakeClient:
    def __init__(self):
        self.chat = SimpleNamespace(completions=FakeCompletions())


class CostGuardTest(unittest.TestCase):
    def setUp(self):
        gpt._call_count = 0

    def test_refuses_more_model_calls_than_budget(self):
        with patch.dict(os.environ, {"AI_MAX_CALLS": "2"}, clear=False), patch.object(
            gpt, "_get_client", return_value=FakeClient()
        ):
            self.assertEqual(gpt.generate_product_description("1"), "ok")
            self.assertEqual(gpt.generate_product_description("2"), "ok")
            with self.assertRaisesRegex(RuntimeError, "AI call budget exhausted"):
                gpt.generate_product_description("3")

    def test_rejects_dataframe_larger_than_budget_before_any_call(self):
        class OversizedFrame:
            columns = ["sku"]

            def __len__(self):
                return 101

            def apply(self, *args, **kwargs):
                raise AssertionError("must not process rows")

        df = OversizedFrame()
        with patch.dict(os.environ, {"AI_MAX_CALLS": "100"}, clear=False), patch.object(
            gpt, "generate_product_description", side_effect=AssertionError("must not call")
        ):
            with self.assertRaisesRegex(RuntimeError, "101 rows.*100-call budget"):
                gpt.enrich_dataframe(df)

    def test_rejects_budget_above_hard_ceiling(self):
        with patch.dict(os.environ, {"AI_MAX_CALLS": "501"}, clear=False), patch.object(
            gpt, "_get_client", return_value=FakeClient()
        ):
            with self.assertRaisesRegex(ValueError, "between 1 and 500"):
                gpt.generate_product_description("1")

    def test_workflow_exposes_bounded_manual_budget_and_timeout(self):
        workflow = (ROOT / ".github/workflows/pipeline.yml").read_text(encoding="utf-8")
        for needle in (
            "max_ai_calls:",
            "default: '100'",
            "AI_MAX_CALLS: ${{ inputs.max_ai_calls }}",
            "timeout-minutes: 20",
            "cancel-in-progress: true",
        ):
            self.assertIn(needle, workflow)


if __name__ == "__main__":
    unittest.main()
