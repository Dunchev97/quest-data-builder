{
"class" : "AssetPrototype",
"classname" : "Pet19_TwoDaysTournament_2026_05_01_1",
"title" : "Хомяк",
"description" : "Этот малыш очень активный и весёлый питомец. Он неутомимо может играть или бегать в круге на марафонские дистанции!",
"group" : "pet",
"subgroup" : "pet22",
"price" : 100,
"currency" : "money_crown",
"lifespan" : 259200,
"as_stuff_in_inventory" : 1,
"can_extra_info_be_updated_by_client" : 1,

"extra" : {
    "check_spoil_in_inventory": 0,
    "pos_y": 435,
    "delta": 130,
    "speed": 5,
    "default_name": "Мяфлик",
    "event_frame": "BD19",
    "open_price": "money_alt=30000",
    "feed_price": "asset=BuckwheatPot:1",
    "spoil_price": "money=5",
    "hungry_booster_price": "money=5",
    "feed_time": 207360,
    
    "garbage_reward" : {"p":40, "one_of":[{"p":95, "money_alt":1, "xp":1}, {"p":5, "energy":1, "xp":4, "money_alt":4}]},
    "garbage_in_guest_reward" : {"p":40, "one_of":[{"p":97, "xp":1, "reputation_progress":1}, {"p":3, "energy":1, "xp":4, "reputation_progress":4}]},
    "take_crop_reward" : {"p":40, "one_of":[{"p":92, "pie":1, "xp":1}, {"p":8, "pie":4, "xp":4}]},
    "take_crop_reward_in_guest" : {"p":40, "one_of":[{"p":94, "reputation_progress":1, "xp":1}, {"p":6, "pie":4, "xp":4, "reputation_progress":4}]},
    
    "idle_animations" : {"angry":1, "happy":1, "normal":1},
    
    "wow_effects_by_state" : ["happy"],
    
    "love_by_hungry_percent" : [
        {"id": 1, "min" : 0, "max" : 15, "action":"remove", "amount":7},
        {"id": 2, "min" : 16, "max" : 30, "action":"remove", "amount":3},
        {"id": 3, "min" : 31, "max" : 80, "action":"add", "amount":7},
        {"id": 4, "min" : 81, "max" : 90, "action":"add", "amount":3},
        {"id": 5, "min" : 91, "max" : 100, "action":"remove", "amount":7}
    ],

    "start_love" : 30,
    "start_love_my_mail_test" : 10,

    "behaviour_by_love" : [
        {"min" : 0, "max" : 20, "animation":"angry"},
        {"min" : 21, "max" : 74, "animation":"normal"},
        {"min" : 75, "max" : 100, "animation":"happy"}
    ],

    "title_feed" : "От 100% до 0% Сытость падает за 3д. Одно кормление прибавляет 80% Сытости.",
    "title_attention" : "Можно получить в майском турнире 2026",
    "encyclopedia_conditions" : "time>2026-05-22 11:00",
    "encyclopedia_conditions_my_mail_test" : "time>2026-01-01 11:00",
    "encyclopedia_conditions_my_mail_test_prod" : "time>2026-01-01 11:00",
    "clothes" : []
},

"id" : 83661
}