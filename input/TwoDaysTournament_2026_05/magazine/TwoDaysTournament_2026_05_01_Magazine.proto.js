{
  "class": "MagazinePrototype",
  "identifier": "TwoDaysTournament_2026_05_01_Magazine",
  "title": "Майский турнир",
  "view": "Magazine_TwoDaysTournament_2026_05_01_Window",
  "marks": [
    {
      "page_id": 1,
      "is_content": 1
    },
    {
      "page_id": 2,
      "mark_view": "MagazinePage_TwoDaysTournament_2026_05_01_Mark",
      "icon": "MagazinePage_Fun4_Mark_Icon_RewardTop"
    },
    {
      "page_id": 3,
      "mark_view": "MagazinePage_TwoDaysTournament_2026_05_01_Mark",
      "icon": "MagazinePage_Fun4_Mark_Icon_TaskDaily"
    },
    {
      "page_id": 4,
      "mark_view": "MagazinePage_TwoDaysTournament_2026_05_01_Mark",
      "icon": "MagazinePage_TwoDaysTournament_2026_05_01_Mark_Icon_Reward"
    }
  ],
  "pages": [
    {
      "page_number": 1,
      "template": "quest_content_simple",
      "label_title": "Турнир!",
      "page_content_view": "MagazinePage_TwoDaysTournament_2026_05_01_Content",
      "text_fields": [
        {
          "id": "title",
          "is_bold": 1,
          "text": "Турнир!"
        },
        {
          "id": "description",
          "is_bold": 1,
          "text": "Участвуй в турнире, и выигрывай уникального кроху!\nА также: кубок, подарки, щедрый ларчик, хрюшку, жаб и другие полезности!"
        }
      ],
      "icons": [
        {
          "id": "icon",
          "icon": "MagazinePage_Fun4_Content"
        }
      ]
    },
    {
      "page_number": 2,
      "template": "competition_rewards_info",
      "label_title": "Награды",
      "page_content_view": "MagazinePage_TwoDaysTournament_2026_05_01_CompetitionRewardsInfo",
      "icon_reward_asset_view": "MagazinePage_TwoDaysTournament_2026_05_01_CompetitionRewardsIconAsset",
      "icon_reward_resource_view": "MagazinePage_TwoDaysTournament_2026_05_01_CompetitionRewardsIconResource",
      "icon_reward_delta": 30,
      "competitions": [
        "TwoDaysTournament_2026_05_01_Competition_1"
      ],
      "additional_reward": {
        "text_fields": {
          "tf_title": "-",
          "tf_reward_weekly": "-",
          "tf_reward_total": "-",
          "tf_description_1": "-",
          "tf_description_2": "-",
          "tf_footnotes": "-"
        }
      },
      "text_fields": [
        {
          "id": "title",
          "text": "Награды",
          "is_bold": 1
        },
        {
          "id": "field1",
          "is_bold": 1,
          "text": "Участвуй турнире и получай достойные призы! Больше конфет — выше\nтвое место в топе, а значит и больше наград! Ты можешь получить кубки, кроху,\nхрюшки с червончиками и подарочные коробки!\n\nТурнир начнётся 25.05.2026 в 09:00 и завершится 26.05.2026 22:00"
        }
      ]
    },
    {
      "page_number": 3,
      "label_title": "Турнир",
      "template": "competition_endless_tasks",
      "page_content_view": "MagazinePage_TwoDaysTournament_2026_05_01_CompetitionEndlessTasks",
      "competition_group_identifiers": [
        "TwoDaysTournament_2026_05_01_Competition_1"
      ],
      "text_fields": [
        {
          "id": "title_tf",
          "text": "Турнир"
        },
        {
          "id": "field1_tf",
          "text": "Выполняй задания и получай за них конфеты. После выполнения задания у тебя будет время до получения нового, чтобы сократить это время, выполни все три задания или можешь ускорить за 2 червончика. Чем больше у тебя конфет, тем выше твоё место в топе."
        },
        {
          "id": "field2_tf",
          "text": "Твоё место"
        },
        {
          "id": "field3_tf",
          "text": "Набранных конфет"
        }
      ]
    },
    {
      "page_number": 4,
      "template": "recipes",
      "label_title": "Конфетный магазин",
      "available_conditions": "level>0",
      "lock_shield": "MagazinePage_TwoDaysTournament_2026_05_01_LockShield",
      "page_content_view": "MagazinePage_TwoDaysTournament_2026_05_01_Recipes",
      "text_fields": [
        {"id": "title","is_bold": 1, "text": "Конфетный магазин"},
        {"id": "field1","is_bold": 1,"text": "Обменивай полученные конфеты на декор с этой страницы! Обменивай в любое время - место в топе при этом не теряется."}
      ],
      "delta_x": 150,
      "delta_y": 220,
      "scrollbar_view_port": 430,
      "row_amount": 3,
      "recipe_view": "MagazinePage_TwoDaysTournament_2026_05_01_Recipes_Icon",
      "main_resource": "TwoDaysTournament_2026_05_01_Resource_Competition",
      "recipes": [
        "TwoDaysTournament_2026_05_01_Magazine_01_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_02_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_03_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_04_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_05_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_06_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_07_Recipe",
        "TwoDaysTournament_2026_05_01_Magazine_08_Recipe"
      ]
    }
  ],
  "id": 83660
}