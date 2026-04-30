import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.campaigns import (
    copy_current_output_to_pack,
    create_campaign,
    create_pack,
    generated_sequence_offsets,
    generated_sequence_offsets_for_json,
    load_memory,
    pack_dir,
    update_memory_from_pack,
    rebuild_memory_from_packs,
)


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sample_context_pack() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-020",
                        "candidate_domain": "garbage",
                        "candidates": [
                            {
                                "candidate_id": "garbage:Ashes",
                                "domain": "garbage",
                                "garbage_classname": "Ashes",
                                "garbage_title": "Пепел",
                                "locations": [{"code": "loc1", "title": "Котельная"}],
                            }
                        ],
                    },
                    {
                        "task_number": 2,
                        "task_template_id": "TT-011",
                        "candidate_domain": "collection_drop",
                        "candidates": [
                            {
                                "candidate_id": "collection_drop:PlateCollection1:BrokenPlate:home",
                                "domain": "collection_drop",
                                "collection_classname": "PlateCollection1",
                                "collection_title": "Фарфоровый осколок",
                                "source_type": "garbage",
                                "source_classname": "BrokenPlate",
                                "source_title": "Разбитая тарелка",
                                "locations": [{"code": "loc1", "title": "Котельная"}],
                            }
                        ],
                    },
                ],
            }
        ]
    }


def sample_filled_tasks() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Event_2026_Story_1",
                "quest_number": 1,
                "tasks": [
                    {
                        "task_number": 1,
                        "task_template_id": "TT-020",
                        "task_template_name": "Уборка конкретного мусора в гостях",
                        "selected_candidate_id": "garbage:Ashes",
                        "task_object": {"type": "garbage", "classname": "Ashes", "title": "Убери Пепел"},
                    },
                    {
                        "task_number": 2,
                        "task_template_id": "TT-011",
                        "task_template_name": "Получить элемент коллекции",
                        "selected_candidate_id": "collection_drop:PlateCollection1:BrokenPlate:home",
                        "task_object": {
                            "type": "get_asset",
                            "classname": "PlateCollection1",
                            "icon": "PlateCollection1",
                            "title": "Найди Фарфоровый осколок",
                        },
                    },
                    {
                        "task_number": 3,
                        "task_template_id": "TT-008",
                        "task_template_name": "Получить ASK",
                        "selected_candidate_id": None,
                        "task_object": {
                            "type": "get_asset",
                            "classname": "Event_2026_ASK_1",
                            "icon": "Event_2026_ASK_1",
                            "title": "Попроси Крышку",
                        },
                    },
                ],
            }
        ]
    }


class CampaignTests(unittest.TestCase):
    def test_creates_campaign_and_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaign = create_campaign(
                "Event_2026",
                title="Тестовая кампания",
                tone="юмор",
                characters=["Домовед"],
                campaigns_dir=root,
            )
            pack = create_pack("Event_2026", title="Первый пак", campaigns_dir=root)

            self.assertEqual(campaign["campaign_id"], "Event_2026")
            self.assertEqual(pack["pack_id"], "pack_001")
            self.assertTrue((root / "Event_2026" / "campaign.json").exists())
            self.assertTrue((root / "Event_2026" / "campaign_memory.json").exists())
            self.assertTrue((root / "Event_2026" / "pack_001" / "pack.json").exists())

    def test_updates_memory_from_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_campaign("Event_2026", campaigns_dir=root)
            create_pack("Event_2026", campaigns_dir=root)
            target = pack_dir("Event_2026", "pack_001", root)
            write_json(target / "context_pack.json", sample_context_pack())
            write_json(target / "filled_tasks.json", sample_filled_tasks())
            write_json(target / "quest_group.json", {"title": "Проверочная группа"})
            write_json(target / "quest_group.validation.json", {"summary": {"errors": 0, "warnings": 0}})

            memory = update_memory_from_pack("Event_2026", "pack_001", root)

            self.assertIn("Ashes", memory["used_garbage"])
            self.assertIn("BrokenPlate", memory["used_garbage"])
            self.assertIn("PlateCollection1", memory["used_collections"])
            self.assertIn("Котельная", memory["used_locations"])
            self.assertIn("Event_2026_ASK_1", memory["used_generated_assets"])
            self.assertEqual(memory["packs"]["pack_001"]["tasks_found"], 3)
            self.assertEqual(memory["packs"]["pack_001"]["quest_group"], str(target / "quest_group.json"))

    def test_rebuild_memory_is_stable_when_pack_did_not_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_campaign("Event_2026", campaigns_dir=root)
            create_pack("Event_2026", campaigns_dir=root)
            target = pack_dir("Event_2026", "pack_001", root)
            write_json(target / "context_pack.json", sample_context_pack())
            write_json(target / "filled_tasks.json", sample_filled_tasks())

            first = update_memory_from_pack("Event_2026", "pack_001", root)
            second = update_memory_from_pack("Event_2026", "pack_001", root)

            self.assertEqual(second, first)

    def test_rebuild_memory_removes_replaced_entities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            create_campaign("Event_2026", campaigns_dir=root)
            create_pack("Event_2026", campaigns_dir=root)
            target = pack_dir("Event_2026", "pack_001", root)
            write_json(target / "context_pack.json", sample_context_pack())
            write_json(target / "filled_tasks.json", sample_filled_tasks())
            memory = update_memory_from_pack("Event_2026", "pack_001", root)
            self.assertIn("Ashes", memory["used_garbage"])

            context = sample_context_pack()
            context["quests"][0]["tasks"][0]["candidates"][0] = {
                "candidate_id": "garbage:BrokenPlate",
                "domain": "garbage",
                "garbage_classname": "BrokenPlate",
                "garbage_title": "Разбитая тарелка",
                "locations": [{"code": "loc1", "title": "Котельная"}],
            }
            filled = sample_filled_tasks()
            filled["quests"][0]["tasks"][0]["selected_candidate_id"] = "garbage:BrokenPlate"
            filled["quests"][0]["tasks"][0]["task_object"]["classname"] = "BrokenPlate"
            write_json(target / "context_pack.json", context)
            write_json(target / "filled_tasks.json", filled)

            rebuilt = rebuild_memory_from_packs("Event_2026", root)
            self.assertNotIn("Ashes", rebuilt["used_garbage"])
            self.assertIn("BrokenPlate", rebuilt["used_garbage"])

    def test_generated_sequence_offsets_are_campaign_wide(self) -> None:
        memory = {
            "used_generated_assets": {
                "Event_2026_HOG_1": {"pack_id": "pack_001"},
                "Event_2026_HOG_2": {"pack_id": "pack_001"},
                "Event_2026_GR_4": {"pack_id": "pack_002"},
                "Other_2026_ASK_3": {"pack_id": "pack_001"},
                "Event_2026_Character_1": {"pack_id": "pack_001"},
            }
        }

        offsets = generated_sequence_offsets(memory)
        self.assertEqual(offsets[("Event_2026", "HOG")], 2)
        self.assertEqual(offsets[("Event_2026", "GR")], 4)
        self.assertEqual(offsets[("Other_2026", "ASK")], 3)
        self.assertNotIn(("Event_2026", "Character"), offsets)

        offsets_without_current_pack = generated_sequence_offsets_for_json(memory, current_pack_id="pack_002")
        self.assertEqual(offsets_without_current_pack["Event_2026"]["HOG"], 2)
        self.assertNotIn("GR", offsets_without_current_pack["Event_2026"])


if __name__ == "__main__":
    unittest.main()
