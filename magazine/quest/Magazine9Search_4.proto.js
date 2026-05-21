{
  "class": "QuestPrototype",
  "identifier": "Magazine9Search_4",
  "disabled": 1,
  "disabled_ru": 0,
  "position": 4,
  "is_hidden": 1,
  "group_identifier": "Magazine9Search",
  "title": "Подсказка №4",
  "description": "Стук наковальни не слышен в домишке.\nИ тут видны следы пройдохи-воришки.\nСорока с умом приоритеты расставила:\nСерёжку взяла, дырявую калошу оставила.",
  "on_activate": [
    {"do": "add_stuff", "classname": "Magazine9SearchClue_4", "x": 400, "y": 372, "location": 8}
  ],
  "on_accomplish": [
    {"do": "remove_asset", "classname": "Magazine9SearchKey_4"},
    {"do": "remove_stuff", "classname": "Magazine9SearchClue_4"},
    {"do": "display_window", "type": "magazine_search", "view": "Magazine9SearchViewWindow", "quest_id": "Magazine9Search_5"}
  ],
  "tasks": [
    {
      "identifier" : "e3426",
      "type": "action",
      "action": "clean_debris",
      "param": "Magazine9SearchClue_4",
      "title": "Найди Серёжки",
      "price": 15,
      "amount": 1
    }
  ],
  "opens": ["Magazine9Search_5"],
  "id" : 53525
}