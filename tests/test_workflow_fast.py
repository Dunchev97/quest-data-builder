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

    def test_quest_group_fast_command_reads_choices_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            campaigns_dir = root / "campaigns"
            context_path = root / "active_context.json"
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "filled_tasks.json").write_text(
                json.dumps(
                    {
                        "quests": [
                            {
                                "classname_quests": "Event_2026_Story_1",
                                "title_quest": "Проверка",
                                "tasks": [],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (pack_dir / "quest_group_choices.json").write_text(
                json.dumps(
                    {
                        "title": "Проверочная группа",
                        "description": "Начало проверки.",
                        "description_complete": "Проверка завершена.",
                        "description_spoil": "Проверка не завершена.",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            context_path.write_text(
                json.dumps(
                    {
                        "campaign_id": "Event_2026",
                        "pack_id": "pack_001",
                        "stage_approvals": {
                            "4": {
                                "approved": True,
                                "campaign_id": "Event_2026",
                                "pack_id": "pack_001",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            exit_code = workflow_fast.main(
                [
                    "quest-group",
                    "--campaign",
                    "Event_2026",
                    "--pack",
                    "pack_001",
                    "--campaigns-dir",
                    str(campaigns_dir),
                    "--context",
                    str(context_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((pack_dir / "quest_group.json").exists())

    def test_interactive_objects_fast_command_writes_selection_preview(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            campaigns_dir = root / "campaigns"
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)

            exit_code = workflow_fast.main(
                [
                    "interactive-objects",
                    "--campaign",
                    "Event_2026",
                    "--pack",
                    "pack_001",
                    "--campaigns-dir",
                    str(campaigns_dir),
                    "--select",
                    "chest_1",
                    "--select",
                    "help_1",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((campaigns_dir / "Event_2026" / "interactive_objects.json").exists())
            self.assertTrue((campaigns_dir / "Event_2026" / "interactive_objects.preview.md").exists())

    def test_stage6_exports_interactive_object_csv_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            campaigns_dir = root / "campaigns"
            context_path = root / "active_context.json"
            campaign_dir = campaigns_dir / "Event_2026"
            pack_dir = campaign_dir / "pack_001"
            pack_dir.mkdir(parents=True)
            (campaign_dir / "campaign.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "campaign_id": "Event_2026",
                        "packs": [{"pack_id": "pack_001"}],
                    }
                ),
                encoding="utf-8",
            )
            (campaign_dir / "campaign_memory.json").write_text(
                json.dumps({"version": 1, "campaign_id": "Event_2026", "packs": {}}),
                encoding="utf-8",
            )
            (pack_dir / "filled_tasks.json").write_text(
                json.dumps(
                    {
                        "quests": [
                            {
                                "classname_quests": "Event_2026_Story_1",
                                "title_quest": "Проверка",
                                "tasks": [],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (pack_dir / "context_pack.json").write_text(json.dumps({"quests": []}), encoding="utf-8")
            (pack_dir / "filled_tasks.validation.json").write_text(
                json.dumps({"summary": {"errors": 0, "warnings": 0}}),
                encoding="utf-8",
            )
            (pack_dir / "quest_group.json").write_text(
                json.dumps(
                    {
                        "input": "/quest_group/fun/Fun13_Story_1.proto.js",
                        "output": "/quest_group/fun/Event_2026_pack_001.proto.js",
                        "title": "Проверочная группа",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (pack_dir / "quest_group.validation.json").write_text(
                json.dumps({"summary": {"errors": 0, "warnings": 0}}),
                encoding="utf-8",
            )
            (campaign_dir / "interactive_objects.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "selected_objects": [
                            {"template_id": "chest_1"},
                            {"template_id": "help_1"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            context_path.write_text(
                json.dumps(
                    {
                        "campaign_id": "Event_2026",
                        "pack_id": "pack_001",
                        "stage_approvals": {
                            "5": {
                                "approved": True,
                                "campaign_id": "Event_2026",
                                "pack_id": "pack_001",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            exit_code = workflow_fast.main(
                [
                    "stage6",
                    "--campaign",
                    "Event_2026",
                    "--pack",
                    "pack_001",
                    "--campaigns-dir",
                    str(campaigns_dir),
                    "--context",
                    str(context_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((campaign_dir / "generated_interactive_objects_chest_1.csv").exists())
            self.assertTrue((campaign_dir / "generated_interactive_objects_help_1.csv").exists())
            self.assertTrue((campaign_dir / "generated_interactive_objects.summary.json").exists())
            self.assertTrue((campaign_dir / "resource_table.csv").exists())
            self.assertTrue((campaign_dir / "resource_table.summary.json").exists())


if __name__ == "__main__":
    unittest.main()
