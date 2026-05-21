{
  "class": "QuestPrototype",
  "identifier": "Magazine9TinyHoroscope_final",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "group_identifier": "Magazine9TinyHoroscope",
  "title": "Завершаем квест группу",
  "description": "Как вырастить дерево?",
  "conditions": "quest_active_or_finished=Magazine9_1+done_quest=Magazine9TinyHoroscope_1+done_quest=Magazine9TinyHoroscope_2+done_quest=Magazine9TinyHoroscope_3+done_quest=Magazine9TinyHoroscope_4+done_quest=Magazine9TinyHoroscope_5+done_quest=Magazine9TinyHoroscope_6+done_quest=Magazine9TinyHoroscope_7+done_quest=Magazine9TinyHoroscope_8+done_quest=Magazine9TinyHoroscope_9+done_quest=Magazine9TinyHoroscope_10+done_quest=Magazine9TinyHoroscope_11+done_quest=Magazine9TinyHoroscope_12",

"tasks" : 
		[
      {
        "identifier" : "e3397",
        "title":"Забрать награду",
		"hint":"Нажми на кнопку \"Забрать\"",
        "icon":"Pet13_10_NormalIcon",
        "type":"action",
        "action":"action_Magazine9_TinyHoroscope_TakeReward",
		"amount":1
      } 
    ],

  "on_accomplish": [
    {"do": "add_asset", "classname": "Magazine9_TinyHoroscope_Hidden", "amount": 1}
  ],

  "id" : 53486
}