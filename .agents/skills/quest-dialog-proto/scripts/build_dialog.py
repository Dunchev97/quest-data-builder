#!/usr/bin/env python3
"""Build a UI dialog and its opening quest action from a structured brief."""

import argparse
import json
from pathlib import Path


TRANSITION = {"in": "dialog_effect_light_in", "out": "dialog_effect_light_out"}


def fail(message):
    raise ValueError(message)


def nonempty_string(value, label):
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value


def file_identifier(file_name, label):
    nonempty_string(file_name, label)
    if Path(file_name).name != file_name or file_name in {".", ".."}:
        fail(f"{label} must be a bare filename")
    if not file_name.endswith(".proto.js"):
        fail(f"{label} must end in .proto.js")
    return nonempty_string(file_name[: -len(".proto.js")], f"{label} identifier")


def needs_horizontal_flip(view_class, side, asset_facing):
    """An unflipped left portrait must face right; a right portrait must face left."""
    if side not in {"left", "right"}:
        fail("character side must be left/right")
    facing = asset_facing.get(view_class)
    if facing not in {"left", "right"}:
        fail(f"Missing asset_facing for {view_class}; ask which way the original asset faces")
    return facing == side


def build(brief):
    if not isinstance(brief, dict):
        fail("brief must be a JSON object")
    proto_id = brief.get("id")
    if isinstance(proto_id, bool) or not isinstance(proto_id, int) or proto_id <= 0:
        fail("id must be a positive integer")
    file_name = brief.get("file_name")
    identifier = file_identifier(file_name, "file_name")

    raw_characters = brief.get("characters")
    if not isinstance(raw_characters, list) or not 1 <= len(raw_characters) <= 2:
        fail("characters must contain one or two entries")
    characters = {}
    sides = set()
    states = {}
    for index, character in enumerate(raw_characters, 1):
        if not isinstance(character, dict):
            fail(f"character {index} must be an object")
        key = nonempty_string(character.get("key"), f"character {index} key")
        name = nonempty_string(character.get("name"), f"character {index} name")
        side = character.get("side", "left" if len(raw_characters) == 1 else None)
        if side not in {"left", "right"} or side in sides or key in characters:
            fail(f"character {index} needs a unique key and side (left/right)")
        emotions = character.get("emotions")
        if not isinstance(emotions, dict) or "базовая" not in emotions:
            fail(f"character {index} needs emotions including базовая")
        for emotion, view_class in emotions.items():
            nonempty_string(emotion, f"character {index} emotion")
            nonempty_string(view_class, f"character {index} view_class")
        asset_facing = character.get("asset_facing")
        if not isinstance(asset_facing, dict):
            fail(f"character {index} needs asset_facing by exact view_class; ask the user")
        for view_class, facing in asset_facing.items():
            nonempty_string(view_class, f"character {index} asset_facing view_class")
            if facing not in {"left", "right"}:
                fail(f"asset_facing for {view_class} must be left/right")
        initial = character.get("initial_emotion", "базовая")
        if initial not in emotions:
            fail(f"character {index} initial_emotion is not mapped")
        characters[key] = {"name": name, "side": side, "emotions": emotions,
                           "asset_facing": asset_facing}
        states[key] = initial
        sides.add(side)

    raw_lines = brief.get("lines")
    if not isinstance(raw_lines, list) or not raw_lines:
        fail("lines must be a non-empty array")
    expected = brief.get("expected_line_count")
    if expected is not None and (type(expected) is not int or expected != len(raw_lines)):
        fail("expected_line_count does not match lines")
    frames = []
    for index, line in enumerate(raw_lines, 1):
        if not isinstance(line, dict):
            fail(f"line {index} must be an object")
        speaker = line.get("speaker")
        if speaker not in characters:
            fail(f"line {index} has an unknown speaker")
        emotion = nonempty_string(line.get("emotion"), f"line {index} emotion")
        if emotion not in characters[speaker]["emotions"]:
            fail(f"line {index} has an unmapped speaker emotion")
        text = nonempty_string(line.get("text"), f"line {index} text")
        other_emotions = line.get("other_emotions", {})
        if not isinstance(other_emotions, dict):
            fail(f"line {index} other_emotions must be an object")
        for key, value in other_emotions.items():
            if key not in characters or key == speaker or value not in characters[key]["emotions"]:
                fail(f"line {index} has an invalid other_emotions entry")
            states[key] = value
        states[speaker] = emotion
        frame = {}
        for key, character in characters.items():
            view_class = character["emotions"][states[key]]
            flip = needs_horizontal_flip(view_class, character['side'], character['asset_facing'])
            frame[f"character_{character['side']}"] = {
                "view_class": view_class,
                **({"flip": "horizontal"} if flip else {}),
                "offset": {"x": 0, "y": 0},
                "transition": TRANSITION.copy(),
            }
        frame["speech_bubble"] = {
            "target_character": characters[speaker]["side"],
            "texts": {"speaker_tf": characters[speaker]["name"], "text_tf": text},
            "transition": TRANSITION.copy(),
        }
        frame["transition"] = TRANSITION.copy()
        frames.append(frame)
    return file_name, {
        "class": "UserInterfacePrototype",
        "identifier": identifier,
        "type": "ui_dialog",
        "processor": "ui_template",
        "params": {"view_class": "Temp_Dialog_Window", "dialog": frames},
        "id": proto_id,
    }


def build_action(brief, dialog_identifier):
    action = brief.get("action")
    if not isinstance(action, dict):
        fail("action must be an object with id, file_name, and conditions")
    action_id = action.get("id")
    if isinstance(action_id, bool) or not isinstance(action_id, int) or action_id <= 0:
        fail("action.id must be a positive integer")
    if action_id == brief["id"]:
        fail("action.id must differ from dialog id")
    file_name = action.get("file_name")
    identifier = file_identifier(file_name, "action.file_name")
    conditions = nonempty_string(action.get("conditions"), "action.conditions")
    return file_name, {
        "class": "QuestActionPrototype",
        "identifier": identifier,
        "work_without_proof": 1,
        "conditions": conditions,
        "stuff_actions": [
            {"do": "show_user_interface", "identifier": dialog_identifier}
        ],
        "id": action_id,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief", type=Path, help="UTF-8 JSON brief")
    parser.add_argument("--output-dir", required=True, type=Path, help="UI dialog directory")
    parser.add_argument("--action-output-dir", required=True, type=Path, help="quest action directory")
    parser.add_argument("--force", action="store_true", help="overwrite existing files")
    args = parser.parse_args()
    brief = json.loads(args.brief.read_text(encoding="utf-8-sig"))
    file_name, prototype = build(brief)
    action_file_name, action_prototype = build_action(brief, prototype["identifier"])
    output = args.output_dir / file_name
    action_output = args.action_output_dir / action_file_name
    if output.resolve() == action_output.resolve():
        parser.error("dialog and action output paths must differ")
    existing = [path for path in (output, action_output) if path.exists()]
    if existing and not args.force:
        parser.error(f"output already exists: {', '.join(map(str, existing))}; use --force to overwrite")
    output.parent.mkdir(parents=True, exist_ok=True)
    action_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(prototype, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    action_output.write_text(json.dumps(action_prototype, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    print(action_output)


if __name__ == "__main__":
    main()
