from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_entity_sets,
        campaign_memory_path as campaign_memory_path_for,
        candidate_is_used_by_campaign,
        generated_sequence_offsets_for_json,
    )
    from .workflow_context import DEFAULT_CONTEXT_PATH, load_context, stage_is_approved
except ImportError:
    from campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_entity_sets,
        campaign_memory_path as campaign_memory_path_for,
        candidate_is_used_by_campaign,
        generated_sequence_offsets_for_json,
    )
    from workflow_context import DEFAULT_CONTEXT_PATH, load_context, stage_is_approved


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "quest_plan.resolved.json"
DEFAULT_QUEST_READY_INDEX_PATH = PROJECT_ROOT / "data" / "quest_ready_index.json"
DEFAULT_QUEST_READY_DROPS_PATH = PROJECT_ROOT / "data" / "quest_ready_drops.index.json"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "context_pack.json"
DEFAULT_OUTPUT_PREVIEW_PATH = PROJECT_ROOT / "output" / "context_pack.preview.md"
DEFAULT_HISTORY_PATH = PROJECT_ROOT / "output" / "context_candidate_history.json"
DEFAULT_CANDIDATE_LIMIT = 12
REQUIRED_APPROVAL_STAGE = "3"
WORLD_LOCATION_TAG = "world"


STOPWORDS = {
    "для",
    "что",
    "это",
    "как",
    "его",
    "она",
    "они",
    "оно",
    "нам",
    "нас",
    "вам",
    "вас",
    "мне",
    "тебе",
    "теперь",
    "нужно",
    "надо",
    "можно",
    "будет",
    "быть",
    "если",
    "или",
    "при",
    "про",
    "уже",
    "все",
    "ещё",
    "еще",
    "дома",
    "гостях",
    "друга",
    "друзей",
}


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_json_or_default(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return read_json(path)


def normalize_text(value: Any) -> str:
    return str(value or "").lower().replace("ё", "е")


def text_tokens(*values: Any) -> set[str]:
    text = " ".join(normalize_text(value) for value in values)
    tokens = set(re.findall(r"[a-zа-я0-9_]{3,}", text, flags=re.IGNORECASE))
    return {token for token in tokens if token not in STOPWORDS}


def compact_locations(locations: list[dict[str, Any]], limit: int = 4) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    seen: set[str] = set()
    for location in locations:
        code = str(location.get("code") or "")
        title = location.get("title")
        key = code or str(title)
        if not key or key in seen:
            continue
        compact.append(
            {
                "code": location.get("code"),
                "title": title,
                "tags": location.get("tags") or [],
            }
        )
        seen.add(key)
        if len(compact) >= limit:
            break
    return compact


def location_has_tag(location: dict[str, Any], tag: str) -> bool:
    return tag.lower() in {str(item).lower() for item in location.get("tags") or []}


def has_world_location(locations: list[dict[str, Any]]) -> bool:
    return any(location_has_tag(location, WORLD_LOCATION_TAG) for location in locations)


def build_locations_by_garbage(locations: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    result: dict[str, list[dict[str, Any]]] = {}
    for location in locations.values():
        for garbage_classname in location.get("garbage_assets", []):
            result.setdefault(garbage_classname, []).append(
                {
                    "code": location.get("code"),
                    "title": location.get("title"),
                    "tags": location.get("tags") or [],
                }
            )
    return result


def candidate_id(domain: str, *parts: Any) -> str:
    safe_parts = [str(part) for part in parts if part not in (None, "")]
    return ":".join([domain, *safe_parts])


def make_garbage_candidates(quest_ready_index: dict[str, Any]) -> list[dict[str, Any]]:
    locations_by_garbage = build_locations_by_garbage(quest_ready_index.get("quest_ready_locations", {}))
    candidates: list[dict[str, Any]] = []
    for garbage in quest_ready_index.get("quest_ready_garbage", {}).values():
        classname = garbage.get("classname")
        title = garbage.get("title")
        all_locations = locations_by_garbage.get(classname, [])
        locations = compact_locations(all_locations)
        if not classname or not title or not locations:
            continue
        candidates.append(
            {
                "candidate_id": candidate_id("garbage", classname),
                "domain": "garbage",
                "garbage_classname": classname,
                "garbage_title": title,
                "garbage_id": garbage.get("id"),
                "locations": locations,
                "has_world_location": has_world_location(all_locations),
                "search_text": " ".join(
                    [
                        str(classname),
                        str(title),
                        " ".join(str(location.get("title") or "") for location in locations),
                        " ".join(" ".join(location.get("tags") or []) for location in locations),
                    ]
                ),
            }
        )
    return candidates


def make_flower_candidates(quest_ready_index: dict[str, Any]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for flower in quest_ready_index.get("quest_ready_flowers", {}).values():
        classname = flower.get("classname")
        title = flower.get("title")
        if not classname or not title:
            continue
        candidates.append(
            {
                "candidate_id": candidate_id("flower", classname),
                "domain": "flower",
                "flower_classname": classname,
                "flower_title": title,
                "flower_id": flower.get("id"),
                "flower_tags": flower.get("tags") or [],
                "req_user_level": flower.get("req_user_level"),
                "search_text": " ".join([str(classname), str(title), " ".join(flower.get("tags") or [])]),
            }
        )
    return candidates


def make_collection_drop_candidates(quest_ready_drops: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    for drop in quest_ready_drops:
        collection_classname = drop.get("collection_classname")
        source_classname = drop.get("source_classname")
        mode = drop.get("mode")
        if not collection_classname or not drop.get("collection_title") or not source_classname:
            continue
        key = candidate_id("collection_drop", collection_classname, source_classname, mode)
        if key in seen:
            continue
        seen.add(key)
        all_locations = drop.get("locations") or []
        locations = compact_locations(all_locations)
        candidates.append(
            {
                "candidate_id": key,
                "domain": "collection_drop",
                "collection_classname": collection_classname,
                "collection_title": drop.get("collection_title"),
                "collection_id": drop.get("collection_id"),
                "source_type": drop.get("source_type"),
                "source_classname": source_classname,
                "source_title": drop.get("source_title"),
                "mode": mode,
                "locations": locations,
                "has_world_location": has_world_location(all_locations),
                "search_text": " ".join(
                    [
                        str(collection_classname),
                        str(drop.get("collection_title")),
                        str(source_classname),
                        str(drop.get("source_title")),
                        str(mode),
                        " ".join(str(location.get("title") or "") for location in locations),
                        " ".join(" ".join(location.get("tags") or []) for location in locations),
                    ]
                ),
            }
        )
    return candidates


def make_gr_garbage_candidates(quest_ready_drops: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates_by_key: dict[str, dict[str, Any]] = {}
    for drop in quest_ready_drops:
        if drop.get("source_type") != "garbage":
            continue
        source_classname = drop.get("source_classname")
        source_title = drop.get("source_title")
        mode = drop.get("mode")
        all_locations = drop.get("locations") or []
        locations = compact_locations(all_locations)
        if not source_classname or not source_title or not locations:
            continue
        key = candidate_id("gr_garbage", source_classname, mode)
        candidate = candidates_by_key.setdefault(
            key,
            {
                "candidate_id": key,
                "domain": "gr_garbage",
                "garbage_classname": source_classname,
                "garbage_title": source_title,
                "mode": mode,
                "locations": locations,
                "has_world_location": has_world_location(all_locations),
                "example_drops": [],
                "search_text": " ".join(
                    [
                        str(source_classname),
                        str(source_title),
                        str(mode),
                        " ".join(str(location.get("title") or "") for location in locations),
                        " ".join(" ".join(location.get("tags") or []) for location in locations),
                    ]
                ),
            },
        )
        candidate["has_world_location"] = bool(candidate.get("has_world_location") or has_world_location(all_locations))
        if len(candidate["example_drops"]) < 3:
            candidate["example_drops"].append(
                {
                    "collection_classname": drop.get("collection_classname"),
                    "collection_title": drop.get("collection_title"),
                }
            )
            candidate["search_text"] += " " + str(drop.get("collection_title") or "")
    return list(candidates_by_key.values())


def build_candidate_pools(
    quest_ready_index: dict[str, Any],
    quest_ready_drops: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    return {
        "garbage": make_garbage_candidates(quest_ready_index),
        "flower": make_flower_candidates(quest_ready_index),
        "collection_drop": make_collection_drop_candidates(quest_ready_drops),
        "gr_garbage": make_gr_garbage_candidates(quest_ready_drops),
    }


def quest_context_tokens(quest: dict[str, Any]) -> set[str]:
    return text_tokens(
        quest.get("title_quest"),
        quest.get("description"),
        quest.get("congratulation"),
        quest.get("character"),
        quest.get("classname_quests"),
    )


def candidate_score(candidate: dict[str, Any], context_tokens: set[str], task: dict[str, Any]) -> int:
    candidate_tokens = text_tokens(candidate.get("search_text"))
    overlap = len(context_tokens & candidate_tokens)
    score = overlap * 10

    task_type = normalize_text(task.get("task_type"))
    mode = candidate.get("mode")
    if "in_guest" in task_type and mode == "guest":
        score += 5
    if "in_guest" not in task_type and mode == "home":
        score += 3

    if candidate.get("locations"):
        score += 2
    return score


def ordered_candidates(
    pool: list[dict[str, Any]],
    context_tokens: set[str],
    task: dict[str, Any],
    used_this_run: set[str],
    history_counts: dict[str, int],
    prefer_candidate_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    prefer_candidate_ids = prefer_candidate_ids or set()
    decorated: list[tuple[int, int, int, int, str, dict[str, Any]]] = []
    for candidate in pool:
        cid = candidate["candidate_id"]
        prefer_rank = 0 if cid in prefer_candidate_ids else 1
        history_count = history_counts.get(cid, 0)
        used_penalty = 1 if cid in used_this_run else 0
        score = candidate_score(candidate, context_tokens, task)
        decorated.append((prefer_rank, used_penalty, history_count, -score, cid, candidate))
    decorated.sort()
    return [candidate for *_prefix, candidate in decorated]


def select_candidates(
    pool: list[dict[str, Any]],
    context_tokens: set[str],
    task: dict[str, Any],
    used_this_run: set[str],
    history_counts: dict[str, int],
    limit: int,
    prefer_candidate_ids: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    selected = ordered_candidates(
        pool,
        context_tokens,
        task,
        used_this_run,
        history_counts,
        prefer_candidate_ids=prefer_candidate_ids,
    )[:limit]
    notes: list[str] = []
    if len(selected) < limit:
        notes.append(f"Only {len(selected)} candidates available for this task.")
    if any(candidate["candidate_id"] in used_this_run for candidate in selected):
        notes.append("Some candidates were repeated inside this context pack because fresh candidates were not enough.")
    if any(history_counts.get(candidate["candidate_id"], 0) > 0 for candidate in selected):
        notes.append("Some candidates were used in previous context packs because fresh candidates were not enough.")
    return selected, notes


def candidate_override_sets(manual_override: dict[str, Any]) -> tuple[set[str], set[str], str | None]:
    avoid = {str(item) for item in manual_override.get("avoid_candidates", []) if item}
    prefer = {str(item) for item in manual_override.get("prefer_candidates", []) if item}
    force = manual_override.get("force_candidate_id")
    return avoid, prefer, str(force) if force else None


def apply_manual_candidate_filters(
    pool: list[dict[str, Any]],
    manual_override: dict[str, Any],
) -> tuple[list[dict[str, Any]], set[str], list[str], list[dict[str, Any]]]:
    avoid_ids, prefer_ids, force_id = candidate_override_sets(manual_override)
    notes: list[str] = []
    issues: list[dict[str, Any]] = []
    filtered = list(pool)

    if avoid_ids:
        before = len(filtered)
        filtered = [candidate for candidate in filtered if candidate.get("candidate_id") not in avoid_ids]
        notes.append(f"Manual override excluded {before - len(filtered)} avoided candidates.")

    if force_id:
        forced = [candidate for candidate in filtered if candidate.get("candidate_id") == force_id]
        if forced:
            filtered = forced
            notes.append(f"Manual override forced candidate: {force_id}.")
        else:
            issues.append(
                {
                    "code": "forced_candidate_not_found",
                    "candidate_id": force_id,
                    "message": "Forced candidate was not found in the available pool after filters.",
                }
            )

    if prefer_ids:
        notes.append(f"Manual override prefers candidates: {', '.join(sorted(prefer_ids))}.")

    instruction = manual_override.get("instruction")
    if instruction:
        notes.append(f"Manual instruction: {instruction}")

    return filtered, prefer_ids, notes, issues


def apply_campaign_memory_filters(
    pool: list[dict[str, Any]],
    campaign_memory: dict[str, Any] | None,
    force_candidate_id: str | None = None,
    current_pack_id: str | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    if not campaign_memory or force_candidate_id:
        return pool, []

    memory_for_filters = campaign_memory
    if current_pack_id:
        memory_for_filters = dict(campaign_memory)
        for bucket in ("used_candidate_ids", "used_garbage", "used_collections", "used_flowers", "used_locations"):
            values = campaign_memory.get(bucket)
            if isinstance(values, dict):
                memory_for_filters[bucket] = {
                    key: value
                    for key, value in values.items()
                    if not (isinstance(value, dict) and value.get("pack_id") == current_pack_id)
                }
    memory_sets = campaign_memory_entity_sets(memory_for_filters)
    fresh = [candidate for candidate in pool if not candidate_is_used_by_campaign(candidate, memory_sets)]
    excluded = len(pool) - len(fresh)
    if excluded == 0:
        return pool, []
    if fresh:
        return fresh, [f"Campaign memory excluded {excluded} already used candidates."]
    return pool, [
        f"Campaign memory marks all {len(pool)} candidates as already used; reused candidates are shown because no fresh alternatives remain."
    ]


def domain_for_task(task: dict[str, Any]) -> str | None:
    task_template_id = task.get("resolved_template_id") or task.get("task_template_id")
    category = task.get("category") or ""
    task_type = normalize_text(task.get("task_type"))

    if task_template_id in {"TT-020", "TT-021", "TT-024", "TT-025", "TT-029", "TT-030"}:
        return "garbage"
    if task_template_id in {"TT-018", "TT-019", "TT-022", "TT-023", "TT-031", "TT-032"}:
        return "flower"
    if task_template_id in {"TT-011", "TT-026", "TT-027", "TT-028"}:
        return "collection_drop"
    if task_template_id in {"TT-013", "TT-014", "TT-015"}:
        return "gr_garbage"
    if task_template_id in {"TT-016", "TT-017"}:
        return "flower"

    if "collection" in task_type:
        return "collection_drop"
    if "flower" in task_type or "take_crop" in task_type or "flower" in category:
        return "flower"
    if "garbage" in task_type:
        if "gr" in task_type and "get_asset" in task_type:
            return "gr_garbage"
        return "garbage"
    return None


def is_guest_task(task: dict[str, Any]) -> bool:
    return "in_guest" in normalize_text(task.get("task_type"))


def candidate_is_world_garbage_related(candidate: dict[str, Any]) -> bool:
    if not candidate.get("has_world_location"):
        return False
    domain = candidate.get("domain")
    if domain in {"garbage", "gr_garbage"}:
        return True
    return domain == "collection_drop" and candidate.get("source_type") == "garbage"


def apply_guest_world_guardrail(
    pool: list[dict[str, Any]],
    task: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    if not is_guest_task(task):
        return pool, []

    filtered = [candidate for candidate in pool if not candidate_is_world_garbage_related(candidate)]
    excluded = len(pool) - len(filtered)
    if excluded == 0:
        return filtered, []
    return filtered, [
        f"Guest/world guardrail excluded {excluded} garbage or collection candidates tied to world locations."
    ]


def filtered_pool_for_task(domain: str, pools: dict[str, list[dict[str, Any]]], task: dict[str, Any]) -> list[dict[str, Any]]:
    pool = list(pools.get(domain, []))
    task_type = normalize_text(task.get("task_type"))
    if domain in {"collection_drop", "gr_garbage"}:
        if "in_guest" in task_type:
            guest_pool = [candidate for candidate in pool if candidate.get("mode") == "guest"]
            return guest_pool
        if "in_guest" not in task_type and "mystery" not in task_type and "is_silhouette" not in task_type:
            home_pool = [candidate for candidate in pool if candidate.get("mode") == "home"]
            return home_pool or pool
    return pool


def strip_search_text(candidate: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in candidate.items() if key != "search_text"}


def load_history(path: Path, reset: bool = False) -> dict[str, Any]:
    if reset:
        return {"version": 1, "candidate_counts": {}, "runs": []}
    return load_json_or_default(path, {"version": 1, "candidate_counts": {}, "runs": []})


def update_history(
    history: dict[str, Any],
    emitted_candidate_ids: list[str],
    input_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    counts = history.setdefault("candidate_counts", {})
    for cid in emitted_candidate_ids:
        counts[cid] = int(counts.get(cid, 0)) + 1

    history.setdefault("runs", []).append(
        {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "input": str(input_path),
            "output": str(output_path),
            "candidates_emitted": len(emitted_candidate_ids),
            "unique_candidates_emitted": len(set(emitted_candidate_ids)),
        }
    )
    return history


def build_context_pack(
    resolved_plan: dict[str, Any],
    quest_ready_index: dict[str, Any],
    quest_ready_drops: list[dict[str, Any]],
    history: dict[str, Any],
    candidate_limit: int,
    campaign_memory: dict[str, Any] | None = None,
    current_pack_id: str | None = None,
) -> tuple[dict[str, Any], list[str]]:
    pools = build_candidate_pools(quest_ready_index, quest_ready_drops)
    history_counts = {key: int(value) for key, value in history.get("candidate_counts", {}).items()}
    used_this_run: set[str] = set()
    emitted_candidate_ids: list[str] = []
    issues: list[dict[str, Any]] = []
    context_quests: list[dict[str, Any]] = []

    for quest_index, quest in enumerate(resolved_plan.get("quests", []), start=1):
        tokens = quest_context_tokens(quest)
        context_quest = {
            "classname_quests": quest.get("classname_quests"),
            "title_quest": quest.get("title_quest"),
            "quest_number": quest.get("quest_number"),
            "description": quest.get("description"),
            "congratulation": quest.get("congratulation"),
            "character": quest.get("character"),
            "tasks": [],
        }

        for task_index, task in enumerate(quest.get("tasks", []), start=1):
            domain = domain_for_task(task)
            manual_override = task.get("manual_override") or {}
            context_task = {
                "task_number": task.get("task_number"),
                "task_template_id": task.get("task_template_id"),
                "task_template_name": task.get("task_template_name"),
                "task_type": task.get("task_type"),
                "category": task.get("category"),
                "data_needs": task.get("data_needs") or [],
                "manual_override": manual_override,
                "candidate_domain": domain,
                "candidates": [],
                "notes": [],
            }

            if task.get("status") == "issue":
                context_task["notes"].append("Template resolver reported issues for this task.")
                issues.append(
                    {
                        "code": "task_has_template_issues",
                        "quest_index": quest_index,
                        "task_index": task_index,
                        "task_number": task.get("task_number"),
                        "task_template_id": task.get("task_template_id"),
                        "message": "Task has unresolved template issues; candidates may be incomplete.",
                    }
                )

            if domain is None:
                context_task["notes"].append("No real quest-ready candidates are needed for this generated/story template.")
            else:
                pool = filtered_pool_for_task(domain, pools, task)
                pool, prefer_ids, override_notes, override_issues = apply_manual_candidate_filters(pool, manual_override)
                context_task["notes"].extend(override_notes)
                pool, guest_world_notes = apply_guest_world_guardrail(pool, task)
                context_task["notes"].extend(guest_world_notes)
                _avoid_ids, _prefer_ids, force_id = candidate_override_sets(manual_override)
                pool, campaign_notes = apply_campaign_memory_filters(pool, campaign_memory, force_candidate_id=force_id, current_pack_id=current_pack_id)
                context_task["notes"].extend(campaign_notes)
                for issue in override_issues:
                    issues.append(
                        {
                            **issue,
                            "quest_index": quest_index,
                            "task_index": task_index,
                            "task_number": task.get("task_number"),
                            "task_template_id": task.get("task_template_id"),
                            "candidate_domain": domain,
                        }
                    )
                selected, notes = select_candidates(
                    pool,
                    tokens,
                    task,
                    used_this_run,
                    history_counts,
                    candidate_limit,
                    prefer_candidate_ids=prefer_ids,
                )
                context_task["candidates"] = [strip_search_text(candidate) for candidate in selected]
                context_task["notes"].extend(notes)
                for candidate in selected:
                    cid = candidate["candidate_id"]
                    used_this_run.add(cid)
                    emitted_candidate_ids.append(cid)
                if not selected:
                    issues.append(
                        {
                            "code": "no_candidates",
                            "quest_index": quest_index,
                            "task_index": task_index,
                            "task_number": task.get("task_number"),
                            "task_template_id": task.get("task_template_id"),
                            "candidate_domain": domain,
                            "message": "No quest-ready candidates found for this task.",
                        }
                    )

            context_quest["tasks"].append(context_task)
        context_quests.append(context_quest)

    generated_offsets = generated_sequence_offsets_for_json(campaign_memory, current_pack_id=current_pack_id)
    next_generated_numbers = {
        prefix: {kind: number + 1 for kind, number in kinds.items()}
        for prefix, kinds in generated_offsets.items()
    }

    context_pack = {
        "quests": context_quests,
        "issues": issues,
        "summary": {
            "quests_found": len(context_quests),
            "tasks_found": sum(len(quest["tasks"]) for quest in context_quests),
            "candidate_limit": candidate_limit,
            "candidates_emitted": len(emitted_candidate_ids),
            "unique_candidates_emitted": len(set(emitted_candidate_ids)),
            "issues": len(issues),
            "campaign_memory_used": campaign_memory is not None,
        },
        "candidate_pool_summary": {domain: len(pool) for domain, pool in pools.items()},
        "generated_sequence_offsets": generated_offsets,
        "next_generated_numbers": next_generated_numbers,
    }
    return context_pack, emitted_candidate_ids


def render_preview(context_pack: dict[str, Any]) -> str:
    lines = [
        "# Context Pack Preview",
        "",
        f"Quests found: {context_pack['summary']['quests_found']}",
        f"Tasks found: {context_pack['summary']['tasks_found']}",
        f"Candidate limit: {context_pack['summary']['candidate_limit']}",
        f"Candidates emitted: {context_pack['summary']['candidates_emitted']}",
        f"Unique candidates emitted: {context_pack['summary']['unique_candidates_emitted']}",
        f"Issues: {context_pack['summary']['issues']}",
        f"Campaign memory used: {'yes' if context_pack['summary'].get('campaign_memory_used') else 'no'}",
        "",
        "## Candidate Pools",
        "",
    ]
    for domain, count in context_pack.get("candidate_pool_summary", {}).items():
        lines.append(f"- {domain}: {count}")
    lines.append("")

    if context_pack.get("next_generated_numbers"):
        lines.extend(["## Next Generated Numbers", ""])
        for prefix, kinds in context_pack["next_generated_numbers"].items():
            parts = [f"{kind}_{number}" for kind, number in sorted(kinds.items())]
            lines.append(f"- `{prefix}`: {', '.join(parts)}")
        lines.append("")

    for quest in context_pack["quests"]:
        lines.extend(
            [
                f"## {quest.get('classname_quests') or 'Quest'} — {quest.get('title_quest') or ''}",
                "",
                f"Character: {quest.get('character') or ''}",
                "",
            ]
        )
        for task in quest.get("tasks", []):
            lines.extend(
                [
                    f"### Task {task.get('task_number')}: {task.get('task_template_id')} {task.get('task_template_name')}",
                    "",
                    f"- Task type: `{task.get('task_type')}`",
                    f"- Candidate domain: `{task.get('candidate_domain') or 'generated'}`",
                    f"- Candidates: {len(task.get('candidates', []))}",
                ]
            )
            for note in task.get("notes", []):
                lines.append(f"- Note: {note}")
            for candidate in task.get("candidates", [])[:5]:
                label = (
                    candidate.get("collection_title")
                    or candidate.get("garbage_title")
                    or candidate.get("flower_title")
                    or candidate.get("candidate_id")
                )
                lines.append(f"  - `{candidate.get('candidate_id')}`: {label}")
            lines.append("")

    if context_pack["issues"]:
        lines.extend(["## Issues", ""])
        for issue in context_pack["issues"]:
            lines.append(
                f"- `{issue['code']}` quest_index={issue.get('quest_index')} "
                f"task={issue.get('task_number')}: {issue['message']}"
            )
        lines.append("")

    return "\n".join(lines)


def build_context_pack_file(
    input_path: Path,
    quest_ready_index_path: Path,
    quest_ready_drops_path: Path,
    history_path: Path,
    output_json_path: Path,
    output_preview_path: Path,
    candidate_limit: int,
    reset_history: bool = False,
    campaign_memory_path: Path | None = None,
    current_pack_id: str | None = None,
) -> dict[str, Any]:
    history = load_history(history_path, reset=reset_history)
    campaign_memory = read_json(campaign_memory_path) if campaign_memory_path and campaign_memory_path.exists() else None
    context_pack, emitted_candidate_ids = build_context_pack(
        resolved_plan=read_json(input_path),
        quest_ready_index=read_json(quest_ready_index_path),
        quest_ready_drops=read_json(quest_ready_drops_path),
        history=history,
        candidate_limit=candidate_limit,
        campaign_memory=campaign_memory,
        current_pack_id=current_pack_id,
    )
    write_json(output_json_path, context_pack)
    output_preview_path.parent.mkdir(parents=True, exist_ok=True)
    output_preview_path.write_text(render_preview(context_pack), encoding="utf-8")
    updated_history = update_history(history, emitted_candidate_ids, input_path, output_json_path)
    write_json(history_path, updated_history)
    return context_pack


def stage3_approval_error(
    context_path: Path,
    campaign_id: str | None = None,
    pack_id: str | None = None,
) -> str | None:
    context = load_context(context_path)
    expected_campaign_id = campaign_id or context.get("campaign_id") or ""
    expected_pack_id = pack_id or context.get("pack_id") or ""
    if stage_is_approved(
        context,
        REQUIRED_APPROVAL_STAGE,
        campaign_id=expected_campaign_id,
        pack_id=expected_pack_id,
    ):
        return None

    approval = (context.get("stage_approvals") or {}).get(REQUIRED_APPROVAL_STAGE) or {}
    if approval.get("approved"):
        return (
            "stage 3 approval belongs to another campaign/pack: "
            f"{approval.get('campaign_id') or '-'} / {approval.get('pack_id') or '-'}"
        )
    return "stage 3 approval is missing"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build compact real-data context pack for stage 4 AI filling.")
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        default=DEFAULT_INPUT_PATH,
        help="Resolved quest plan JSON. Default: output/quest_plan.resolved.json",
    )
    parser.add_argument(
        "--quest-ready-index",
        type=Path,
        default=DEFAULT_QUEST_READY_INDEX_PATH,
        help="Quest-ready index JSON.",
    )
    parser.add_argument(
        "--quest-ready-drops",
        type=Path,
        default=DEFAULT_QUEST_READY_DROPS_PATH,
        help="Quest-ready drops JSON.",
    )
    parser.add_argument(
        "--history",
        type=Path,
        default=DEFAULT_HISTORY_PATH,
        help="Candidate usage history JSON.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=DEFAULT_OUTPUT_JSON_PATH,
        help="Output context pack JSON path.",
    )
    parser.add_argument(
        "--preview",
        type=Path,
        default=DEFAULT_OUTPUT_PREVIEW_PATH,
        help="Output human-readable preview path.",
    )
    parser.add_argument(
        "--candidate-limit",
        type=int,
        default=DEFAULT_CANDIDATE_LIMIT,
        help=f"Maximum candidates per real-data task. Default: {DEFAULT_CANDIDATE_LIMIT}",
    )
    parser.add_argument(
        "--reset-history",
        action="store_true",
        help="Ignore previous candidate history and start a new rotation.",
    )
    parser.add_argument(
        "--campaign",
        default="",
        help="Campaign id. If set, uses campaigns/<campaign_id>/campaign_memory.json to avoid already selected entities.",
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
    parser.add_argument(
        "--approval-context",
        type=Path,
        default=DEFAULT_CONTEXT_PATH,
        help="Active context JSON with recorded stage approvals.",
    )
    parser.add_argument(
        "--require-stage3-approval",
        action="store_true",
        help="Optional legacy guard: require recorded stage 3 approval before building context_pack.",
    )
    parser.add_argument(
        "--allow-unapproved-stage3",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)

    if args.candidate_limit < 1:
        print("--candidate-limit must be at least 1")
        return 1
    if not args.input.exists():
        print(f"input file not found: {args.input}")
        print("Сначала запусти: python src/task_type_resolver.py output/quest_plan.json")
        return 1

    campaign_memory_path = args.campaign_memory
    if campaign_memory_path is None and args.campaign:
        campaign_memory_path = campaign_memory_path_for(args.campaign, args.campaigns_dir)
    if campaign_memory_path is not None and not campaign_memory_path.exists():
        print(f"campaign memory file not found: {campaign_memory_path}")
        print("Сначала создай campaign: python src/start_campaign.py <campaign_id>")
        return 1

    if args.require_stage3_approval:
        approval_error = stage3_approval_error(
            args.approval_context,
            campaign_id=args.campaign or None,
            pack_id=args.current_pack or None,
        )
        if approval_error is not None:
            print(f"context_pack was not built: {approval_error}.")
            print("Сначала покажи пользователю результат этапа 3 и получи явный апрув в чате.")
            print(
                "Затем запиши апрув командой: "
                "python src/workflow_context.py approve --stage 3 "
                "--campaign <campaign_id> --pack <pack_id>"
            )
            return 1

    context_pack = build_context_pack_file(
        input_path=args.input,
        quest_ready_index_path=args.quest_ready_index,
        quest_ready_drops_path=args.quest_ready_drops,
        history_path=args.history,
        output_json_path=args.output_json,
        output_preview_path=args.preview,
        candidate_limit=args.candidate_limit,
        reset_history=args.reset_history,
        campaign_memory_path=campaign_memory_path,
        current_pack_id=args.current_pack or None,
    )
    print(f"quests found: {context_pack['summary']['quests_found']}")
    print(f"tasks found: {context_pack['summary']['tasks_found']}")
    print(f"candidate limit: {context_pack['summary']['candidate_limit']}")
    print(f"candidates emitted: {context_pack['summary']['candidates_emitted']}")
    print(f"unique candidates emitted: {context_pack['summary']['unique_candidates_emitted']}")
    print(f"issues: {context_pack['summary']['issues']}")
    print(f"json written: {args.output_json}")
    print(f"preview written: {args.preview}")
    print(f"history written: {args.history}")
    if campaign_memory_path is not None:
        print(f"campaign memory used: {campaign_memory_path}")
    return 0 if context_pack["summary"]["issues"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
