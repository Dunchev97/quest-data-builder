import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.parse_stage3 import build_quest_plan, main, parse_stage2_story_text, parse_stage3_text


ONE_QUEST = """
Classname quests: Event_2026_Story_1
title_quest: Первый переполох
№ quest: 1
№ task: 1 2 3
Task template ID: TT-020 / TT-011 / TT-019
Task template name: Уборка конкретного мусора в гостях / Получить элемент коллекции (зависит от редкости) / Сбор цветов в гостях
Task type: garbage classname in_guest / get_asset Collection / action take_crop_in_guest
description: "Нужно быстро привести дом в порядок."
Tasks:
[пусто]
congratulation: "Дом снова сияет!"
Character: Домовёнок
"""


TWO_QUESTS = ONE_QUEST + """

Classname quests: Event_2026_Story_2
title_quest: Второй переполох
№ quest: 2
№ task: 4 5 6
Task template ID: TT-021 / TT-014 / TT-011
Task template name: Уборка конкретного мусора дома / GR с конкретного мусора в гостях / Получить элемент коллекции (зависит от редкости)
Task type: garbage classname / get_asset GR in_guest garbage classname / get_asset Collection
description: "Пора искать материалы."
Tasks:
[пусто]
congratulation: "Материалы собраны!"
Character: Леший
"""


STAGE2_ONE_QUEST = """
ЭТАП 2: РЕПЛИКИ НАЧАЛА И ЗАВЕРШЕНИЯ

Домовёнок: Первый переполох
Суть задания: Дом нужно быстро привести в порядок.
Старт:
"Нужно быстро привести дом в порядок."
Завершение:
"Дом снова сияет!"
"""


STAGE2_ONE_QUEST_REVIEW_FORMAT = """
1. Домовёнок: Первый переполох
Суть: Дом нужно быстро привести в порядок.
Старт: "Нужно быстро привести дом в порядок."
Завершение: "Дом снова сияет!"
"""


STAGE2_ONE_QUEST_MISMATCH = """
ЭТАП 2: РЕПЛИКИ НАЧАЛА И ЗАВЕРШЕНИЯ

Домовёнок: Первый переполох
Суть задания: Дом нужно быстро привести в порядок.
Старт:
"Это другой старт."
Завершение:
"Это другое завершение."
"""


MISMATCHED_TASKS = """
Classname quests: Event_2026_Story_3
title_quest: Сломанный план
№ quest: 3
№ task: 7 8 9
Task template ID: TT-020 / TT-011
Task template name: Уборка конкретного мусора в гостях / Получить элемент коллекции (зависит от редкости) / Сбор цветов в гостях
Task type: garbage classname in_guest / get_asset Collection / action take_crop_in_guest
description: "Проверяем несовпадение."
Tasks:
[пусто]
congratulation: "Проверка завершена."
Character: Домовёнок
"""


NOT_READY_TEMPLATE = """
Classname quests: Event_2026_Story_4
title_quest: Не готовый шаблон
№ quest: 4
№ task: 10
Task template ID: TT-035
Task template name: Следы с ресурсами
Task type: not_ready
description: "Проверяем запрет."
Tasks:
[пусто]
congratulation: "Проверка завершена."
Character: Домовёнок
"""


CRAFT_LIKE_TOO_CLOSE = """
Classname quests: Event_2026_Story_1
title_quest: Первый крафт
№ quest: 1
№ task: 1 2 3
Task template ID: TT-002 / TT-008 / TT-014
Task template name: Крафт / Получить ASK / GR с конкретного мусора в гостях
Task type: get_and_decrease_asset craft / get_asset ASK / get_asset GR in_guest garbage classname
description: "Собираем первый предмет."
Tasks:
[пусто]
congratulation: "Первый предмет готов."
Character: Домовёнок

Classname quests: Event_2026_Story_3
title_quest: Передача рядом
№ quest: 3
№ task: 7 8 9
Task template ID: TT-033 / TT-013 / TT-008
Task template name: Передача предмета / GR с мусора в локации дома / Получить ASK
Task type: action give / get_asset GR garbage location_tags / get_asset ASK
description: "Слишком близко ставим передачу."
Tasks:
[пусто]
congratulation: "Проверка завершена."
Character: Домовёнок
"""


class ParseStage3Tests(unittest.TestCase):
    def test_parses_one_quest(self) -> None:
        quests = parse_stage3_text(ONE_QUEST)

        self.assertEqual(len(quests), 1)
        quest = quests[0]
        self.assertEqual(quest.classname_quests, "Event_2026_Story_1")
        self.assertEqual(quest.title_quest, "Первый переполох")
        self.assertEqual(quest.quest_number, 1)
        self.assertEqual(quest.task_numbers, [1, 2, 3])
        self.assertEqual(quest.task_template_ids, ["TT-020", "TT-011", "TT-019"])
        self.assertEqual(
            quest.task_template_names,
            [
                "Уборка конкретного мусора в гостях",
                "Получить элемент коллекции (зависит от редкости)",
                "Сбор цветов в гостях",
            ],
        )
        self.assertEqual(quest.character, "Домовёнок")
        self.assertIn("Нужно быстро", quest.description or "")
        self.assertIn("Дом снова", quest.congratulation or "")
        self.assertIn("Classname quests: Event_2026_Story_1", quest.raw_text)

    def test_parses_multiple_quests(self) -> None:
        quests = parse_stage3_text(TWO_QUESTS)

        self.assertEqual(len(quests), 2)
        self.assertEqual(quests[0].classname_quests, "Event_2026_Story_1")
        self.assertEqual(quests[1].classname_quests, "Event_2026_Story_2")
        self.assertEqual(quests[1].quest_number, 2)
        self.assertEqual(quests[1].character, "Леший")

    def test_splits_task_fields_by_slash(self) -> None:
        quest = parse_stage3_text(ONE_QUEST)[0]

        self.assertEqual(quest.task_template_ids, ["TT-020", "TT-011", "TT-019"])
        self.assertEqual(
            quest.task_types,
            [
                "garbage classname in_guest",
                "get_asset Collection",
                "action take_crop_in_guest",
            ],
        )

    def test_builds_quest_plan_with_summary(self) -> None:
        quest_plan = build_quest_plan(TWO_QUESTS)

        self.assertEqual(quest_plan["summary"]["quests_found"], 2)
        self.assertEqual(quest_plan["summary"]["tasks_found"], 6)
        self.assertEqual(quest_plan["summary"]["issues"], 0)
        self.assertEqual(quest_plan["quests"][0]["classname_quests"], "Event_2026_Story_1")
        self.assertEqual(
            quest_plan["quests"][0]["tasks"][0],
            {
                "task_number": 1,
                "task_template_id": "TT-020",
                "task_template_name": "Уборка конкретного мусора в гостях",
                "task_type": "garbage classname in_guest",
            },
        )

    def test_parses_stage2_start_and_finish_by_title(self) -> None:
        stage2_quests = parse_stage2_story_text(STAGE2_ONE_QUEST)

        self.assertIn("первый переполох", stage2_quests)
        self.assertEqual(stage2_quests["первый переполох"].start, "Нужно быстро привести дом в порядок.")
        self.assertEqual(stage2_quests["первый переполох"].finish, "Дом снова сияет!")

    def test_parses_stage2_review_format_start_and_finish(self) -> None:
        stage2_quests = parse_stage2_story_text(STAGE2_ONE_QUEST_REVIEW_FORMAT)

        self.assertIn("первый переполох", stage2_quests)
        self.assertEqual(stage2_quests["первый переполох"].start, "Нужно быстро привести дом в порядок.")
        self.assertEqual(stage2_quests["первый переполох"].finish, "Дом снова сияет!")

    def test_accepts_stage3_texts_copied_from_stage2(self) -> None:
        quest_plan = build_quest_plan(ONE_QUEST, stage2_text=STAGE2_ONE_QUEST)

        self.assertEqual(quest_plan["summary"]["issues"], 0)

    def test_reports_stage3_texts_not_copied_from_stage2(self) -> None:
        quest_plan = build_quest_plan(ONE_QUEST, stage2_text=STAGE2_ONE_QUEST_MISMATCH)

        self.assertEqual(quest_plan["summary"]["issues"], 2)
        self.assertEqual(
            [issue["code"] for issue in quest_plan["issues"]],
            ["description_not_from_stage2_start", "congratulation_not_from_stage2_finish"],
        )

    def test_reports_task_count_mismatch(self) -> None:
        quest_plan = build_quest_plan(MISMATCHED_TASKS)

        self.assertEqual(quest_plan["summary"]["issues"], 1)
        self.assertEqual(quest_plan["issues"][0]["code"], "task_count_mismatch")

    def test_reports_not_ready_template(self) -> None:
        quest_plan = build_quest_plan(NOT_READY_TEMPLATE)

        self.assertEqual(quest_plan["summary"]["issues"], 1)
        self.assertEqual(quest_plan["issues"][0]["code"], "not_ready_task_template")

    def test_reports_craft_like_templates_too_close(self) -> None:
        quest_plan = build_quest_plan(CRAFT_LIKE_TOO_CLOSE)

        self.assertEqual(quest_plan["summary"]["issues"], 1)
        self.assertEqual(quest_plan["issues"][0]["code"], "craft_like_tasks_too_close")
        self.assertEqual(quest_plan["issues"][0]["previous_task_template_id"], "TT-002")
        self.assertEqual(quest_plan["issues"][0]["task_template_id"], "TT-033")

    def test_cli_writes_json_and_preview(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "stage3_quests.txt"
            output_json = root / "quest_plan.json"
            preview = root / "quest_plan.preview.md"
            input_path.write_text(ONE_QUEST, encoding="utf-8")

            exit_code = main(
                [
                    str(input_path),
                    "--output-json",
                    str(output_json),
                    "--preview",
                    str(preview),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_json.exists())
            self.assertTrue(preview.exists())

            data = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["quests_found"], 1)
            self.assertEqual(data["summary"]["tasks_found"], 3)
            self.assertEqual(data["summary"]["issues"], 0)
            self.assertEqual(data["quests"][0]["tasks"][0]["task_template_id"], "TT-020")
            self.assertIn("Quest 1", preview.read_text(encoding="utf-8"))
            self.assertIn("TT-020", preview.read_text(encoding="utf-8"))

    def test_cli_validates_stage2_when_path_is_provided(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "stage3_quests.txt"
            stage2_path = root / "stage2_story.txt"
            output_json = root / "quest_plan.json"
            preview = root / "quest_plan.preview.md"
            input_path.write_text(ONE_QUEST, encoding="utf-8")
            stage2_path.write_text(STAGE2_ONE_QUEST_MISMATCH, encoding="utf-8")

            exit_code = main(
                [
                    str(input_path),
                    "--stage2",
                    str(stage2_path),
                    "--output-json",
                    str(output_json),
                    "--preview",
                    str(preview),
                ]
            )

            self.assertEqual(exit_code, 2)
            data = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(data["summary"]["issues"], 2)


if __name__ == "__main__":
    unittest.main()
