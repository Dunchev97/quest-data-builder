# Reviewed Fun14 potekha references

These rules apply to `quest-data-builder` and its reviewed Fun14 interactive objects. They do not change unrelated quest/adventure template modes.

## Source and reuse

- `data/fun_interactive_object_templates.json:reviewed_templates` selects the authoritative `conf` in `docs/FunCollection/Fun14/` for `Exchanger`, `FunCollection_3`, `_4`, `_5`, `_7`, `_8` and `workbench_single`. Total: 168 prototype definitions.
- These seven reference XLSX have `input = output` pointing to existing Fun14 prototypes and blank IDs. The user-reviewed working XLSX retain their assigned IDs.
- Historical `docs/FunCollection/FunCollection_N.xlsx` and parameterized `templates[].blocks` are legacy references for older layouts. Do not use them in place of a promoted Fun14 family.
- Start a new event with `python src/reviewed_proto_templates.py FunCollection_7 --prefix Fun15 --output output/Fun15_FunCollection_7.xlsx`. This copies the verified structure, keeps real Fun14 inputs, rewrites outputs/mechanical references, adds the source-prefix replacement and leaves IDs blank. It is a technical starting point; fill the new theme and confirm the new event's locations, weeks and art.
- The same-event reviewed tables can remain self-referencing. A new output becomes a valid self-input only after that prototype actually exists. Test full JSON equality and two successive conversions before promoting new tables.
- Use the current user folder first. An unrelated new workbook in that folder does not enter an explicitly selected set automatically.

## Audit decisions to preserve

- Compare both parameter counts and types. A one-key difference may expose an object overwritten with a string. Verify intended fields against real converter output and distinguish mechanical references from graphics.
- `view_classname` may intentionally retain Fun10–Fun13/BD23 or other existing art names. Preserve it unless the user changes that visual. The replacement audit excludes only this key; stale asset/reward/conditions references still need review.
- Output directory names must also belong to the target event: `/asset_package/HeavenlyExotic/Fun14_*.proto.js` is wrong even though the filename contains Fun14. `/asset_package/Fun14/...` and existing `/asset_package/Fun/Fun14/...` layouts are valid; root `/post_action/...Fun14...` is valid.
- Gift conversion stays an object: `transformation_to_other_asset_while_gifting.asset=<result classname>`. A bare string assigned to `transformation_to_other_asset_while_gifting` does not supply the reward spec expected by the server.
- The reviewed `FunCollection_4_REAL` directly awards one of CL_1..10 with weights `20,20,20,20,15,15,3,3,2,2`. Its optional MB_1 definition is retained but is not used by REAL. Do not restore the MB route without a new request.
- Omitted reward `amount` means 1 in this checkout's `RandomRewardConf`. A shorter field count is not automatically a lost reward.
- Keep numeric IDs from supplied ranges in working XLSX, never allocate a new range implicitly. Reference copies/new-event templates have blank IDs; blank IDs inherit donor IDs during conversion, so assign production IDs separately before import.

## Confirmed Fun14 configuration (reference-specific)

All existing object placement/state-return `location`/`to_location` fields use **411**. GR tags were preserved; their display names were updated:

| Tag | Code | Name |
|---|---:|---|
| Fun14_loc_1 | 411 | Праздничная площадь |
| Fun14_loc_2 | 412 | Сладкий Мир |
| Fun14_loc_3 | 413 | Мир Оригами |
| Fun14_loc_4 | 414 | Травяное царство |
| Fun14_loc_5 | 415 | Звёздные Просторы |
| Fun14_loc_6 | 416 | Мир Льда и Пламени |
| Fun14_loc_7 | 418 | Пластилиновый мир |

Week mapping is explicit: `FunCollection_7 → Tech_Weekly_1`, `3 → 2`, `4 → 3`, `8 → 4`, `5 → 5`. Preserve the remaining condition clauses, including `multiplicity`. Do not infer a week from the collection number. `Tech_Weekly_3` and `_5` prototype bodies were excluded from these table edits.

These locations/weeks are Fun14 decisions, not universal defaults for another event. See `workflows/FUN_INTERACTIVE_OBJECT_WORKFLOW.md` for the authoring workflow.
