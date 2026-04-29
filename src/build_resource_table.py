from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAMPAIGNS_DIR = PROJECT_ROOT / "campaigns"

RESOURCE_KINDS = ("ASK", "PER", "GR", "FG", "FA", "R")

BLOCK_TITLES = {
    "HOG",
    "GR ассет",
    "GR способы получения",
    "GR ПАКЕТЫ",
    "ASK",
    "ASK пост экшен",
    "ASK ПАКЕТЫ",
    "PER",
    "PER пост экшен",
    "PER ПАКЕТЫ",
    "FG АССЕТ",
    "FG МЕХАНИКА",
    "FG ПАКЕТЫ",
    "R ассет",
    "Рецепты 4 ингридиента",
    "FA ассет",
    "FA Пакеты",
}

STRICT_DESCRIPTIONS = {
    "ASK": "Попроси у друзей или купи.",
    "PER": "Отправь личные просьбы друзьям или купи.",
    "FG": "Получи в качестве бесплатного подарка от друзей или купи.",
}

PACKAGE_RULES = {
    "ASK": (1, 2),
    "PER": (1, 2),
    "FG": (10, 2),
    "FA": (2, 3),
    "GR": (1, 1),
}


@dataclass
class Resource:
    kind: str
    classname: str
    title: str
    quest_classname: str
    task_number: int | None
    task_type: str
    hint: str
    amount: int
    selected_candidate_id: str
    candidate: dict[str, Any] | None


@dataclass
class HogResource:
    classname: str
    title: str
    quest_classname: str
    task_number: int | None


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_csv(path: Path, rows: list[list[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="cp1251", newline="") as handle:
        writer = csv.writer(handle, delimiter=";", quotechar='"', lineterminator="\r\n")
        writer.writerows(rows)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def normalize_title(value: Any, kind: str | None = None) -> str:
    title = str(value or "").strip()
    stripped_prefix = ""
    replacements = [
        "Попроси у друзей ",
        "Получи ",
        "Создай ",
        "Найди ",
    ]
    for prefix in replacements:
        if title.startswith(prefix):
            stripped_prefix = prefix
            title = title[len(prefix):].strip()
            break
    if stripped_prefix == "Получи ":
        title = normalize_simple_accusative(title)
    if kind == "HOG" and title:
        title = title[:1].upper() + title[1:]
    return title


def normalize_simple_accusative(title: str) -> str:
    words = title.split()
    normalized: list[str] = []
    for index, word in enumerate(words):
        if word.endswith("ую"):
            normalized.append(f"{word[:-2]}ая")
        elif word.endswith("юю"):
            normalized.append(f"{word[:-2]}яя")
        elif index == len(words) - 1 and word.endswith("у"):
            normalized.append(f"{word[:-1]}а")
        else:
            normalized.append(word)
    return " ".join(normalized)


def ensure_period(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    return value if value[-1] in ".!?" else f"{value}."


def fit_row(row: list[Any], width: int) -> list[Any]:
    fitted = list(row[:width])
    if len(fitted) < width:
        fitted.extend([""] * (width - len(fitted)))
    return fitted


def parse_generated_classname(value: Any, campaign_id: str) -> tuple[str, int] | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(rf"{re.escape(campaign_id)}_(ASK|PER|GR|FG|FA|R)_(\d+)", value)
    if not match:
        return None
    return match.group(1), int(match.group(2))


def parse_hog_classname(value: Any, campaign_id: str) -> bool:
    return isinstance(value, str) and re.fullmatch(rf"{re.escape(campaign_id)}_HOG_\d+", value) is not None


def candidate_index(context_pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for quest in context_pack.get("quests", []):
        for task in quest.get("tasks", []):
            for candidate in task.get("candidates", []):
                candidate_id = candidate.get("candidate_id")
                if candidate_id:
                    result[str(candidate_id)] = candidate
    return result


def iter_pack_dirs(campaign_dir: Path, pack_ids: list[str] | None = None) -> list[Path]:
    if pack_ids:
        return [campaign_dir / pack_id for pack_id in pack_ids]
    return [path for path in sorted(campaign_dir.glob("pack_*")) if path.is_dir()]


def collect_resources(campaign_id: str, pack_dirs: list[Path]) -> tuple[list[HogResource], list[Resource], list[dict[str, Any]]]:
    hogs: list[HogResource] = []
    resources: list[Resource] = []
    warnings: list[dict[str, Any]] = []

    for pack_dir in pack_dirs:
        filled_tasks_path = pack_dir / "filled_tasks.json"
        context_pack_path = pack_dir / "context_pack.json"
        if not filled_tasks_path.exists():
            warnings.append({"pack": pack_dir.name, "warning": "filled_tasks.json not found"})
            continue
        if not context_pack_path.exists():
            warnings.append({"pack": pack_dir.name, "warning": "context_pack.json not found"})
            context_candidates: dict[str, dict[str, Any]] = {}
        else:
            context_candidates = candidate_index(read_json(context_pack_path))

        filled_tasks = read_json(filled_tasks_path)
        for quest in filled_tasks.get("quests", []):
            quest_classname = str(quest.get("classname_quests") or "")
            for task in quest.get("tasks", []):
                task_object = task.get("task_object") if isinstance(task.get("task_object"), dict) else task
                task_number = task.get("task_number") if isinstance(task.get("task_number"), int) else None

                hog_classname = task_object.get("param")
                if parse_hog_classname(hog_classname, campaign_id):
                    hogs.append(
                        HogResource(
                            classname=str(hog_classname),
                            title=normalize_title(task_object.get("title"), "HOG"),
                            quest_classname=quest_classname,
                            task_number=task_number,
                        )
                    )

                classname = task_object.get("classname")
                parsed = parse_generated_classname(classname, campaign_id)
                if not parsed:
                    continue
                kind, _ = parsed
                selected_candidate_id = str(task.get("selected_candidate_id") or "")
                resources.append(
                    Resource(
                        kind=kind,
                        classname=str(classname),
                        title=normalize_title(task_object.get("title"), kind),
                        quest_classname=quest_classname,
                        task_number=task_number,
                        task_type=str(task.get("task_type") or ""),
                        hint=str(task_object.get("hint") or ""),
                        amount=int(task_object.get("amount") or 1),
                        selected_candidate_id=selected_candidate_id,
                        candidate=context_candidates.get(selected_candidate_id),
                    )
                )

    return hogs, resources, warnings


def block(rows: list[list[Any]], title_row: list[Any], types_row: list[Any], headers_row: list[Any], data_rows: list[list[Any]]) -> None:
    if not data_rows:
        return
    width = max(len(types_row), len(headers_row))
    rows.append(fit_row(title_row, width))
    rows.append(fit_row(types_row, width))
    rows.append(fit_row(headers_row, width))
    rows.extend(fit_row(row, width) for row in data_rows)
    rows.append([])


def package_row(prefix: str, kind: str, resource: Resource) -> list[Any]:
    amount, price = PACKAGE_RULES[kind]
    package_classname = f"{resource.classname}_Package"
    return [
        "",
        package_input(kind),
        f"/asset_package/Fun/{prefix}/{package_classname}.proto.js",
        package_classname,
        resource.classname,
        resource.title,
        f"asset={resource.classname}:{amount}",
        str(amount),
        str(price),
        resource.classname,
        "",
    ]


def package_input(kind: str) -> str:
    if kind == "GR":
        return "/asset_package/Fun/Fun10/resource/Fun10_GR_10_Package.proto.js"
    if kind == "ASK":
        return "/asset_package/Fun/Fun10/resource/Fun10_ASK_1_Package.proto.js"
    if kind == "PER":
        return "/asset_package/Fun/Fun10/resource/Fun10_PER_1_Package.proto.js"
    return "/asset_package/Fun/Fun10/resource/Fun10_FG_1_Package.proto.js"


def gr_description(resource: Resource) -> str:
    if resource.hint:
        return ensure_period(resource.hint)
    candidate = resource.candidate or {}
    if candidate.get("flower_title"):
        return (
            f"Собирай цветы {candidate['flower_title']} в гостях, чтобы найти. "
            "Чтобы собрать растение, кликни на горшок с нужным растением в гостях у друга."
        )
    if candidate.get("garbage_title"):
        guest = "в гостях" if "guest" in resource.task_type else "дома"
        return f"Убирай мусор {candidate['garbage_title']} {guest}, чтобы найти."
    return ""


def gr_reward_action(resource: Resource) -> tuple[str, str, str]:
    candidate = resource.candidate or {}
    task_type = resource.task_type
    if "take_crop_in_guest" in task_type or candidate.get("domain") == "flower":
        return "take_crop_in_guest", "/global_reward/Fun10/Fun11_GR_10.proto.js", "30"
    if "in_guest" in task_type:
        return "clean_garbage_in_guest", "/global_reward/Fun10/Fun11_GR_10.proto.js", "40" if candidate.get("garbage_classname") else "50"
    return "clean_garbage", "/global_reward/Fun10/Fun11_GR_7.proto.js" if candidate.get("garbage_classname") else "/global_reward/Fun10/Fun11_GR_11.proto.js", "60" if candidate.get("garbage_classname") else "40"


def gr_assets(resource: Resource) -> str:
    candidate = resource.candidate or {}
    for key in ("flower_classname", "garbage_classname", "source_classname"):
        if candidate.get(key):
            return str(candidate[key])
    return ""


def recipe_rows(prefix: str, resources: list[Resource]) -> tuple[list[list[Any]], list[dict[str, Any]]]:
    result: list[list[Any]] = []
    warnings: list[dict[str, Any]] = []
    by_quest: dict[str, list[Resource]] = {}
    for resource in resources:
        by_quest.setdefault(resource.quest_classname, []).append(resource)

    for craft in [resource for resource in resources if resource.kind == "R"]:
        quest_resources = sorted(by_quest.get(craft.quest_classname, []), key=lambda item: item.task_number or 0)
        before = [
            item
            for item in quest_resources
            if item.kind != "R" and item.task_number is not None and craft.task_number is not None and item.task_number < craft.task_number
        ]
        ingredients = before[-2:]
        if len(ingredients) < 2:
            warnings.append(
                {
                    "resource": craft.classname,
                    "warning": "recipe has fewer than two nearby resource tasks; recipe skipped",
                }
            )
            continue
        ingredients = [ingredients[0], ingredients[1], ingredients[0], ingredients[1]]
        ingredient_parts = [f"asset={item.classname}:{item.amount}" for item in ingredients]
        identifier = f"{craft.classname}_Recipe"
        result.append(
            [
                "",
                "/recipe/Dacha_2025/Dacha_2025_R_1_Recipe.proto.js",
                f"/recipe/{prefix}/{identifier}.proto.js",
                identifier,
                craft.classname,
                "2400",
                prefix,
                "+".join(ingredient_parts),
                ingredients[0].classname,
                str(ingredients[0].amount),
                ingredients[1].classname,
                str(ingredients[1].amount),
                ingredients[2].classname,
                str(ingredients[2].amount),
                ingredients[3].classname,
                str(ingredients[3].amount),
                f"active_quest={craft.quest_classname}+asset!={craft.classname}:1",
                f"asset={craft.classname}:1",
                "",
            ]
        )
    return result, warnings


def build_rows(campaign_id: str, hogs: list[HogResource], resources: list[Resource]) -> tuple[list[list[Any]], list[dict[str, Any]]]:
    rows: list[list[Any]] = []
    warnings: list[dict[str, Any]] = []
    by_kind = {kind: [resource for resource in resources if resource.kind == kind] for kind in RESOURCE_KINDS}

    block(
        rows,
        ["", "HOG"],
        ["temp_01", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "id"],
        [
            [
                "",
                "/debris/Dacha_2025/Dacha_2025_HOG_1.proto.js",
                f"/debris/{campaign_id}/{hog.classname}.proto.js",
                hog.classname,
                hog.classname,
                hog.title,
                "",
            ]
            for hog in hogs
        ],
    )

    block(
        rows,
        ["", "GR ассет"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun11/resource/Fun11_GR_1.proto.js",
                f"/quest_item/{campaign_id}/{resource.classname}.proto.js",
                resource.classname,
                resource.classname,
                resource.title,
                gr_description(resource),
                f"pack_asset={resource.classname}_Package",
                "",
            ]
            for resource in by_kind["GR"]
        ],
    )

    gr_way_rows = []
    for resource in by_kind["GR"]:
        action, input_path, probability = gr_reward_action(resource)
        gr_way_rows.append(
            [
                "",
                input_path,
                f"/global_reward/{campaign_id}/{resource.classname}.proto.js",
                resource.classname,
                action,
                "",
                probability,
                resource.classname,
                f"active_quest={resource.quest_classname}",
                gr_assets(resource),
                "",
                "",
                "",
                "",
                "",
                "",
            ]
        )
    block(
        rows,
        ["", "", "", "GR способы получения"],
        ["temp_01", "string", "string", "ignore", "array", "array", "int", "string", "string", "array", "int"],
        ["", "input", "output", "file_name", "actions", "location_tags", "rand_reward.p", "rand_reward.asset", "conditions", "assets", "id"],
        gr_way_rows,
    )

    package_headers = ["", "input", "output", "classname", "asset", "title", "reward", "Количество ассетов", "price", "stuff_icon", "id"]
    package_types = ["temp_01", "string", "string", "string", "ignore", "string", "string", "ignore", "int", "string", "int"]
    block(rows, ["", "GR ПАКЕТЫ"], package_types, package_headers, [package_row(campaign_id, "GR", resource) for resource in by_kind["GR"]])

    for kind, title, asset_input, post_title, package_title in [
        ("ASK", "ASK", "/quest_item/Fun/Fun10/resource/Fun10_ASK_1.proto.js", "ASK пост экшен", "ASK ПАКЕТЫ"),
        ("PER", "PER", "/quest_item/Fun/Fun10/resource/Fun10_PER_1.proto.js", "PER пост экшен", "PER ПАКЕТЫ"),
    ]:
        block(
            rows,
            ["", title],
            ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "int"],
            ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "conditions", "id"],
            [
                [
                    "",
                    asset_input,
                    f"/quest_item/{campaign_id}/{resource.classname}.proto.js",
                    resource.classname,
                    resource.classname,
                    resource.title,
                    STRICT_DESCRIPTIONS[kind],
                    f"pack_asset={resource.classname}_Package",
                    "",
                    "",
                ]
                for resource in by_kind[kind]
            ],
        )
        block(
            rows,
            ["", post_title],
            ["temp_01", "string", "string", "string", "ignore", "string", "string", "int", "int", "int", "int"],
            ["", "input", "output", "identifier", "classname", "title", "poster_reward", "clicks_limit", "life_time", "send_interval", "id"],
            [
                [
                    "",
                    f"/post_action/ask_for_Fun10_{kind}_{'10' if kind == 'ASK' else '1'}.proto.js",
                    f"/post_action/ask_for_{resource.classname}.proto.js",
                    f"ask_for_{resource.classname}",
                    resource.classname,
                    resource.title,
                    f"asset={resource.classname}:1",
                    "5",
                    "43200",
                    "7200",
                    "",
                ]
                for resource in by_kind[kind]
            ],
        )
        block(rows, ["", package_title], package_types, package_headers, [package_row(campaign_id, kind, resource) for resource in by_kind[kind]])

    block(
        rows,
        ["", "FG АССЕТ"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "conditions", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun10/resource/Fun10_FG_1.proto.js",
                f"/quest_item/Fun/{campaign_id}/resource/{resource.classname}.proto.js",
                resource.classname,
                resource.classname,
                resource.title,
                STRICT_DESCRIPTIONS["FG"],
                f"pack_asset={resource.classname}_Package",
                "",
                "",
            ]
            for resource in by_kind["FG"]
        ],
    )
    block(
        rows,
        ["", "FG МЕХАНИКА"],
        ["temp_01", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "asset_classname", "conditions", "label", "id"],
        [
            [
                "",
                "/free_gift/Fun/Fun10/Fun10_FG_1.proto.js",
                f"/free_gift/{resource.classname}.proto.js",
                resource.classname,
                f"active_quest={resource.quest_classname}",
                "Fun",
                "",
            ]
            for resource in by_kind["FG"]
        ],
    )
    block(rows, ["", "FG ПАКЕТЫ"], package_types, package_headers, [package_row(campaign_id, "FG", resource) for resource in by_kind["FG"]])

    block(
        rows,
        ["", "R ассет"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "tags.0", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun11/repair/Fun11_R_1.proto.js",
                f"/quest_item/{campaign_id}/{resource.classname}.proto.js",
                resource.classname,
                resource.classname,
                resource.title,
                ensure_period(resource.hint),
                "",
                campaign_id,
                "",
            ]
            for resource in by_kind["R"]
        ],
    )

    recipe_data, recipe_warnings = recipe_rows(campaign_id, resources)
    warnings.extend(recipe_warnings)
    block(
        rows,
        ["", "Рецепты 4 ингридиента"],
        ["temp_01", "string", "string", "string", "ignore", "int", "array", "string", "ignore", "ignore", "ignore", "ignore", "ignore", "ignore", "ignore", "ignore", "string", "string", "int"],
        ["", "input", "output", "identifier", "", "lifespan", "tags", "ingredients", "ingredient_1_asset", "ingredient_1_asset_amount", "ingredient_2_asset", "ingredient_2_asset_amount", "ingredient_3_asset", "ingredient_3_asset_amount", "ingredient_4_asset", "ingredient_4_asset_amount", "conditions", "reward", "id"],
        recipe_data,
    )

    block(
        rows,
        ["", "FA ассет"],
        ["temp_01", "string", "string", "string", "string", "string", "string", "string", "string", "int"],
        ["", "input", "output", "classname", "view_classname", "title", "description", "meta_info", "tags.0", "id"],
        [
            [
                "",
                "/quest_item/Fun/Fun11/repair/Fun11_R_1.proto.js",
                f"/quest_item/{campaign_id}/{resource.classname}.proto.js",
                resource.classname,
                resource.classname,
                resource.title,
                ensure_period(resource.hint),
                f"pack_asset={resource.classname}_Package",
                campaign_id,
                "",
            ]
            for resource in by_kind["FA"]
        ],
    )
    block(rows, ["", "FA Пакеты"], package_types, package_headers, [package_row(campaign_id, "FA", resource) for resource in by_kind["FA"]])

    if rows and all(cell == "" for cell in rows[-1]):
        rows.pop()
    return rows, warnings


def build_resource_table(
    campaign_id: str,
    campaigns_dir: Path = DEFAULT_CAMPAIGNS_DIR,
    pack_ids: list[str] | None = None,
) -> tuple[list[list[Any]], dict[str, Any]]:
    campaign_dir = campaigns_dir / campaign_id
    if not campaign_dir.exists():
        raise FileNotFoundError(f"campaign not found: {campaign_dir}")
    pack_dirs = iter_pack_dirs(campaign_dir, pack_ids)
    hogs, resources, warnings = collect_resources(campaign_id, pack_dirs)
    rows, row_warnings = build_rows(campaign_id, hogs, resources)
    warnings.extend(row_warnings)
    summary = {
        "campaign_id": campaign_id,
        "packs": [path.name for path in pack_dirs],
        "blocks": [cell for row in rows for cell in row if str(cell).strip() in BLOCK_TITLES],
        "hogs": len(hogs),
        "resources": {kind: len([resource for resource in resources if resource.kind == kind]) for kind in RESOURCE_KINDS},
        "warnings": warnings,
    }
    return rows, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build developer resource table CSV for a campaign.")
    parser.add_argument("campaign_id")
    parser.add_argument("--pack", action="append", default=None, help="Optional pack filter. Can be repeated.")
    parser.add_argument("--campaigns-dir", type=Path, default=DEFAULT_CAMPAIGNS_DIR)
    parser.add_argument("--output-csv", type=Path, default=None)
    parser.add_argument("--summary-json", type=Path, default=None)
    args = parser.parse_args(argv)

    output_csv = args.output_csv or args.campaigns_dir / args.campaign_id / "resource_table.csv"
    summary_json = args.summary_json or args.campaigns_dir / args.campaign_id / "resource_table.summary.json"
    rows, summary = build_resource_table(args.campaign_id, campaigns_dir=args.campaigns_dir, pack_ids=args.pack)
    write_csv(output_csv, rows)
    write_json(summary_json, summary)

    print(f"campaign id: {args.campaign_id}")
    print(f"packs: {', '.join(summary['packs'])}")
    print(f"blocks: {len(summary['blocks'])}")
    print(f"hogs: {summary['hogs']}")
    for kind, count in summary["resources"].items():
        if count:
            print(f"{kind}: {count}")
    print(f"warnings: {len(summary['warnings'])}")
    print(f"csv written: {output_csv}")
    print(f"summary written: {summary_json}")
    return 0 if not summary["warnings"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
