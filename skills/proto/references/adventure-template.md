# Adventure Template

Use this reference when the user mentions `Adventure_template`, Adventure-style event documentation, or a ready event package with folders like `quest`, `quest_action`, `quest_group`, `pet`, `pot`, `furniture`, `collection_item`, and `trophy`.

## Stored Example

Canonical edited workbook:

```text
skills/proto/assets/Adventure_template/Adventure_template.xlsx
```

Split workbooks, one sheet per file:

```text
skills/proto/assets/Adventure_template/split_xlsx/
```

The split data files use a first worksheet named `conf`; `README.xlsx` is documentation only.

## Package Input Paths

For implemented reference packages, each proto folder may contain `Path.txt`. Build `input` by joining:

```text
<Path.txt normalized to /...> + / + <proto filename>
```

Example:

```text
quest/Path.txt = \quest\marketing_action\Adventure\Adventure_3_Sport\Adventure_3_Sport_9\
Adventure_3_Sport_9_rewards.proto.js
=> /quest/marketing_action/Adventure/Adventure_3_Sport/Adventure_3_Sport_9/Adventure_3_Sport_9_rewards.proto.js
```

Use these same paths as the reference `input`. For a new event, `output` should point to the new target path/classname, while the reference file remains in `input`.

## Final File Shape

Do not merge all Adventure families into one giant workbook. For final delivery, create separate XLSX files per family. Each final family workbook must have its first worksheet named `conf`.

Typical family files:

```text
collection_item.xlsx
furniture.xlsx
pet.xlsx
pot.xlsx
mystery_box.xlsx
quest.xlsx
quest_action.xlsx
quest_group.xlsx
trophy.xlsx
```

`quest_item.xlsx` is a first-creation artifact for a new shared progress resource.
Do not deliver it again for subsequent packs using an existing resource.

A multi-tab workbook is useful only as an editing/training surface.

## Master Brief Workflow

For Adventure-style generation briefs, keep the user's manual entry surface compact.

On `01_Паки`, the user fills only event-wide values:

```text
new_prefix
main_resource
event_title_ru
quest_group_title
duration_text
source_reference
Последний id proto
Последний id task
```

`event_folder` is derived from `new_prefix` (`Adventure_4_1` -> `Adventure_4`), and `output_root_hint` is derived from `event_folder/new_prefix`. Do not keep `theme_short`; the user writes visible text manually.

On `02_Замены`, generated formulas should handle repeated replaces:

```text
Adventure_3_Sport_9 -> new_prefix
Adventure_3_Sport -> event_folder
Adventure_GR_3 -> main_resource
Pet17_Sport_9 -> "Pet17_" + new_prefix
TrophyPet17_Sport_9 -> "TrophyPet17_" + new_prefix
```

When a future reference uses different pet/trophy constants, detect them from the reference pet/trophy classnames and apply the same constant-prefix + `new_prefix` pattern.

On `03_Объекты`, leave the broad manual object-editing surface intact. The user expects to fill or adjust classnames, visible titles/descriptions, prices, subgroup, and `extra_json_or_notes` here.

On `04_Квесты`, `new_identifier` should be formula-derived from `new_prefix`:

```text
<new_prefix>_quest
<new_prefix>_quest_task_1
<new_prefix>_quest_task_2
<new_prefix>_quest_task_3
<new_prefix>_rewards
<new_prefix>
```

Keep visible text fields available for manual editing: `title`, `description`, `congratulation`, and `rule_window_description`. Event-wide titles may be formula-fed from `01_Паки`, but the user can overwrite them.

On `05_Награды`, reward positions are stable for this Adventure pattern. It is acceptable for Codex tooling to fill these from `03_Объекты` and for the user to manually polish text afterward.

Do not keep `06_Экономика`, `07_Выходные файлы`, or `08_Чеклист` in the simplified Adventure brief. Economy values that mattered in practice came from `03_Объекты.extra_json_or_notes`.

ID generation:

- `Последний id proto` is the last occupied numeric proto id. The user may fill it once in any pack row; treat that single value as the baseline before pack 1 and continue the id chain across all packs in order. Output tables should write `last + 1`, then increment by one only for real proto rows whose `input` or `output` value is an actual prototype path starting with `/`. Never assign ids to human title rows such as `task - ...`.
- `Последний id task` in the brief is the last occupied task identifier, e.g. `e8697`. A new Adventure pack has **17 tasks**, including the root quest, general restarter, tech quest and trophy. Continue the chain across packs in order. When a user instead supplies the first free ID for patching reviewed tables, use that exact value without incrementing it first. Preserve all existing manual identifiers, including the `z` identifiers in Adventure_4_2.

## Core Replace Rule

For Adventure-style quest, quest_group, quest_action, and trophy protos, prefer broad `replace` columns over exposing every dependent field.

The main event prefix appears everywhere and is stable inside the reference package. In the Adventure_3 example:

```text
find = Adventure_3_Sport_9
replace = Adventure_3_Sport_9
```

In a new event, the `replace` value becomes the new prefix/classname root. This preserves all hidden reference fields and updates identifiers, group links, conditions, actions, and nested JSON that contain the old prefix.

This is intentional: fields omitted from the table remain copied from the donor reference proto.

Use additional broad replace pairs when a shared reward/resource classname changes across task protos. In the Adventure_3 task quest blocks, this pattern was used for:

```text
find = Adventure_GR_3
replace = Adventure_GR_3
```

For a new event, replace it with the new GR/reward classname.

## Field Style By Family

### quest_item

Create the main Adventure progress resource once when introducing a new resource classname:

```text
classname
title
subgroup
inventory_section
id
```

Use `/quest_item/Adventure_GR_3.proto.js` as the donor for Adventure-style GR resources unless the user provides a closer reference.

The generator omits this workbook by default. `--create-shared-resources` explicitly enables first creation of the progress resource and `Box_1`; use it only once. Adventure_4 already uses the existing `Adventure_GR_4` and `Adventure_4_Box_1`.

### collection_item

Keep:

```text
classname
title
description
rand_reward
id
```

Encode `rand_reward` as an `object` column so `one_of` can stay as JSON in the value cell.

### furniture

Keep:

```text
classname
title
description
subgroup
inventory_section
price
currency
meta_info
id
```

### pet

Keep:

```text
classname
title
description
subgroup
extra
id
```

Encode `extra` as one `object` column. Preserve nested values as JSON where they are too large or structural.

### pot

Keep:

```text
classname
title
description
subgroup
price
currency
id
```

Use one flat `sl` block for multiple pot rows.

### mystery_box

Keep definitions only for boxes that need creating or changing. In the reviewed Adventure_4 packs omit the existing `Adventure_4_Box_1` definition and retain its reward references. Keep Box_2 and Box_3 with their manual content. First creation of a new shared Box_1 requires `--create-shared-resources`.

```text
classname
title
description
price
currency
meta_info
rand_reward
id
```

Encode `rand_reward` as an `object` column with `all` in the key cell and the JSON array of rewards in the value cell.
Each box needs its own `ml` block, with a blank row between blocks. Several input rows in one `ml` block create only the first prototype.
Use the package `Path.txt` when present; in the Adventure_3 reference it resolves to:

```text
/mystery_box/Adventure/
```

### quest_group

Main group keeps:

```text
identifier
title
first_quest
last_quest
extra
id
```

Restarter and tech groups keep:

```text
identifier
replace(find/replace for event prefix)
id
```

Every restarter row with `replace` needs a separate block; a multi-row `sl` block resets replacements after its first prototype.

The confirmed FairyTale windows from Adventure_4_2 are:

| extra key | value |
| --- | --- |
| quest_confirm_window | FairyTaleConfirmWindow |
| quest_complete_window | FairyTaleQuestCompleteWindow |
| quest_progress_window | FairyTaleQuestProgressWindow |
| quest_rule_window.view_classname | FairyTaleQuestRuleWindow |
| quest_window.view_classname | FairyTaleQuestWindow |
| quest_window.quest_task_item | FairyTaleQuestTaskItem |

Preserve the manual rule title, description and other window properties. Apply these Adventure window defaults without changing unrelated event families.

### quest_action

For free reset and skip actions, keep only:

```text
replace(find/replace for event prefix)
id
```

For paid reset actions, also keep:

```text
open_price
```

Do not expose `stuff_actions` by default; the event-prefix replace updates the copied reference action chain.

### trophy

Keep:

```text
identifier
title
tasks.0.identifier
tasks.0.title
replace(find/replace for trophy/pet classname)
id
```

Set `tasks.0.title` to this pack's pet title. Replace `Pet17_Sport_9` with the new pet classname: this also updates the embedded substring in `TrophyPet17_Sport_9`, the task `param` and the pet conditions. A replacement limited to `TrophyPet17_Sport_9` leaves references to the donor pet behind.

### quest

Main/root, restarter, tech, and ordinary task quest protos should usually be reduced to `replace` and `id`, with explicit scalar fields only when the user must edit the content.

For task quest protos, include two replace pairs when applicable:

```text
event prefix replace
reward/resource classname replace
```

For every non-reward QuestPrototype, including the root `*_quest`, ordinary `quest_task_1`–`3`, their restarters, the general `*_restarter`, `*_tech` and trophy, expose these scalar dot-path columns in the same proto block:

```text
tasks.0.identifier
tasks.0.title
```

Use the pack's pet title for an absent non-reward task title. Preserve existing manual text. The root quest must also replace the progress resource (`Adventure_GR_3` → the actual resource), covering its reward and remove_asset action.

Do not create a separate `ml object` block for these ordinary task ids. The user only needs to replace the nested `identifier`; the rest of the `tasks.0` object should remain inherited from the donor proto.

Rewards quest (`*_rewards.proto.js`) is special:

- Keep a compact header block with event-prefix `replace`, `title`, `congratulation`, `id`.
- Do not keep the whole `tasks` array as one array column.
- Split reward tasks into separate object blocks: `tasks.0`, `tasks.1`, ...
- First create the rewards quest from the donor. In **every subsequent reward task block**, both `input` and `output` must be the newly created rewards quest path. Reading the donor again discards previously applied task updates.

Reward task object blocks should be vertical key/value pairs. The Adventure_3 edited template kept these keys:

```text
type
classname
amount
reward
title
hint
congratulation
identifier
```

For generated briefs, `identifier` should be auto-filled from `Последний id task` when provided. Leave it blank only when the user has not supplied a task id baseline. This form is easier for manual reward editing than a large JSON array.

For fresh generated tables keep the six ordinary task/restarter identifiers followed by seven reward tasks, then allocate the previously omitted root, general restarter, tech and trophy: 17 total. This is not permission to renumber existing reviewed tables. The historical proto stride of 35 is retained to avoid moving existing ranges; default reuse of the shared GR and Box_1 produces 33 unique prototypes and leaves two reserved positions unused.

## Applying Confirmed Developer Corrections

Canonical manual reference: `D:/domovoy/trunk/data_ingenering/GD/Adventure/Adventure_4_2_pack_tables/` (reviewed 2026-10-19). Do not replace the delivery by rebuilding from the brief: manual text, IDs and balance are authoritative.

- `tools/build_adventure_pack_from_brief.py` uses the project `.agents/skills/proto/assets/Adventure_template/split_xlsx/` templates and the shared repairs in `tools/adventure_table_review.py`.
- `tools/apply_adventure_developer_review.py` stages reviewed packs, adds only missing task IDs/titles, fixes references/windows/block boundaries, omits Box_1 definitions and removes the repeated quest_item workbook. It converts each complete staged pack with the actual converter before applying. Existing manual IDs are checked for preservation and global task uniqueness; existing manual `z` values are preserved, new values use the supplied `e` range. This does not relax the general quest pipeline's e-only assignment contract.
- First run without `--apply` to inspect the staged output. Applying requires an explicit `--apply`; backups of every changed/deleted workbook go to the chosen `--work` directory under ignored `output/`.
- Never overwrite existing XLSX with the brief generator; choose a new output directory. Do not freeze rows. Reopen, check Cyrillic, verify every task survives JSON serialization and run `python -m unittest discover -s tests` after code/template changes.

## Validation Notes

- `replace` is a two-column field: merged type cell `replace`, key row labels `find` and `replace`.
- Do not mistake the second key-row label `replace` for a type-row value.
- Run a workbook structural smoke-test after manual edits; shifted type/key rows are easy to create while editing.
- If a user manually deletes fields, treat deletion as a signal that those fields should stay inherited from the donor reference.
