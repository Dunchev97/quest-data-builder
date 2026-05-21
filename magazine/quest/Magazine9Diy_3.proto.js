{
  "class": "QuestPrototype",
  "identifier": "Magazine9Diy_3",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "reward": "asset=Magazine9_DiyReward:1",
  "group_identifier": "Magazine9Diy",
  "title": "Душевая кабина 3",
  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_DiyReward"},
    {"do": "add_asset", "classname": "Magazine9_Diy_Hidden", "amount": 1},
    {"do": "show_post_action", "identifier": "quest_Magazine9Diy_3_accomplished"}
  ],

  "tasks": [
    {
      "identifier": "e3369",
      "type": "action",
      "action": "take_crop_in_guest",
      "param": "FlowerTwo",
      "amount": 60,
      "price": 15,
      "title": "Собери ирисы в гостях"
    },
    {
      "identifier": "e3370",
      "type": "action",
      "action": "take_crop",
      "param": "VegetableSeedCorn",
      "amount": 60,
      "price": 20,
      "title": "Вырасти кукурузу"
    },
    {
      "identifier": "e3371",
      "type": "get_asset",
      "classname": "WornGlovesCollection1",
      "title": "Найди леечки",
      "amount": 7,
      "price": 5
    }
  ],

  "id": 53344
}