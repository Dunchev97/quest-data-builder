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


def give_context_pack() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_2",
                "title_quest": "Большой перезвон",
                "quest_number": 2,
                "description": "Нужно подготовить ключ перезвона и передать его дирижёру.",
                "congratulation": "Перезвон готов, но путь дальше только открылся.",
                "character": "Госпожа Молоточек",
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-033",
                        "task_template_name": "Передача предмета",
                        "task_type": "action give",
                        "candidates": [],
                    },
                    {
                        "task_number": 2,
                        "task_template_id": "TT-013",
                        "task_template_name": "GR с мусора в локации дома",
                        "task_type": "get_asset GR garbage location_tags",
                        "candidates": [
                            {
                                "candidate_id": "garbage:GearDust",
                                "garbage_classname": "GearDust",
                                "garbage_title": "Пыльная шестерёнка",
                                "locations": [{"code": "42", "title": "Мастерская", "tags": ["home"]}],
                            }
                        ],
                    },
                    {
                        "task_number": 3,
                        "task_template_id": "TT-008",
                        "task_template_name": "Получить ASK",
                        "task_type": "get_asset ASK",
                        "candidates": [],
                    },
                ],
            }
        ],
        "generated_sequence_offsets": {},
        "next_generated_numbers": {},
    }


def give_choices() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_2",
                "tasks": [
                    {
                        "task_number": 1,
                        "item_title": "Праздничный ключ перезвона",
                        "person": "Госпоже Молоточек",
                        "location_title": "Мастерская",
                    },
                    {
                        "task_number": 2,
                        "selected_candidate_id": "garbage:GearDust",
                        "item_title": "Латунная пластинка ключа",
                    },
                    {"task_number": 3, "item_title": "Крепёжные колечки ключа"},
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

    def test_template_catalog_has_task_object_defaults_from_csv(self) -> None:
        templates = build_template_catalog(PROJECT_ROOT / "data" / "task_templates.json")

        self.assertEqual(templates["TT-004"]["task_object_defaults"], {"amount": 20, "price": 20})
        self.assertEqual(templates["TT-008"]["task_object_defaults"], {"amount": 10, "price": 20})
        self.assertEqual(templates["TT-016"]["task_object_defaults"], {"amount": 80, "price": 40})
        self.assertEqual(templates["TT-033"]["task_object_defaults"], {"amount": 1})
        self.assertNotIn("task_object_defaults", templates["TT-001"])

    def test_builds_strict_task_objects_from_semantic_choices(self) -> None:
        result = build_filled_tasks(context_pack(), choices())

        self.assertEqual(result["summary"]["issues"], 0)
        self.assertEqual(result["quests"][0]["helper"], "Event_2026_Character_1")
        tasks = result["quests"][0]["tasks"]
        self.assertEqual(tasks[0]["task_object"]["hint"], "Поговори с Царевна Несмеяна. Для этого просто кликни на неё. Она находится в Оранжерея.")
        self.assertEqual(tasks[1]["task_object"]["hint"], "Найди Огуречный значок. Место поиска: Оранжерея. Если найти все не удаётся, можно купить подсказку.")
        self.assertEqual(tasks[1]["task_object"]["amount"], 20)
        self.assertEqual(tasks[1]["task_object"]["price"], 20)
        self.assertEqual(tasks[1]["resource_title"], "Огуречный значок")
        self.assertEqual(tasks[2]["task_object"]["amount"], 20)
        self.assertEqual(tasks[2]["task_object"]["price"], 20)
        self.assertEqual(tasks[3]["task_object"]["hint"], "Попроси у друзей или купи.")
        self.assertEqual(tasks[3]["task_object"]["amount"], 10)
        self.assertEqual(tasks[3]["task_object"]["price"], 20)
        self.assertEqual(tasks[3]["resource_title"], "Барабанные палочки")
        self.assertEqual(tasks[4]["task_object"]["amount"], 80)
        self.assertEqual(tasks[4]["task_object"]["price"], 40)
        self.assertEqual(tasks[5]["task_object"]["hint"], "Для создания используй Станок.")
        self.assertEqual(tasks[5]["task_object"]["amount"], 1)
        self.assertNotIn("price", tasks[5]["task_object"])
        self.assertIn("создаём Парадный барабан", tasks[3]["choice_reason"])

        validation = validate_filled_tasks(
            {"quests": result["quests"]},
            context_pack(),
            build_template_catalog(PROJECT_ROOT / "data" / "task_templates.json"),
        )
        self.assertEqual(validation["summary"]["errors"], 0)

    def test_item_text_field_controls_task_title_and_resource_title(self) -> None:
        context = {
            "quests": [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "title_quest": "Проверка падежей",
                    "quest_number": 1,
                    "tasks": [
                        {
                            "task_number": 1,
                            "task_template_id": "TT-011",
                            "task_template_name": "Получить элемент коллекции (зависит от редкости)",
                            "task_type": "get_asset Collection",
                            "candidates": [
                                {
                                    "candidate_id": "collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home",
                                    "collection_classname": "GarbageCupCoffeeCollection5",
                                    "collection_title": "Турка",
                                    "source_title": "Кофейная чашка",
                                }
                            ],
                        },
                        {
                            "task_number": 2,
                            "task_template_id": "TT-008",
                            "task_template_name": "Получить ASK",
                            "task_type": "get_asset ASK",
                            "candidates": [],
                        },
                    ],
                }
            ]
        }
        choice_data = {
            "quests": [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "tasks": [
                        {
                            "task_number": 1,
                            "selected_candidate_id": "collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home",
                            "item_title_accusative": "Турку",
                        },
                        {
                            "task_number": 2,
                            "item_title": "Занавеска",
                            "item_title_accusative": "Занавеску",
                        },
                    ],
                }
            ]
        }

        result = build_filled_tasks(context, choice_data)

        self.assertEqual(result["summary"]["issues"], 0)
        tasks = result["quests"][0]["tasks"]
        self.assertEqual(tasks[0]["task_object"]["title"], "Найди Турку")
        self.assertEqual(tasks[1]["task_object"]["title"], "Попроси у друзей Занавеску")
        self.assertEqual(tasks[1]["resource_title"], "Занавеска")

    def test_tt033_acts_as_craft_anchor_for_neighbor_resources(self) -> None:
        result = build_filled_tasks(give_context_pack(), give_choices())

        self.assertEqual(result["summary"]["issues"], 0)
        tasks = result["quests"][0]["tasks"]
        self.assertEqual(tasks[0]["task_object"]["title"], "Передай Праздничный ключ перезвона")
        self.assertEqual(tasks[0]["task_object"]["icon"], "Event_2026_Give_2_1")
        self.assertEqual(tasks[0]["task_object"]["action"], "Event_2026_Give_2_1_Give")
        self.assertIn("Праздничный ключ перезвона", tasks[1]["choice_reason"])
        self.assertIn("Праздничный ключ перезвона", tasks[2]["choice_reason"])

        validation = validate_filled_tasks(
            {"quests": result["quests"]},
            give_context_pack(),
            build_template_catalog(PROJECT_ROOT / "data" / "task_templates.json"),
        )
        self.assertEqual(validation["summary"]["errors"], 0)

    def test_tt033_reuses_existing_target_character_number(self) -> None:
        context = {
            "quests": [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "quest_number": 1,
                    "character": "Кот Учёный",
                    "tasks": [],
                },
                {
                    "classname_quests": "Event_2026_Story_2",
                    "quest_number": 2,
                    "character": "Полицейский",
                    "tasks": [],
                },
                {
                    "classname_quests": "Event_2026_Story_3",
                    "quest_number": 3,
                    "character": "Ректор",
                    "tasks": [
                        {
                            "task_number": 1,
                            "task_template_id": "TT-033",
                            "task_template_name": "Передача предмета",
                            "task_type": "action give",
                            "candidates": [],
                        }
                    ],
                },
            ],
            "generated_sequence_offsets": {},
            "next_generated_numbers": {},
        }
        choice_data = {
            "quests": [
                {
                    "classname_quests": "Event_2026_Story_3",
                    "tasks": [
                        {
                            "task_number": 1,
                            "item_title": "Церемониальная печать",
                            "person": "Ректор",
                            "location_title": "Омут",
                        }
                    ],
                }
            ]
        }

        result = build_filled_tasks(context, choice_data)

        task_object = result["quests"][2]["tasks"][0]["task_object"]
        self.assertEqual(result["summary"]["issues"], 0)
        self.assertEqual(task_object["icon"], "Event_2026_Give_3_1")
        self.assertEqual(task_object["action"], "Event_2026_Give_3_1_Give")

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
