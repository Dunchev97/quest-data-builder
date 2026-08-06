{
  "class": "QuestPrototype",
  "identifier": "TwoDaysTournament_2026_05_01_Tech1",
  "disabled": 1,
  "disabled_ru": 0,
  "is_root": 1,
  "is_autostart": 1,

  "conditions": "time>2026-05-24 09:00+time<2026-05-31 23:59",

  "group_identifier": "TwoDaysTournament_2026_05_01_Tech",
  "on_activate": [],
  "on_accomplish": [],
  "tasks": [
    {
      "identifier" : "e9812",
      "type": "have_location",
      "location_index": 1
    }
  ],
  "is_hidden": 1,
  "opens": [
    "TwoDaysTournament_2026_05_01_Tech2",
    "TwoDaysTournament_2026_05_01_Tech_Magazine",
    "TwoDaysTournament_2026_05_01_Tech_MagazineShopAvailable"
  ],
  "id" : 83674
}