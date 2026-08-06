# TwoDaysTournament Template

Use this reference when the user mentions `TwoDaysTournament`, `Двухдневный турнир`, or a ready event package with folders like `competition`, `magazine`, `recipe`, `quest/competition`, `quest_action`, `quest_group`, `quest_item`, `mystery_box`, `pet`, `furniture`, `collection_item`, and `trophy`.

## Stored Example

Canonical edited workbook:

```text
skills/proto/assets/TwoDaysTournament_template/TwoDaysTournament_template.xlsx
```

Split converter-ready workbooks:

```text
skills/proto/assets/TwoDaysTournament_template/split_xlsx/
```

Source reference currently used:

```text
input/TwoDaysTournament_2026_05
```

## Prefixes And Paths

The main reference prefix is:

```text
TwoDaysTournament_2026_05_01
```

For the next monthly event, the common edit is:

```text
TwoDaysTournament_2026_05_01 -> TwoDaysTournament_2026_08_01
```

The month prefix without the final pack suffix also appears:

```text
TwoDaysTournament_2026_05 -> TwoDaysTournament_2026_08
```

Quest group paths are special: `quest_group/Path.txt` uses only the date folder:

```text
\quest_group\TwoDaysTournament\2026_05_01\
```

For a new prefix `TwoDaysTournament_2026_08_01`, the quest group path folder should become:

```text
2026_08_01
```

Build `input` from each folder's `Path.txt` plus the proto filename, normalizing backslashes to `/`.

## Family Files

Final converter files should stay split by family, not merged:

```text
quest_item.xlsx
collection_item.xlsx
furniture.xlsx
pet.xlsx
mystery_box.xlsx
competition.xlsx
magazine.xlsx
recipe.xlsx
quest.xlsx
quest_action.xlsx
quest_group.xlsx
trophy.xlsx
```

A combined workbook is useful for review only.

## Compact Field Policy

Use broad `replace` for the event prefix, and expose only fields the user normally changes:

- visible titles and descriptions;
- dates and time conditions;
- `tasks.0.identifier`;
- `competition.quest_task_identifier`;
- pet visible fields and key `extra.*` values;
- magazine visible text fields;
- competition reward maps;
- recipe reward/ingredients;
- ids only when a user supplied an id baseline.

Do not expose stable mechanical fields such as `class`, `group`, disabled flags, tags, `stuff_actions`, opens, reset chains, or generated window classnames unless the user asks. Those should inherit from the donor and be updated by broad replace.

## Task Id Order

`TwoDaysTournament` uses 13 task identifiers in this reference pattern. If the user provides `Последний id task`, generate new task ids in this order:

```text
1. trophy.tasks.0.identifier
2. competition Activate tasks.0.identifier
3. competition.quest_task_identifier and Competition Counter tasks.0.identifier (same id)
4. Competition Task1 tasks.0.identifier
5. Competition Task1 restarter tasks.0.identifier
6. Competition Task2 tasks.0.identifier
7. Competition Task2 restarter tasks.0.identifier
8. Competition Task3 tasks.0.identifier
9. Competition Task3 restarter tasks.0.identifier
10. Tech1 tasks.0.identifier
11. Tech2 tasks.0.identifier
12. Tech_Magazine tasks.0.identifier
13. Tech_MagazineShopAvailable tasks.0.identifier
```

For the first production use after Adventure_4, the user supplied:

```text
last_task_id = e100217
next_task_id = e100218
```

## Brief Shape

The master brief lives at:

```text
input/TwoDaysTournament_master_brief.xlsx
```

Current sheets:

```text
01_Event
02_Objects_Text
03_Magazine_Text
04_Task_Id_Order
```

The user should be able to fill mostly one event page plus text tabs:

- `new_prefix`, usually `TwoDaysTournament_2026_08_01`;
- `new_month_prefix`, usually `TwoDaysTournament_2026_08`;
- `new_quest_group_folder`, usually `2026_08_01`;
- title/genitive title/resource/pet text;
- date fields;
- `last_proto_id` if final proto ids are needed;
- `last_task_id`.

The brief currently pre-fills `last_task_id = e100217` from the user's message.

