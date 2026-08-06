{
  "class": "QuestPrototype",
  "identifier": "TwoDaysTournament_2026_05_01_Tech_Magazine",
  "disabled": 1,
  "disabled_ru": 0,
  "group_identifier": "TwoDaysTournament_2026_05_01_Tech",
  "title": "Майский турнир!",
  "show_quest_title_on_mouse_over": 1,
  "icon": "TwoDaysTournament_2026_05_01_MagazineQuestIcon",
  "conditions": "active_quest_group=TwoDaysTournament_2026_05_01_Tech",
  "task_type": "magazine",
  "hide_quest_accomplish": 1,
  "on_activate": [
    {
      "do": "display_magazine",
      "identifier": "TwoDaysTournament_2026_05_01_Magazine",
      "open_first_page": 0,
      "instructions": {
        "forcibly_first_page": 1
      }
    }
  ],
  "tasks": [
    {
      "identifier" : "e9814",
      "type": "action",
      "action": "no_such_action",
      "amount": 1
    }
  ],
  "id" : 83676
}