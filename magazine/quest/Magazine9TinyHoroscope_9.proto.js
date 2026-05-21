{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_9",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 9,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconSagittarius",
  "title": "Домовенок-стрелец",
  "description": "«Без правды жить — с бела света бежать»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:9+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3421",
      "title": "Вырасти Фуксии",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerFuchsia",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3422",
      "type": "get_asset",
      "classname": "PestCollection5",
      "title": "Найди деревянный лук",
      "amount": 10,
      "price": 20
    },
    {
      "identifier" : "e3423",
      "type": "get_asset",
      "classname": "Spear",
      "title": "Сделать Копьё",
      "amount": 4,
      "price": 30
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Sagittarius"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Sagittarius", "amount": 1}
  ],

  "id" : 53494
}