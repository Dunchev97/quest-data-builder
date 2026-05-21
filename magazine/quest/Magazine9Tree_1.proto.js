{
  "class": "QuestPrototype",
  "identifier": "Magazine9Tree_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "reward": "asset=Magazine9_Tree_Viburnum:1",
  "group_identifier": "Magazine9Tree",
  "title": "Калина",
  "description": "Как вырастить дерево?",
  "conditions": "quest_active_or_finished=Magazine9_1",

  "tasks": [
    {
      "identifier": "e3327",
      "type": "have_asset",
      "classname": "Magazine9_WateringCan",
      "title": "Получи леечки с бабочкой",
      "only_in_inventory": 1,
      "always_refresh_progress": 1,
      "amount": 25,
      "post_id": "ask_for_Magazine9_WateringCan",
      "price": 10
    },
    {
      "identifier": "e3328",
      "type": "get_asset",
      "classname": "BigHome_Garbage_Nursery_MomsPortrait_Collection4",
      "title": "Найди поделки",
      "amount": 3,
      "price": 15
    },
    {
      "identifier": "e3329",
      "type": "get_asset",
      "classname": "WaterBucket",
      "title": "Получи ведра воды",
      "amount": 100,
      "price": 10
    }
  ],

  "on_accomplish": [
    {"do": "remove_asset",	"classname": "Magazine9_WateringCan", "amount": 25},
    {"do": "show_bonus_reward", "icon": "Magazine9_Tree_Viburnum"},
    {"do": "add_asset", "classname": "Magazine9_Tree_Hidden", "amount": 1}
  ],

  "id": 53277
}