# AGENTS.md

## Project goal

This project builds a clean game data index for a legacy game quest generation system.

The final future goal is to generate quest task CSV files, but the current goal is only data parsing and indexing.

Do not implement quest generation or CSV export unless explicitly asked.

## Language

Always respond to the user in Russian.

All explanations, summaries, questions, plans, and final answers must be written in Russian.

Code, file names, JSON keys, CSV headers, Python identifiers, and technical field names must stay in their original language if they are part of the project format.

Do not translate game classnames, JSON keys, paths, or code identifiers.

## Important folders

- `raw/` contains original game data files.
- `data/` contains generated indexes.
- `src/` contains parser and builder code.
- `tests/` contains tests.
- `workspace/active_context.json` contains the current active workflow context.

Never modify files in `raw/`.

## Session and active context rule

When the user asks about the current session, active context, current campaign, pack, stage, quest, task, or selected templates, always read `workspace/active_context.json` first.

Treat `workspace/active_context.json` as the project source of truth for the active workflow context. Do not answer those questions from memory or from generic project instructions before checking this file.

Use the active context to locate campaign files, for example:

```text
campaigns/<campaign_id>/<pack_id>/stage3_quests.txt
campaigns/<campaign_id>/<pack_id>/context_pack.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.json
```

If the active context file is missing, invalid, or incomplete, say that clearly and then infer from nearby campaign/output files only with an explicit caveat.

## Current task

Build data indexes from raw game files.

Input sources:

### `raw/locations/`

Location objects.

Important fields:

- `code`
- `title`
- `tags`
- `garbage_assets`

Locations connect garbage to places.

Example meaning:

```text
location -> garbage_assets -> garbage classname
raw/garbage/

Garbage AssetPrototype objects.

Garbage is identified by:

group = "garbage"

Important fields:

classname
title
id
group
subgroup
rand_reward
rand_reward_in_guest

Garbage can drop collection elements through reward structures.

Parse:

rand_reward as mode = "home"
rand_reward_in_guest as mode = "guest"
raw/flowers/

Flower or seed AssetPrototype objects.

Flowers are identified by:

group = "seeds"
subgroup = "flower"

Important fields:

classname
title
id
tags
price
req_user_level
meta_info
rand_reward
rand_reward_in_guest

Flowers can drop collection elements through reward structures.

Parse:

rand_reward as mode = "home"
rand_reward_in_guest as mode = "guest"

For flowers:

mode = "home" means collecting the flower at home.
mode = "guest" means collecting the flower in a friend's home.

Flowers are not connected to locations through garbage_assets.

raw/collections/

Collection AssetPrototype objects.

Collection elements are identified by:

group = "collection"

Important fields:

classname
title
id
group
subgroup

Collection titles are required for quest task titles and hints.

Required generated outputs

Generate these files:

data/master_index.json
data/garbage.index.json
data/flowers.index.json
data/collections.index.json
data/drops.index.json
data/validation_report.json
master_index.json

The master index should contain:

locations_by_code
locations_by_garbage
garbage_by_classname
flowers_by_classname
collections_by_classname
summary metadata
drops.index.json

This should be a flat list of drop links.

It must include both:

garbage -> collection
flower -> collection

Every drop record must include universal fields:

source_type
source_classname
source_title
source_id
collection_classname
collection_title
collection_id
mode
reward_group_p
asset_p

For garbage drops, also include:

garbage_classname
garbage_title
garbage_id
locations

For flower drops, also include:

flower_classname
flower_title
flower_id
flower_tags
req_user_level
locations: []
Reward parsing rules

Reward structures can be nested.

Search recursively for dictionaries with an asset field.

If the asset value points to an existing collection classname, create a drop link.

Preserve raw probability fields:

reward_group_p
asset_p

Do not calculate final probability yet.

For example:

{
  "p": 33,
  "one_of": [
    {
      "asset": "Fl6Col1",
      "p": 20
    }
  ]
}

Should produce:

{
  "reward_group_p": 33,
  "asset_p": 20
}
Strict data rules

Do not invent game facts.

The following fields must come only from parsed data:

location code
location title
location tags
garbage classname
garbage title
flower classname
flower title
collection classname
collection title

If something is missing, write a warning or error to validation_report.json.

Validation rules

Create data/validation_report.json.

Add warnings for:

location has garbage_assets, but a garbage classname is missing from garbage_by_classname
garbage object has no title
flower object has no title
collection object has no title
location has no title
location has no tags
location has empty or null garbage_assets
garbage exists but is not used in any location

Add errors for:

reward references an asset that looks like a collection but is missing from collections_by_classname
duplicate garbage classname
duplicate flower classname
duplicate collection classname
duplicate location code
CLI

Create a CLI command:

python src/build_index.py

The command must:

Read raw files.
Build all indexes.
Write files to data/.
Print summary statistics.

Required printed statistics:

locations found
garbage found
flowers found
collections found
garbage drop links created
flower drop links created
errors
warnings
Future goal

Later this project will use the generated indexes to fill quest task templates and export CSV files.

Do not implement CSV generation now.

Do not implement quest generation now.

## Quest-ready validation policy

Raw validation issues are not always critical.

The project must distinguish:

- raw validation issues
- non-critical issues
- critical issues
- quest-ready data

Quest generation must use only quest-ready indexes.

### Non-critical issues

The following issues are non-critical for quest generation:

#### `location_empty_garbage_assets`

A location with empty or null `garbage_assets` is not needed for quest generation.

Exclude it from `quest_ready_locations`.

#### `location_unknown_garbage`

If a location references garbage that is missing from `raw/garbage`, ignore that garbage.

Reason:

The user manually placed all needed garbage prototypes into `raw/garbage`.

Unknown garbage entries are not needed for quest generation.

#### `garbage_unused_in_locations`

If garbage exists in `raw/garbage` but is not used by any quest-ready location, it is not needed for quest generation.

Exclude it from `quest_ready_garbage`.

#### `missing_collection_asset` for ignored patterns

If a missing collection asset contains one of these fragments:

- `Cocoon`
- `Web`
- `Common`
- `Mold`

then it is non-critical.

These collection assets are not needed for quest generation.

Do not create drop links for them.

Do not treat them as critical errors.

Do not automatically exclude the source garbage only because it has ignored reward assets.

A garbage object can still be useful for `garbage classname` tasks even if some of its reward assets are ignored.

#### `missing_collection_asset` from excluded garbage

If the source garbage is excluded from `quest_ready_garbage`, then missing collection assets from this garbage are non-critical.

### Critical issues

Only issues that affect quest-ready data are critical.

Critical issues include:

- quest-ready garbage has no title
- quest-ready flower has no title
- quest-ready collection has no title
- quest-ready drop references a missing collection asset that is not ignored by policy
- duplicate classname
- duplicate location code

### Required quest-ready outputs

Generate:

- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`
- `data/non_critical_issues.json`
- `data/critical_issues.json`
- `data/excluded_entities.json`
- `data/validation_summary.md`

### Future generation rule

Future quest and CSV generation must use only:

- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`

Do not use raw indexes directly for generation.
