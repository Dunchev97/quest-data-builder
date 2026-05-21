{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_8",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "position" : 8,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "icon": "Magazine9TinyHoroscope_IconScorpion",
  "title": "Домовёнок-скорпион",
  "description": "«Око за око, зуб за зуб»",
  "conditions": "stuff=Magazine9TinyHoroscope_Memory:1+stuff_extra=Magazine9TinyHoroscope_Memory:8+quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier" : "e3418",
      "title": "Вырасти Петунии",
	  "type":"action",
      "action":"take_crop",
      "param":"FlowerPetunia",
      "amount": 200,
      "price": 30
    },
    {
      "identifier" : "e3419",
      "type": "get_asset",
      "classname": "BigHome_Garbage_Overview_LizardTooth_Collection2",
      "title": "Найди морской скорпион",
      "amount": 7,
      "price": 20
    },
    {
      "identifier" : "e3420",
      "type": "get_asset",
      "classname": "BigHome_Resource_ForkFinal",
      "title": "Сделать Расписную вилку",
      "go_to_location" : 
      [
        {
          "classname" : "BigHome_ExchangeCutlery"
        }
      ],
      "amount": 2,
      "price": 30
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_TinyHoroscope_Poster_Scorpion"},
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Poster_Scorpion", "amount": 1}
  ],

  "id" : 53493
}