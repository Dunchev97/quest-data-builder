import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src import workflow_fast


STAGE3_ONE_DIALOG = """
Classname quests: Event_2026_Story_1
title_quest: Test Quest
# quest: 1
# task: 1
Task template ID: TT-001
Task template name: Диалог
Task type: action dialog
description: "Talk to the helper."
Tasks:
[empty]
congratulation: "Done."
Character: Helper
"""


class WorkflowFastTests(unittest.TestCase):
    def test_stage3_fast_command_writes_pack_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            campaigns_dir = Path(temp_dir) / "campaigns"
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "stage3_quests.txt").write_text(STAGE3_ONE_DIALOG, encoding="utf-8")

            exit_code = workflow_fast.main(
                [
                    "stage3",
                    "--campaign",
                    "Event_2026",
                    "--pack",
                    "pack_001",
                    "--campaigns-dir",
                    str(campaigns_dir),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((pack_dir / "quest_plan.json").exists())
            self.assertTrue((pack_dir / "quest_plan.resolved.json").exists())
            resolved = json.loads((pack_dir / "quest_plan.resolved.json").read_text(encoding="utf-8"))
            self.assertEqual(resolved["summary"]["issues"], 0)
            self.assertEqual(resolved["quests"][0]["tasks"][0]["task_template_id"], "TT-001")

    def test_status_uses_active_context_when_ids_are_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            campaigns_dir = root / "campaigns"
            context_path = root / "active_context.json"
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            context_path.write_text(
                json.dumps(
                    {
                        "campaign_id": "Event_2026",
                        "pack_id": "pack_001",
                        "stage_approvals": {},
                    }
                ),
                encoding="utf-8",
            )

            exit_code = workflow_fast.main(
                [
                    "status",
                    "--campaigns-dir",
                    str(campaigns_dir),
                    "--context",
                    str(context_path),
                ]
            )

            self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
