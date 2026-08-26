import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src import review_docs


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


class ReviewDocsTests(unittest.TestCase):
    def test_stage4_short_title_keeps_head_noun(self) -> None:
        self.assertEqual(review_docs.short_stage4_title("розовую мерную ложечку"), "Розовая ложечка")
        self.assertEqual(review_docs.short_stage4_title("приличное зелье первого впечатления"), "Приличное зелье")
        self.assertEqual(review_docs.short_stage4_title("мягкий цветочный настил"), "Мягкий настил")

    def test_stage1_review_applies_back_to_stage1_story(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "stage1_story.txt").write_text(
                """
Основной сюжет:
Домовята ищут пропавший ключ от кладовой.

Персонажи истории:

Домовед — ворчливый, но добрый хранитель ключей.

Задания сюжета:

1. Домовед: Потерянный ключ
Суть задания: Ключ звенит где-то под половицей.

Конец этапа 1.
""".strip(),
                encoding="utf-8",
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "1", campaigns_dir)
            review_text = review_path.read_text(encoding="utf-8").replace(
                "Ключ звенит где-то под половицей.",
                "Ключ нашёлся в старой сахарнице.",
            )
            review_path.write_text(review_text, encoding="utf-8")

            target = review_docs.apply_review_doc("Event_2026", "pack_001", "1", campaigns_dir)

            result = target.read_text(encoding="utf-8")
            self.assertIn("Ключ нашёлся в старой сахарнице.", result)
            self.assertIn("Конец этапа 1.", result)

    def test_stage1_review_keeps_player_role_out_of_characters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "stage1_story.txt").write_text(
                """
Основной сюжет:
Домовёнок помогает за кулисами.

Роль игрока:
Домовёнок — это игрок, а не отдельный персонаж игры.

Персонажи истории:

Ведущая — объявляет испытания.

Задания сюжета:

1. Ведущая: Первый выпуск
Суть задания: Нужно подготовить площадку.

Конец этапа 1.
""".strip(),
                encoding="utf-8",
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "1", campaigns_dir)

            review = review_path.read_text(encoding="utf-8")
            self.assertIn("## Роль игрока", review)
            characters = review.split("## Персонажи", 1)[1].split("## Квесты", 1)[0]
            self.assertNotIn("- Домовёнок", characters)

    def test_stage1_review_parses_legacy_unnumbered_quests(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "stage1_story.txt").write_text(
                """Основной сюжет:
Домовята собирают старых друзей.

Персонажи истории:

Дед Домовед — хранитель дома.

Задания сюжета:

Дед Домовед: Первое письмо
Суть задания: Дед нашёл старый адрес.

Баба Яга: Второе письмо
Суть задания: Яга готовит ответ.

Конец этапа 1.
""",
                encoding="utf-8",
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "1", campaigns_dir)
            review = review_path.read_text(encoding="utf-8")

            self.assertIn("### 1. Первое письмо", review)
            self.assertIn("Персонаж: Дед Домовед", review)
            self.assertIn("### 2. Второе письмо", review)
            self.assertTrue(review_docs.review_file_is_usable(review_path, "1"))

    def test_stage2_review_parses_legacy_unnumbered_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "stage2_story.txt").write_text(
                """Дед Домовед: Первое письмо
Суть задания: Дед нашёл старое письмо.
Старт:
Домовёнок, взгляни на конверт!
Завершение:
Спасибо, дружок, письмо прочитано.

Баба Яга: Второе письмо
Суть задания: Яга готовит ответ.
Старт:
Домовятушка, подай чернила!
Завершение:
Ай да ответ получился!

Конец этапа 2.
""",
                encoding="utf-8",
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "2", campaigns_dir)
            review = review_path.read_text(encoding="utf-8")

            self.assertIn("### 1. Первое письмо", review)
            self.assertIn("Персонаж: Дед Домовед", review)
            self.assertIn("### 2. Второе письмо", review)
            self.assertTrue(review_docs.review_file_is_usable(review_path, "2"))

    def test_stage3_review_applies_template_names_to_stage3_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            write_json(
                pack_dir / "quest_plan.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "title_quest": "Проверка ключа",
                            "quest_number": 1,
                            "character": "Домовед",
                            "description": "Стартовый текст.",
                            "congratulation": "Финальный текст.",
                            "task_numbers": [1, 2],
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "task_template_id": "TT-001",
                                    "task_template_name": "Диалог",
                                    "task_type": "action dialog",
                                },
                                {
                                    "task_number": 2,
                                    "task_template_id": "TT-020",
                                    "task_template_name": "Уборка конкретного мусора в гостях",
                                    "task_type": "garbage classname in_guest",
                                },
                            ],
                        }
                    ]
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "3", campaigns_dir)
            original_review = review_path.read_text(encoding="utf-8")
            self.assertIn("## Справочник Task Templates", original_review)
            self.assertIn("TT-001 Диалог", original_review)
            self.assertIn("TT-035 Следы с ресурсами", original_review)
            self.assertNotIn("`TT-001`", original_review)
            self.assertNotIn("not_ready, не выбирать", original_review)
            self.assertLess(original_review.index("## Справочник Task Templates"), original_review.index("## Квесты"))
            review_text = review_path.read_text(encoding="utf-8").replace(
                "TT-020 Уборка конкретного мусора в гостях",
                "TT-004 HOG на локации",
            )
            review_path.write_text(review_text, encoding="utf-8")

            target = review_docs.apply_review_doc("Event_2026", "pack_001", "3", campaigns_dir)

            result = target.read_text(encoding="utf-8")
            self.assertIn("Task template ID: TT-001 / TT-004", result)
            self.assertIn("Task type: action dialog / HOG clean_debris location", result)

    def test_stage4_review_updates_task_choices(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            write_json(
                pack_dir / "filled_tasks.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "title_quest": "Проверка",
                            "quest_number": 1,
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "task_template_id": "TT-001",
                                    "task_template_name": "Диалог",
                                    "dialogue_replica": "Старая реплика.",
                                }
                            ],
                        }
                    ]
                },
            )
            write_json(
                pack_dir / "task_choices.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "tasks": [{"task_number": 1, "dialogue_replica": "Старая реплика."}],
                        }
                    ]
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "4", campaigns_dir)
            review_path.write_text(
                review_path.read_text(encoding="utf-8").replace("Старая реплика.", "Новая реплика."),
                encoding="utf-8",
            )

            target = review_docs.apply_review_doc("Event_2026", "pack_001", "4", campaigns_dir)

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["quests"][0]["tasks"][0]["dialogue_replica"], "Новая реплика.")

    def test_stage4_review_uses_readable_candidate_choices(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            task = {
                "task_number": 1,
                "task_template_id": "TT-011",
                "task_template_name": "Получить элемент коллекции (зависит от редкости)",
                "candidates": [
                    {
                        "candidate_id": "collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home",
                        "collection_classname": "GarbageCupCoffeeCollection5",
                        "collection_title": "Турка",
                    },
                    {
                        "candidate_id": "collection_drop:OldCameraCollection5:OldCamera:home",
                        "collection_classname": "OldCameraCollection5",
                        "collection_title": "Линза",
                    },
                ],
            }
            write_json(
                pack_dir / "context_pack.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "title_quest": "Проверка",
                            "quest_number": 1,
                            "tasks": [task],
                        }
                    ]
                },
            )
            write_json(
                pack_dir / "filled_tasks.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "title_quest": "Проверка",
                            "quest_number": 1,
                            "tasks": [task],
                        }
                    ]
                },
            )
            write_json(
                pack_dir / "task_choices.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "selected_candidate_id": "collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home",
                                    "choice_reason": "Старое обоснование.",
                                }
                            ],
                        }
                    ]
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "4", campaigns_dir)
            review = review_path.read_text(encoding="utf-8")
            self.assertIn("В тексте задания: Турку", review)
            self.assertIn("Выбранный кандидат: Турка.GarbageCupCoffeeCollection5", review)
            self.assertIn("Кандидаты:\nТурка.GarbageCupCoffeeCollection5\nЛинза.OldCameraCollection5", review)
            self.assertNotIn("Обоснование:", review)
            review_path.write_text(
                review.replace(
                    "Выбранный кандидат: Турка.GarbageCupCoffeeCollection5",
                    "Выбранный кандидат: Линза.OldCameraCollection5",
                ),
                encoding="utf-8",
            )

            target = review_docs.apply_review_doc("Event_2026", "pack_001", "4", campaigns_dir)

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(
                data["quests"][0]["tasks"][0]["selected_candidate_id"],
                "collection_drop:OldCameraCollection5:OldCamera:home",
            )
            self.assertEqual(data["quests"][0]["tasks"][0]["item_title_accusative"], "Линзу")

    def test_stage4_review_applies_item_from_subject_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            write_json(
                pack_dir / "context_pack.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "title_quest": "Проверка",
                            "quest_number": 1,
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "task_template_id": "TT-008",
                                    "task_template_name": "Получить ASK",
                                }
                            ],
                        }
                    ]
                },
            )
            write_json(
                pack_dir / "filled_tasks.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "title_quest": "Проверка",
                            "quest_number": 1,
                            "tasks": [
                                {
                                    "task_number": 1,
                                    "task_template_id": "TT-008",
                                    "task_template_name": "Получить ASK",
                                }
                            ],
                        }
                    ]
                },
            )
            write_json(
                pack_dir / "task_choices.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "tasks": [{"task_number": 1, "item_title": "мерную ложечку"}],
                        }
                    ]
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "4", campaigns_dir)
            review = review_path.read_text(encoding="utf-8")
            self.assertIn("Название: Мерная ложечка", review)
            self.assertIn("Предмет: Мерная ложечка", review)
            self.assertIn("В тексте задания: Мерную ложечку", review)
            review_path.write_text(
                review.replace("Предмет: Мерная ложечка", "Предмет: Половник главного повара"),
                encoding="utf-8",
            )

            target = review_docs.apply_review_doc("Event_2026", "pack_001", "4", campaigns_dir)

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["quests"][0]["tasks"][0]["item_title"], "Половник повара")
            self.assertEqual(data["quests"][0]["tasks"][0]["item_title_nominative"], "Половник главного повара")
            self.assertEqual(data["quests"][0]["tasks"][0]["item_title_accusative"], "Половник главного повара")

    def test_stage4_review_adds_hog_location_tags_reference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "stage2_story.txt").write_text(
                """
1. Домовед: Проверка
Суть: Домовед расставил реквизит и просит выбрать, что действительно нужно для сцены.
Старт: Домовед зовёт домовёнка к реквизиту.
Завершение: Реквизит разложен по местам.
""".strip(),
                encoding="utf-8",
            )
            quest = {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Проверка",
                "quest_number": 1,
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-005",
                        "task_template_name": "HOG в локациях дома",
                    }
                ],
            }
            write_json(pack_dir / "context_pack.json", {"quests": [quest]})
            write_json(pack_dir / "filled_tasks.json", {"quests": [quest]})
            write_json(
                pack_dir / "task_choices.json",
                {
                    "quests": [
                        {
                            "classname_quests": "Event_2026_Story_1",
                            "tasks": [{"task_number": 1, "item_title": "микрофон Русалки"}],
                        }
                    ]
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "4", campaigns_dir)

            review = review_path.read_text(encoding="utf-8")
            self.assertIn(
                "### 1. Проверка\nСуть: Домовед расставил реквизит и просит выбрать, что действительно нужно для сцены.\n\n#### 1.1. HOG в локациях дома",
                review,
            )
            self.assertIn("Тэги локаций: rnd_old_home,rnd_new_home,rnd_big_home", review)
            self.assertIn("Стандартные кандидаты:", review)
            self.assertIn("HOG в локациях дома - rnd_old_home,rnd_new_home,rnd_big_home", review)
            self.assertIn("HOG в мире - rnd_world", review)
            self.assertIn("HOG на даче - farm_room", review)

    def test_stage5_review_reads_wrapped_quest_group_choices(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            write_json(
                pack_dir / "quest_group_choices.json",
                {
                    "quest_group": {
                        "title": "Жених из чащи",
                        "description": "Описание выпуска.",
                        "description_complete": "Выпуск завершён.",
                        "description_spoil": "Закулисье ждёт помощи.",
                    }
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "5", campaigns_dir)

            review = review_path.read_text(encoding="utf-8")
            self.assertIn("Название: Жених из чащи", review)
            self.assertIn("Описание: Описание выпуска.", review)
            self.assertIn("Успех: Выпуск завершён.", review)
            self.assertIn("Провал: Закулисье ждёт помощи.", review)

    def test_stage5_review_updates_quest_group_choices(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            campaigns_dir = Path(tmp)
            pack_dir = campaigns_dir / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            write_json(
                pack_dir / "quest_group_choices.json",
                {
                    "title": "Старое название",
                    "description": "Описание.",
                    "description_complete": "Успех.",
                    "description_spoil": "Провал.",
                },
            )

            review_path = review_docs.write_review_doc("Event_2026", "pack_001", "5", campaigns_dir)
            review_path.write_text(
                review_path.read_text(encoding="utf-8").replace("Старое название", "Новое название"),
                encoding="utf-8",
            )

            target = review_docs.apply_review_doc("Event_2026", "pack_001", "5", campaigns_dir)

            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(data["title"], "Новое название")


if __name__ == "__main__":
    unittest.main()
