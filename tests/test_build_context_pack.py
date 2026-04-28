import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.build_context_pack import build_context_pack, build_context_pack_file


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sample_quest_ready_index() -> dict[str, object]:
    return {
        "quest_ready_locations": {
            "loc1": {
                "code": "loc1",
                "title": "Котельная",
                "tags": ["home", "boiler"],
                "garbage_assets": ["Ashes", "BrokenPlate", "CandyWrapper"],
            }
        },
        "quest_ready_garbage": {
            "Ashes": {"classname": "Ashes", "title": "Пепел", "id": 1},
            "BrokenPlate": {"classname": "BrokenPlate", "title": "Разбитая тарелка", "id": 2},
            "CandyWrapper": {"classname": "CandyWrapper", "title": "Фантик", "id": 3},
        },
        "quest_ready_flowers": {
            "FlowerSix": {"classname": "FlowerSix", "title": "Василек", "id": 4, "tags": ["blue"]},
            "FlowerSeven": {"classname": "FlowerSeven", "title": "Мак", "id": 5, "tags": ["red"]},
        },
        "quest_ready_collections": {},
    }


def sample_drops() -> list[dict[str, object]]:
    return [
        {
            "source_type": "garbage",
            "source_classname": "Ashes",
            "source_title": "Пепел",
            "collection_classname": "AshesCollection1",
            "collection_title": "Огненная саламандра",
            "mode": "guest",
            "locations": [{"code": "loc1", "title": "Котельная", "tags": ["home"]}],
        },
        {
            "source_type": "garbage",
            "source_classname": "BrokenPlate",
            "source_title": "Разбитая тарелка",
            "collection_classname": "PlateCollection1",
            "collection_title": "Фарфоровый осколок",
            "mode": "guest",
            "locations": [{"code": "loc1", "title": "Котельная", "tags": ["home"]}],
        },
    ]


def resolved_plan(tasks: list[dict[str, object]]) -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "title_quest": "Проверка кандидатов",
                "quest_number": 1,
                "description": "Нужно прибраться и найти детали.",
                "congratulation": "Все готово.",
                "character": "Домовенок",
                "tasks": tasks,
            }
        ],
        "issues": [],
        "summary": {"quests_found": 1, "tasks_found": len(tasks), "resolved_tasks": len(tasks), "issues": 0},
    }


def task(number: int, template_id: str, name: str, task_type: str, category: str) -> dict[str, object]:
    return {
        "task_number": number,
        "task_template_id": template_id,
        "task_template_name": name,
        "task_type": task_type,
        "resolved_template_id": template_id,
        "canonical_task_template_name": name,
        "canonical_task_type": task_type,
        "category": category,
        "data_needs": [],
        "status": "ok",
        "issues": [],
    }


class BuildContextPackTests(unittest.TestCase):
    def test_avoids_repeating_candidates_inside_pack(self) -> None:
        context_pack, emitted = build_context_pack(
            resolved_plan(
                [
                    task(1, "TT-020", "Уборка конкретного мусора в гостях", "garbage classname in_guest", "garbage"),
                    task(2, "TT-021", "Уборка конкретного мусора дома", "garbage classname", "garbage"),
                ]
            ),
            sample_quest_ready_index(),
            sample_drops(),
            {"version": 1, "candidate_counts": {}, "runs": []},
            candidate_limit=1,
        )

        tasks = context_pack["quests"][0]["tasks"]
        first = tasks[0]["candidates"][0]["candidate_id"]
        second = tasks[1]["candidates"][0]["candidate_id"]
        self.assertNotEqual(first, second)
        self.assertEqual(len(set(emitted)), 2)

    def test_history_rotates_candidates_between_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "quest_plan.resolved.json"
            index_path = root / "quest_ready_index.json"
            drops_path = root / "quest_ready_drops.index.json"
            history_path = root / "context_candidate_history.json"
            output_one = root / "context_pack_1.json"
            output_two = root / "context_pack_2.json"
            preview = root / "preview.md"
            write_json(
                input_path,
                resolved_plan(
                    [
                        task(
                            1,
                            "TT-020",
                            "Уборка конкретного мусора в гостях",
                            "garbage classname in_guest",
                            "garbage",
                        )
                    ]
                ),
            )
            write_json(index_path, sample_quest_ready_index())
            write_json(drops_path, sample_drops())

            first_pack = build_context_pack_file(
                input_path,
                index_path,
                drops_path,
                history_path,
                output_one,
                preview,
                candidate_limit=1,
            )
            second_pack = build_context_pack_file(
                input_path,
                index_path,
                drops_path,
                history_path,
                output_two,
                preview,
                candidate_limit=1,
            )

            first_candidate = first_pack["quests"][0]["tasks"][0]["candidates"][0]["candidate_id"]
            second_candidate = second_pack["quests"][0]["tasks"][0]["candidates"][0]["candidate_id"]
            self.assertNotEqual(first_candidate, second_candidate)
            self.assertTrue(history_path.exists())

    def test_builds_collection_and_flower_candidate_domains(self) -> None:
        context_pack, _emitted = build_context_pack(
            resolved_plan(
                [
                    task(
                        1,
                        "TT-011",
                        "Получить элемент коллекции (зависит от редкости)",
                        "get_asset Collection",
                        "collection",
                    ),
                    task(2, "TT-019", "Сбор цветов в гостях", "action take_crop_in_guest", "flower"),
                ]
            ),
            sample_quest_ready_index(),
            sample_drops(),
            {"version": 1, "candidate_counts": {}, "runs": []},
            candidate_limit=2,
        )

        tasks = context_pack["quests"][0]["tasks"]
        self.assertEqual(tasks[0]["candidate_domain"], "collection_drop")
        self.assertEqual(tasks[1]["candidate_domain"], "flower")
        self.assertIn("collection_classname", tasks[0]["candidates"][0])
        self.assertIn("flower_classname", tasks[1]["candidates"][0])

    def test_applies_manual_avoid_and_prefer_candidates(self) -> None:
        overridden_task = task(
            1,
            "TT-020",
            "Уборка конкретного мусора в гостях",
            "garbage classname in_guest",
            "garbage",
        )
        overridden_task["manual_override"] = {
            "avoid_candidates": ["garbage:Ashes"],
            "prefer_candidates": ["garbage:CandyWrapper"],
            "instruction": "Не используй пепел, лучше что-то легкое и бытовое.",
        }

        context_pack, _emitted = build_context_pack(
            resolved_plan([overridden_task]),
            sample_quest_ready_index(),
            sample_drops(),
            {"version": 1, "candidate_counts": {}, "runs": []},
            candidate_limit=2,
        )

        context_task = context_pack["quests"][0]["tasks"][0]
        candidate_ids = [candidate["candidate_id"] for candidate in context_task["candidates"]]
        self.assertNotIn("garbage:Ashes", candidate_ids)
        self.assertEqual(candidate_ids[0], "garbage:CandyWrapper")
        self.assertTrue(any("Manual instruction" in note for note in context_task["notes"]))

    def test_campaign_memory_filters_already_used_entities(self) -> None:
        context_pack, _emitted = build_context_pack(
            resolved_plan(
                [
                    task(1, "TT-020", "Уборка конкретного мусора в гостях", "garbage classname in_guest", "garbage"),
                    task(2, "TT-011", "Получить элемент коллекции (зависит от редкости)", "get_asset Collection", "collection"),
                ]
            ),
            sample_quest_ready_index(),
            sample_drops(),
            {"version": 1, "candidate_counts": {}, "runs": []},
            candidate_limit=1,
            campaign_memory={
                "used_garbage": {"Ashes": {"title": "Пепел"}},
                "used_collections": {},
                "used_flowers": {},
                "used_candidate_ids": {},
            },
        )

        tasks = context_pack["quests"][0]["tasks"]
        self.assertNotEqual(tasks[0]["candidates"][0]["garbage_classname"], "Ashes")
        self.assertNotEqual(tasks[1]["candidates"][0]["source_classname"], "Ashes")
        self.assertTrue(any("Campaign memory excluded" in note for note in tasks[0]["notes"]))

    def test_context_pack_reports_next_campaign_generated_numbers(self) -> None:
        context_pack, _emitted = build_context_pack(
            resolved_plan([task(1, "TT-008", "Получить ASK", "get_asset ASK", "request")]),
            sample_quest_ready_index(),
            sample_drops(),
            {"version": 1, "candidate_counts": {}, "runs": []},
            candidate_limit=1,
            campaign_memory={
                "used_generated_assets": {
                    "Event_2026_HOG_2": {"pack_id": "pack_001"},
                    "Event_2026_GR_5": {"pack_id": "pack_001"},
                    "Event_2026_ASK_1": {"pack_id": "pack_001"},
                    "Event_2026_R_1": {"pack_id": "pack_002"},
                }
            },
            current_pack_id="pack_002",
        )

        self.assertEqual(context_pack["generated_sequence_offsets"]["Event_2026"]["HOG"], 2)
        self.assertEqual(context_pack["next_generated_numbers"]["Event_2026"]["GR"], 6)
        self.assertEqual(context_pack["next_generated_numbers"]["Event_2026"]["ASK"], 2)
        self.assertNotIn("R", context_pack["generated_sequence_offsets"]["Event_2026"])


if __name__ == "__main__":
    unittest.main()
