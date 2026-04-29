import json
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.validate_pot_description import main, validate_pot_description


class ValidatePotDescriptionTests(unittest.TestCase):
    def test_accepts_valid_magic_pot_description(self) -> None:
        validation = validate_pot_description(
            {
                "pot_type": "Волшебный",
                "title": "Горшок Звёздная чаша",
                "description": "Синий горшок с золотым ободком выглядит так, будто его берегли для самых редких ростков.",
                "postfix": "Выращивай в нём сразу 5 волшебных цветов!",
                "final_text": "Синий горшок с золотым ободком выглядит так, будто его берегли для самых редких ростков. Выращивай в нём сразу 5 волшебных цветов!",
            }
        )

        self.assertEqual(validation["summary"]["errors"], 0)

    def test_accepts_hanging_as_regular_type_alias(self) -> None:
        validation = validate_pot_description(
            {
                "pot_type": "Подвесной",
                "title": "Подвесная Мечта хозяюшки",
                "description": "Аккуратный подвесной горшок подойдёт для уютного цветочного уголка.",
                "postfix": "Выращивай в нём сразу 5 цветов!",
                "final_text": "Аккуратный подвесной горшок подойдёт для уютного цветочного уголка. Выращивай в нём сразу 5 цветов!",
            }
        )

        self.assertEqual(validation["summary"]["errors"], 0)
        self.assertEqual(validation["normalized"]["pot_type"], "Обычный")

    def test_reports_wrong_postfix(self) -> None:
        validation = validate_pot_description(
            {
                "pot_type": "Грибница для грибов",
                "title": "Грибница Лесная",
                "description": "Небольшая грибница с мягким мхом выглядит как кусочек тихой поляны.",
                "postfix": "Выращивай в нём сразу 5 цветов!",
                "final_text": "Небольшая грибница с мягким мхом выглядит как кусочек тихой поляны. Выращивай в нём сразу 5 цветов!",
            }
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("postfix_mismatch", codes)

    def test_reports_invented_mechanics(self) -> None:
        validation = validate_pot_description(
            {
                "pot_type": "Короб для овощей",
                "title": "Короб Богатый урожай",
                "description": "Этот короб увеличивает урожайность на 20 процентов.",
                "postfix": "Выращивай в нём сразу 5 овощей!",
                "final_text": "Этот короб увеличивает урожайность на 20 процентов. Выращивай в нём сразу 5 овощей!",
            }
        )

        codes = [error["code"] for error in validation["errors"]]
        self.assertIn("forbidden_game_mechanics", codes)

    def test_cli_writes_validation_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_path = root / "pot_description.json"
            validation_path = root / "pot_description.validation.json"
            preview_path = root / "pot_description.preview.md"
            input_path.write_text(
                json.dumps(
                    {
                        "pot_type": "Обычный",
                        "title": "Горшок Берёзовый уют",
                        "description": "Светлый горшок с простым узором выглядит спокойно и по-домашнему.",
                        "postfix": "Выращивай в нём сразу 5 цветов!",
                        "final_text": "Светлый горшок с простым узором выглядит спокойно и по-домашнему. Выращивай в нём сразу 5 цветов!",
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            exit_code = main(
                [
                    str(input_path),
                    "--output-json",
                    str(validation_path),
                    "--preview",
                    str(preview_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue(validation_path.exists())
            self.assertTrue(preview_path.exists())


if __name__ == "__main__":
    unittest.main()
