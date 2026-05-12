import json
import tempfile
import unittest
from pathlib import Path

from src.interactive_objects import (
    build_interactive_objects_files,
    recipe_ingredients_from_manifest,
    validate_manifest,
)


def manifest() -> dict[str, object]:
    return {
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
    }


def duplicate_chest_manifest() -> dict[str, object]:
    return {
        "version": 1,
        "selected_objects": [
            {
                "template_id": "chest_1",
                "object_title": "First chest",
                "activation_resource_title": "First key",
                "result_resource_title": "First relic",
            },
            {
                "template_id": "chest_1",
                "object_title": "Second chest",
                "activation_resource_title": "Second key",
                "result_resource_title": "Second relic",
            },
        ],
    }


def friend_action_manifest() -> dict[str, object]:
    return {
        "version": 1,
        "selected_objects": [
            {
                "template_id": "chest_1",
                "object_title": "Запертый сундук",
                "activation_resource_title": "Отмычки",
                "result_resource_title": "Реликвия Камелота",
            },
            {
                "template_id": "friend_action_1",
                "available_title": "Флаг доступности броска одуванчиков",
                "action_title": "Бросок одуванчика",
                "reward_for_action_title": "Семена странствий",
                "reward_on_receive_title": "Цветы странствий",
                "action_start_time": "2026-03-04 15:00",
                "action_end_time": "2026-04-15 15:00",
            },
        ],
    }


class InteractiveObjectsTests(unittest.TestCase):
    def test_validates_minimum_selected_objects(self) -> None:
        validation = validate_manifest({"version": 1, "selected_objects": [{"template_id": "chest_1"}]})

        self.assertEqual(validation["summary"]["errors"], 1)
        self.assertEqual(validation["errors"][0]["code"], "not_enough_interactive_objects")

    def test_recipe_ingredients_use_selected_result_resources(self) -> None:
        ingredients, validation = recipe_ingredients_from_manifest("Event_2026", manifest())

        self.assertEqual(validation["summary"]["errors"], 0)
        self.assertEqual([item.classname for item in ingredients], ["Event_2026_Chest_1_R_1", "Event_2026_HELP_1_R_Opener"])
        self.assertEqual([item.amount for item in ingredients], [1, 1])

    def test_duplicate_object_templates_are_numbered(self) -> None:
        ingredients, validation = recipe_ingredients_from_manifest("Event_2026", duplicate_chest_manifest())

        self.assertEqual(validation["summary"]["errors"], 0)
        self.assertEqual([item.classname for item in ingredients], ["Event_2026_Chest_1_R_1", "Event_2026_Chest_2_R_1"])

    def test_friend_action_uses_receive_reward_as_recipe_resource(self) -> None:
        ingredients, validation = recipe_ingredients_from_manifest("Event_2026", friend_action_manifest())

        self.assertEqual(validation["summary"]["errors"], 0)
        self.assertEqual([item.classname for item in ingredients], ["Event_2026_Chest_1_R_1", "Event_2026_Story_FA_2"])
        self.assertEqual(ingredients[1].title, "Цветы странствий")

    def test_exports_interactive_csv_files_without_fun12_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "interactive_objects.json"
            manifest_path.write_text(json.dumps(manifest(), ensure_ascii=False), encoding="utf-8")

            summary = build_interactive_objects_files(
                campaign_id="Event_2026",
                pack_id="pack_001",
                manifest_path=manifest_path,
                output_dir=root,
                summary_path=root / "summary.json",
            )

            self.assertEqual(len(summary["files_written"]), 2)
            chest_csv = root / "generated_interactive_objects_chest_1.csv"
            help_csv = root / "generated_interactive_objects_help_1.csv"
            self.assertTrue(chest_csv.exists())
            self.assertTrue(help_csv.exists())
            combined = chest_csv.read_text(encoding="cp1251") + help_csv.read_text(encoding="cp1251")
            self.assertIn("Event_2026_Chest_1_R_1", combined)
            self.assertIn("Event_2026_HELP_1_R_Opener", combined)
            self.assertNotIn("/Fun12/", combined)

    def test_exports_friend_action_csv(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            manifest_path = root / "interactive_objects.json"
            manifest_path.write_text(json.dumps(friend_action_manifest(), ensure_ascii=False), encoding="utf-8")

            summary = build_interactive_objects_files(
                campaign_id="Event_2026",
                pack_id="pack_001",
                manifest_path=manifest_path,
                output_dir=root,
            )

            self.assertEqual(len(summary["files_written"]), 2)
            csv_path = root / "generated_interactive_objects_story_friendaction_1.csv"
            self.assertTrue(csv_path.exists())
            content = csv_path.read_text(encoding="cp1251")
            self.assertIn("Event_2026_Story_FriendAction_1", content)
            self.assertIn("asset=Event_2026_Story_FA_1:1", content)
            self.assertIn("asset=Event_2026_Story_FA_2:1", content)
            self.assertIn("stuff=Event_2026_Story_FriendAction_1_Available+time<2026-04-15 15:00", content)


if __name__ == "__main__":
    unittest.main()
