from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


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
CRAFT_TEMPLATES = {"TT-002"}

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
}


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
    for prefix in ("Найди ", "Получи ", "Создай ", "Подари другу "):
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

    if template_id == "TT-003" and "Место поиска: Мир" in hint:
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


def quest_prefix(classname_quests: Any) -> str:
    value = str(classname_quests or "")
    marker = "_Story_"
    if marker in value:
        return value.split(marker, 1)[0]
    return value


def validate_generated_sequences(filled_tasks: dict[str, Any]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
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
            counters[key] = counters.get(key, 0) + 1
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
    issues.extend(
        validate_location_references(
            task_object,
            template_id,
            quest,
            task,
            context_quest_location_titles(context_quest_index.get(classname_quests)),
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
    all_issues.extend(validate_generated_sequences(filled_tasks))

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
) -> dict[str, Any]:
    validation = validate_filled_tasks(
        filled_tasks=read_json(input_path),
        context_pack=read_json(context_pack_path),
        templates=build_template_catalog(templates_path),
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
    args = parser.parse_args(argv)

    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Создай output/filled_tasks.json на этапе 4 или смотри output/filled_tasks.example.json.")
        return 1
    if not args.context_pack.exists():
        print(f"context pack not found: {args.context_pack}")
        print("Сначала запусти: python src/build_context_pack.py output/quest_plan.resolved.json")
        return 1

    validation = validate_file(args.input, args.context_pack, args.templates, args.output_json, args.preview)
    summary = validation["summary"]
    print(f"quests found: {summary['quests_found']}")
    print(f"tasks found: {summary['tasks_found']}")
    print(f"valid tasks: {summary['valid_tasks']}")
    print(f"errors: {summary['errors']}")
    print(f"warnings: {summary['warnings']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    return 0 if summary["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
