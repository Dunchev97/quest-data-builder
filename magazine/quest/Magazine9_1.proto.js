{
  "class": "QuestPrototype",
  "identifier": "Magazine9_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "show_group_title_on_mouse_over": 1,
  "reward": "asset=Magazine9_FinalReward:1",
  "group_identifier": "Magazine9",
  "hide_progress_arrow": 1,
  "title": "Журнал №9",
  "conditions": "level>10",
  "conditions_my_mail_test": "level>10",
  "conditions_my_mail_test_prod": "level>10",
  "on_activate": [{"do": "refresh_magazine_likes", "magazine_identifier": "Magazine9"}],
  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_FinalReward"},
    {"do": "show_post_action", "identifier": "quest_Magazine9_1_accomplished"}
  ],
  "tasks": [
    {"identifier": "e3428", "type": "have_asset", "classname": "Magazine9_Stone_Hidden",   "only_in_inventory": 1, "amount": 1, "title":  "3"},
	{"identifier": "e3429", "type": "have_asset", "classname": "Magazine9_Flower_Hidden",  "only_in_inventory": 1, "amount": 1, "title":  "4"},
	{"identifier": "e3430", "type": "have_asset", "classname": "Magazine9_Tree_Hidden",    "only_in_inventory": 1, "amount": 1, "title":  "5"},
	{"identifier": "e3431", "type": "have_asset", "classname": "Magazine9_Animal_Hidden",  "only_in_inventory": 1, "amount": 1, "title":  "6"},
	{"identifier": "e3432", "type": "have_asset", "classname": "Magazine9_Photo_Hidden",   "only_in_inventory": 1, "amount": 1, "title":  "7"},
	{"identifier": "e3433", "type": "have_asset", "classname": "Magazine9_Clothes_Hidden", "only_in_inventory": 1, "amount": 1, "title":  "8"},
	{"identifier": "e3434", "type": "have_asset", "classname": "Magazine9_Diy_Hidden",     "only_in_inventory": 1, "amount": 1, "title":  "9"},
	{"identifier": "e3435", "type": "have_asset", "classname": "Magazine9_Achieve_Hidden",     "only_in_inventory": 1, "amount": 1, "title":  "22"},
	{"identifier": "e3436", "type": "have_asset", "classname": "Magazine9_Search_Hidden",     "only_in_inventory": 1, "amount": 1, "title":  "23"},
	{"identifier": "e3437", "type": "have_asset", "classname": "Magazine9_Domovestnik_Hidden",     "only_in_inventory": 1, "amount": 1, "title":  "24"},
	{"identifier": "e3438", "type": "have_asset", "classname": "Pet13_10", "amount": 1, "title":  "26"},
    {"identifier": "e3319", "type": "action", "action": "Magazine9", "param": "take_magazine_surprise", "amount": 1}
  ],
  "id": 53258
}