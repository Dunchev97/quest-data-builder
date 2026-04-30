from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from . import build_context_pack as context_pack_builder
    from . import build_filled_tasks as filled_tasks_builder
    from . import build_quest_group as quest_group_builder
    from . import build_resource_table as resource_table_builder
    from . import export_csv
    from . import parse_stage3
    from . import task_type_resolver
    from . import validate_task_objects
    from .campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_path,
        pack_dir,
        update_memory_from_pack,
    )
    from .workflow_context import DEFAULT_CONTEXT_PATH, approve_stage, load_context, write_json
except ImportError:
    import build_context_pack as context_pack_builder
    import build_filled_tasks as filled_tasks_builder
    import build_quest_group as quest_group_builder
    import build_resource_table as resource_table_builder
    import export_csv
    import parse_stage3
    import task_type_resolver
    import validate_task_objects
    from campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_path,
        pack_dir,
        update_memory_from_pack,
    )
    from workflow_context import DEFAULT_CONTEXT_PATH, approve_stage, load_context, write_json


STAGE3_TEXT = "stage3_quests.txt"
QUEST_PLAN = "quest_plan.json"
QUEST_PLAN_PREVIEW = "quest_plan.preview.md"
QUEST_PLAN_RESOLVED = "quest_plan.resolved.json"
QUEST_PLAN_RESOLVED_PREVIEW = "quest_plan.resolved.preview.md"
CONTEXT_HISTORY = "context_candidate_history.json"
CONTEXT_PACK = "context_pack.json"
CONTEXT_PACK_PREVIEW = "context_pack.preview.md"
TASK_CHOICES = "task_choices.json"
FILLED_TASKS_BUILD = "filled_tasks.build.json"
FILLED_TASKS = "filled_tasks.json"
FILLED_TASKS_VALIDATION = "filled_tasks.validation.json"
FILLED_TASKS_PREVIEW = "filled_tasks.preview.md"
QUEST_GROUP = "quest_group.json"
QUEST_GROUP_CHOICES = "quest_group_choices.json"
QUEST_GROUP_VALIDATION = "quest_group.validation.json"
QUEST_GROUP_PREVIEW = "quest_group.preview.md"
GENERATED_QUESTS = "generated_quests.csv"


def pack_artifact(campaign_id: str, pack_id: str, filename: str, campaigns_dir: Path) -> Path:
    return pack_dir(campaign_id, pack_id, campaigns_dir) / filename


def resolve_ids(args: argparse.Namespace, require_pack: bool = True) -> tuple[str, str]:
    context = load_context(args.context)
    campaign_id = args.campaign or str(context.get("campaign_id") or "")
    pack_id = getattr(args, "pack", "") or str(context.get("pack_id") or "")
    if not campaign_id:
        raise ValueError("campaign_id is required. Pass --campaign or set active_context.")
    if require_pack and not pack_id:
        raise ValueError("pack_id is required. Pass --pack or set active_context.")
    return campaign_id, pack_id


def existing_campaign_memory(campaign_id: str, campaigns_dir: Path) -> Path:
    path = campaign_memory_path(campaign_id, campaigns_dir)
    if not path.exists():
        raise FileNotFoundError(f"campaign memory file not found: {path}")
    return path


def run_stage3(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    stage3_path = pack_artifact(campaign_id, pack_id, STAGE3_TEXT, args.campaigns_dir)
    quest_plan_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN, args.campaigns_dir)
    quest_plan_preview_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN_PREVIEW, args.campaigns_dir)
    resolved_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN_RESOLVED, args.campaigns_dir)
    resolved_preview_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN_RESOLVED_PREVIEW, args.campaigns_dir)

    if not stage3_path.exists():
        print(f"stage3 file not found: {stage3_path}")
        return 1

    quest_plan = parse_stage3.parse_file(stage3_path, quest_plan_path, quest_plan_preview_path)
    print(f"stage 3 parsed: quests={quest_plan['summary']['quests_found']} tasks={quest_plan['summary']['tasks_found']}")
    print(f"json written: {quest_plan_path}")
    print(f"preview written: {quest_plan_preview_path}")
    if quest_plan["summary"]["issues"]:
        print(f"stage 3 parse issues: {quest_plan['summary']['issues']}")
        return 2

    resolved_plan = task_type_resolver.resolve_file(
        quest_plan_path,
        task_type_resolver.DEFAULT_TEMPLATES_PATH,
        resolved_path,
        resolved_preview_path,
    )
    print(f"stage 3 resolved: issues={resolved_plan['summary']['issues']}")
    print(f"json written: {resolved_path}")
    print(f"preview written: {resolved_preview_path}")
    return 0 if resolved_plan["summary"]["issues"] == 0 else 2


def run_context(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    approval_error = context_pack_builder.stage3_approval_error(args.context, campaign_id, pack_id)
    if approval_error is not None and args.require_stage3_approval:
        print(f"context_pack was not built: {approval_error}.")
        print("Approve stage 3 first.")
        return 1

    memory_path = existing_campaign_memory(campaign_id, args.campaigns_dir)
    context_pack = context_pack_builder.build_context_pack_file(
        input_path=pack_artifact(campaign_id, pack_id, QUEST_PLAN_RESOLVED, args.campaigns_dir),
        quest_ready_index_path=context_pack_builder.DEFAULT_QUEST_READY_INDEX_PATH,
        quest_ready_drops_path=context_pack_builder.DEFAULT_QUEST_READY_DROPS_PATH,
        history_path=pack_artifact(campaign_id, pack_id, CONTEXT_HISTORY, args.campaigns_dir),
        output_json_path=pack_artifact(campaign_id, pack_id, CONTEXT_PACK, args.campaigns_dir),
        output_preview_path=pack_artifact(campaign_id, pack_id, CONTEXT_PACK_PREVIEW, args.campaigns_dir),
        candidate_limit=args.candidate_limit,
        reset_history=args.reset_history,
        campaign_memory_path=memory_path,
        current_pack_id=pack_id,
    )
    summary = context_pack["summary"]
    print(f"context pack built: quests={summary['quests_found']} tasks={summary['tasks_found']} candidates={summary['candidates_emitted']}")
    print(f"issues: {summary['issues']}")
    print(f"json written: {pack_artifact(campaign_id, pack_id, CONTEXT_PACK, args.campaigns_dir)}")
    return 0 if summary["issues"] == 0 else 2


def run_fill(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    context_pack_path = pack_artifact(campaign_id, pack_id, CONTEXT_PACK, args.campaigns_dir)
    choices_path = pack_artifact(campaign_id, pack_id, TASK_CHOICES, args.campaigns_dir)
    output_path = pack_artifact(campaign_id, pack_id, FILLED_TASKS, args.campaigns_dir)
    build_path = pack_artifact(campaign_id, pack_id, FILLED_TASKS_BUILD, args.campaigns_dir)

    result = filled_tasks_builder.build_filled_tasks_file(
        context_pack_path=context_pack_path,
        choices_path=choices_path,
        output_json_path=output_path,
        build_json_path=build_path,
    )
    summary = result["summary"]
    print(f"stage 4 filled: quests={summary['quests_found']} tasks={summary['tasks_found']} issues={summary['issues']}")
    print(f"json written: {output_path}")
    print(f"build summary written: {build_path}")
    if summary["issues"]:
        return 2
    return run_validate(args)


def run_validate(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    validation = validate_task_objects.validate_file(
        input_path=pack_artifact(campaign_id, pack_id, FILLED_TASKS, args.campaigns_dir),
        context_pack_path=pack_artifact(campaign_id, pack_id, CONTEXT_PACK, args.campaigns_dir),
        templates_path=validate_task_objects.DEFAULT_TEMPLATES_PATH,
        output_json_path=pack_artifact(campaign_id, pack_id, FILLED_TASKS_VALIDATION, args.campaigns_dir),
        preview_path=pack_artifact(campaign_id, pack_id, FILLED_TASKS_PREVIEW, args.campaigns_dir),
        campaign_memory_path=existing_campaign_memory(campaign_id, args.campaigns_dir),
        current_pack_id=pack_id,
    )
    summary = validation["summary"]
    print(f"stage 4 validation: tasks={summary['tasks_found']} errors={summary['errors']} warnings={summary['warnings']}")
    print(f"json written: {pack_artifact(campaign_id, pack_id, FILLED_TASKS_VALIDATION, args.campaigns_dir)}")
    print(f"preview written: {pack_artifact(campaign_id, pack_id, FILLED_TASKS_PREVIEW, args.campaigns_dir)}")
    return 0 if summary["errors"] == 0 else 2


def run_quest_group(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    approval_error = quest_group_builder.stage4_approval_error(args.context, campaign_id, pack_id)
    if approval_error is not None and not args.allow_unapproved:
        print(f"quest_group was not built: {approval_error}.")
        print("Approve stage 4 first.")
        return 1

    texts = {
        "title": args.title,
        "description": args.description,
        "description_complete": args.description_complete,
        "description_spoil": args.description_spoil,
        "output_classname": args.output_classname,
    }
    if not all(texts[field] for field in ("title", "description", "description_complete", "description_spoil")):
        choices_path = pack_artifact(campaign_id, pack_id, QUEST_GROUP_CHOICES, args.campaigns_dir)
        if not choices_path.exists():
            print(f"quest group choices not found: {choices_path}")
            print("Create quest_group_choices.json or pass --title/--description/--description-complete/--description-spoil.")
            return 1
        file_texts = quest_group_builder.read_quest_group_choices(choices_path)
        texts = {field: texts[field] or file_texts[field] for field in texts}
    missing = [field for field in ("title", "description", "description_complete", "description_spoil") if not texts[field]]
    if missing:
        print(f"quest_group text fields are missing: {', '.join(missing)}")
        return 1

    quest_group, validation = quest_group_builder.build_quest_group_file(
        input_path=pack_artifact(campaign_id, pack_id, FILLED_TASKS, args.campaigns_dir),
        output_json_path=pack_artifact(campaign_id, pack_id, QUEST_GROUP, args.campaigns_dir),
        validation_path=pack_artifact(campaign_id, pack_id, QUEST_GROUP_VALIDATION, args.campaigns_dir),
        preview_path=pack_artifact(campaign_id, pack_id, QUEST_GROUP_PREVIEW, args.campaigns_dir),
        title=texts["title"],
        description=texts["description"],
        description_complete=texts["description_complete"],
        description_spoil=texts["description_spoil"],
        output_classname=texts["output_classname"] or None,
        campaign_id=campaign_id,
        pack_id=pack_id,
    )
    summary = validation["summary"]
    print(f"quest group built: output={quest_group['output']}")
    print(f"errors: {summary['errors']} warnings: {summary['warnings']}")
    print(f"json written: {pack_artifact(campaign_id, pack_id, QUEST_GROUP, args.campaigns_dir)}")
    return 0 if summary["errors"] == 0 else 2


def run_stage6(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    input_path = pack_artifact(campaign_id, pack_id, FILLED_TASKS, args.campaigns_dir)
    validation_path = pack_artifact(campaign_id, pack_id, FILLED_TASKS_VALIDATION, args.campaigns_dir)
    quest_group_path = pack_artifact(campaign_id, pack_id, QUEST_GROUP, args.campaigns_dir)
    quest_group_validation_path = pack_artifact(campaign_id, pack_id, QUEST_GROUP_VALIDATION, args.campaigns_dir)
    output_csv_path = pack_artifact(campaign_id, pack_id, GENERATED_QUESTS, args.campaigns_dir)

    approval_error = export_csv.stage5_approval_error(args.context, campaign_id, pack_id)
    if approval_error is not None and not args.allow_unapproved:
        print(f"CSV was not created: {approval_error}.")
        print("Approve stage 5 first.")
        return 1

    try:
        export_csv.ensure_validation_passed(input_path, validation_path, args.allow_stale_validation)
        export_csv.ensure_quest_group_validation_passed(
            quest_group_path,
            quest_group_validation_path,
            allow_stale=args.allow_stale_validation,
        )
        summary = export_csv.export_filled_tasks_to_csv(
            export_csv.read_json(input_path),
            output_csv_path,
            quest_group=export_csv.read_json(quest_group_path),
        )
        memory = update_memory_from_pack(campaign_id, pack_id, args.campaigns_dir)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 2

    print(f"csv written: {output_csv_path}")
    print(f"rows written: {summary['rows_written']}")
    print(f"memory updated: used_garbage={len(memory.get('used_garbage', {}))} used_flowers={len(memory.get('used_flowers', {}))}")
    return 0


def run_resource_table(args: argparse.Namespace) -> int:
    campaign_id, _ = resolve_ids(args, require_pack=False)
    output_csv = args.output_csv or args.campaigns_dir / campaign_id / "resource_table.csv"
    summary_json = args.summary_json or args.campaigns_dir / campaign_id / "resource_table.summary.json"
    rows, summary = resource_table_builder.build_resource_table(campaign_id, campaigns_dir=args.campaigns_dir, pack_ids=args.pack_filter)
    try:
        resource_table_builder.write_csv(output_csv, rows)
        resource_table_builder.write_json(summary_json, summary)
    except PermissionError as exc:
        print(f"could not write resource table: {output_csv}")
        print("Close the file in Excel/Sheets sync or pass --output-csv to write another copy.")
        print(str(exc))
        return 3
    print(f"resource table written: {output_csv}")
    print(f"summary written: {summary_json}")
    print(f"blocks: {len(summary['blocks'])} warnings: {len(summary['warnings'])}")
    return 0 if not summary["warnings"] else 2


def run_approve(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    context = approve_stage(load_context(args.context), args.stage, campaign_id=campaign_id, pack_id=pack_id, notes=args.notes)
    write_json(args.context, context)
    print(f"stage approved: {args.stage}")
    print(f"context written: {args.context}")
    return 0


def run_status(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    files = [
        STAGE3_TEXT,
        QUEST_PLAN_RESOLVED,
        CONTEXT_PACK,
        TASK_CHOICES,
        FILLED_TASKS_BUILD,
        FILLED_TASKS,
        FILLED_TASKS_VALIDATION,
        QUEST_GROUP_CHOICES,
        QUEST_GROUP,
        QUEST_GROUP_VALIDATION,
        GENERATED_QUESTS,
    ]
    print(f"campaign: {campaign_id}")
    print(f"pack: {pack_id}")
    for filename in files:
        path = pack_artifact(campaign_id, pack_id, filename, args.campaigns_dir)
        print(f"{filename}: {'ok' if path.exists() else 'missing'}")
    return 0


def add_pack_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--campaign", default="", help="Campaign id. Defaults to active_context.")
    parser.add_argument("--pack", default="", help="Pack id. Defaults to active_context.")
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT_PATH)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Fast wrappers for common quest workflow steps.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    stage3_parser = subparsers.add_parser("stage3", help="Parse stage3_quests.txt and resolve task templates.")
    add_pack_options(stage3_parser)
    stage3_parser.set_defaults(func=run_stage3)

    context_parser = subparsers.add_parser("context", help="Build stage 3.1 context_pack.")
    add_pack_options(context_parser)
    context_parser.add_argument("--candidate-limit", type=int, default=context_pack_builder.DEFAULT_CANDIDATE_LIMIT)
    context_parser.add_argument("--reset-history", action="store_true")
    context_parser.add_argument("--require-stage3-approval", action="store_true")
    context_parser.set_defaults(func=run_context)

    fill_parser = subparsers.add_parser("fill", help="Build strict stage 4 filled_tasks.json from task_choices.json and validate it.")
    add_pack_options(fill_parser)
    fill_parser.set_defaults(func=run_fill)

    validate_parser = subparsers.add_parser("validate", help="Validate stage 4 filled_tasks.json.")
    add_pack_options(validate_parser)
    validate_parser.set_defaults(func=run_validate)

    quest_group_parser = subparsers.add_parser("quest-group", help="Build stage 5 quest_group.json.")
    add_pack_options(quest_group_parser)
    quest_group_parser.add_argument("--title", default="")
    quest_group_parser.add_argument("--description", default="")
    quest_group_parser.add_argument("--description-complete", default="")
    quest_group_parser.add_argument("--description-spoil", default="")
    quest_group_parser.add_argument("--output-classname", default="")
    quest_group_parser.add_argument("--allow-unapproved", action="store_true")
    quest_group_parser.set_defaults(func=run_quest_group)

    stage6_parser = subparsers.add_parser("stage6", help="Export CSV and update campaign memory.")
    add_pack_options(stage6_parser)
    stage6_parser.add_argument("--allow-stale-validation", action="store_true")
    stage6_parser.add_argument("--allow-unapproved", action="store_true")
    stage6_parser.set_defaults(func=run_stage6)

    resource_table_parser = subparsers.add_parser("resource-table", help="Build campaign resource_table.csv.")
    resource_table_parser.add_argument("--campaign", default="", help="Campaign id. Defaults to active_context.")
    resource_table_parser.add_argument("--pack-filter", action="append", default=None, help="Optional pack filter. Repeatable.")
    resource_table_parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    resource_table_parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT_PATH)
    resource_table_parser.add_argument("--output-csv", type=Path, default=None)
    resource_table_parser.add_argument("--summary-json", type=Path, default=None)
    resource_table_parser.set_defaults(func=run_resource_table)

    approve_parser = subparsers.add_parser("approve", help="Approve a workflow stage in active_context.")
    add_pack_options(approve_parser)
    approve_parser.add_argument("--stage", required=True)
    approve_parser.add_argument("--notes", default="")
    approve_parser.set_defaults(func=run_approve)

    status_parser = subparsers.add_parser("status", help="Show pack artifact status.")
    add_pack_options(status_parser)
    status_parser.set_defaults(func=run_status)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (FileNotFoundError, OSError, ValueError) as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
