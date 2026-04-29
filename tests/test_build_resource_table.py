import json
import tempfile
import unittest
from pathlib import Path

from src.build_resource_table import build_resource_table, write_csv


class BuildResourceTableTests(unittest.TestCase):
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
                                        "task_object": {
                                            "type": "action",
                                            "param": "Event_2026_HOG_1",
                                            "title": "Найди синюю ленту",
                                        },
                                    },
                                    {
                                        "task_number": 2,
                                        "task_type": "get_asset ASK",
                                        "task_object": {
                                            "type": "get_asset",
                                            "classname": "Event_2026_ASK_1",
                                            "title": "Попроси у друзей Барабанные палочки",
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
            self.assertTrue(any("active_quest=Event_2026_Story_1+asset!=Event_2026_R_1:1" in row for row in flat_rows))
            self.assertTrue(any("asset=Event_2026_ASK_1:1+asset=Event_2026_GR_1:1+asset=Event_2026_ASK_1:1+asset=Event_2026_GR_1:1" in row for row in flat_rows))

            output_csv = root / "resource_table.csv"
            write_csv(output_csv, rows)
            self.assertIn("GR ассет", output_csv.read_text(encoding="cp1251"))


if __name__ == "__main__":
    unittest.main()
