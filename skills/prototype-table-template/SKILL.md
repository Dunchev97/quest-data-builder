---
name: prototype-table-template
description: "Build converter-compatible XLSX/CSV table templates from .proto.js / JSON prototypes, especially quest_group + quest + task prototypes. Use when Codex must create dev tables for the radmirxan xlsx-to-json.js pipeline with ml/sl/temp_01/temp_02 blocks, input/output donor paths, update keys, and nested object blocks such as tasks.0."
---

# Prototype Table Template

This skill creates templates for the real converter, not decorative planning sheets.

Converter to inspect when in this repo:

```text
D:/domovoy/trunk/data_ingenering/tool/NodeTest/radmirxan/xlsx-to-json.js
D:/domovoy/trunk/data_ingenering/tool/NodeTest/radmirxan/myXLSX.js
D:/domovoy/trunk/data_ingenering/tool/NodeTest/radmirxan/proto.js
```

## Non-Negotiable Format

`xlsx-to-json.js` reads only the first worksheet and only rows where column A is non-empty.

Column A may contain only parser directives:

```text
temp_01
temp_02
sl
ml
```

Never put human titles in column A. Put human section titles in column B with column A blank.

Each parser block has this shape:

```csv
<directive>;<type for input>;<type for output>;<type for update field>...
;input;output;<update key>...
;<donor input path>;<target output path>;<value>...
```

Rules:

- Column B is always `input`.
- Column C is always `output`.
- Columns B/C are `tech`; columns D onward are proto `update`.
- `input` is the donor proto path.
- `output` is the target proto path.
- Leave `id` blank unless the user explicitly gave ids.
- Unknown generated identifiers may be blank if the downstream pipeline fills/preserves them.

## Directives

| Directive | Converter behavior | Use |
|---|---|---|
| `sl` | Flat multi-row table, internally prefixes types with `sl_` | One row per quest or simple proto update. |
| `ml` | One logical multiline block, internally prefixes types with `ml_` | Quest group blocks, task object blocks, arrays/objects. |
| `temp_01` | Same shape as `sl`, no prefix | Only when donor examples use it. |
| `temp_02` | Same shape as `ml`, no prefix | Only when donor examples use it. |

Use base type names in the sheet:

```text
string
int
array
array_of_values
array_of_objects
object
ignore
replace
```

Do not write `ml_string` or `sl_string` in the table when using `ml`/`sl`; the converter adds the prefix.

## Canonical Quest Template

For a quest pack, the first worksheet should be named `conf` and ordered exactly like this:

1. Human title row:

```csv
;Квест группа;;;;;;
```

2. Quest group block:

```csv
ml;string;string;string;string;string;array_of_values;string;string
;input;output;title;description;description_complete;extra.quest_reward_prewiew;extra.description_condition;extra.description_complete
;/quest_group/...donor.proto.js;/quest_group/...target.proto.js;...
```

3. For each quest in that group, human title row plus quest block:

```csv
;Квест 1;;;;;;
sl;string;string;string;string;string;string;string
;input;output;title;description;congratulation;helper;extra.sequence_icon
;/quest/...donor.proto.js;/quest/...target.proto.js;...
```

4. Immediately after that quest, add its task blocks:

```csv
;Таск 1;Диалог;;;
ml;string;string;object
;input;output;tasks.0
;/quest/...donor.proto.js;/quest/...target.proto.js;type;action
;;;icon;SomeCharacterIcon
;;;action;Some_Dialog_Action
;;;title;Поговори с персонажем
;;;hint;Поговори с персонажем.
;;;identifier;
```

Task rules:

- One task = one `ml` block.
- The task update key is `tasks.N`, zero-based.
- The task object is written as vertical key/value pairs in columns D/E.
- On continuation rows, columns A/B/C stay blank.
- Include `identifier` with an empty value when the pipeline/dev should generate or preserve it.
- JSON object/array values must be valid JSON text in a cell, for example:

```json
[{"classname":"SomeObject"}]
```

## Object Encoding

For `ml` object blocks:

```csv
;Название блока;;;
ml;string;string;object
;input;output;some.nested.key
;/donor.proto.js;/target.proto.js;field_1;value_1
;;;field_2;value_2
```

For `ml array_of_values`:

```csv
;Название блока;;;
ml;string;string;array_of_values
;input;output;opens
;/donor.proto.js;/target.proto.js;Quest_1
;;;Quest_2
```

Use dot paths exactly as proto update keys:

```text
tasks.0
tasks.1
extra.sequence_icon
extra.window_spec.view_window
on_accomplish
```

## Workflow

1. Read donor prototypes structurally as JSON.
2. Read any user-provided example CSV/XLSX and preserve its block style.
3. Map source `quest_group` to quests by `group_identifier`, `first_quest`, `last_quest`, and `opens`.
4. Build the parser table itself as the primary artifact. Do not make a pretty hierarchy sheet as the main output.
5. Put the final XLSX parser sheet first and name it `conf`.
6. Use donor paths in `input`, target paths in `output`, and update columns D onward.
7. Replace stale donor names in target values; donor names may remain in `input` only.
8. Leave unknown ids/prices/classnames blank or clearly mark only non-parser planning sheets. In parser blocks, prefer blank cells over prose markers.
9. Reopen and validate the XLSX before reporting.

## Helper Scripts

Optional helpers live in `scripts/`:

- `scripts/prototype_to_table.py`: creates a first-pass `conf` XLSX from one JSON `.proto.js`. Use it as a starting point, then curate block order and values.
- `scripts/validate_converter_table.py`: validates a produced XLSX against the converter block rules.

Example:

```powershell
python skills/prototype-table-template/scripts/validate_converter_table.py magazine/Magazine10.xlsx
```

## Validation

Before finalizing:

- Reopen the XLSX with `openpyxl`.
- Assert the first worksheet is `conf`.
- Assert column A has only blank, `temp_01`, `temp_02`, `sl`, `ml`.
- Assert every directive row is followed by a key row with `input` in B and `output` in C.
- Assert every task block is `ml; string; string; object` with update key `tasks.N`.
- Assert `id` cells are blank unless ids were supplied.
- Assert no mojibake or `????`.
- Assert stale donor identifiers are absent from target values except donor `input` paths or explicit `replace` blocks.
- If practical, run the converter on a small copy and inspect generated proto JSON.

## Report

Return:

- Link to the created XLSX/CSV.
- Source prototypes and converter scripts used.
- Counts of quest groups, quests, and task blocks.
- Remaining assumptions: blank ids, unknown classnames, balance values, or copied donor tasks.
