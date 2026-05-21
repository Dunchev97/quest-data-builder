{
  "class": "QuestPrototype",
  "identifier": "Magazine9Stone_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "reward": "",
  "group_identifier": "Magazine9Stone",
  "title": "Хризолит",
  "conditions": "quest_active_or_finished=Magazine9_1",
  "pass_conditions": "asset_or_stuff=MagazineStoneBeryl:1",
  "on_activate": [
    {"do": "add_random_stuffs", "classname": "MagazineStonePileBerylMacadam", "amount":99, "locations_tags":["rnd_old_home","rnd_new_home"]},
    {"do": "add_random_stuffs", "classname": "MagazineStonePileBeryl",        "amount": 1, "locations_tags":["rnd_old_home","rnd_new_home"]}
  ],
  "on_accomplish": [
    {"do": "remove_stuff", "classname": "MagazineStonePileBerylMacadam"},
    {"do": "add_asset", "classname": "Magazine9_Stone_Hidden", "amount": 1}
  ],
  "tasks": [
    {
      "identifier": "e3320",
      "type": "action",
      "action": "clean_debris",
      "icon": "clean_debris",
      "param": "MagazineStoneBeryl",
      "title": "Найди хризолит",
      "price": 5,
      "amount": 1
    }
  ],
  "id": 53260
}