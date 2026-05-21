{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_4",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 4,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconCancer",
  "title": "Домовёнок-рак",
  "description": "«Мой дом — моя крепость»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:4+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3406",
      "title": "Вырасти Синие розы",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerBlueRose",
      "amount": 150,
      "price": 30
    },
    {
      "identifier" : "e3407",
      "title": "Убери речных раков",
      "type":"garbage",
      "classname":"Crayfish",
      "amount": 30,
      "price": 30
    },
    {
      "identifier" : "e3408",
      "type": "get_asset",
      "classname": "Delicacy",
      "title": "Сделать Деликатес",
      "amount": 2,
      "price": 20
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Cancer"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Cancer", "amount": 1}
  ],

  "id" : 53489
}