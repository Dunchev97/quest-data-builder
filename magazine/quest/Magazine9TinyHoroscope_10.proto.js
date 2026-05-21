{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_10",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 10,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconCapricorn",
  "title": "Домовенок-козерог",
  "description": "«Терпение и труд все перетрут»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:10+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3388",
      "title": "Вырасти Лилии",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerFour",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3389",
      "type": "get_asset",
      "classname": "ClayLumpCollection5",
      "title": "Найди козлика",
      "amount": 12,
      "price": 30
    },
    {
      "identifier" : "e3390",
      "type": "get_asset",
      "classname": "Ring",
      "title": "Сделать Перстень",
      "amount": 1,
      "price": 20
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Capricorn"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Capricorn", "amount": 1}
  ],

  "id" : 53483
}