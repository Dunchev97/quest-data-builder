import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.workflow_context import approve_stage, detect_mode, file_sha256, load_modes, main, stage_is_approved


class WorkflowContextTests(unittest.TestCase):
    def test_detects_quest_generation_from_russian_keywords(self) -> None:
        detection = detect_mode(
            "Продолжаем campaign MeatballRain_2026, создай pack 2: с неба начали падать соленые огурцы, 3 квеста."
        )

        self.assertEqual(detection["mode"], "quest_generation")
        self.assertTrue(detection["matched_keywords"])

    def test_detects_quest_edit_from_russian_keywords(self) -> None:
        detection = detect_mode("В квесте 2, таск 1 замени мусор Аммонит на другой.")

        self.assertEqual(detection["mode"], "quest_edit")

    def test_detects_pot_description_from_russian_keywords(self) -> None:
        detection = detect_mode("Вот картинка горшка, опиши горшок в нашем стиле.")

        self.assertEqual(detection["mode"], "pot_description")

    def test_cli_sets_active_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            context_path = Path(tmp) / "active_context.json"
            exit_code = main(
                [
                    "--context",
                    str(context_path),
                    "set",
                    "--mode",
                    "quest_edit",
                    "--campaign",
                    "MeatballRain_2026",
                    "--pack",
                    "pack_001",
                    "--stage",
                    "4",
                    "--quest",
                    "2",
                    "--task",
                    "1",
                ]
            )

            self.assertEqual(exit_code, 0)
            context = json.loads(context_path.read_text(encoding="utf-8"))
            self.assertEqual(context["mode"], "quest_edit")
            self.assertEqual(context["campaign_id"], "MeatballRain_2026")
            self.assertEqual(context["pack_id"], "pack_001")
            self.assertEqual(context["quest_number"], 2)
            self.assertEqual(context["task_number"], 1)

    def test_cli_detects_and_applies_context(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            context_path = Path(tmp) / "active_context.json"
            exit_code = main(
                [
                    "--context",
                    str(context_path),
                    "detect",
                    "--text",
                    "создай csv для текущего пака",
                    "--apply",
                    "--campaign",
                    "MeatballRain_2026",
                    "--pack",
                    "pack_001",
                ]
            )

            self.assertEqual(exit_code, 0)
            context = json.loads(context_path.read_text(encoding="utf-8"))
            self.assertEqual(context["mode"], "csv_export")
            self.assertEqual(context["campaign_id"], "MeatballRain_2026")
            self.assertEqual(context["pack_id"], "pack_001")
            self.assertIn("создай csv", context["matched_keywords"])

    def test_direct_cli_approval_is_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            context_path = Path(tmp) / "active_context.json"
            main(
                [
                    "--context",
                    str(context_path),
                    "set",
                    "--mode",
                    "quest_generation",
                    "--campaign",
                    "MeatballRain_2026",
                    "--pack",
                    "pack_002",
                    "--stage",
                    "3",
                ]
            )

            exit_code = main(["--context", str(context_path), "approve", "--stage", "3"])

            self.assertEqual(exit_code, 1)
            context = json.loads(context_path.read_text(encoding="utf-8"))
            self.assertFalse(stage_is_approved(context, "3", "MeatballRain_2026", "pack_002"))
            self.assertFalse(stage_is_approved(context, "3", "MeatballRain_2026", "pack_003"))

    def test_review_checksum_invalidates_approval_after_edit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review_path = Path(tmp) / "stage3_review.md"
            review_path.write_text("approved", encoding="utf-8")
            context = approve_stage(
                {"stage_approvals": {}},
                "3",
                campaign_id="MeatballRain_2026",
                pack_id="pack_002",
                review_path=review_path,
                review_sha256=file_sha256(review_path),
            )

            self.assertTrue(stage_is_approved(context, "3", "MeatballRain_2026", "pack_002"))
            review_path.write_text("changed", encoding="utf-8")
            self.assertFalse(stage_is_approved(context, "3", "MeatballRain_2026", "pack_002"))


if __name__ == "__main__":
    unittest.main()
