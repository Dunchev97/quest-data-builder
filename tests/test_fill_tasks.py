import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.fill_tasks import parse_stage3_quests, run_fill
from src.task_templates import detect_template_id


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class FillTasksTests(unittest.TestCase):
    def test_detects_first_supported_task_types(self) -> None:
        self.assertEqual(
            detect_template_id("garbage classname in_guest"),
            "garbage_classname_in_guest",
        )
        self.assertEqual(
            detect_template_id("garbage, classname"),
            "garbage_classname",
        )
        self.assertEqual(
            detect_template_id("get_asset Collection"),
            "get_asset_collection",
        )
        self.assertEqual(
            detect_template_id("get_asset GR in_guest garbage"),
            "get_asset_gr_in_guest_garbage",
        )
        self.assertEqual(
            detect_template_id("action take_crop_in_guest"),
            "action_take_crop_in_guest",
        )

    def test_parses_stage3_text(self) -> None:
        quests = parse_stage3_quests(
            """
Classname quests: Labor_2025_Story_1
title_quest: Потерянный мангал
№ quest: 1
№ task: 1 2 3
Task type: garbage classname in_guest / get_asset Collection / action take_crop_in_guest
description: "Описание"
Tasks:
[пусто на этом этапе]
congratulation: "Готово"
Character: Григорий
"""
        )

        self.assertEqual(len(quests), 1)
        self.assertEqual(quests[0]["classname"], "Labor_2025_Story_1")
        self.assertEqual(quests[0]["task_numbers"], [1, 2, 3])
        self.assertEqual(len(quests[0]["task_types"]), 3)

    def test_fills_tasks_and_exports_csv(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "stage3.txt"
            input_path.write_text(
                """
Classname quests: Labor_2025_Story_1
title_quest: Потерянный мангал
№ quest: 1
№ task: 1 2 3 4 5
Task type: garbage classname in_guest / garbage classname / get_asset Collection / get_asset GR in_guest garbage / action take_crop_in_guest
description: "Описание"
Tasks:
[пусто на этом этапе]
congratulation: "Готово"
Character: Григорий
""",
                encoding="utf-8",
            )
            templates_path = root / "task_templates.json"
            templates_path.write_text(
                (PROJECT_ROOT / "data" / "task_templates.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            write_json(
                root / "quest_ready_index.json",
                {
                    "quest_ready_locations": {
                        "loc1": {
                            "code": "loc1",
                            "title": "Котельная",
                            "tags": ["home"],
                            "garbage_assets": ["Ashes"],
                        }
                    },
                    "quest_ready_garbage": {
                        "Ashes": {
                            "classname": "Ashes",
                            "title": "Пепел",
                            "id": 1,
                        }
                    },
                    "quest_ready_flowers": {
                        "FlowerSix": {
                            "classname": "FlowerSix",
                            "title": "Василек",
                            "id": 2,
                        }
                    },
                    "quest_ready_collections": {
                        "AshesCollection1": {
                            "classname": "AshesCollection1",
                            "title": "Огненная саламандра",
                            "id": 3,
                        }
                    },
                },
            )
            write_json(
                root / "quest_ready_drops.index.json",
                [
                    {
                        "source_type": "garbage",
                        "source_classname": "Ashes",
                        "source_title": "Пепел",
                        "garbage_title": "Пепел",
                        "collection_classname": "AshesCollection1",
                        "collection_title": "Огненная саламандра",
                        "mode": "guest",
                        "locations": [
                            {
                                "code": "loc1",
                                "title": "Котельная",
                                "tags": ["home"],
                            }
                        ],
                    }
                ],
            )

            output = run_fill(
                input_path=input_path,
                templates_path=templates_path,
                quest_ready_index_path=root / "quest_ready_index.json",
                quest_ready_drops_path=root / "quest_ready_drops.index.json",
                output_json_path=root / "generated_tasks.json",
                output_csv_path=root / "generated_quests.csv",
            )

            self.assertEqual(output["summary"]["issues"], 0)
            tasks = output["quests"][0]["tasks"]
            self.assertEqual(len(tasks), 5)
            self.assertEqual(tasks[0]["type"], "garbage")
            self.assertEqual(tasks[0]["in_guest"], 1)
            self.assertEqual(tasks[1]["type"], "garbage")
            self.assertNotIn("in_guest", tasks[1])
            self.assertEqual(tasks[2]["classname"], "AshesCollection1")
            self.assertEqual(tasks[3]["classname"], "Labor_2025_GR_4")
            self.assertEqual(tasks[4]["action"], "take_crop_in_guest")
            self.assertTrue((root / "generated_tasks.json").exists())
            self.assertTrue((root / "generated_quests.csv").exists())

            with (root / "generated_quests.csv").open("r", encoding="utf-8-sig", newline="") as stream:
                rows = list(csv.reader(stream, delimiter=";"))
            self.assertEqual(rows[0][1], "Квест 1")
            self.assertTrue(any("tasks.0" in row for row in rows))
            self.assertTrue(any("AshesCollection1" in row for row in rows))


if __name__ == "__main__":
    unittest.main()
