from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .validate_task_objects import (
        COLLECTION_TEMPLATES,
        FIXED_TITLE_HINTS,
        FLOWER_ACTION_TEMPLATES,
        GARBAGE_TEMPLATES,
        GENERATED_SEQUENCE_RULES,
        MYSTERY_TITLES,
        candidate_by_id,
        candidate_title_for_template,
        dialogue_pronouns,
        quest_prefix,
        selected_location_text,
        title_item_text,
    )
except ImportError:
    from validate_task_objects import (
        COLLECTION_TEMPLATES,
        FIXED_TITLE_HINTS,
        FLOWER_ACTION_TEMPLATES,
        GARBAGE_TEMPLATES,
        GENERATED_SEQUENCE_RULES,
        MYSTERY_TITLES,
        candidate_by_id,
        candidate_title_for_template,
        dialogue_pronouns,
        quest_prefix,
        selected_location_text,
        title_item_text,
    )


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTEXT_PACK_PATH = PROJECT_ROOT / "output" / "context_pack.json"
DEFAULT_CHOICES_PATH = PROJECT_ROOT / "output" / "task_choices.json"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "filled_tasks.json"
DEFAULT_BUILD_JSON_PATH = PROJECT_ROOT / "output" / "filled_tasks.build.json"
DEFAULT_TEMPLATES_PATH = PROJECT_ROOT / "data" / "task_templates.json"

SUPPORTED_TEMPLATE_IDS = {f"TT-{number:03d}" for number in range(1, 35)}
MYSTERY_TEMPLATE_IDS = set(MYSTERY_TITLES)
SILHOUETTE_TEMPLATE_IDS = {"TT-028", "TT-029", "TT-030", "TT-031", "TT-032"}
GENERATED_RESOURCE_TEMPLATE_IDS = set(GENERATED_SEQUENCE_RULES) - {"TT-003", "TT-004", "TT-005", "TT-006", "TT-007"}
CRAFT_ANCHOR_TEMPLATE_IDS = {"TT-002", "TT-033"}
GENERIC_REASON_MARKERS = (
    "подходит по контексту",
    "подходит по смыслу",
    "соответствует контексту",
    "соответствует теме",
    "логично подходит",
    "выбран по смыслу",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_template_catalog(path: Path) -> dict[str, dict[str, Any]]:
    data = read_json(path)
    return {template["id"]: template for template in data.get("templates", [])}


def task_object_defaults(template: dict[str, Any] | None) -> dict[str, Any]:
    defaults = (template or {}).get("task_object_defaults")
    return defaults if isinstance(defaults, dict) else {}


def int_choice_or_default(choice: dict[str, Any], defaults: dict[str, Any], field_name: str, fallback: int = 1) -> int:
    for source in (choice, defaults):
        value = source.get(field_name)
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        try:
            return int(text)
        except ValueError:
            continue
    return fallback


def task_amount(choice: dict[str, Any], defaults: dict[str, Any]) -> int:
    return int_choice_or_default(choice, defaults, "amount")


def task_price(choice: dict[str, Any], defaults: dict[str, Any]) -> int:
    return int_choice_or_default(choice, defaults, "price")


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def choice_key(classname_quests: Any, task_number: Any) -> tuple[str, int] | None:
    if not classname_quests or not isinstance(task_number, int):
        return None
    return str(classname_quests), task_number


def build_choice_index(choices: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for quest in as_list(choices.get("quests")):
        classname_quests = quest.get("classname_quests")
        for task in as_list(quest.get("tasks")):
            key = choice_key(classname_quests, task.get("task_number"))
            if key is not None:
                index[key] = task
    return index


def generated_sequence_offsets(context_pack: dict[str, Any]) -> dict[tuple[str, str], int]:
    result: dict[tuple[str, str], int] = {}
    offsets = context_pack.get("generated_sequence_offsets") or {}
    next_numbers = context_pack.get("next_generated_numbers") or {}
    for source, subtract in ((offsets, 0), (next_numbers, 1)):
        if not isinstance(source, dict):
            continue
        for prefix, kinds in source.items():
            if not isinstance(kinds, dict):
                continue
            for kind, value in kinds.items():
                try:
                    result[(str(prefix), str(kind))] = max(0, int(value) - subtract)
                except (TypeError, ValueError):
                    continue
    return result


class BuildState:
    def __init__(self, context_pack: dict[str, Any]) -> None:
        self.counters = generated_sequence_offsets(context_pack)

    def next_generated(self, prefix: str, kind: str) -> str:
        key = (prefix, kind)
        self.counters[key] = self.counters.get(key, 0) + 1
        return f"{prefix}_{kind}_{self.counters[key]}"


def context_location_titles(context_quest: dict[str, Any]) -> list[str]:
    titles: list[str] = []
    for task in as_list(context_quest.get("tasks")):
        for candidate in as_list(task.get("candidates")):
            for location in as_list(candidate.get("locations")):
                title = str(location.get("title") or "").strip()
                if title and title not in titles:
                    titles.append(title)
    return titles


def first_location_title(context_quest: dict[str, Any], choice: dict[str, Any] | None = None) -> str:
    choice = choice or {}
    location_title = str(choice.get("location_title") or "").strip()
    if location_title:
        return location_title
    location_titles = choice.get("location_titles")
    if isinstance(location_titles, list):
        for title in location_titles:
            value = str(title or "").strip()
            if value:
                return value
    titles = context_location_titles(context_quest)
    return titles[0] if titles else "Мир"


def location_text_from_choice_or_candidate(
    context_quest: dict[str, Any],
    choice: dict[str, Any],
    selected_candidate: dict[str, Any] | None,
) -> str:
    location_titles = choice.get("location_titles")
    if isinstance(location_titles, list):
        values = [str(title).strip() for title in location_titles if str(title or "").strip()]
        if values:
            return ", ".join(values)
    location_title = str(choice.get("location_title") or "").strip()
    if location_title:
        return location_title
    candidate_location = selected_location_text(selected_candidate)
    if candidate_location:
        return candidate_location
    return first_location_title(context_quest, choice)


def selected_candidate(context_task: dict[str, Any], choice: dict[str, Any], issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidate_id = choice.get("selected_candidate_id")
    if candidate_id:
        candidate = candidate_by_id(context_task, str(candidate_id))
        if candidate is None:
            issues.append(
                {
                    "level": "error",
                    "code": "selected_candidate_not_found",
                    "task_number": context_task.get("task_number"),
                    "task_template_id": context_task.get("task_template_id"),
                    "selected_candidate_id": candidate_id,
                }
            )
        return candidate

    candidates = as_list(context_task.get("candidates"))
    if len(candidates) == 1:
        return candidates[0]
    if candidates:
        issues.append(
            {
                "level": "error",
                "code": "selected_candidate_required",
                "task_number": context_task.get("task_number"),
                "task_template_id": context_task.get("task_template_id"),
                "message": "Choose selected_candidate_id from context_pack candidates.",
            }
        )
    return None


def selected_candidate_id(context_task: dict[str, Any], candidate: dict[str, Any] | None, choice: dict[str, Any]) -> str | None:
    if candidate is None:
        return None
    return str(choice.get("selected_candidate_id") or candidate.get("candidate_id") or "") or None


def clean_item_title(value: Any) -> str:
    text = str(value or "").strip()
    for prefix in ("Найди ", "Получи ", "Создай ", "Передай ", "Попроси у друзей ", "Подари другу ", "Убери мусор "):
        if text.startswith(prefix):
            return text[len(prefix) :].strip()
    return text


def item_title_for_choice(
    template_id: str,
    choice: dict[str, Any],
    selected: dict[str, Any] | None,
    fallback: str = "Предмет",
) -> str:
    for key in ("item_title", "resource_title", "hog_item_title", "craft_title", "title_item"):
        value = clean_item_title(choice.get(key))
        if value:
            return value
    candidate_title = candidate_title_for_template(template_id, selected)
    if candidate_title:
        return candidate_title
    return fallback


def hog_title(choice: dict[str, Any], item_title: str) -> str:
    title = str(choice.get("title") or "").strip()
    if title:
        return title
    return f"Найди {item_title}"


def riddle_text(choice: dict[str, Any], selected: dict[str, Any] | None, template_id: str, issues: list[dict[str, Any]]) -> str:
    for key in ("riddle", "hint", "mystery_hint"):
        value = str(choice.get(key) or "").strip()
        if value:
            return value
    answer = candidate_title_for_template(template_id, selected)
    issues.append(
        {
            "level": "error",
            "code": "riddle_required",
            "task_number": choice.get("task_number"),
            "task_template_id": template_id,
            "answer_title": answer,
            "message": "Mystery templates need a real riddle in choice.riddle. The code will not invent it.",
        }
    )
    return ""


def craft_item_title(context_quest: dict[str, Any], choices_by_task_number: dict[int, dict[str, Any]]) -> str:
    for context_task in as_list(context_quest.get("tasks")):
        template_id = str(context_task.get("task_template_id") or "")
        if template_id in CRAFT_ANCHOR_TEMPLATE_IDS:
            task_number = context_task.get("task_number")
            choice = choices_by_task_number.get(task_number, {}) if isinstance(task_number, int) else {}
            item = item_title_for_choice(template_id, choice, None, "")
            if item:
                return item
            task_object = choice.get("task_object") if isinstance(choice.get("task_object"), dict) else {}
            item = title_item_text(task_object.get("title"))
            if item:
                return item
    return ""


def is_generic_reason(reason: str) -> bool:
    normalized = reason.lower().replace("ё", "е").strip()
    if len(normalized) < 35:
        return True
    return any(marker in normalized for marker in GENERIC_REASON_MARKERS)


def choice_reason(
    quest: dict[str, Any],
    template_id: str,
    choice: dict[str, Any],
    selected: dict[str, Any] | None,
    task_object: dict[str, Any],
    craft_title: str,
) -> str:
    provided = str(choice.get("choice_reason") or "").strip()
    if provided and not is_generic_reason(provided):
        return provided

    item = title_item_text(task_object.get("title")) or item_title_for_choice(template_id, choice, selected, "предмет")
    quest_title = str(quest.get("title_quest") or "квеста").strip()

    if template_id == "TT-002":
        return f"Создаём {item}, потому что это главный предмет действия в квесте «{quest_title}»."
    if template_id == "TT-033":
        return f"Готовим и передаём {item}, потому что это главный предмет действия в квесте «{quest_title}»."
    if craft_title and template_id in GENERATED_RESOURCE_TEMPLATE_IDS:
        if template_id in {"TT-008", "TT-009"}:
            return f"В этом квесте создаём {craft_title}. Просим у друзей {item}, потому что это похоже на деталь или материал для {craft_title}."
        return f"В этом квесте создаём {craft_title}. {item} выглядит как часть, материал или украшение для {craft_title}, поэтому его логично получить перед крафтом."
    if template_id in {"TT-003", "TT-004", "TT-005", "TT-006", "TT-007"}:
        return f"Ищем {item}, потому что это конкретный предмет в сцене квеста «{quest_title}»."
    candidate_title = candidate_title_for_template(template_id, selected)
    if candidate_title:
        return f"{candidate_title} связан с темой квеста «{quest_title}», а выбранный источник доступен для этого типа задания."
    return f"Выбор поддерживает действие квеста «{quest_title}» и не меняет строгий шаблон задания."


def generated_resource_object(
    template_id: str,
    classname: str,
    item_title: str,
    choice: dict[str, Any],
    selected: dict[str, Any] | None,
    context_quest: dict[str, Any],
    defaults: dict[str, Any],
) -> dict[str, Any]:
    if template_id == "TT-008":
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Попроси у друзей {item_title}",
            "hint": "Попроси у друзей или купи.",
            "identifier": "",
        }
    if template_id == "TT-009":
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Попроси у друзей {item_title}",
            "hint": "Отправь личные просьбы друзьям или купи.",
            "identifier": "",
        }
    if template_id == "TT-010":
        collection_title = candidate_title_for_template("TT-011", selected)
        source_title = str((selected or {}).get("source_title") or "")
        location_text = location_text_from_choice_or_candidate(context_quest, choice, selected)
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Найди {item_title}",
            "hint": f"{item_title} можно получить за сбор коллекции {collection_title} при уборке мусора {source_title} в локации {location_text} дома и в гостях.",
            "identifier": "",
        }
    if template_id == "TT-012":
        action_text = str(choice.get("friend_action_text") or "за действие на площади у друга").strip()
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Получи {item_title}",
            "hint": f"{item_title} можно получить {action_text}",
            "identifier": "",
        }
    if template_id == "TT-013":
        location_text = location_text_from_choice_or_candidate(context_quest, choice, selected)
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Найди {item_title}",
            "hint": f"Убирай мусор в локации {location_text} дома, чтобы найти.",
            "identifier": "",
        }
    if template_id in {"TT-014", "TT-015"}:
        garbage_title = candidate_title_for_template(template_id, selected)
        mode_text = "в гостях" if template_id == "TT-014" else "дома"
        location_text = location_text_from_choice_or_candidate(context_quest, choice, selected)
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Найди {item_title}",
            "hint": f"Убирай мусор {garbage_title} {mode_text}, чтобы найти. Место поиска: {location_text}.",
            "identifier": "",
        }
    if template_id in {"TT-016", "TT-017"}:
        flower_title = candidate_title_for_template(template_id, selected)
        if template_id == "TT-016":
            hint = f"Собирай цветы {flower_title} в гостях, чтобы найти. Чтобы собрать растение, кликни на горшок с нужным растением в гостях у друга"
        else:
            hint = f"Собирай цветы {flower_title} дома, чтобы найти. Чтобы собрать растение, кликни на горшок с нужным растением."
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Получи {item_title}",
            "hint": hint,
            "identifier": "",
        }
    raise ValueError(f"Unsupported generated resource template: {template_id}")


def build_task_object(
    context_quest: dict[str, Any],
    context_task: dict[str, Any],
    choice: dict[str, Any],
    selected: dict[str, Any] | None,
    state: BuildState,
    issues: list[dict[str, Any]],
    template: dict[str, Any] | None = None,
) -> dict[str, Any]:
    template_id = str(context_task.get("task_template_id") or "")
    prefix = quest_prefix(context_quest.get("classname_quests"))
    item_title = item_title_for_choice(template_id, choice, selected)
    defaults = task_object_defaults(template)

    if template_id == "TT-001":
        person = str(choice.get("person") or context_quest.get("character") or "").strip()
        icon = str(choice.get("character_classname") or f"{prefix}_Character_{context_quest.get('quest_number') or 1}")
        object_pronoun, subject_pronoun = dialogue_pronouns(context_quest, person)
        location_title = first_location_title(context_quest, choice)
        return {
            "type": "action",
            "icon": icon,
            "action": f"{icon}_Dialog_{context_task.get('task_number') or 1}",
            "title": f"Поговори с {person}",
            "hint": f"Поговори с {person}. Для этого просто кликни на {object_pronoun}. {subject_pronoun} находится в {location_title}.",
            "go_to_location": [{"classname": icon}],
            "identifier": "",
        }

    if template_id == "TT-002":
        classname = state.next_generated(prefix, "R")
        return {
            "type": "get_and_decrease_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "title": f"Создай {item_title}",
            "go_to_location": [{"classname": f"{prefix}_Workbench_1"}],
            "hint": "Для создания используй Станок.",
            "identifier": "",
        }

    if template_id in {"TT-003", "TT-004"}:
        classname = state.next_generated(prefix, "HOG")
        title = hog_title(choice, item_title)
        location_text = "Мир" if template_id == "TT-003" else first_location_title(context_quest, choice)
        return {
            "type": "action",
            "action": "clean_debris",
            "param": classname,
            "search_action": f"search_{classname}",
            "after_buy_actions": [{"do": "remove_stuff", "classname": classname}],
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": title,
            "hint": f"{title}. Место поиска: {location_text}. Если найти все не удаётся, можно купить подсказку.",
            "identifier": "",
        }

    if template_id in {"TT-005", "TT-006", "TT-007"}:
        classname = state.next_generated(prefix, "HOG")
        title = hog_title(choice, item_title)
        if template_id == "TT-005":
            locations = location_text_from_choice_or_candidate(context_quest, choice, selected)
            hint = f"{title}. Они могут быть в {locations}."
        else:
            hint = str(choice.get("hint") or f"{title}.").strip()
            if hint and not hint.endswith("."):
                hint += "."
        return {
            "type": "action",
            "action": "clean_debris",
            "param": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": title,
            "hint": hint,
            "identifier": "",
        }

    if template_id in GENERATED_RESOURCE_TEMPLATE_IDS:
        kind, _field = GENERATED_SEQUENCE_RULES[template_id]
        classname = state.next_generated(prefix, kind)
        return generated_resource_object(template_id, classname, item_title, choice, selected, context_quest, defaults)

    if template_id == "TT-011":
        collection_title = candidate_title_for_template(template_id, selected)
        source_title = str((selected or {}).get("source_title") or "")
        location_text = location_text_from_choice_or_candidate(context_quest, choice, selected)
        classname = str((selected or {}).get("collection_classname") or "")
        return {
            "type": "get_asset",
            "classname": classname,
            "icon": classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Найди {collection_title}",
            "hint": f"{collection_title} - элемент коллекции, выпадает при уборке мусора {source_title} дома и в гостях. Место поиска: {location_text}.",
            "identifier": "",
        }

    if template_id in FLOWER_ACTION_TEMPLATES:
        flower_title = candidate_title_for_template(template_id, selected)
        flower_classname = str((selected or {}).get("flower_classname") or "")
        in_guest = template_id in {"TT-019", "TT-022", "TT-031"}
        if template_id in MYSTERY_TEMPLATE_IDS:
            task_object = {
                "type": "action",
                "action": "take_crop_in_guest" if in_guest else "take_crop",
                "param": flower_classname,
                "is_hide": 1,
                "amount": task_amount(choice, defaults),
                "price": task_price(choice, defaults),
                "title": MYSTERY_TITLES[template_id],
                "hint": riddle_text(choice, selected, template_id, issues),
                "identifier": "",
            }
        elif template_id in SILHOUETTE_TEMPLATE_IDS:
            task_object = {
                "type": "action",
                "action": "take_crop_in_guest" if in_guest else "take_crop",
                "param": flower_classname,
                "is_silhouette": 1,
                "amount": task_amount(choice, defaults),
                "price": task_price(choice, defaults),
                "title": FIXED_TITLE_HINTS[template_id][0],
                "hint": FIXED_TITLE_HINTS[template_id][1],
                "identifier": "",
            }
        else:
            place = "в гостях" if in_guest else "дома"
            hint = f"Собирай {flower_title} {place}. Чтобы собрать растение, кликни на горшок с нужным растением"
            if in_guest:
                hint += " в гостях у друга"
            task_object = {
                "type": "action",
                "action": "take_crop_in_guest" if in_guest else "take_crop",
                "param": flower_classname,
                "amount": task_amount(choice, defaults),
                "price": task_price(choice, defaults),
                "title": f"Собери {flower_title} {place}",
                "hint": hint,
                "identifier": "",
            }
        return task_object

    if template_id in GARBAGE_TEMPLATES:
        garbage_title = candidate_title_for_template(template_id, selected)
        garbage_classname = str((selected or {}).get("garbage_classname") or "")
        location_text = location_text_from_choice_or_candidate(context_quest, choice, selected)
        in_guest = template_id in {"TT-020", "TT-024", "TT-029"}
        if template_id in MYSTERY_TEMPLATE_IDS:
            task_object = {
                "type": "garbage",
                "classname": garbage_classname,
                "is_hide": 1,
                "amount": task_amount(choice, defaults),
                "price": task_price(choice, defaults),
                "title": MYSTERY_TITLES[template_id],
                "hint": riddle_text(choice, selected, template_id, issues),
                "identifier": "",
            }
            if in_guest:
                task_object["in_guest"] = 1
            return task_object
        if template_id in SILHOUETTE_TEMPLATE_IDS:
            task_object = {
                "type": "garbage",
                "classname": garbage_classname,
                "is_silhouette": 1,
                "amount": task_amount(choice, defaults),
                "price": task_price(choice, defaults),
                "title": FIXED_TITLE_HINTS[template_id][0],
                "hint": FIXED_TITLE_HINTS[template_id][1],
                "identifier": "",
            }
            if in_guest:
                task_object["in_guest"] = 1
            return task_object
        if in_guest:
            return {
                "type": "garbage",
                "classname": garbage_classname,
                "in_guest": 1,
                "amount": task_amount(choice, defaults),
                "price": task_price(choice, defaults),
                "title": f"Убери мусор {garbage_title} в гостях",
                "hint": f"Убери мусор {garbage_title} в гостях. Для этого просто кликни на нужный мусор в гостях у друга. Место поиска: {location_text}.",
                "identifier": "",
            }
        return {
            "type": "garbage",
            "classname": garbage_classname,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": f"Убери мусор {garbage_title} дома",
            "hint": f"Убери мусор {garbage_title} дома. Для этого просто кликни на нужный мусор дома. Место поиска: {location_text}.",
            "identifier": "",
        }

    if template_id == "TT-027":
        collection_classname = str((selected or {}).get("collection_classname") or "")
        return {
            "type": "get_asset",
            "classname": collection_classname,
            "icon": collection_classname,
            "is_silhouette": 1,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": str(choice.get("reverse_clue_title") or choice.get("title") or "Йиден ан йандерпамон"),
            "hint": "Прочитай фразу задания задом наперед.",
            "identifier": "",
        }

    if template_id == "TT-026":
        collection_classname = str((selected or {}).get("collection_classname") or "")
        return {
            "type": "get_asset",
            "classname": collection_classname,
            "icon": collection_classname,
            "is_hide": 1,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": MYSTERY_TITLES[template_id],
            "hint": riddle_text(choice, selected, template_id, issues),
            "identifier": "",
        }

    if template_id == "TT-028":
        collection_classname = str((selected or {}).get("collection_classname") or "")
        return {
            "type": "get_asset",
            "classname": collection_classname,
            "icon": collection_classname,
            "is_silhouette": 1,
            "amount": task_amount(choice, defaults),
            "price": task_price(choice, defaults),
            "title": FIXED_TITLE_HINTS[template_id][0],
            "hint": FIXED_TITLE_HINTS[template_id][1],
            "identifier": "",
        }

    if template_id == "TT-033":
        item_classname = str(choice.get("item_classname") or f"{prefix}_Give_{context_task.get('task_number') or 1}")
        person = str(choice.get("person") or context_quest.get("character") or "персонажу").strip()
        location_title = first_location_title(context_quest, choice)
        title = str(choice.get("title") or f"Передай {item_title}").strip()
        return {
            "type": "action",
            "action": str(choice.get("action") or f"{item_classname}_Give"),
            "icon": item_classname,
            "go_to_location": [{"classname": item_classname}],
            "amount": task_amount(choice, defaults),
            "title": title,
            "hint": f"Передай {item_title} персонажу {person}. Он находится на {location_title}.",
            "identifier": "",
        }

    if template_id == "TT-034":
        person = str(choice.get("person") or context_quest.get("character") or "").strip()
        icon = str(choice.get("character_classname") or f"{prefix}_Character_{context_quest.get('quest_number') or 1}")
        location_title = first_location_title(context_quest, choice)
        return {
            "type": "action",
            "action": "post_photo",
            "icon": icon,
            "param": icon,
            "go_to_location": [{"classname": icon}],
            "amount": task_amount(choice, defaults),
            "title": f"Сфотографируйся с {person}",
            "hint": f"{person} - персонаж, с которым нужно сфотографироваться. Найди его у себя на {location_title} и нажми на иконку \"Сделать фотографию\" в правом верхнем углу. Наведи фокус на {person}, сфотографируйся с ним и нажми \"Славненько\".",
            "identifier": "",
        }

    raise ValueError(f"Unsupported template: {template_id}")


def build_filled_tasks(
    context_pack: dict[str, Any],
    choices: dict[str, Any],
    templates: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    if templates is None and DEFAULT_TEMPLATES_PATH.exists():
        templates = build_template_catalog(DEFAULT_TEMPLATES_PATH)

    choice_index = build_choice_index(choices)
    state = BuildState(context_pack)
    issues: list[dict[str, Any]] = []
    filled_quests: list[dict[str, Any]] = []
    supported_template_ids = set(SUPPORTED_TEMPLATE_IDS)
    if templates is not None:
        supported_template_ids = {
            template_id
            for template_id, template in templates.items()
            if template.get("status") != "not_ready"
            and (
                not template.get("stage4_contract")
                or template.get("stage4_contract", {}).get("ai_writes_task_object") is False
            )
        }

    for context_quest in as_list(context_pack.get("quests")):
        classname_quests = context_quest.get("classname_quests")
        choices_by_task_number = {
            task_number: task
            for (quest_classname, task_number), task in choice_index.items()
            if quest_classname == classname_quests
        }
        craft_title = craft_item_title(context_quest, choices_by_task_number)
        filled_quest = {
            key: context_quest.get(key)
            for key in ("classname_quests", "title_quest", "quest_number", "description", "congratulation", "character")
            if key in context_quest
        }
        filled_quest["tasks"] = []

        for context_task in as_list(context_quest.get("tasks")):
            template_id = str(context_task.get("task_template_id") or "")
            task_number = context_task.get("task_number")
            key = choice_key(classname_quests, task_number)
            choice = choice_index.get(key or ("", -1), {})
            if not choice:
                issues.append(
                    {
                        "level": "error",
                        "code": "task_choice_missing",
                        "quest": classname_quests,
                        "task_number": task_number,
                        "task_template_id": template_id,
                    }
                )
            if template_id not in supported_template_ids:
                issues.append(
                    {
                        "level": "error",
                        "code": "unsupported_template",
                        "quest": classname_quests,
                        "task_number": task_number,
                        "task_template_id": template_id,
                    }
                )
                continue

            selected = selected_candidate(context_task, choice, issues)
            template = templates.get(template_id) if templates else None
            try:
                task_object = build_task_object(context_quest, context_task, choice, selected, state, issues, template)
            except (TypeError, ValueError) as exc:
                issues.append(
                    {
                        "level": "error",
                        "code": "task_object_build_failed",
                        "quest": classname_quests,
                        "task_number": task_number,
                        "task_template_id": template_id,
                        "message": str(exc),
                    }
                )
                continue

            filled_task = {
                "task_number": task_number,
                "task_template_id": template_id,
                "task_template_name": context_task.get("task_template_name"),
                "task_type": context_task.get("task_type"),
                "selected_candidate_id": selected_candidate_id(context_task, selected, choice),
                "choice_reason": choice_reason(context_quest, template_id, choice, selected, task_object, craft_title),
                "task_object": task_object,
            }
            dialogue = str(choice.get("dialogue_replica") or choice.get("dialogue") or choice.get("replica") or "").strip()
            if not dialogue and template_id == "TT-001":
                dialogue = str(context_quest.get("description") or "").strip()[:360]
            if dialogue:
                filled_task["dialogue_replica"] = dialogue
            filled_quest["tasks"].append(filled_task)

        filled_quests.append(filled_quest)

    return {
        "quests": filled_quests,
        "summary": {
            "quests_found": len(filled_quests),
            "tasks_found": sum(len(quest.get("tasks", [])) for quest in filled_quests),
            "issues": len([issue for issue in issues if issue.get("level") == "error"]),
            "warnings": len([issue for issue in issues if issue.get("level") == "warning"]),
        },
        "issues": issues,
    }


def build_filled_tasks_file(
    context_pack_path: Path,
    choices_path: Path,
    output_json_path: Path,
    build_json_path: Path,
    templates_path: Path = DEFAULT_TEMPLATES_PATH,
) -> dict[str, Any]:
    context_pack = read_json(context_pack_path)
    choices = read_json(choices_path)
    templates = build_template_catalog(templates_path)
    result = build_filled_tasks(context_pack, choices, templates)
    filled_tasks = {"quests": result["quests"]}
    write_json(output_json_path, filled_tasks)
    write_json(build_json_path, {"summary": result["summary"], "issues": result["issues"]})
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build strict stage 4 filled_tasks.json from semantic task_choices.json.")
    parser.add_argument("--context-pack", type=Path, default=DEFAULT_CONTEXT_PACK_PATH)
    parser.add_argument("--choices", type=Path, default=DEFAULT_CHOICES_PATH)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON_PATH)
    parser.add_argument("--build-json", type=Path, default=DEFAULT_BUILD_JSON_PATH)
    parser.add_argument("--templates", type=Path, default=DEFAULT_TEMPLATES_PATH)
    args = parser.parse_args(argv)

    if not args.context_pack.exists():
        print(f"context pack not found: {args.context_pack}")
        return 1
    if not args.choices.exists():
        print(f"task choices not found: {args.choices}")
        return 1

    result = build_filled_tasks_file(args.context_pack, args.choices, args.output_json, args.build_json, args.templates)
    summary = result["summary"]
    print(f"quests found: {summary['quests_found']}")
    print(f"tasks found: {summary['tasks_found']}")
    print(f"errors: {summary['issues']}")
    print(f"warnings: {summary['warnings']}")
    print(f"json written: {args.output_json}")
    print(f"build summary written: {args.build_json}")
    return 0 if summary["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
