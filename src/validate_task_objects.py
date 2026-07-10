from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from .campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_path as campaign_memory_path_for,
        generated_sequence_offsets,
    )
except ImportError:
    from campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_path as campaign_memory_path_for,
        generated_sequence_offsets,
    )


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "filled_tasks.json"
DEFAULT_CONTEXT_PACK_PATH = PROJECT_ROOT / "output" / "context_pack.json"
DEFAULT_TEMPLATES_PATH = PROJECT_ROOT / "data" / "task_templates.json"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "filled_tasks.validation.json"
DEFAULT_PREVIEW_PATH = PROJECT_ROOT / "output" / "filled_tasks.preview.md"
DIALOGUE_TEMPLATE_IDS = {"TT-001"}
DIALOGUE_REPLICA_KEYS = ("dialogue_replica", "dialogue", "replica", "dialogue_text")
DIALOGUE_REPLICA_MAX_CHARS = 360


REQUIRED_FIELDS_BY_TEMPLATE = {
    "TT-001": ["type", "icon", "action", "title", "hint", "go_to_location"],
    "TT-002": ["type", "classname", "icon", "amount", "title", "go_to_location", "hint"],
    "TT-003": ["type", "action", "param", "search_action", "after_buy_actions", "amount", "price", "title", "hint"],
    "TT-004": ["type", "action", "param", "search_action", "after_buy_actions", "amount", "price", "title", "hint"],
    "TT-005": ["type", "action", "param", "amount", "price", "title", "hint"],
    "TT-006": ["type", "action", "param", "amount", "price", "title", "hint"],
    "TT-007": ["type", "action", "param", "amount", "price", "title", "hint"],
    "TT-008": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-009": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-010": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-011": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-012": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-013": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-014": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-015": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-016": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-017": ["type", "classname", "icon", "amount", "price", "title", "hint"],
    "TT-018": ["type", "action", "param", "amount", "price", "title", "hint"],
    "TT-019": ["type", "action", "param", "amount", "price", "title", "hint"],
    "TT-020": ["type", "classname", "in_guest", "amount", "price", "title", "hint"],
    "TT-021": ["type", "classname", "amount", "price", "title", "hint"],
    "TT-022": ["type", "action", "param", "is_hide", "amount", "price", "title", "hint"],
    "TT-023": ["type", "action", "param", "is_hide", "amount", "price", "title", "hint"],
    "TT-024": ["type", "classname", "in_guest", "is_hide", "amount", "price", "title", "hint"],
    "TT-025": ["type", "classname", "is_hide", "amount", "price", "title", "hint"],
    "TT-026": ["type", "classname", "is_hide", "amount", "price", "title", "hint"],
    "TT-027": ["type", "classname", "is_silhouette", "amount", "price", "title", "hint"],
    "TT-028": ["type", "classname", "is_silhouette", "amount", "price", "title", "hint"],
    "TT-029": ["type", "classname", "is_silhouette", "in_guest", "amount", "price", "title", "hint"],
    "TT-030": ["type", "classname", "is_silhouette", "amount", "price", "title", "hint"],
    "TT-031": ["type", "action", "param", "is_silhouette", "amount", "price", "title", "hint"],
    "TT-032": ["type", "action", "param", "is_silhouette", "amount", "price", "title", "hint"],
    "TT-033": ["type", "action", "icon", "go_to_location", "amount", "title", "hint"],
    "TT-034": ["type", "action", "icon", "param", "amount", "title", "hint"],
}


EXPECTED_VALUES_BY_TEMPLATE = {
    "TT-001": {"type": "action"},
    "TT-002": {"type": "get_and_decrease_asset"},
    "TT-003": {"type": "action", "action": "clean_debris"},
    "TT-004": {"type": "action", "action": "clean_debris"},
    "TT-005": {"type": "action", "action": "clean_debris"},
    "TT-006": {"type": "action", "action": "clean_debris"},
    "TT-007": {"type": "action", "action": "clean_debris"},
    "TT-008": {"type": "get_asset"},
    "TT-009": {"type": "get_asset"},
    "TT-010": {"type": "get_asset"},
    "TT-011": {"type": "get_asset"},
    "TT-012": {"type": "get_asset"},
    "TT-013": {"type": "get_asset"},
    "TT-014": {"type": "get_asset"},
    "TT-015": {"type": "get_asset"},
    "TT-016": {"type": "get_asset"},
    "TT-017": {"type": "get_asset"},
    "TT-018": {"type": "action", "action": "take_crop"},
    "TT-019": {"type": "action", "action": "take_crop_in_guest"},
    "TT-020": {"type": "garbage", "in_guest": 1},
    "TT-021": {"type": "garbage"},
    "TT-022": {"type": "action", "action": "take_crop_in_guest", "is_hide": 1},
    "TT-023": {"type": "action", "action": "take_crop", "is_hide": 1},
    "TT-024": {"type": "garbage", "in_guest": 1, "is_hide": 1},
    "TT-025": {"type": "garbage", "is_hide": 1},
    "TT-026": {"type": "get_asset", "is_hide": 1},
    "TT-027": {"type": "get_asset", "is_silhouette": 1},
    "TT-028": {"type": "get_asset", "is_silhouette": 1},
    "TT-029": {"type": "garbage", "in_guest": 1, "is_silhouette": 1},
    "TT-030": {"type": "garbage", "is_silhouette": 1},
    "TT-031": {"type": "action", "action": "take_crop_in_guest", "is_silhouette": 1},
    "TT-032": {"type": "action", "action": "take_crop", "is_silhouette": 1},
    "TT-033": {"type": "action"},
    "TT-034": {"type": "action", "action": "post_photo"},
}


GARBAGE_TEMPLATES = {"TT-020", "TT-021", "TT-024", "TT-025", "TT-029", "TT-030"}
FLOWER_ACTION_TEMPLATES = {"TT-018", "TT-019", "TT-022", "TT-023", "TT-031", "TT-032"}
COLLECTION_TEMPLATES = {"TT-011", "TT-026", "TT-027", "TT-028"}
GENERATED_ASSET_TEMPLATES = {
    "TT-008",
    "TT-009",
    "TT-010",
    "TT-012",
    "TT-013",
    "TT-014",
    "TT-015",
    "TT-016",
    "TT-017",
}
HOG_TEMPLATES = {"TT-003", "TT-004", "TT-005", "TT-006", "TT-007"}
CRAFT_TEMPLATES = {"TT-002", "TT-033"}

GENERATED_SEQUENCE_RULES = {
    "TT-002": ("R", "classname"),
    "TT-003": ("HOG", "param"),
    "TT-004": ("HOG", "param"),
    "TT-005": ("HOG", "param"),
    "TT-006": ("HOG", "param"),
    "TT-007": ("HOG", "param"),
    "TT-008": ("ASK", "classname"),
    "TT-009": ("PER", "classname"),
    "TT-010": ("CL", "classname"),
    "TT-012": ("FA", "classname"),
    "TT-013": ("GR", "classname"),
    "TT-014": ("GR", "classname"),
    "TT-015": ("GR", "classname"),
    "TT-016": ("GR", "classname"),
    "TT-017": ("GR", "classname"),
}

ABSTRACT_ITEM_WORDS = {
    "давление",
    "энергия",
    "сила",
    "магия",
    "настроение",
    "удача",
    "сытость",
    "тепло",
    "холод",
    "фронт",
    "поток",
    "заряд",
    "импульс",
    "парад",
    "парадный",
    "парадная",
    "хруст",
    "ритм",
    "звучание",
    "печаль",
    "грусть",
    "улыбка",
}

CONCRETE_ITEM_ANCHORS = {
    "банка",
    "баночка",
    "бутылка",
    "крышка",
    "ключ",
    "камень",
    "осколок",
    "стрелка",
    "пружина",
    "шестеренка",
    "шестерёнка",
    "колесико",
    "колёсико",
    "лепесток",
    "лист",
    "цветок",
    "порошок",
    "мешочек",
    "катушка",
    "лента",
    "провод",
    "лампа",
    "фонарь",
    "флакон",
    "кристалл",
    "табличка",
    "ложка",
    "чашка",
    "котелок",
    "котёлок",
    "усмиритель",
    "барометр",
    "барабан",
    "палочка",
    "палочки",
    "колокольчик",
    "значок",
    "флажок",
    "шнур",
    "ткань",
    "ручка",
    "обод",
}

STRICT_IDENTIFIER_TEMPLATES = {f"TT-{number:03d}" for number in range(1, 35)}
HOG_TITLE_PREFIXES = ("Найди ", "Отыщи ", "Собери ", "Поймай ", "Верни ", "Забери ")
MYSTERY_TITLES = {
    "TT-022": "Загадка, цветы в гостях у друга",
    "TT-023": "Загадка, цветы дома",
    "TT-024": "Загадка, мусор в гостях",
    "TT-025": "Загадка, мусор дома",
    "TT-026": "Загадка, предмет из коллекции",
}
FIXED_TITLE_HINTS = {
    "TT-028": (
        "Угадай элемент коллекции",
        "Угадай элемент коллекции и найди его дома или в гостях у друзей",
    ),
    "TT-029": (
        "Угадай загаданный мусор",
        "Угадай загаданный мусор и убери его в гостях у друзей",
    ),
    "TT-030": (
        "Угадай загаданный мусор и убери его дома",
        "Угадай загаданный мусор и убери его дома",
    ),
    "TT-031": (
        "Угадай загаданный цветок",
        "Угадай загаданный цветок и собери его в гостях у друга",
    ),
    "TT-032": (
        "Угадай загаданный цветок и собери его дома",
        "Угадай загаданный цветок и собери его дома",
    ),
}
FEMALE_CHARACTER_MARKERS = {
    "баба",
    "бабушка",
    "ведьма",
    "госпожа",
    "девочка",
    "королева",
    "леди",
    "мама",
    "мать",
    "несмияна",
    "принцесса",
    "русалка",
    "сестра",
    "снегурочка",
    "тетя",
    "тётя",
    "фея",
    "царевна",
}
MALE_CHARACTER_MARKERS = {
    "брат",
    "дед",
    "дедушка",
    "детектив",
    "домоведом",
    "домовенком",
    "домовёнком",
    "домовенок",
    "домовёнок",
    "кот",
    "кролик",
    "король",
    "принц",
}
TITLE_WORD_STOPWORDS = {
    "весь",
    "все",
    "всё",
    "для",
    "друг",
    "друга",
    "друзей",
    "загадка",
    "коллекции",
    "мусор",
    "найди",
    "парадная",
    "парадную",
    "парадный",
    "предмет",
    "получи",
    "попроси",
    "создай",
    "цветы",
}
CRAFT_LINK_REASON_MARKERS = (
    "крафт",
    "созда",
    "собира",
    "част",
    "детал",
    "ингреди",
    "рецепт",
    "итог",
    "состав",
    "основ",
)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def issue(
    severity: str,
    code: str,
    message: str,
    quest: dict[str, Any] | None = None,
    task: dict[str, Any] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    item = {
        "severity": severity,
        "code": code,
        "message": message,
    }
    if quest is not None:
        item["classname_quests"] = quest.get("classname_quests")
        item["quest_number"] = quest.get("quest_number")
    if task is not None:
        item["task_number"] = task.get("task_number")
        item["task_template_id"] = task.get("task_template_id")
    item.update(extra)
    return item


def build_template_catalog(path: Path) -> dict[str, dict[str, Any]]:
    data = read_json(path)
    return {template["id"]: template for template in data.get("templates", [])}


def build_context_task_index(context_pack: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    index: dict[tuple[str, int], dict[str, Any]] = {}
    for quest in context_pack.get("quests", []):
        classname = quest.get("classname_quests")
        for task in quest.get("tasks", []):
            task_number = task.get("task_number")
            if classname and isinstance(task_number, int):
                index[(classname, task_number)] = task
    return index


def build_context_quest_index(context_pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        quest.get("classname_quests"): quest
        for quest in context_pack.get("quests", [])
        if quest.get("classname_quests")
    }


def context_quest_location_titles(context_quest: dict[str, Any] | None) -> set[str]:
    titles: set[str] = set()
    if context_quest is None:
        return titles
    for task in context_quest.get("tasks", []):
        for candidate in task.get("candidates", []):
            for location in candidate.get("locations", []) or []:
                title = location.get("title")
                if title:
                    titles.add(str(title))
    return titles


def build_filled_task_rows(filled_tasks: dict[str, Any]) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    rows: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for quest in filled_tasks.get("quests", []):
        for task in quest.get("tasks", []):
            rows.append((quest, task))
    return rows


def is_missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def is_dialogue_task(task: dict[str, Any], task_object: dict[str, Any]) -> bool:
    template_id = str(task.get("task_template_id") or "")
    template_name = str(task.get("task_template_name") or "").lower()
    task_type = str(task.get("task_type") or "").lower()
    action = str(task_object.get("action") or "").lower()
    return (
        template_id in DIALOGUE_TEMPLATE_IDS
        or template_name == "диалог"
        or "dialog" in task_type
        or "_dialog_" in action
    )


def dialogue_replica(task: dict[str, Any], task_object: dict[str, Any]) -> str | None:
    for source in (task, task_object):
        for key in DIALOGUE_REPLICA_KEYS:
            value = source.get(key)
            if value not in (None, ""):
                return str(value).strip()
    return None


def validate_dialogue_replica(
    task_object: dict[str, Any],
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    if not is_dialogue_task(task, task_object):
        return []

    replica = dialogue_replica(task, task_object)
    if not replica:
        return [
            issue(
                "error",
                "missing_dialogue_replica",
                "Dialogue task must include dialogue_replica for the CSV task header row.",
                quest,
                task,
            )
        ]

    if len(replica) > DIALOGUE_REPLICA_MAX_CHARS:
        return [
            issue(
                "error",
                "dialogue_replica_too_long",
                "Dialogue replica must be no longer than 360 characters including spaces.",
                quest,
                task,
                limit=DIALOGUE_REPLICA_MAX_CHARS,
                actual=len(replica),
            )
        ]
    return []


def candidate_by_id(context_task: dict[str, Any], candidate_id: str | None) -> dict[str, Any] | None:
    if not candidate_id:
        return None
    for candidate in context_task.get("candidates", []):
        if candidate.get("candidate_id") == candidate_id:
            return candidate
    return None


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
    return " ".join(converted)


def upper_first(value: str) -> str:
    text = value.strip()
    return text[:1].upper() + text[1:] if text else text


def validate_required_fields(
    task_object: dict[str, Any],
    template_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    required_fields = REQUIRED_FIELDS_BY_TEMPLATE.get(template_id)
    if required_fields is None:
        issues.append(issue("error", "unknown_required_fields", "No required-field rule for template.", quest, task))
        return issues

    for field_name in required_fields:
        if is_missing(task_object.get(field_name)):
            issues.append(
                issue(
                    "error",
                    "missing_task_object_field",
                    f"task_object is missing required field: {field_name}",
                    quest,
                    task,
                    field=field_name,
                )
            )
    return issues


def validate_expected_values(
    task_object: dict[str, Any],
    template_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for field_name, expected in EXPECTED_VALUES_BY_TEMPLATE.get(template_id, {}).items():
        actual = task_object.get(field_name)
        if actual != expected:
            issues.append(
                issue(
                    "error",
                    "task_object_value_mismatch",
                    f"task_object.{field_name} must match template.",
                    quest,
                    task,
                    field=field_name,
                    expected=expected,
                    actual=actual,
                )
            )
    return issues


def validate_candidate_match(
    task_object: dict[str, Any],
    template_id: str,
    selected_candidate: dict[str, Any] | None,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    if template_id in GARBAGE_TEMPLATES:
        expected = selected_candidate.get("garbage_classname") if selected_candidate else None
        actual = task_object.get("classname")
        if expected and not is_missing(actual) and actual != expected:
            issues.append(
                issue(
                    "error",
                    "garbage_classname_mismatch",
                    "garbage task_object.classname must match selected candidate.",
                    quest,
                    task,
                    expected=expected,
                    actual=actual,
                )
            )

    if template_id in FLOWER_ACTION_TEMPLATES:
        expected = selected_candidate.get("flower_classname") if selected_candidate else None
        actual = task_object.get("param")
        if expected and not is_missing(actual) and actual != expected:
            issues.append(
                issue(
                    "error",
                    "flower_param_mismatch",
                    "flower task_object.param must match selected candidate.",
                    quest,
                    task,
                    expected=expected,
                    actual=actual,
                )
            )

    if template_id in COLLECTION_TEMPLATES:
        expected = selected_candidate.get("collection_classname") if selected_candidate else None
        classname = task_object.get("classname")
        icon = task_object.get("icon")
        if expected and not is_missing(classname) and classname != expected:
            issues.append(
                issue(
                    "error",
                    "collection_classname_mismatch",
                    "collection task_object.classname must match selected candidate.",
                    quest,
                    task,
                    expected=expected,
                    actual=classname,
                )
            )
        if expected and not is_missing(icon) and icon != expected:
            issues.append(
                issue(
                    "error",
                    "collection_icon_mismatch",
                    "collection task_object.icon must match selected candidate when icon is present.",
                    quest,
                    task,
                    expected=expected,
                    actual=icon,
                )
            )

    return issues


def validate_generated_naming(
    task_object: dict[str, Any],
    template_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    classname = task_object.get("classname")
    icon = task_object.get("icon")

    if template_id in GENERATED_ASSET_TEMPLATES:
        if not classname or not re.search(r"_(GR|ASK|PER|CL|FA)_", str(classname)):
            issues.append(
                issue(
                    "warning",
                    "generated_classname_pattern_unknown",
                    "Generated get_asset classname does not look like GR/ASK/PER/CL/FA resource.",
                    quest,
                    task,
                    classname=classname,
                )
            )
        if icon is not None and classname is not None and icon != classname:
            issues.append(
                issue(
                    "warning",
                    "generated_icon_differs_from_classname",
                    "Generated get_asset icon usually matches classname.",
                    quest,
                    task,
                    classname=classname,
                    icon=icon,
                )
            )

    return issues


def title_item_text(title: Any) -> str:
    value = str(title or "").strip()
    for prefix in ("Найди ", "Получи ", "Создай ", "Передай ", "Подари другу "):
        if value.startswith(prefix):
            value = value[len(prefix) :]
    value = value.replace("Попроси у друзей", "").strip()
    return value.strip(' "«»')


def validate_generated_item_concreteness(
    task_object: dict[str, Any],
    template_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    if template_id not in GENERATED_ASSET_TEMPLATES and template_id not in CRAFT_TEMPLATES:
        return []

    item = title_item_text(task_object.get("title"))
    normalized = item.lower().replace("ё", "е")
    words = set(re.findall(r"[а-яa-z0-9_]{3,}", normalized, flags=re.IGNORECASE))
    has_abstract = bool(words & ABSTRACT_ITEM_WORDS)
    has_concrete_anchor = bool(words & {word.replace("ё", "е") for word in CONCRETE_ITEM_ANCHORS})
    if has_abstract and not has_concrete_anchor:
        return [
            issue(
                "error",
                "generated_item_not_visualizable",
                "Generated GR/ASK/PER/R item looks abstract; use a concrete drawable object.",
                quest,
                task,
                title=task_object.get("title"),
                item=item,
            )
        ]
    return []


def validate_location_references(
    task_object: dict[str, Any],
    template_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
    allowed_location_titles: set[str],
) -> list[dict[str, Any]]:
    hint = str(task_object.get("hint") or "")
    if not hint:
        return []

    requires_location = "Место поиска:" in hint or "Он находится" in hint or "она находится" in hint.lower()
    if not requires_location:
        return []

    if "Мир" in hint:
        return []

    if any(title and title in hint for title in allowed_location_titles):
        return []

    return [
        issue(
            "error",
            "unknown_location_in_hint",
            "Location reference in hint must use an exact real location title from context_pack candidates.",
            quest,
            task,
            hint=hint,
            allowed_location_titles=sorted(allowed_location_titles),
        )
    ]


def normalized_words(value: Any) -> set[str]:
    normalized = str(value or "").lower().replace("ё", "е")
    return set(re.findall(r"[а-яa-z0-9_]{3,}", normalized, flags=re.IGNORECASE))


def significant_title_words(value: Any) -> set[str]:
    return {
        word
        for word in normalized_words(value)
        if len(word) >= 4 and word not in TITLE_WORD_STOPWORDS
    }


def dialogue_pronouns(quest: dict[str, Any], person: str) -> tuple[str, str]:
    source = f"{quest.get('character') or ''} {person}".lower().replace("ё", "е")
    words = set(re.findall(r"[а-яa-z]+", source, flags=re.IGNORECASE))
    if words & FEMALE_CHARACTER_MARKERS:
        return "неё", "Она"
    if words & MALE_CHARACTER_MARKERS:
        return "него", "Он"
    character = str(quest.get("character") or "").strip().lower().replace("ё", "е")
    if character.endswith(("а", "я")) and not character.endswith(("илья", "никита")):
        return "неё", "Она"
    return "него", "Он"


def candidate_title_for_template(template_id: str, selected_candidate: dict[str, Any] | None) -> str:
    if not selected_candidate:
        return ""
    if template_id in GARBAGE_TEMPLATES or template_id in {"TT-013", "TT-014", "TT-015"}:
        return str(selected_candidate.get("garbage_title") or "")
    if template_id in FLOWER_ACTION_TEMPLATES or template_id in {"TT-016", "TT-017"}:
        return str(selected_candidate.get("flower_title") or "")
    if template_id in COLLECTION_TEMPLATES:
        return str(selected_candidate.get("collection_title") or "")
    return ""


def selected_location_text(selected_candidate: dict[str, Any] | None) -> str:
    if not selected_candidate:
        return ""
    titles = [
        str(location.get("title"))
        for location in selected_candidate.get("locations", []) or []
        if location.get("title")
    ]
    return ", ".join(titles)


def split_location_text(location_text: str) -> list[str]:
    return [part.strip() for part in location_text.split(",") if part.strip()]


def validate_location_text(
    location_text: str,
    allowed_location_titles: set[str],
    quest: dict[str, Any],
    task: dict[str, Any],
    code: str,
) -> list[dict[str, Any]]:
    locations = split_location_text(location_text)
    unknown_locations = [location for location in locations if location not in allowed_location_titles and location != "Мир"]
    if not unknown_locations:
        return []
    return [
        issue(
            "error",
            code,
            "Template location text must use exact real location titles from the context pack.",
            quest,
            task,
            unknown_locations=unknown_locations,
            allowed_location_titles=sorted(allowed_location_titles),
        )
    ]


def strict_text_issue(
    message: str,
    quest: dict[str, Any],
    task: dict[str, Any],
    field: str,
    expected: Any,
    actual: Any,
) -> dict[str, Any]:
    return issue(
        "error",
        "strict_template_text_mismatch",
        message,
        quest,
        task,
        field=field,
        expected=expected,
        actual=actual,
    )


def validate_exact_text(
    task_object: dict[str, Any],
    quest: dict[str, Any],
    task: dict[str, Any],
    field: str,
    expected: str,
    message: str,
) -> list[dict[str, Any]]:
    actual = str(task_object.get(field) or "")
    if actual == expected:
        return []
    return [strict_text_issue(message, quest, task, field, expected, actual)]


def validate_identifier_blank(
    task_object: dict[str, Any],
    template_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    if template_id not in STRICT_IDENTIFIER_TEMPLATES:
        return []
    if task_object.get("identifier") == "":
        return []
    return [
        issue(
            "error",
            "strict_identifier_mismatch",
            "Strict stage 4 templates must keep identifier as an empty string.",
            quest,
            task,
            expected="",
            actual=task_object.get("identifier"),
        )
    ]


def validate_mystery_riddle_text(
    task_object: dict[str, Any],
    template_id: str,
    answer_title: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    expected_title = MYSTERY_TITLES.get(template_id)
    title = str(task_object.get("title") or "")
    hint = str(task_object.get("hint") or "")

    if expected_title and title != expected_title:
        issues.append(
            issue(
                "error",
                "strict_template_text_mismatch",
                "Mystery title must keep the exact fixed template text.",
                quest,
                task,
                field="title",
                expected=expected_title,
                actual=title,
            )
        )

    if len(hint.strip()) < 40:
        issues.append(
            issue(
                "error",
                "mystery_hint_not_riddle",
                "Mystery hint must be a real short riddle, not a bare instruction.",
                quest,
                task,
                hint=hint,
            )
        )

    if "Место поиска:" in hint:
        issues.append(
            issue(
                "error",
                "mystery_hint_has_location",
                "Mystery hint must be a riddle and must not reveal a search location.",
                quest,
                task,
                hint=hint,
            )
        )

    forbidden_words = significant_title_words(answer_title)
    leaked_words = sorted(forbidden_words & normalized_words(f"{title} {hint}"))
    if leaked_words:
        issues.append(
            issue(
                "error",
                "mystery_answer_leaked",
                "Mystery title/hint must not directly name the answer or obvious answer words.",
                quest,
                task,
                answer_title=answer_title,
                leaked_words=leaked_words,
            )
        )

    return issues


def validate_strict_stage4_templates(
    task_object: dict[str, Any],
    template_id: str,
    selected_candidate: dict[str, Any] | None,
    quest: dict[str, Any],
    task: dict[str, Any],
    allowed_location_titles: set[str],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    issues.extend(validate_identifier_blank(task_object, template_id, quest, task))

    title = str(task_object.get("title") or "")
    hint = str(task_object.get("hint") or "")

    if template_id == "TT-001":
        person = title.replace("Поговори с ", "", 1).strip() if title.startswith("Поговори с ") else ""
        expected_title = "Поговори с [персонаж]"
        issues.extend(
            []
            if person
            else [
                strict_text_issue(
                    "TT-001 title must keep the exact fixed template text.",
                    quest,
                    task,
                    "title",
                    expected_title,
                    title,
                )
            ]
        )

        object_pronoun, subject_pronoun = dialogue_pronouns(quest, person)
        expected_prefix = (
            f"Поговори с {person}. Для этого просто кликни на {object_pronoun}. "
            f"{subject_pronoun} находится в "
        )
        if not person or not hint.startswith(expected_prefix) or not hint.endswith("."):
            issues.append(
                strict_text_issue(
                    "TT-001 hint must keep exact fixed text around the character and location.",
                    quest,
                    task,
                    "hint",
                    (
                        "Поговори с [персонаж]. Для этого просто кликни на [него/неё]. "
                        "[Он/Она] находится в [локация]."
                    ),
                    hint,
                )
            )
        else:
            location_text = hint[len(expected_prefix) : -1].strip()
            issues.extend(
                validate_location_text(
                    location_text,
                    allowed_location_titles,
                    quest,
                    task,
                    "strict_dialog_location_unknown",
                )
            )

        icon = str(task_object.get("icon") or "")
        action = str(task_object.get("action") or "")
        go_to_location = task_object.get("go_to_location")
        first_classname = ""
        if isinstance(go_to_location, list) and go_to_location and isinstance(go_to_location[0], dict):
            first_classname = str(go_to_location[0].get("classname") or "")
        if icon and first_classname != icon:
            issues.append(
                issue(
                    "error",
                    "strict_dialog_location_target_mismatch",
                    "TT-001 go_to_location classname must match the dialog icon character classname.",
                    quest,
                    task,
                    expected=icon,
                    actual=first_classname,
                )
            )
        if icon and not action.startswith(f"{icon}_Dialog_"):
            issues.append(
                issue(
                    "error",
                    "strict_dialog_action_mismatch",
                    "TT-001 action must be [Character classname]_Dialog_[Номер].",
                    quest,
                    task,
                    expected=f"{icon}_Dialog_[Номер]",
                    actual=action,
                )
            )

    if template_id in {"TT-003", "TT-004"}:
        param = str(task_object.get("param") or "")
        expected_search_action = f"search_{param}" if param else ""
        if task_object.get("search_action") != expected_search_action:
            issues.append(
                issue(
                    "error",
                    "strict_hog_search_action_mismatch",
                    f"{template_id} search_action must be search_[HOG classname].",
                    quest,
                    task,
                    expected=expected_search_action,
                    actual=task_object.get("search_action"),
                )
            )

        expected_after_buy_actions = [{"do": "remove_stuff", "classname": param}]
        if task_object.get("after_buy_actions") != expected_after_buy_actions:
            issues.append(
                issue(
                    "error",
                    "strict_hog_after_buy_actions_mismatch",
                    f"{template_id} after_buy_actions must remove the generated HOG stuff.",
                    quest,
                    task,
                    expected=expected_after_buy_actions,
                    actual=task_object.get("after_buy_actions"),
                )
            )

        if not title.startswith(HOG_TITLE_PREFIXES) or not title_item_text(title):
            issues.append(
                issue(
                    "error",
                    "hog_title_not_object_search",
                    "HOG title must be a short search action for a concrete object/resource/character/beast.",
                    quest,
                    task,
                    title=title,
                )
            )

        expected_suffix = ". Если найти все не удаётся, можно купить подсказку."
        expected_prefix = f"{title}. Место поиска: "
        if not hint.startswith(expected_prefix) or not hint.endswith(expected_suffix):
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    f"{template_id} hint must keep exact fixed text around the title and location.",
                    quest,
                    task,
                    expected=f"{title}. Место поиска: [локация]{expected_suffix}",
                    actual=hint,
                )
            )
        else:
            location_text = hint[len(expected_prefix) : -len(expected_suffix)].strip()
            if template_id == "TT-003":
                if location_text != "Мир":
                    issues.append(
                        strict_text_issue(
                            "TT-003 hint must use fixed location 'Мир'.",
                            quest,
                            task,
                            "hint",
                            f"{title}. Место поиска: Мир{expected_suffix}",
                            hint,
                        )
                    )
            else:
                issues.extend(
                    validate_location_text(
                        location_text,
                        allowed_location_titles,
                        quest,
                        task,
                        "strict_hog_location_unknown",
                    )
                )

    if template_id == "TT-005":
        item = title_item_text(title)
        if not title.startswith("Найди ") or not item:
            issues.append(
                strict_text_issue(
                    "TT-005 title must be exactly 'Найди [название скрытого предмета]'.",
                    quest,
                    task,
                    "title",
                    "Найди [название скрытого предмета]",
                    title,
                )
            )
        expected_prefix = f"Найди {item}. Они могут быть в "
        if item and (not hint.startswith(expected_prefix) or not hint.endswith(".")):
            issues.append(
                strict_text_issue(
                    "TT-005 hint must keep exact fixed text around the hidden item and home locations.",
                    quest,
                    task,
                    "hint",
                    f"Найди {item}. Они могут быть в [список домашних локаций].",
                    hint,
                )
            )
        elif item:
            location_text = hint[len(expected_prefix) : -1].strip()
            issues.extend(
                validate_location_text(
                    location_text,
                    allowed_location_titles,
                    quest,
                    task,
                    "strict_hog_location_unknown",
                )
            )

    if template_id in {"TT-006", "TT-007"}:
        if not title:
            issues.append(
                strict_text_issue(
                    f"{template_id} title must fill the template placeholder with a non-empty object clue.",
                    quest,
                    task,
                    "title",
                    "[заполненный текст]",
                    title,
                )
            )
        if not hint or not hint.endswith("."):
            issues.append(
                strict_text_issue(
                    f"{template_id} hint must fill the template placeholder and end with a period.",
                    quest,
                    task,
                    "hint",
                    "[заполненная подсказка].",
                    hint,
                )
            )

    if template_id == "TT-009":
        if not title.startswith("Попроси у друзей ") or not title_item_text(title):
            issues.append(
                strict_text_issue(
                    "TT-009 title must be exactly 'Попроси у друзей [название предмета]'.",
                    quest,
                    task,
                    "title",
                    "Попроси у друзей [название предмета]",
                    title,
                )
            )
        issues.extend(
            validate_exact_text(
                task_object,
                quest,
                task,
                "hint",
                "Отправь личные просьбы друзьям или купи.",
                "TT-009 hint must keep the exact fixed template text.",
            )
        )

    if template_id == "TT-010":
        item = title_item_text(title)
        if not title.startswith("Найди ") or not item:
            issues.append(
                strict_text_issue(
                    "TT-010 title must be exactly 'Найди [название ресурса]'.",
                    quest,
                    task,
                    "title",
                    "Найди [название ресурса]",
                    title,
                )
            )
        expected_prefix = f"{item} можно получить за сбор коллекции "
        expected_middle = " при уборке мусора в локации "
        expected_suffix = " дома и в гостях."
        if item and (not hint.startswith(expected_prefix) or expected_middle not in hint or not hint.endswith(expected_suffix)):
            issues.append(
                strict_text_issue(
                    "TT-010 hint must keep the exact fixed template text.",
                    quest,
                    task,
                    "hint",
                    f"{item} можно получить за сбор коллекции [название коллекции] при уборке мусора в локации [локация] дома и в гостях.",
                    hint,
                )
            )
        elif item:
            location_text = hint.split(expected_middle, 1)[1][: -len(expected_suffix)].strip()
            issues.extend(
                validate_location_text(
                    location_text,
                    allowed_location_titles,
                    quest,
                    task,
                    "strict_collection_reward_location_unknown",
                )
            )

    if template_id == "TT-011" and selected_candidate:
        source_title = str(selected_candidate.get("source_title") or "")
        location_text = selected_location_text(selected_candidate)
        if not title.startswith("Найди ") or not title_item_text(title):
            issues.append(strict_text_issue("TT-011 title must keep 'Найди [collection title]'.", quest, task, "title", "Найди [collection title]", title))
        if location_text:
            expected_middle = f" - элемент коллекции, выпадает при уборке мусора {source_title} дома и в гостях. Место поиска: {location_text}."
            if not hint.endswith(expected_middle):
                issues.append(strict_text_issue("TT-011 hint must keep the fixed text and full location list.", quest, task, "hint", f"[collection title]{expected_middle}", hint))

    if template_id == "TT-012":
        item = title_item_text(title)
        if not title.startswith("Получи ") or not item:
            issues.append(
                strict_text_issue(
                    "TT-012 title must be exactly 'Получи [название ресурса]'.",
                    quest,
                    task,
                    "title",
                    "Получи [название ресурса]",
                    title,
                )
            )
        expected_prefix = f"{item} можно получить "
        if item and not hint.startswith(expected_prefix):
            issues.append(
                strict_text_issue(
                    "TT-012 hint must keep the exact fixed template text prefix.",
                    quest,
                    task,
                    "hint",
                    f"{item} можно получить [описание действия на площади у друга]",
                    hint,
                )
            )

    if template_id == "TT-013":
        item = title_item_text(title)
        if not title.startswith("Найди ") or not item:
            issues.append(
                strict_text_issue(
                    "TT-013 title must be exactly 'Найди [название ресурса]'.",
                    quest,
                    task,
                    "title",
                    "Найди [название ресурса]",
                    title,
                )
            )
        expected_prefix = "Убирай мусор в локации "
        expected_suffix = " дома, чтобы найти."
        if not hint.startswith(expected_prefix) or not hint.endswith(expected_suffix):
            issues.append(
                strict_text_issue(
                    "TT-013 hint must keep the exact fixed template text.",
                    quest,
                    task,
                    "hint",
                    "Убирай мусор в локации [локация] дома, чтобы найти.",
                    hint,
                )
            )
        else:
            location_text = hint[len(expected_prefix) : -len(expected_suffix)].strip()
            issues.extend(validate_location_text(location_text, allowed_location_titles, quest, task, "strict_gr_location_unknown"))

    if template_id in {"TT-014", "TT-015"} and selected_candidate:
        item = title_item_text(title)
        mode_text = "в гостях" if template_id == "TT-014" else "дома"
        location_text = selected_location_text(selected_candidate)
        expected_title_prefix = "Найди "
        if not title.startswith(expected_title_prefix) or not item:
            issues.append(
                strict_text_issue(
                    f"{template_id} title must be exactly 'Найди [название ресурса]'.",
                    quest,
                    task,
                    "title",
                    "Найди [название ресурса]",
                    title,
                )
            )
        if location_text:
            expected_prefix = "Убирай мусор "
            expected_suffix = f" {mode_text}, чтобы найти. Место поиска: {location_text}."
            if not hint.startswith(expected_prefix) or not hint.endswith(expected_suffix):
                issues.append(strict_text_issue(f"{template_id} hint must keep the fixed text and full location list.", quest, task, "hint", f"Убирай мусор [garbage title] {mode_text}, чтобы найти. Место поиска: {location_text}.", hint))

    if template_id == "TT-017":
        flower_title = candidate_title_for_template(template_id, selected_candidate)
        expected_hint = (
            f"Собирай цветы {flower_title} дома, чтобы найти. "
            "Чтобы собрать растение, кликни на горшок с нужным растением."
        )
        if not title.startswith("Получи ") or not title_item_text(title):
            issues.append(
                strict_text_issue(
                    "TT-017 title must be exactly 'Получи [название ресурса]'.",
                    quest,
                    task,
                    "title",
                    "Получи [название ресурса]",
                    title,
                )
            )
        if flower_title:
            issues.extend(validate_exact_text(task_object, quest, task, "hint", expected_hint, "TT-017 hint must keep the exact fixed template text."))

    if template_id in {"TT-018", "TT-019"} and selected_candidate:
        flower_title = candidate_title_for_template(template_id, selected_candidate)
        place = "дома" if template_id == "TT-018" else "в гостях"
        expected_title = f"Собери {upper_first(simple_nominative_to_accusative(flower_title))} {place}"
        expected_hint = f"Собирай {flower_title} {place}. Чтобы собрать растение, кликни на горшок с нужным растением"
        if template_id == "TT-019":
            expected_hint += " в гостях у друга"
        issues.extend(validate_exact_text(task_object, quest, task, "title", expected_title, f"{template_id} title must keep the exact fixed template text."))
        issues.extend(validate_exact_text(task_object, quest, task, "hint", expected_hint, f"{template_id} hint must keep the exact fixed template text."))

    if template_id == "TT-021" and selected_candidate:
        location_text = selected_location_text(selected_candidate)
        if not title.startswith("Убери мусор ") or not title.endswith(" дома"):
            issues.append(strict_text_issue("TT-021 title must keep 'Убери мусор [garbage title] дома'.", quest, task, "title", "Убери мусор [garbage title] дома", title))
        if location_text:
            expected_prefix = "Убери мусор "
            expected_suffix = f" дома. Для этого просто кликни на нужный мусор дома. Место поиска: {location_text}."
            if not hint.startswith(expected_prefix) or not hint.endswith(expected_suffix):
                issues.append(strict_text_issue("TT-021 hint must keep the fixed text and full location list.", quest, task, "hint", f"Убери мусор [garbage title] дома. Для этого просто кликни на нужный мусор дома. Место поиска: {location_text}.", hint))

    if template_id == "TT-027":
        issues.extend(
            validate_exact_text(
                task_object,
                quest,
                task,
                "hint",
                "Прочитай фразу задания задом наперед.",
                "TT-027 hint must keep the exact fixed template text.",
            )
        )
        answer_title = candidate_title_for_template(template_id, selected_candidate)
        if answer_title:
            leaked_words = sorted(significant_title_words(answer_title) & normalized_words(title))
            if leaked_words:
                issues.append(
                    issue(
                        "error",
                        "reverse_mystery_answer_leaked",
                        "TT-027 title must be a reverse clue and must not directly name the collection answer.",
                        quest,
                        task,
                        answer_title=answer_title,
                        leaked_words=leaked_words,
                    )
                )

    if template_id in FIXED_TITLE_HINTS:
        expected_title, expected_hint = FIXED_TITLE_HINTS[template_id]
        issues.extend(validate_exact_text(task_object, quest, task, "title", expected_title, f"{template_id} title must keep the exact fixed template text."))
        issues.extend(validate_exact_text(task_object, quest, task, "hint", expected_hint, f"{template_id} hint must keep the exact fixed template text."))

    if template_id == "TT-033":
        if not title:
            issues.append(strict_text_issue("TT-033 title must fill '[Действие] [название предмета]'.", quest, task, "title", "[Действие] [название предмета]", title))
        expected_prefix = ""
        expected_suffix = "."
        if "Он находится на " not in hint or not hint.endswith(expected_suffix):
            issues.append(
                strict_text_issue(
                    "TT-033 hint must keep fixed location sentence: 'Он находится на [локация].'",
                    quest,
                    task,
                    "hint",
                    "[Инструкция как передать предмет]. Он находится на [локация].",
                    hint,
                )
            )
        else:
            location_text = hint.rsplit("Он находится на ", 1)[1][:-1].strip()
            issues.extend(validate_location_text(location_text, allowed_location_titles, quest, task, "strict_give_location_unknown"))

    if template_id == "TT-034":
        person = title.replace("Сфотографируйся с ", "", 1).strip() if title.startswith("Сфотографируйся с ") else ""
        if not person:
            issues.append(
                strict_text_issue(
                    "TT-034 title must be exactly 'Сфотографируйся с [персонаж]'.",
                    quest,
                    task,
                    "title",
                    "Сфотографируйся с [персонаж]",
                    title,
                )
            )
        location_match = re.search(
            r" - персонаж, с которым нужно сфотографироваться\. Найди .+? у себя на (.+?) и нажми на иконку \"Сделать фотографию\"",
            hint,
        )
        expected_tail = " и нажми \"Славненько\"."
        if person and (location_match is None or not hint.endswith(expected_tail)):
            issues.append(
                strict_text_issue(
                    "TT-034 hint must keep the exact fixed template text around the character and location.",
                    quest,
                    task,
                    "hint",
                    "[персонаж] - персонаж, с которым нужно сфотографироваться. Найди [его/её] у себя на [локация] и нажми на иконку \"Сделать фотографию\" в правом верхнем углу. Наведи фокус на [персонаж], сфотографируйся с [ним/ней] и нажми \"Славненько\".",
                    hint,
                )
            )
        elif person and location_match is not None:
            location_text = location_match.group(1).strip()
            issues.extend(validate_location_text(location_text, allowed_location_titles, quest, task, "strict_photo_location_unknown"))
        icon = str(task_object.get("icon") or "")
        param = str(task_object.get("param") or "")
        if icon and param and icon != param:
            issues.append(
                issue(
                    "error",
                    "strict_photo_icon_param_mismatch",
                    "TT-034 icon and param must use the same character classname.",
                    quest,
                    task,
                    expected=icon,
                    actual=param,
                )
            )

    if template_id == "TT-008":
        if not title.startswith("Попроси у друзей ") or not title_item_text(title):
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-008 title must be exactly 'Попроси у друзей [название предмета]'.",
                    quest,
                    task,
                    expected="Попроси у друзей [название предмета]",
                    actual=title,
                )
            )
        if hint != "Попроси у друзей или купи.":
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-008 hint must keep the exact fixed template text.",
                    quest,
                    task,
                    expected="Попроси у друзей или купи.",
                    actual=hint,
                )
            )

    if template_id == "TT-016":
        flower_title = candidate_title_for_template(template_id, selected_candidate)
        expected_hint = (
            f"Собирай цветы {flower_title} в гостях, чтобы найти. "
            "Чтобы собрать растение, кликни на горшок с нужным растением в гостях у друга"
        )
        if not title.startswith("Получи ") or not title_item_text(title):
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-016 title must be exactly 'Получи [название ресурса]'.",
                    quest,
                    task,
                    expected="Получи [название ресурса]",
                    actual=title,
                )
            )
        if flower_title and hint != expected_hint:
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-016 hint must keep the exact fixed template text.",
                    quest,
                    task,
                    expected=expected_hint,
                    actual=hint,
                )
            )

    if template_id == "TT-002":
        if not title.startswith("Создай ") or not title_item_text(title):
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-002 title must be exactly 'Создай [название предмета]'.",
                    quest,
                    task,
                    expected="Создай [название предмета]",
                    actual=title,
                )
            )
        if hint != "Для создания используй Станок.":
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-002 hint must keep the exact fixed template text.",
                    quest,
                    task,
                    expected="Для создания используй Станок.",
                    actual=hint,
                )
            )
        go_to_location = task_object.get("go_to_location")
        expected_prefix = f"{quest_prefix(quest.get('classname_quests'))}_Workbench_"
        first_classname = ""
        if isinstance(go_to_location, list) and go_to_location and isinstance(go_to_location[0], dict):
            first_classname = str(go_to_location[0].get("classname") or "")
        if not first_classname.startswith(expected_prefix):
            issues.append(
                issue(
                    "error",
                    "strict_craft_workbench_mismatch",
                    "TT-002 go_to_location must point to the generated Workbench classname.",
                    quest,
                    task,
                    expected=f"{expected_prefix}[Номер]",
                    actual=first_classname,
                )
            )

    if template_id == "TT-020" and selected_candidate:
        location_text = selected_location_text(selected_candidate)
        if not title.startswith("Убери мусор ") or not title.endswith(" в гостях"):
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-020 title must keep the exact fixed template text.",
                    quest,
                    task,
                    expected="Убери мусор [garbage title] в гостях",
                    actual=title,
                )
            )
        expected_prefix = "Убери мусор "
        expected_suffix = f" в гостях. Для этого просто кликни на нужный мусор в гостях у друга. Место поиска: {location_text}."
        if location_text and (not hint.startswith(expected_prefix) or not hint.endswith(expected_suffix)):
            issues.append(
                issue(
                    "error",
                    "strict_template_text_mismatch",
                    "TT-020 hint must keep the exact fixed template text and full location list.",
                    quest,
                    task,
                    expected=f"Убери мусор [garbage title] в гостях. Для этого просто кликни на нужный мусор в гостях у друга. Место поиска: {location_text}.",
                    actual=hint,
                )
            )

    if template_id in MYSTERY_TITLES:
        answer_title = candidate_title_for_template(template_id, selected_candidate)
        if answer_title:
            issues.extend(validate_mystery_riddle_text(task_object, template_id, answer_title, quest, task))

    return issues


def quest_prefix(classname_quests: Any) -> str:
    value = str(classname_quests or "")
    marker = "_Story_"
    if marker in value:
        return value.split(marker, 1)[0]
    return value


def validate_generated_sequences(
    filled_tasks: dict[str, Any],
    sequence_offsets: dict[tuple[str, str], int] | None = None,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    sequence_offsets = sequence_offsets or {}
    counters: dict[tuple[str, str], int] = {}
    for quest in filled_tasks.get("quests", []):
        prefix = quest_prefix(quest.get("classname_quests"))
        for task in quest.get("tasks", []):
            template_id = task.get("task_template_id")
            rule = GENERATED_SEQUENCE_RULES.get(template_id)
            if not rule:
                continue
            kind, field_name = rule
            key = (prefix, kind)
            counters[key] = counters.get(key, sequence_offsets.get(key, 0)) + 1
            expected = f"{prefix}_{kind}_{counters[key]}"
            task_object = task.get("task_object") or {}
            actual = task_object.get(field_name)
            if actual != expected:
                issues.append(
                    issue(
                        "error",
                        "generated_classname_sequence_mismatch",
                        "Generated classname numbering must be sequential per entity kind, not based on task number.",
                        quest,
                        task,
                        field=field_name,
                        sequence_offset=sequence_offsets.get(key, 0),
                        expected=expected,
                        actual=actual,
                    )
                )

            icon = task_object.get("icon")
            if field_name == "classname" and icon is not None and icon != actual:
                issues.append(
                    issue(
                        "error",
                        "generated_icon_mismatch",
                        "Generated icon must match generated classname.",
                        quest,
                        task,
                        expected=actual,
                        actual=icon,
                    )
                )
    return issues


def selected_candidate_for_task(
    quest: dict[str, Any],
    task: dict[str, Any],
    context_index: dict[tuple[str, int], dict[str, Any]],
) -> dict[str, Any] | None:
    classname_quests = quest.get("classname_quests")
    task_number = task.get("task_number")
    if not classname_quests or not isinstance(task_number, int):
        return None
    context_task = context_index.get((classname_quests, task_number))
    if not context_task:
        return None
    return candidate_by_id(context_task, task.get("selected_candidate_id"))


def validate_cross_task_source_conflicts(
    filled_tasks: dict[str, Any],
    context_index: dict[tuple[str, int], dict[str, Any]],
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for quest in filled_tasks.get("quests", []):
        used_garbage: dict[str, int] = {}
        collection_sources: list[tuple[str, int, dict[str, Any]]] = []

        for task in quest.get("tasks", []):
            selected = selected_candidate_for_task(quest, task, context_index)
            if not selected:
                continue
            template_id = task.get("task_template_id")
            if template_id in GARBAGE_TEMPLATES and selected.get("garbage_classname"):
                used_garbage[str(selected["garbage_classname"])] = task.get("task_number")
            if template_id in COLLECTION_TEMPLATES and selected.get("source_type") == "garbage":
                source = selected.get("source_classname")
                if source:
                    collection_sources.append((str(source), task.get("task_number"), task))

        for source, task_number, task in collection_sources:
            if source in used_garbage:
                issues.append(
                    issue(
                        "error",
                        "collection_source_reuses_selected_garbage",
                        "Do not pair a garbage task and a collection drop from the same garbage in one quest unless explicitly overridden.",
                        quest,
                        task,
                        source_classname=source,
                        garbage_task_number=used_garbage[source],
                        collection_task_number=task_number,
                    )
                )
    return issues


def validate_craft_resource_links(filled_tasks: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for quest in filled_tasks.get("quests", []):
        craft_items = [
            title_item_text((task.get("task_object") or {}).get("title"))
            for task in quest.get("tasks", [])
            if task.get("task_template_id") in CRAFT_TEMPLATES
        ]
        craft_words = set().union(*(significant_title_words(item) for item in craft_items)) if craft_items else set()
        if not craft_items:
            continue

        for task in quest.get("tasks", []):
            if task.get("task_template_id") not in GENERATED_ASSET_TEMPLATES:
                continue

            task_object = task.get("task_object") or {}
            resource_title = title_item_text(task_object.get("title"))
            reason = str(task.get("choice_reason") or "")
            combined_words = significant_title_words(f"{resource_title} {reason}")
            reason_normalized = reason.lower().replace("ё", "е")
            has_craft_word = bool(craft_words & combined_words)
            has_link_marker = any(marker in reason_normalized for marker in CRAFT_LINK_REASON_MARKERS)
            if not has_craft_word and not has_link_marker:
                issues.append(
                    issue(
                        "error",
                        "craft_resource_reason_too_generic",
                        "Generated ASK/PER/GR in a craft quest must explain how the resource is an ingredient, part, or close component of the crafted item.",
                        quest,
                        task,
                        craft_items=craft_items,
                        resource_title=resource_title,
                        choice_reason=reason,
                    )
                )

    return issues


def validate_task(
    quest: dict[str, Any],
    task: dict[str, Any],
    context_index: dict[tuple[str, int], dict[str, Any]],
    context_quest_index: dict[str, dict[str, Any]],
    templates: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    issues: list[dict[str, Any]] = []
    template_id = task.get("task_template_id")
    task_number = task.get("task_number")
    classname_quests = quest.get("classname_quests")
    task_object = task.get("task_object")

    if not template_id:
        issues.append(issue("error", "missing_task_template_id", "Filled task is missing task_template_id.", quest, task))
        template_id = ""

    template = templates.get(template_id)
    if template is None:
        issues.append(issue("error", "unknown_task_template_id", "Task template ID is not in template catalog.", quest, task))
    elif template.get("status") == "not_ready":
        issues.append(issue("error", "not_ready_task_template", "TT-035/not_ready template must not be used.", quest, task))

    if not isinstance(task_object, dict):
        issues.append(issue("error", "missing_task_object", "Filled task is missing task_object.", quest, task))
        return {"status": "error", "errors": len(issues), "warnings": 0}, issues

    context_task = None
    if classname_quests and isinstance(task_number, int):
        context_task = context_index.get((classname_quests, task_number))
    if context_task is None:
        issues.append(issue("error", "context_task_not_found", "Task was not found in context_pack.", quest, task))
    elif context_task.get("task_template_id") != template_id:
        issues.append(
            issue(
                "error",
                "context_template_mismatch",
                "Task template ID differs from context_pack.",
                quest,
                task,
                expected=context_task.get("task_template_id"),
                actual=template_id,
            )
        )

    selected_candidate = None
    selected_candidate_id = task.get("selected_candidate_id")
    if context_task is not None:
        candidate_domain = context_task.get("candidate_domain")
        candidates = context_task.get("candidates", [])
        if candidates:
            if not selected_candidate_id:
                issues.append(issue("error", "missing_selected_candidate", "Task must select a candidate from context_pack.", quest, task))
            else:
                selected_candidate = candidate_by_id(context_task, selected_candidate_id)
                if selected_candidate is None:
                    issues.append(
                        issue(
                            "error",
                            "selected_candidate_not_found",
                            "selected_candidate_id is not present in context_pack candidates for this task.",
                            quest,
                            task,
                            selected_candidate_id=selected_candidate_id,
                        )
                    )
        elif candidate_domain:
            issues.append(issue("warning", "context_task_has_no_candidates", "Context task expected candidates but none were available.", quest, task))
        elif selected_candidate_id:
            issues.append(issue("warning", "unneeded_selected_candidate", "Task has selected_candidate_id but context task does not need candidates.", quest, task))

    issues.extend(validate_required_fields(task_object, template_id, quest, task))
    issues.extend(validate_expected_values(task_object, template_id, quest, task))
    issues.extend(validate_dialogue_replica(task_object, quest, task))
    if selected_candidate is not None:
        issues.extend(validate_candidate_match(task_object, template_id, selected_candidate, quest, task))
    issues.extend(validate_generated_naming(task_object, template_id, quest, task))
    issues.extend(validate_generated_item_concreteness(task_object, template_id, quest, task))
    allowed_location_titles = context_quest_location_titles(context_quest_index.get(classname_quests))
    issues.extend(
        validate_location_references(
            task_object,
            template_id,
            quest,
            task,
            allowed_location_titles,
        )
    )
    issues.extend(
        validate_strict_stage4_templates(
            task_object,
            template_id,
            selected_candidate,
            quest,
            task,
            allowed_location_titles,
        )
    )

    errors = sum(1 for item in issues if item["severity"] == "error")
    warnings = sum(1 for item in issues if item["severity"] == "warning")
    status = "ok" if errors == 0 else "error"
    if status == "ok" and warnings:
        status = "warning"
    return {"status": status, "errors": errors, "warnings": warnings}, issues


def validate_filled_tasks(
    filled_tasks: dict[str, Any],
    context_pack: dict[str, Any],
    templates: dict[str, dict[str, Any]],
    sequence_offsets: dict[tuple[str, str], int] | None = None,
) -> dict[str, Any]:
    context_index = build_context_task_index(context_pack)
    context_quest_index = build_context_quest_index(context_pack)
    task_results: list[dict[str, Any]] = []
    all_issues: list[dict[str, Any]] = []

    for quest, task in build_filled_task_rows(filled_tasks):
        result, issues = validate_task(quest, task, context_index, context_quest_index, templates)
        task_results.append(
            {
                "classname_quests": quest.get("classname_quests"),
                "quest_number": quest.get("quest_number"),
                "task_number": task.get("task_number"),
                "task_template_id": task.get("task_template_id"),
                **result,
            }
        )
        all_issues.extend(issues)

    all_issues.extend(validate_cross_task_source_conflicts(filled_tasks, context_index))
    all_issues.extend(validate_craft_resource_links(filled_tasks))
    all_issues.extend(validate_generated_sequences(filled_tasks, sequence_offsets=sequence_offsets))

    errors = [item for item in all_issues if item["severity"] == "error"]
    warnings = [item for item in all_issues if item["severity"] == "warning"]
    return {
        "summary": {
            "quests_found": len(filled_tasks.get("quests", [])),
            "tasks_found": len(task_results),
            "valid_tasks": sum(1 for item in task_results if item["status"] in {"ok", "warning"}),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "tasks": task_results,
        "errors": errors,
        "warnings": warnings,
    }


def render_preview(validation: dict[str, Any]) -> str:
    summary = validation["summary"]
    lines = [
        "# Filled Tasks Validation",
        "",
        f"Quests found: {summary['quests_found']}",
        f"Tasks found: {summary['tasks_found']}",
        f"Valid tasks: {summary['valid_tasks']}",
        f"Errors: {summary['errors']}",
        f"Warnings: {summary['warnings']}",
        "",
        "## Tasks",
        "",
        "| Quest | Task | Template | Status | Errors | Warnings |",
        "|-------|------|----------|--------|--------|----------|",
    ]
    for task in validation["tasks"]:
        lines.append(
            "| "
            f"{task.get('classname_quests') or ''} | "
            f"{task.get('task_number') or ''} | "
            f"`{task.get('task_template_id') or ''}` | "
            f"{task.get('status') or ''} | "
            f"{task.get('errors', 0)} | "
            f"{task.get('warnings', 0)} |"
        )

    if validation["errors"]:
        lines.extend(["", "## Errors", ""])
        for item in validation["errors"]:
            lines.append(
                f"- `{item['code']}` {item.get('classname_quests')} task {item.get('task_number')}: {item['message']}"
            )

    if validation["warnings"]:
        lines.extend(["", "## Warnings", ""])
        for item in validation["warnings"]:
            lines.append(
                f"- `{item['code']}` {item.get('classname_quests')} task {item.get('task_number')}: {item['message']}"
            )

    lines.append("")
    return "\n".join(lines)


def validate_file(
    input_path: Path,
    context_pack_path: Path,
    templates_path: Path,
    output_json_path: Path,
    preview_path: Path,
    campaign_memory_path: Path | None = None,
    current_pack_id: str | None = None,
) -> dict[str, Any]:
    campaign_memory = read_json(campaign_memory_path) if campaign_memory_path and campaign_memory_path.exists() else None
    validation = validate_filled_tasks(
        filled_tasks=read_json(input_path),
        context_pack=read_json(context_pack_path),
        templates=build_template_catalog(templates_path),
        sequence_offsets=generated_sequence_offsets(campaign_memory, current_pack_id=current_pack_id),
    )
    write_json(output_json_path, validation)
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(render_preview(validation), encoding="utf-8")
    return validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate AI-filled stage 4 task objects before CSV export.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="AI-filled tasks JSON. Default: output/filled_tasks.json",
    )
    parser.add_argument(
        "--context-pack",
        type=Path,
        default=DEFAULT_CONTEXT_PACK_PATH,
        help="Context pack JSON used for stage 4 filling.",
    )
    parser.add_argument(
        "--templates",
        type=Path,
        default=DEFAULT_TEMPLATES_PATH,
        help="Task template catalog JSON.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON_PATH,
        help="Output validation JSON.",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=DEFAULT_PREVIEW_PATH,
        help="Output validation Markdown preview.",
    )
    parser.add_argument(
        "--campaign",
        default="",
        help="Campaign id. If set, uses campaigns/<campaign_id>/campaign_memory.json for campaign-wide generated numbering.",
    )
    parser.add_argument(
        "--campaign-memory",
        type=Path,
        default=None,
        help="Explicit campaign_memory.json path. Overrides --campaign.",
    )
    parser.add_argument(
        "--current-pack",
        default="",
        help="Current pack id to ignore when reading campaign memory, useful during edits.",
    )
    parser.add_argument(
        "--campaigns-dir",
        type=Path,
        default=DEFAULT_CAMPAIGNS_DIR,
        help="Campaigns directory used with --campaign.",
    )
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Создай output/filled_tasks.json на этапе 4 или смотри output/filled_tasks.example.json.")
        return 1
    if not args.context_pack.exists():
        print(f"context pack not found: {args.context_pack}")
        print("Сначала запусти: python src/build_context_pack.py output/quest_plan.resolved.json")
        return 1

    campaign_memory_path = args.campaign_memory
    if campaign_memory_path is None and args.campaign:
        campaign_memory_path = campaign_memory_path_for(args.campaign, args.campaigns_dir)
    if campaign_memory_path is not None and not campaign_memory_path.exists():
        print(f"campaign memory file not found: {campaign_memory_path}")
        return 1

    validation = validate_file(
        args.input,
        args.context_pack,
        args.templates,
        args.output_json,
        args.preview,
        campaign_memory_path=campaign_memory_path,
        current_pack_id=args.current_pack or None,
    )
    summary = validation["summary"]
    print(f"quests found: {summary['quests_found']}")
    print(f"tasks found: {summary['tasks_found']}")
    print(f"valid tasks: {summary['valid_tasks']}")
    print(f"errors: {summary['errors']}")
    print(f"warnings: {summary['warnings']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    if campaign_memory_path is not None:
        print(f"campaign memory used: {campaign_memory_path}")
    return 0 if summary["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
