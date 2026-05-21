{
  "class": "QuestPrototype",
  "identifier": "Magazine9Animal_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "reward": "asset=Magazine9_AnimalReward:1",
  "group_identifier": "Magazine9Animal",
  "title": "Лемур",
  "conditions": "quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier": "e3330",
      "type": "get_asset",
      "classname": "WoodenCrestCollection1",
      "title": "Найди запонки",
      "amount": 1,
      "price": 5
    },
    {
      "identifier": "e3331",
      "type": "action",
      "action": "take_crop",
      "param": "FlowerOrchid",
      "amount": 40,
      "title": "Вырасти ванды",
      "price": 20
    },
    {
      "identifier": "e3332",
      "type": "action",
      "action": "send_free_gift",
      "amount": 300,
      "title": "Подари подарки друзьям",
      "price": 10
    }
  ],

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_AnimalReward"},
    {"do": "add_asset", "classname": "Magazine9_Animal_Hidden", "amount": 1},
    {"do": "show_post_action", "identifier": "quest_Magazine9Animal_1_accomplished"}
  ],

  "id": 53297
}