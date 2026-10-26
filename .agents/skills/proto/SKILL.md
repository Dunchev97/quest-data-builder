---
name: proto
description: "Build compact converter-compatible XLSX/CSV dev-table templates from .proto.js / JSON prototypes for the radmirxan xlsx-to-json.js pipeline. Use when Codex must create or revise proto tables with ml/sl directives, donor input/output paths, one compact block per prototype family, dot-path columns, object/array continuation cells, skipped game-design-irrelevant fields, or replace columns."
---

# Proto

Create tables for the real `radmirxan/xlsx-to-json.js` converter, not decorative planning sheets.

Resolve `<game_repo_root>` to the current machine's game checkout before inspecting converter sources or donor prototypes. Do not assume every contributor uses the same drive or checkout directory.

Converter files to inspect when needed:

```text
<game_repo_root>/data_ingenering/tool/NodeTest/radmirxan/xlsx-to-json.js
<game_repo_root>/data_ingenering/tool/NodeTest/radmirxan/myXLSX.js
<game_repo_root>/data_ingenering/tool/NodeTest/radmirxan/proto.js
```

The prototype root is normally `<game_repo_root>/server/prototypes`. If the checkout cannot be located from the current workspace or user-provided context, ask for its path instead of silently using a machine-specific path.

## Output Contract

The first worksheet must be named `conf`. `xlsx-to-json.js` reads only rows where column A is non-empty.

Column A may contain only:

```text
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
- Use base type names in the sheet: `string`, `int`, `array`, `object`, `ignore`, `replace`.
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
- Keep arrays in the same block as `array` columns with vertical continuation rows.
- Keep `replace` in the same block when a donor substring should be rewritten globally for that output proto.
- Leave A/B/C blank on continuation rows inside a compact block.
- Use `sl` for simple flat multi-row tables.
- Use `ml` when any row needs `object`, `array`, or `replace`.

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

- Leave every `id` cell blank (true null), including quests, quest groups, characters, and actions. There is no reference-ID exception in this project.
- It is acceptable to keep an empty `id` column so a dev can fill it later.
- Donor/reference IDs are not copied into delivered tables; do not allocate numeric IDs.

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

For `ml array`, write one value per continuation row:

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
- Global rewards with `replace`: one separate `sl` block per prototype. The converter resets replacements after the first row.

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
$gameRepoRoot = 'D:\path\to\domovoy\trunk'
python .agents/skills/proto/scripts/prototype_to_table.py "$gameRepoRoot/server/prototypes/collection/631.proto.js" output/collection_template.xlsx --target-proto /collection/New_Collection.proto.js --root "$gameRepoRoot/server/prototypes"
python .agents/skills/proto/scripts/validate_converter_table.py output/collection_template.xlsx
```

## Validation

Before finalizing:

- Reopen the XLSX with `openpyxl`.
- Assert the first worksheet is `conf`.
- Assert column A has only blank, `sl`, `ml`.
- Assert every directive row is followed by a key row with `input` in B and `output` in C.
- Assert `object` columns are merged across key/value pair columns on type and key rows.
- Assert `replace` columns are merged across key/value pair columns on the type row, while the key row still shows `find` and `replace`.
- Assert every task block is `ml; string; string; object` with update key `tasks.N`.
- In initial authoring mode assert every id cell is blank. After the user supplies free proto/task IDs and explicitly requests assignment, use the strict `--assigned-ids` mode: all prototype IDs and task identifiers must be present and unique across the delivery. The validator has no --allow-id bypass.
- Assert no mojibake or `????`.
- Assert stale donor identifiers are absent from target values except donor `input` paths or explicit `replace` blocks.
- For quest delivery, run `src/validate_proto_exports.py` against the actual converter and real donors in an isolated directory. Verify every intended field survives JSON serialization, not just the exit code.

## Report

Return:

- Link to the final XLSX files in the pack review/proto directory.
- Source prototypes and converter scripts used.
- Counts of compact proto blocks and data rows.
- Remaining assumptions: skipped fields, blank ids, unknown classnames, balance values, or copied donor values.

## Verified converter limitations (2026-10-19)

- `temp_01`/`temp_02` are JS module names, not accepted column-A directives. `array_of_values` and `array_of_objects` are unsupported types in this checkout.
- One `ml` block creates exactly one prototype. Repeat the block for each entity; only continuation B/C cells remain blank.
- One `sl` block with `replace` also needs one input row: replacement state is reset by the converter after its first update.
- Blank cells must be actual null cells, not inline empty strings or formulas returning an empty string. Otherwise `sl` may read a phantom input row and fail with EISDIR.
- Use Excel numeric cells for int fields. Runtime button text such as `extra.open_now_btn_window` is string.
- Array dot paths require an index: `behaviour.0.window_spec.description_1`. JS silently drops properties written onto an array without its index during JSON serialization.
- A blank id cell inherits the donor id; it does not erase it. Keep the requested empty cells, and reserve/assign production IDs separately before game import.
- Read `workflows/PROTO_EXPORT_WORKFLOW.md` for the project split/export/validation commands and known donor repairs.

## Quest pipeline delivery preference (2026-10-19)

For quest work deliver only final XLSX files under `campaigns/<campaign_id>/<pack_id>/review/proto/`, each containing exactly one `conf` sheet. Put FunCollection and quest accomplished workbooks there too. Do not create CSV files, ZIP archives, bundle_manifest.json, manifest.json, validation_report.json, export summary JSON, or an additional combined review workbook. Validation stays mandatory; print results to the console. Necessary temporary converter inputs and outputs belong in ignored output/, never in the delivery folder.

The user is now reviewing the final workbooks by hand. Preserve those files. After the user reports completion, read those exact workbooks, reconcile confirmed corrections into the generator/template/documentation, and verify regenerated behavior in output/ without replacing the manual reference. Create the full quest-authoring skill after the table review and confirmed pipeline corrections, not before. Stage 6 approval checksums cover all final XLSX directly, without a manifest file.

Every final quest workbook filename must contain the exact campaign prefix. Prepend `<campaign_id>_` to generic names, e.g. `VelesNight_2026_quests.xlsx`, `VelesNight_2026_resources.xlsx`, `VelesNight_2026_funcollection_4.xlsx`. Do not duplicate a prefix already present in names such as `quest_VelesNight_2026_accomplished.xlsx`. This rule covers Stage 6, standalone generators, FunCollection, and legacy workbook splitting. Rename existing manual files without regenerating their contents.

## Quest character and output corrections (2026-10-19)

Generated furniture outputs use `/furniture/<campaign_id>/Character/`; generated quest action outputs use `/quest_action/<campaign_id>/`. Do not insert `/Fun/` into these generated paths. Preserve donor input paths exactly, including their real `/Fun/` folders.

Every generated character classname includes both character and emotion numbers: `<campaign_id>_Character_<character_number>_<emotion_number>`. Use emotion 1 when unspecified and preserve explicit emotion numbers. Physical icon/param/action/go_to_location references use the game classname; quest helper and UI view_class use the graphic class from dialogue_characters.json. Keep those roles distinct, including JSON cell values. Give numbering uses the character number, not the emotion number. Connect pack dialogs with workflow_fast.py dialogs after manual table review; see workflows/DIALOGUE_WORKFLOW.md.

Initially all final tables have blank id cells, including quests, quest groups, entities and actions. Remove previous reference-ID/range-allocation exceptions. Never place donor IDs, numeric zero, or an empty-string formula in those cells. Once the user explicitly supplies free proto/task IDs and asks for assignment, use src/proto_ids.py directly on the reviewed XLSX. Preserve assigned values and every other manual edit; do not regenerate the workbooks. Allocate once per unique output path and once per (quest output, tasks.N). Task identifiers are e-prefixed strings; proto IDs are Excel integers. Validate the complete set with validate_proto_exports.py --assigned-ids, which requires complete unique IDs and checks their converted values. Report the next free numbers. See workflows/PROTO_EXPORT_WORKFLOW.md for the two phases and commands.

## Technical quest delivery (2026-10-19)

For every ordinary quest pack also create `MB_RECIPEMB_POTS_<campaign_id>.xlsx`: three reward mystery boxes, three recipes and three matching prize pots. For ALL `R_MB_N_Recipe.ingredients`, copy the exact current `<campaign_id>_R_1_Recipe.ingredients`, including order and quantities; never choose R_N by box number. Placeholder titles are explicitly allowed. Use `src/mystery_rewards.py`; it is integrated into Stage 6 before technical cleanup. Existing manual workbooks are protected; `--update-ingredients` changes only those cells. Read the mandatory reward-table section of `workflows/PROTO_EXPORT_WORKFLOW.md` for donors, links, lifecycle and converter checks. Preserve permanent prize pots during event cleanup.

Stage 6 also delivers `<campaign_id>_technical_quests.xlsx`, one `conf`, in the same review/proto folder. Use `src/technical_quest_tables.py` after all other tables, including FunCollection. Verified donors are `/quest_group/event/Night_2026/Night_2026_Tech.proto.js` and `/quest/event/Night_2026/Night_2026_Tech_1.proto.js`, `_Tech_2.proto.js`.

The user clarified that blank `identifier` means TASK identifiers (`e9586`, `e9587`), not the prototype names. Initially leave every `tasks.N.identifier` and prototype id blank for later assignment by the user. Fill prototype identifiers and their links with the campaign prefix. Preserve subsequently assigned manual values by protecting the reviewed files.

Tech_2 on_spoil must cover every generated campaign resource, character/emotion, HOG, interactive object/resource and FunCollection state/effect defined in the current reviewed XLSX across the campaign packs. Collect definitions, not arbitrary references to existing game ingredients. quest_item/workbench_item/mystery_box use remove_asset; furniture/debris/chest/workbench use remove_stuff. Both action objects use the donor key `classname`. Service definitions (packages, recipes, rewards, actions, quests/groups, UI) are not inventory objects. Deduplicate and reject foreign classnames or unclassified families. Preserve cancellation of campaign-tagged crafting. Encode on_spoil as ml/array with one JSON action per continuation row, never a JSON array in one cell.

Expose group spoil_conditions for the event deadline. If none is supplied, leave a highlighted blank with a comment requiring completion before import. Blank updates inherit the donor's expired date; do not invent a release date or call converter success an import-ready schedule. The real-converter validator checks cleanup coverage against all XLSX supplied in the run; always validate the complete set. See workflows/PROTO_EXPORT_WORKFLOW.md for the command and full contract.
