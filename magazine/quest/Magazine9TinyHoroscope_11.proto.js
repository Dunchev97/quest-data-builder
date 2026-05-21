{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_11",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 11,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconAquarius",
  "title": "Домовенок-водолей",
  "description": "«С волками жить — по-волчьи выть»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:11+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3391",
      "title": "Вырасти Маргаритки",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerTwelve",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3392",
      "type":"garbage",
      "classname": "MasterSet",
      "title": "Найди разбитый набор мастера",
      "amount": 50,
      "price": 34
    },
    {
      "identifier" : "e3393",
      "type": "get_asset",
      "classname": "PickledApples",
      "title": "Сделай моченые яблоки",
      "amount": 1,
      "price": 16
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Aquarius"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Aquarius", "amount": 1}
  ],

  "id" : 53484
}