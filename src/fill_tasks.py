from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from .export_csv import export_quests_to_csv
    from .task_templates import detect_template_id, load_task_templates
except ImportError:
    from export_csv import export_quests_to_csv
    from task_templates import detect_template_id, load_task_templates


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class FillContext:
    quest_ready_index: dict[str, Any]
    quest_ready_drops: list[dict[str, Any]]
    templates: dict[str, Any]
    garbage_cursor: int = 0
    collection_cursor: int = 0
    flower_cursor: int = 0
    gr_cursor: int = 0

    def __post_init__(self) -> None:
        self.locations_by_garbage = build_locations_by_garbage(
            self.quest_ready_index["quest_ready_locations"]
        )
        self.garbage_items = [
            item
            for item in self.quest_ready_index["quest_ready_garbage"].values()
            if item.get("title") and self.locations_by_garbage.get(item.get("classname"))
        ]
        self.garbage_items.sort(key=lambda item: item["classname"])
        self.flower_items = [
            item
            for item in self.quest_ready_index["quest_ready_flowers"].values()
            if item.get("title")
        ]
        self.flower_items.sort(key=lambda item: item["classname"])
        self.collection_drops = [
            drop
            for drop in self.quest_ready_drops
            if drop.get("collection_classname")
            and drop.get("collection_title")
            and drop.get("source_title")
        ]
        self.collection_drops.sort(
            key=lambda drop: (
                drop.get("collection_classname", ""),
                drop.get("source_classname", ""),
                drop.get("mode", ""),
            )
        )
        self.garbage_gr_drops = [
            drop
            for drop in self.quest_ready_drops
            if drop.get("source_type") == "garbage"
            and drop.get("source_title")
            and drop.get("locations")
        ]
        self.garbage_gr_drops.sort(
            key=lambda drop: (
                drop.get("source_classname", ""),
                drop.get("collection_classname", ""),
                drop.get("mode", ""),
            )
        )

    def next_garbage(self) -> dict[str, Any]:
        if not self.garbage_items:
            raise ValueError("Нет quest-ready мусора для заполнения garbage task.")
        item = self.garbage_items[self.garbage_cursor % len(self.garbage_items)]
        self.garbage_cursor += 1
        return item

    def next_collection_drop(self) -> dict[str, Any]:
        if not self.collection_drops:
            raise ValueError("Нет quest-ready collection drops для get_asset Collection.")
        item = self.collection_drops[self.collection_cursor % len(self.collection_drops)]
        self.collection_cursor += 1
        return item

    def next_garbage_gr_drop(self) -> dict[str, Any]:
        if not self.garbage_gr_drops:
            raise ValueError("Нет quest-ready garbage drops для get_asset GR in_guest garbage.")
        item = self.garbage_gr_drops[self.gr_cursor % len(self.garbage_gr_drops)]
        self.gr_cursor += 1
        return item

    def next_flower(self) -> dict[str, Any]:
        if not self.flower_items:
            raise ValueError("Нет quest-ready цветов для action take_crop_in_guest.")
        item = self.flower_items[self.flower_cursor % len(self.flower_items)]
        self.flower_cursor += 1
        return item


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_locations_by_garbage(locations: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for location in locations.values():
        for garbage_classname in location.get("garbage_assets", []):
            result.setdefault(garbage_classname, []).append(
                {
                    "code": location.get("code"),
                    "title": location.get("title"),
                    "tags": location.get("tags"),
                }
            )
    return result


def parse_stage3_quests(text: str) -> list[dict[str, Any]]:
    quests: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    key_map = {
        "Classname quests": "classname",
        "title_quest": "title_quest",
        "№ quest": "quest_number",
        "№ task": "task_numbers",
        "Task type": "task_types",
        "description": "description",
        "congratulation": "congratulation",
        "Character": "character",
    }

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("Classname quests:"):
            if current:
                finalize_quest(current)
                quests.append(current)
            current = {}

        if current is None or ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = clean_text_value(value.strip())
        if key not in key_map:
            continue

        mapped_key = key_map[key]
        if mapped_key == "task_numbers":
            current[mapped_key] = [int(number) for number in re.findall(r"\d+", value)]
        elif mapped_key == "task_types":
            current[mapped_key] = [part.strip() for part in value.split("/") if part.strip()]
        elif mapped_key == "quest_number":
            match = re.search(r"\d+", value)
            current[mapped_key] = int(match.group(0)) if match else None
        else:
            current[mapped_key] = value

    if current:
        finalize_quest(current)
        quests.append(current)

    return [quest for quest in quests if quest.get("classname") and quest.get("task_types")]


def clean_text_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def finalize_quest(quest: dict[str, Any]) -> None:
    task_types = quest.get("task_types", [])
    if not quest.get("task_numbers"):
        quest["task_numbers"] = list(range(1, len(task_types) + 1))
    if len(quest["task_numbers"]) < len(task_types):
        start = quest["task_numbers"][-1] + 1 if quest["task_numbers"] else 1
        quest["task_numbers"].extend(range(start, start + len(task_types) - len(quest["task_numbers"])))


def quest_prefix(classname: str) -> str:
    match = re.match(r"(.+)_Story_\d+$", classname)
    return match.group(1) if match else classname


def compact_location_titles(locations: list[dict[str, Any]], limit: int = 3) -> str:
    titles = []
    for location in locations:
        title = location.get("title")
        if title and title not in titles:
            titles.append(title)
    return ", ".join(titles[:limit])


def make_proto_path(quest: dict[str, Any]) -> str:
    classname = quest.get("classname", "Quest")
    prefix = quest_prefix(classname)
    return f"/quest/event/{prefix}/{classname}.proto.js"


def fill_quests(
    quests: list[dict[str, Any]],
    context: FillContext,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    filled: list[dict[str, Any]] = []
    issues: list[dict[str, Any]] = []

    for quest in quests:
        filled_quest = dict(quest)
        filled_quest["proto_path"] = make_proto_path(quest)
        filled_quest["tasks"] = []

        for index, raw_task_type in enumerate(quest.get("task_types", [])):
            template_id = detect_template_id(raw_task_type)
            task_number = quest["task_numbers"][index]
            if template_id is None:
                issues.append(
                    {
                        "code": "unsupported_task_type",
                        "quest": quest.get("classname"),
                        "task_number": task_number,
                        "task_type": raw_task_type,
                        "message": "Task type is not implemented in this first CSV stage.",
                    }
                )
                continue

            try:
                task = fill_task(template_id, raw_task_type, quest, task_number, context)
            except ValueError as exc:
                issues.append(
                    {
                        "code": "fill_failed",
                        "quest": quest.get("classname"),
                        "task_number": task_number,
                        "task_type": raw_task_type,
                        "message": str(exc),
                    }
                )
                continue

            filled_quest["tasks"].append(task)

        filled.append(filled_quest)

    return filled, issues


def fill_task(
    template_id: str,
    raw_task_type: str,
    quest: dict[str, Any],
    task_number: int,
    context: FillContext,
) -> dict[str, Any]:
    if template_id == "garbage_classname_in_guest":
        return fill_garbage_task(context, in_guest=True)
    if template_id == "garbage_classname":
        return fill_garbage_task(context, in_guest=False)
    if template_id == "get_asset_collection":
        return fill_get_asset_collection(context)
    if template_id == "get_asset_gr_in_guest_garbage":
        return fill_get_asset_gr_in_guest_garbage(context, quest, task_number)
    if template_id == "action_take_crop_in_guest":
        return fill_take_crop_in_guest(context)
    raise ValueError(f"Unsupported template id: {template_id}")


def fill_garbage_task(context: FillContext, in_guest: bool) -> dict[str, Any]:
    garbage = context.next_garbage()
    locations = context.locations_by_garbage.get(garbage["classname"], [])
    location_titles = compact_location_titles(locations)
    task = {
        "type": "garbage",
        "classname": garbage["classname"],
        "amount": 1,
        "price": 1,
        "title": f"Убери {garbage['title']}",
        "hint": (
            "Чтобы убрать мусор - нажми на него мышкой "
            + ("в гостях друга" if in_guest else "дома")
            + f". Место поиска: {location_titles}."
        ),
    }
    if in_guest:
        task["in_guest"] = 1
    return task


def fill_get_asset_collection(context: FillContext) -> dict[str, Any]:
    drop = context.next_collection_drop()
    collection_title = drop["collection_title"]
    source_title = drop["source_title"]
    source_type = drop["source_type"]

    if source_type == "garbage":
        locations = compact_location_titles(drop.get("locations", []))
        source_hint = f"выпадает при уборке мусора {source_title}. Место поиска: {locations}"
    else:
        source_hint = f"выпадает при сборе цветка {source_title}"

    return {
        "type": "get_asset",
        "classname": drop["collection_classname"],
        "icon": drop["collection_classname"],
        "amount": 1,
        "price": 1,
        "title": f"Найди {collection_title}",
        "hint": f"{collection_title} - элемент коллекции, {source_hint}.",
    }


def fill_get_asset_gr_in_guest_garbage(
    context: FillContext,
    quest: dict[str, Any],
    task_number: int,
) -> dict[str, Any]:
    drop = context.next_garbage_gr_drop()
    source_title = drop["source_title"]
    locations = compact_location_titles(drop.get("locations", []))
    classname = f"{quest_prefix(quest['classname'])}_GR_{task_number}"

    return {
        "type": "get_asset",
        "classname": classname,
        "icon": classname,
        "amount": 1,
        "price": 1,
        "title": f"Найди {drop['collection_title']}",
        "hint": f"Убирай мусор {source_title} в гостях, чтобы найти. Место поиска: {locations}.",
    }


def fill_take_crop_in_guest(context: FillContext) -> dict[str, Any]:
    flower = context.next_flower()
    return {
        "type": "action",
        "action": "take_crop_in_guest",
        "title": f"Собери {flower['title']} в гостях",
        "hint": f"Собирай {flower['title']} в гостях. Чтобы собрать растение, кликни на горшок с нужным растением в гостях у друга",
        "param": flower["classname"],
        "amount": 1,
        "price": 1,
    }


def run_fill(
    input_path: Path,
    templates_path: Path,
    quest_ready_index_path: Path,
    quest_ready_drops_path: Path,
    output_json_path: Path,
    output_csv_path: Path,
) -> dict[str, Any]:
    quests = parse_stage3_quests(input_path.read_text(encoding="utf-8-sig"))
    context = FillContext(
        quest_ready_index=read_json(quest_ready_index_path),
        quest_ready_drops=read_json(quest_ready_drops_path),
        templates=load_task_templates(templates_path),
    )
    filled_quests, issues = fill_quests(quests, context)

    output = {
        "quests": filled_quests,
        "issues": issues,
        "summary": {
            "quests_found": len(quests),
            "quests_written": len(filled_quests),
            "tasks_written": sum(len(quest.get("tasks", [])) for quest in filled_quests),
            "issues": len(issues),
        },
    }
    write_json(output_json_path, output)
    export_quests_to_csv(filled_quests, output_csv_path)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fill first task templates from stage 3 quests.")
    parser.add_argument(
        "--input",
        type=Path,
        default=PROJECT_ROOT / "data" / "stage3_quests.txt",
        help="Text file with stage 3 quests.",
    )
    parser.add_argument(
        "--templates",
        type=Path,
        default=PROJECT_ROOT / "data" / "task_templates.json",
        help="Task templates JSON.",
    )
    parser.add_argument(
        "--quest-ready-index",
        type=Path,
        default=PROJECT_ROOT / "data" / "quest_ready_index.json",
        help="Quest-ready index JSON.",
    )
    parser.add_argument(
        "--quest-ready-drops",
        type=Path,
        default=PROJECT_ROOT / "data" / "quest_ready_drops.index.json",
        help="Quest-ready drops JSON.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=PROJECT_ROOT / "output" / "generated_tasks.json",
        help="Intermediate filled task objects JSON.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=PROJECT_ROOT / "output" / "generated_quests.csv",
        help="Generated CSV path.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Передай файл этапа 3 через --input или положи его в data/stage3_quests.txt.")
        return 1

    output = run_fill(
        input_path=args.input,
        templates_path=args.templates,
        quest_ready_index_path=args.quest_ready_index,
        quest_ready_drops_path=args.quest_ready_drops,
        output_json_path=args.output_json,
        output_csv_path=args.output_csv,
    )
    summary = output["summary"]
    print(f"quests found: {summary['quests_found']}")
    print(f"tasks written: {summary['tasks_written']}")
    print(f"issues: {summary['issues']}")
    print(f"json written: {args.output_json}")
    print(f"csv written: {args.output_csv}")
    return 0 if summary["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
