---
name: prototype-table-template
description: "Analyze a user-provided prototype file or donor artifact and turn it into a reusable table/CSV/XLSX template. Use when the user asks to create a template for tables, Excel, CSV, conf sheets, generated object tables, or dev-ready spreadsheets based on a prototype, sample .proto.js, JSON-like object, XLSX, CSV, or similar donor file."
---

# Prototype Table Template

## Core Workflow

Use this skill when the user gives a prototype and wants a reusable table template, not just a one-off explanation.

1. Read the prototype from source.
   - Prefer the exact file the user attached or referenced.
   - If the file is JSON-like JavaScript, parse structurally where possible; tolerate comments/trailing commas only after inspecting format.
   - If the file is XLSX/CSV, read the actual sheet/range and preserve existing block order, headers, and donor paths unless the user asks to redesign them.

2. Map the mechanic.
   - Identify class/type, primary object id/classname, title, groups, behaviours/actions, prices, rewards, conditions, progress/counters, windows, icons, visual actions, packages, recipes, and generated resources.
   - Separate fixed structure from theme-specific values.
   - Mark stale donor-only fields that must be removed or replaced in the new template.

3. Define the template contract.
   - Choose a stable template id and mechanic prefix.
   - List required user fields, optional fields, defaults, list fields, resource suffixes, and numbering rules.
   - Define classname/output patterns with placeholders such as `{prefix}`, `{campaign_id}`, `{object_number}`, `{resource_suffix}`.
   - Normalize obvious suffix typos when the pattern is clear, for example `GR2` -> `GR_2`.

4. Convert to table blocks.
   - Preserve donor `input` paths as donor references.
   - Generate target `output`, `classname`, `file_name`, `identifier`, `reward`, `ingredients`, `conditions`, `view_classname`, `stuff_icon`, `pack_asset`, and related fields from the new prefix.
   - Leave `id` blank unless the user explicitly provides ids.
   - Keep one logical block per object/resource/action/package/recipe/global reward.
   - If the final artifact is XLSX, put the dev table on a `conf` sheet unless the project convention says otherwise.

5. Implement in the local project when appropriate.
   - Prefer existing project generators, template registries, validators, and CSV/XLSX helpers over ad hoc generation.
   - Add or update tests for at least one realistic sample based on the user's data.
   - Do not edit raw donor data unless the user explicitly requests it.

6. Verify the generated artifacts.
   - Read generated CSV/XLSX back with the correct encoding.
   - Assert that required Russian titles, classnames, rewards, prices, and output paths are present.
   - Assert that forbidden stale donor markers are absent.
   - For XLSX, render or inspect at least the key sheet/range and scan for formula errors.
   - Run the narrow validator/test for the changed workflow; run broader tests if code, templates, or workflow docs changed.

7. Report the result.
   - Explain the principle of the new template briefly.
   - List the created/changed files.
   - Include the final CSV/XLSX link when an artifact was created.
   - Mention any assumption, especially if the prototype had fields whose runtime behavior is not visible in the file.

## Analysis Checklist

Use this checklist while reading the prototype:

- What does the player/user action consume?
- What does it always or randomly produce?
- Which fields are user-facing text?
- Which fields are technical ids that must follow prefix/numbering rules?
- Which arrays are weighted pools, ordered lists, or conditional branches?
- Which conditions gate behavior?
- Which fields are visual-only and should not survive if the mechanic changes?
- Which resources need assets, packages, post actions, recipes, or global rewards?
- Which values are donor leftovers and must be replaced?

## Template Output Checklist

Before finalizing, make sure the template has:

- Stable `template_id`.
- Clear required fields and defaults.
- Classname patterns for object, resources, actions, recipes, packages, and outputs.
- Exact table block names and headers.
- Sample data filled from the user's example.
- Validation notes for stale donor markers and encoding.
