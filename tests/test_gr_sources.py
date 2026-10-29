import copy
import unittest

from src import build_filled_tasks, build_resource_table, review_docs, validate_task_objects


class GrSourcesTests(unittest.TestCase):
    def context(self, mode="home"):
        return {"quests": [{"classname_quests": "Event_2026_Story_1", "quest_number": 1,
                            "title_quest": "Крепления", "tasks": [{
                                "task_number": 1, "task_template_id": "TT-013",
                                "task_template_name": "GR с мусора в локации дома",
                                "task_type": "get_asset GR garbage location_tags",
                                "candidates": [{"candidate_id": f"gr_garbage:RustyNail:{mode}",
                                                "garbage_classname": "RustyNail", "garbage_title": "Ржавый гвоздь",
                                                "mode": mode, "locations": [{"code": "65", "title": "Котельная"}]}]}]}]}

    def choices(self, mode="home"):
        return {"quests": [{"classname_quests": "Event_2026_Story_1", "tasks": [{
            "task_number": 1, "item_title": "Железный крючок", "amount": 37, "price": 9,
            "selected_candidate_id": f"gr_garbage:RustyNail:{mode}"}]}]}

    def test_specific_source_resolves_template_hint_and_description_together(self):
        for mode, template, place, action in [("home", "TT-015", "дома", "clean_garbage"),
                                               ("guest", "TT-014", "в гостях", "clean_garbage_in_guest")]:
            with self.subTest(mode=mode):
                context = self.context(mode)
                result = build_filled_tasks.build_filled_tasks(context, self.choices(mode))
                task = result["quests"][0]["tasks"][0]
                expected = f"Убирай Ржавый гвоздь {place}, чтобы найти. Место поиска: Котельная."
                self.assertEqual(task["task_template_id"], template)
                self.assertEqual(task["requested_task_template_id"], "TT-013")
                self.assertEqual(task["task_object"]["hint"], expected)
                self.assertEqual(task["task_object"]["amount"], 37)
                self.assertEqual(task["task_object"]["price"], 9)
                self.assertEqual(context["quests"][0]["tasks"][0]["task_template_id"], "TT-013")
                candidate = context["quests"][0]["tasks"][0]["candidates"][0]
                resource = build_resource_table.Resource("GR", "Event_2026_GR_1", "Крючок", "pack_001",
                                                        "Event_2026_Story_1", 1, task["task_type"],
                                                        "Убирай мусор в локации Котельная дома, чтобы найти.",
                                                        37, candidate["candidate_id"], candidate)
                self.assertEqual(build_resource_table.gr_description(resource), expected)
                self.assertEqual(build_resource_table.gr_reward_action(resource)[0], action)
                self.assertEqual(build_resource_table.gr_assets(resource), "RustyNail")
                validation = validate_task_objects.validate_filled_tasks(result, context,
                    build_filled_tasks.build_template_catalog(build_filled_tasks.DEFAULT_TEMPLATES_PATH))
                self.assertEqual(validation["summary"]["errors"], 0, validation["errors"])
                stale = copy.deepcopy(result)
                stale["quests"][0]["tasks"][0]["task_object"]["hint"] = resource.hint
                validation = validate_task_objects.validate_filled_tasks(stale, context,
                    build_filled_tasks.build_template_catalog(build_filled_tasks.DEFAULT_TEMPLATES_PATH))
                self.assertIn("strict_template_text_mismatch", [e["code"] for e in validation["errors"]])

    def test_review_candidate_change_rebuilds_actual_source_text(self):
        context = self.context()
        context["quests"][0]["tasks"][0]["candidates"].append({
            "candidate_id": "gr_garbage:Chips:home", "garbage_classname": "Chips", "garbage_title": "Стружка",
            "mode": "home", "locations": [{"code": "1", "title": "Мастерская"}]})
        text = "## Квесты\n\n### 1. Крепления\n\n#### 1.1. GR\nНазвание: Крючок\nВыбранный кандидат: Стружка.Chips\n"
        choices = review_docs.parse_stage4_review(text, self.choices(), context)
        result = build_filled_tasks.build_filled_tasks(context, choices)
        self.assertEqual(result["quests"][0]["tasks"][0]["task_object"]["hint"],
                         "Убирай Стружку дома, чтобы найти. Место поиска: Мастерская.")


if __name__ == "__main__":
    unittest.main()
