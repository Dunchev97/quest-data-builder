from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATES_PATH = PROJECT_ROOT / "data" / "interactive_object_templates.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "output"

INTERACTIVE_OBJECTS_NAME = "interactive_objects.json"
INTERACTIVE_OBJECTS_PREVIEW_NAME = "interactive_objects.preview.md"
GENERATED_INTERACTIVE_SUMMARY_NAME = "generated_interactive_objects.summary.json"
MIN_SELECTED_OBJECTS = 2
CSV_ENCODING = "cp1251"
CASE_FORMS = {
    "Бочка с солеными огурцами": {"accusative": "Бочку с солеными огурцами"},
    "Банка малосольных огурчиков": {"accusative": "Банку малосольных огурчиков"},
    "Хрустящая реликвия праздника": {"accusative": "Хрустящую реликвию праздника"},
    "Малосольная долька": {"accusative": "Малосольную дольку"},
    "Малосольный гостинец": {"accusative": "Малосольный гостинец"},
    "Рассольные ключики": {"accusative": "Рассольные ключики"},
    "Душистый укроп": {"accusative": "Душистый укроп"},
}


@dataclass(frozen=True)
class InteractiveIngredient:
    template_id: str
    classname: str
    title: str
    object_id: str
    amount: int = 1


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=CSV_ENCODING, newline="") as handle:
        writer = csv.writer(handle, delimiter=";", quotechar='"', lineterminator="\r\n")
        writer.writerows(rows)


def load_templates(path: Path = DEFAULT_TEMPLATES_PATH) -> dict[str, Any]:
    data = read_json(path)
    templates = {template["id"]: template for template in data.get("templates", [])}
    return {
        "version": data.get("version", 1),
        "min_selected_objects": int(data.get("min_selected_objects") or MIN_SELECTED_OBJECTS),
        "templates": templates,
    }


def safe_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return value.strip("_") or "object"


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def clean_text(value: Any) -> str:
    return str(value or "").strip()


def phrase_form(value: Any, case_name: str) -> str:
    text = clean_text(value)
    return str((CASE_FORMS.get(text) or {}).get(case_name) or text)


def accusative(value: Any) -> str:
    return phrase_form(value, "accusative")


def ensure_period(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    return value if value[-1] in ".!?" else f"{value}."


def first_non_empty(*values: Any) -> str:
    for value in values:
        text = clean_text(value)
        if text:
            return text
    return ""


def normalize_raw_selection(raw: Any) -> dict[str, Any]:
    if isinstance(raw, str):
        return {"template_id": raw}
    if isinstance(raw, dict):
        return dict(raw)
    return {}


def mechanic_family(mechanic_prefix: str) -> str:
    match = re.fullmatch(r"(.+)_1", mechanic_prefix)
    return match.group(1) if match else mechanic_prefix


def numbered_mechanic_prefix(default_prefix: str, number: int, duplicate_count: int) -> str:
    family = mechanic_family(default_prefix)
    if duplicate_count > 1 or default_prefix.endswith("_1"):
        return f"{family}_{number}"
    return default_prefix


def merged_selection(raw: Any, templates: dict[str, dict[str, Any]]) -> dict[str, Any]:
    selection = normalize_raw_selection(raw)
    template_id = clean_text(selection.get("template_id") or selection.get("id"))
    template = templates.get(template_id) or {}
    merged = dict(template.get("defaults") or {})
    merged.update(selection)
    merged["template_id"] = template_id
    return merged


def selected_objects(manifest: dict[str, Any], templates: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    source = manifest.get("selected_objects")
    if source is None:
        source = manifest.get("objects")
    result: list[dict[str, Any]] = []
    for raw in as_list(source):
        item = merged_selection(raw, templates)
        if item.get("enabled") is False:
            continue
        result.append(item)

    family_totals: dict[str, int] = {}
    for item in result:
        template = templates.get(str(item.get("template_id"))) or {}
        family = mechanic_family(clean_text(template.get("mechanic_prefix")) or str(item.get("template_id")))
        family_totals[family] = family_totals.get(family, 0) + 1

    family_seen: dict[str, int] = {}
    normalized: list[dict[str, Any]] = []
    for item in result:
        template = templates.get(str(item.get("template_id"))) or {}
        default_prefix = clean_text(template.get("mechanic_prefix")) or str(item.get("template_id"))
        family = mechanic_family(default_prefix)
        explicit_number = item.get("object_number")
        if explicit_number not in (None, ""):
            number = int(explicit_number)
        else:
            family_seen[family] = family_seen.get(family, 0) + 1
            number = family_seen[family]
        mechanic_prefix = clean_text(item.get("mechanic_prefix")) or numbered_mechanic_prefix(default_prefix, number, family_totals.get(family, 1))
        updated = dict(item)
        updated["object_number"] = number
        updated["mechanic_prefix"] = mechanic_prefix
        updated["object_id"] = clean_text(updated.get("object_id")) or mechanic_prefix.lower()
        normalized.append(updated)
    return normalized


def selected_count(objects: list[dict[str, Any]], templates: dict[str, dict[str, Any]]) -> int:
    return sum(int((templates.get(item["template_id"]) or {}).get("counts_as") or 1) for item in objects)


def validate_list_field(
    selection: dict[str, Any],
    template: dict[str, Any],
    field_name: str,
    expected_count: int,
    errors: list[dict[str, Any]],
) -> None:
    values = as_list(selection.get(field_name))
    if len(values) != expected_count:
        errors.append(
            {
                "code": "interactive_list_length_mismatch",
                "template_id": selection.get("template_id"),
                "field": field_name,
                "expected": expected_count,
                "actual": len(values),
                "message": f"{field_name} must contain {expected_count} items.",
            }
        )
    if any(not clean_text(value) for value in values):
        errors.append(
            {
                "code": "interactive_list_has_empty_value",
                "template_id": selection.get("template_id"),
                "field": field_name,
                "message": f"{field_name} contains an empty value.",
            }
        )


def validate_manifest(
    manifest: dict[str, Any],
    templates_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    templates_data = templates_data or load_templates()
    templates = templates_data["templates"]
    objects = selected_objects(manifest, templates)
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    count = selected_count(objects, templates)
    if count < int(templates_data.get("min_selected_objects") or MIN_SELECTED_OBJECTS):
        errors.append(
            {
                "code": "not_enough_interactive_objects",
                "message": "Select at least two interactive objects. Paired Home/Guest objects count as one.",
                "selected_count": count,
                "required_count": int(templates_data.get("min_selected_objects") or MIN_SELECTED_OBJECTS),
            }
        )

    seen_object_ids: set[str] = set()
    seen_result_suffixes: set[str] = set()
    for selection in objects:
        template_id = selection.get("template_id")
        template = templates.get(template_id)
        if template is None:
            errors.append(
                {
                    "code": "unknown_interactive_template",
                    "template_id": template_id,
                    "message": "Interactive object template is not supported.",
                }
            )
            continue

        object_id = clean_text(selection.get("object_id")) or template_id
        if object_id in seen_object_ids:
            errors.append(
                {
                    "code": "duplicate_interactive_object_id",
                    "template_id": template_id,
                    "object_id": object_id,
                    "message": "Each selected interactive object must have a unique object_id.",
                }
            )
        seen_object_ids.add(object_id)

        result_suffix = result_resource_suffix(selection, template)
        if result_suffix in seen_result_suffixes:
            errors.append(
                {
                    "code": "duplicate_interactive_result_resource",
                    "template_id": template_id,
                    "result_resource_suffix": result_suffix,
                    "message": "Selected interactive object result resources must be unique.",
                }
            )
        seen_result_suffixes.add(result_suffix)

        for field_name in template.get("required_fields") or []:
            if not clean_text(selection.get(field_name)):
                errors.append(
                    {
                        "code": "missing_interactive_field",
                        "template_id": template_id,
                        "field": field_name,
                        "message": f"{field_name} is required for {template_id}.",
                    }
                )

        for field_name, expected_count in (template.get("list_fields") or {}).items():
            validate_list_field(selection, template, str(field_name), int(expected_count), errors)

        if template_id == "exchanger":
            source_mode = clean_text(selection.get("source_mode") or "generator")
            if source_mode not in {"generator", "gr"}:
                errors.append(
                    {
                        "code": "invalid_exchanger_source_mode",
                        "template_id": template_id,
                        "source_mode": source_mode,
                        "message": "Exchanger source_mode must be generator or gr.",
                    }
                )

    return {
        "summary": {
            "selected_count": count,
            "objects_found": len(objects),
            "errors": len(errors),
            "warnings": len(warnings),
        },
        "objects": objects,
        "errors": errors,
        "warnings": warnings,
    }


def validate_manifest_file(path: Path, templates_path: Path = DEFAULT_TEMPLATES_PATH) -> dict[str, Any]:
    return validate_manifest(read_json(path), load_templates(templates_path))


def result_resource_suffix(selection: dict[str, Any], template: dict[str, Any]) -> str:
    suffix = clean_text(template.get("result_resource_suffix"))
    default_prefix = clean_text(template.get("mechanic_prefix"))
    mechanic_prefix = clean_text(selection.get("mechanic_prefix")) or default_prefix
    if suffix.startswith(default_prefix):
        return mechanic_prefix + suffix[len(default_prefix):]
    return suffix


def result_resource_classname(campaign_id: str, selection: dict[str, Any], template: dict[str, Any]) -> str:
    return f"{campaign_id}_{result_resource_suffix(selection, template)}"


def result_resource_title(selection: dict[str, Any], template: dict[str, Any]) -> str:
    title_field = clean_text(template.get("result_title_field"))
    return first_non_empty(
        selection.get("result_resource_title"),
        selection.get(title_field) if title_field else "",
        template.get("display_name_ru"),
    )


def recipe_ingredients_from_manifest(
    campaign_id: str,
    manifest: dict[str, Any],
    templates_data: dict[str, Any] | None = None,
) -> tuple[list[InteractiveIngredient], dict[str, Any]]:
    templates_data = templates_data or load_templates()
    validation = validate_manifest(manifest, templates_data)
    templates = templates_data["templates"]
    ingredients: list[InteractiveIngredient] = []
    for selection in validation["objects"]:
        template = templates.get(selection.get("template_id"))
        if template is None:
            continue
        title = result_resource_title(selection, template)
        ingredients.append(
            InteractiveIngredient(
                template_id=str(selection["template_id"]),
                classname=result_resource_classname(campaign_id, selection, template),
                title=title,
                object_id=str(selection.get("object_id") or selection.get("template_id")),
                amount=1,
            )
        )
    return ingredients, validation


def recipe_ingredients_from_file(
    campaign_id: str,
    manifest_path: Path,
    templates_path: Path = DEFAULT_TEMPLATES_PATH,
) -> tuple[list[InteractiveIngredient], dict[str, Any]]:
    return recipe_ingredients_from_manifest(campaign_id, read_json(manifest_path), load_templates(templates_path))


def template_object_prefix(campaign_id: str, mechanic_prefix: str) -> str:
    return f"{campaign_id}_{mechanic_prefix}"


def output_path(*parts: str) -> str:
    return "/" + "/".join(part.strip("/") for part in parts if part)


def block(rows: list[list[Any]], title_row: list[Any], types_row: list[Any], headers_row: list[Any], data_rows: list[list[Any]]) -> None:
    if not data_rows:
        return
    width = max(len(title_row), len(types_row), len(headers_row), *(len(row) for row in data_rows))
    rows.append(fit_row(title_row, width))
    rows.append(fit_row(types_row, width))
    rows.append(fit_row(headers_row, width))
    rows.extend(fit_row(row, width) for row in data_rows)
    rows.append([])


def fit_row(row: list[Any], width: int) -> list[Any]:
    fitted = list(row[:width])
    if len(fitted) < width:
        fitted.extend([""] * (width - len(fitted)))
    return fitted


def chest_rows(campaign_id: str, selection: dict[str, Any]) -> list[list[Any]]:
    prefix = template_object_prefix(campaign_id, clean_text(selection.get("mechanic_prefix")) or "Chest_1")
    guest = f"{prefix}_Guest"
    home = f"{prefix}_Home"
    gr = f"{prefix}_GR_1"
    result = f"{prefix}_R_1"
    object_title = clean_text(selection.get("object_title"))
    activation_title = clean_text(selection.get("activation_resource_title"))
    result_title = clean_text(selection.get("result_resource_title"))
    description_window = first_non_empty(
        selection.get("description_window"),
        f"Положи {accusative(activation_title)} в {accusative(object_title)}, чтобы получить {accusative(result_title)}",
    )
    reward_description = first_non_empty(
        selection.get("reward_description"),
        f"Собирай {accusative(result_title)}, кликая на {accusative(object_title)} дома и в гостях.",
    )
    instruction_title = clean_text(selection.get("instruction_title"))

    object_types = ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "int"]
    object_headers = [
        "",
        "input",
        "output",
        "classname",
        "title",
        "action_availability_conditions",
        "open_price",
        "extra.description_window",
        "extra.reward_description",
        "extra.instruction_title",
        "extra.tile_till_window",
        "extra.open_btn_window",
        "extra.open_now_btn_window",
        "id",
    ]
    object_row_common = [
        object_title,
        f"stuff={home}",
        f"asset={gr}:3",
        description_window,
        reward_description,
        instruction_title,
        "Можно получить через:",
        "Получить",
        "Получить сейчас за {price}",
        "",
    ]

    rows: list[list[Any]] = []
    block(
        rows,
        ["", "ОБЪЕКТ Chest_Guest"],
        object_types,
        object_headers,
        [
            [
                "",
                "/chest/Dacha_2025/Dacha_2025_Chest_1_Guest.proto.js",
                output_path("chest", "Fun", campaign_id, f"{guest}.proto.js"),
                guest,
                *object_row_common,
            ]
        ],
    )
    block(
        rows,
        ["", "ОБЪЕКТ Chest_Home"],
        object_types,
        object_headers,
        [
            [
                "",
                "/chest/Dacha_2025/Dacha_2025_Chest_1_Home.proto.js",
                output_path("chest", "Fun", campaign_id, f"{home}.proto.js"),
                home,
                *object_row_common,
            ]
        ],
    )
    block(
        rows,
        ["", "АССЕТЫ Ресурсов"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "title", "description", "meta_info", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun10/Fun10_Chest_1_GR_1.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{gr}.proto.js"),
                gr,
                activation_title,
                ensure_period(clean_text(selection.get("activation_resource_description"))),
                f"pack_asset={gr}_Package",
                "",
            ],
            [
                "",
                "/quest_item/Fun/Fun10/Fun10_Chest_1_CL_1.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{result}.proto.js"),
                result,
                result_title,
                ensure_period(first_non_empty(selection.get("result_resource_description"), f"Можно получить из {object_title} дома или в гостях")),
                "",
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "ПАКЕТЫ ДЛЯ ПРОДАЖИ"],
        ["temp_01", "string", "string", "string", "ignore", "string", "string", "int", "ignore", "string", "int"],
        ["", "input", "output", "classname", "asset", "title", "reward", "price", "Количество ассетов", "stuff_icon", "id"],
        [
            [
                "",
                "/asset_package/Fun/Fun10/Fun10_Chest_1_GR_1_Package.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{gr}_Package.proto.js"),
                f"{gr}_Package",
                gr,
                activation_title,
                f"asset={gr}:3",
                "4",
                "3",
                gr,
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "СПОСОБ ВЫПАДЕНИЯ GR"],
        ["temp_01", "string", "string", "ignore", "array", "array", "int", "string", "string", "int"],
        ["", "input", "output", "file_name", "actions", "location_tags", "rand_reward.p", "rand_reward.asset", "conditions", "id"],
        [
            [
                "",
                "/global_reward/Fun11/Fun11_Chest_1_GR_1.proto.js",
                output_path("global_reward", campaign_id, f"{gr}.proto.js"),
                gr,
                "clean_garbage_in_guest",
                clean_text(selection.get("location_tags")) or "lawn",
                "40",
                gr,
                f"stuff={home}",
                "",
            ]
        ],
    )
    return rows


def help_rows(campaign_id: str, selection: dict[str, Any]) -> list[list[Any]]:
    prefix = template_object_prefix(campaign_id, clean_text(selection.get("mechanic_prefix")) or "HELP_1")
    home = f"{prefix}_Home"
    guest = f"{prefix}_Guest"
    result = f"{prefix}_R_Opener"
    path = f"{prefix}_R_OpenerPath"
    ask = f"{prefix}_ASK_Open_1"
    object_title = clean_text(selection.get("object_title"))
    path_title = clean_text(selection.get("path_resource_title"))
    result_title = clean_text(selection.get("result_resource_title"))
    activation_title = clean_text(selection.get("activation_resource_title"))

    rows: list[list[Any]] = []
    block(
        rows,
        ["", "ОБЪЕКТ HELP_1_Home"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "int"],
        [
            "",
            "input",
            "output",
            "classname",
            "title",
            "open_price",
            "extra.window_spec.view_window",
            "extra.window_spec.main_asset",
            "extra.window_spec.mark_1",
            "extra.window_spec.mark_2",
            "extra.window_spec.comment_1",
            "extra.window_spec.comment_2",
            "extra.window_spec.comment_3",
            "extra.window_spec.comment_4",
            "extra.window_spec.comment_4",
            "id",
        ],
        [
            [
                "",
                "/chest/Veles_2024/Veles_2024_Chest_2_Home.proto.js",
                output_path("chest", "Fun", campaign_id, f"{home}.proto.js"),
                home,
                object_title,
                f"asset={ask}:10",
                f"{prefix}_Window",
                result,
                clean_text(selection.get("mark_1")) or "Дары",
                clean_text(selection.get("mark_2")) or "Обереги",
                clean_text(selection.get("help_comment")),
                clean_text(selection.get("activation_comment")),
                clean_text(selection.get("active_state_comment")),
                clean_text(selection.get("activate_button_title")) or "Активировать",
                clean_text(selection.get("activate_window_title")) or "Активируй объект",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "ОБЪЕКТ HELP_1_Guest"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "string", "int", "int"],
        [
            "",
            "input",
            "output",
            "classname",
            "title",
            "stuff_icon",
            "behaviour.1.chest",
            "behaviour.1.conditions_title",
            "rand_reward.asset",
            "rand_reward_in_guest.asset",
            "daily_help_limit",
            "id",
        ],
        [
            [
                "",
                "/furniture/Veles_2024/Veles_2024_Stuff_2_Guest.proto.js",
                output_path("furniture", "Fun", campaign_id, f"{guest}.proto.js"),
                guest,
                object_title,
                f"{guest}_StuffIcon",
                home,
                clean_text(selection.get("guest_conditions_title")),
                path,
                path,
                "5",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "АССЕТЫ Ресурсов HELP"],
        ["temp_01", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "title", "meta_info", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun10/Fun10_FunCollection_2_HELP_1_R_OpenerPath.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{path}.proto.js"),
                path,
                path_title,
                f"pack_asset={path}_Package",
                "",
            ],
            [
                "",
                "/quest_item/Fun/Fun10/Fun10_FunCollection_2_HELP_1_R_Opener.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{result}.proto.js"),
                result,
                result_title,
                f"pack_asset={result}_Package",
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "АССЕТЫ Ресурсов ASK"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun10/resource/Fun10_ASK_1.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{ask}.proto.js"),
                ask,
                ask,
                activation_title,
                "Попроси у друзей или купи.",
                f"pack_asset={ask}_Package",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "ПОСТЭКШЕНЫ ASK и PER"],
        ["temp_01", "string", "string", "string", "string", "string", "int", "int", "int", "int"],
        ["", "input", "output", "identifier", "title", "poster_reward", "clicks_limit", "life_time", "send_interval", "id"],
        [
            [
                "",
                "/post_action/ask_for_Fun10_ASK_10.proto.js",
                output_path("post_action", f"ask_for_{ask}.proto.js"),
                f"ask_for_{ask}",
                activation_title,
                f"asset={ask}:1",
                "5",
                "43200",
                "7200",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "ПАКЕТЫ ДЛЯ ПРОДАЖИ"],
        ["temp_01", "string", "string", "string", "ignore", "string", "string", "int", "ignore", "string", "int"],
        ["", "input", "output", "classname", "asset", "title", "reward", "price", "Количество ассетов", "stuff_icon", "id"],
        [
            [
                "",
                "/asset_package/Fun/Fun10/Fun10_FunCollection_2_HELP_1_R_OpenerPath_Package.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{path}_Package.proto.js"),
                f"{path}_Package",
                path,
                path_title,
                f"asset={path}:3",
                "3",
                "1",
                path,
                "",
            ],
            [
                "",
                "/asset_package/Fun/Fun10/Fun10_FunCollection_2_HELP_1_R_Opener_Package.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{result}_Package.proto.js"),
                f"{result}_Package",
                result,
                result_title,
                f"asset={result}:15",
                "15",
                "1",
                result,
                "",
            ],
            [
                "",
                "/asset_package/Fun/Fun10/resource/Fun10_ASK_1_Package.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{ask}_Package.proto.js"),
                f"{ask}_Package",
                ask,
                activation_title,
                f"asset={ask}:2",
                "2",
                "1",
                ask,
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "РЕЦЕПТ HELP_R_Opener"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "identifier", "reward", "tags.2", "ingredients", "id"],
        [
            [
                "",
                "/recipe/Fun/Fun10/Fun10_FunCollection_2_HELP_1_R_Opener_Recipe.proto.js",
                output_path("recipe", "Fun", campaign_id, f"{result}_Recipe.proto.js"),
                f"{result}_Recipe",
                f"asset={result}:1",
                campaign_id,
                f"asset={path}:5",
                "",
            ]
        ],
    )
    return rows


def friend_action_rows(campaign_id: str, selection: dict[str, Any]) -> list[list[Any]]:
    mechanic_prefix = clean_text(selection.get("mechanic_prefix")) or "Story_FriendAction_1"
    action = f"{campaign_id}_{mechanic_prefix}"
    available = f"{action}_Available"
    resource_prefix = clean_text(selection.get("resource_prefix")) or "Story_FA"
    reward_for_action = f"{campaign_id}_{resource_prefix}_1"
    reward_on_receive = f"{campaign_id}_{resource_prefix}_2"

    available_title = clean_text(selection.get("available_title"))
    action_title = clean_text(selection.get("action_title"))
    reward_for_action_title = clean_text(selection.get("reward_for_action_title"))
    reward_on_receive_title = clean_text(selection.get("reward_on_receive_title"))
    action_start_time = clean_text(selection.get("action_start_time"))
    action_end_time = clean_text(selection.get("action_end_time"))
    viewer_conditions = first_non_empty(
        selection.get("viewer_conditions"),
        f"stuff={available}+time<{action_end_time}",
    )
    friend_conditions = first_non_empty(
        selection.get("friend_conditions"),
        f"stuff={available}+time<{action_end_time}",
    )
    bot_conditions = first_non_empty(
        selection.get("bot_conditions"),
        f"time>{action_start_time}+time<{action_end_time}",
    )

    rows: list[list[Any]] = []
    block(
        rows,
        ["", "ОБЪЕКТ доступности Story_FriendAction_1_Available"],
        ["temp_01", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "title", "id"],
        [
            [
                "",
                "/furniture/Fun/Fun12/Fun12_Story_FriendAction_1_Available.proto.js",
                output_path("furniture", "Fun", campaign_id, f"{available}.proto.js"),
                available,
                available_title,
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "ОБЪЕКТ Story_FriendAction_1"],
        ["temp_01", "string", "string", "string", "string", "int", "int", "string", "string", "string", "string", "string", "string", "string", "int"],
        [
            "",
            "input",
            "output",
            "classname",
            "title",
            "day_limit",
            "probability",
            "reward_for_action",
            "reward_on_receive",
            "viewer_conditions",
            "friend_conditions",
            "bot_conditions",
            "extra.wall_block_title_success",
            "extra.wall_block_title_not_success",
            "id",
        ],
        [
            [
                "",
                "/friend_action/Fun12_Story_FriendAction_1.proto.js",
                output_path("friend_action", f"{action}.proto.js"),
                action,
                action_title,
                clean_text(selection.get("day_limit")) or "1",
                clean_text(selection.get("probability")) or "65",
                f"asset={reward_for_action}:{clean_text(selection.get('reward_for_action_amount')) or '1'}",
                f"asset={reward_on_receive}:{clean_text(selection.get('reward_on_receive_amount')) or '1'}",
                viewer_conditions,
                friend_conditions,
                bot_conditions,
                clean_text(selection.get("wall_block_title_success")),
                clean_text(selection.get("wall_block_title_not_success")),
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "АССЕТЫ ресурсов Story_FriendAction_1"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "title", "description", "meta_info", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun12/Fun12_Story_FA_1.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{reward_for_action}.proto.js"),
                reward_for_action,
                reward_for_action_title,
                ensure_period(clean_text(selection.get("reward_for_action_description"))),
                f"pack_asset={reward_for_action}_Package",
                "",
            ],
            [
                "",
                "/quest_item/Fun/Fun12/Fun12_Story_FA_2.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{reward_on_receive}.proto.js"),
                reward_on_receive,
                reward_on_receive_title,
                ensure_period(clean_text(selection.get("reward_on_receive_description"))),
                f"pack_asset={reward_on_receive}_Package",
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "ПАКЕТЫ продажи ресурсов Story_FriendAction_1"],
        ["temp_01", "string", "string", "string", "string", "string", "int", "ignore", "string", "int"],
        ["", "input", "output", "classname", "title", "reward", "price", "Количество ассетов", "stuff_icon", "id"],
        [
            [
                "",
                "/asset_package/Fun/Fun12/Fun12_Story_FA_1.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{reward_for_action}_Package.proto.js"),
                f"{reward_for_action}_Package",
                reward_for_action_title,
                f"asset={reward_for_action}:{clean_text(selection.get('package_amount')) or '3'}",
                clean_text(selection.get("package_price")) or "2",
                clean_text(selection.get("package_amount")) or "3",
                reward_for_action,
                "",
            ],
            [
                "",
                "/asset_package/Fun/Fun12/Fun12_Story_FA_2.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{reward_on_receive}_Package.proto.js"),
                f"{reward_on_receive}_Package",
                reward_on_receive_title,
                f"asset={reward_on_receive}:{clean_text(selection.get('package_amount')) or '3'}",
                clean_text(selection.get("package_price")) or "2",
                clean_text(selection.get("package_amount")) or "3",
                reward_on_receive,
                "",
            ],
        ],
    )
    return rows


def exchanger_rows(campaign_id: str, selection: dict[str, Any]) -> list[list[Any]]:
    mechanic_prefix = clean_text(selection.get("mechanic_prefix")) or "Exchanger"
    exchanger = f"{campaign_id}_{mechanic_prefix}"
    result = f"{campaign_id}_{mechanic_prefix}_R_1"
    source_mode = clean_text(selection.get("source_mode")) or "generator"
    exchanger_title = clean_text(selection.get("exchanger_title"))
    location_title = clean_text(selection.get("location_title"))
    generator_base_title = clean_text(selection.get("generator_base_title"))
    part_group_title = clean_text(selection.get("part_group_title")) or "Детали"
    part_titles = [clean_text(value) for value in as_list(selection.get("part_resource_titles"))]
    generator_titles = [clean_text(value) for value in as_list(selection.get("generator_titles"))]
    result_title = clean_text(selection.get("result_resource_title"))

    rg_classnames = [f"{campaign_id}_{mechanic_prefix}_RG_{index}" for index in range(1, 6)]
    generator_classnames = [f"{campaign_id}_{mechanic_prefix}_Generator_{index}" for index in range(1, 6)]
    rows: list[list[Any]] = []

    if source_mode == "generator":
        block(
            rows,
            ["", "ОБЪЕКТ Generator РЕСУРСОВ"],
            ["temp_01", "string", "string", "string", "string", "int"],
            ["", "input", "output", "classname", "title", "id"],
            [
                [
                    "",
                    f"/debris/Fun/Fun10/Fun10_Exchanger_Generator_{index}.proto.js",
                    output_path("debris", "Fun", campaign_id, f"{generator_classnames[index - 1]}.proto.js"),
                    generator_classnames[index - 1],
                    generator_titles[index - 1],
                    "",
                ]
                for index in range(1, 6)
            ],
        )

    block(
        rows,
        ["", "ОБЪЕКТ Exchanger"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "string", "string", "int"],
        [
            "",
            "input",
            "output",
            "classname",
            "title",
            "extra.hint_add_to_exchange",
            "extra.hint_get_asset",
            "behaviour.title_mark_workbencg",
            "behaviour.ingredient_description",
            "behaviour.description_1",
            "behaviour.description_2",
            "id",
        ],
        [
            [
                "",
                "/furniture/Fun/Fun10/Fun10_Exchanger.proto.js",
                output_path("furniture", "Fun", campaign_id, f"{exchanger}.proto.js"),
                exchanger,
                exchanger_title,
                first_non_empty(
                    selection.get("hint_add_to_exchange"),
                    f"Нажми на {exchanger_title} в {location_title} и выбери вкладку \"Обмен с друзьями\". Выбери ресурс, который хочешь обменять, и нажми \"Сохранить\".",
                ),
                first_non_empty(
                    selection.get("hint_get_asset"),
                    f"Бери {part_group_title} из {generator_base_title} в {location_title}, чтобы найти.",
                ),
                first_non_empty(selection.get("workbench_title"), result_title),
                first_non_empty(selection.get("ingredient_description"), "Если тебе нужен {0}"),
                first_non_empty(
                    selection.get("description_1"),
                    f"Чтобы обменять {part_group_title}, собери его из {generator_base_title} в {location_title}.",
                ),
                first_non_empty(
                    selection.get("description_2"),
                    f"Чтобы получить {result_title}, нужны все 5 видов ресурса. Один вид можно добыть самостоятельно, остальные обменивай у друзей или покупай.",
                ),
                "",
            ]
        ],
    )
    asset_rows = []
    for index, classname in enumerate(rg_classnames, start=1):
        source_title = generator_titles[index - 1] if source_mode == "generator" else "GR-источника"
        asset_rows.append(
            [
                "",
                f"/quest_item/Fun/Fun10/Fun10_Exchanger_RG_{index}.proto.js",
                output_path("quest_item", "Fun", campaign_id, f"{classname}.proto.js"),
                classname,
                part_titles[index - 1],
                first_non_empty(
                    selection.get(f"part_resource_description_{index}"),
                    f"Можно получить из {source_title} дома.",
                ),
                f"pack_asset={classname}_Package",
                "",
            ]
        )
    asset_rows.append(
        [
            "",
            "/quest_item/Fun/Fun10/Fun10_Exchanger_R_1.proto.js",
            output_path("quest_item", "Fun", campaign_id, f"{result}.proto.js"),
            result,
            result_title,
            ensure_period(clean_text(selection.get("result_resource_description"))),
            f"pack_asset={result}_Package",
            "",
        ]
    )
    block(
        rows,
        ["", "АССЕТ Generator и Exchanger"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "title", "description", "meta_info", "id"],
        asset_rows,
    )
    block(
        rows,
        ["", "РЕЦПТ Exchanger"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "identifier", "reward", "ingredients", "conditions", "id"],
        [
            [
                "",
                "/recipe/Fun/Fun10/Fun10_Exchanger_R_1_Recipe.proto.js",
                output_path("recipe", "Fun", campaign_id, f"{result}_Recipe.proto.js"),
                f"{result}_Recipe",
                f"asset={result}:1",
                "+".join(f"asset={classname}:4" for classname in rg_classnames),
                f"stuff={exchanger}",
                "",
            ]
        ],
    )
    package_rows = []
    for index, classname in enumerate(rg_classnames, start=1):
        package_rows.append(
            [
                "",
                f"/asset_package/Fun/Fun10/Fun10_Exchanger_RG_{index}_Package.proto.js",
                output_path("asset_package", "Fun", campaign_id, f"{classname}_Package.proto.js"),
                f"{classname}_Package",
                classname,
                part_titles[index - 1],
                f"asset={classname}:4",
                "3",
                "4",
                classname,
                "",
            ]
        )
    package_rows.append(
        [
            "",
            "/asset_package/Fun/Fun10/Fun10_Exchanger_R_1_Package.proto.js",
            output_path("asset_package", "Fun", campaign_id, f"{result}_Package.proto.js"),
            f"{result}_Package",
            result,
            result_title,
            f"asset={result}:1",
            "15",
            "1",
            result,
            "",
        ]
    )
    block(
        rows,
        ["", "ПАКЕТЫ ПРОДАЖИ РЕСУРСОВ Generator и Exchanger"],
        ["temp_01", "string", "string", "string", "ignore", "string", "string", "int", "ignore", "string", "int"],
        ["", "input", "output", "classname", "asset", "title", "reward", "price", "Количество ассетов", "stuff_icon", "id"],
        package_rows,
    )
    return rows


def mixer_rows(campaign_id: str, selection: dict[str, Any]) -> list[list[Any]]:
    mechanic_prefix = clean_text(selection.get("mechanic_prefix")) or "Mixer_1"
    mixer = template_object_prefix(campaign_id, mechanic_prefix)
    gr_1 = f"{mixer}_GR_1"
    gr_2 = f"{mixer}_GR_2"
    ask = f"{mixer}_ASK_1"
    result = f"{mixer}_R_1"
    object_title = clean_text(selection.get("object_title"))
    ingredient_a_title = clean_text(selection.get("ingredient_a_title"))
    ingredient_b_title = clean_text(selection.get("ingredient_b_title"))
    ask_title = clean_text(selection.get("ask_resource_title"))
    result_title = clean_text(selection.get("result_resource_title"))
    tech_quest = clean_text(selection.get("tech_quest")) or f"{campaign_id}_Tech_Weekly_2"
    active_condition = f"active_quest={tech_quest}" if tech_quest else ""
    right_open_price = (
        f"asset={gr_1}:{clean_text(selection.get('open_amount_a')) or '5'}"
        f"+asset={gr_2}:{clean_text(selection.get('open_amount_b')) or '7'}"
        f"+asset={ask}:{clean_text(selection.get('open_amount_ask')) or '3'}"
    )
    wrong_open_price = (
        f"asset={gr_1}:{clean_text(selection.get('wrong_amount_a')) or '1'}"
        f"+asset={gr_2}:{clean_text(selection.get('wrong_amount_b')) or '1'}"
        f"+asset={ask}:{clean_text(selection.get('wrong_amount_ask')) or '1'}"
    )

    rows: list[list[Any]] = []
    block(
        rows,
        ["", "Mixer object"],
        ["temp_01", "string", "string", "string", "string", "replace", "", "int", "int"],
        ["", "input", "output", "classname", "title", "find", "replace", "limit", "id"],
        [
            [
                "",
                "/furniture/NY24/NY24_Mixer_1.proto.js",
                output_path("furniture", "Fun", campaign_id, f"{mixer}.proto.js"),
                mixer,
                object_title,
                "NY24_Mixer_1",
                mixer,
                clean_text(selection.get("object_limit")) or "8",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "Mixer resources GR"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "replace", "", "int"],
        ["", "input", "output", "classname", "title", "description", "meta_info", "find", "replace", "id"],
        [
            [
                "",
                "/quest_item/Fun12/Fun12_GR_10.proto.js",
                output_path("quest_item", campaign_id, f"{gr_1}.proto.js"),
                gr_1,
                ingredient_a_title,
                ensure_period(clean_text(selection.get("ingredient_a_description"))),
                f"pack_asset={gr_1}_Package",
                "NY24",
                campaign_id,
                "",
            ],
            [
                "",
                "/quest_item/Fun12/Fun12_GR_10.proto.js",
                output_path("quest_item", campaign_id, f"{gr_2}.proto.js"),
                gr_2,
                ingredient_b_title,
                ensure_period(clean_text(selection.get("ingredient_b_description"))),
                f"pack_asset={gr_2}_Package",
                "NY24",
                campaign_id,
                "",
            ],
            [
                "",
                "/quest_item/Fun12/NY24_Mixer_R_1.proto.js",
                output_path("quest_item", campaign_id, f"{result}.proto.js"),
                result,
                result_title,
                ensure_period(clean_text(selection.get("result_resource_description"))),
                f"pack_asset={result}",
                "NY24",
                campaign_id,
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "Mixer global rewards"],
        ["temp_01", "string", "string", "ignore", "array", "array", "int", "string", "string", "array", "array", "replace", "", "int"],
        ["", "input", "output", "file_name", "actions", "location_tags", "rand_reward.p", "rand_reward.asset", "conditions", "assets", "assets.2", "find", "replace", "id"],
        [
            [
                "",
                "/global_reward/Fun11/Fun11_FunCollection_2_CL_1.proto.js",
                output_path("global_reward", campaign_id, f"{gr_1}.proto.js"),
                gr_1,
                clean_text(selection.get("source_action_a")) or "clean_garbage",
                clean_text(selection.get("location_tag_a")),
                clean_text(selection.get("drop_probability_a")) or "30",
                gr_1,
                active_condition,
                clean_text(selection.get("assets_a")),
                clean_text(selection.get("assets_a_2")),
                "Fun11",
                campaign_id,
                "",
            ],
            [
                "",
                "/global_reward/Fun11/Fun11_FunCollection_2_CL_1.proto.js",
                output_path("global_reward", campaign_id, f"{gr_2}.proto.js"),
                gr_2,
                clean_text(selection.get("source_action_b")) or "take_crop_in_guest",
                clean_text(selection.get("location_tag_b")),
                clean_text(selection.get("drop_probability_b")) or "40",
                gr_2,
                active_condition,
                clean_text(selection.get("assets_b")),
                clean_text(selection.get("assets_b_2")),
                "Fun11",
                campaign_id,
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "Mixer resources ASK"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "id"],
        [
            [
                "",
                "/quest_item/Fun12/Fun12_ASK_1.proto.js",
                output_path("quest_item", campaign_id, f"{ask}.proto.js"),
                ask,
                ask,
                ask_title,
                ensure_period(clean_text(selection.get("ask_resource_description"))),
                f"pack_asset={ask}",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "Post action ASK Mixer"],
        ["temp_01", "string", "string", "string", "ignore", "string", "string", "int", "int", "int", "int"],
        ["", "input", "output", "identifier", "classname", "title", "poster_reward", "clicks_limit", "life_time", "send_interval", "id"],
        [
            [
                "",
                "/post_action/ask_for_Fun10_ASK_10.proto.js",
                output_path("post_action", f"{ask}.proto.js"),
                ask,
                ask,
                ask_title,
                f"asset={ask}:1",
                clean_text(selection.get("ask_clicks_limit")) or "5",
                clean_text(selection.get("ask_life_time")) or "43200",
                clean_text(selection.get("ask_send_interval")) or "7200",
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "Mixer packages"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "int", "int"],
        ["", "input", "output", "classname", "title", "stuff_icon", "reward", "price", "id"],
        [
            [
                "",
                "/asset_package/Fun/Fun10/resource/Fun10_GR_10_Package.proto.js",
                output_path("asset_package", "HeavenlyExotic", f"{ask}_Package.proto.js"),
                f"{ask}_Package",
                ask_title,
                ask,
                f"asset={ask}:{clean_text(selection.get('ask_package_amount')) or '1'}",
                clean_text(selection.get("ask_package_price")) or "3",
                "",
            ],
            [
                "",
                "/asset_package/Fun/Fun10/resource/Fun10_GR_10_Package.proto.js",
                output_path("asset_package", "HeavenlyExotic", f"{gr_1}_Package.proto.js"),
                f"{gr_1}_Package",
                ingredient_a_title,
                gr_1,
                f"asset={gr_1}:{clean_text(selection.get('ingredient_package_amount')) or '2'}",
                clean_text(selection.get("ingredient_package_price")) or "5",
                "",
            ],
            [
                "",
                "/asset_package/Fun/Fun10/resource/Fun10_GR_10_Package.proto.js",
                output_path("asset_package", "HeavenlyExotic", f"{gr_2}_Package.proto.js"),
                f"{gr_2}_Package",
                ingredient_b_title,
                gr_2,
                f"asset={gr_2}:{clean_text(selection.get('ingredient_package_amount')) or '2'}",
                clean_text(selection.get("ingredient_package_price")) or "5",
                "",
            ],
        ],
    )
    block(
        rows,
        ["", "right_action Mixer"],
        ["sl", "string", "string", "string", "string", "replace", "", "replace", "", "string", "int"],
        ["", "input", "output", "identifier", "conditions", "find", "replace", "find", "replace", "open_price", "id"],
        [
            [
                "",
                "/quest_action/NY24/action_NY24_Mixer_1_Right.proto.js",
                output_path("quest_action", "Fun", campaign_id, f"action_{mixer}_Right.proto.js"),
                f"action_{mixer}_Right",
                f"stuff={mixer}",
                "NY24_Mixer_1",
                mixer,
                "NY24_Mixer_R_1",
                result,
                right_open_price,
                "",
            ]
        ],
    )
    block(
        rows,
        ["", "wrong_action Mixer"],
        ["sl", "string", "string", "string", "string", "replace", "", "string", "int"],
        ["", "input", "output", "identifier", "conditions", "find", "replace", "open_price", "id"],
        [
            [
                "",
                "/quest_action/NY24/action_NY24_Mixer_1_Wrong.proto.js",
                output_path("quest_action", "Fun", campaign_id, f"action_{mixer}_Wrong.proto.js"),
                f"action_{mixer}_Wrong",
                f"stuff={mixer}",
                "NY24_Mixer_1",
                mixer,
                wrong_open_price,
                "",
            ]
        ],
    )
    for suffix, default_price in (("Hint2", "money_crown=20"), ("Hint3", "money_crown=30")):
        block(
            rows,
            ["", f"action_{suffix} Mixer"],
            ["sl", "string", "string", "string", "string", "replace", "", "string", "int"],
            ["", "input", "output", "identifier", "open_price", "find", "replace", "conditions", "id"],
            [
                [
                    "",
                    f"/quest_action/NY24/action_NY24_Mixer_1_{suffix}.proto.js",
                    output_path("quest_action", "Fun", campaign_id, f"action_{mixer}_{suffix}.proto.js"),
                    f"action_{mixer}_{suffix}",
                    clean_text(selection.get(f"{suffix.lower()}_open_price")) or default_price,
                    "NY24_Mixer_1",
                    mixer,
                    "",
                    "",
                ]
            ],
        )
    return rows


BUILDERS = {
    "chest_1": chest_rows,
    "help_1": help_rows,
    "friend_action_1": friend_action_rows,
    "exchanger": exchanger_rows,
    "mixer_1": mixer_rows,
}


def build_rows_for_selection(campaign_id: str, selection: dict[str, Any]) -> list[list[Any]]:
    builder = BUILDERS.get(str(selection.get("template_id")))
    if builder is None:
        raise ValueError(f"unsupported interactive object template: {selection.get('template_id')}")
    rows = builder(campaign_id, selection)
    if rows and rows[-1] == []:
        rows.pop()
    return rows


def render_preview(campaign_id: str, pack_id: str, validation: dict[str, Any], templates_data: dict[str, Any]) -> str:
    templates = templates_data["templates"]
    lines = [
        "# Interactive Objects",
        "",
        f"Campaign: {campaign_id}",
        f"Pack: {pack_id}",
        f"Selected count: {validation['summary']['selected_count']}",
        f"Errors: {validation['summary']['errors']}",
        "",
        "## Selected",
        "",
    ]
    for selection in validation["objects"]:
        template = templates.get(selection.get("template_id")) or {}
        result = result_resource_classname(campaign_id, selection, template) if template else ""
        title = result_resource_title(selection, template) if template else ""
        lines.append(f"- `{selection.get('template_id')}` -> `{result}`: {title}")

    if validation["errors"]:
        lines.extend(["", "## Errors", ""])
        for item in validation["errors"]:
            lines.append(f"- `{item['code']}`: {item['message']}")
    lines.append("")
    return "\n".join(lines)


def write_preview(
    campaign_id: str,
    pack_id: str,
    manifest_path: Path,
    preview_path: Path,
    templates_path: Path = DEFAULT_TEMPLATES_PATH,
) -> dict[str, Any]:
    templates_data = load_templates(templates_path)
    validation = validate_manifest(read_json(manifest_path), templates_data)
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    preview_path.write_text(render_preview(campaign_id, pack_id, validation, templates_data), encoding="utf-8")
    return validation


def default_manifest(template_ids: list[str]) -> dict[str, Any]:
    return {
        "version": 1,
        "selected_objects": [{"template_id": template_id} for template_id in template_ids],
    }


def build_interactive_objects_files(
    campaign_id: str,
    pack_id: str,
    manifest_path: Path,
    output_dir: Path,
    summary_path: Path | None = None,
    templates_path: Path = DEFAULT_TEMPLATES_PATH,
) -> dict[str, Any]:
    templates_data = load_templates(templates_path)
    manifest = read_json(manifest_path)
    validation = validate_manifest(manifest, templates_data)
    if validation["summary"]["errors"]:
        first = validation["errors"][0]
        raise ValueError(f"interactive_objects.json is invalid: {first['code']}: {first['message']}")

    files: list[dict[str, Any]] = []
    for selection in validation["objects"]:
        template_id = str(selection["template_id"])
        rows = build_rows_for_selection(campaign_id, selection)
        output_csv = output_dir / f"generated_interactive_objects_{safe_filename(selection['object_id'] or template_id)}.csv"
        write_csv(output_csv, rows)
        template = templates_data["templates"][template_id]
        files.append(
            {
                "template_id": template_id,
                "object_id": selection.get("object_id") or template_id,
                "result_resource": result_resource_classname(campaign_id, selection, template),
                "csv": str(output_csv),
                "rows": len(rows),
            }
        )

    summary = {
        "campaign_id": campaign_id,
        "pack_id": pack_id,
        "manifest": str(manifest_path),
        "selected_count": validation["summary"]["selected_count"],
        "files_written": files,
    }
    if summary_path is not None:
        write_json(summary_path, summary)
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and export selected interactive object CSV files.")
    parser.add_argument("--templates", type=Path, default=DEFAULT_TEMPLATES_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="List supported interactive object templates.")
    list_parser.set_defaults(command_name="list")

    validate_parser = subparsers.add_parser("validate", help="Validate interactive_objects.json.")
    validate_parser.add_argument("manifest", type=Path)
    validate_parser.add_argument("--campaign", default="")
    validate_parser.add_argument("--pack", default="")
    validate_parser.add_argument("--preview", type=Path, default=None)
    validate_parser.set_defaults(command_name="validate")

    export_parser = subparsers.add_parser("export", help="Export selected interactive object CSV files.")
    export_parser.add_argument("manifest", type=Path)
    export_parser.add_argument("--campaign", required=True)
    export_parser.add_argument("--pack", required=True)
    export_parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    export_parser.add_argument("--summary-json", type=Path, default=None)
    export_parser.set_defaults(command_name="export")

    args = parser.parse_args(argv)
    templates_data = load_templates(args.templates)

    if args.command_name == "list":
        for template_id, template in templates_data["templates"].items():
            pair = "paired" if template.get("paired") else "single"
            print(f"{template_id}: {template.get('display_name_ru') or template_id} ({pair})")
        return 0

    if args.command_name == "validate":
        validation = validate_manifest(read_json(args.manifest), templates_data)
        if args.preview:
            args.preview.parent.mkdir(parents=True, exist_ok=True)
            args.preview.write_text(
                render_preview(args.campaign, args.pack, validation, templates_data),
                encoding="utf-8",
            )
            print(f"preview written: {args.preview}")
        print(f"selected count: {validation['summary']['selected_count']}")
        print(f"errors: {validation['summary']['errors']}")
        for item in validation["errors"]:
            print(f"{item['code']}: {item['message']}")
        return 0 if validation["summary"]["errors"] == 0 else 2

    if args.command_name == "export":
        summary = build_interactive_objects_files(
            campaign_id=args.campaign,
            pack_id=args.pack,
            manifest_path=args.manifest,
            output_dir=args.output_dir,
            summary_path=args.summary_json,
            templates_path=args.templates,
        )
        print(f"interactive objects exported: {len(summary['files_written'])}")
        for item in summary["files_written"]:
            print(f"csv written: {item['csv']}")
        if args.summary_json:
            print(f"summary written: {args.summary_json}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
