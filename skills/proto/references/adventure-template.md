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
quest_item.xlsx
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
- `Последний id task` is the last occupied task identifier, e.g. `e8697`. The user may fill it once in any pack row; treat that single value as the baseline before pack 1 and continue the task id chain across all packs in order, preserving the letter prefix and numeric width.

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

Keep the main Adventure progress resource when the new pack changes the resource classname:

```text
classname
title
subgroup
inventory_section
id
```

Use `/quest_item/Adventure_GR_3.proto.js` as the donor for Adventure-style GR resources unless the user provides a closer reference.

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

Keep the three reward boxes when reward tasks reference new box classnames:

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
replace(find/replace for trophy/pet classname)
id
```

### quest

Main/root, restarter, tech, and ordinary task quest protos should usually be reduced to `replace` and `id`, with explicit scalar fields only when the user must edit the content.

For task quest protos, include two replace pairs when applicable:

```text
event prefix replace
reward/resource classname replace
```

For ordinary Adventure `quest_task_1`, `quest_task_2`, `quest_task_3` protos and their `*_restarter` quest protos, expose the internal task id as a scalar dot-path column in the same quest proto table:

```text
tasks.0.identifier
```

Do not create a separate `ml object` block for these ordinary task ids. The user only needs to replace the nested `identifier`; the rest of the `tasks.0` object should remain inherited from the donor proto.

Rewards quest (`*_rewards.proto.js`) is special:

- Keep a compact header block with event-prefix `replace`, `title`, `congratulation`, `id`.
- Do not keep the whole `tasks` array as one array column.
- Split reward tasks into separate object blocks: `tasks.0`, `tasks.1`, ...

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

Task id allocation in generated Adventure tables should run through the ordinary task dot-path columns first (`quest_task_1`, `quest_task_1_restarter`, `quest_task_2`, `quest_task_2_restarter`, `quest_task_3`, `quest_task_3_restarter`), then continue through the seven rewards task object blocks.

## Validation Notes

- `replace` is a two-column field: merged type cell `replace`, key row labels `find` and `replace`.
- Do not mistake the second key-row label `replace` for a type-row value.
- Run a workbook structural smoke-test after manual edits; shifted type/key rows are easy to create while editing.
- If a user manually deletes fields, treat deletion as a signal that those fields should stay inherited from the donor reference.
