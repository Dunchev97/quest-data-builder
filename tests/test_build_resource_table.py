import json
import tempfile
import unittest
from pathlib import Path

from src.build_resource_table import Resource, build_resource_table, build_rows, write_csv
from src.interactive_objects import InteractiveIngredient


class BuildResourceTableTests(unittest.TestCase):
    def test_recipe_interactive_ingredients_rotate_by_craft_order(self):
        resources = []
        for quest_index in range(1, 4):
            quest = f"Event_2026_Story_{quest_index}"
            resources.extend(
                [
                    Resource("ASK", f"Event_2026_ASK_{quest_index}", "Ask", "pack_001", quest, 1, "get_asset ASK", "", 1, "", None),
                    Resource("GR", f"Event_2026_GR_{quest_index}", "Gr", "pack_001", quest, 2, "get_asset GR", "", 1, "", None),
                    Resource("R", f"Event_2026_R_{quest_index}", "Craft", "pack_001", quest, 3, "get_and_decrease_asset craft", "", 1, "", None),
                ]
            )
        interactive = [
            InteractiveIngredient("chest_1", "Event_2026_Chest_1_R_1", "Chest 1", "Chest_1"),
            InteractiveIngredient("help_1", "Event_2026_HELP_1_R_Opener", "Help 1", "HELP_1"),
            InteractiveIngredient("chest_1", "Event_2026_Chest_2_R_1", "Chest 2", "Chest_2"),
        ]

        rows, warnings = build_rows("Event_2026", [], resources, interactive)

        self.assertEqual(warnings, [])
        flat_rows = [";".join(str(cell) for cell in row) for row in rows]
        self.assertTrue(any("asset=Event_2026_Chest_1_R_1:1+asset=Event_2026_HELP_1_R_Opener:1" in row for row in flat_rows))
        self.assertTrue(any("asset=Event_2026_Chest_2_R_1:1+asset=Event_2026_Chest_1_R_1:1" in row for row in flat_rows))
        self.assertTrue(any("asset=Event_2026_HELP_1_R_Opener:1+asset=Event_2026_Chest_2_R_1:1" in row for row in flat_rows))

    def test_recipe_uses_resource_tasks_after_craft_when_craft_is_first(self):
        quest = "Event_2026_Story_1"
        resources = [
            Resource("R", "Event_2026_R_1", "Craft", "pack_001", quest, 1, "get_and_decrease_asset craft", "", 1, "", None),
            Resource("ASK", "Event_2026_ASK_1", "Ask", "pack_001", quest, 2, "get_asset ASK", "", 1, "", None),
            Resource("GR", "Event_2026_GR_1", "Gr", "pack_001", quest, 3, "get_asset GR", "", 1, "", None),
        ]
        interactive = [
            InteractiveIngredient("chest_1", "Event_2026_Chest_1_R_1", "Chest 1", "Chest_1"),
            InteractiveIngredient("help_1", "Event_2026_HELP_1_R_Opener", "Help 1", "HELP_1"),
        ]

        rows, warnings = build_rows("Event_2026", [], resources, interactive)

        self.assertEqual(warnings, [])
        flat_rows = [";".join(str(cell) for cell in row) for row in rows]
        self.assertTrue(any("Event_2026_R_1_Recipe" in row for row in flat_rows))
        self.assertTrue(
            any(
                "asset=Event_2026_ASK_1:1+asset=Event_2026_GR_1:1+asset=Event_2026_Chest_1_R_1:1+asset=Event_2026_HELP_1_R_Opener:1" in row
                for row in flat_rows
            )
        )

    def test_builds_campaign_resource_table_blocks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pack_dir = root / "campaigns" / "Event_2026" / "pack_001"
            pack_dir.mkdir(parents=True)
            (pack_dir / "filled_tasks.json").write_text(
                json.dumps(
                    {
                        "quests": [
                            {
                                "classname_quests": "Event_2026_Story_1",
                                "tasks": [
                                    {
                                        "task_number": 1,
                                        "task_type": "HOG clean_debris location",
                                        "resource_title": "Синяя лента",
                                        "task_object": {
                                            "type": "action",
                                            "param": "Event_2026_HOG_1",
                                            "title": "Найди синюю ленту",
                                        },
                                    },
                                    {
                                        "task_number": 2,
                                        "task_type": "get_asset ASK",
                                        "resource_title": "Занавеска",
                                        "task_object": {
                                            "type": "get_asset",
                                            "classname": "Event_2026_ASK_1",
                                            "title": "Попроси у друзей Занавеску",
                                            "amount": 1,
                                        },
                                    },
                                    {
                                        "task_number": 3,
                                        "task_type": "get_asset GR in_guest flower",
                                        "selected_candidate_id": "flower:FlowerOne",
                                        "task_object": {
                                            "type": "get_asset",
                                            "classname": "Event_2026_GR_1",
                                            "title": "Получи парадную ленту",
                                            "hint": "Собирай цветы Ромашки в гостях, чтобы найти.",
                                            "amount": 1,
                                        },
                                    },
                                    {
                                        "task_number": 4,
                                        "task_type": "get_and_decrease_asset craft",
                                        "task_object": {
                                            "type": "get_and_decrease_asset",
                                            "classname": "Event_2026_R_1",
                                            "title": "Создай Парадный барабан",
                                            "hint": "Для создания используй Станок.",
                                            "amount": 1,
                                        },
                                    },
                                ],
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (pack_dir / "context_pack.json").write_text(
                json.dumps(
                    {
                        "quests": [
                            {
                                "tasks": [
                                    {
                                        "candidates": [
                                            {
                                                "candidate_id": "flower:FlowerOne",
                                                "domain": "flower",
                                                "flower_classname": "FlowerOne",
                                                "flower_title": "Ромашки",
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            (root / "campaigns" / "Event_2026" / "interactive_objects.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "selected_objects": [
                            {
                                "template_id": "chest_1",
                                "object_title": "Запертый сундук",
                                "activation_resource_title": "Отмычки",
                                "result_resource_title": "Реликвия Камелота",
                            },
                            {
                                "template_id": "help_1",
                                "object_title": "Рыцарский факел",
                                "activation_resource_title": "Священное масло",
                                "path_resource_title": "Искра доблести",
                                "result_resource_title": "Пламя доблести",
                            },
                        ],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            rows, summary = build_resource_table("Event_2026", campaigns_dir=root / "campaigns")

            self.assertEqual(summary["warnings"], [])
            self.assertIn("HOG", summary["blocks"])
            self.assertIn("GR ассет", summary["blocks"])
            self.assertIn("ASK", summary["blocks"])
            self.assertIn("R ассет", summary["blocks"])
            self.assertIn("Рецепты 4 ингридиента", summary["blocks"])
            ask_header_index = next(index for index, row in enumerate(rows) if row and row[1] == "ASK")
            recipe_data_index = next(index for index, row in enumerate(rows) if "Event_2026_R_1_Recipe" in row)
            recipe_header_index = recipe_data_index - 3
            self.assertEqual([len(row) for row in rows[ask_header_index : ask_header_index + 4]], [10, 10, 10, 10])
            self.assertEqual([len(row) for row in rows[recipe_header_index : recipe_header_index + 4]], [19, 19, 19, 19])

            flat_rows = [";".join(str(cell) for cell in row) for row in rows]
            self.assertTrue(any("Синяя лента" in row for row in flat_rows))
            self.assertTrue(any("Занавеска" in row for row in flat_rows))
            self.assertTrue(any("active_quest=Event_2026_Story_1+asset!=Event_2026_R_1:1" in row for row in flat_rows))
            self.assertTrue(any("asset=Event_2026_ASK_1:1+asset=Event_2026_GR_1:1+asset=Event_2026_Chest_1_R_1:1+asset=Event_2026_HELP_1_R_Opener:1" in row for row in flat_rows))

            output_csv = root / "resource_table.csv"
            write_csv(output_csv, rows)
            self.assertIn("GR ассет", output_csv.read_text(encoding="cp1251"))


if __name__ == "__main__":
    unittest.main()
