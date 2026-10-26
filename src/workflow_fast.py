from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from . import build_actions_table as actions_table_builder
    from . import build_context_pack as context_pack_builder
    from . import build_filled_tasks as filled_tasks_builder
    from . import build_quest_group as quest_group_builder
    from . import build_resource_table as resource_table_builder
    from . import export_csv
    from . import export_xlsx
    from . import interactive_objects as interactive_objects_builder
    from . import parse_stage3
    from . import review_docs
    from . import task_type_resolver
    from . import validate_task_objects
    from .campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_path,
        pack_dir,
        update_memory_from_pack,
    )
    from .workflow_context import DEFAULT_CONTEXT_PATH, approve_stage, file_sha256, load_context, stage_approval_error, write_json
except ImportError:
    import build_actions_table as actions_table_builder
    import build_context_pack as context_pack_builder
    import build_filled_tasks as filled_tasks_builder
    import build_quest_group as quest_group_builder
    import build_resource_table as resource_table_builder
    import export_csv
    import export_xlsx
    import interactive_objects as interactive_objects_builder
    import parse_stage3
    import review_docs
    import task_type_resolver
    import validate_task_objects
    from campaigns import (
        DEFAULT_CAMPAIGNS_DIR,
        campaign_memory_path,
        pack_dir,
        update_memory_from_pack,
    )
    from workflow_context import DEFAULT_CONTEXT_PATH, approve_stage, file_sha256, load_context, stage_approval_error, write_json


STAGE3_TEXT = "stage3_quests.txt"
STAGE2_TEXT = "stage2_story.txt"
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
GENERATED_ACTIONS = "generated_actions.csv"
GENERATED_ACTIONS_SUMMARY = "generated_actions.summary.json"
RESOURCE_TABLE = "resource_table.csv"
RESOURCE_TABLE_SUMMARY = "resource_table.summary.json"
STAGE6_REVIEW_XLSX = "review/stage6_review.xlsx"
INTERACTIVE_OBJECTS = "interactive_objects.json"
INTERACTIVE_OBJECTS_PREVIEW = "interactive_objects.preview.md"
GENERATED_INTERACTIVE_OBJECTS_SUMMARY = "generated_interactive_objects.summary.json"
REVIEW_DIR = "review"


def pack_artifact(campaign_id: str, pack_id: str, filename: str, campaigns_dir: Path) -> Path:
    return pack_dir(campaign_id, pack_id, campaigns_dir) / filename


def ensure_stage_review(campaign_id: str, pack_id: str, stage: str, campaigns_dir: Path) -> Path:
    path = review_docs.review_path(campaign_id, pack_id, stage, campaigns_dir)
    existed = path.exists() and path.stat().st_size > 0
    review_docs.write_review_doc(campaign_id, pack_id, stage, campaigns_dir, overwrite=False)
    action = "preserved" if existed else "written"
    print(f"stage {stage} review {action}: {path}")
    return path


def outputs_are_fresh(outputs: list[Path], inputs: list[Path]) -> bool:
    existing_outputs = [path for path in outputs if path.exists()]
    existing_inputs = [path for path in inputs if path.exists()]
    if len(existing_outputs) != len(outputs) or not existing_inputs:
        return False
    oldest_output = min(path.stat().st_mtime for path in existing_outputs)
    newest_input = max(path.stat().st_mtime for path in existing_inputs)
    return oldest_output >= newest_input


def campaign_pack_dirs(campaign_id: str, campaigns_dir: Path) -> list[Path]:
    campaign_dir = campaigns_dir / campaign_id
    return sorted(path for path in campaign_dir.glob("pack_*") if path.is_dir())


def resource_table_inputs(campaign_id: str, campaigns_dir: Path) -> list[Path]:
    campaign_dir = campaigns_dir / campaign_id
    inputs = [campaign_dir / INTERACTIVE_OBJECTS]
    for current_pack_dir in campaign_pack_dirs(campaign_id, campaigns_dir):
        inputs.extend(
            [
                current_pack_dir / FILLED_TASKS,
                current_pack_dir / CONTEXT_PACK,
                current_pack_dir / INTERACTIVE_OBJECTS,
            ]
        )
    return inputs


def generated_interactive_outputs(campaign_id: str, campaigns_dir: Path) -> list[Path]:
    campaign_dir = campaigns_dir / campaign_id
    return list(campaign_dir.glob("generated_interactive_objects_*.csv"))


def stage6_legacy_csv_outputs(campaign_id: str, pack_id: str, campaigns_dir: Path) -> list[Path]:
    return [
        pack_artifact(campaign_id, pack_id, GENERATED_QUESTS, campaigns_dir),
        pack_artifact(campaign_id, pack_id, GENERATED_ACTIONS, campaigns_dir),
        campaigns_dir / campaign_id / RESOURCE_TABLE,
        *generated_interactive_outputs(campaign_id, campaigns_dir),
    ]


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
    stage2_path = pack_artifact(campaign_id, pack_id, STAGE2_TEXT, args.campaigns_dir)
    quest_plan_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN, args.campaigns_dir)
    quest_plan_preview_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN_PREVIEW, args.campaigns_dir)
    resolved_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN_RESOLVED, args.campaigns_dir)
    resolved_preview_path = pack_artifact(campaign_id, pack_id, QUEST_PLAN_RESOLVED_PREVIEW, args.campaigns_dir)

    if not stage3_path.exists():
        print(f"stage3 file not found: {stage3_path}")
        return 1

    quest_plan = parse_stage3.parse_file(stage3_path, quest_plan_path, quest_plan_preview_path, stage2_path)
    print(f"stage 3 parsed: quests={quest_plan['summary']['quests_found']} tasks={quest_plan['summary']['tasks_found']}")
    print(f"json written: {quest_plan_path}")
    print(f"preview written: {quest_plan_preview_path}")
    if quest_plan["summary"]["issues"]:
        print(f"stage 3 parse issues: {quest_plan['summary']['issues']}")
        ensure_stage_review(campaign_id, pack_id, "3", args.campaigns_dir)
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
    ensure_stage_review(campaign_id, pack_id, "3", args.campaigns_dir)
    return 0 if resolved_plan["summary"]["issues"] == 0 else 2


def run_context(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    approval_error = context_pack_builder.stage3_approval_error(args.context, campaign_id, pack_id)
    if approval_error is not None:
        print(f"context_pack was not built: {approval_error}.")
        print("Review and approve stage 3 first through workflow_fast.py approve.")
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
        ensure_stage_review(campaign_id, pack_id, "4", args.campaigns_dir)
        return 2
    validate_rc = run_validate(args)
    # Always remind the user where to inspect the result
    print(f"\nStage-4 artifact for review: {output_path}")
    print(f"Validation result: {validate_rc} (0=ok, 2=errors/warnings)")
    return validate_rc


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
    ensure_stage_review(campaign_id, pack_id, "4", args.campaigns_dir)
    return 0 if summary["errors"] == 0 else 2


def run_quest_group(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    approval_error = quest_group_builder.stage4_approval_error(args.context, campaign_id, pack_id)
    if approval_error is not None:
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
    ensure_stage_review(campaign_id, pack_id, "5", args.campaigns_dir)
    return 0 if summary["errors"] == 0 else 2


def run_stage6_split(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    source = pack_artifact(campaign_id, pack_id, STAGE6_REVIEW_XLSX, args.campaigns_dir)
    try:
        result = export_xlsx.split_stage6_workbook(source, campaign_id=campaign_id, force=args.force)
    except (OSError, ValueError) as exc:
        print(str(exc))
        return 2
    print(f"conf tables written: {len(result['files'])} ({source.parent / 'proto'})")
    return 0


def run_stage6(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    input_path = pack_artifact(campaign_id, pack_id, FILLED_TASKS, args.campaigns_dir)
    validation_path = pack_artifact(campaign_id, pack_id, FILLED_TASKS_VALIDATION, args.campaigns_dir)
    quest_group_path = pack_artifact(campaign_id, pack_id, QUEST_GROUP, args.campaigns_dir)
    quest_group_validation_path = pack_artifact(campaign_id, pack_id, QUEST_GROUP_VALIDATION, args.campaigns_dir)
    workbook_path = pack_artifact(campaign_id, pack_id, STAGE6_REVIEW_XLSX, args.campaigns_dir)
    proto_dir = workbook_path.parent / "proto"
    campaign_interactive_manifest_path = args.campaigns_dir / campaign_id / INTERACTIVE_OBJECTS
    pack_interactive_manifest_path = pack_artifact(campaign_id, pack_id, INTERACTIVE_OBJECTS, args.campaigns_dir)
    interactive_manifest_path = campaign_interactive_manifest_path if campaign_interactive_manifest_path.exists() else pack_interactive_manifest_path

    reviews_error = review_docs.required_reviews_error(campaign_id, pack_id, campaigns_dir=args.campaigns_dir)
    if reviews_error is not None:
        print(f"XLSX was not created: {reviews_error}.")
        print("Create and approve review documents for stages 1-5 first.")
        return 1

    if (any(proto_dir.glob("*.xlsx")) or workbook_path.exists()) and not args.force_review:
        print(f"XLSX was not created: stage 6 tables already exist and may contain manual edits: {proto_dir}")
        print("Use the existing conf files for review; pass --force only to regenerate intentionally.")
        return 1

    approval_context = load_context(args.context)
    for required_stage in review_docs.EDITABLE_TEXT_REVIEW_STAGES:
        approval_error = stage_approval_error(
            approval_context,
            required_stage,
            campaign_id=campaign_id,
            pack_id=pack_id,
        )
        if approval_error is not None:
            print(f"XLSX was not created: {approval_error}.")
            print("Approve stages 1-5 in order through workflow_fast.py approve.")
            return 1

    try:
        export_csv.ensure_validation_passed(input_path, validation_path, args.allow_stale_validation)
        export_csv.ensure_quest_group_validation_passed(
            quest_group_path,
            quest_group_validation_path,
            allow_stale=args.allow_stale_validation,
        )
        result = export_xlsx.build_stage6_tables(
            campaign_id=campaign_id,
            pack_id=pack_id,
            campaigns_dir=args.campaigns_dir,
            interactive_manifest_path=interactive_manifest_path,
            force=args.force_review,
        )
        try:
            from .fun_collection_tables import ensure_selected_tables
        except ImportError:
            from fun_collection_tables import ensure_selected_tables
        fun_tables = ensure_selected_tables(campaign_id, pack_id, args.campaigns_dir)
        try:
            from .mystery_rewards import ensure as ensure_mystery_rewards
        except ImportError:
            from mystery_rewards import ensure as ensure_mystery_rewards
        mystery_table = ensure_mystery_rewards(campaign_id, proto_dir)
        try:
            from .technical_quest_tables import build as build_technical_table
        except ImportError:
            from technical_quest_tables import build as build_technical_table
        technical_table = build_technical_table(campaign_id, pack_id, args.campaigns_dir,
                                               force=args.force_review)
        try:
            from .gr_table_review import validate as validate_gr_text
        except ImportError:
            from gr_table_review import validate as validate_gr_text
        validate_gr_text(campaign_id, proto_dir)
        summary = result["quest_summary"]
        actions_summary = result["actions_summary"]
        resource_summary = result["resource_summary"]
        interactive_summary = result["interactive_summary"]
        memory = update_memory_from_pack(campaign_id, pack_id, args.campaigns_dir)
        removed_csv = []
        for path in stage6_legacy_csv_outputs(campaign_id, pack_id, args.campaigns_dir):
            if path.exists():
                path.unlink()
                removed_csv.append(path)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 2

    print(f"final XLSX tables: {len(result['files']) + len(fun_tables) + 2} ({proto_dir})")
    print(f"mystery boxes, recipes and pots: {mystery_table}")
    print(f"invisible shop package list: {proto_dir / (campaign_id + '_shop_invisible_packages.txt')}")
    print(f"workbench recipe addition: {proto_dir / (campaign_id + '_DayOfDomovoyCaldron.txt')}")
    print(f"technical cleanup: assets={technical_table['assets']} stuff={technical_table['stuff']}")
    print(f"quest rows written: {summary['rows_written']}")
    print(
        "actions sheet written: "
        f"(entities={actions_summary['entities']} dialog={actions_summary['dialog_actions']} "
        f"search={actions_summary['search_actions']} give={actions_summary['give_actions']})"
    )
    print(
        "interactive object sheets written: "
        f"{len(interactive_summary['sheets_written'])}"
    )
    print(f"memory updated: used_garbage={len(memory.get('used_garbage', {}))} used_flowers={len(memory.get('used_flowers', {}))}")
    print(f"resource sheet written: blocks={len(resource_summary['blocks'])} warnings={len(resource_summary['warnings'])}")
    if removed_csv:
        print(f"legacy csv removed: {len(removed_csv)}")
    print('Next required step: Stage 6.1 dialogs after manual review; workflow_fast.py dialogs --help.')
    return 0


def run_package_list(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    try:
        from .package_list import build
    except ImportError:
        from package_list import build
    folder = args.tables_dir or pack_artifact(campaign_id,pack_id,"review/proto",args.campaigns_dir)
    try:
        result = build(campaign_id, folder)
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 1
    print(f"package list written: {result['txt']} ({result['packages']} packages)")
    return 0


def run_dialogs(args: argparse.Namespace) -> int:
    """Stage 6.1 edits reviewed tables independently of their original generation gates."""
    try:
        from .dialogue_pipeline import execute
    except ImportError:
        from dialogue_pipeline import execute
    campaign_id, pack_id = resolve_ids(args)
    result = execute(campaign_id, pack_id, campaigns_dir=args.campaigns_dir,
                     game_root=args.game_root, tables_dir=args.tables_dir,
                     plan_path=args.plan, characters_path=args.characters,
                     proto_start=args.proto_start, task_start=args.task_start,
                     apply=args.apply, output_dir=args.output_dir, node=args.node)
    print(f"stage 6.1: {result['mode']}; dialogs={result['dialogs']} replicas={result['replicas']}")
    print(f"tasks: added={result['added_tasks']} existing={result['existing_tasks']}")
    print(f"converter: {result['converter']}; changed files: {result['changed_files']}")
    print(f"candidate and backups: {result['candidate']}")
    print(f"next proto ID: {result['next_proto_id']}; next task ID: {result['next_task_id']}")
    return 0


def run_workbench_addition(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    try:
        from .workbench_addition import build
    except ImportError:
        from workbench_addition import build
    folder = args.tables_dir or pack_artifact(campaign_id,pack_id,"review/proto",args.campaigns_dir)
    try:
        result = build(campaign_id, folder, title=args.title)
    except (ValueError, OSError) as exc:
        print(str(exc))
        return 1
    print(f"workbench addition written: {result['txt']} ({result['recipes']} recipes)")
    return 0


def run_resource_table(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    output_path = args.output_csv or args.output_xlsx or pack_artifact(campaign_id,pack_id,f"review/proto/{campaign_id}_resources.xlsx",args.campaigns_dir)
    rows, summary = resource_table_builder.build_resource_table(campaign_id, campaigns_dir=args.campaigns_dir, pack_ids=args.pack_filter)
    try:
        if output_path.exists() and not args.force:
            raise FileExistsError(f"Preserving existing resource table: {output_path}; use --force to regenerate intentionally")
        if args.output_csv:  # legacy opt-in only; normal quest work never writes CSV
            resource_table_builder.write_csv(output_path, rows)
        else:
            export_xlsx.write_workbook(output_path,[export_xlsx.WorkbookSheet("conf",rows,"resource_table")],campaign_id=campaign_id)
        if args.summary_json:
            resource_table_builder.write_json(args.summary_json, summary)
    except (OSError, ValueError) as exc:
        print(f"could not write resource table: {output_path}")
        print(str(exc))
        return 3
    print(f"resource table written: {output_path}")
    print(f"blocks: {len(summary['blocks'])} warnings: {len(summary['warnings'])}")
    return 0 if not summary["warnings"] else 2


def run_interactive_objects(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args, require_pack=False)
    campaign_dir_path = args.campaigns_dir / campaign_id
    manifest_path = campaign_dir_path / INTERACTIVE_OBJECTS
    preview_path = campaign_dir_path / INTERACTIVE_OBJECTS_PREVIEW

    if args.select:
        manifest = interactive_objects_builder.default_manifest(args.select)
        interactive_objects_builder.write_json(manifest_path, manifest)
        print(f"interactive object selection written: {manifest_path}")

    if not manifest_path.exists():
        print(f"interactive_objects.json not found: {manifest_path}")
        print("Ask the user to choose at least two interactive objects and save the selection first.")
        return 1

    try:
        validation = interactive_objects_builder.write_preview(campaign_id, pack_id, manifest_path, preview_path)
        export_summary = None
        if args.export:
            if not pack_id:
                raise ValueError("pack_id is required for XLSX export; pass --pack")
            sheets, _ = export_xlsx.build_interactive_sheets(campaign_id,pack_id,manifest_path)
            export_summary = export_xlsx.write_conf_tables(
                pack_artifact(campaign_id,pack_id,"review/proto",args.campaigns_dir),sheets,campaign_id=campaign_id,force=args.force)
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(str(exc))
        return 2

    print(f"interactive objects selected: {validation['summary']['selected_count']}")
    print(f"errors: {validation['summary']['errors']}")
    print(f"preview written: {preview_path}")
    if export_summary is not None:
        print(f"interactive object XLSX tables written: {len(export_summary)}")
    return 0 if validation["summary"]["errors"] == 0 else 2


def rebuild_stage_after_review(args: argparse.Namespace, stage: str) -> int:
    if stage == "3":
        return run_stage3(args)
    if stage == "4":
        return run_fill(args)
    if stage == "5":
        rebuild_args = argparse.Namespace(**vars(args))
        rebuild_args.title = ""
        rebuild_args.description = ""
        rebuild_args.description_complete = ""
        rebuild_args.description_spoil = ""
        rebuild_args.output_classname = ""
        rebuild_args.allow_unapproved = False
        return run_quest_group(rebuild_args)
    return 0


def run_approve(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    stage = review_docs.normalize_stage(args.stage)
    current_context = load_context(args.context)
    for prior_stage_number in range(1, int(stage)):
        prior_stage = str(prior_stage_number)
        prior_error = stage_approval_error(
            current_context,
            prior_stage,
            campaign_id=campaign_id,
            pack_id=pack_id,
        )
        if prior_error is not None:
            print(f"stage was not approved: prior gate failed: {prior_error}")
            print("Approve stages in order through workflow_fast.py approve.")
            return 1
    stage_review_path = review_docs.review_path(campaign_id, pack_id, stage, args.campaigns_dir)
    if not review_docs.review_file_is_usable(stage_review_path, stage):
        print(f"stage was not approved: required review document is missing, empty, or has no parsed content: {stage_review_path}")
        print(f"Create it first: workflow_fast.py review --stage {stage} --campaign {campaign_id} --pack {pack_id}")
        return 1

    if stage != "6":
        applied_path = review_docs.apply_review_doc(campaign_id, pack_id, stage, args.campaigns_dir)
        print(f"review applied before approval: {applied_path}")
        rebuild_rc = rebuild_stage_after_review(args, stage)
        if rebuild_rc != 0:
            print(f"stage was not approved: rebuild/validation after review failed with code {rebuild_rc}")
            return rebuild_rc

    context = approve_stage(
        current_context,
        stage,
        campaign_id=campaign_id,
        pack_id=pack_id,
        notes=args.notes,
        review_path=stage_review_path,
        review_sha256=file_sha256(stage_review_path),
    )
    write_json(args.context, context)
    print(f"stage approved: {stage}")
    print(f"review checksum recorded: {context['stage_approvals'][stage]['review_sha256']}")
    print(f"context written: {args.context}")
    return 0


def run_review(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    path = review_docs.review_path(campaign_id, pack_id, args.stage, args.campaigns_dir)
    existed = path.exists() and path.stat().st_size > 0
    path = review_docs.write_review_doc(campaign_id, pack_id, args.stage, args.campaigns_dir, overwrite=args.force)
    action = "overwritten" if existed and args.force else "preserved" if existed else "written"
    print(f"review {action}: {path}")
    return 0


def run_apply_review(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    path = review_docs.apply_review_doc(campaign_id, pack_id, args.stage, args.campaigns_dir)
    print(f"review applied: {path}")
    return 0


def run_status(args: argparse.Namespace) -> int:
    campaign_id, pack_id = resolve_ids(args)
    files = [
        (STAGE2_TEXT, True),
        (STAGE3_TEXT, True),
        (QUEST_PLAN_RESOLVED, True),
        (CONTEXT_PACK, True),
        (INTERACTIVE_OBJECTS, False),
        (INTERACTIVE_OBJECTS_PREVIEW, False),
        (TASK_CHOICES, True),
        (FILLED_TASKS_BUILD, True),
        (FILLED_TASKS, True),
        (FILLED_TASKS_VALIDATION, True),
        (QUEST_GROUP_CHOICES, False),
        (QUEST_GROUP, True),
        (QUEST_GROUP_VALIDATION, True),
        (f"review/proto/{campaign_id}_quests.xlsx", True),
        (f"review/proto/{campaign_id}_actions.xlsx", True),
        (f"review/proto/{campaign_id}_resources.xlsx", True),
        (f"review/proto/{campaign_id}_technical_quests.xlsx", True),
        (f"review/proto/MB_RECIPEMB_POTS_{campaign_id}.xlsx", True),
        ("review/proto/" + export_xlsx.accomplished_workbook_name(campaign_id), True),
    ]
    print(f"campaign: {campaign_id}")
    print(f"pack: {pack_id}")
    campaign_files = [
        (INTERACTIVE_OBJECTS, False),
        (INTERACTIVE_OBJECTS_PREVIEW, False),
        ('dialogue_characters.json', True),
    ]
    for filename, required in campaign_files:
        path = args.campaigns_dir / campaign_id / filename
        if path.exists():
            status = "ok"
        else:
            status = "missing" if required else "optional-missing"
        print(f"campaign/{filename}: {status}")
    for filename, required in files:
        path = pack_artifact(campaign_id, pack_id, filename, args.campaigns_dir)
        if path.exists():
            status = "ok"
        else:
            status = "missing" if required else "optional-missing"
        print(f"{filename}: {status}")
    dialog_plan = pack_artifact(campaign_id, pack_id, 'dialogue_plan.json', args.campaigns_dir)
    print(f"stage 6.1 dialog plan: {'configured' if dialog_plan.is_file() else 'missing'}")
    review_root = pack_artifact(campaign_id, pack_id, REVIEW_DIR, args.campaigns_dir)
    missing_reviews = 0
    for stage, filename in review_docs.STAGE_REVIEW_FILES.items():
        path = review_root / filename
        status = "ok" if review_docs.review_file_is_usable(path, stage) else "missing-or-invalid"
        if status != "ok":
            missing_reviews += 1
        print(f"review/stage {stage}: {status}")
    return 0 if missing_reviews == 0 else 1


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
    quest_group_parser.set_defaults(func=run_quest_group)

    split_parser = subparsers.add_parser("stage6-split", help="Split the existing reviewed XLSX into single-conf files.")
    add_pack_options(split_parser)
    split_parser.add_argument("--force", action="store_true", help="Intentionally replace existing conf exports.")
    split_parser.set_defaults(func=run_stage6_split)

    package_parser = subparsers.add_parser("package-list", help="Refresh the copy-ready shop_invisible package TXT from current XLSX.")
    add_pack_options(package_parser)
    package_parser.add_argument("--tables-dir",type=Path,default=None,help="Explicit folder containing the user's current manual XLSX.")
    package_parser.set_defaults(func=run_package_list)

    workbench_parser = subparsers.add_parser("workbench-addition", help="Refresh the DayOfDomovoyCaldron TXT from all recipes in current XLSX.")
    add_pack_options(workbench_parser)
    workbench_parser.add_argument("--tables-dir",type=Path,default=None,help="Folder containing the user's current manual XLSX.")
    workbench_parser.add_argument("--title",default=None,help="Optional display title; defaults to the reviewed Story group title.")
    workbench_parser.set_defaults(func=run_workbench_addition)

    stage6_parser = subparsers.add_parser("stage6", help="Create final XLSX/conf and shop/workbench TXT; update campaign memory.")
    add_pack_options(stage6_parser)
    stage6_parser.add_argument("--allow-stale-validation", action="store_true")
    stage6_parser.add_argument(
        "--force", "--force-review",
        dest="force_review",
        action="store_true",
        help="Intentionally regenerate existing final XLSX tables (selected FunCollection files are preserved).",
    )
    stage6_parser.set_defaults(func=run_stage6)

    dialogs_parser = subparsers.add_parser('dialogs', help='Stage 6.1: attach reviewed dialogs; preview by default.')
    add_pack_options(dialogs_parser)
    dialogs_parser.add_argument('--game-root', type=Path, required=True)
    dialogs_parser.add_argument('--tables-dir', type=Path)
    dialogs_parser.add_argument('--characters', type=Path, help='Campaign dialogue_characters.json override.')
    dialogs_parser.add_argument('--plan', type=Path, help='Pack dialogue_plan.json override.')
    dialogs_parser.add_argument('--proto-start', type=int)
    dialogs_parser.add_argument('--task-start')
    dialogs_parser.add_argument('--node', default='node')
    dialogs_parser.add_argument('--output-dir', type=Path, help='Empty folder for candidates and backups.')
    dialogs_parser.add_argument('--apply', action='store_true', help='Apply the verified candidate to reviewed files.')
    dialogs_parser.set_defaults(func=run_dialogs)

    resource_table_parser = subparsers.add_parser("resource-table", help="Build final resources.xlsx from all campaign packs.")
    resource_table_parser.add_argument("--campaign", default="", help="Campaign id. Defaults to active_context.")
    resource_table_parser.add_argument("--pack",default="",help="Pack whose review/proto receives resources.xlsx.")
    resource_table_parser.add_argument("--output-xlsx",type=Path,default=None)
    resource_table_parser.add_argument("--force",action="store_true")
    resource_table_parser.add_argument("--pack-filter", action="append", default=None, help="Optional pack filter. Repeatable.")
    resource_table_parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    resource_table_parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT_PATH)
    resource_table_parser.add_argument("--output-csv", type=Path, default=None)
    resource_table_parser.add_argument("--summary-json", type=Path, default=None)
    resource_table_parser.set_defaults(func=run_resource_table)

    interactive_parser = subparsers.add_parser("interactive-objects", help="Validate selected interactive objects and optionally export final XLSX files.")
    add_pack_options(interactive_parser)
    interactive_parser.add_argument("--select", action="append", default=None, help="Template id to write into interactive_objects.json. Repeatable.")
    interactive_parser.add_argument("--export", action="store_true", help="Also export XLSX/conf to the current pack review/proto.")
    interactive_parser.add_argument("--force",action="store_true")
    interactive_parser.set_defaults(func=run_interactive_objects)

    approve_parser = subparsers.add_parser("approve", help="Approve a workflow stage in active_context.")
    add_pack_options(approve_parser)
    approve_parser.add_argument("--stage", required=True)
    approve_parser.add_argument("--notes", default="")
    approve_parser.set_defaults(func=run_approve)

    review_parser = subparsers.add_parser("review", help="Write a user-facing review document for a stage.")
    add_pack_options(review_parser)
    review_parser.add_argument("--stage", required=True)
    review_parser.add_argument("--force", action="store_true", help="Intentionally overwrite an existing text review.")
    review_parser.set_defaults(func=run_review)

    apply_review_parser = subparsers.add_parser("apply-review", help="Apply edits from a stage review document back to workflow files.")
    add_pack_options(apply_review_parser)
    apply_review_parser.add_argument("--stage", required=True)
    apply_review_parser.set_defaults(func=run_apply_review)

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
