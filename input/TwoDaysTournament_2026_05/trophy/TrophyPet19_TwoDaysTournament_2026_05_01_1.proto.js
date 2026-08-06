{
    "class": "QuestPrototype",
    "disabled": 1,
    "disabled_ru": 0,
    "disabled_my_mail_test": 0,
    "disabled_my_mail_test_prod": 0,
    "identifier": "TrophyPet19_TwoDaysTournament_2026_05_01_1",
    "title": "Хомяк",
    "group_identifier": "Trophy",
    "is_hidden": 1,
    "pass_conditions": "asset=TrophyPet19_TwoDaysTournament_2026_05_01_1:1",
    "conditions": "asset_or_stuff=Pet19_TwoDaysTournament_2026_05_01_1:1",
    "on_accomplish": [
        {
            "do": "remove_asset",
            "classname": "TrophyPet19_TwoDaysTournament_2026_05_01_1"
        },
        {
            "do": "add_stuff",
            "classname": "TrophyPet19_TwoDaysTournament_2026_05_01_1",
            "location": 75,
            "x": 0,
            "y": 0
        },
        {
            "do": "show_trophy_wow_effect",
            "icon": "TrophyPet19_TwoDaysTournament_2026_05_01_1"
        }
    ],
    "tasks": [
        {
            "identifier": "e9803",
            "title": "Хомяк",
            "type": "action",
            "action": "feed_pet_happy",
            "param": "Pet19_TwoDaysTournament_2026_05_01_1",
            "amount": 20,
            "price": 30
        }
    ],
    "id": 83663
}