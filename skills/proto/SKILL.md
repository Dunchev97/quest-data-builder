---
name: proto
description: "Build compact converter-compatible XLSX/CSV dev-table templates from .proto.js / JSON prototypes for the radmirxan xlsx-to-json.js pipeline. Use when Codex must create or revise proto tables with ml/sl/temp_01/temp_02 directives, donor input/output paths, one compact block per prototype family, dot-path columns, object/array continuation cells, skipped game-design-irrelevant fields, or replace columns."
---

# Proto

Create tables for the real `radmirxan/xlsx-to-json.js` converter, not decorative planning sheets.

Converter files to inspect when needed:

```text
D:/domovoy/trunk/data_ingenering/tool/NodeTest/radmirxan/xlsx-to-json.js
D:/domovoy/trunk/data_ingenering/tool/NodeTest/radmirxan/myXLSX.js
D:/domovoy/trunk/data_ingenering/tool/NodeTest/radmirxan/proto.js
```

## Output Contract

The first worksheet must be named `conf`. `xlsx-to-json.js` reads only rows where column A is non-empty.

Column A may contain only:

```text
temp_01
temp_02
sl
ml
```

Never put human titles in column A. Put human section titles in column B with column A blank.

Every parser block has this shape:

```csv
<directive>;<type for input>;<type for output>;<type for update field>...
;input;output;<update key>...
;<donor input path>;<target output path>;<value>...
```

Rules:

- Column B is always `input`; column C is always `output`.
- Columns B/C are `tech`; columns D onward are proto `update`.
- Use donor proto path in `input` and target proto path in `output`.
- Use paths relative to `server/prototypes`, usually like `/collection/...` or `/seed/...`.
- Use base type names in the sheet: `string`, `int`, `array`, `array_of_values`, `array_of_objects`, `object`, `ignore`, `replace`.
- Do not write `ml_string` or `sl_string`; the converter adds the prefix for `ml` and `sl`.

## Default Style: Compact Blocks

Default to the Kizil-style compact table: one human section title plus one parser block per prototype family or repeated proto row set.

Prefer this:

```csv
;Collection_BushSeed_Kizil;;;;;;;;
ml;string;string;string;string;string;string;string;object;int
;input;output;identifier;title;reward;conditions;special_icon.icon;special_icon.title;req_assets;id
;/collection/631.proto.js;/collection/Collection_BushSeed_Kizil.proto.js;Collection_BushSeed_Kizil;Кизил;asset=RainbowFin:1;asset=Magazine10_Kizil_Condition:1;BushSeed_Kizil;Кизил;Magazine10_Kizil_Collection_1;
;;;;;;;;;Magazine10_Kizil_Collection_2;1
```

Avoid this unless the user explicitly wants a diagnostic decomposition:

```csv
;special_icon
ml;string;string;object
...
;req_assets
ml;string;string;object
...
```

Compact-block rules:

- Keep scalar fields for the same prototype on one data row.
- Flatten nested scalar fields into dot-path columns, for example `special_icon.icon`, `special_icon.title`, `extra.window_spec.view_window`.
- Keep map-like objects in the same block as `object` columns with key/value continuation rows.
- Keep arrays in the same block as `array` or `array_of_values` columns with vertical continuation rows.
- Keep `replace` in the same block when a donor substring should be rewritten globally for that output proto.
- Leave A/B/C blank on continuation rows inside a compact block.
- Use `sl` for simple flat multi-row tables.
- Use `ml` when any row needs `object`, `array`, `array_of_values`, `array_of_objects`, or `replace`.

## Fields To Omit

Do not mechanically copy every proto field. A template is for fields a game designer or table author should change.

Always omit by default:

```text
class
group
```

Usually omit when unchanged from donor:

```text
subgroup
currency
permit_sell
tags
meta_info
price
```

Include these only when the new proto needs a changed value or the user explicitly asks for them.

For `id`:

- Leave `id` blank unless the user supplied ids.
- It is acceptable to keep an empty `id` column so a dev can fill it later.
- If the user-provided reference table has real ids, preserve them.

## Replace

Use `replace` only when there is an obvious donor-to-target substring rewrite, for example `Raspberries` -> `Kizil`.

Encode it as a merged two-column type cell with visible `find` / `replace` labels on the key row:

```csv
ml;string;string;string;replace;string
;input;output;classname;find;replace;shop_conditions
;/seed/BushSeed_Raspberries.proto.js;/seed/BushSeed_Kizil.proto.js;BushSeed_Kizil;Raspberries;Kizil;asset=Magazine10_Kizil_Condition:1
```

Do not invent complex replace plans when unsure. Prefer explicit dot-path columns for fields the user will edit.

## Object And Array Encoding

For an `ml object` column, merge the type cell and key cell across the key/value pair columns so the next field starts after both columns:

```csv
ml;string;string;object;string
;input;output;req_assets;title
;/collection/631.proto.js;/collection/New.proto.js;Item_1;1;New title
;;;Item_2;1
```

For `ml array` or `ml array_of_values`, write one value per continuation row:

```csv
ml;string;string;array
;input;output;rand_reward.all.0.one_of
;/seed/BushSeed_Raspberries.proto.js;/seed/BushSeed_Kizil.proto.js;{"asset":"Magazine10_Kizil_Collection_1","p":100}
;;;{"asset":"Magazine10_Kizil_Collection_2","p":60}
```

JSON object/array values must be valid JSON text in a cell.

## Reading Reference Sheets

If the user gives a Google Sheets link as a reference:

- Read the exact tab and range first.
- If the file is a native Google Sheet, use the Google Sheets connector metadata before range reads.
- If the file is an Office `.xlsx` opened in Google Sheets, fetch the raw Drive file and inspect it with `openpyxl`.
- Preserve the reference table's block style, merges, directive choice, and omitted fields unless they conflict with converter rules.

The Kizil reference style on tab `В тени дерева` uses:

- `special_icon.icon` and `special_icon.title` as same-row dot-path columns.
- `req_assets` as one `object` column in the collection block.
- Collection items as one `sl` block with one item per row.
- Seed prototypes as one compact `ml` block per seed kind, with `replace`, reward arrays/objects, and `id`.
- Global rewards as one `sl` block with repeated rows and `replace`.

## Adventure Event Packages

When the user mentions `Adventure_template`, Adventure-style event docs, or an implemented event package with `quest`, `quest_action`, `quest_group`, `pet`, `pot`, `furniture`, `collection_item`, `trophy`, `quest_item`, or `mystery_box` folders, read:

```text
references/adventure-template.md
```

Use that reference instead of a generic JSON flatten. Important defaults:

- Build `input` from each folder's `Path.txt` plus the proto filename.
- Final output is multiple XLSX files by family, not one giant workbook.
- Each final family workbook's first worksheet must be named `conf`.
- Use broad `replace` pairs for shared prefixes such as `Adventure_3_Sport_9 -> <new event prefix>`.
- Omitted fields intentionally stay inherited from the donor/reference proto.
- Split `*_rewards.proto.js` reward `tasks.N` into separate vertical `object` blocks instead of one large `tasks` array column.

## TwoDaysTournament Event Packages

When the user mentions `TwoDaysTournament`, `Двухдневный турнир`, or an implemented monthly two-day tournament package with `competition`, `magazine`, `recipe`, `quest/competition`, `quest_action`, `quest_group`, `quest_item`, `mystery_box`, `pet`, `furniture`, `collection_item`, and `trophy` folders, read:

```text
references/twodays-tournament-template.md
```

Use that reference instead of Adventure-specific assumptions. Important defaults:

- Main prefix looks like `TwoDaysTournament_2026_05_01`.
- Quest group folder paths use a shorter date folder such as `2026_05_01`.
- Keep the final converter output split by family.
- Use broad prefix replace and expose task ids as scalar `tasks.0.identifier` dot-path columns.
- `competition.quest_task_identifier` shares the same generated id as the Competition Counter task.

## Quest Template Exception

For quest packs, keep the established quest workflow structure:

1. Human title row for quest group.
2. One `ml` quest-group block.
3. For each quest, one `sl` quest block.
4. Immediately after each quest, one `ml; string; string; object` task block per `tasks.N`.

Task block rules:

- One task = one `ml` block.
- The update key is `tasks.N`, zero-based.
- The task object is vertical key/value pairs.
- Include `identifier` with an empty value when the pipeline/dev should generate or preserve it.

## Workflow

1. Read donor prototypes structurally as JSON.
2. Read any user-provided example CSV/XLSX and preserve its compact block style.
3. Decide which fields a designer should edit; omit stable technical fields.
4. Build the parser table itself as the primary artifact.
5. Put the final XLSX parser sheet first and name it `conf`.
6. Use donor paths in `input`, target paths in `output`, and update columns D onward.
7. Replace stale donor names in target values; donor names may remain in `input` only.
8. Keep related nested data inside the same compact block where converter encoding allows it.
9. Reopen and validate the XLSX before reporting.

## Helper Scripts

Optional helpers live in `scripts/`:

- `scripts/prototype_to_table.py`: creates a compact first-pass `conf` XLSX from one JSON `.proto.js`.
- `scripts/validate_converter_table.py`: validates converter block rules.

`prototype_to_table.py` uses `--preset auto` by default:

- `CollectionPrototype` -> `identifier`, `title`, `reward`, `conditions`, `special_icon.*`, `req_assets`, `id`.
- collection item `AssetPrototype` -> `classname`, `title`, `id`.
- bush seed `AssetPrototype` -> `classname`, `title`, `description`, `extra.preparing_title`, `shop_conditions`, rewards, `id`.
- `classname` / `identifier` are derived from `--target-proto` so stale donor names do not leak into target values.

Example:

```powershell
python skills/proto/scripts/prototype_to_table.py D:/domovoy/trunk/server/prototypes/collection/631.proto.js output/collection_template.xlsx --target-proto /collection/New_Collection.proto.js --root D:/domovoy/trunk/server/prototypes
python skills/proto/scripts/validate_converter_table.py output/collection_template.xlsx
```

## Validation

Before finalizing:

- Reopen the XLSX with `openpyxl`.
- Assert the first worksheet is `conf`.
- Assert column A has only blank, `temp_01`, `temp_02`, `sl`, `ml`.
- Assert every directive row is followed by a key row with `input` in B and `output` in C.
- Assert `object` columns are merged across key/value pair columns on type and key rows.
- Assert `replace` columns are merged across key/value pair columns on the type row, while the key row still shows `find` and `replace`.
- Assert every task block is `ml; string; string; object` with update key `tasks.N`.
- Assert `id` cells are blank unless ids were supplied.
- Assert no mojibake or `????`.
- Assert stale donor identifiers are absent from target values except donor `input` paths or explicit `replace` blocks.
- If practical, run the converter on a small copy and inspect generated proto JSON.

## Report

Return:

- Link to the created XLSX/CSV.
- Source prototypes and converter scripts used.
- Counts of compact proto blocks and data rows.
- Remaining assumptions: skipped fields, blank ids, unknown classnames, balance values, or copied donor values.
