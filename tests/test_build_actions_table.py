import tempfile
import unittest
from pathlib import Path

from src.build_actions_table import build_actions, write_csv
from src.campaigns import write_json


class BuildActionsTableTests(unittest.TestCase):
    def test_builds_actions_and_keeps_sequence_across_packs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            campaigns_dir = Path(temp_dir) / "campaigns"
            campaign_dir = campaigns_dir / "Event_2026"
            pack_001 = campaign_dir / "pack_001"
            pack_002 = campaign_dir / "pack_002"
            pack_001.mkdir(parents=True)
            pack_002.mkdir(parents=True)

            write_json(
                pack_001 / "filled_tasks.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "quest_number": 1,
                            "character": "Мастер",
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "task_template_id": "TT-001",
                                    "task_type": "action dialog",
                                    "dialogue_replica": "Первая реплика.",
                                    "task_object": {
                                        "icon": "Event_2026_Character_1",
                                        "title": "Поговори с Мастером",
                                    },
                                },
                                {
                                    "task_number": 2,
                                    "task_template_id": "TT-004",
                                    "task_type": "HOG clean_debris location",
                                    "task_object": {"param": "Event_2026_HOG_1"},
                                },
                            ],
                        }
                    ]
                },
            )

            write_json(
                pack_002 / "filled_tasks.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_2",
                            "quest_number": 2,
                            "character": "Мастер",
                            "tasks": [
                                {
                                    "task_number": 3,
                                    "task_template_id": "TT-001",
                                    "task_type": "action dialog",
                                    "dialogue_replica": "Вторая реплика.",
                                    "task_object": {
                                        "icon": "Event_2026_Character_1",
                                        "title": "Поговори с Мастером",
                                    },
                                },
                                {
                                    "task_number": 4,
                                    "task_template_id": "TT-033",
                                    "task_type": "action give",
                                    "task_object": {
                                        "icon": "Event_2026_R_1",
                                        "go_to_location": [{"classname": "Event_2026_Character_1"}],
                                        "hint": "Передай Деталь персонажу Мастер. Он находится на Площадь.",
                                        "title": "Передай Деталь",
                                    },
                                },
                            ],
                        }
                    ]
                },
            )

            rows, summary = build_actions("Event_2026", campaigns_dir=campaigns_dir, current_pack_id="pack_002")

            flat_rows = [";".join(str(cell) for cell in row) for row in rows]
            self.assertEqual(summary["dialog_actions"], 1)
            self.assertEqual(summary["search_actions"], 0)
            self.assertEqual(summary["give_actions"], 1)
            self.assertFalse(any("Event_2026_Character_1_Dialog_1" in row for row in flat_rows))
            self.assertTrue(any("Event_2026_Character_1_Dialog_2" in row for row in flat_rows))
            self.assertTrue(any("action_Event_2026_Character_1_Give_1" in row for row in flat_rows))
            self.assertFalse(any("search_Event_2026_HOG_1" in row for row in flat_rows))
            self.assertTrue(any("active_quest=Event_2026_Story_2" in row for row in flat_rows))

            output_csv = campaign_dir / "pack_002" / "generated_actions.csv"
            write_csv(output_csv, rows)
            self.assertIn("ЭКШЕНЫ Give", output_csv.read_text(encoding="cp1251"))

    def test_can_still_build_campaign_wide_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            campaigns_dir = Path(temp_dir) / "campaigns"
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)

            write_json(
                pack_dir / "filled_tasks.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "quest_number": 1,
                            "character": "Мастер",
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "task_template_id": "TT-001",
                                    "task_type": "action dialog",
                                    "dialogue_replica": "Первая реплика.",
                                    "task_object": {
                                        "icon": "Event_2026_Character_1",
                                        "title": "Поговори с Мастером",
                                    },
                                },
                                {
                                    "task_number": 2,
                                    "task_template_id": "TT-004",
                                    "task_type": "HOG clean_debris location",
                                    "task_object": {"param": "Event_2026_HOG_1"},
                                },
                            ],
                        }
                    ]
                },
            )

            rows, summary = build_actions("Event_2026", campaigns_dir=campaigns_dir)

            flat_rows = [";".join(str(cell) for cell in row) for row in rows]
            self.assertEqual(summary["dialog_actions"], 1)
            self.assertEqual(summary["search_actions"], 1)
            self.assertTrue(any("money=2" in row for row in flat_rows))


if __name__ == "__main__":
    unittest.main()
