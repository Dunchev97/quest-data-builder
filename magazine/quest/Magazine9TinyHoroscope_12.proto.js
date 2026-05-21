{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_12",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 12,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconFish",
  "title": "Домовенок-рыба",
  "description": "«Жить весело, да есть нечего»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:12+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3394",
      "title": "Вырасти примулы",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerPrimula",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3395",
      "type": "get_asset",
      "classname": "FishScalesCollection2",
      "title": "Найди лещей",
      "amount": 10,
      "price": 30
    },
    {
      "identifier" : "e3396",
      "type": "get_asset",
      "classname": "FishSoup",
      "title": "Сделай уху",
      "amount": 6,
      "price": 20
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Fish"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Fish", "amount": 1}
  ],

  "id" : 53485
}