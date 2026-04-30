import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.build_quest_group import build_quest_group, build_quest_group_file, main, read_quest_group_choices, validate_quest_group


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def sample_filled_tasks() -> dict[str, object]:
    return {
        "quests": [
            {
                "classname_quests": "Fun14_Story_1_1",
                "title_quest": "Огуречный раскат",
                "description": "С неба падают соленья, и герои ищут причину.",
                "congratulation": "Облако усмирено, огурцы больше не гремят.",
                "tasks": [],
            },
            {
                "classname_quests": "Fun14_Story_1_2",
                "title_quest": "Помидорная осада",
                "description": "На огород наступает помидорная волна.",
                "congratulation": "Осада снята.",
                "tasks": [],
            },
        ]
    }


class BuildQuestGroupTests(unittest.TestCase):
    def test_builds_required_quest_group_fields(self) -> None:
        quest_group = build_quest_group(
            sample_filled_tasks(),
            title="Овощной переполох",
            description="Герои разбираются, почему на дом обрушился овощной дождь.",
            description_complete="Причина найдена, урожай спасен, а небо снова спокойно.",
            description_spoil="Овощной дождь не остановлен, и переполох продолжается.",
        )

        self.assertEqual(quest_group["input"], "/quest_group/fun/Fun13_Story_1.proto.js")
        self.assertEqual(quest_group["output"], "/quest_group/fun/Fun14_Story_1.proto.js")
        self.assertEqual(quest_group["extra"]["quest_reward_prewiew"], ["", "", ""])
        self.assertEqual(quest_group["extra"]["description_condition"], quest_group["description"])
        self.assertEqual(quest_group["extra"]["description_complete"], quest_group["description_complete"])
        self.assertEqual(validate_quest_group(quest_group)["summary"]["errors"], 0)

    def test_reports_invalid_reward_preview(self) -> None:
        quest_group = build_quest_group(
            sample_filled_tasks(),
            title="Овощной переполох",
            description="Завязка.",
            description_complete="Успех.",
            description_spoil="Провал.",
        )
        quest_group["extra"]["quest_reward_prewiew"] = ["Fun14_Story_1_1", "", ""]

        validation = validate_quest_group(quest_group)

        self.assertEqual(validation["summary"]["errors"], 1)
        self.assertEqual(validation["errors"][0]["code"], "quest_reward_prewiew_must_be_empty")

    def test_cli_writes_quest_group_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            output_path = root / "quest_group.json"
            validation_path = root / "quest_group.validation.json"
            preview_path = root / "quest_group.preview.md"
            write_json(input_path, sample_filled_tasks())

            exit_code = main(
                [
                    str(input_path),
                    "--output-json",
                    str(output_path),
                    "--validation-json",
                    str(validation_path),
                    "--preview",
                    str(preview_path),
                    "--title",
                    "Овощной переполох",
                    "--description",
                    "Герои разбираются с овощным дождем.",
                    "--description-complete",
                    "Овощной дождь остановлен.",
                    "--description-spoil",
                    "Овощной дождь продолжился.",
                    "--allow-unapproved-stage4",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(output_path.exists())
            self.assertTrue(validation_path.exists())
            self.assertTrue(preview_path.exists())

    def test_cli_can_read_quest_group_choices_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            choices_path = root / "quest_group_choices.json"
            output_path = root / "quest_group.json"
            validation_path = root / "quest_group.validation.json"
            preview_path = root / "quest_group.preview.md"
            write_json(input_path, sample_filled_tasks())
            write_json(
                choices_path,
                {
                    "title": "Овощной переполох",
                    "description": "Герои разбираются с овощным дождем.",
                    "description_complete": "Овощной дождь остановлен.",
                    "description_spoil": "Овощной дождь продолжился.",
                },
            )

            exit_code = main(
                [
                    str(input_path),
                    "--choices",
                    str(choices_path),
                    "--output-json",
                    str(output_path),
                    "--validation-json",
                    str(validation_path),
                    "--preview",
                    str(preview_path),
                    "--allow-unapproved-stage4",
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertEqual(read_quest_group_choices(choices_path)["title"], "Овощной переполох")
            quest_group = json.loads(output_path.read_text(encoding="utf-8"))
            self.assertEqual(quest_group["description_complete"], "Овощной дождь остановлен.")

    def test_file_builder_uses_campaign_and_pack_for_output_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "filled_tasks.json"
            output_path = root / "quest_group.json"
            validation_path = root / "quest_group.validation.json"
            preview_path = root / "quest_group.preview.md"
            write_json(input_path, sample_filled_tasks())

            quest_group, validation = build_quest_group_file(
                input_path=input_path,
                output_json_path=output_path,
                validation_path=validation_path,
                preview_path=preview_path,
                title="Овощной переполох",
                description="Вы отправляетесь вслед за овощным дождем.",
                description_complete="Вы нашли источник дождя и подготовили путь наверх.",
                description_spoil="В следующий раз стоит взять клубочек и крепкий зонт.",
                campaign_id="MeatballRain_2026",
                pack_id="pack_002",
            )

            self.assertEqual(validation["summary"]["errors"], 0)
            self.assertEqual(quest_group["output"], "/quest_group/fun/MeatballRain_2026_pack_002.proto.js")

    def test_cli_defaults_to_campaign_pack_outputs_when_campaign_pack_known(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            campaigns_dir = root / "campaigns"
            input_path = root / "filled_tasks.json"
            write_json(input_path, sample_filled_tasks())

            with patch("src.build_quest_group.DEFAULT_CAMPAIGNS_DIR", campaigns_dir):
                exit_code = main(
                    [
                        str(input_path),
                        "--campaign",
                        "Event_2026",
                        "--current-pack",
                        "pack_001",
                        "--title",
                        "Овощной переполох",
                        "--description",
                        "Вы отправляетесь вслед за овощным дождем.",
                        "--description-complete",
                        "Вы нашли источник дождя и подготовили путь наверх.",
                        "--description-spoil",
                        "В следующий раз стоит взять клубочек и крепкий зонт.",
                        "--allow-unapproved-stage4",
                    ]
                )

            pack_path = campaigns_dir / "Event_2026" / "pack_001"
            self.assertEqual(exit_code, 0)
            self.assertTrue((pack_path / "quest_group.json").exists())
            self.assertTrue((pack_path / "quest_group.validation.json").exists())
            self.assertTrue((pack_path / "quest_group.preview.md").exists())


if __name__ == "__main__":
    unittest.main()
