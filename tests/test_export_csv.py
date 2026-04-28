import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.export_csv import export_filled_tasks_to_csv, main


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sample_filled_tasks() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_2",
                "title_quest": "Проверка",
                "quest_number": 2,
                "description": "Описание квеста.",
                "congratulation": "Поздравление квеста.",
                "tasks": [
                    {
                        "task_number": 4,
                        "task_template_id": "TT-020",
                        "task_template_name": "Уборка конкретного мусора в гостях",
                        "task_type": "garbage classname in_guest",
                        "selected_candidate_id": "garbage:Ashes",
                        "task_object": {
                            "type": "garbage",
                            "classname": "Ashes",
                            "in_guest": 1,
                            "amount": 1,
                            "price": 1,
                            "title": "Убери мусор Пепел в гостях",
                            "hint": "Место поиска: Котельная.",
                            "identifier": "",
                        },
                    },
                    {
                        "task_number": 5,
                        "task_template_id": "TT-001",
                        "task_template_name": "Диалог",
                        "task_type": "action dialog",
                        "selected_candidate_id": None,
                        "dialogue_replica": "Нужно проверить, всё ли готово к запуску квеста.",
                        "task_object": {
                            "type": "action",
                            "icon": "Event_2026_Character_1",
                            "action": "Event_2026_Character_1_Dialog_1",
                            "title": "Поговори с героем",
                            "hint": "Он находится в локации Котельная.",
                            "go_to_location": [{"classname": "Event_2026_Character_1"}],
                        },
                    },
                ],
            }
        ]
    }


def sample_quest_group() -> dict[str, object]:
    return {
        "input": "/quest_group/fun/Fun13_Story_1.proto.js",
        "output": "/quest_group/fun/Event_2026_Story_2.proto.js",
        "title": "Проверочный переполох",
        "description": "Герои проверяют запуск квестового пака.",
        "description_complete": "Пак проверен, все задачи готовы.",
        "description_spoil": "Проверка не удалась, и запуск придется повторить.",
        "extra": {
            "quest_reward_prewiew": ["", "", ""],
            "description_condition": "Герои проверяют запуск квестового пака.",
            "description_complete": "Пак проверен, все задачи готовы.",
        },
    }


class ExportCsvTests(unittest.TestCase):
    def test_exports_filled_tasks_csv_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output_path = Path(tmp) / "generated_quests.csv"
            summary = export_filled_tasks_to_csv(sample_filled_tasks(), output_path, quest_group=sample_quest_group())

            self.assertEqual(summary["quests_found"], 1)
            self.assertEqual(summary["quest_group_exported"], 1)
            self.assertEqual(summary["tasks_exported"], 2)
            self.assertTrue(output_path.exists())

            with output_path.open("r", encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream, delimiter=";"))

            self.assertEqual(rows[0][1], "Квест группа")
            self.assertEqual(rows[1][:10], ["ml", "string", "string", "string", "string", "string", "string", "array_of_values", "string", "string"])
            self.assertEqual(rows[2][1:10], ["input", "output", "title", "description", "description_complete", "description_spoil", "extra.quest_reward_prewiew", "extra.description_condition", "extra.description_complete"])
            self.assertEqual(rows[3][1], "/quest_group/fun/Fun13_Story_1.proto.js")
            self.assertEqual(rows[3][2], "/quest_group/fun/Event_2026_Story_2.proto.js")
            self.assertEqual(rows[3][7], "")
            self.assertEqual(rows[4][7], "")
            self.assertEqual(rows[5][7], "")

            quest_row_index = next(index for index, row in enumerate(rows) if row[1] == "Квест 2")
            self.assertEqual(rows[quest_row_index + 1][:8], ["sl", "string", "string", "string", "string", "string", "string", "string"])
            self.assertEqual(rows[quest_row_index + 2][1:8], ["input", "output", "title", "description", "congratulation", "helper", "extra.sequence_icon"])
            self.assertEqual(rows[quest_row_index + 3][3], "Проверка")
            self.assertEqual(rows[quest_row_index + 3][4], "Описание квеста.")
            self.assertEqual(rows[quest_row_index + 3][5], "Поздравление квеста.")
            self.assertEqual(rows[quest_row_index + 3][6], "Event_2026_Character_1")
            self.assertEqual(rows[quest_row_index + 3][7], "MagazinePage_Event_2026_QuestIcon_1")
            self.assertEqual(rows[quest_row_index + 5][1], "Таск 1")
            self.assertEqual(rows[quest_row_index + 5][2], "Уборка конкретного мусора в гостях")
            self.assertEqual(rows[quest_row_index + 7][3], "tasks.0")
            self.assertEqual(rows[quest_row_index + 8][1], "/quest/generated/Event_2026/story_2/Event_2026_Story_2.proto.js")
            self.assertEqual(rows[quest_row_index + 8][3], "type")
            self.assertEqual(rows[quest_row_index + 8][4], "garbage")
            dialog_header = next(row for row in rows if row[1] == "Таск 2" and row[2] == "Диалог")
            self.assertEqual(dialog_header[5], "РЕПЛИКА ДИАЛОГА: Нужно проверить, всё ли готово к запуску квеста.")
            self.assertTrue(any(row[3] == "identifier" for row in rows))
            self.assertTrue(any(row[3] == "go_to_location" and "Event_2026_Character_1" in row[4] for row in rows))

    def test_cli_refuses_validation_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            validation_path = root / "filled_tasks.validation.json"
            quest_group_path = root / "quest_group.json"
            quest_group_validation_path = root / "quest_group.validation.json"
            output_path = root / "generated_quests.csv"
            write_json(input_path, sample_filled_tasks())
            write_json(validation_path, {"summary": {"errors": 1}})
            write_json(quest_group_path, sample_quest_group())
            write_json(quest_group_validation_path, {"summary": {"errors": 0}})

            exit_code = main(
                [
                    str(input_path),
                    "--validation-json",
                    str(validation_path),
                    "--quest-group",
                    str(quest_group_path),
                    "--quest-group-validation-json",
                    str(quest_group_validation_path),
                    "--output-csv",
                    str(output_path),
                    "--allow-unapproved-stage5",
                ]
            )

            self.assertEqual(exit_code, 2)
            self.assertFalse(output_path.exists())

    def test_cli_exports_when_validation_passed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            validation_path = root / "filled_tasks.validation.json"
            quest_group_path = root / "quest_group.json"
            quest_group_validation_path = root / "quest_group.validation.json"
            output_path = root / "generated_quests.csv"
            write_json(input_path, sample_filled_tasks())
            write_json(validation_path, {"summary": {"errors": 0}})
            write_json(quest_group_path, sample_quest_group())
            write_json(quest_group_validation_path, {"summary": {"errors": 0}})

            exit_code = main(
                [
                    str(input_path),
                    "--validation-json",
                    str(validation_path),
                    "--quest-group",
                    str(quest_group_path),
                    "--quest-group-validation-json",
                    str(quest_group_validation_path),
                    "--output-csv",
                    str(output_path),
                    "--allow-unapproved-stage5",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())

    def test_cli_defaults_to_campaign_pack_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaigns_dir = root / "campaigns"
            pack_path = campaigns_dir / "Event_2026" / "pack_001"
            input_path = pack_path / "filled_tasks.json"
            validation_path = pack_path / "filled_tasks.validation.json"
            quest_group_path = pack_path / "quest_group.json"
            quest_group_validation_path = pack_path / "quest_group.validation.json"
            output_path = pack_path / "generated_quests.csv"
            write_json(input_path, sample_filled_tasks())
            write_json(validation_path, {"summary": {"errors": 0}})
            write_json(quest_group_path, sample_quest_group())
            write_json(quest_group_validation_path, {"summary": {"errors": 0}})

            with patch("src.export_csv.DEFAULT_CAMPAIGNS_DIR", campaigns_dir):
                exit_code = main(
                    [
                        "--campaign",
                        "Event_2026",
                        "--current-pack",
                        "pack_001",
                        "--allow-unapproved-stage5",
                    ]
                )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())

    def test_cli_refuses_without_stage5_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            validation_path = root / "filled_tasks.validation.json"
            quest_group_path = root / "quest_group.json"
            quest_group_validation_path = root / "quest_group.validation.json"
            context_path = root / "active_context.json"
            output_path = root / "generated_quests.csv"
            write_json(input_path, sample_filled_tasks())
            write_json(validation_path, {"summary": {"errors": 0}})
            write_json(quest_group_path, sample_quest_group())
            write_json(quest_group_validation_path, {"summary": {"errors": 0}})
            write_json(
                context_path,
                {
                    "version": 1,
                    "campaign_id": "Event_2026",
                    "pack_id": "pack_001",
                    "stage_approvals": {},
                },
            )

            exit_code = main(
                [
                    str(input_path),
                    "--validation-json",
                    str(validation_path),
                    "--quest-group",
                    str(quest_group_path),
                    "--quest-group-validation-json",
                    str(quest_group_validation_path),
                    "--approval-context",
                    str(context_path),
                    "--campaign",
                    "Event_2026",
                    "--current-pack",
                    "pack_001",
                    "--output-csv",
                    str(output_path),
                ]
            )

            self.assertEqual(exit_code, 1)
            self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
