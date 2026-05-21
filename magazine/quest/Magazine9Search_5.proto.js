{
  "class": "QuestPrototype",
  "identifier": "Magazine9Search_5",
  "disabled": 1,
  "disabled_ru": 0,
  "position": 5,
  "is_hidden": 1,
  "reward": "asset=Magazine9_SearchReward:1",
  "group_identifier": "Magazine9Search",
  "title": "Подсказка №5",
  "description": "Работа не идёт, посуда не клеится,\nГончарный круг больше не вертится.\nПропала корзинка шурупов и гаек -\nНапрочь подорвано доверие домохозяек.",
  "on_activate": [
    {"do": "add_stuff", "classname": "Magazine9SearchClue_5", "x": 250, "y": 372, "location": 3}
  ],
  "on_accomplish": [
    {"do": "remove_asset", "classname": "Magazine9SearchKey_5"},
    {"do": "remove_stuff", "classname": "Magazine9SearchClue_5"},
    {"do": "add_asset", "classname": "Magazine9_Search_Hidden", "amount": 1},

        {
          "do" : "display_window",
          "type" : "simple",
		  "is_info" : 1,
          "window_spec" : 
          {
            "view_window" : "Magazine9SearchCongratulations",
            "btns" : [{"type" : "simple", "mc" : "close_btn", "action":"action_Magazine9_Search_Congratulations"}]
          }
        }
		
  ],
  "tasks": [
    {
      "identifier" : "e3427",
      "type": "action",
      "action": "clean_debris",
      "param": "Magazine9SearchClue_5",
      "title": "Найди Коробка шурупов",
      "price": 15,
      "amount": 1
    }
  ],
  "id" : 53526
}