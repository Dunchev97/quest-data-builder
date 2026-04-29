from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "pot_description.json"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "pot_description.validation.json"
DEFAULT_PREVIEW_PATH = PROJECT_ROOT / "output" / "pot_description.preview.md"

POSTFIX_BY_TYPE = {
    "Обычный": "Выращивай в нём сразу 5 цветов!",
    "Волшебный": "Выращивай в нём сразу 5 волшебных цветов!",
    "Короб для овощей": "Выращивай в нём сразу 5 овощей!",
    "Грибница для грибов": "Выращивай в ней сразу 5 грибочков!",
}

TYPE_ALIASES = {
    "обычный": "Обычный",
    "подвесной": "Обычный",
    "мини": "Обычный",
    "мини горшок": "Обычный",
    "волшебный": "Волшебный",
    "магический": "Волшебный",
    "короб": "Короб для овощей",
    "короб для овощей": "Короб для овощей",
    "овощной короб": "Короб для овощей",
    "грибница": "Грибница для грибов",
    "грибница для грибов": "Грибница для грибов",
}

FORBIDDEN_MECHANIC_WORDS = (
    "бонус",
    "ускоряет",
    "увеличивает",
    "сокращает",
    "прибавляет",
    "повышает",
    "шанс",
    "урожайность",
    "опыт",
    "монет",
    "золота",
    "%",
    "+",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def issue(severity: str, code: str, message: str, **extra: Any) -> dict[str, Any]:
    item = {"severity": severity, "code": code, "message": message}
    item.update(extra)
    return item


def normalize_pot_type(value: Any) -> str:
    text = str(value or "").strip().lower().replace("ё", "е")
    return TYPE_ALIASES.get(text, str(value or "").strip())


def expected_postfix(pot_type: Any) -> str:
    return POSTFIX_BY_TYPE.get(normalize_pot_type(pot_type), "")


def validate_pot_description(data: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []

    pot_type = normalize_pot_type(data.get("pot_type"))
    title = str(data.get("title") or "").strip()
    description = str(data.get("description") or "").strip()
    postfix = str(data.get("postfix") or "").strip()
    final_text = str(data.get("final_text") or "").strip()

    if pot_type not in POSTFIX_BY_TYPE:
        issues.append(
            issue(
                "error",
                "unknown_pot_type",
                "pot_type must be one of the supported pot description types.",
                allowed=list(POSTFIX_BY_TYPE),
                actual=data.get("pot_type"),
            )
        )

    if not title:
        issues.append(issue("error", "missing_title", "title must be filled."))
    if not description:
        issues.append(issue("error", "missing_description", "description must be filled."))
    if len(description) > 420:
        issues.append(
            issue(
                "warning",
                "description_too_long",
                "description should be short enough for an item card.",
                limit=420,
                actual=len(description),
            )
        )

    expected = expected_postfix(pot_type)
    if expected and postfix != expected:
        issues.append(
            issue(
                "error",
                "postfix_mismatch",
                "postfix must exactly match pot_type.",
                expected=expected,
                actual=postfix,
            )
        )

    if expected and final_text and not final_text.endswith(expected):
        issues.append(
            issue(
                "error",
                "final_text_postfix_mismatch",
                "final_text must end with the exact postfix for pot_type.",
                expected_suffix=expected,
                actual=final_text,
            )
        )

    if final_text and description and description not in final_text:
        issues.append(
            issue(
                "warning",
                "final_text_missing_description",
                "final_text should include the description text plus postfix.",
            )
        )

    lower_text = f"{title} {description} {final_text}".lower().replace("ё", "е")
    forbidden = [word for word in FORBIDDEN_MECHANIC_WORDS if word in lower_text]
    if forbidden:
        issues.append(
            issue(
                "error",
                "forbidden_game_mechanics",
                "Do not invent gameplay bonuses, numeric effects, currencies, or mechanics from the image.",
                forbidden=forbidden,
            )
        )

    errors = [item for item in issues if item["severity"] == "error"]
    warnings = [item for item in issues if item["severity"] == "warning"]
    return {
        "summary": {
            "status": "ok" if not errors else "error",
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "normalized": {
            "pot_type": pot_type,
            "expected_postfix": expected,
        },
        "errors": errors,
        "warnings": warnings,
    }


def render_preview(data: dict[str, Any], validation: dict[str, Any]) -> str:
    summary = validation["summary"]
    lines = [
        "# Pot Description Validation",
        "",
        f"Status: {summary['status']}",
        f"Errors: {summary['errors']}",
        f"Warnings: {summary['warnings']}",
        "",
        f"- pot_type: {validation['normalized'].get('pot_type') or ''}",
        f"- title: {data.get('title') or ''}",
        f"- postfix: {data.get('postfix') or ''}",
        "",
    ]
    if data.get("final_text"):
        lines.extend(["## Final Text", "", str(data["final_text"]), ""])
    if validation["errors"]:
        lines.extend(["## Errors", ""])
        for item in validation["errors"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")
    if validation["warnings"]:
        lines.extend(["## Warnings", ""])
        for item in validation["warnings"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")
    return "\n".join(lines)


def validate_file(input_path: Path, output_json_path: Path, preview_path: Path) -> dict[str, Any]:
    data = read_json(input_path)
    if not isinstance(data, dict):
        raise ValueError("pot description input must be a JSON object.")
    validation = validate_pot_description(data)
    write_json(output_json_path, validation)
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(render_preview(data, validation), encoding="utf-8")
    return validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate pot description workflow output.")
    parser.add_argument("input", nargs="?", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON_PATH)
    parser.add_argument("--preview", type=Path, default=DEFAULT_PREVIEW_PATH)
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        return 1
    try:
        validation = validate_file(args.input, args.output_json, args.preview)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(str(exc))
        return 1

    summary = validation["summary"]
    print(f"status: {summary['status']}")
    print(f"errors: {summary['errors']}")
    print(f"warnings: {summary['warnings']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    return 0 if summary["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
