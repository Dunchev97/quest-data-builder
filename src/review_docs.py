from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from .campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir
except ImportError:
    from campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASK_TEMPLATES_PATH = PROJECT_ROOT / "data" / "task_templates.json"
REVIEW_DIR = "review"
STAGE_REVIEW_FILES = {
    "1": "stage1_review.md",
    "2": "stage2_review.md",
    "3": "stage3_review.md",
    "4": "stage4_review.md",
    "5": "stage5_review.md",
    "6": "stage6_review.xlsx",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_stage(stage: str | int) -> str:
    stage_text = str(stage).strip()
    if stage_text not in STAGE_REVIEW_FILES:
        raise ValueError(f"unsupported review stage: {stage_text}")
    return stage_text


def review_path(campaign_id: str, pack_id: str, stage: str | int, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    stage_text = normalize_stage(stage)
    return pack_dir(campaign_id, pack_id, campaigns_dir) / REVIEW_DIR / STAGE_REVIEW_FILES[stage_text]


def pack_artifact(campaign_id: str, pack_id: str, filename: str, campaigns_dir: Path) -> Path:
    return pack_dir(campaign_id, pack_id, campaigns_dir) / filename


def strip_fences(value: str) -> str:
    value = value.strip()
    if value.startswith("```") and value.endswith("```"):
        lines = value.splitlines()
        if len(lines) >= 2:
            return "\n".join(lines[1:-1]).strip()
    return value


def compact(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())


def split_section(text: str, heading: str, level: int = 2) -> str:
    pattern = re.compile(rf"^{'#' * level}\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if match is None:
        return ""
    next_heading = re.search(rf"^{'#' * level}\s+", text[match.end() :], re.MULTILINE)
    end = match.end() + next_heading.start() if next_heading else len(text)
    return text[match.end() : end].strip()


def heading_blocks(text: str, level: int = 3) -> list[tuple[str, str]]:
    pattern = re.compile(rf"^{'#' * level}\s+(.+?)\s*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1).strip(), text[match.end() : end].strip()))
    return blocks


def clean_heading_title(heading: str) -> str:
    return re.sub(r"^\d+(?:\.\d+)?\.\s*", "", heading).strip()


def parse_fields(body: str, labels: list[str]) -> dict[str, str]:
    fields: dict[str, str] = {}
    label_set = set(labels)
    current: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_lines, current
        if current is not None:
            fields[current] = strip_fences("\n".join(current_lines).strip())
        current = None
        current_lines = []

    label_pattern = re.compile(r"^([A-Za-zА-Яа-яЁё0-9 _/.-]+):\s*(.*)$")
    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        match = label_pattern.match(line)
        if match and match.group(1).strip() in label_set:
            flush()
            current = match.group(1).strip()
            current_lines = [match.group(2).strip()]
            continue
        if current is not None:
            current_lines.append(line)
    flush()
    return fields


def parse_stage1_source(text: str) -> dict[str, Any]:
    story_match = re.search(r"Основной сюжет:\s*(.*?)(?:\n\s*Роль игрока:|\n\s*Персонажи истории:|\Z)", text, re.S)
    player_role_match = re.search(r"Роль игрока:\s*(.*?)(?:\n\s*Персонажи истории:|\Z)", text, re.S)
    characters_match = re.search(r"Персонажи истории:\s*(.*?)(?:\n\s*Задания сюжета:|\Z)", text, re.S)
    quests_match = re.search(r"Задания сюжета:\s*(.*?)(?:\n\s*Конец этапа 1\.?|\Z)", text, re.S)

    characters: list[dict[str, str]] = []
    for paragraph in re.split(r"\n\s*\n", (characters_match.group(1) if characters_match else "").strip()):
        paragraph = compact(paragraph)
        if not paragraph:
            continue
        name, sep, description = re.split(r"\s+[—-]\s+", paragraph, maxsplit=1)[0], "", ""
        parts = re.split(r"\s+[—-]\s+", paragraph, maxsplit=1)
        if len(parts) == 2:
            name, description = parts
            sep = "ok"
        if sep:
            characters.append({"name": name.strip("* "), "description": description.strip()})

    quests: list[dict[str, str]] = []
    quest_text = quests_match.group(1).strip() if quests_match else ""
    quest_pattern = re.compile(r"^\s*(\d+)\.\s*(.+?)\s*$", re.MULTILINE)
    matches = list(quest_pattern.finditer(quest_text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(quest_text)
        header = match.group(2).strip()
        body = quest_text[match.end() : end].strip()
        character = ""
        title = header
        if ":" in header:
            character, title = [part.strip() for part in header.split(":", 1)]
        summary_match = re.search(r"Суть задания:\s*(.*)", body, re.S)
        quests.append(
            {
                "number": match.group(1),
                "title": title,
                "character": character,
                "summary": compact(summary_match.group(1) if summary_match else body),
            }
        )

    return {
        "story": (story_match.group(1).strip() if story_match else text.strip()),
        "player_role": (player_role_match.group(1).strip() if player_role_match else ""),
        "characters": characters,
        "quests": quests,
    }


def parse_stage1_review(text: str) -> dict[str, Any]:
    characters: list[dict[str, str]] = []
    for line in split_section(text, "Персонажи").splitlines():
        line = line.strip().lstrip("-").strip()
        if not line:
            continue
        line = re.sub(r"^\*\*(.+?)\*\*\s*[:—-]\s*", r"\1 — ", line)
        parts = re.split(r"\s+[—-]\s+|:\s+", line, maxsplit=1)
        if len(parts) == 2:
            characters.append({"name": parts[0].strip("* "), "description": parts[1].strip()})

    quests: list[dict[str, str]] = []
    for heading, body in heading_blocks(split_section(text, "Квесты"), level=3):
        fields = parse_fields(body, ["Персонаж", "Суть"])
        quests.append(
            {
                "title": clean_heading_title(heading),
                "character": fields.get("Персонаж", "").strip(),
                "summary": fields.get("Суть", "").strip(),
            }
        )
    return {
        "story": split_section(text, "Основной сюжет").strip(),
        "player_role": split_section(text, "Роль игрока").strip(),
        "characters": characters,
        "quests": quests,
    }


def render_stage1_review(data: dict[str, Any]) -> str:
    lines = ["# Контрольный документ. Этап 1", "", "## Основной сюжет", "", data.get("story", "").strip(), ""]
    if data.get("player_role"):
        lines.extend(["## Роль игрока", "", data.get("player_role", "").strip(), ""])
    lines.extend(["## Персонажи", ""])
    for character in data.get("characters", []):
        lines.append(f"- {character.get('name', '').strip()} — {character.get('description', '').strip()}")
    lines.extend(["", "## Квесты", ""])
    for index, quest in enumerate(data.get("quests", []), start=1):
        lines.extend(
            [
                f"### {index}. {quest.get('title', '').strip()}",
                f"Персонаж: {quest.get('character', '').strip()}",
                f"Суть: {quest.get('summary', '').strip()}",
                "",
            ]
        )
    return "\n".join(lines)


def render_stage1_source(data: dict[str, Any]) -> str:
    lines = ["Основной сюжет:", data.get("story", "").strip(), "", "Персонажи истории:", ""]
    if data.get("player_role"):
        lines = ["Основной сюжет:", data.get("story", "").strip(), "", "Роль игрока:", data.get("player_role", "").strip(), "", "Персонажи истории:", ""]
    for character in data.get("characters", []):
        lines.append(f"{character.get('name', '').strip()} — {character.get('description', '').strip()}")
        lines.append("")
    lines.extend(["Задания сюжета:", ""])
    for index, quest in enumerate(data.get("quests", []), start=1):
        prefix = f"{quest.get('character', '').strip()}: " if quest.get("character") else ""
        lines.extend(
            [
                f"{index}. {prefix}{quest.get('title', '').strip()}",
                f"Суть задания: {quest.get('summary', '').strip()}",
                "",
            ]
        )
    lines.append("Конец этапа 1.")
    return "\n".join(lines)


def parse_stage2_source(text: str) -> list[dict[str, str]]:
    quests: list[dict[str, str]] = []
    header_pattern = re.compile(r"^\s*(\d+)\.\s*(.+?)\s*$", re.MULTILINE)
    matches = list(header_pattern.finditer(text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        header = match.group(2).strip()
        body = text[match.end() : end].strip()
        character = ""
        title = header
        if ":" in header:
            character, title = [part.strip() for part in header.split(":", 1)]
        fields = parse_fields(body, ["Суть", "Старт", "Завершение"])
        if "Суть" not in fields:
            fields = parse_fields(body.replace("Суть задания:", "Суть:"), ["Суть", "Старт", "Завершение"])
        quests.append(
            {
                "title": title,
                "character": character,
                "summary": fields.get("Суть", ""),
                "start": fields.get("Старт", ""),
                "finish": fields.get("Завершение", ""),
            }
        )
    return quests


def stage2_summary_lookup(campaign_id: str, pack_id: str, campaigns_dir: Path) -> dict[str, str]:
    stage2_path = pack_artifact(campaign_id, pack_id, "stage2_story.txt", campaigns_dir)
    summaries: dict[str, str] = {}
    for quest in parse_stage2_source(read_text(stage2_path)):
        title_key = compact(quest.get("title")).casefold()
        summary = compact(quest.get("summary"))
        if title_key and summary:
            summaries[title_key] = summary
    return summaries


def parse_stage2_review(text: str) -> list[dict[str, str]]:
    quests: list[dict[str, str]] = []
    for heading, body in heading_blocks(split_section(text, "Квесты"), level=3):
        fields = parse_fields(body, ["Персонаж", "Суть", "Старт", "Завершение"])
        quests.append(
            {
                "title": clean_heading_title(heading),
                "character": fields.get("Персонаж", ""),
                "summary": fields.get("Суть", ""),
                "start": fields.get("Старт", ""),
                "finish": fields.get("Завершение", ""),
            }
        )
    return quests


def render_stage2_review(quests: list[dict[str, str]]) -> str:
    lines = ["# Контрольный документ. Этап 2", "", "## Квесты", ""]
    for index, quest in enumerate(quests, start=1):
        lines.extend(
            [
                f"### {index}. {quest.get('title', '').strip()}",
                f"Персонаж: {quest.get('character', '').strip()}",
                f"Суть: {quest.get('summary', '').strip()}",
                f"Старт: {quest.get('start', '').strip()}",
                f"Завершение: {quest.get('finish', '').strip()}",
                "",
            ]
        )
    return "\n".join(lines)


def render_stage2_source(quests: list[dict[str, str]]) -> str:
    lines: list[str] = []
    for index, quest in enumerate(quests, start=1):
        prefix = f"{quest.get('character', '').strip()}: " if quest.get("character") else ""
        lines.extend(
            [
                f"{index}. {prefix}{quest.get('title', '').strip()}",
                f"Суть: {quest.get('summary', '').strip()}",
                f"Старт: {quest.get('start', '').strip()}",
                f"Завершение: {quest.get('finish', '').strip()}",
                "",
            ]
        )
    lines.append("Конец этапа 2.")
    return "\n".join(lines)


def load_template_catalog(path: Path = TASK_TEMPLATES_PATH) -> dict[str, Any]:
    data = read_json(path)
    templates = data.get("templates", [])
    by_id = {str(item.get("id")): item for item in templates if item.get("id")}
    by_name = {compact(item.get("name_ru")).casefold(): item for item in templates if item.get("name_ru")}
    return {"by_id": by_id, "by_name": by_name}


def template_label(task: dict[str, Any]) -> str:
    template_id = task.get("task_template_id") or task.get("resolved_template_id") or ""
    name = task.get("task_template_name") or task.get("canonical_task_template_name") or ""
    return compact(f"{template_id} {name}")


def render_task_template_reference(path: Path = TASK_TEMPLATES_PATH) -> list[str]:
    data = read_json(path)
    lines = ["## Справочник Task Templates", ""]
    for template in data.get("templates", []):
        template_id = str(template.get("id") or "").strip()
        name_ru = str(template.get("name_ru") or "").strip()
        lines.append(compact(f"{template_id} {name_ru}"))
    lines.append("")
    return lines


def parse_template_entry(entry: str, catalog: dict[str, Any]) -> dict[str, str]:
    entry = entry.strip().strip("`")
    id_match = re.search(r"\bTT-\d{3}\b", entry)
    template: dict[str, Any] | None = None
    if id_match:
        template = catalog["by_id"].get(id_match.group(0))
    if template is None:
        template = catalog["by_name"].get(compact(entry).casefold())
    if template is None and id_match:
        return {
            "task_template_id": id_match.group(0),
            "task_template_name": compact(entry.replace(id_match.group(0), "")),
            "task_type": "",
        }
    if template is None:
        return {"task_template_id": "", "task_template_name": entry, "task_type": ""}
    return {
        "task_template_id": str(template.get("id") or ""),
        "task_template_name": str(template.get("name_ru") or ""),
        "task_type": str(template.get("task_type") or ""),
    }


def load_quest_plan_for_review(campaign_id: str, pack_id: str, campaigns_dir: Path) -> dict[str, Any]:
    for filename in ("quest_plan.resolved.json", "quest_plan.json"):
        path = pack_artifact(campaign_id, pack_id, filename, campaigns_dir)
        if path.exists():
            return read_json(path)
    stage3_path = pack_artifact(campaign_id, pack_id, "stage3_quests.txt", campaigns_dir)
    if stage3_path.exists():
        try:
            from .parse_stage3 import build_quest_plan
        except ImportError:
            from parse_stage3 import build_quest_plan

        return build_quest_plan(read_text(stage3_path))
    return {"quests": []}


def render_stage3_review(quest_plan: dict[str, Any]) -> str:
    lines = ["# Контрольный документ. Этап 3", ""]
    lines.extend(render_task_template_reference())
    lines.extend(["## Квесты", ""])
    for index, quest in enumerate(quest_plan.get("quests", []), start=1):
        templates = " / ".join(template_label(task) for task in quest.get("tasks", []))
        lines.extend(
            [
                f"### {quest.get('quest_number') or index}. {quest.get('title_quest') or ''}",
                f"Персонаж: {quest.get('character') or ''}",
                f"Шаблоны: {templates}",
                f"Старт: {quest.get('description') or ''}",
                f"Завершение: {quest.get('congratulation') or ''}",
                "",
            ]
        )
    return "\n".join(lines)


def parse_stage3_review(text: str, base_plan: dict[str, Any]) -> dict[str, Any]:
    catalog = load_template_catalog()
    base_quests = list(base_plan.get("quests", []))
    quests: list[dict[str, Any]] = []
    blocks = heading_blocks(split_section(text, "Квесты"), level=3)
    for index, (heading, body) in enumerate(blocks):
        base = dict(base_quests[index]) if index < len(base_quests) else {}
        fields = parse_fields(body, ["Персонаж", "Шаблоны", "Старт", "Завершение"])
        entries = [item.strip() for item in fields.get("Шаблоны", "").split("/") if item.strip()]
        task_numbers = list(base.get("task_numbers") or [task.get("task_number") for task in base.get("tasks", [])])
        while len(task_numbers) < len(entries):
            task_numbers.append((task_numbers[-1] if task_numbers else 0) + 1)
        parsed_templates = [parse_template_entry(entry, catalog) for entry in entries]
        tasks = [
            {
                "task_number": task_numbers[item_index] if item_index < len(task_numbers) else item_index + 1,
                **template,
            }
            for item_index, template in enumerate(parsed_templates)
        ]
        quest = {
            **base,
            "title_quest": clean_heading_title(heading),
            "quest_number": base.get("quest_number") or index + 1,
            "character": fields.get("Персонаж", base.get("character") or ""),
            "description": fields.get("Старт", base.get("description") or ""),
            "congratulation": fields.get("Завершение", base.get("congratulation") or ""),
            "task_numbers": [task["task_number"] for task in tasks],
            "task_template_ids": [task["task_template_id"] for task in tasks],
            "task_template_names": [task["task_template_name"] for task in tasks],
            "task_types": [task["task_type"] for task in tasks],
            "tasks": tasks,
        }
        quests.append(quest)
    return {"quests": quests}


def render_stage3_source(quest_plan: dict[str, Any], campaign_id: str, pack_id: str) -> str:
    lines = [f"{campaign_id}, {pack_id}, {len(quest_plan.get('quests', []))} квестов", ""]
    for quest in quest_plan.get("quests", []):
        tasks = quest.get("tasks", [])
        lines.extend(
            [
                f"Classname quests: {quest.get('classname_quests') or ''}",
                f"title_quest: {quest.get('title_quest') or ''}",
                f"№ quest: {quest.get('quest_number') or ''}",
                "№ task: " + " ".join(str(task.get("task_number") or "") for task in tasks).strip(),
                "Task template ID: " + " / ".join(str(task.get("task_template_id") or "") for task in tasks),
                "Task template name: " + " / ".join(str(task.get("task_template_name") or "") for task in tasks),
                "Task type: " + " / ".join(str(task.get("task_type") or "") for task in tasks),
                f"description: \"{quest.get('description') or ''}\"",
                "Tasks:",
                "[пусто на этом этапе]",
                f"congratulation: \"{quest.get('congratulation') or ''}\"",
                f"Character: {quest.get('character') or ''}",
                "",
            ]
        )
    return "\n".join(lines)


def choice_index(choices: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    result: dict[tuple[str, int], dict[str, Any]] = {}
    for quest in choices.get("quests", []):
        classname = str(quest.get("classname_quests") or "")
        for task in quest.get("tasks", []):
            number = task.get("task_number")
            if classname and isinstance(number, int):
                result[(classname, number)] = task
    return result


def quest_index(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(quest.get("classname_quests") or ""): quest for quest in data.get("quests", [])}


def task_lookup(data: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    result: dict[tuple[str, int], dict[str, Any]] = {}
    for quest in data.get("quests", []):
        classname = str(quest.get("classname_quests") or "")
        for task in quest.get("tasks", []):
            number = task.get("task_number")
            if classname and isinstance(number, int):
                result[(classname, number)] = task
    return result


def candidate_display(candidate: dict[str, Any] | None) -> str:
    if not candidate:
        return ""
    pairs = (
        ("collection_title", "collection_classname"),
        ("flower_title", "flower_classname"),
        ("garbage_title", "garbage_classname"),
        ("location_title", "location_classname"),
    )
    for title_key, code_key in pairs:
        title = str(candidate.get(title_key) or "").strip()
        code = str(candidate.get(code_key) or "").strip()
        if title and code:
            return f"{title}.{code}"
    candidate_id = str(candidate.get("candidate_id") or "").strip()
    return candidate_id


def candidate_display_code(value: str) -> str:
    text = value.strip()
    if "." not in text:
        return text
    code = text.rsplit(".", 1)[1].strip()
    return code.split()[0].strip()


def candidate_by_display(context_task: dict[str, Any], value: str) -> dict[str, Any] | None:
    text = value.strip()
    code = candidate_display_code(text)
    if not code:
        return None
    for candidate in context_task.get("candidates", []):
        if candidate_display(candidate).strip() == text:
            return candidate
    for candidate in context_task.get("candidates", []):
        for key in ("collection_classname", "flower_classname", "garbage_classname", "location_classname"):
            if str(candidate.get(key) or "").strip() == code:
                return candidate
    return None


def candidate_by_selected_id(context_task: dict[str, Any], selected_candidate_id: str) -> dict[str, Any] | None:
    for candidate in context_task.get("candidates", []):
        if str(candidate.get("candidate_id") or "") == selected_candidate_id:
            return candidate
    return None


def title_from_choice_or_task(choice: dict[str, Any], task: dict[str, Any]) -> str:
    for key in ("item_title", "craft_title", "hog_item_title", "resource_title", "title_item"):
        value = str(choice.get(key) or "").strip()
        if value:
            return value
    task_object = task.get("task_object") if isinstance(task.get("task_object"), dict) else {}
    title = str(task_object.get("title") or "").strip()
    for prefix in ("Найди ", "Получи ", "Создай ", "Передай ", "Попроси у друзей "):
        if title.startswith(prefix):
            return title[len(prefix) :].strip()
    return title


def lower_first(value: str) -> str:
    text = value.strip()
    return text[:1].lower() + text[1:] if text else text


def upper_first(value: str) -> str:
    text = value.strip()
    return text[:1].upper() + text[1:] if text else text


def short_stage4_title(value: str) -> str:
    text = upper_first(simple_accusative_to_nominative(value))
    words = text.split()
    stopwords = {"для", "из", "от", "у", "в", "во", "на", "с", "со", "при", "по"}
    if any(word.lower() in stopwords for word in words):
        words = words[: next(index for index, word in enumerate(words) if word.lower() in stopwords)]
    if len(words) > 2:
        second = words[1].lower()
        modifier_endings = ("ый", "ий", "ая", "яя", "ое", "ее", "ой", "ей", "ого", "его", "ому", "ему", "ым", "им")
        words = [words[0], words[-1]] if second.endswith(modifier_endings) else words[:2]
    return " ".join(words) or text


def simple_accusative_to_nominative(value: str) -> str:
    words = value.strip().rstrip(".").split()
    normalized: list[str] = []
    for word in words:
        lower = word.lower()
        if lower.endswith("ую"):
            normalized.append(word[:-2] + ("ая" if word[-2:].islower() else "ая"))
        elif lower.endswith("юю"):
            normalized.append(word[:-2] + "яя")
        elif lower.endswith("чку") or lower.endswith("жку") or lower.endswith("шку") or lower.endswith("щку"):
            normalized.append(word[:-1] + "а")
        elif lower.endswith("ку"):
            normalized.append(word[:-1] + "а")
        elif lower.endswith("лю") or lower.endswith("рю"):
            normalized.append(word[:-1] + "я")
        elif lower.endswith("ию"):
            normalized.append(word[:-2] + "ия")
        elif lower.endswith("у"):
            normalized.append(word[:-1] + "а")
        elif lower.endswith("ю"):
            normalized.append(word[:-1] + "я")
        else:
            normalized.append(word)
    return " ".join(normalized)


def simple_nominative_to_accusative(value: str) -> str:
    words = value.strip().rstrip(".").split()
    converted: list[str] = []
    has_feminine_modifier = any(word.lower().endswith(("ая", "яя")) for word in words[:-1])
    last_index = len(words) - 1
    for index, word in enumerate(words):
        lower = word.lower()
        if lower.endswith("ая"):
            converted.append(word[:-2] + "ую")
        elif lower.endswith("яя"):
            converted.append(word[:-2] + "юю")
        elif index == last_index and (
            lower.endswith("чка") or lower.endswith("жка") or lower.endswith("шка") or lower.endswith("щка")
        ):
            converted.append(word[:-1] + "у")
        elif index == last_index and lower.endswith("ка"):
            converted.append(word[:-1] + "у")
        elif index == last_index and (lower.endswith("ля") or lower.endswith("ря")):
            converted.append(word[:-1] + "ю")
        elif index == last_index and lower.endswith("ия"):
            converted.append(word[:-2] + "ию")
        elif index == last_index and lower.endswith("а") and (len(words) == 1 or has_feminine_modifier):
            converted.append(word[:-1] + "у")
        elif index == last_index and lower.endswith("я") and (len(words) == 1 or has_feminine_modifier):
            converted.append(word[:-1] + "ю")
        else:
            converted.append(word)
    return lower_first(" ".join(converted))


def candidate_title(candidate: dict[str, Any] | None) -> str:
    if not candidate:
        return ""
    for key in ("collection_title", "flower_title", "garbage_title", "source_title", "location_title"):
        value = str(candidate.get(key) or "").strip()
        if value:
            return value
    return ""


def display_item_for_review(choice: dict[str, Any], task: dict[str, Any]) -> str:
    source = str(choice.get("item_title_nominative") or "").strip()
    if source:
        return source
    title = title_from_choice_or_task(choice, task)
    return upper_first(simple_accusative_to_nominative(title))


def resource_title_for_review(choice: dict[str, Any], task: dict[str, Any], selected: dict[str, Any] | None = None) -> str:
    source = str(choice.get("craft_title") or choice.get("item_title") or choice.get("item_title_nominative") or "").strip()
    if not source:
        source = candidate_title(selected) or title_from_choice_or_task(choice, task)
    return short_stage4_title(source)


def task_text_item_for_review(choice: dict[str, Any], task: dict[str, Any], selected: dict[str, Any] | None = None) -> str:
    source = str(choice.get("item_title_accusative") or "").strip()
    if source and choice.get("craft_title") and choice.get("item_title"):
        old_auto = upper_first(simple_nominative_to_accusative(str(choice.get("item_title") or "")))
        if source.casefold() == old_auto.casefold():
            source = ""
    if source:
        return upper_first(source)
    source = str(choice.get("craft_title") or choice.get("item_title_nominative") or "").strip() or candidate_title(selected) or display_item_for_review(choice, task)
    return upper_first(simple_nominative_to_accusative(short_stage4_title(source)))


def default_hog_location_tags(template_id: str) -> str:
    if template_id == "TT-003":
        return "rnd_world"
    if template_id == "TT-005":
        return "rnd_old_home,rnd_new_home,rnd_big_home"
    return "rnd_big_home"


def hog_location_tags_reference_lines() -> list[str]:
    return [
        "Стандартные кандидаты:",
        "HOG в локациях дома - rnd_old_home,rnd_new_home,rnd_big_home",
        "HOG в мире - rnd_world",
        "HOG на даче - farm_room",
    ]


def selected_interactive_ingredients(campaign_id: str, campaigns_dir: Path) -> list[tuple[str, str]]:
    preview_path = campaigns_dir / campaign_id / "interactive_objects.preview.md"
    if not preview_path.exists():
        return []
    result: list[tuple[str, str]] = []
    pattern = re.compile(r"^-\s+`[^`]+`\s+->\s+`([^`]+)`:\s*(.+?)\s*$")
    for line in read_text(preview_path).splitlines():
        match = pattern.match(line.strip())
        if match:
            classname = match.group(1).strip()
            title = match.group(2).strip()
            result.append((title, classname))
    if len(result) >= 3:
        return result[1:3]
    return result[:2]


def craft_ingredients_lines(
    quest: dict[str, Any],
    choices_by_key: dict[tuple[str, int], dict[str, Any]],
    campaign_id: str,
    campaigns_dir: Path,
) -> list[str]:
    classname = str(quest.get("classname_quests") or "")
    tasks = list(quest.get("tasks", []))
    ingredients: list[tuple[str, str]] = []
    for task in tasks[1:3]:
        task_number = task.get("task_number")
        choice = choices_by_key.get((classname, task_number), {}) if isinstance(task_number, int) else {}
        title = display_item_for_review(choice, task)
        template_id = str(task.get("task_template_id") or "")
        suffix = "ASK" if template_id == "TT-008" else "PER" if template_id == "TT-009" else "GR"
        if title:
            ingredients.append((title, suffix))
    ingredients.extend(selected_interactive_ingredients(campaign_id, campaigns_dir))
    lines = ["Ингредиенты:"]
    for index, (title, classname_or_kind) in enumerate(ingredients[:4], start=1):
        lines.append(f"Ингредиент {index} - {title}.{classname_or_kind}")
    return lines


def render_stage4_review(campaign_id: str, pack_id: str, campaigns_dir: Path) -> str:
    context_path = pack_artifact(campaign_id, pack_id, "context_pack.json", campaigns_dir)
    filled_path = pack_artifact(campaign_id, pack_id, "filled_tasks.json", campaigns_dir)
    choices_path = pack_artifact(campaign_id, pack_id, "task_choices.json", campaigns_dir)
    source = read_json(filled_path) if filled_path.exists() else read_json(context_path)
    context = read_json(context_path) if context_path.exists() else source
    choices = read_json(choices_path) if choices_path.exists() else {"quests": []}
    choices_by_key = choice_index(choices)
    context_tasks_by_key = task_lookup(context)
    summaries_by_title = stage2_summary_lookup(campaign_id, pack_id, campaigns_dir)
    lines = ["# Контрольный документ. Этап 4", "", "## Квесты", ""]
    for quest_index, quest in enumerate(source.get("quests", []), start=1):
        quest_classname = str(quest.get("classname_quests") or "")
        quest_title = str(quest.get("title_quest") or "")
        lines.append(f"### {quest.get('quest_number') or quest_index}. {quest_title}")
        summary = summaries_by_title.get(compact(quest_title).casefold())
        if summary:
            lines.append(f"Суть: {summary}")
        lines.append("")
        for task_index, task in enumerate(quest.get("tasks", []), start=1):
            task_number = task.get("task_number")
            choice = choices_by_key.get((str(quest.get("classname_quests") or ""), task_number), {})
            context_task = context_tasks_by_key.get((quest_classname, task_number), {})
            template_id = str(task.get("task_template_id") or "")
            selected_id = str(choice.get("selected_candidate_id") or task.get("selected_candidate_id") or "")
            selected = candidate_by_selected_id(context_task, selected_id)
            task_text_line_written = False
            lines.append(f"#### {quest_index}.{task_index}. {task.get('task_template_name') or task.get('task_template_id') or ''}")
            if template_id == "TT-001":
                lines.append(f"Реплика: {choice.get('dialogue_replica') or task.get('dialogue_replica') or ''}")
                if choice.get("person"):
                    lines.append(f"Персонаж в действии: {choice.get('person') or ''}")
            elif template_id in {"TT-002", "TT-033"}:
                lines.append(f"Название: {resource_title_for_review(choice, task, selected)}")
                lines.append(f"В тексте задания: {task_text_item_for_review(choice, task, selected)}")
                task_text_line_written = True
                lines.extend(craft_ingredients_lines(quest, choices_by_key, campaign_id, campaigns_dir))
            elif template_id in {"TT-008", "TT-009"}:
                lines.append(f"Название: {resource_title_for_review(choice, task, selected)}")
                lines.append(f"Предмет: {display_item_for_review(choice, task)}")
                lines.append(f"В тексте задания: {task_text_item_for_review(choice, task, selected)}")
                task_text_line_written = True
            elif template_id in {"TT-003", "TT-004", "TT-005", "TT-006", "TT-007"}:
                lines.append(f"Название: {resource_title_for_review(choice, task, selected)}")
                lines.append(f"Предмет: {display_item_for_review(choice, task)}")
                lines.append(f"В тексте задания: {task_text_item_for_review(choice, task, selected)}")
                task_text_line_written = True
                lines.append(f"Тэги локаций: {choice.get('location_tags') or default_hog_location_tags(template_id)}")
                lines.extend(hog_location_tags_reference_lines())
            elif choice.get("item_title"):
                lines.append(f"Название: {resource_title_for_review(choice, task, selected)}")
                lines.append(f"В тексте задания: {task_text_item_for_review(choice, task, selected)}")
                task_text_line_written = True
            if context_task.get("candidates"):
                if not task_text_line_written and template_id not in {"TT-026", "TT-027", "TT-028", "TT-029", "TT-030", "TT-031", "TT-032"}:
                    lines.append(f"В тексте задания: {task_text_item_for_review(choice, task, selected)}")
                lines.append(f"Выбранный кандидат: {candidate_display(selected) or selected_id}")
                lines.append("Кандидаты:")
                for candidate in context_task.get("candidates", []):
                    lines.append(candidate_display(candidate))
            if choice.get("riddle"):
                lines.append(f"Загадка: {choice.get('riddle') or ''}")
            lines.append("")
    return "\n".join(lines)


def parse_stage4_review(text: str, current_choices: dict[str, Any], context_pack: dict[str, Any] | None = None) -> dict[str, Any]:
    updated = json.loads(json.dumps(current_choices, ensure_ascii=False))
    context_tasks_by_key = task_lookup(context_pack or {})
    quest_blocks = heading_blocks(split_section(text, "Квесты"), level=3)
    for quest_index, (_, quest_body) in enumerate(quest_blocks):
        if quest_index >= len(updated.get("quests", [])):
            continue
        quest = updated["quests"][quest_index]
        task_blocks = heading_blocks(quest_body, level=4)
        for task_index, (_, task_body) in enumerate(task_blocks):
            if task_index >= len(quest.get("tasks", [])):
                continue
            fields = parse_fields(
                task_body,
                [
                    "Реплика",
                    "Персонаж в действии",
                    "Название",
                    "Предмет",
                    "В тексте задания",
                    "Тэги локаций",
                    "Выбранный кандидат",
                    "Кандидаты",
                    "Загадка",
                    "Ингредиенты",
                ],
            )
            task = quest["tasks"][task_index]
            context_task = context_tasks_by_key.get((str(quest.get("classname_quests") or ""), task.get("task_number")), {})
            original_task = json.loads(json.dumps(task, ensure_ascii=False))
            original_selected_id = str(original_task.get("selected_candidate_id") or "")
            original_selected = candidate_by_selected_id(context_task, original_selected_id)
            original_name = resource_title_for_review(original_task, context_task, original_selected)
            original_task_text = task_text_item_for_review(original_task, context_task, original_selected)
            field_map = {
                "Реплика": "dialogue_replica",
                "Персонаж в действии": "person",
                "Загадка": "riddle",
            }
            for label, key in field_map.items():
                if label in fields:
                    value = fields[label].strip()
                    if value:
                        task[key] = value
                    elif key in task:
                        task.pop(key)
            if "Выбранный кандидат" in fields:
                value = fields["Выбранный кандидат"].strip()
                if value:
                    candidate = candidate_by_display(context_task, value)
                    task["selected_candidate_id"] = str((candidate or {}).get("candidate_id") or value)
                elif "selected_candidate_id" in task:
                    task.pop("selected_candidate_id")
            selected_id = str(task.get("selected_candidate_id") or "")
            selected = candidate_by_selected_id(context_task, selected_id)
            subject_value = fields.get("Предмет", "").strip().rstrip(".")
            subject_nominative = upper_first(simple_accusative_to_nominative(subject_value)) if subject_value else ""
            if "Название" in fields:
                value = fields["Название"].strip().rstrip(".")
                value_title = short_stage4_title(value) if value else ""
                if value_title and (not subject_nominative or value_title.casefold() != original_name.casefold()):
                    task["item_title"] = value_title
                elif subject_nominative:
                    task["item_title"] = short_stage4_title(subject_nominative)
                elif value_title:
                    task["item_title"] = value_title
                elif "item_title" in task:
                    task.pop("item_title")
            elif subject_nominative:
                task["item_title"] = short_stage4_title(subject_nominative)
            if "В тексте задания" in fields:
                value = fields["В тексте задания"].strip().rstrip(".")
                value_text = upper_first(value) if value else ""
                if value_text and value_text.casefold() != original_task_text.casefold():
                    task["item_title_accusative"] = value_text
                elif subject_nominative:
                    task["item_title_accusative"] = upper_first(simple_nominative_to_accusative(subject_nominative))
                elif candidate_title(selected):
                    task["item_title_accusative"] = upper_first(simple_nominative_to_accusative(candidate_title(selected)))
                elif value_text:
                    task["item_title_accusative"] = value_text
                elif "item_title_accusative" in task:
                    task.pop("item_title_accusative")
            if "Предмет" in fields:
                if subject_nominative:
                    task["item_title_nominative"] = subject_nominative
                    if not task.get("item_title"):
                        task["item_title"] = short_stage4_title(subject_nominative)
                    if not task.get("item_title_accusative"):
                        task["item_title_accusative"] = upper_first(simple_nominative_to_accusative(subject_nominative))
                elif "item_title_nominative" in task:
                    task.pop("item_title_nominative")
            if "Тэги локаций" in fields:
                value = fields["Тэги локаций"].strip()
                if value:
                    task["location_tags"] = value
                elif "location_tags" in task:
                    task.pop("location_tags")
    return updated


def render_stage5_review(data: dict[str, Any]) -> str:
    source = data.get("quest_group") if isinstance(data.get("quest_group"), dict) else data
    return "\n".join(
        [
            "# Контрольный документ. Этап 5",
            "",
            "## Quest group",
            "",
            f"Название: {source.get('title') or ''}",
            f"Описание: {source.get('description') or ''}",
            f"Успех: {source.get('description_complete') or ''}",
            f"Провал: {source.get('description_spoil') or ''}",
        ]
    )


def parse_stage5_review(text: str) -> dict[str, str]:
    fields = parse_fields(split_section(text, "Quest group"), ["Название", "Описание", "Успех", "Провал"])
    return {
        "title": fields.get("Название", ""),
        "description": fields.get("Описание", ""),
        "description_complete": fields.get("Успех", ""),
        "description_spoil": fields.get("Провал", ""),
    }


def render_stage6_review(campaign_id: str, pack_id: str, campaigns_dir: Path) -> str:
    target = pack_dir(campaign_id, pack_id, campaigns_dir)
    campaign_target = campaigns_dir / campaign_id
    files = [
        target / "generated_quests.csv",
        target / "generated_actions.csv",
        target / "generated_actions.summary.json",
        campaign_target / "generated_interactive_objects.summary.json",
        campaign_target / "resource_table.csv",
        campaign_target / "resource_table.summary.json",
    ]
    lines = ["# Контрольный документ. Этап 6", "", "## Файлы", ""]
    for path in files:
        status = "ok" if path.exists() else "missing"
        lines.append(f"- {path}: {status}")
    for summary_name in ("generated_actions.summary.json",):
        summary_path = target / summary_name
        if summary_path.exists():
            summary = read_json(summary_path)
            lines.extend(["", f"## {summary_name}", ""])
            for key, value in summary.items():
                if isinstance(value, (str, int, float, bool)):
                    lines.append(f"- {key}: {value}")
    return "\n".join(lines)


def write_review_doc(campaign_id: str, pack_id: str, stage: str | int, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    stage_text = normalize_stage(stage)
    target = review_path(campaign_id, pack_id, stage_text, campaigns_dir)
    pack = pack_dir(campaign_id, pack_id, campaigns_dir)
    if stage_text == "1":
        content = render_stage1_review(parse_stage1_source(read_text(pack / "stage1_story.txt")))
    elif stage_text == "2":
        content = render_stage2_review(parse_stage2_source(read_text(pack / "stage2_story.txt")))
    elif stage_text == "3":
        content = render_stage3_review(load_quest_plan_for_review(campaign_id, pack_id, campaigns_dir))
    elif stage_text == "4":
        content = render_stage4_review(campaign_id, pack_id, campaigns_dir)
    elif stage_text == "5":
        source_path = pack / "quest_group_choices.json"
        if not source_path.exists():
            source_path = pack / "quest_group.json"
        content = render_stage5_review(read_json(source_path) if source_path.exists() else {})
    else:
        if not target.exists():
            raise FileNotFoundError(f"stage 6 workbook not found: {target}. Run stage6 first.")
        return target
    write_text(target, content)
    return target


def apply_review_doc(campaign_id: str, pack_id: str, stage: str | int, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    stage_text = normalize_stage(stage)
    source = review_path(campaign_id, pack_id, stage_text, campaigns_dir)
    if not source.exists():
        raise FileNotFoundError(f"review document not found: {source}")
    pack = pack_dir(campaign_id, pack_id, campaigns_dir)
    text = read_text(source)
    if stage_text == "1":
        target = pack / "stage1_story.txt"
        write_text(target, render_stage1_source(parse_stage1_review(text)))
    elif stage_text == "2":
        target = pack / "stage2_story.txt"
        write_text(target, render_stage2_source(parse_stage2_review(text)))
    elif stage_text == "3":
        target = pack / "stage3_quests.txt"
        plan = parse_stage3_review(text, load_quest_plan_for_review(campaign_id, pack_id, campaigns_dir))
        write_text(target, render_stage3_source(plan, campaign_id, pack_id))
    elif stage_text == "4":
        target = pack / "task_choices.json"
        choices = read_json(target) if target.exists() else {"quests": []}
        context_path = pack / "context_pack.json"
        context_pack = read_json(context_path) if context_path.exists() else {"quests": []}
        write_json(target, parse_stage4_review(text, choices, context_pack))
    elif stage_text == "5":
        target = pack / "quest_group_choices.json"
        write_json(target, parse_stage5_review(text))
    else:
        raise ValueError("stage 6 review is read-only")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or apply user-facing quest review documents.")
    parser.add_argument("command", choices=["write", "apply"])
    parser.add_argument("--campaign", required=True)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    args = parser.parse_args(argv)
    try:
        if args.command == "write":
            path = write_review_doc(args.campaign, args.pack, args.stage, args.campaigns_dir)
            print(f"review written: {path}")
        else:
            path = apply_review_doc(args.campaign, args.pack, args.stage, args.campaigns_dir)
            print(f"review applied: {path}")
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
