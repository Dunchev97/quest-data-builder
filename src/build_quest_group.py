from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .workflow_context import DEFAULT_CONTEXT_PATH, load_context, stage_is_approved
except ImportError:
    from workflow_context import DEFAULT_CONTEXT_PATH, load_context, stage_is_approved

try:
    from .campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir
except ImportError:
    from campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT_PATH = PROJECT_ROOT / "output" / "filled_tasks.json"
DEFAULT_OUTPUT_JSON_PATH = PROJECT_ROOT / "output" / "quest_group.json"
DEFAULT_VALIDATION_PATH = PROJECT_ROOT / "output" / "quest_group.validation.json"
DEFAULT_PREVIEW_PATH = PROJECT_ROOT / "output" / "quest_group.preview.md"
QUEST_GROUP_JSON_NAME = "quest_group.json"
QUEST_GROUP_CHOICES_NAME = "quest_group_choices.json"
QUEST_GROUP_VALIDATION_NAME = "quest_group.validation.json"
QUEST_GROUP_PREVIEW_NAME = "quest_group.preview.md"
FILLED_TASKS_JSON_NAME = "filled_tasks.json"
QUEST_REFERENCE_CAMPAIGN_ID = "Night_2026"
QUEST_GROUP_REFERENCE_ID = 125028
QUEST_GROUP_INPUT_PATH = f"/quest_group/event/{QUEST_REFERENCE_CAMPAIGN_ID}_Story.proto.js"
QUEST_GROUP_PATH_PREFIX = "/quest_group/event"
REQUIRED_APPROVAL_STAGE = "4"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def resolve_campaign_pack(
    campaign_id: str | None,
    pack_id: str | None,
    context_path: Path = DEFAULT_CONTEXT_PATH,
) -> tuple[str | None, str | None]:
    if campaign_id and pack_id:
        return campaign_id, pack_id

    context = load_context(context_path)
    return campaign_id or context.get("campaign_id"), pack_id or context.get("pack_id")


def pack_artifact_path(campaign_id: str | None, pack_id: str | None, filename: str) -> Path | None:
    if not campaign_id or not pack_id:
        return None
    return pack_dir(campaign_id, pack_id, DEFAULT_CAMPAIGNS_DIR) / filename


def default_artifact_path(campaign_id: str | None, pack_id: str | None, filename: str, fallback: Path) -> Path:
    path = pack_artifact_path(campaign_id, pack_id, filename)
    return path if path is not None else fallback


def quest_classname(quest: dict[str, Any]) -> str:
    return str(quest.get("classname_quests") or quest.get("classname") or "QuestGroup")


def infer_group_classname(filled_tasks: dict[str, Any]) -> str:
    quests = filled_tasks.get("quests") or []
    if not quests:
        return "QuestGroup"

    classname = quest_classname(quests[0])
    if "_Story_" in classname:
        return classname.split("_Story_", 1)[0]
    return classname


def infer_output_path(filled_tasks: dict[str, Any], output_classname: str | None = None) -> str:
    campaign_id = output_classname or infer_group_classname(filled_tasks)
    if "_Story_" in campaign_id:
        campaign_id = campaign_id.split("_Story_", 1)[0]
    if campaign_id.endswith("_Story"):
        campaign_id = campaign_id[: -len("_Story")]
    return f"{QUEST_GROUP_PATH_PREFIX}/{campaign_id}_Story.proto.js"


def quest_group_classname(campaign_id: str | None = None, pack_id: str | None = None) -> str | None:
    if not campaign_id:
        return None
    return campaign_id


def build_quest_group(
    filled_tasks: dict[str, Any],
    title: str,
    description: str,
    description_complete: str,
    description_spoil: str,
    output_classname: str | None = None,
) -> dict[str, Any]:
    campaign_id = output_classname or infer_group_classname(filled_tasks)
    if "_Story_" in campaign_id:
        campaign_id = campaign_id.split("_Story_", 1)[0]
    if campaign_id.endswith("_Story"):
        campaign_id = campaign_id[: -len("_Story")]
    return {
        "input": QUEST_GROUP_INPUT_PATH,
        "output": infer_output_path(filled_tasks, output_classname=campaign_id),
        "title": title,
        "description": description,
        "description_complete": description_complete,
        "description_spoil": description_spoil,
        "id": QUEST_GROUP_REFERENCE_ID,
        "find": QUEST_REFERENCE_CAMPAIGN_ID,
        "replace": campaign_id,
    }


def normalize_quest_group_choices(choices: dict[str, Any]) -> dict[str, str]:
    source = choices.get("quest_group") if isinstance(choices.get("quest_group"), dict) else choices
    return {
        "title": str(source.get("title") or "").strip(),
        "description": str(source.get("description") or "").strip(),
        "description_complete": str(source.get("description_complete") or "").strip(),
        "description_spoil": str(source.get("description_spoil") or "").strip(),
        "output_classname": str(source.get("output_classname") or "").strip(),
    }


def read_quest_group_choices(path: Path) -> dict[str, str]:
    return normalize_quest_group_choices(read_json(path))


def issue(severity: str, code: str, message: str, **extra: Any) -> dict[str, Any]:
    item = {"severity": severity, "code": code, "message": message}
    item.update(extra)
    return item


def validate_quest_group(quest_group: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, Any]] = []
    for field_name in ("input", "output", "title", "description", "description_complete", "description_spoil", "id", "find", "replace"):
        if quest_group.get(field_name) in (None, "", []):
            issues.append(issue("error", "missing_quest_group_field", f"quest_group is missing field: {field_name}", field=field_name))

    if quest_group.get("input") != QUEST_GROUP_INPUT_PATH:
        issues.append(
            issue(
                "error",
                "quest_group_input_mismatch",
                "quest_group.input must stay fixed.",
                expected=QUEST_GROUP_INPUT_PATH,
                actual=quest_group.get("input"),
            )
        )

    output = str(quest_group.get("output") or "")
    if not output.startswith(f"{QUEST_GROUP_PATH_PREFIX}/") or not output.endswith(".proto.js"):
        issues.append(
            issue(
                "error",
                "quest_group_output_path_invalid",
                "quest_group.output must look like /quest_group/event/<campaign_id>_Story.proto.js.",
                actual=quest_group.get("output"),
            )
        )

    if quest_group.get("id") != QUEST_GROUP_REFERENCE_ID:
        issues.append(
            issue(
                "error",
                "quest_group_reference_id_mismatch",
                "quest_group.id must match the Night_2026 donor row.",
                expected=QUEST_GROUP_REFERENCE_ID,
                actual=quest_group.get("id"),
            )
        )

    if quest_group.get("find") != QUEST_REFERENCE_CAMPAIGN_ID:
        issues.append(
            issue(
                "error",
                "quest_group_find_mismatch",
                "quest_group.find must reference the Night_2026 donor.",
                expected=QUEST_REFERENCE_CAMPAIGN_ID,
                actual=quest_group.get("find"),
            )
        )

    expected_output = f"{QUEST_GROUP_PATH_PREFIX}/{quest_group.get('replace') or ''}_Story.proto.js"
    if output != expected_output:
        issues.append(
            issue(
                "error",
                "quest_group_replace_output_mismatch",
                "quest_group.output must be built from quest_group.replace.",
                expected=expected_output,
                actual=output,
            )
        )

    if "extra" in quest_group:
        issues.append(issue("error", "legacy_quest_group_extra", "quest_group.extra is not part of the Night_2026 template."))

    errors = [item for item in issues if item["severity"] == "error"]
    warnings = [item for item in issues if item["severity"] == "warning"]
    return {
        "summary": {
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "errors": errors,
        "warnings": warnings,
    }


def render_preview(quest_group: dict[str, Any], validation: dict[str, Any]) -> str:
    summary = validation["summary"]
    lines = [
        "# Quest Group Preview",
        "",
        f"Errors: {summary['errors']}",
        f"Warnings: {summary['warnings']}",
        "",
        f"- input: `{quest_group.get('input') or ''}`",
        f"- output: `{quest_group.get('output') or ''}`",
        f"- title: {quest_group.get('title') or ''}",
        f"- description: {quest_group.get('description') or ''}",
        f"- description_complete: {quest_group.get('description_complete') or ''}",
        f"- description_spoil: {quest_group.get('description_spoil') or ''}",
        f"- id: `{quest_group.get('id') or ''}`",
        f"- find: `{quest_group.get('find') or ''}`",
        f"- replace: `{quest_group.get('replace') or ''}`",
        "",
    ]
    if validation["errors"]:
        lines.extend(["## Errors", ""])
        for item in validation["errors"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
        lines.append("")
    return "\n".join(lines)


def stage4_approval_error(
    context_path: Path,
    campaign_id: str | None = None,
    pack_id: str | None = None,
) -> str | None:
    context = load_context(context_path)
    expected_campaign_id = campaign_id or context.get("campaign_id") or ""
    expected_pack_id = pack_id or context.get("pack_id") or ""
    if stage_is_approved(context, REQUIRED_APPROVAL_STAGE, campaign_id=expected_campaign_id, pack_id=expected_pack_id):
        return None

    approval = (context.get("stage_approvals") or {}).get(REQUIRED_APPROVAL_STAGE) or {}
    if approval.get("approved"):
        return (
            "stage 4 approval belongs to another campaign/pack: "
            f"{approval.get('campaign_id') or '-'} / {approval.get('pack_id') or '-'}"
        )
    return "stage 4 approval is missing"


def build_quest_group_file(
    input_path: Path,
    output_json_path: Path,
    validation_path: Path,
    preview_path: Path,
    title: str,
    description: str,
    description_complete: str,
    description_spoil: str,
    output_classname: str | None = None,
    campaign_id: str | None = None,
    pack_id: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    output_classname = output_classname or quest_group_classname(campaign_id, pack_id)
    quest_group = build_quest_group(
        read_json(input_path),
        title=title,
        description=description,
        description_complete=description_complete,
        description_spoil=description_spoil,
        output_classname=output_classname,
    )
    validation = validate_quest_group(quest_group)
    write_json(output_json_path, quest_group)
    write_json(validation_path, validation)
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(render_preview(quest_group, validation), encoding="utf-8")
    return quest_group, validation


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build stage 5 quest group metadata from AI-written pack summary.")
    parser.add_argument("input", nargs="?", type=Path, default=None, help="Stage 4 filled_tasks.json.")
    parser.add_argument("--output-json", type=Path, default=None)
    parser.add_argument("--validation-json", type=Path, default=None)
    parser.add_argument("--preview", type=Path, default=None)
    parser.add_argument("--choices", type=Path, default=None, help="AI-written quest_group_choices.json.")
    parser.add_argument("--title", default="", help="AI-written quest group title.")
    parser.add_argument("--description", default="", help="AI-written short setup description.")
    parser.add_argument("--description-complete", default="", help="AI-written successful completion description.")
    parser.add_argument("--description-spoil", default="", help="AI-written failed completion description.")
    parser.add_argument("--output-classname", default="", help="Optional quest group classname for output path.")
    parser.add_argument("--approval-context", type=Path, default=DEFAULT_CONTEXT_PATH)
    parser.add_argument("--campaign", default="")
    parser.add_argument("--current-pack", default="")
    parser.add_argument(
        "--allow-unapproved-stage4",
        action="store_true",
        help="Emergency override: build quest_group without recorded stage 4 approval.",
    )
    args = parser.parse_args(argv)

    campaign_id, pack_id = resolve_campaign_pack(
        args.campaign or None,
        args.current_pack or None,
        context_path=args.approval_context,
    )
    input_path = args.input or default_artifact_path(campaign_id, pack_id, FILLED_TASKS_JSON_NAME, DEFAULT_INPUT_PATH)
    output_json_path = args.output_json or default_artifact_path(campaign_id, pack_id, QUEST_GROUP_JSON_NAME, DEFAULT_OUTPUT_JSON_PATH)
    validation_path = args.validation_json or default_artifact_path(campaign_id, pack_id, QUEST_GROUP_VALIDATION_NAME, DEFAULT_VALIDATION_PATH)
    preview_path = args.preview or default_artifact_path(campaign_id, pack_id, QUEST_GROUP_PREVIEW_NAME, DEFAULT_PREVIEW_PATH)
    choices_path = args.choices or default_artifact_path(campaign_id, pack_id, QUEST_GROUP_CHOICES_NAME, DEFAULT_OUTPUT_JSON_PATH.with_name(QUEST_GROUP_CHOICES_NAME))

    if not input_path.exists():
        print(f"input file not found: {input_path}")
        return 1

    choices = {
        "title": args.title,
        "description": args.description,
        "description_complete": args.description_complete,
        "description_spoil": args.description_spoil,
        "output_classname": args.output_classname,
    }
    if not all(choices[field] for field in ("title", "description", "description_complete", "description_spoil")):
        if choices_path.exists():
            file_choices = read_quest_group_choices(choices_path)
            choices = {
                field: choices[field] or file_choices[field]
                for field in ("title", "description", "description_complete", "description_spoil", "output_classname")
            }
        else:
            print(f"quest group choices not found: {choices_path}")
            print("Pass --title/--description/... or create quest_group_choices.json.")
            return 1

    missing_fields = [field for field in ("title", "description", "description_complete", "description_spoil") if not choices[field]]
    if missing_fields:
        print(f"quest_group text fields are missing: {', '.join(missing_fields)}")
        return 1

    if not args.allow_unapproved_stage4:
        approval_error = stage4_approval_error(
            args.approval_context,
            campaign_id=campaign_id,
            pack_id=pack_id,
        )
        if approval_error is not None:
            print(f"quest_group was not built: {approval_error}.")
            print("Сначала покажи пользователю результат этапа 4 и получи явный апрув в чате.")
            print(
                "Затем запиши апрув командой: "
                "python src/workflow_context.py approve --stage 4 "
                "--campaign <campaign_id> --pack <pack_id>"
            )
            return 1

    try:
        quest_group, validation = build_quest_group_file(
            input_path=input_path,
            output_json_path=output_json_path,
            validation_path=validation_path,
            preview_path=preview_path,
            title=choices["title"],
            description=choices["description"],
            description_complete=choices["description_complete"],
            description_spoil=choices["description_spoil"],
            output_classname=choices["output_classname"] or None,
            campaign_id=campaign_id,
            pack_id=pack_id,
        )
    except OSError as exc:
        print(str(exc))
        return 1

    summary = validation["summary"]
    print(f"output: {quest_group['output']}")
    print(f"errors: {summary['errors']}")
    print(f"warnings: {summary['warnings']}")
    print(f"json written: {output_json_path}")
    print(f"validation written: {validation_path}")
    print(f"preview written: {preview_path}")
    return 0 if summary["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
