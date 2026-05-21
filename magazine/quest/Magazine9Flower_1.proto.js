{
  "class": "QuestPrototype",
  "identifier": "Magazine9Flower_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "reward": "",
  "group_identifier": "Magazine9Flower",
  "title": "Плюмерия",
  "conditions": "quest_active_or_finished=Magazine9_1",
  "pass_conditions": "asset_or_stuff=FlowerMagazine9_PlumeriaCondition:1",
  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "FlowerMagazine9_PlumeriaCondition"},
    {"do": "add_asset", "classname": "Magazine9_Flower_Hidden", "amount": 1}
  ],
  "tasks": [
    {"identifier": "e3321", "type": "get_asset", "amount": 1, "price":  30, "classname": "Fl4Col1"},
    {"identifier": "e3322", "type": "get_asset", "amount": 6, "price": 11, "classname": "FlowerAlstromeriaCollection3"},
    {"identifier": "e3323", "type": "get_asset", "amount": 1, "price": 18, "classname": "FlowerMagazine6_TerryMallowCollection3"},
    {"identifier": "e3324", "type": "get_asset", "amount": 2, "price":  13, "classname": "Fl9Col2"},
    {"identifier": "e3325", "type": "get_asset", "amount": 3, "price":  12, "classname": "FlowerFuchsiaCollection5"},
    {"identifier": "e3326", "type": "get_asset", "amount": 1, "classname": "FlowerMagazine9_PlumeriaCondition"}
  ],
  "id": 53268
}