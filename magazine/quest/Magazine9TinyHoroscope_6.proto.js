{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_6",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 6,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconVirgo",
  "title": "Домовёнок-дева",
  "description": "«Без дела жить — только небо коптить»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:6+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3412",
      "title": "Вырасти Колокольчики",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerTen",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3413",
      "type": "get_asset",
      "classname": "WebStoveCollection1",
      "title": "Найди горшочки",
      "amount": 7,
      "price": 30
    },
    {
      "identifier" : "e3414",
      "type": "get_asset",
      "classname": "Ring",
      "title": "Сделать Перстень",
      "amount": 1,
      "price": 20
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Virgo"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Virgo", "amount": 1}
  ],

  "id" : 53491
}