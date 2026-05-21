{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_2",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 2,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconTaurus",
  "title": "Домовёнок-Телец",
  "description": "«Чтоб и здесь найти, и там не потерять»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:2+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3400",
      "title": "Собери Тюльпаны",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerThree",
      "amount": 150,
      "price": 30
    },
    {
      "identifier" : "e3401",
      "title": "Найди шлем викинга",
      "type":"get_asset",
      "classname":"Garbage_HelmetCollection4",
      "amount": 15,
      "price": 30
    },
    {
      "identifier" : "e3402",
	  "title": "Сделать Бидончик молока",
      "type": "get_asset",
      "classname": "CanOfMilk", 
      "amount": 1,
      "price": 20
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Taurus"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Taurus", "amount": 1}
  ],

  "id" : 53487
}