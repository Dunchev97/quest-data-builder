{
  "class": "AssetPrototype",
  "classname": "TrophyPet17_Sport_9",
  "title": "Медалька \"Волейболистка\"",
  "description": "Раз в день можно получить бонус.",
  "group": "chest",
  "subgroup": "collection_trophy",
  "use_asset_random_helper": 1,
  "is_hidden": 1,
  "price": 30,
  "currency": "money",
  "reward_time_interval": 86400,
  "extra": {
    "type": "pet"
  },
  "save_chest_reward_in_log": 1,
  "as_stuff_in_inventory": 1,
  "rand_reward": {
    "one_of": [
      {
        "xp": 600,
        "p": 38
      },
      {
        "xp": 1200,
        "p": 33
      },
      {
        "asset": "DomovoySpeedModifier_12h",
        "amount": 1,
        "p": 20
      },
      {
        "asset": "BuckwheatPot",
        "amount": 1,
        "p": 5
      },
      {
        "money": 1,
        "p": 4
      }
    ]
  },
  "id": 68372
}