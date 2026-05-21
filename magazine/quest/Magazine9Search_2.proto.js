{
  "class": "QuestPrototype",
  "identifier": "Magazine9Search_2",
  "disabled": 1,
  "disabled_ru": 0,
  "position": 2,
  "is_hidden": 1,
  "group_identifier": "Magazine9Search",
  "title": "Подсказка №2",
  "description": "Ситуация получается нелицеприятная.\nИ логика пропаж совершенно непонятная,\nПтица нахальная, ты точно здорова?\nУ коня с телегой пропала одна подкова.",
  "on_activate": [
    {"do": "add_stuff", "classname": "Magazine9SearchClue_2", "x": 1000, "y": 372, "location": 7}
  ],
  "on_accomplish": [
    {"do": "remove_asset", "classname": "Magazine9SearchKey_2"},
    {"do": "remove_stuff", "classname": "Magazine9SearchClue_2"},
    {"do": "display_window", "type": "magazine_search", "view": "Magazine9SearchViewWindow", "quest_id": "Magazine9Search_3"}
  ],
  "tasks": [
    {
      "identifier" : "e3424",
      "type": "action",
      "action": "clean_debris",
      "param": "Magazine9SearchClue_2",
      "title": "Найди Подковы",
      "price": 15,
      "amount": 1
    }
  ],
  "opens": ["Magazine9Search_3"],
  "id" : 53523
}