from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAMPAIGNS_DIR = PROJECT_ROOT / "campaigns"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"
DEFAULT_INPUT_DIR = PROJECT_ROOT / "input"
GENERATED_ASSET_KINDS = ("HOG", "GR", "ASK", "PER", "CL", "FA", "R", "Character")
TIMESTAMP_FIELDS = {"created_at", "updated_at", "first_seen_at", "last_seen_at"}
INTERACTIVE_OBJECTS_NAME = "interactive_objects.json"
INTERACTIVE_OBJECTS_PREVIEW_NAME = "interactive_objects.preview.md"

PACK_FILE_CANDIDATES = [
    (DEFAULT_INPUT_DIR / "stage3_quests.txt", "stage3_quests.txt"),
    (DEFAULT_INPUT_DIR / "manual_overrides.json", "manual_overrides.json"),
    (DEFAULT_OUTPUT_DIR / "quest_plan.json", "quest_plan.json"),
    (DEFAULT_OUTPUT_DIR / "quest_plan.preview.md", "quest_plan.preview.md"),
    (DEFAULT_OUTPUT_DIR / "quest_plan.overridden.json", "quest_plan.overridden.json"),
    (DEFAULT_OUTPUT_DIR / "manual_overrides_report.md", "manual_overrides_report.md"),
    (DEFAULT_OUTPUT_DIR / "quest_plan.resolved.json", "quest_plan.resolved.json"),
    (DEFAULT_OUTPUT_DIR / "quest_plan.resolved.preview.md", "quest_plan.resolved.preview.md"),
    (DEFAULT_OUTPUT_DIR / "context_pack.json", "context_pack.json"),
    (DEFAULT_OUTPUT_DIR / "context_pack.preview.md", "context_pack.preview.md"),
    (DEFAULT_OUTPUT_DIR / INTERACTIVE_OBJECTS_NAME, INTERACTIVE_OBJECTS_NAME),
    (DEFAULT_OUTPUT_DIR / INTERACTIVE_OBJECTS_PREVIEW_NAME, INTERACTIVE_OBJECTS_PREVIEW_NAME),
    (DEFAULT_OUTPUT_DIR / "filled_tasks.json", "filled_tasks.json"),
    (DEFAULT_OUTPUT_DIR / "filled_tasks.validation.json", "filled_tasks.validation.json"),
    (DEFAULT_OUTPUT_DIR / "filled_tasks.preview.md", "filled_tasks.preview.md"),
    (DEFAULT_OUTPUT_DIR / "quest_group.json", "quest_group.json"),
    (DEFAULT_OUTPUT_DIR / "quest_group.validation.json", "quest_group.validation.json"),
    (DEFAULT_OUTPUT_DIR / "quest_group.preview.md", "quest_group.preview.md"),
    (DEFAULT_OUTPUT_DIR / "generated_quests.csv", "generated_quests.csv"),
    (DEFAULT_OUTPUT_DIR / "generated_quests.with_quest_blocks.csv", "generated_quests.csv"),
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def load_json_or_default(path: Path, default: Any) -> Any:
    if path.exists():
        return read_json(path)
    return default


def without_timestamp_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: without_timestamp_fields(item)
            for key, item in value.items()
            if key not in TIMESTAMP_FIELDS
        }
    if isinstance(value, list):
        return [without_timestamp_fields(item) for item in value]
    return value


def preserve_memory_timestamps(memory: dict[str, Any], previous_memory: dict[str, Any] | None) -> None:
    if not isinstance(previous_memory, dict):
        return

    if previous_memory.get("created_at"):
        memory["created_at"] = previous_memory["created_at"]

    for bucket, entries in list(memory.items()):
        if not isinstance(entries, dict):
            continue
        previous_entries = previous_memory.get(bucket)
        if not isinstance(previous_entries, dict):
            continue
        for key, entry in entries.items():
            if not isinstance(entry, dict):
                continue
            previous_entry = previous_entries.get(key)
            if not isinstance(previous_entry, dict):
                continue
            if "first_seen_at" in previous_entry and "first_seen_at" in entry:
                entry["first_seen_at"] = previous_entry["first_seen_at"]
            if without_timestamp_fields(entry) == without_timestamp_fields(previous_entry):
                for field_name in ("created_at", "updated_at", "last_seen_at"):
                    if field_name in previous_entry and field_name in entry:
                        entry[field_name] = previous_entry[field_name]

    if (
        previous_memory.get("updated_at")
        and without_timestamp_fields(memory) == without_timestamp_fields(previous_memory)
    ):
        memory["updated_at"] = previous_memory["updated_at"]


def validate_campaign_id(campaign_id: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", campaign_id or ""):
        raise ValueError("campaign_id must contain only latin letters, digits, '_' or '-' and must not be empty.")
    return campaign_id


def pack_id_from_number(number: int) -> str:
    if number < 1:
        raise ValueError("pack number must be positive.")
    return f"pack_{number:03d}"


def campaign_dir(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    return campaigns_dir / validate_campaign_id(campaign_id)


def pack_dir(campaign_id: str, pack_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    return campaign_dir(campaign_id, campaigns_dir) / pack_id


def campaign_json_path(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    return campaign_dir(campaign_id, campaigns_dir) / "campaign.json"


def campaign_memory_path(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    return campaign_dir(campaign_id, campaigns_dir) / "campaign_memory.json"


def campaign_summary_path(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> Path:
    return campaign_dir(campaign_id, campaigns_dir) / "campaign_summary.md"


def default_campaign(campaign_id: str, title: str | None = None, tone: str | None = None, characters: list[str] | None = None) -> dict[str, Any]:
    created_at = now_iso()
    return {
        "version": 1,
        "campaign_id": campaign_id,
        "title": title or campaign_id,
        "tone": tone or "",
        "characters": characters or [],
        "status": "in_progress",
        "created_at": created_at,
        "updated_at": created_at,
        "next_pack_number": 1,
        "packs": [],
    }


def default_memory(campaign_id: str) -> dict[str, Any]:
    created_at = now_iso()
    return {
        "version": 1,
        "campaign_id": campaign_id,
        "created_at": created_at,
        "updated_at": created_at,
        "packs": {},
        "used_candidate_ids": {},
        "used_task_templates": {},
        "used_garbage": {},
        "used_collections": {},
        "used_flowers": {},
        "used_locations": {},
        "used_generated_assets": {},
    }


def load_campaign(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> dict[str, Any]:
    path = campaign_json_path(campaign_id, campaigns_dir)
    if not path.exists():
        raise FileNotFoundError(f"campaign not found: {path}")
    return read_json(path)


def load_memory(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> dict[str, Any]:
    path = campaign_memory_path(campaign_id, campaigns_dir)
    return load_json_or_default(path, default_memory(campaign_id))


def save_campaign(campaign: dict[str, Any], campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> None:
    write_json(campaign_json_path(str(campaign["campaign_id"]), campaigns_dir), campaign)


def save_memory(memory: dict[str, Any], campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> None:
    write_json(campaign_memory_path(str(memory["campaign_id"]), campaigns_dir), memory)


def create_campaign(
    campaign_id: str,
    title: str | None = None,
    tone: str | None = None,
    characters: list[str] | None = None,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    overwrite: bool = False,
) -> dict[str, Any]:
    campaign_id = validate_campaign_id(campaign_id)
    path = campaign_json_path(campaign_id, campaigns_dir)
    if path.exists() and not overwrite:
        return read_json(path)

    campaign = default_campaign(campaign_id, title=title, tone=tone, characters=characters)
    memory = default_memory(campaign_id)
    save_campaign(campaign, campaigns_dir)
    save_memory(memory, campaigns_dir)
    interactive_path = campaign_dir(campaign_id, campaigns_dir) / INTERACTIVE_OBJECTS_NAME
    if not interactive_path.exists():
        write_json(interactive_path, {"version": 1, "selected_objects": []})
    render_campaign_summary(campaign_id, campaigns_dir)
    return campaign


def create_pack(
    campaign_id: str,
    title: str | None = None,
    notes: str | None = None,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    pack_number: int | None = None,
) -> dict[str, Any]:
    campaign = load_campaign(campaign_id, campaigns_dir)
    if pack_number is None:
        pack_number = int(campaign.get("next_pack_number") or 1)
    pack_id = pack_id_from_number(pack_number)
    target = pack_dir(campaign_id, pack_id, campaigns_dir)
    target.mkdir(parents=True, exist_ok=True)

    pack = {
        "pack_id": pack_id,
        "pack_number": pack_number,
        "title": title or "",
        "notes": notes or "",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "status": "created",
    }
    write_json(target / "pack.json", pack)

    stage3_path = target / "stage3_quests.txt"
    if not stage3_path.exists():
        write_text(stage3_path, "")

    packs = campaign.setdefault("packs", [])
    if pack_id not in [item.get("pack_id") for item in packs if isinstance(item, dict)]:
        packs.append({"pack_id": pack_id, "title": title or "", "created_at": pack["created_at"]})
    campaign["next_pack_number"] = max(int(campaign.get("next_pack_number") or 1), pack_number + 1)
    campaign["updated_at"] = now_iso()
    save_campaign(campaign, campaigns_dir)
    render_campaign_summary(campaign_id, campaigns_dir)
    return pack


def copy_current_output_to_pack(
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    overwrite: bool = True,
) -> list[str]:
    target = pack_dir(campaign_id, pack_id, campaigns_dir)
    target.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for source, relative_name in PACK_FILE_CANDIDATES:
        if not source.exists():
            continue
        destination = target / relative_name
        if destination.exists() and not overwrite:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied.append(relative_name)
    return copied


def context_task_index(context_pack: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    result: dict[tuple[str, int], dict[str, Any]] = {}
    for quest in context_pack.get("quests", []):
        classname = quest.get("classname_quests")
        for task in quest.get("tasks", []):
            number = task.get("task_number")
            if classname and isinstance(number, int):
                result[(str(classname), number)] = task
    return result


def candidate_by_id(context_task: dict[str, Any] | None, candidate_id: Any) -> dict[str, Any] | None:
    if context_task is None or not candidate_id:
        return None
    for candidate in context_task.get("candidates", []):
        if candidate.get("candidate_id") == candidate_id:
            return candidate
    return None


def add_usage(memory: dict[str, Any], bucket: str, key: Any, data: dict[str, Any]) -> None:
    if key in (None, ""):
        return
    key = str(key)
    values = memory.setdefault(bucket, {})
    existing = values.setdefault(key, {**data, "uses": 0, "first_seen_at": now_iso()})
    existing["uses"] = int(existing.get("uses", 0)) + 1
    existing["last_seen_at"] = now_iso()
    for field_name, value in data.items():
        if value not in (None, "", []):
            existing.setdefault(field_name, value)


def collect_locations(memory: dict[str, Any], candidate: dict[str, Any], pack_id: str, quest: dict[str, Any], task: dict[str, Any]) -> None:
    for location in candidate.get("locations") or []:
        title = location.get("title")
        code = location.get("code")
        key = title or code
        add_usage(
            memory,
            "used_locations",
            key,
            {
                "code": code,
                "title": title,
                "pack_id": pack_id,
                "classname_quests": quest.get("classname_quests"),
                "task_number": task.get("task_number"),
            },
        )


def collect_candidate_usage(
    memory: dict[str, Any],
    candidate: dict[str, Any],
    pack_id: str,
    quest: dict[str, Any],
    task: dict[str, Any],
) -> None:
    ref = {
        "pack_id": pack_id,
        "classname_quests": quest.get("classname_quests"),
        "task_number": task.get("task_number"),
        "task_template_id": task.get("task_template_id"),
    }
    add_usage(memory, "used_candidate_ids", candidate.get("candidate_id"), {**ref, "domain": candidate.get("domain")})
    add_usage(
        memory,
        "used_garbage",
        candidate.get("garbage_classname"),
        {**ref, "classname": candidate.get("garbage_classname"), "title": candidate.get("garbage_title")},
    )
    if candidate.get("source_type") == "garbage":
        add_usage(
            memory,
            "used_garbage",
            candidate.get("source_classname"),
            {**ref, "classname": candidate.get("source_classname"), "title": candidate.get("source_title"), "used_as": "collection_source"},
        )
    add_usage(
        memory,
        "used_collections",
        candidate.get("collection_classname"),
        {**ref, "classname": candidate.get("collection_classname"), "title": candidate.get("collection_title")},
    )
    add_usage(
        memory,
        "used_flowers",
        candidate.get("flower_classname"),
        {**ref, "classname": candidate.get("flower_classname"), "title": candidate.get("flower_title")},
    )
    collect_locations(memory, candidate, pack_id, quest, task)


def collect_generated_assets(memory: dict[str, Any], task_object: dict[str, Any], pack_id: str, quest: dict[str, Any], task: dict[str, Any]) -> None:
    ref = {
        "pack_id": pack_id,
        "classname_quests": quest.get("classname_quests"),
        "task_number": task.get("task_number"),
        "task_template_id": task.get("task_template_id"),
        "title": task_object.get("title"),
    }
    for field_name in ("classname", "param", "icon"):
        value = task_object.get(field_name)
        if isinstance(value, str) and quest.get("classname_quests"):
            prefix = str(quest["classname_quests"]).split("_Story_", 1)[0]
            if value.startswith(prefix):
                add_usage(memory, "used_generated_assets", value, {**ref, "field": field_name})


def parse_generated_asset_classname(value: Any) -> tuple[str, str, int] | None:
    if not isinstance(value, str):
        return None
    for kind in GENERATED_ASSET_KINDS:
        marker = f"_{kind}_"
        if marker not in value:
            continue
        prefix, number_text = value.rsplit(marker, 1)
        if prefix and number_text.isdigit():
            return prefix, kind, int(number_text)
    return None


def generated_sequence_offsets(
    memory: dict[str, Any] | None,
    current_pack_id: str | None = None,
) -> dict[tuple[str, str], int]:
    offsets: dict[tuple[str, str], int] = {}
    if not memory:
        return offsets

    used_generated_assets = memory.get("used_generated_assets") or {}
    if not isinstance(used_generated_assets, dict):
        return offsets

    for classname, data in used_generated_assets.items():
        if current_pack_id and isinstance(data, dict) and data.get("pack_id") == current_pack_id:
            continue
        parsed = parse_generated_asset_classname(classname)
        if parsed is None:
            continue
        prefix, kind, number = parsed
        key = (prefix, kind)
        offsets[key] = max(offsets.get(key, 0), number)
    return offsets


def generated_sequence_offsets_for_json(
    memory: dict[str, Any] | None,
    current_pack_id: str | None = None,
) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for (prefix, kind), number in generated_sequence_offsets(memory, current_pack_id).items():
        result.setdefault(prefix, {})[kind] = number
    return result


def update_memory_from_pack(
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
) -> dict[str, Any]:
    campaign = load_campaign(campaign_id, campaigns_dir)
    packs = campaign.get("packs") or []
    if isinstance(packs, list) and packs:
        return rebuild_memory_from_packs(campaign_id, campaigns_dir)
    return rebuild_memory_from_packs(campaign_id, campaigns_dir, pack_ids=[pack_id])


def rebuild_memory_from_packs(
    campaign_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    pack_ids: list[str] | None = None,
) -> dict[str, Any]:
    campaign = load_json_or_default(campaign_json_path(campaign_id, campaigns_dir), default_campaign(campaign_id))
    memory_path = campaign_memory_path(campaign_id, campaigns_dir)
    previous_memory = read_json(memory_path) if memory_path.exists() else None
    if pack_ids is None:
        pack_ids = [
            str(pack.get("pack_id"))
            for pack in campaign.get("packs", [])
            if isinstance(pack, dict) and pack.get("pack_id")
        ]
    if not pack_ids:
        pack_ids = [path.name for path in sorted(campaign_dir(campaign_id, campaigns_dir).glob("pack_*")) if path.is_dir()]

    memory = default_memory(campaign_id)
    memory["updated_at"] = now_iso()

    for pack_id in pack_ids:
        update_memory_from_single_pack(memory, campaign_id, pack_id, campaigns_dir)

    preserve_memory_timestamps(memory, previous_memory)
    save_memory(memory, campaigns_dir)
    render_campaign_summary(campaign_id, campaigns_dir)
    return memory


def update_memory_from_single_pack(
    memory: dict[str, Any],
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
) -> None:
    target = pack_dir(campaign_id, pack_id, campaigns_dir)
    filled_tasks_path = target / "filled_tasks.json"
    context_pack_path = target / "context_pack.json"
    quest_group_path = target / "quest_group.json"
    quest_group_validation_path = target / "quest_group.validation.json"
    interactive_objects_path = campaign_dir(campaign_id, campaigns_dir) / INTERACTIVE_OBJECTS_NAME
    if not filled_tasks_path.exists():
        raise FileNotFoundError(f"filled_tasks.json not found in pack: {filled_tasks_path}")
    if not context_pack_path.exists():
        raise FileNotFoundError(f"context_pack.json not found in pack: {context_pack_path}")

    filled_tasks = read_json(filled_tasks_path)
    context_pack = read_json(context_pack_path)
    context_index = context_task_index(context_pack)

    task_count = 0
    selected_count = 0
    for quest in filled_tasks.get("quests", []):
        classname = quest.get("classname_quests")
        helper = quest.get("helper") or quest.get("quest_helper") or quest.get("character_classname")
        if isinstance(helper, str) and classname:
            prefix = str(classname).split("_Story_", 1)[0]
            if helper.startswith(prefix):
                add_usage(
                    memory,
                    "used_generated_assets",
                    helper,
                    {
                        "pack_id": pack_id,
                        "classname_quests": classname,
                        "field": "helper",
                        "title": quest.get("character"),
                    },
                )
        for task in quest.get("tasks", []):
            task_count += 1
            template_id = task.get("task_template_id")
            add_usage(memory, "used_task_templates", template_id, {"pack_id": pack_id, "task_template_name": task.get("task_template_name")})
            task_object = task.get("task_object") if isinstance(task.get("task_object"), dict) else task
            collect_generated_assets(memory, task_object, pack_id, quest, task)
            context_task = context_index.get((str(classname), task.get("task_number")))
            candidate = candidate_by_id(context_task, task.get("selected_candidate_id"))
            if candidate:
                selected_count += 1
                collect_candidate_usage(memory, candidate, pack_id, quest, task)

    pack_memory = {
        "pack_id": pack_id,
        "updated_at": now_iso(),
        "filled_tasks": str(filled_tasks_path),
        "context_pack": str(context_pack_path),
        "tasks_found": task_count,
        "selected_candidates_found": selected_count,
    }
    if quest_group_path.exists():
        pack_memory["quest_group"] = str(quest_group_path)
    if quest_group_validation_path.exists():
        pack_memory["quest_group_validation"] = str(quest_group_validation_path)
    if interactive_objects_path.exists():
        pack_memory["interactive_objects"] = str(interactive_objects_path)
    memory.setdefault("packs", {})[pack_id] = pack_memory


def memory_count(memory: dict[str, Any], bucket: str) -> int:
    value = memory.get(bucket)
    if isinstance(value, dict):
        return len(value)
    if isinstance(value, list):
        return len(value)
    return 0


def first_keys(memory: dict[str, Any], bucket: str, limit: int = 12) -> list[str]:
    value = memory.get(bucket)
    if isinstance(value, dict):
        return list(value.keys())[:limit]
    if isinstance(value, list):
        return [str(item) for item in value[:limit]]
    return []


def render_campaign_summary(campaign_id: str, campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR) -> str:
    campaign = load_json_or_default(campaign_json_path(campaign_id, campaigns_dir), default_campaign(campaign_id))
    memory = load_json_or_default(campaign_memory_path(campaign_id, campaigns_dir), default_memory(campaign_id))
    lines = [
        f"# Campaign Summary: {campaign_id}",
        "",
        f"Title: {campaign.get('title') or ''}",
        f"Tone: {campaign.get('tone') or ''}",
        f"Status: {campaign.get('status') or ''}",
        f"Next pack number: {campaign.get('next_pack_number') or 1}",
        "",
        "## Characters",
        "",
    ]
    characters = campaign.get("characters") or []
    if characters:
        lines.extend(f"- {character}" for character in characters)
    else:
        lines.append("- Не заданы")

    lines.extend(
        [
            "",
            "## Packs",
            "",
        ]
    )
    packs = campaign.get("packs") or []
    if packs:
        for pack in packs:
            if isinstance(pack, dict):
                lines.append(f"- {pack.get('pack_id')}: {pack.get('title') or ''}")
    else:
        lines.append("- Паков пока нет")

    lines.extend(
        [
            "",
            "## Memory Counts",
            "",
            f"- used garbage: {memory_count(memory, 'used_garbage')}",
            f"- used collections: {memory_count(memory, 'used_collections')}",
            f"- used flowers: {memory_count(memory, 'used_flowers')}",
            f"- used locations: {memory_count(memory, 'used_locations')}",
            f"- used generated assets: {memory_count(memory, 'used_generated_assets')}",
            f"- used task templates: {memory_count(memory, 'used_task_templates')}",
            "",
            "## Recent Used Examples",
            "",
            f"- garbage: {', '.join(first_keys(memory, 'used_garbage')) or 'нет'}",
            f"- collections: {', '.join(first_keys(memory, 'used_collections')) or 'нет'}",
            f"- flowers: {', '.join(first_keys(memory, 'used_flowers')) or 'нет'}",
            f"- locations: {', '.join(first_keys(memory, 'used_locations')) or 'нет'}",
            "",
        ]
    )
    summary = "\n".join(lines)
    write_text(campaign_summary_path(campaign_id, campaigns_dir), summary)
    return summary


def memory_key_set(memory: dict[str, Any], bucket: str) -> set[str]:
    value = memory.get(bucket)
    if isinstance(value, dict):
        return {str(key) for key in value.keys()}
    if isinstance(value, list):
        return {str(item) for item in value}
    return set()


def campaign_memory_entity_sets(memory: dict[str, Any] | None) -> dict[str, set[str]]:
    memory = memory or {}
    return {
        "candidate_ids": memory_key_set(memory, "used_candidate_ids"),
        "garbage": memory_key_set(memory, "used_garbage"),
        "collections": memory_key_set(memory, "used_collections"),
        "flowers": memory_key_set(memory, "used_flowers"),
        "locations": memory_key_set(memory, "used_locations"),
    }


def candidate_is_used_by_campaign(candidate: dict[str, Any], memory_sets: dict[str, set[str]]) -> bool:
    if candidate.get("candidate_id") in memory_sets["candidate_ids"]:
        return True
    if candidate.get("garbage_classname") in memory_sets["garbage"]:
        return True
    if candidate.get("source_type") == "garbage" and candidate.get("source_classname") in memory_sets["garbage"]:
        return True
    if candidate.get("collection_classname") in memory_sets["collections"]:
        return True
    if candidate.get("flower_classname") in memory_sets["flowers"]:
        return True
    return False
