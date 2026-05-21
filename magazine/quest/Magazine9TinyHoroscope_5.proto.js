{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_5",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 5,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconLion",
  "title": "Домовёнок-лев",
  "description": "«Волков бояться — в лес не ходить»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:5+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3409",
      "title": "Вырасти Пионы",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerPeony",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3410",
      "type": "get_asset",
      "classname": "BrokenMaskCollection2",
      "title": "Найди маски льва",
      "amount": 7,
      "price": 35
    },
    {
      "identifier" : "e3411",
      "type": "get_asset",
      "classname": "Medicine",
      "title": "Сделать лекарство",
      "amount": 1,
      "price": 15
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Lion"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Lion", "amount": 1}
  ],

  "id" : 53490
}