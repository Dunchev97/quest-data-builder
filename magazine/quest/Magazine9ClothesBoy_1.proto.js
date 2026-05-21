{
  "class": "QuestPrototype",
  "identifier": "Magazine9ClothesBoy_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "reward": "",
  "group_identifier": "Magazine9ClothesBoy",
  "title": "Костюм Безумного Шляпника",
  "description": "Открой для себя сказочное очарование мира маленькой Алисы!",
  "conditions": "quest_active_or_finished=Magazine9_1+personage_sex=male",
  "pass_conditions": "asset_or_stuff=Magazine9ClothesBoy_Body:1+asset_or_stuff=Magazine9ClothesBoy_Head:1+asset_or_stuff=Magazine9ClothesBoy_Pants:1+asset_or_stuff=Magazine9ClothesBoy_Boot:1+asset_or_stuff=Magazine9ClothesBoy_Neck:1+asset_or_stuff=Magazine9ClothesBoy_Glove:1+asset_or_stuff=Magazine9ClothesBoy_Wings:1",

  "tasks": [
    {"identifier": "e3351", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Body"},
    {"identifier": "e3352", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Head"},
    {"identifier": "e3353", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Pants"},
    {"identifier": "e3354", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Boot"},
    {"identifier": "e3359", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Glove"},
    {"identifier": "e3360", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Wings"},
    {"identifier": "e3355", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesBoy_Neck"},

    {"identifier": "e3356", "type": "have_location", "location_index":1, "title":"Служебное задание"},
    {"identifier": "e3357", "type": "have_location", "location_index":1, "title":"Служебное задание"},
    {"identifier": "e3358", "type": "have_location", "location_index":1, "title":"Служебное задание"}
  ],

  "on_accomplish": [
    {"do": "add_asset", "classname": "Magazine9_Clothes_Hidden", "amount": 1},
    {"do": "show_post_action", "identifier": "quest_Magazine9ClothesBoy_1_accomplished"}
  ],

  "id": 53306
}
