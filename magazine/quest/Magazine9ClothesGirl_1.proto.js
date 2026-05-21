{
  "class": "QuestPrototype",
  "identifier": "Magazine9ClothesGirl_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "reward": "",
  "group_identifier": "Magazine9ClothesGirl",
  "title": "Костюм Червовой Королевы",
  "description": "Открой для себя сказочное очарование мира маленькой Алисы!",
  "conditions": "quest_active_or_finished=Magazine9_1+personage_sex=female",
  "pass_conditions": "asset_or_stuff=Magazine9ClothesGirl_Body:1+asset_or_stuff=Magazine9ClothesGirl_Head:1+asset_or_stuff=Magazine9ClothesGirl_Earring:1+asset_or_stuff=Magazine9ClothesGirl_Boot:1+asset_or_stuff=Magazine9ClothesGirl_Neck:1+asset_or_stuff=Magazine9ClothesGirl_Wings:1+asset_or_stuff=Magazine9ClothesGirl_Glove:1",

  "tasks": [
    {"identifier": "e3343", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Body"},
    {"identifier": "e3344", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Head"},
    {"identifier": "e3345", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Earring"},
    {"identifier": "e3346", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Boot"},
    {"identifier": "e3361", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Glove"},
    {"identifier": "e3362", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Wings"},
    {"identifier": "e3347", "type": "have_asset", "always_refresh_progress": 1, "amount": 1, "classname": "Magazine9ClothesGirl_Neck"},

    {"identifier": "e3348", "type": "have_location", "location_index":1, "title":"Служебное задание"},
    {"identifier": "e3349", "type": "have_location", "location_index":1, "title":"Служебное задание"},
    {"identifier": "e3350", "type": "have_location", "location_index":1, "title":"Служебное задание"}
  ],

  "on_accomplish": [
    {"do": "add_asset", "classname": "Magazine9_Clothes_Hidden", "amount": 1},
    {"do": "show_post_action", "identifier": "quest_Magazine9ClothesGirl_1_accomplished"}
  ],

  "id": 53307
}