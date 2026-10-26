from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

try:
    from . import build_actions_table, build_resource_table, export_csv, interactive_objects, converter_tables
    from .campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir
except ImportError:
    import build_actions_table
    import build_resource_table
    import export_csv
    import interactive_objects
    import converter_tables
    from campaigns import DEFAULT_CAMPAIGNS_DIR, pack_dir


MAX_SHEET_NAME_LENGTH = 31
STAGE6_WORKBOOK_NAME = "stage6_review.xlsx"
ACCOMPLISHED_WORKBOOK_PATTERN = "quest_{campaign_id}_accomplished.xlsx"


def campaign_workbook_name(campaign_id: str, filename: str) -> str:
    """Every delivered table identifies its campaign, including standalone exports."""
    if not campaign_id:
        raise ValueError("campaign_id is required in final workbook filenames")
    return filename if campaign_id in Path(filename).stem else f"{campaign_id}_{filename}"

INTERACTIVE_SHEET_NAMES = {
    "chest_1": "ИНТЕРАКТИВ Chest",
    "help_1": "ИНТЕРАКТИВ HELP",
    "friend_action_1": "ИНТЕРАКТИВ Story_FriendAction",
    "story_random_recipe": "ИНТЕРАКТИВ Story_RandomRecipe",
    "exchanger": "ИНТЕРАКТИВ Exchanger",
    "mixer_1": "ИНТЕРАКТИВ Mixer",
}
INTERACTIVE_ORDER = {
    "chest_1": 10,
    "help_1": 20,
    "exchanger": 30,
    "friend_action_1": 40,
    "story_random_recipe": 50,
    "mixer_1": 60,
}


@dataclass
class WorkbookSheet:
    name: str
    rows: list[list[Any]]
    source: str


def cell_value(value: Any) -> Any:
    if value is None or value == "":
        # The converter distinguishes null from an empty-string cell: only null
        # terminates sl rows. An inline empty string starts a spurious update.
        return None
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return value


def safe_sheet_name(value: str) -> str:
    name = re.sub(r"[:\\/?*\[\]]+", " ", str(value or "").strip())
    name = re.sub(r"\s+", " ", name).strip("' ")
    return name or "Лист"


def unique_sheet_name(value: str, used: set[str]) -> str:
    base = safe_sheet_name(value)[:MAX_SHEET_NAME_LENGTH]
    candidate = base
    counter = 2
    while candidate in used:
        suffix = f" {counter}"
        candidate = f"{base[: MAX_SHEET_NAME_LENGTH - len(suffix)]}{suffix}"
        counter += 1
    used.add(candidate)
    return candidate


def style_sheet(ws) -> None:
    header_fill = PatternFill("solid", fgColor="D9EAF7")
    section_fill = PatternFill("solid", fgColor="EAF3E8")
    type_fill = PatternFill("solid", fgColor="F5F7FA")
    header_font = Font(bold=True, color="1F2933")
    section_font = Font(bold=True, color="234E52")
    thin = Side(style="thin", color="D9E2EC")
    bottom_border = Border(bottom=thin)
    widths: dict[int, int] = {}

    for row in ws.iter_rows():
        values = [cell.value for cell in row]
        non_empty = [str(value).strip() for value in values if str(value or "").strip()]
        first = non_empty[0] if non_empty else ""
        is_type_row = first in {"ml", "sl", "temp_01"}
        is_header_row = "input" in non_empty and "output" in non_empty
        is_section_row = bool(non_empty) and len(non_empty) <= 2

        for cell in row:
            value = "" if cell.value is None else str(cell.value)
            if value:
                widths[cell.column] = min(max(widths.get(cell.column, 8), len(value) + 2), 60)
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            if is_header_row:
                cell.font = header_font
                cell.fill = header_fill
                cell.border = bottom_border
            elif is_section_row:
                cell.font = section_font
                cell.fill = section_fill
                cell.border = bottom_border
            elif is_type_row:
                cell.fill = type_fill

    for column_index, width in widths.items():
        ws.column_dimensions[get_column_letter(column_index)].width = max(10, width)
    ws.sheet_view.showGridLines = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0


def write_workbook(output_path: Path, sheets: list[WorkbookSheet], *, campaign_id: str | None = None) -> dict[str, Any]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    wb.remove(wb.active)

    used_names: set[str] = set()
    written_sheets: list[dict[str, Any]] = []
    for sheet in sheets:
        sheet_name = unique_sheet_name(sheet.name, used_names)
        ws = wb.create_sheet(title=sheet_name)
        max_columns = 0
        normalized_rows = converter_tables.normalize_rows(sheet.rows,campaign_id=campaign_id)
        for row in normalized_rows:
            values = [cell_value(value) for value in row]
            max_columns = max(max_columns, len(values))
            ws.append(values)
        style_sheet(ws)
        ws.freeze_panes = None
        converter_tables.prepare_sheet(ws)
        errors = converter_tables.validate_sheet(ws,campaign_id=campaign_id)
        if errors:
            raise ValueError(f"{sheet.name}: " + "; ".join(errors))
        written_sheets.append(
            {
                "name": sheet_name,
                "source": sheet.source,
                "rows": len(normalized_rows),
                "columns": max_columns,
            }
        )

    wb.save(output_path)
    reopened = load_workbook(output_path, data_only=False)
    expected_names = [item["name"] for item in written_sheets]
    if reopened.sheetnames != expected_names:
        raise ValueError(f"xlsx sheet order mismatch: {reopened.sheetnames} != {expected_names}")
    for ws in reopened.worksheets:
        for row in ws.iter_rows(values_only=True):
            for value in row:
                if isinstance(value, str) and "????" in value:
                    raise ValueError(f"xlsx contains broken Cyrillic marker on sheet {ws.title}")

    if campaign_id and expected_names == ["conf"]:
        try:
            from .package_list import build as build_package_list
            from .workbench_addition import build as build_workbench_addition
        except ImportError:
            from package_list import build as build_package_list
            from workbench_addition import build as build_workbench_addition
        build_package_list(campaign_id, output_path.parent)
        build_workbench_addition(campaign_id, output_path.parent)
    return {"xlsx": str(output_path), "sheets": written_sheets}


def split_stage6_workbook(source: Path, output_dir: Path | None = None, *, campaign_id: str | None = None, force: bool = False) -> dict[str, Any]:
    """Read the human-reviewed book; never regenerate its authored values."""
    output_dir = output_dir or source.parent / "proto"
    if campaign_id is None and source.parent.name == "review" and source.parent.parent.name.startswith("pack_"):
        campaign_id = source.parents[2].name
    if not campaign_id:
        raise ValueError("campaign_id is required for prefixed conf filenames")
    wb = load_workbook(source, data_only=False)
    names = {"КВЕСТЫ": ("quests", "generated_quests"),
             "ЭКШЕНЫ": ("actions", "generated_actions"),
             "РЕСУРСЫ": ("resources", "resource_table")}
    files = []
    planned = []
    for index, ws in enumerate(wb.worksheets, 1):
        stem, kind = names.get(ws.title, (
            "interactive_" + re.sub(r"[^a-z0-9]+", "_", ws.title.split(" ",1)[-1].lower()).strip("_"),
            "interactive"))
        stem = stem or f"sheet_{index}"
        path = output_dir / campaign_workbook_name(campaign_id, f"{stem}.xlsx")
        if path in [item[2] for item in planned]:
            raise ValueError(f"Duplicate export filename for sheet {ws.title}: {path}")
        if path.exists() and not force:
            raise FileExistsError(f"Preserving existing conf table: {path}; use --force to replace it")
        planned.append((ws,kind,path))
    for ws, kind, path in planned:
        result = write_workbook(path, [WorkbookSheet("conf", list(ws.values), kind)],campaign_id=campaign_id)
        # Fresh conf files do not inherit frozen rows from the legacy master.
        errors = converter_tables.validate(path)
        if errors:
            raise ValueError(f"{path}: {errors}")
        files.append({"source_sheet":ws.title,"xlsx":str(path),"rows":result["sheets"][0]["rows"]})
    wb.close()
    return {"source":str(source),"files":files}


def accomplished_workbook_name(campaign_id: str) -> str:
    return ACCOMPLISHED_WORKBOOK_PATTERN.format(campaign_id=campaign_id)


def accomplished_rows(campaign_id: str, filled_tasks: dict[str, Any]) -> list[list[Any]]:
    rows: list[list[Any]] = [
        ["", f"quest_{campaign_id}_Story_accomplished"],
        ["sl", "string", "string", "string", "string", "string", "string", "string", "string", "string", "int", "int", "int"],
        ["", "input", "output", "identifier", "title", "text", "img_url", "photo_id", "link_text", "clicker_reward", "clicks_limit", "life_time", "id"],
    ]
    seen: set[str] = set()
    for quest in filled_tasks.get("quests", []):
        classname = str(quest.get("classname_quests") or "").strip()
        if not classname:
            raise ValueError("filled_tasks quest is missing classname_quests for accomplished export")
        if classname in seen:
            raise ValueError(f"duplicate classname_quests in accomplished export: {classname}")
        seen.add(classname)
        identifier = f"quest_{classname}_accomplished"
        rows.append(
            [
                "",
                "/post_action/quest_Night_2026_Story_1_accomplished.proto.js",
                f"/post_action/{identifier}.proto.js",
                identifier,
                "Задание выполнено!",
                "ТЫ МОЛОДЕЦ!",
                "icon/post_new/quest_Night_2026_Story.jpg",
                "456244744",
                "Получить {0}",
                "money_alt=50",
                5,
                43200,
                "",
            ]
        )
    return rows


def build_accomplished_workbook(
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    output_xlsx: Path | None = None,
) -> dict[str, Any]:
    target = pack_dir(campaign_id, pack_id, campaigns_dir)
    filled_tasks = export_csv.read_json(target / "filled_tasks.json")
    rows = accomplished_rows(campaign_id, filled_tasks)
    output_path = output_xlsx or target / "review" / "proto" / accomplished_workbook_name(campaign_id)
    workbook = write_workbook(output_path, [WorkbookSheet("conf", rows, "quest_accomplished")],campaign_id=campaign_id)
    return {
        "xlsx": str(output_path),
        "quests": len(rows) - 3,
        "rows": len(rows),
        "workbook": workbook,
    }


def quest_rows_and_summary(filled_tasks: dict[str, Any], quest_group: dict[str, Any]) -> tuple[list[list[Any]], dict[str, int]]:
    quests = filled_tasks.get("quests", [])
    rows = export_csv.iter_csv_rows(quests, quest_group=quest_group)
    return rows, {
        "quests_found": len(quests),
        "quest_group_exported": 1,
        "quest_blocks_exported": len(quests),
        "tasks_exported": sum(len(quest.get("tasks", [])) for quest in quests),
        "rows_written": len(rows),
    }


def interactive_sheet_title(selection: dict[str, Any], template: dict[str, Any]) -> str:
    template_id = str(selection.get("template_id") or "")
    if template_id in INTERACTIVE_SHEET_NAMES:
        return INTERACTIVE_SHEET_NAMES[template_id]
    display = template.get("display_name_ru") or template_id
    return f"ИНТЕРАКТИВ {display}"


def build_interactive_sheets(
    campaign_id: str,
    pack_id: str,
    manifest_path: Path,
) -> tuple[list[WorkbookSheet], dict[str, Any]]:
    templates_data = interactive_objects.load_templates()
    manifest = interactive_objects.read_json(manifest_path)
    validation = interactive_objects.validate_manifest(manifest, templates_data)
    if validation["summary"]["errors"]:
        first = validation["errors"][0]
        raise ValueError(f"interactive_objects.json is invalid: {first['code']}: {first['message']}")

    templates = templates_data["templates"]
    selections = sorted(
        validation["objects"],
        key=lambda item: (
            INTERACTIVE_ORDER.get(str(item.get("template_id") or ""), 1000),
            str(item.get("object_id") or item.get("template_id") or ""),
        ),
    )

    sheets: list[WorkbookSheet] = []
    sheet_items: list[dict[str, Any]] = []
    for selection in selections:
        template_id = str(selection["template_id"])
        template = templates[template_id]
        rows = interactive_objects.build_rows_for_selection(campaign_id, selection)
        sheet_name = interactive_sheet_title(selection, template)
        object_id = str(selection.get("object_id") or template_id)
        sheets.append(WorkbookSheet(sheet_name, rows, f"interactive:{object_id}"))
        sheet_items.append(
            {
                "template_id": template_id,
                "object_id": object_id,
                "result_resource": interactive_objects.result_resource_classname(campaign_id, selection, template),
                "sheet": sheet_name,
                "rows": len(rows),
            }
        )

    summary = {
        "campaign_id": campaign_id,
        "pack_id": pack_id,
        "manifest": str(manifest_path),
        "selected_count": validation["summary"]["selected_count"],
        "sheets_written": sheet_items,
        "files_written": sheet_items,
    }
    return sheets, summary


def stage6_sheets_and_summaries(
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    interactive_manifest_path: Path | None = None,
) -> dict[str, Any]:
    target = pack_dir(campaign_id, pack_id, campaigns_dir)

    filled_tasks = export_csv.read_json(target / "filled_tasks.json")
    quest_group = export_csv.read_json(target / "quest_group.json")
    quest_rows, quest_summary = quest_rows_and_summary(filled_tasks, quest_group)
    registry_path = campaigns_dir / campaign_id / 'dialogue_characters.json'
    if registry_path.exists():
        try:
            from .dialogue_pipeline import load_registry, map_helper_rows
        except ImportError:
            from dialogue_pipeline import load_registry, map_helper_rows
        map_helper_rows(quest_rows, load_registry(registry_path))

    actions_rows, actions_summary = build_actions_table.build_actions(
        campaign_id,
        campaigns_dir=campaigns_dir,
        current_pack_id=pack_id,
    )
    resource_rows, resource_summary = build_resource_table.build_resource_table(
        campaign_id,
        campaigns_dir=campaigns_dir,
    )

    sheets = [
        WorkbookSheet("КВЕСТЫ", quest_rows, "generated_quests"),
        WorkbookSheet("ЭКШЕНЫ", actions_rows, "generated_actions"),
        WorkbookSheet("РЕСУРСЫ", resource_rows, "resource_table"),
    ]

    interactive_summary = {
        "campaign_id": campaign_id,
        "pack_id": pack_id,
        "manifest": "",
        "selected_count": 0,
        "sheets_written": [],
        "files_written": [],
    }
    if interactive_manifest_path is not None and interactive_manifest_path.exists():
        interactive_sheets, interactive_summary = build_interactive_sheets(
            campaign_id,
            pack_id,
            interactive_manifest_path,
        )
        sheets.extend(interactive_sheets)

    return {
        "sheets": sheets,
        "quest_summary": quest_summary,
        "actions_summary": actions_summary,
        "resource_summary": resource_summary,
        "interactive_summary": interactive_summary,
    }


def build_stage6_review_workbook(
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    output_xlsx: Path | None = None,
    interactive_manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Legacy overview helper; normal Stage 6 writes final conf files directly."""
    result = stage6_sheets_and_summaries(campaign_id,pack_id,campaigns_dir,interactive_manifest_path)
    path = output_xlsx or pack_dir(campaign_id,pack_id,campaigns_dir)/"review"/STAGE6_WORKBOOK_NAME
    result["workbook"] = write_workbook(path,result.pop("sheets"),campaign_id=campaign_id)
    return result


def build_stage6_tables(
    campaign_id: str,
    pack_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    interactive_manifest_path: Path | None = None,
    *, force: bool = False,
) -> dict[str, Any]:
    """Create final XLSX and shop/workbench TXT; no overview, manifests, CSV or ZIP."""
    result = stage6_sheets_and_summaries(campaign_id,pack_id,campaigns_dir,interactive_manifest_path)
    target = pack_dir(campaign_id,pack_id,campaigns_dir)/"review"/"proto"
    filled_tasks = export_csv.read_json(pack_dir(campaign_id,pack_id,campaigns_dir)/"filled_tasks.json")
    result["sheets"].append(WorkbookSheet(Path(accomplished_workbook_name(campaign_id)).stem,accomplished_rows(campaign_id,filled_tasks),"quest_accomplished"))
    result["files"] = write_conf_tables(target,result.pop("sheets"),campaign_id=campaign_id,force=force)
    return result


def write_conf_tables(target: Path, sheets: list[WorkbookSheet], *, campaign_id: str, force=False):
    names = {"generated_quests":"quests","generated_actions":"actions","resource_table":"resources",
             }
    planned, used = [], set()
    for sheet in sheets:
        stem = names.get(sheet.source) or (sheet.name if sheet.source=="quest_accomplished" else "interactive_" + re.sub(r"[^a-z0-9]+","_",sheet.name.split(" ",1)[-1].lower()).strip("_"))
        base, number = stem, 2
        while stem in used:
            stem, number = f"{base}_{number}", number+1
        used.add(stem)
        path = target/campaign_workbook_name(campaign_id,f"{stem}.xlsx")
        if path.exists() and not force:
            raise FileExistsError(f"Preserving manually editable table: {path}; use --force to regenerate intentionally")
        planned.append((sheet,path))
    files = []
    for sheet,path in planned:
        rows = sheet.rows
        book = write_workbook(path,[WorkbookSheet("conf",rows,sheet.source)],campaign_id=campaign_id)
        files.append({"xlsx":str(path),"source":sheet.source,"rows":book["sheets"][0]["rows"]})
    return files
