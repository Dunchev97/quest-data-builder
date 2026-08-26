from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

try:
    from .workflow_context import DEFAULT_CONTEXT_PATH, load_context, stage_approval_error
except ImportError:
    from workflow_context import DEFAULT_CONTEXT_PATH, load_context, stage_approval_error

try:
    from .campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir
except ImportError:
    from campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "filled_tasks.json"
DEFAULT_VALIDATION_PATH = PROJECT_ROOT / "output" / "filled_tasks.validation.json"
DEFAULT_QUEST_GROUP_PATH = PROJECT_ROOT / "output" / "quest_group.json"
DEFAULT_QUEST_GROUP_VALIDATION_PATH = PROJECT_ROOT / "output" / "quest_group.validation.json"
DEFAULT_OUTPUT_CSV_PATH = PROJECT_ROOT / "output" / "generated_quests.csv"
FILLED_TASKS_JSON_NAME = "filled_tasks.json"
FILLED_TASKS_VALIDATION_NAME = "filled_tasks.validation.json"
QUEST_GROUP_JSON_NAME = "quest_group.json"
QUEST_GROUP_VALIDATION_NAME = "quest_group.validation.json"
GENERATED_QUESTS_CSV_NAME = "generated_quests.csv"

CSV_WIDTH = 28
DIALOGUE_TEMPLATE_IDS = {"TT-001"}
DIALOGUE_REPLICA_KEYS = ("dialogue_replica", "dialogue", "replica", "dialogue_text")
DIALOGUE_HEADER_PREFIX = "РЕПЛИКА ДИАЛОГА: "
REQUIRED_APPROVAL_STAGE = "5"
QUEST_REFERENCE_CAMPAIGN_ID = "Night_2026"
QUEST_GROUP_REFERENCE_ID = 125028


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_campaign_pack(
    campaign_id: str | None,
    pack_id: str | None,
    context_path: Path = DEFAULT_CONTEXT_PATH,
) -> tuple[str | None, str | None]:
    if campaign_id and pack_id:
        return campaign_id, pack_id

    context = load_context(context_path)
    return campaign_id or context.get("campaign_id"), pack_id or context.get("pack_id")


def pack_artifact_path(campaign_id: str | None, pack_id: str | None, filename: str) -> Path | None:
    if not campaign_id or not pack_id:
        return None
    return pack_dir(campaign_id, pack_id, DEFAULT_CAMPAIGNS_DIR) / filename


def default_artifact_path(campaign_id: str | None, pack_id: str | None, filename: str, fallback: Path) -> Path:
    path = pack_artifact_path(campaign_id, pack_id, filename)
    return path if path is not None else fallback


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


def append_quest_group_block(rows: list[list[Any]], quest_group: dict[str, Any]) -> None:
    find = str(quest_group.get("find") or QUEST_REFERENCE_CAMPAIGN_ID)
    replace = str(quest_group.get("replace") or quest_prefix_from_group(quest_group))
    rows.append(pad_row(["", "Квест группа"]))
    rows.append(
        pad_row(
            [
                "ml",
                "string",
                "string",
                "string",
                "string",
                "string",
                "string",
                "int",
                "replace",
            ]
        )
    )
    rows.append(
        pad_row(
            [
                "",
                "input",
                "output",
                "title",
                "description",
                "description_complete",
                "description_spoil",
                "id",
                "find",
                "replace",
            ]
        )
    )
    rows.append(
        pad_row(
            [
                "",
                f"/quest_group/event/{find}_Story.proto.js",
                f"/quest_group/event/{replace}_Story.proto.js",
                quest_group.get("title") or "",
                quest_group.get("description") or "",
                quest_group.get("description_complete") or "",
                quest_group.get("description_spoil") or "",
                quest_group.get("id") or QUEST_GROUP_REFERENCE_ID,
                find,
                replace,
            ]
        )
    )
    rows.extend([blank_row()] * 5)


def quest_classname(quest: dict[str, Any]) -> str:
    return str(quest.get("classname_quests") or quest.get("classname") or "Quest")


def quest_prefix(classname: str) -> str:
    marker = "_Story_"
    if marker in classname:
        return classname.split(marker, 1)[0]
    return classname


def quest_prefix_from_group(quest_group: dict[str, Any]) -> str:
    output = str(quest_group.get("output") or "")
    match = re.search(r"/([^/]+)_Story\.proto\.js$", output)
    if match:
        return match.group(1)
    return "Campaign"


def quest_number(quest: dict[str, Any], quest_index: int = 0) -> int:
    try:
        return int(quest.get("quest_number") or quest_index + 1)
    except (TypeError, ValueError):
        return quest_index + 1


def make_proto_path(quest: dict[str, Any]) -> str:
    classname = quest_classname(quest)
    prefix = quest_prefix(classname)
    number = quest_number(quest)
    return f"/quest/{prefix}/story_{number}/{classname}.proto.js"


def make_reference_proto_path(quest: dict[str, Any], quest_index: int = 0) -> str:
    number = quest_number(quest, quest_index)
    return f"/quest/event/{QUEST_REFERENCE_CAMPAIGN_ID}/{QUEST_REFERENCE_CAMPAIGN_ID}_Story_{number}.proto.js"


def quest_reference_id(quest: dict[str, Any], quest_index: int = 0) -> int:
    return QUEST_GROUP_REFERENCE_ID + quest_number(quest, quest_index)


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


def append_quest_block(
    rows: list[list[Any]],
    quest: dict[str, Any],
    quest_index: int,
    input_proto_path: str,
    output_proto_path: str,
) -> None:
    rows.append(pad_row(["", quest_label(quest, quest_index)]))
    rows.append(pad_row(["sl", "string", "string", "string", "string", "string", "string", "int", "replace"]))
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
                "id",
                "find",
                "replace",
            ]
        )
    )
    rows.append(
        pad_row(
            [
                "",
                input_proto_path,
                output_proto_path,
                quest_title(quest),
                quest_description(quest),
                quest_congratulation(quest),
                quest_helper(quest),
                quest_reference_id(quest, quest_index),
                QUEST_REFERENCE_CAMPAIGN_ID,
                quest_prefix(quest_classname(quest)),
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


def iter_csv_rows(quests: list[dict[str, Any]], quest_group: dict[str, Any] | None = None) -> list[list[Any]]:
    rows: list[list[Any]] = []
    if quest_group is not None:
        append_quest_group_block(rows, quest_group)
    for quest_index, quest in enumerate(quests):
        output_proto_path = make_proto_path(quest)
        input_proto_path = make_reference_proto_path(quest, quest_index)
        append_quest_block(rows, quest, quest_index, input_proto_path, output_proto_path)
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
            rows.append(pad_row(["", output_proto_path, output_proto_path, first_key, first_value]))
            for key, value in fields[1:]:
                rows.append(pad_row(["", "", "", key, value]))
            rows.append(blank_row())
    return rows


def write_csv_rows(rows: list[list[Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream, delimiter=";", lineterminator="\n")
        writer.writerows(rows)


def export_filled_tasks_to_csv(
    filled_tasks: dict[str, Any],
    output_path: Path,
    quest_group: dict[str, Any] | None = None,
) -> dict[str, int]:
    quests = filled_tasks.get("quests", [])
    rows = iter_csv_rows(quests, quest_group=quest_group)
    write_csv_rows(rows, output_path)
    return {
        "quests_found": len(quests),
        "quest_group_exported": 1 if quest_group is not None else 0,
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
            "Сначала запусти stage 4 validation для текущего campaign/pack."
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


def ensure_quest_group_validation_passed(
    quest_group_path: Path,
    validation_path: Path,
    allow_stale: bool = False,
) -> dict[str, Any]:
    if not quest_group_path.exists():
        raise ValueError(
            f"quest group file not found: {quest_group_path}. "
            "Сначала создай этап 5: python src/build_quest_group.py --campaign <campaign_id> --current-pack <pack_id>"
        )
    if not validation_path.exists():
        raise ValueError(
            f"quest group validation file not found: {validation_path}. "
            "Сначала запусти этап 5 для текущего campaign/pack."
        )

    validation = read_json(validation_path)
    summary = validation.get("summary", {})
    errors = int(summary.get("errors", 0) or 0)
    if errors:
        raise ValueError(
            f"quest group validation has errors: {errors}. "
            "CSV не создан, нужно исправить этап 5."
        )

    if not allow_stale and validation_path.stat().st_mtime < quest_group_path.stat().st_mtime:
        raise ValueError(
            "quest_group.validation.json is older than quest_group.json. "
            "Сначала заново проверь этап 5."
        )

    return validation


def stage5_approval_error(
    context_path: Path,
    campaign_id: str | None = None,
    pack_id: str | None = None,
) -> str | None:
    context = load_context(context_path)
    expected_campaign_id = campaign_id or context.get("campaign_id") or ""
    expected_pack_id = pack_id or context.get("pack_id") or ""
    return stage_approval_error(
        context,
        REQUIRED_APPROVAL_STAGE,
        campaign_id=expected_campaign_id,
        pack_id=expected_pack_id,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export approved stage 5 quest group and validated stage 4 task objects to CSV.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=None,
        help="Validated filled tasks JSON. Default: campaigns/<campaign_id>/<pack_id>/filled_tasks.json when campaign/pack are known.",
    )
    parser.add_argument(
        "--validation-json",
        type=Path,
        default=None,
        help="Validation JSON produced by validate_task_objects.py.",
    )
    parser.add_argument(
        "--quest-group",
        type=Path,
        default=None,
        help="Stage 5 quest group JSON. Default: campaigns/<campaign_id>/<pack_id>/quest_group.json when campaign/pack are known.",
    )
    parser.add_argument(
        "--quest-group-validation-json",
        type=Path,
        default=None,
        help="Stage 5 quest group validation JSON.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=None,
        help="CSV output path. Default: campaigns/<campaign_id>/<pack_id>/generated_quests.csv when campaign/pack are known.",
    )
    parser.add_argument(
        "--allow-stale-validation",
        action="store_true",
        help="Allow validation JSON older than input. Use only for manual debugging.",
    )
    parser.add_argument("--approval-context", type=Path, default=DEFAULT_CONTEXT_PATH)
    parser.add_argument("--campaign", default="")
    parser.add_argument("--current-pack", default="")
    parser.add_argument(
        "--allow-unapproved-stage5",
        action="store_true",
        help="Emergency override: export CSV without recorded stage 5 approval.",
    )
    args = parser.parse_args(argv)

    campaign_id, pack_id = resolve_campaign_pack(
        args.campaign or None,
        args.current_pack or None,
        context_path=args.approval_context,
    )
    input_path = args.input or default_artifact_path(campaign_id, pack_id, FILLED_TASKS_JSON_NAME, DEFAULT_INPUT_PATH)
    validation_path = args.validation_json or default_artifact_path(campaign_id, pack_id, FILLED_TASKS_VALIDATION_NAME, DEFAULT_VALIDATION_PATH)
    quest_group_path = args.quest_group or default_artifact_path(campaign_id, pack_id, QUEST_GROUP_JSON_NAME, DEFAULT_QUEST_GROUP_PATH)
    quest_group_validation_path = args.quest_group_validation_json or default_artifact_path(
        campaign_id,
        pack_id,
        QUEST_GROUP_VALIDATION_NAME,
        DEFAULT_QUEST_GROUP_VALIDATION_PATH,
    )
    output_csv_path = args.output_csv or default_artifact_path(campaign_id, pack_id, GENERATED_QUESTS_CSV_NAME, DEFAULT_OUTPUT_CSV_PATH)

    if not input_path.exists():
        print(f"input file not found: {input_path}")
        return 1

    if not args.allow_unapproved_stage5:
        approval_error = stage5_approval_error(
            args.approval_context,
            campaign_id=campaign_id,
            pack_id=pack_id,
        )
        if approval_error is not None:
            print(f"CSV was not created: {approval_error}.")
            print("Сначала покажи пользователю quest_group этапа 5 и получи явный апрув в чате.")
            print(
                "Затем запиши апрув командой: "
                "python src/workflow_fast.py approve --stage 5 "
                "--campaign <campaign_id> --pack <pack_id>"
            )
            return 1

    try:
        ensure_validation_passed(input_path, validation_path, args.allow_stale_validation)
        ensure_quest_group_validation_passed(
            quest_group_path,
            quest_group_validation_path,
            allow_stale=args.allow_stale_validation,
        )
    except ValueError as exc:
        print(str(exc))
        return 2

    try:
        summary = export_filled_tasks_to_csv(
            read_json(input_path),
            output_csv_path,
            quest_group=read_json(quest_group_path),
        )
    except OSError as exc:
        print(f"could not write csv: {output_csv_path}")
        print(str(exc))
        return 3
    print(f"quests found: {summary['quests_found']}")
    print(f"quest group exported: {summary['quest_group_exported']}")
    print(f"quest blocks exported: {summary['quest_blocks_exported']}")
    print(f"tasks exported: {summary['tasks_exported']}")
    print(f"rows written: {summary['rows_written']}")
    print(f"csv written: {output_csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
