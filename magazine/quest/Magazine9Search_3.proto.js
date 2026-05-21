{
  "class": "QuestPrototype",
  "identifier": "Magazine9Search_3",
  "disabled": 1,
  "disabled_ru": 0,
  "position": 3,
  "is_hidden": 1,
  "group_identifier": "Magazine9Search",
  "title": "Подсказка №3",
  "description": "Лягушачье кваканье наполнено спорами,\nПропали крышки от банок с помидорами.\nПодобного случая еще свет не видывал -\nПреступник налёт свой странно спланировал.",
  "on_activate": [
    {"do": "add_stuff", "classname": "Magazine9SearchClue_3", "x": 1320, "y": 372, "location": 10}
  ],
  "on_accomplish": [
    {"do": "remove_asset", "classname": "Magazine9SearchKey_3"},
    {"do": "remove_stuff", "classname": "Magazine9SearchClue_3"},
    {"do": "display_window", "type": "magazine_search", "view": "Magazine9SearchViewWindow", "quest_id": "Magazine9Search_4"}
  ],
  "tasks": [
    {
      "identifier" : "e3425",
      "type": "action",
      "action": "clean_debris",
      "param": "Magazine9SearchClue_3",
      "title": "Найди Банка с крышкой",
      "price": 15,
      "amount": 1
    }
  ],
  "opens": ["Magazine9Search_4"],
  "id" : 53524
}