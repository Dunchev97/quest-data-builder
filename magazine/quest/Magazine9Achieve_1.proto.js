{
  "class": "QuestPrototype",
  "identifier": "Magazine9Achieve_1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_hidden": 1,
  "progress_arrow_id": "Magazine9_1",
  "reward": "asset=Magazine9_AchieveReward:1",
  "group_identifier": "Magazine9Achieve",
  "title": "Обнимальщик панд",
  "conditions": "quest_active_or_finished=Magazine9_1",

  "on_accomplish": [
    {"do": "show_bonus_reward", "icon": "Magazine9_AchieveReward"},
    {"do": "add_asset", "classname": "Magazine9_Achieve_Hidden", "amount": 1},
    {"do": "show_post_action", "identifier": "quest_Magazine9Achieve_1_accomplished"}
  ],

  "tasks": [
    {
      "identifier": "e3382",
      "type":"garbage",
      "location_index":25,
      "amount":75,
      "title":"Убери мусор в Селе",
      "hint":"Выйди на карту Мира, найди зону Село и нажми на нее.",
      "exclude_garbage_on_stuff":1,      
      "go_to_location":[{"location_id":25}],
      "price":15  
    },
    {
      "identifier": "e3383",
      "type": "action",
      "action": "take_crop",
      "param": "VegetableSeedTomato",
      "amount": 25,
      "price": 15,
      "title": "Вырасти помидоры"
    },
    {
      "identifier": "e3374",
      "type": "garbage",
      "in_guest": 1,
      "classname": "BottleWithNote",
      "amount": 90,
      "title": "Убери бутылки с запиской в гостях",
      "price": 14
    },
    {
      "identifier": "e3375",
      "type": "action",
      "action": "feed_any_pet",
      "title": "Покорми любого крохоньку",
      "amount": 8,
      "price": 16
    },		
    {
      "identifier": "e3376",
      "type": "get_asset",
      "classname": "GarbageNapkinsCollection5",
      "title": "Найди поварские колпаки",
      "amount": 3,
      "price": 15
    },
    {
      "identifier": "e3377",
      "type":"action",
      "action":"kill_pest",
      "amount":20,
      "title":"Прогони вредителя",
      "price":10  
    },		
    {
      "identifier": "e3378",
      "type":"action",
      "action":"clean_personage",
      "amount":7,
      "title":"Помойся",
      "price":15
    },
    {
      "identifier": "e3379",
      "title": "Получи бесплатные подарки",
      "type": "action",
      "action": "receive_free_gift",
      "amount": 800,
      "price": 20
    },
    {
      "identifier": "e3380",
      "title": "Убери бюллетени",
      "type": "garbage",
      "classname": "Bulletin",
      "amount": 20,
      "price": 24
    },
    {
      "identifier": "e3381",
      "title": "Собери горох в гостях",
      "type": "action",
      "action": "take_crop_in_guest",
      "param": "VegetableSeedPeas",
      "amount": 80,
      "price": 20
    }
  ],
  "id": 53470
}