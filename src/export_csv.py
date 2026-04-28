from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "filled_tasks.json"
DEFAULT_VALIDATION_PATH = PROJECT_ROOT / "output" / "filled_tasks.validation.json"
DEFAULT_OUTPUT_CSV_PATH = PROJECT_ROOT / "output" / "generated_quests.csv"

CSV_WIDTH = 28
DIALOGUE_TEMPLATE_IDS = {"TT-001"}
DIALOGUE_REPLICA_KEYS = ("dialogue_replica", "dialogue", "replica", "dialogue_text")
DIALOGUE_HEADER_PREFIX = "РЕПЛИКА ДИАЛОГА: "


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pad_row(values: list[Any], width: int = CSV_WIDTH) -> list[Any]:
    row = [csv_value(value) for value in values]
    if len(row) < width:
        row.extend([""] * (width - len(row)))
    return row


def csv_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def flatten_task(task_object: dict[str, Any]) -> list[tuple[str, Any]]:
    rows: list[tuple[str, Any]] = []
    for key, value in task_object.items():
        if key in DIALOGUE_REPLICA_KEYS:
            continue
        rows.append((key, csv_value(value)))
    if "identifier" not in task_object:
        rows.append(("identifier", ""))
    return rows


def blank_row() -> list[Any]:
    return pad_row([])


def quest_classname(quest: dict[str, Any]) -> str:
    return str(quest.get("classname_quests") or quest.get("classname") or "Quest")


def quest_prefix(classname: str) -> str:
    marker = "_Story_"
    if marker in classname:
        return classname.split(marker, 1)[0]
    return classname


def make_proto_path(quest: dict[str, Any]) -> str:
    if quest.get("proto_path"):
        return str(quest["proto_path"])
    classname = quest_classname(quest)
    prefix = quest_prefix(classname)
    quest_number = quest.get("quest_number") or 1
    return f"/quest/generated/{prefix}/story_{quest_number}/{classname}.proto.js"


def task_object_from_entry(task_entry: dict[str, Any]) -> dict[str, Any]:
    task_object = task_entry.get("task_object")
    if isinstance(task_object, dict):
        return task_object
    return task_entry


def quest_label(quest: dict[str, Any], quest_index: int) -> str:
    quest_number = quest.get("quest_number") or quest_index + 1
    return f"Квест {quest_number}"


def quest_title(quest: dict[str, Any]) -> str:
    return str(quest.get("title_quest") or quest.get("title") or "")


def quest_description(quest: dict[str, Any]) -> str:
    return str(quest.get("description") or "")


def quest_congratulation(quest: dict[str, Any]) -> str:
    return str(quest.get("congratulation") or "")


def explicit_quest_helper(quest: dict[str, Any]) -> str:
    for field_name in ("helper", "quest_helper", "character_classname"):
        value = quest.get(field_name)
        if value:
            return str(value)

    extra = quest.get("extra")
    if isinstance(extra, dict) and extra.get("helper"):
        return str(extra["helper"])

    character = quest.get("Character", quest.get("character"))
    if isinstance(character, str) and "_" in character and " " not in character.strip():
        return character
    return ""


def task_character_classname(task_entry: dict[str, Any]) -> str:
    task_object = task_object_from_entry(task_entry)
    go_to_location = task_object.get("go_to_location")
    if isinstance(go_to_location, list):
        for item in go_to_location:
            if isinstance(item, dict):
                classname = item.get("classname")
                if isinstance(classname, str) and "Character" in classname:
                    return classname

    for field_name in ("icon", "param", "action"):
        value = task_object.get(field_name)
        if isinstance(value, str) and "Character" in value:
            if field_name == "action" and "_Dialog_" in value:
                return value.split("_Dialog_", 1)[0]
            return value
    return ""


def quest_helper(quest: dict[str, Any]) -> str:
    explicit = explicit_quest_helper(quest)
    if explicit:
        return explicit
    for task_entry in quest.get("tasks", []):
        classname = task_character_classname(task_entry)
        if classname:
            return classname
    return ""


def explicit_sequence_icon(quest: dict[str, Any]) -> str:
    for field_name in ("extra.sequence_icon", "sequence_icon", "quest_sequence_icon"):
        value = quest.get(field_name)
        if value:
            return str(value)

    extra = quest.get("extra")
    if isinstance(extra, dict) and extra.get("sequence_icon"):
        return str(extra["sequence_icon"])
    return ""


def sequence_icon_base(classname: str) -> str:
    parts = classname.split("_Story_")
    if len(parts) != 2:
        return classname

    prefix, suffix = parts
    numbers = suffix.split("_")
    if len(numbers) >= 2 and all(part.isdigit() for part in numbers[:2]):
        return f"{prefix}_Story_{numbers[0]}"
    if numbers and numbers[0].isdigit():
        return prefix
    return classname


def quest_sequence_icon(quest: dict[str, Any]) -> str:
    explicit = explicit_sequence_icon(quest)
    if explicit:
        return explicit

    classname = quest_classname(quest)
    if not classname or classname == "Quest":
        return ""
    return f"MagazinePage_{sequence_icon_base(classname)}_QuestIcon_1"


def append_quest_block(rows: list[list[Any]], quest: dict[str, Any], quest_index: int, proto_path: str) -> None:
    rows.append(pad_row(["", quest_label(quest, quest_index)]))
    rows.append(pad_row(["sl", "string", "string", "string", "string", "string", "string", "string"]))
    rows.append(
        pad_row(
            [
                "",
                "input",
                "output",
                "title",
                "description",
                "congratulation",
                "helper",
                "extra.sequence_icon",
            ]
        )
    )
    rows.append(
        pad_row(
            [
                "",
                proto_path,
                proto_path,
                quest_title(quest),
                quest_description(quest),
                quest_congratulation(quest),
                quest_helper(quest),
                quest_sequence_icon(quest),
            ]
        )
    )
    rows.append(blank_row())


def task_header_title(task_entry: dict[str, Any], task_object: dict[str, Any], local_index: int) -> str:
    return str(
        task_entry.get("task_template_name")
        or task_entry.get("task_type")
        or task_object.get("title")
        or f"Task {local_index + 1}"
    )


def task_label(task_entry: dict[str, Any], local_index: int) -> str:
    return f"Таск {local_index + 1}"


def is_dialogue_task(task_entry: dict[str, Any], task_object: dict[str, Any]) -> bool:
    template_id = str(task_entry.get("task_template_id") or "")
    template_name = str(task_entry.get("task_template_name") or "").lower()
    task_type = str(task_entry.get("task_type") or "").lower()
    action = str(task_object.get("action") or "").lower()
    return (
        template_id in DIALOGUE_TEMPLATE_IDS
        or template_name == "диалог"
        or "dialog" in task_type
        or "_dialog_" in action
    )


def dialogue_replica(task_entry: dict[str, Any], task_object: dict[str, Any]) -> str:
    for source in (task_entry, task_object):
        for key in DIALOGUE_REPLICA_KEYS:
            value = source.get(key)
            if value not in (None, ""):
                return str(value).strip()
    return ""


def dialogue_header_value(task_entry: dict[str, Any], task_object: dict[str, Any]) -> str:
    if not is_dialogue_task(task_entry, task_object):
        return ""
    replica = dialogue_replica(task_entry, task_object)
    if not replica:
        return ""
    if replica.startswith(DIALOGUE_HEADER_PREFIX.strip()):
        return replica
    return DIALOGUE_HEADER_PREFIX + replica


def task_header_row(task_entry: dict[str, Any], task_object: dict[str, Any], local_index: int) -> list[Any]:
    row = ["", task_label(task_entry, local_index), task_header_title(task_entry, task_object, local_index)]
    replica = dialogue_header_value(task_entry, task_object)
    if replica:
        row.extend(["", "", replica])
    return row


def iter_csv_rows(quests: list[dict[str, Any]]) -> list[list[Any]]:
    rows: list[list[Any]] = []
    for quest_index, quest in enumerate(quests):
        proto_path = make_proto_path(quest)
        append_quest_block(rows, quest, quest_index, proto_path)
        for local_index, task_entry in enumerate(quest.get("tasks", [])):
            task_object = task_object_from_entry(task_entry)
            rows.append(pad_row(task_header_row(task_entry, task_object, local_index)))
            rows.append(pad_row(["ml", "string", "string", "object"]))
            rows.append(pad_row(["", "input", "output", f"tasks.{local_index}"]))

            fields = flatten_task(task_object)
            if not fields:
                rows.append(blank_row())
                continue

            first_key, first_value = fields[0]
            rows.append(pad_row(["", proto_path, proto_path, first_key, first_value]))
            for key, value in fields[1:]:
                rows.append(pad_row(["", "", "", key, value]))
            rows.append(blank_row())
    return rows


def write_csv_rows(rows: list[list[Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";", lineterminator="\n")
        writer.writerows(rows)


def export_filled_tasks_to_csv(filled_tasks: dict[str, Any], output_path: Path) -> dict[str, int]:
    quests = filled_tasks.get("quests", [])
    rows = iter_csv_rows(quests)
    write_csv_rows(rows, output_path)
    return {
        "quests_found": len(quests),
        "quest_blocks_exported": len(quests),
        "tasks_exported": sum(len(quest.get("tasks", [])) for quest in quests),
        "rows_written": len(rows),
    }


def export_quests_to_csv(quests: list[dict[str, Any]], output_path: Path) -> None:
    """Compatibility wrapper for the older prototype filler."""
    export_filled_tasks_to_csv({"quests": quests}, output_path)


def ensure_validation_passed(input_path: Path, validation_path: Path, allow_stale: bool = False) -> dict[str, Any]:
    if not validation_path.exists():
        raise ValueError(
            f"validation file not found: {validation_path}. "
            "Сначала запусти: python src/validate_task_objects.py output/filled_tasks.json"
        )

    validation = read_json(validation_path)
    summary = validation.get("summary", {})
    errors = int(summary.get("errors", 0) or 0)
    if errors:
        raise ValueError(
            f"validation has errors: {errors}. "
            "CSV не создан, нужно исправить этап 4."
        )

    if not allow_stale and validation_path.stat().st_mtime < input_path.stat().st_mtime:
        raise ValueError(
            "validation file is older than filled_tasks.json. "
            "Сначала заново запусти: python src/validate_task_objects.py output/filled_tasks.json"
        )

    return validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export validated stage 4 task objects to CSV.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Validated filled tasks JSON. Default: output/filled_tasks.json",
    )
    parser.add_argument(
        "--validation-json",
        type=Path,
        default=DEFAULT_VALIDATION_PATH,
        help="Validation JSON produced by validate_task_objects.py.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=DEFAULT_OUTPUT_CSV_PATH,
        help="CSV output path. Default: output/generated_quests.csv",
    )
    parser.add_argument(
        "--allow-stale-validation",
        action="store_true",
        help="Allow validation JSON older than input. Use only for manual debugging.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        return 1

    try:
        ensure_validation_passed(args.input, args.validation_json, args.allow_stale_validation)
    except ValueError as exc:
        print(str(exc))
        return 2

    summary = export_filled_tasks_to_csv(read_json(args.input), args.output_csv)
    print(f"quests found: {summary['quests_found']}")
    print(f"quest blocks exported: {summary['quest_blocks_exported']}")
    print(f"tasks exported: {summary['tasks_exported']}")
    print(f"rows written: {summary['rows_written']}")
    print(f"csv written: {args.output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
