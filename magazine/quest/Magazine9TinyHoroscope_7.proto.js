{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_7",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 7,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconScales",
  "title": "Домовята-весы",
  "description": "«Хорошо там, где нас нет»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:7+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3415",
      "title": "Вырасти Лилии",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerFour",
      "amount": 150,
      "price": 30
    },
    {
      "identifier" : "e3416",
      "type": "get_asset",
      "classname": "RarityCollection1",
      "title": "Найди сломанные весы",
      "amount": 7,
      "price": 30
    },
    {
      "identifier" : "e3417",
      "type": "get_asset",
      "classname": "GlassFlask",
      "title": "Сделать Стеклянную колбу",
      "amount": 2,
      "price": 10
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Scales"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Scales", "amount": 1}
  ],

  "id" : 53492
}