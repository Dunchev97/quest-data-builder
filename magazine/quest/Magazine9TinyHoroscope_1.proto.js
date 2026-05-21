{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 1,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconAries",
  "title": "Домовёнок-Овен",
  "description": "«Голова без пылкости — все равно, что бесплодное дерево»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:1+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3385",
      "title": "Собери Герберы",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerNine",
      "amount": 150,
      "price": 30
    },
    {
      "identifier" : "e3386",
      "title": "Убери Клыки",
      "type":"garbage",
      "classname":"Tush",
      "amount": 25,
      "price": 26
    },
    {
      "identifier" : "e3387",
      "title": "Сделать Копьё",
      "type": "get_asset",
      "classname": "Spear",
      "amount": 3,
      "price": 24
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Aries"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Aries", "amount": 1}
  ],

  "id" : 53482
}