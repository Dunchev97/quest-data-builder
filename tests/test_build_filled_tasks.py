import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.build_filled_tasks import build_filled_tasks, build_filled_tasks_file
from src.validate_task_objects import build_template_catalog, validate_filled_tasks


def context_pack() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Парадная проверка",
                "quest_number": 1,
                "description": "Парад рассыпался на детали, но домовой помощник быстро вернет порядок.",
                "congratulation": "Парад снова готов.",
                "character": "Царевна Несмеяна",
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-001",
                        "task_template_name": "Диалог",
                        "task_type": "action dialog",
                        "candidates": [],
                    },
                    {
                        "task_number": 2,
                        "task_template_id": "TT-004",
                        "task_template_name": "HOG на локации",
                        "task_type": "HOG clean_debris location",
                        "candidates": [],
                    },
                    {
                        "task_number": 3,
                        "task_template_id": "TT-020",
                        "task_template_name": "Уборка конкретного мусора в гостях",
                        "task_type": "garbage classname in_guest",
                        "candidates": [
                            {
                                "candidate_id": "garbage:Cucumber",
                                "garbage_classname": "Cucumber",
                                "garbage_title": "Надкусанный огурец",
                                "locations": [{"code": "31", "title": "Оранжерея", "tags": ["home"]}],
                            }
                        ],
                    },
                    {
                        "task_number": 4,
                        "task_template_id": "TT-008",
                        "task_template_name": "Получить ASK",
                        "task_type": "get_asset ASK",
                        "candidates": [],
                    },
                    {
                        "task_number": 5,
                        "task_template_id": "TT-016",
                        "task_template_name": "GR с цветов в гостях",
                        "task_type": "get_asset GR in_guest flower",
                        "candidates": [
                            {
                                "candidate_id": "flower:FlowerCvetikSemicvetik",
                                "flower_classname": "FlowerCvetikSemicvetik",
                                "flower_title": "Цветик-семицветик",
                            }
                        ],
                    },
                    {
                        "task_number": 6,
                        "task_template_id": "TT-002",
                        "task_template_name": "Крафт",
                        "task_type": "get_and_decrease_asset craft",
                        "candidates": [],
                    },
                    {
                        "task_number": 7,
                        "task_template_id": "TT-024",
                        "task_template_name": "Загадка на мусор в гостях",
                        "task_type": "garbage classname in_guest mystery",
                        "candidates": [
                            {
                                "candidate_id": "garbage:Garbage_WarmBlanket",
                                "garbage_classname": "Garbage_WarmBlanket",
                                "garbage_title": "Тёплое Покрывало",
                                "locations": [{"code": "31", "title": "Оранжерея", "tags": ["home"]}],
                            }
                        ],
                    },
                ],
            }
        ],
        "generated_sequence_offsets": {},
        "next_generated_numbers": {},
    }


def choices() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "tasks": [
                    {
                        "task_number": 1,
                        "location_title": "Оранжерея",
                        "dialogue_replica": "Поговорим спокойно и найдем пропажу до начала парада.",
                    },
                    {
                        "task_number": 2,
                        "item_title": "огуречный значок",
                        "location_title": "Оранжерея",
                        "choice_reason": "Ищем огуречный значок как маленькую улику рядом с праздничным пьедесталом.",
                    },
                    {"task_number": 3, "selected_candidate_id": "garbage:Cucumber"},
                    {"task_number": 4, "item_title": "Барабанные палочки"},
                    {"task_number": 5, "selected_candidate_id": "flower:FlowerCvetikSemicvetik", "item_title": "Парадная лента"},
                    {"task_number": 6, "item_title": "Парадный барабан"},
                    {
                        "task_number": 7,
                        "selected_candidate_id": "garbage:Garbage_WarmBlanket",
                        "riddle": "На кресле тихо я лежу, узором домик сторожу. У друга взглядом отыщи, и след в истории найди.",
                    },
                ],
            }
        ]
    }


class BuildFilledTasksTests(unittest.TestCase):
    def test_template_catalog_declares_stage4_contracts(self) -> None:
        templates = build_template_catalog(PROJECT_ROOT / "data" / "task_templates.json")

        for template_id, template in templates.items():
            self.assertIn("stage4_contract", template)
            if template_id != "TT-035":
                self.assertIs(template["stage4_contract"]["ai_writes_task_object"], False)
                self.assertIn("task_number", template["stage4_contract"]["choice_fields"])

    def test_builds_strict_task_objects_from_semantic_choices(self) -> None:
        result = build_filled_tasks(context_pack(), choices())

        self.assertEqual(result["summary"]["issues"], 0)
        tasks = result["quests"][0]["tasks"]
        self.assertEqual(tasks[0]["task_object"]["hint"], "Поговори с Царевна Несмеяна. Для этого просто кликни на неё. Она находится в Оранжерея.")
        self.assertEqual(tasks[1]["task_object"]["hint"], "Найди огуречный значок. Место поиска: Оранжерея. Если найти все не удаётся, можно купить подсказку.")
        self.assertEqual(tasks[3]["task_object"]["hint"], "Попроси у друзей или купи.")
        self.assertEqual(tasks[5]["task_object"]["hint"], "Для создания используй Станок.")
        self.assertIn("создаём Парадный барабан", tasks[3]["choice_reason"])

        validation = validate_filled_tasks(
            {"quests": result["quests"]},
            context_pack(),
            build_template_catalog(PROJECT_ROOT / "data" / "task_templates.json"),
        )
        self.assertEqual(validation["summary"]["errors"], 0)

    def test_file_builder_writes_filled_tasks_and_build_summary(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            context_path = root / "context_pack.json"
            choices_path = root / "task_choices.json"
            output_path = root / "filled_tasks.json"
            build_path = root / "filled_tasks.build.json"
            context_path.write_text(json.dumps(context_pack(), ensure_ascii=False), encoding="utf-8")
            choices_path.write_text(json.dumps(choices(), ensure_ascii=False), encoding="utf-8")

            result = build_filled_tasks_file(context_path, choices_path, output_path, build_path)

            self.assertEqual(result["summary"]["issues"], 0)
            self.assertTrue(output_path.exists())
            self.assertTrue(build_path.exists())


if __name__ == "__main__":
    unittest.main()
