{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_3",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 3,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconTwins",
  "title": "Домовёнок-Близнецы",
  "description": "«Брось его в море — вынырнет с рыбой в зубах»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:3+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3403",
      "title": "Вырасти  Антуриумы",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerMagazine8_Anthurium",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3404",
      "type":"garbage",
      "classname":"Trowel",
      "title": "Убери мастерки",
      "amount": 35,
      "price": 30
    },
    {
      "identifier" : "e3405",
      "type": "get_asset",
      "classname": "Amulet",
      "title": "Сделай амулет",
      "amount": 1,
      "price": 20
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Twins"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Twins", "amount": 1}
  ],

  "id" : 53488
}