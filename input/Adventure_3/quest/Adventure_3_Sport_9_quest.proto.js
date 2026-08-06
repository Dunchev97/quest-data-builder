{
  "class": "QuestPrototype",
  "identifier": "Adventure_3_Sport_9_quest",
  "group_identifier": "Adventure_3_Sport_9",
  "disabled": 0,
  "disabled_ru": 0,
  "is_root": 1,
  "is_autostart": 0,
  "is_hidden": 0,
  "is_optional": 0,
  "title": "Q_Текст_1",
  "congratulation": "Q_Текст_2",
  "icon": "AdventureQuestIcon",
  "task_type": "Zodiac",
  "hide_quest_accomplish": 1,
  "tasks": [
    {
      "identifier": "e9786",
      "type": "action",
      "action": "no_such_action",
      "amount": 1,
      "hide_on_progress_arrow": 1,
      "reward": "asset=Adventure_GR_3:1"
    }
  ],
  "on_activate": [
    {
      "do": "reset_quest_group",
      "group": "Adventure_3_Sport_9_quest_task_1_restarter"
    },
    {
      "do": "reset_quest_group",
      "group": "Adventure_3_Sport_9_quest_task_2_restarter"
    },
    {
      "do": "reset_quest_group",
      "group": "Adventure_3_Sport_9_quest_task_3_restarter"
    },
    {
      "do": "reset_quest_group",
      "group": "Adventure_3_Sport_9_tech"
    },
    {
      "do": "remove_asset",
      "classname": "Adventure_GR_3"
    },
    {
      "do": "activate_quest",
      "quest": "Adventure_3_Sport_9_rewards",
      "conditions": "active_quest!=Adventure_3_Sport_9_rewards"
    },
    {
      "do": "activate_quest",
      "quest": "Adventure_3_Sport_9_quest_task_1",
      "conditions": "active_quest!=Adventure_3_Sport_9_quest_task_1"
    },
    {
      "do": "activate_quest",
      "quest": "Adventure_3_Sport_9_quest_task_2",
      "conditions": "active_quest!=Adventure_3_Sport_9_quest_task_2"
    },
    {
      "do": "activate_quest",
      "quest": "Adventure_3_Sport_9_quest_task_3",
      "conditions": "active_quest!=Adventure_3_Sport_9_quest_task_3"
    },
    {
      "do": "force_send_commands"
    }
  ],
  "on_accomplish": [
    {
      "do": "reset_quest",
      "quest": "Adventure_3_Sport_9_restarter"
    },
    {
      "do": "activate_quest",
      "quest": "Adventure_3_Sport_9_restarter"
    },
    {
      "do": "force_send_commands"
    }
  ],
  "disable_logs": [
    "activate",
    "accomplish",
    "spoil",
    "restart"
  ],
  "id": 68357
}