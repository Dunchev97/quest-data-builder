{
  "class": "QuestPrototype",
  "disabled": 1,
  "disabled_ru": 0,
  "disabled_my_mail_test": 0,
  "disabled_my_mail_test_prod": 0,
  "identifier": "TrophyPet17_Sport_9",
  "title": "Волейболистка",
  "group_identifier": "Trophy",
  "is_hidden": 1,
  "pass_conditions": "asset=TrophyPet17_Sport_9:1",
  "conditions": "asset_or_stuff=Pet17_Sport_9:1",
  "on_accomplish": [
    {
      "do": "remove_asset",
      "classname": "TrophyPet17_Sport_9"
    },
    {
      "do": "add_stuff",
      "classname": "TrophyPet17_Sport_9",
      "location": 75,
      "x": 0,
      "y": 0
    },
    {
      "do": "show_trophy_wow_effect",
      "icon": "TrophyPet17_Sport_9"
    }
  ],
  "tasks": [
    {
      "identifier": "e9802",
      "title": "Теннисистка",
      "type": "action",
      "action": "feed_pet_happy",
      "param": "Pet17_Sport_9",
      "amount": 20,
      "price": 30
    }
  ],
  "id": 68371
}