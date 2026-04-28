from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODES_PATH = PROJECT_ROOT / "workflows" / "workflow_modes.json"
DEFAULT_CONTEXT_PATH = PROJECT_ROOT / "workspace" / "active_context.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_text(value: str) -> str:
    value = value.lower().replace("ё", "е")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def load_modes(path: Path = DEFAULT_MODES_PATH) -> dict[str, Any]:
    data = read_json(path)
    modes = data.get("modes") or []
    data["modes_by_id"] = {mode["id"]: mode for mode in modes}
    return data


def default_context() -> dict[str, Any]:
    return {
        "version": 1,
        "mode": "",
        "mode_name_ru": "",
        "campaign_id": "",
        "pack_id": "",
        "stage": "",
        "quest_number": None,
        "task_number": None,
        "source": "default",
        "last_request": "",
        "matched_keywords": [],
        "notes": "",
        "stage_approvals": {},
        "updated_at": now_iso(),
    }


def load_context(path: Path = DEFAULT_CONTEXT_PATH) -> dict[str, Any]:
    if not path.exists():
        return default_context()
    context = read_json(path)
    context.setdefault("stage_approvals", {})
    return context


def approve_stage(
    context: dict[str, Any],
    stage: str,
    campaign_id: str | None = None,
    pack_id: str | None = None,
    notes: str = "",
) -> dict[str, Any]:
    stage = str(stage)
    updated = dict(context)
    approvals = dict(updated.get("stage_approvals") or {})
    approvals[stage] = {
        "approved": True,
        "approved_at": now_iso(),
        "campaign_id": campaign_id if campaign_id is not None else updated.get("campaign_id") or "",
        "pack_id": pack_id if pack_id is not None else updated.get("pack_id") or "",
        "notes": notes,
    }
    updated["stage_approvals"] = approvals
    updated["updated_at"] = now_iso()
    return updated


def stage_is_approved(
    context: dict[str, Any],
    stage: str,
    campaign_id: str | None = None,
    pack_id: str | None = None,
) -> bool:
    approval = (context.get("stage_approvals") or {}).get(str(stage)) or {}
    if not approval.get("approved"):
        return False
    if campaign_id is not None and approval.get("campaign_id") != campaign_id:
        return False
    if pack_id is not None and approval.get("pack_id") != pack_id:
        return False
    return True


def keyword_score(keyword: str) -> int:
    words = [word for word in keyword.split() if word]
    return max(1, len(words)) * 10 + len(keyword)


def detect_mode(text: str, modes_data: dict[str, Any] | None = None) -> dict[str, Any]:
    modes_data = modes_data or load_modes()
    normalized = normalize_text(text)
    results: list[dict[str, Any]] = []

    for mode in modes_data.get("modes", []):
        matched: list[str] = []
        score = 0
        for keyword in mode.get("keywords_ru", []):
            normalized_keyword = normalize_text(str(keyword))
            if normalized_keyword and normalized_keyword in normalized:
                matched.append(str(keyword))
                score += keyword_score(normalized_keyword)
        if score:
            results.append(
                {
                    "mode": mode["id"],
                    "mode_name_ru": mode.get("name_ru") or mode["id"],
                    "score": score,
                    "matched_keywords": matched,
                    "requires_context": mode.get("requires_context") or [],
                    "default_stage": mode.get("default_stage") or "",
                }
            )

    results.sort(key=lambda item: (-int(item["score"]), item["mode"]))
    if not results:
        return {
            "mode": "",
            "mode_name_ru": "",
            "score": 0,
            "matched_keywords": [],
            "requires_context": [],
            "default_stage": "",
            "alternatives": [],
        }

    best = dict(results[0])
    best["alternatives"] = results[1:4]
    return best


def context_with_mode(
    mode_id: str,
    modes_data: dict[str, Any],
    existing: dict[str, Any] | None = None,
    source: str = "manual",
    last_request: str = "",
    matched_keywords: list[str] | None = None,
    **updates: Any,
) -> dict[str, Any]:
    modes_by_id = modes_data["modes_by_id"]
    if mode_id not in modes_by_id:
        raise ValueError(f"unknown mode: {mode_id}")

    mode = modes_by_id[mode_id]
    context = dict(existing or default_context())
    context["version"] = 1
    context["mode"] = mode_id
    context["mode_name_ru"] = mode.get("name_ru") or mode_id
    context["source"] = source
    context["updated_at"] = now_iso()
    context["matched_keywords"] = matched_keywords or []
    if last_request:
        context["last_request"] = last_request

    if not context.get("stage") and mode.get("default_stage"):
        context["stage"] = mode.get("default_stage")

    for key, value in updates.items():
        if value is not None:
            context[key] = value
    return context


def set_context(args: argparse.Namespace) -> dict[str, Any]:
    modes_data = load_modes(args.modes)
    existing = load_context(args.context)
    context = context_with_mode(
        args.mode,
        modes_data,
        existing=existing,
        source="manual",
        campaign_id=args.campaign or existing.get("campaign_id") or "",
        pack_id=args.pack or existing.get("pack_id") or "",
        stage=args.stage if args.stage is not None else existing.get("stage") or "",
        quest_number=args.quest if args.quest is not None else existing.get("quest_number"),
        task_number=args.task if args.task is not None else existing.get("task_number"),
        notes=args.notes if args.notes is not None else existing.get("notes") or "",
    )
    write_json(args.context, context)
    return context


def detect_context(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any] | None]:
    modes_data = load_modes(args.modes)
    detection = detect_mode(args.text, modes_data)
    applied_context = None
    if args.apply:
        if not detection["mode"]:
            raise ValueError("mode was not detected; active context was not changed.")
        existing = load_context(args.context)
        applied_context = context_with_mode(
            detection["mode"],
            modes_data,
            existing=existing,
            source="detected",
            last_request=args.text,
            matched_keywords=detection["matched_keywords"],
            campaign_id=args.campaign or existing.get("campaign_id") or "",
            pack_id=args.pack or existing.get("pack_id") or "",
            stage=args.stage if args.stage is not None else detection.get("default_stage") or existing.get("stage") or "",
            quest_number=args.quest if args.quest is not None else existing.get("quest_number"),
            task_number=args.task if args.task is not None else existing.get("task_number"),
        )
        write_json(args.context, applied_context)
    return detection, applied_context


def approve_context(args: argparse.Namespace) -> dict[str, Any]:
    existing = load_context(args.context)
    context = approve_stage(
        existing,
        str(args.stage),
        campaign_id=args.campaign or existing.get("campaign_id") or "",
        pack_id=args.pack or existing.get("pack_id") or "",
        notes=args.notes or "",
    )
    write_json(args.context, context)
    return context


def print_context(context: dict[str, Any]) -> None:
    print(f"mode: {context.get('mode') or ''}")
    print(f"mode name: {context.get('mode_name_ru') or ''}")
    print(f"campaign id: {context.get('campaign_id') or ''}")
    print(f"pack id: {context.get('pack_id') or ''}")
    print(f"stage: {context.get('stage') or ''}")
    print(f"quest number: {context.get('quest_number') or ''}")
    print(f"task number: {context.get('task_number') or ''}")
    print(f"source: {context.get('source') or ''}")
    print(f"updated at: {context.get('updated_at') or ''}")
    if context.get("last_request"):
        print(f"last request: {context['last_request']}")
    if context.get("matched_keywords"):
        print(f"matched keywords: {', '.join(context['matched_keywords'])}")
    if context.get("notes"):
        print(f"notes: {context['notes']}")
    approvals = context.get("stage_approvals") or {}
    approved_stages = [
        str(stage)
        for stage, approval in sorted(approvals.items())
        if isinstance(approval, dict) and approval.get("approved")
    ]
    if approved_stages:
        print(f"approved stages: {', '.join(approved_stages)}")


def print_modes(modes_data: dict[str, Any]) -> None:
    for mode in modes_data.get("modes", []):
        print(f"{mode['id']}: {mode.get('name_ru') or ''}")
        print(f"  {mode.get('description_ru') or ''}")
        print(f"  keywords: {', '.join(mode.get('keywords_ru', [])[:8])}")
        print("")


def print_detection(detection: dict[str, Any]) -> None:
    if not detection.get("mode"):
        print("mode: not detected")
        return
    print(f"mode: {detection['mode']}")
    print(f"mode name: {detection.get('mode_name_ru') or ''}")
    print(f"score: {detection.get('score')}")
    print(f"matched keywords: {', '.join(detection.get('matched_keywords') or [])}")
    requires = detection.get("requires_context") or []
    if requires:
        print(f"requires context: {', '.join(requires)}")
    alternatives = detection.get("alternatives") or []
    if alternatives:
        print("alternatives:")
        for item in alternatives:
            print(f"  - {item['mode']} ({item['score']}): {', '.join(item.get('matched_keywords') or [])}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage workflow modes and active project context.")
    parser.add_argument("--modes", type=Path, default=DEFAULT_MODES_PATH)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show", help="Show active context.")
    subparsers.add_parser("list-modes", help="List workflow modes and Russian keywords.")

    set_parser = subparsers.add_parser("set", help="Set active context manually.")
    set_parser.add_argument("--mode", required=True)
    set_parser.add_argument("--campaign", default="")
    set_parser.add_argument("--pack", default="")
    set_parser.add_argument("--stage", default=None)
    set_parser.add_argument("--quest", type=int, default=None)
    set_parser.add_argument("--task", type=int, default=None)
    set_parser.add_argument("--notes", default=None)

    detect_parser = subparsers.add_parser("detect", help="Detect workflow mode from Russian request text.")
    detect_parser.add_argument("--text", required=True)
    detect_parser.add_argument("--apply", action="store_true", help="Save detected mode to active context.")
    detect_parser.add_argument("--campaign", default="")
    detect_parser.add_argument("--pack", default="")
    detect_parser.add_argument("--stage", default=None)
    detect_parser.add_argument("--quest", type=int, default=None)
    detect_parser.add_argument("--task", type=int, default=None)

    approve_parser = subparsers.add_parser("approve", help="Record a human approval for a workflow stage.")
    approve_parser.add_argument("--stage", required=True, help="Approved stage number, for example 3.")
    approve_parser.add_argument("--campaign", default="")
    approve_parser.add_argument("--pack", default="")
    approve_parser.add_argument("--notes", default="")

    subparsers.add_parser("clear", help="Reset active context.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "show":
            print_context(load_context(args.context))
            return 0
        if args.command == "list-modes":
            print_modes(load_modes(args.modes))
            return 0
        if args.command == "set":
            context = set_context(args)
            print_context(context)
            print(f"context written: {args.context}")
            return 0
        if args.command == "detect":
            detection, applied_context = detect_context(args)
            print_detection(detection)
            if applied_context is not None:
                print(f"context written: {args.context}")
            return 0 if detection.get("mode") else 2
        if args.command == "approve":
            context = approve_context(args)
            print_context(context)
            print(f"stage approved: {args.stage}")
            print(f"context written: {args.context}")
            return 0
        if args.command == "clear":
            context = default_context()
            context["source"] = "cleared"
            write_json(args.context, context)
            print_context(context)
            print(f"context written: {args.context}")
            return 0
    except (OSError, ValueError) as exc:
        print(str(exc))
        return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
