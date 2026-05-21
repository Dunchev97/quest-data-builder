{
  "class": "QuestPrototype",
  "identifier": "Magazine9Diy_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9Diy",
  "title": "Душевая кабина 1",
  "conditions": "quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier": "e3363",
      "type": "get_asset",
      "classname": "BarometerCollection1",
      "title": "Найди гидрокостюмы",
      "amount": 15,
      "price": 18
    },
    {
      "identifier": "e3364",
      "type": "action",
      "action": "take_crop",
      "param": "FlowerOne",
      "amount": 100,
      "price": 14,
      "title": "Вырасти нарциссы"
    },
    {
      "identifier": "e3365",
      "type": "garbage",
      "in_guest": 1,
      "classname": "TurbidWater",
      "amount": 100,
      "title": "Убери мутную воду в гостях",
      "price": 15
    }
  ],

  "id": 53346,
  "opens": ["Magazine9Diy_2"]
}