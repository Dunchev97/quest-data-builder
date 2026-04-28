import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.validate_task_objects import main, validate_filled_tasks


def context_pack() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Проверка",
                "quest_number": 1,
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-020",
                        "task_template_name": "Уборка конкретного мусора в гостях",
                        "task_type": "garbage classname in_guest",
                        "candidate_domain": "garbage",
                        "candidates": [
                            {
                                "candidate_id": "garbage:Ashes",
                                "garbage_classname": "Ashes",
                                "garbage_title": "Пепел",
                                "locations": [{"code": "loc1", "title": "Котельная"}],
                            }
                        ],
                    },
                    {
                        "task_number": 2,
                        "task_template_id": "TT-011",
                        "task_template_name": "Получить элемент коллекции (зависит от редкости)",
                        "task_type": "get_asset Collection",
                        "candidate_domain": "collection_drop",
                        "candidates": [
                            {
                                "candidate_id": "collection_drop:PlateCollection1:BrokenPlate:home",
                                "collection_classname": "PlateCollection1",
                                "collection_title": "Фарфоровый осколок",
                                "source_classname": "BrokenPlate",
                                "source_title": "Разбитая тарелка",
                                "source_type": "garbage",
                            }
                        ],
                    },
                    {
                        "task_number": 3,
                        "task_template_id": "TT-019",
                        "task_template_name": "Сбор цветов в гостях",
                        "task_type": "action take_crop_in_guest",
                        "candidate_domain": "flower",
                        "candidates": [
                            {
                                "candidate_id": "flower:FlowerSix",
                                "flower_classname": "FlowerSix",
                                "flower_title": "Василек",
                            }
                        ],
                    },
                ],
            }
        ]
    }


def templates() -> dict[str, dict[str, object]]:
    data = json.loads((PROJECT_ROOT / "data" / "task_templates.json").read_text(encoding="utf-8"))
    return {template["id"]: template for template in data["templates"]}


def filled_task(
    task_number: int,
    task_template_id: str,
    task_template_name: str,
    task_type: str,
    selected_candidate_id: str | None,
    task_object: dict[str, object],
    dialogue_replica: str | None = None,
) -> dict[str, object]:
    task = {
        "task_number": task_number,
        "task_template_id": task_template_id,
        "task_template_name": task_template_name,
        "task_type": task_type,
        "selected_candidate_id": selected_candidate_id,
        "choice_reason": "Подходит по контексту.",
        "task_object": task_object,
    }
    if dialogue_replica is not None:
        task["dialogue_replica"] = dialogue_replica
    return task


def filled_tasks(*tasks: dict[str, object]) -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Проверка",
                "quest_number": 1,
                "tasks": list(tasks),
            }
        ]
    }


class ValidateTaskObjectsTests(unittest.TestCase):
    def test_validates_good_garbage_collection_and_flower_tasks(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-020",
                    "Уборка конкретного мусора в гостях",
                    "garbage classname in_guest",
                    "garbage:Ashes",
                    {
                        "type": "garbage",
                        "classname": "Ashes",
                        "in_guest": 1,
                        "amount": 1,
                        "price": 1,
                        "title": "Убери мусор Пепел в гостях",
                        "hint": "Убери мусор Пепел в гостях.",
                    },
                ),
                filled_task(
                    2,
                    "TT-011",
                    "Получить элемент коллекции (зависит от редкости)",
                    "get_asset Collection",
                    "collection_drop:PlateCollection1:BrokenPlate:home",
                    {
                        "type": "get_asset",
                        "classname": "PlateCollection1",
                        "icon": "PlateCollection1",
                        "amount": 1,
                        "price": 1,
                        "title": "Найди Фарфоровый осколок",
                        "hint": "Фарфоровый осколок - элемент коллекции.",
                    },
                ),
                filled_task(
                    3,
                    "TT-019",
                    "Сбор цветов в гостях",
                    "action take_crop_in_guest",
                    "flower:FlowerSix",
                    {
                        "type": "action",
                        "action": "take_crop_in_guest",
                        "param": "FlowerSix",
                        "amount": 1,
                        "price": 1,
                        "title": "Собери Василек в гостях",
                        "hint": "Собирай Василек в гостях.",
                    },
                ),
            ),
            context_pack(),
            templates(),
        )

        self.assertEqual(validation["summary"]["errors"], 0)
        self.assertEqual(validation["summary"]["valid_tasks"], 3)

    def test_reports_selected_candidate_not_found(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-020",
                    "Уборка конкретного мусора в гостях",
                    "garbage classname in_guest",
                    "garbage:MadeUp",
                    {
                        "type": "garbage",
                        "classname": "MadeUp",
                        "in_guest": 1,
                        "amount": 1,
                        "price": 1,
                        "title": "Убери мусор",
                        "hint": "Убери мусор.",
                    },
                )
            ),
            context_pack(),
            templates(),
        )

        self.assertEqual(validation["summary"]["errors"], 1)
        self.assertEqual(validation["errors"][0]["code"], "selected_candidate_not_found")

    def test_reports_candidate_classname_mismatch(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-020",
                    "Уборка конкретного мусора в гостях",
                    "garbage classname in_guest",
                    "garbage:Ashes",
                    {
                        "type": "garbage",
                        "classname": "BrokenPlate",
                        "in_guest": 1,
                        "amount": 1,
                        "price": 1,
                        "title": "Убери мусор",
                        "hint": "Убери мусор.",
                    },
                )
            ),
            context_pack(),
            templates(),
        )

        self.assertEqual(validation["summary"]["errors"], 1)
        self.assertEqual(validation["errors"][0]["code"], "garbage_classname_mismatch")

    def test_reports_missing_required_field(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    3,
                    "TT-019",
                    "Сбор цветов в гостях",
                    "action take_crop_in_guest",
                    "flower:FlowerSix",
                    {
                        "type": "action",
                        "action": "take_crop_in_guest",
                        "amount": 1,
                        "price": 1,
                        "title": "Собери Василек в гостях",
                        "hint": "Собирай Василек в гостях.",
                    },
                )
            ),
            context_pack(),
            templates(),
        )

        self.assertEqual(validation["summary"]["errors"], 1)
        self.assertEqual(validation["errors"][0]["code"], "missing_task_object_field")

    def test_reports_not_ready_template(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-035",
                    "Следы с ресурсами",
                    "not_ready",
                    None,
                    {"type": "action", "title": "Найди следы"},
                )
            ),
            context_pack(),
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("not_ready_task_template", codes)

    def test_reports_unknown_location_in_hint(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-001",
                    "Диалог",
                    "action dialog",
                    None,
                    {
                        "type": "action",
                        "icon": "Event_2026_Character_1",
                        "action": "Event_2026_Character_1_Dialog_1",
                        "title": "Поговори с Домовенком",
                        "hint": "Поговори с Домовенком. Для этого просто кликни на него. Он находится у крыльца под тучей.",
                        "go_to_location": [{"classname": "Event_2026_Character_1"}],
                    },
                    dialogue_replica="Посмотри, где начинается этот странный переполох.",
                )
            ),
            context_pack(),
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("unknown_location_in_hint", codes)

    def test_reports_missing_dialogue_replica(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-001",
                    "Диалог",
                    "action dialog",
                    None,
                    {
                        "type": "action",
                        "icon": "Event_2026_Character_1",
                        "action": "Event_2026_Character_1_Dialog_1",
                        "title": "Поговори с Домовенком",
                        "hint": "Поговори с Домовенком.",
                        "go_to_location": [{"classname": "Event_2026_Character_1"}],
                    },
                )
            ),
            context_pack(),
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("missing_dialogue_replica", codes)

    def test_reports_too_long_dialogue_replica(self) -> None:
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-001",
                    "Диалог",
                    "action dialog",
                    None,
                    {
                        "type": "action",
                        "icon": "Event_2026_Character_1",
                        "action": "Event_2026_Character_1_Dialog_1",
                        "title": "Поговори с Домовенком",
                        "hint": "Поговори с Домовенком.",
                        "go_to_location": [{"classname": "Event_2026_Character_1"}],
                    },
                    dialogue_replica="а" * 361,
                )
            ),
            context_pack(),
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("dialogue_replica_too_long", codes)

    def test_reports_collection_source_reusing_selected_garbage(self) -> None:
        conflict_context = context_pack()
        conflict_context["quests"][0]["tasks"][1]["candidates"][0] = {
            "candidate_id": "collection_drop:AshesCollection1:Ashes:home",
            "collection_classname": "AshesCollection1",
            "collection_title": "Огненная саламандра",
            "source_classname": "Ashes",
            "source_title": "Пепел",
            "source_type": "garbage",
        }
        validation = validate_filled_tasks(
            filled_tasks(
                filled_task(
                    1,
                    "TT-020",
                    "Уборка конкретного мусора в гостях",
                    "garbage classname in_guest",
                    "garbage:Ashes",
                    {
                        "type": "garbage",
                        "classname": "Ashes",
                        "in_guest": 1,
                        "amount": 1,
                        "price": 1,
                        "title": "Убери мусор Пепел в гостях",
                        "hint": "Убери мусор Пепел в гостях.",
                    },
                ),
                filled_task(
                    2,
                    "TT-011",
                    "Получить элемент коллекции (зависит от редкости)",
                    "get_asset Collection",
                    "collection_drop:AshesCollection1:Ashes:home",
                    {
                        "type": "get_asset",
                        "classname": "AshesCollection1",
                        "icon": "AshesCollection1",
                        "amount": 1,
                        "price": 1,
                        "title": "Найди Огненную саламандру",
                        "hint": "Огненная саламандра - элемент коллекции.",
                    },
                ),
            ),
            conflict_context,
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("collection_source_reuses_selected_garbage", codes)

    def test_reports_generated_sequence_mismatch(self) -> None:
        gr_context = {
            "quests": [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "quest_number": 1,
                    "tasks": [
                        {
                            "task_number": 1,
                            "task_template_id": "TT-014",
                            "candidate_domain": "gr_garbage",
                            "candidates": [
                                {
                                    "candidate_id": "gr_garbage:Ashes:guest",
                                    "garbage_classname": "Ashes",
                                    "garbage_title": "Пепел",
                                    "mode": "guest",
                                    "locations": [{"code": "loc1", "title": "Котельная"}],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        validation = validate_filled_tasks(
            {
                "quests": [
                    {
                        "classname_quests": "Event_2026_Story_1",
                        "quest_number": 1,
                        "tasks": [
                            filled_task(
                                1,
                                "TT-014",
                                "GR с конкретного мусора в гостях",
                                "get_asset GR in_guest garbage classname",
                                "gr_garbage:Ashes:guest",
                                {
                                    "type": "get_asset",
                                    "classname": "Event_2026_GR_6",
                                    "icon": "Event_2026_GR_6",
                                    "amount": 1,
                                    "price": 1,
                                    "title": "Найди Латунную стрелку",
                                    "hint": "Убирай мусор Пепел в гостях, чтобы найти. Место поиска: Котельная.",
                                },
                            )
                        ],
                    }
                ]
            },
            gr_context,
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("generated_classname_sequence_mismatch", codes)

    def test_reports_abstract_generated_item(self) -> None:
        gr_context = {
            "quests": [
                {
                    "classname_quests": "Event_2026_Story_1",
                    "quest_number": 1,
                    "tasks": [
                        {
                            "task_number": 1,
                            "task_template_id": "TT-014",
                            "candidate_domain": "gr_garbage",
                            "candidates": [
                                {
                                    "candidate_id": "gr_garbage:Ashes:guest",
                                    "garbage_classname": "Ashes",
                                    "garbage_title": "Пепел",
                                    "mode": "guest",
                                    "locations": [{"code": "loc1", "title": "Котельная"}],
                                }
                            ],
                        }
                    ],
                }
            ]
        }
        validation = validate_filled_tasks(
            {
                "quests": [
                    {
                        "classname_quests": "Event_2026_Story_1",
                        "quest_number": 1,
                        "tasks": [
                            filled_task(
                                1,
                                "TT-014",
                                "GR с конкретного мусора в гостях",
                                "get_asset GR in_guest garbage classname",
                                "gr_garbage:Ashes:guest",
                                {
                                    "type": "get_asset",
                                    "classname": "Event_2026_GR_1",
                                    "icon": "Event_2026_GR_1",
                                    "amount": 1,
                                    "price": 1,
                                    "title": "Найди Небесное давление",
                                    "hint": "Убирай мусор Пепел в гостях, чтобы найти. Место поиска: Котельная.",
                                },
                            )
                        ],
                    }
                ]
            },
            gr_context,
            templates(),
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("generated_item_not_visualizable", codes)

    def test_cli_writes_validation_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            context_path = root / "context_pack.json"
            templates_path = root / "task_templates.json"
            output_path = root / "filled_tasks.validation.json"
            preview_path = root / "filled_tasks.preview.md"
            input_path.write_text(
                json.dumps(
                    filled_tasks(
                        filled_task(
                            1,
                            "TT-020",
                            "Уборка конкретного мусора в гостях",
                            "garbage classname in_guest",
                            "garbage:Ashes",
                            {
                                "type": "garbage",
                                "classname": "Ashes",
                                "in_guest": 1,
                                "amount": 1,
                                "price": 1,
                                "title": "Убери мусор Пепел в гостях",
                                "hint": "Убери мусор Пепел в гостях.",
                            },
                        )
                    ),
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            context_path.write_text(json.dumps(context_pack(), ensure_ascii=False), encoding="utf-8")
            templates_path.write_text((PROJECT_ROOT / "data" / "task_templates.json").read_text(encoding="utf-8"), encoding="utf-8")

            exit_code = main(
                [
                    str(input_path),
                    "--context-pack",
                    str(context_path),
                    "--templates",
                    str(templates_path),
                    "--output-json",
                    str(output_path),
                    "--preview",
                    str(preview_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertTrue(preview_path.exists())
            data = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["errors"], 0)


if __name__ == "__main__":
    unittest.main()
