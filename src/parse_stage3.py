from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "input" / "stage3_quests.txt"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "quest_plan.json"
DEFAULT_OUTPUT_PREVIEW_PATH = PROJECT_ROOT / "output" / "quest_plan.preview.md"


@dataclass
class QuestPlan:
    classname_quests: str | None = None
    title_quest: str | None = None
    quest_number: int | None = None
    task_numbers: list[int] | None = None
    task_template_ids: list[str] | None = None
    task_template_names: list[str] | None = None
    task_types: list[str] | None = None
    description: str | None = None
    congratulation: str | None = None
    character: str | None = None
    raw_text: str = ""

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        data["task_numbers"] = data["task_numbers"] or []
        data["task_template_ids"] = data["task_template_ids"] or []
        data["task_template_names"] = data["task_template_names"] or []
        data["task_types"] = data["task_types"] or []
        data["tasks"] = build_task_rows(
            data["task_numbers"],
            data["task_template_ids"],
            data["task_template_names"],
            data["task_types"],
        )
        return data


@dataclass
class Stage2QuestText:
    title: str
    start: str = ""
    finish: str = ""


FIELD_ALIASES = {
    "Classname quests": "classname_quests",
    "title_quest": "title_quest",
    "№ quest": "quest_number",
    "в„– quest": "quest_number",
    "# quest": "quest_number",
    "No quest": "quest_number",
    "№ task": "task_numbers",
    "в„– task": "task_numbers",
    "# task": "task_numbers",
    "No task": "task_numbers",
    "Task template ID": "task_template_ids",
    "Task template IDs": "task_template_ids",
    "Task template id": "task_template_ids",
    "Task template ids": "task_template_ids",
    "Task template name": "task_template_names",
    "Task template names": "task_template_names",
    "Task type": "task_types",
    "description": "description",
    "congratulation": "congratulation",
    "Character": "character",
}


REQUIRED_FIELDS = [
    "classname_quests",
    "title_quest",
    "quest_number",
    "task_numbers",
    "task_template_ids",
    "task_template_names",
    "task_types",
    "description",
    "congratulation",
    "character",
]

CRAFT_LIKE_TEMPLATE_IDS = {"TT-002", "TT-033"}
MIN_CRAFT_LIKE_QUEST_SPACING = 4


def read_text(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1251"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="latin-1")


def clean_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def normalize_stage_text(value: str | None) -> str:
    return " ".join(clean_value(value or "").split())


def normalize_title(value: str | None) -> str:
    return normalize_stage_text(value).casefold()


def parse_int_list(value: str) -> list[int]:
    return [int(number) for number in re.findall(r"\d+", value)]


def parse_first_int(value: str) -> int | None:
    match = re.search(r"\d+", value)
    return int(match.group(0)) if match else None


def split_slash_list(value: str) -> list[str]:
    return [part.strip() for part in value.split("/") if part.strip()]


def build_task_rows(
    task_numbers: list[int],
    task_template_ids: list[str],
    task_template_names: list[str],
    task_types: list[str],
) -> list[dict[str, Any]]:
    task_count = max(
        len(task_numbers),
        len(task_template_ids),
        len(task_template_names),
        len(task_types),
        0,
    )
    tasks: list[dict[str, Any]] = []
    for index in range(task_count):
        tasks.append(
            {
                "task_number": task_numbers[index] if index < len(task_numbers) else None,
                "task_template_id": task_template_ids[index] if index < len(task_template_ids) else None,
                "task_template_name": task_template_names[index] if index < len(task_template_names) else None,
                "task_type": task_types[index] if index < len(task_types) else None,
            }
        )
    return tasks


def split_quest_blocks(text: str) -> list[str]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for line in text.splitlines():
        if line.strip().startswith("Classname quests:"):
            if current:
                blocks.append(current)
            current = [line]
        elif current:
            current.append(line)

    if current:
        blocks.append(current)

    return ["\n".join(block).strip() for block in blocks if "\n".join(block).strip()]


def parse_quest_block(block: str) -> QuestPlan:
    quest = QuestPlan(raw_text=block)

    for raw_line in block.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue

        raw_key, raw_value = line.split(":", 1)
        key = raw_key.strip()
        value = clean_value(raw_value)
        field_name = FIELD_ALIASES.get(key)
        if field_name is None:
            continue

        if field_name == "quest_number":
            setattr(quest, field_name, parse_first_int(value))
        elif field_name == "task_numbers":
            setattr(quest, field_name, parse_int_list(value))
        elif field_name in ("task_template_ids", "task_template_names", "task_types"):
            setattr(quest, field_name, split_slash_list(value))
        else:
            setattr(quest, field_name, value)

    task_count = max(
        len(quest.task_template_ids or []),
        len(quest.task_template_names or []),
        len(quest.task_types or []),
        0,
    )
    if task_count and not quest.task_numbers:
        quest.task_numbers = list(range(1, task_count + 1))

    return quest


def parse_stage3_text(text: str) -> list[QuestPlan]:
    return [parse_quest_block(block) for block in split_quest_blocks(text)]


def is_stage2_quest_header(lines: list[str], index: int) -> bool:
    line = lines[index].strip()
    if not line or ":" not in line:
        return False

    key = line.split(":", 1)[0].strip()
    if key in {"ЭТАП 2", "Суть", "Суть задания", "Старт", "Завершение", "Конец этапа 2"}:
        return False

    next_index = index + 1
    while next_index < len(lines) and not lines[next_index].strip():
        next_index += 1
    if next_index >= len(lines):
        return False
    next_line = lines[next_index].strip()
    return next_line.startswith("Суть:") or next_line.startswith("Суть задания:")


def append_stage2_text(target: list[str], value: str) -> None:
    cleaned = clean_value(value)
    if cleaned:
        target.append(cleaned)


def parse_stage2_story_text(text: str) -> dict[str, Stage2QuestText]:
    lines = text.splitlines()
    quests: dict[str, Stage2QuestText] = {}
    index = 0

    while index < len(lines):
        if not is_stage2_quest_header(lines, index):
            index += 1
            continue

        _, raw_title = lines[index].split(":", 1)
        title = clean_value(raw_title)
        start_lines: list[str] = []
        finish_lines: list[str] = []
        active_field: str | None = None
        index += 1

        while index < len(lines):
            line = lines[index].strip()
            if is_stage2_quest_header(lines, index):
                break
            if line.startswith("Старт:"):
                active_field = "start"
                append_stage2_text(start_lines, line.split(":", 1)[1])
            elif line.startswith("Завершение:"):
                active_field = "finish"
                append_stage2_text(finish_lines, line.split(":", 1)[1])
            elif line.startswith("Суть:") or line.startswith("Суть задания:") or line.startswith("Конец этапа 2"):
                active_field = None
            elif active_field == "start":
                append_stage2_text(start_lines, line)
            elif active_field == "finish":
                append_stage2_text(finish_lines, line)
            index += 1

        quests[normalize_title(title)] = Stage2QuestText(
            title=title,
            start=normalize_stage_text(" ".join(start_lines)),
            finish=normalize_stage_text(" ".join(finish_lines)),
        )

    return quests


def find_stage2_text_issues(
    quests: list[QuestPlan],
    stage2_quests: dict[str, Stage2QuestText],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []

    if not stage2_quests:
        return [
            {
                "code": "stage2_story_empty",
                "message": "Stage 2 text was provided, but no quest start/finish blocks were parsed.",
            }
        ]

    for index, quest in enumerate(quests, start=1):
        stage2_quest = stage2_quests.get(normalize_title(quest.title_quest))
        if stage2_quest is None:
            issues.append(
                {
                    "code": "stage2_quest_not_found",
                    "quest_index": index,
                    "classname_quests": quest.classname_quests,
                    "title_quest": quest.title_quest,
                    "message": "Stage 3 title_quest must match a quest title from Stage 2.",
                }
            )
            continue

        description = normalize_stage_text(quest.description)
        congratulation = normalize_stage_text(quest.congratulation)
        if description != stage2_quest.start:
            issues.append(
                {
                    "code": "description_not_from_stage2_start",
                    "quest_index": index,
                    "classname_quests": quest.classname_quests,
                    "title_quest": quest.title_quest,
                    "message": "Stage 3 description must be copied from Stage 2 Старт without rewriting.",
                }
            )
        if congratulation != stage2_quest.finish:
            issues.append(
                {
                    "code": "congratulation_not_from_stage2_finish",
                    "quest_index": index,
                    "classname_quests": quest.classname_quests,
                    "title_quest": quest.title_quest,
                    "message": "Stage 3 congratulation must be copied from Stage 2 Завершение without rewriting.",
                }
            )

    return issues


def find_quest_issues(quests: list[QuestPlan], stage2_text: str | None = None) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    craft_like_quests: list[dict[str, Any]] = []
    for index, quest in enumerate(quests, start=1):
        data = quest.to_json()
        for field_name in REQUIRED_FIELDS:
            value = data.get(field_name)
            if value in (None, "", []):
                issues.append(
                    {
                        "code": "missing_field",
                        "quest_index": index,
                        "classname_quests": quest.classname_quests,
                        "field": field_name,
                        "message": f"Quest is missing required field: {field_name}",
                    }
                )

        task_counts = {
            "task_numbers": len(quest.task_numbers or []),
            "task_template_ids": len(quest.task_template_ids or []),
            "task_template_names": len(quest.task_template_names or []),
            "task_types": len(quest.task_types or []),
        }
        present_task_counts = {field: count for field, count in task_counts.items() if count > 0}
        if len(set(present_task_counts.values())) > 1:
            issues.append(
                {
                    "code": "task_count_mismatch",
                    "quest_index": index,
                    "classname_quests": quest.classname_quests,
                    "task_counts": present_task_counts,
                    "message": "Number of task numbers, template IDs, template names and task types must match.",
                }
            )

        for task_template_id in quest.task_template_ids or []:
            if not re.fullmatch(r"TT-\d{3}", task_template_id):
                issues.append(
                    {
                        "code": "invalid_task_template_id",
                        "quest_index": index,
                        "classname_quests": quest.classname_quests,
                        "task_template_id": task_template_id,
                        "message": "Task template ID must match TT-001 format.",
                    }
                )
            if task_template_id == "TT-035":
                issues.append(
                    {
                        "code": "not_ready_task_template",
                        "quest_index": index,
                        "classname_quests": quest.classname_quests,
                        "task_template_id": task_template_id,
                        "message": "TT-035 is marked as not_ready and must not be used.",
                    }
                )
            if task_template_id in CRAFT_LIKE_TEMPLATE_IDS:
                craft_like_quests.append(
                    {
                        "quest_index": index,
                        "quest_number": quest.quest_number if quest.quest_number is not None else index,
                        "classname_quests": quest.classname_quests,
                        "task_template_id": task_template_id,
                    }
                )

    craft_like_quests.sort(key=lambda item: int(item["quest_number"]))
    previous: dict[str, Any] | None = None
    for current in craft_like_quests:
        if previous is not None:
            distance = int(current["quest_number"]) - int(previous["quest_number"])
            if distance < MIN_CRAFT_LIKE_QUEST_SPACING:
                issues.append(
                    {
                        "code": "craft_like_tasks_too_close",
                        "quest_index": current["quest_index"],
                        "classname_quests": current["classname_quests"],
                        "task_template_id": current["task_template_id"],
                        "previous_classname_quests": previous["classname_quests"],
                        "previous_task_template_id": previous["task_template_id"],
                        "min_quest_spacing": MIN_CRAFT_LIKE_QUEST_SPACING,
                        "message": "TT-002 and TT-033 are craft-like templates and must not be placed close together; use roughly one craft-like task per 4 quests.",
                    }
                )
        previous = current

    if stage2_text is not None:
        issues.extend(find_stage2_text_issues(quests, parse_stage2_story_text(stage2_text)))

    return issues


def build_quest_plan(text: str, stage2_text: str | None = None) -> dict[str, Any]:
    quests = parse_stage3_text(text)
    quest_json = [quest.to_json() for quest in quests]
    issues = find_quest_issues(quests, stage2_text=stage2_text)
    return {
        "quests": quest_json,
        "issues": issues,
        "summary": {
            "quests_found": len(quests),
            "tasks_found": sum(len(quest["tasks"]) for quest in quest_json),
            "issues": len(issues),
        },
    }


def render_preview(quest_plan: dict[str, Any]) -> str:
    lines: list[str] = [
        "# Quest Plan Preview",
        "",
        f"Quests found: {quest_plan['summary']['quests_found']}",
        f"Tasks found: {quest_plan['summary'].get('tasks_found', 0)}",
        f"Issues: {quest_plan['summary']['issues']}",
        "",
    ]

    for index, quest in enumerate(quest_plan["quests"], start=1):
        title = quest.get("title_quest") or "Без названия"
        lines.extend(
            [
                f"## Quest {quest.get('quest_number') or index} — {title}",
                "",
                f"- classname_quests: `{quest.get('classname_quests')}`",
                f"- character: {quest.get('character') or ''}",
                f"- task_numbers: {', '.join(str(number) for number in quest.get('task_numbers', []))}",
                "",
                "| № | Template ID | Template name | Task type |",
                "|---|-------------|---------------|-----------|",
            ]
        )
        for task in quest.get("tasks", []):
            lines.append(
                "| "
                f"{task.get('task_number') or ''} | "
                f"`{task.get('task_template_id') or ''}` | "
                f"{task.get('task_template_name') or ''} | "
                f"`{task.get('task_type') or ''}` |"
            )
        lines.extend(
            [
                "",
                f"Description: {quest.get('description') or ''}",
                "",
                f"Congratulation: {quest.get('congratulation') or ''}",
                "",
            ]
        )

    if quest_plan["issues"]:
        lines.extend(["## Issues", ""])
        for issue in quest_plan["issues"]:
            lines.append(
                f"- `{issue['code']}` quest={issue.get('classname_quests')} field={issue.get('field', '')}: {issue['message']}"
            )
        lines.append("")

    return "\n".join(lines)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_file(
    input_path: Path,
    output_json_path: Path,
    output_preview_path: Path,
    stage2_path: Path | None = None,
) -> dict[str, Any]:
    stage2_text = read_text(stage2_path) if stage2_path is not None and stage2_path.exists() else None
    quest_plan = build_quest_plan(read_text(input_path), stage2_text=stage2_text)
    write_json(output_json_path, quest_plan)
    output_preview_path.parent.mkdir(parents=True, exist_ok=True)
    output_preview_path.write_text(render_preview(quest_plan), encoding="utf-8")
    return quest_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse stage 3 quest text into QuestPlan JSON.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Stage 3 text input file. Default: input/stage3_quests.txt",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON_PATH,
        help="Output quest plan JSON path.",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=DEFAULT_OUTPUT_PREVIEW_PATH,
        help="Output human-readable preview path.",
    )
    parser.add_argument(
        "--stage2",
        type=Path,
        default=None,
        help="Optional Stage 2 text file. When provided, description/congratulation are validated against Старт/Завершение.",
    )
    args = parser.parse_args(argv)

    (PROJECT_ROOT / "input").mkdir(exist_ok=True)
    (PROJECT_ROOT / "output").mkdir(exist_ok=True)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Создай input/stage3_quests.txt или передай путь к файлу этапа 3 первым аргументом.")
        return 1

    quest_plan = parse_file(args.input, args.output_json, args.preview, args.stage2)
    print(f"quests found: {quest_plan['summary']['quests_found']}")
    print(f"tasks found: {quest_plan['summary']['tasks_found']}")
    print(f"issues: {quest_plan['summary']['issues']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    return 0 if quest_plan["summary"]["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
