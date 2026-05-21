{
  "class": "QuestPrototype",
  "identifier": "Magazine9Search_1",
  "disabled": 1,
  "disabled_ru": 0,
  "position": 1,
  "is_root": 1,
  "is_hidden": 1,
  "group_identifier": "Magazine9Search",
  "title": "Подсказка №1",
  "description": "Тут сорока точна была - ответ однозначен.\nДля супа черпак безнадёжно утрачен.\nИ какая речь об интеллигенции?\nОставила немытую посуду и грязные полотенца.",
  "on_activate": [
    {"do": "add_stuff", "classname": "Magazine9SearchClue_1", "x": 187, "y": 372, "location": 86},
    {"do": "display_window", "type": "magazine_search", "view": "Magazine9SearchViewWindow", "quest_id": "Magazine9Search_1"}
  ],
  "on_accomplish": [
    {"do": "remove_asset", "classname": "Magazine9SearchKey_1"},
    {"do": "remove_stuff", "classname": "Magazine9SearchClue_1"},
    {"do": "display_window", "type": "magazine_search", "view": "Magazine9SearchViewWindow", "quest_id": "Magazine9Search_2"}
  ],
  "tasks": [
    {
      "identifier" : "e3399",
      "type": "action",
      "action": "clean_debris",
      "param": "Magazine9SearchClue_1",
      "title": "Найди Кастрюля с черпаком",
      "price": 15,
      "amount": 1
    }
  ],
  "opens": ["Magazine9Search_2"],
  "id" : 53522
}