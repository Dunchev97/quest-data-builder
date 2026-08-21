from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAMPAIGNS_DIR = PROJECT_ROOT / "campaigns"

FILLED_TASKS_NAME = "filled_tasks.json"
GENERATED_ACTIONS_CSV_NAME = "generated_actions.csv"
GENERATED_ACTIONS_SUMMARY_NAME = "generated_actions.summary.json"

TEMPLATE_DIALOG = "TT-001"
TEMPLATE_GIVE = "TT-033"

DIALOG_TEMPLATE_INPUT = "/quest_action/Fun/Fun10/Fun10_Character_1_1_Dialog_1.proto.js"
SEARCH_TEMPLATE_INPUT = "/quest_action/Fun/Fun10/search_Fun10_HOG_1.proto.js"
GIVE_TEMPLATE_INPUT = "/quest_action/Fun/Fun13/Fun13_Character_18_Give_1.proto.js"
FURNITURE_WITHOUT_ACTIONS_TEMPLATE_INPUT = "/furniture/Fun/Fun13/Character/Fun13_Character_23.proto.js"
FURNITURE_WITH_ACTIONS_TEMPLATE_INPUT = "/furniture/Fun/Fun13/Character/Fun13_Character_18.proto.js"
ACTIONS_REFERENCE_FIRST_ID = 125015


@dataclass
class EntityAction:
    action_id: str


@dataclass
class EntityRow:
    classname: str
    title: str
    actions: list[EntityAction] = field(default_factory=list)
    order: int = 0


@dataclass
class DialogActionRow:
    identifier: str
    conditions: str
    icon_mc: str
    title: str
    text: str


@dataclass
class SearchActionRow:
    identifier: str
    replace: str


@dataclass
class GiveActionRow:
    identifier: str
    title: str
    icon: str
    conditions: str
    open_price: str


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="cp1251", newline="") as handle:
        writer = csv.writer(handle, delimiter=";", quotechar='"', lineterminator="\r\n")
        writer.writerows(rows)


def parse_pack_number(pack_id: str) -> int:
    match = re.fullmatch(r"pack_(\d+)", pack_id)
    if match is None:
        return 0
    return int(match.group(1))


def quest_number(quest: dict[str, Any], fallback: int) -> int:
    value = quest.get("quest_number")
    return int(value) if isinstance(value, int) else fallback


def task_number(task: dict[str, Any], fallback: int) -> int:
    value = task.get("task_number")
    return int(value) if isinstance(value, int) else fallback


def safe_text(value: Any) -> str:
    return str(value or "").strip()


def extract_person_from_title(title: str) -> str:
    if title.startswith("Поговори с "):
        return title[len("Поговори с ") :].strip()
    return title


def extract_person_from_hint(hint: str) -> str:
    match = re.search(r"персонажу\s+(.+?)\.", hint)
    if match:
        return match.group(1).strip()
    return ""


def entity_output_path(campaign_id: str, classname: str) -> str:
    return f"/furniture/Fun/{campaign_id}/Character/{classname}.proto.js"


def action_output_path(campaign_id: str, identifier: str) -> str:
    return f"/quest_action/Fun/{campaign_id}/{identifier}.proto.js"


def action_kind(template_id: str, task_type: str, task_object: dict[str, Any]) -> str | None:
    if template_id == TEMPLATE_DIALOG or "dialog" in task_type.lower():
        return "dialog"
    if template_id == TEMPLATE_GIVE or task_type.lower() == "action give":
        return "give"
    param = task_object.get("param")
    if isinstance(param, str) and re.search(r"_HOG_\d+$", param):
        return "search"
    return None


def iter_campaign_tasks(campaign_dir: Path) -> list[tuple[str, dict[str, Any], dict[str, Any]]]:
    rows: list[tuple[int, int, int, str, dict[str, Any], dict[str, Any]]] = []
    for pack_dir in sorted((path for path in campaign_dir.glob("pack_*") if path.is_dir()), key=lambda path: parse_pack_number(path.name)):
        filled_tasks_path = pack_dir / FILLED_TASKS_NAME
        if not filled_tasks_path.exists():
            continue
        data = read_json(filled_tasks_path)
        for quest_index, quest in enumerate(data.get("quests", []), start=1):
            qn = quest_number(quest, quest_index)
            for local_task_index, task in enumerate(quest.get("tasks", []), start=1):
                tn = task_number(task, local_task_index)
                rows.append((parse_pack_number(pack_dir.name), qn, tn, pack_dir.name, quest, task))
    rows.sort(key=lambda item: (item[0], item[1], item[2]))
    return [(pack_id, quest, task) for _pn, _qn, _tn, pack_id, quest, task in rows]


def iter_campaign_quests(campaign_dir: Path) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[int, int, str, dict[str, Any]]] = []
    for pack_dir in sorted((path for path in campaign_dir.glob("pack_*") if path.is_dir()), key=lambda path: parse_pack_number(path.name)):
        filled_tasks_path = pack_dir / FILLED_TASKS_NAME
        if not filled_tasks_path.exists():
            continue
        data = read_json(filled_tasks_path)
        for quest_index, quest in enumerate(data.get("quests", []), start=1):
            rows.append((parse_pack_number(pack_dir.name), quest_number(quest, quest_index), pack_dir.name, quest))
    rows.sort(key=lambda item: (item[0], item[1]))
    return [(pack_id, quest) for _pn, _qn, pack_id, quest in rows]


def should_export_pack(pack_id: str, current_pack_id: str | None) -> bool:
    return current_pack_id is None or pack_id == current_pack_id


def task_object_from_entry(task_entry: dict[str, Any]) -> dict[str, Any]:
    task_object = task_entry.get("task_object")
    return task_object if isinstance(task_object, dict) else task_entry


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


def quest_helper_classname(quest: dict[str, Any]) -> str:
    explicit = explicit_quest_helper(quest)
    if explicit:
        return explicit
    for task_entry in quest.get("tasks", []):
        classname = task_character_classname(task_entry)
        if classname:
            return classname
    return ""


def build_actions(
    campaign_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    current_pack_id: str | None = None,
) -> tuple[list[list[Any]], dict[str, Any]]:
    campaign_dir = campaigns_dir / campaign_id
    if not campaign_dir.exists():
        raise FileNotFoundError(f"campaign not found: {campaign_dir}")

    dialog_counter = 0
    give_counters: dict[str, int] = {}
    entity_rows: dict[str, EntityRow] = {}
    entity_titles: dict[str, str] = {}
    entity_order = 0

    dialog_rows: list[DialogActionRow] = []
    search_rows: list[SearchActionRow] = []
    give_rows: list[GiveActionRow] = []

    def register_entity(classname: str, title: str) -> EntityRow | None:
        nonlocal entity_order
        if not classname:
            return None
        if title:
            entity_titles.setdefault(classname, title)
        if classname not in entity_rows:
            entity_order += 1
            entity_rows[classname] = EntityRow(
                classname=classname,
                title=entity_titles.get(classname) or title or classname,
                order=entity_order,
            )
        elif title and entity_rows[classname].title == classname:
            entity_rows[classname].title = title
        return entity_rows[classname]

    for pack_id, quest in iter_campaign_quests(campaign_dir):
        helper = quest_helper_classname(quest)
        helper_title = safe_text(quest.get("character")) or helper
        if helper:
            entity_titles.setdefault(helper, helper_title)
            if should_export_pack(pack_id, current_pack_id):
                register_entity(helper, helper_title)

    for pack_id, quest, task in iter_campaign_tasks(campaign_dir):
        quest_classname = safe_text(quest.get("classname_quests"))
        if not quest_classname:
            continue
        export_current_task = should_export_pack(pack_id, current_pack_id)
        quest_character = safe_text(quest.get("character"))
        task_type = safe_text(task.get("task_type"))
        template_id = safe_text(task.get("task_template_id"))
        task_object = task.get("task_object") if isinstance(task.get("task_object"), dict) else {}
        kind = action_kind(template_id, task_type, task_object)
        if kind is None:
            continue

        if kind == "dialog":
            icon = safe_text(task_object.get("icon"))
            if not icon:
                continue
            dialog_counter += 1
            task_action = safe_text(task_object.get("action"))
            action_id = task_action if task_action.startswith(f"{icon}_Dialog_") else f"{icon}_Dialog_{dialog_counter}"
            person_title = quest_character or extract_person_from_title(safe_text(task_object.get("title"))) or icon
            entity_titles.setdefault(icon, person_title)
            if not export_current_task:
                continue
            text = safe_text(task.get("dialogue_replica")) or safe_text(quest.get("description"))
            dialog_rows.append(
                DialogActionRow(
                    identifier=action_id,
                    conditions=f"active_quest={quest_classname}",
                    icon_mc=icon,
                    title=person_title,
                    text=text,
                )
            )
            entity = register_entity(icon, person_title)
            if entity is not None:
                entity.actions.append(EntityAction(action_id=action_id))
            continue

        if kind == "search":
            hog_classname = safe_text(task_object.get("param"))
            if hog_classname and export_current_task:
                search_rows.append(
                    SearchActionRow(
                        identifier=f"search_{hog_classname}",
                        replace=hog_classname,
                    )
                )
            continue

        if kind == "give":
            locations = task_object.get("go_to_location")
            location_classname = ""
            if isinstance(locations, list) and locations:
                first = locations[0]
                if isinstance(first, dict):
                    location_classname = safe_text(first.get("classname"))

            task_action = safe_text(task_object.get("action"))
            action_classname = task_action.removesuffix("_Give") if task_action.endswith("_Give") else ""
            icon = safe_text(task_object.get("icon"))
            action_classname = action_classname or icon or location_classname
            if not action_classname:
                continue

            recipient_title = extract_person_from_hint(safe_text(task_object.get("hint")))
            recipient_classname = next(
                (classname for classname, title in entity_titles.items() if title == recipient_title),
                "",
            )
            if not recipient_classname and location_classname in entity_titles:
                recipient_classname = location_classname
            recipient_classname = recipient_classname or location_classname or action_classname

            give_counters[action_classname] = give_counters.get(action_classname, 0) + 1
            action_id = f"action_{action_classname}_Give_{give_counters[action_classname]}"
            target_title = entity_titles.get(recipient_classname) or recipient_title or safe_text(task_object.get("title")) or recipient_classname
            entity_titles.setdefault(recipient_classname, target_title)
            if not export_current_task:
                continue
            open_price = f"asset={icon}:1" if icon else ""
            give_rows.append(
                GiveActionRow(
                    identifier=action_id,
                    title=target_title,
                    icon=icon,
                    conditions=f"active_quest={quest_classname}",
                    open_price=open_price,
                )
            )
            entity = register_entity(recipient_classname, target_title)
            if entity is not None:
                entity.actions.append(EntityAction(action_id=action_id))
            continue

    rows: list[list[Any]] = []
    next_id = ACTIONS_REFERENCE_FIRST_ID

    def take_reference_id() -> int:
        nonlocal next_id
        value = next_id
        next_id += 1
        return value

    entities_sorted = sorted(entity_rows.values(), key=lambda item: item.order)
    reserved_entity_ids = {item.classname: take_reference_id() for item in entities_sorted}
    groups: dict[int, list[EntityRow]] = {}
    for item in entities_sorted:
        groups.setdefault(len(item.actions), []).append(item)

    for count in sorted(groups):
        group_rows = groups[count]
        if count == 0:
            rows.append(["", "ПЕРСОНАЖИ БЕЗ ЭКШЕНОВ"])
            rows.append(["ml", "string", "string", "string", "string", "int", "", "", "", ""])
            rows.append(["", "input", "output", "classname", "title", "id", "", "", "", ""])
            for entity in group_rows:
                rows.append(
                    [
                        "",
                        FURNITURE_WITHOUT_ACTIONS_TEMPLATE_INPUT,
                        entity_output_path(campaign_id, entity.classname),
                        entity.classname,
                        entity.title,
                        reserved_entity_ids[entity.classname],
                        "",
                        "",
                        "",
                        "",
                    ]
                )
            rows.append([])
            continue
        rows.append(["", f"ПЕРСОНАЖИ с {count} " + ("ЭКШЕНОМ" if count == 1 else "ЭКШЕНАМИ")])
        rows.append(["ml", "string", "string", "string", "string", "array", "int", "", "", ""])
        rows.append(["", "input", "output", "classname", "title", "behaviour.0.actions", "id", "", "", ""])
        for entity in group_rows:
            for action_index, action in enumerate(entity.actions):
                if action_index == 0:
                    rows.append(
                        [
                            "",
                            FURNITURE_WITH_ACTIONS_TEMPLATE_INPUT,
                            entity_output_path(campaign_id, entity.classname),
                            entity.classname,
                            entity.title,
                            action.action_id,
                            take_reference_id(),
                            "",
                            "",
                            "",
                        ]
                    )
                else:
                    rows.append(["", "", "", "", "", action.action_id, "", "", "", ""])
        rows.append([])

    if dialog_rows:
        rows.append(["", "ЭКШЕНЫ ДИАЛОГИ"])
        rows.append(["sl", "string", "string", "string", "string", "string", "string", "string", "string", "int"])
        rows.append(
            [
                "",
                "input",
                "output",
                "identifier",
                "conditions",
                "stuff_actions.0.window_spec.view_window",
                "stuff_actions.0.window_spec.icon.0.icon_mc",
                "stuff_actions.0.window_spec.text_fields.0.text",
                "stuff_actions.0.window_spec.text_fields.1.text",
                "id",
            ]
        )
        for row in dialog_rows:
            rows.append(
                [
                    "",
                    DIALOG_TEMPLATE_INPUT,
                    action_output_path(campaign_id, row.identifier),
                    row.identifier,
                    row.conditions,
                    "Character_Dialog_Window",
                    row.icon_mc,
                    row.title,
                    row.text,
                    take_reference_id(),
                ]
            )
        rows.append([])

    if search_rows:
        rows.append(["", "ЭКШЕНЫ search"])
        rows.append(["sl", "string", "string", "string", "string", "replace", "", "int", "", ""])
        rows.append(["", "input", "output", "identifier", "open_price", "find", "replace", "id", "", ""])
        for row in search_rows:
            rows.append(
                [
                    "",
                    SEARCH_TEMPLATE_INPUT,
                    action_output_path(campaign_id, row.identifier),
                    row.identifier,
                    "money=2",
                    "Fun10_HOG_1",
                    row.replace,
                    take_reference_id(),
                    "",
                    "",
                ]
            )
        rows.append([])

    if give_rows:
        rows.append(["", "ЭКШЕНЫ Give"])
        rows.append(["sl", "string", "string", "string", "string", "string", "string", "string", "int", ""])
        rows.append(["", "input", "output", "identifier", "title", "icon", "conditions", "open_price", "id", ""])
        for row in give_rows:
            rows.append(
                [
                    "",
                    GIVE_TEMPLATE_INPUT,
                    action_output_path(campaign_id, row.identifier),
                    row.identifier,
                    row.title,
                    row.icon,
                    row.conditions,
                    row.open_price,
                    take_reference_id(),
                    "",
                ]
            )

    summary = {
        "campaign_id": campaign_id,
        "entities": len(entities_sorted),
        "entities_without_actions": len(groups.get(0, [])),
        "dialog_actions": len(dialog_rows),
        "search_actions": len(search_rows),
        "give_actions": len(give_rows),
        "current_pack_id": current_pack_id or "",
        "packs_scanned": [path.name for path in sorted((p for p in campaign_dir.glob("pack_*") if p.is_dir()), key=lambda p: parse_pack_number(p.name))],
    }
    return rows, summary


def build_actions_table_file(
    campaign_id: str,
    output_csv: Path,
    summary_json: Path,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    current_pack_id: str | None = None,
) -> dict[str, Any]:
    rows, summary = build_actions(campaign_id, campaigns_dir=campaigns_dir, current_pack_id=current_pack_id)
    write_csv(output_csv, rows)
    write_json(summary_json, summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build actions CSV for dialogs, gives and hog search actions.")
    parser.add_argument("campaign_id")
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    parser.add_argument("--pack", default="", help="Optional current pack id. When set, export only actions from this pack while preserving campaign-wide numbering.")
    parser.add_argument("--output-csv", type=Path, default=None)
    parser.add_argument("--summary-json", type=Path, default=None)
    args = parser.parse_args(argv)

    output_csv = args.output_csv or args.campaigns_dir / args.campaign_id / GENERATED_ACTIONS_CSV_NAME
    summary_json = args.summary_json or args.campaigns_dir / args.campaign_id / GENERATED_ACTIONS_SUMMARY_NAME
    summary = build_actions_table_file(
        args.campaign_id,
        output_csv,
        summary_json,
        campaigns_dir=args.campaigns_dir,
        current_pack_id=args.pack or None,
    )
    print(f"actions csv written: {output_csv}")
    print(f"summary written: {summary_json}")
    print(f"entities: {summary['entities']}")
    print(f"dialog_actions: {summary['dialog_actions']}")
    print(f"search_actions: {summary['search_actions']}")
    print(f"give_actions: {summary['give_actions']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
