{
  "class": "QuestPrototype",
  "identifier": "TwoDaysTournament_2026_05_01_Competition_1_Activate",
  "disabled": 1,
  "disabled_ru": 0,
  "is_hidden": 1,
  "hide_quest_accomplish": 1,
  "is_root": 1,
  "is_autostart": 1,

  "conditions": "time>2026-05-25 09:00+time<2026-05-26 22:00",
  
  "group_identifier": "TwoDaysTournament_2026_05_01_Competition_1",
  "title": "Квест-открыватель",
  "tasks": [
    {
      "identifier" : "e9804",
      "type": "have_location",
      "location_index": 1
    }
  ],
  "on_activate": [
    {
      "do": "reset_quest_group",
      "group": "TwoDaysTournament_2026_05_01_Competition_1_Task1_restarter"
    },
    {
      "do": "reset_quest_group",
      "group": "TwoDaysTournament_2026_05_01_Competition_1_Task2_restarter"
    },
    {
      "do": "reset_quest_group",
      "group": "TwoDaysTournament_2026_05_01_Competition_1_Task3_restarter"
    },
    {
      "do": "activate_quest",
      "quest": "TwoDaysTournament_2026_05_01_Competition_1_Task1",
      "conditions": "active_quest!=TwoDaysTournament_2026_05_01_Competition_1_Task1"
    },
    {
      "do": "activate_quest",
      "quest": "TwoDaysTournament_2026_05_01_Competition_1_Task2",
      "conditions": "active_quest!=TwoDaysTournament_2026_05_01_Competition_1_Task2"
    },
    {
      "do": "activate_quest",
      "quest": "TwoDaysTournament_2026_05_01_Competition_1_Task3",
      "conditions": "active_quest!=TwoDaysTournament_2026_05_01_Competition_1_Task3"
    },
    {
      "do": "force_send_commands"
    }
  ],
  "opens": [
    "TwoDaysTournament_2026_05_01_Competition_1_Counter"
  ],
  "id" : 83666
}