# Форматы диалога и экшена

Источники структуры: `server/prototypes/user_interface/dialog/Oseniny_2026/Oseniny_2026_Dialog_1.proto.js` и `server/prototypes/quest_action/Oseniny_2026/Oseniny_2026_Character_2_Dialog_2.proto.js`. Оба содержат JSON, но имеют расширение `.proto.js` и разные `class`.

Постоянные поля и один кадр с персонажем слева:

```json
{
  "class": "UserInterfacePrototype",
  "identifier": "<имя файла без .proto.js>",
  "type": "ui_dialog",
  "processor": "ui_template",
  "params": {
    "view_class": "Temp_Dialog_Window",
    "dialog": [
      {
        "character_left": {
          "view_class": "<точный classname текущей эмоции>",
          "flip": "horizontal",
          "offset": { "x": 0, "y": 0 },
          "transition": { "in": "dialog_effect_light_in", "out": "dialog_effect_light_out" }
        },
        "speech_bubble": {
          "target_character": "left",
          "texts": { "speaker_tf": "<одно имя персонажа>", "text_tf": "<одна реплика>" },
          "transition": { "in": "dialog_effect_light_in", "out": "dialog_effect_light_out" }
        },
        "transition": { "in": "dialog_effect_light_in", "out": "dialog_effect_light_out" }
      }
    ]
  },
  "id": 1
}
```

Для каждого следующего текста добавляется ещё один элемент массива `params.dialog`. Если присутствует персонаж справа, в каждом кадре добавляется `character_right` с теми же полями персонажа; у его реплик `target_character` равен `right`. Если в брифе указан только один персонаж, вторую сторону не заполняй. По требованию пользователя `flip` добавляется каждому присутствующему персонажу, даже если в исходном образце оно отсутствует у персонажа справа.

Парный экшен создаётся отдельно в `server/prototypes/quest_action/<campaign_id>/`:

```json
{
  "class": "QuestActionPrototype",
  "identifier": "<имя файла экшена без .proto.js>",
  "work_without_proof": 1,
  "conditions": "<точная строка из анкеты>",
  "stuff_actions": [
    {
      "do": "show_user_interface",
      "identifier": "<identifier UI-диалога>"
    }
  ],
  "id": 1
}
```

ID экшена и диалога различаются. В `stuff_actions[0].identifier` записывается именно `identifier` UI-файла, а не имя action-файла.
