# Context Pack Preview

Quests found: 16
Tasks found: 48
Candidate limit: 12
Candidates emitted: 384
Unique candidates emitted: 288
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## AutumnEquinox_2026_Story_1 — Обещание на обороте

Character: Дед Домовед

### Task 1: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 2: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BrokenStickCollection3:BrokenStick:home`: Водяной посох
  - `collection_drop:DrumstickCollection4:Drumstick:home`: Там-там
  - `collection_drop:EmptyMoneyBagCollection3:EmptyMoneyBag:home`: Амбарная книга
  - `collection_drop:Garbage_PictureBook_Collection3:Garbage_PictureBook:home`: Панорамная книга
  - `collection_drop:OracleBookCollection1:OracleBook:home`: Кофейная гуща

### Task 3: TT-030 Силуэт мусора дома

- Task type: `garbage classname is_silhouette`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:OracleBook`: Книга с гаданиями
  - `garbage:Anvil`: Наковаленка
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:ArmorOfSnail`: Панцирь улитки
  - `garbage:Ashes`: Пепел

## AutumnEquinox_2026_Story_2 — Письмо без обращения

Character: Баба Зина

### Task 4: TT-025 Загадка на мусор дома

- Task type: `garbage classname mystery`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:SmashedEarthenwareTeaPot`: Разбитая чашка
  - `garbage:SnowPattern`: Снежный узор
  - `garbage:BigHome_Garbage_Bar_NeonStick`: Неоновая палочка 
  - `garbage:BigHome_Garbage_Nursery_Flags`: Флажки
  - `garbage:BigHome_Garbage_Nursery_MatildasCage`: Клетка Матильды

### Task 5: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:Garbage_MakeupCollection5:Garbage_Makeup:home`: Маска из меда
  - `collection_drop:ShardsCollection1:Shards:home`: Глиняная чашка
  - `collection_drop:SmashedEarthenwarePotCollection1:SmashedEarthenwareTeaPot:home`: Чашка
  - `collection_drop:SmashedEarthenwarePotCollection2:SmashedEarthenwareTeaPot:home`: Сахарница
  - `collection_drop:SmashedEarthenwarePotCollection3:SmashedEarthenwareTeaPot:home`: Супник

### Task 6: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:BigHome_Garbage_Server_BrokenBobine`: Сломаная бобина
  - `garbage:BigHome_Garbage_Server_BrokenCable`: Обрывок кабеля
  - `garbage:BigHome_Garbage_Server_TornPunchCard`: Рваная перфокарта
  - `garbage:BirchBark`: Береста
  - `garbage:BirchLeaf`: Березовый лист

## AutumnEquinox_2026_Story_3 — Карта старых друзей

Character: Дед Домовед

### Task 7: TT-003 HOG в мире

- Task type: `HOG clean_debris world`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BirchLeafCollection1:BirchLeaf:home`: Ушат
  - `collection_drop:BirchLeafCollection2:BirchLeaf:home`: Черпачок
  - `collection_drop:BirchLeafCollection3:BirchLeaf:home`: Полотенце
  - `collection_drop:BirchLeafCollection4:BirchLeaf:home`: Кувшинчик
  - `collection_drop:BirchLeafCollection5:BirchLeaf:home`: Кадушка

### Task 9: TT-017 GR с цветов дома

- Task type: `get_asset GR flower`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## AutumnEquinox_2026_Story_4 — Флаги над горизонтом

Character: Капитан

### Task 10: TT-012 Получить FA (экшен на площади у друга)

- Task type: `get_asset FA`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 11: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:BrokenBank`: Разбитая банка
  - `garbage:BrokenBasketForNeedlework`: Сломанная корзиночка для рукоделия
  - `garbage:BrokenBear`: Мишка с оторванной лапой
  - `garbage:BrokenGuitar`: Сломанная гитара
  - `garbage:BrokenPipe`: Сломанная дудка

### Task 12: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## AutumnEquinox_2026_Story_5 — Солнце в дорожном узле

Character: Чинг

### Task 13: TT-018 Сбор цветов дома (зависит от времени роста)

- Task type: `action take_crop`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerLaysPotato`: Картошечка
  - `flower:FlowerMagazine4_Hippeastrum`: Гиппеаструм
  - `flower:FlowerMagazine5_RainbowCalla`: Радужная калла
  - `flower:FlowerMagazine6_TerryMallow`: Мальва махровая
  - `flower:FlowerMagazine7_Lupinus`: Люпин

### Task 14: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BigHome_Garbage_Nursery_MomsPortrait_Collection1:BigHome_Garbage_Nursery_MomsPortrait:home`: Пальчиковые краски
  - `collection_drop:BottleWithNoteCollection1:BottleWithNote:home`: Морской узел
  - `collection_drop:GarbageCupCoffeeCollection1:GarbageCupCoffee:home`: Набор сладкоежки
  - `collection_drop:GarbageCupCoffeeCollection2:GarbageCupCoffee:home`: Кофейное дерево
  - `collection_drop:GarbageCupCoffeeCollection3:GarbageCupCoffee:home`: Подставка под горячее

### Task 15: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerPetunia`: Петунья
  - `flower:FlowerPinkRose`: Роза Нежная страсть
  - `flower:FlowerPrimula`: Примула
  - `flower:FlowerSeaBuckthorn`: Облепиха
  - `flower:FlowerSeven`: Мак

## AutumnEquinox_2026_Story_6 — Бутылка против течения

Character: Водяной

### Task 16: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 17: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:SamovarBoot`: Сапог от самовара 
  - `garbage:TurbidWater`: Мутная вода
  - `garbage:Cucumber`: Надкусанный огурец
  - `garbage:DirtyPan`: Грязная сковорода
  - `garbage:DirtyTowel`: Грязное полотенце

### Task 18: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:Garbage_PinkPetals:guest`: Розовые лепестки
  - `gr_garbage:SamovarBoot:guest`: Сапог от самовара 
  - `gr_garbage:TurbidWater:guest`: Мутная вода
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BagOfFertilizer:guest`: Мешок от удобрения

## AutumnEquinox_2026_Story_7 — Стол из старого дуба

Character: Леший

### Task 19: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 20: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:GarbageCupCoffee:home`: Смятый стаканчик из-под кофе
  - `gr_garbage:LukomorieNugget:home`: Золотой самородок
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:ArmorOfSnail:home`: Панцирь улитки
  - `gr_garbage:Ashes:home`: Пепел

### Task 21: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## AutumnEquinox_2026_Story_8 — Первый иней

Character: Метелица

### Task 22: TT-023 Загадка на цветок дома (зависит от времени роста)

- Task type: `action take_crop mystery`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 23: TT-032 Силуэт цветка дома (зависит от времени роста)

- Task type: `action take_crop is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 24: TT-017 GR с цветов дома

- Task type: `get_asset GR flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## AutumnEquinox_2026_Story_9 — Голоса старого самовара

Character: Хозяйка Медной горы

### Task 25: TT-006 HOG в виде скрытого предмета

- Task type: `HOG clean_debris hidden_object`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 26: TT-030 Силуэт мусора дома

- Task type: `garbage classname is_silhouette`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:BrokenBarrel`: Разбитая бочка
  - `garbage:BrokenJug`: Разбитый кувшин
  - `garbage:BrokenMask`: Сломанная маска
  - `garbage:BrokenOar`: Сломанное весло

### Task 27: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:Garbage_Collapsar_Collection2:Garbage_Collapsar:home`: Потерянный носок
  - `collection_drop:RarityCollection2:BrokenBear:home`: Старая батарея
  - `collection_drop:SamovarBootCollection1:SamovarBoot:home`: Туфелька
  - `collection_drop:SamovarBootCollection2:SamovarBoot:home`: Сапожок
  - `collection_drop:SamovarBootCollection3:SamovarBoot:home`: Кхусса

## AutumnEquinox_2026_Story_10 — Запах того самого пирога

Character: Баба-яга

### Task 28: TT-018 Сбор цветов дома (зависит от времени роста)

- Task type: `action take_crop`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 29: TT-022 Загадка на цветок в гостях

- Task type: `action take_crop_in_guest mystery`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 30: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## AutumnEquinox_2026_Story_11 — Опись забытых сокровищ

Character: Кощей

### Task 31: TT-009 Получить PER

- Task type: `get_asset PER`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 32: TT-027 Загадка задом наперед на коллекцию (зависит от редкости)

- Task type: `get_asset Collection reverse_mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BrokenBarrelCollection3:BrokenBarrel:home`: Трубка
  - `collection_drop:Garbage_DarkenedBustCollection4:Garbage_DarkenedBust:home`: Деревянная такса
  - `collection_drop:GlassblowingTube1:GlassblowingTube:home`: Бур
  - `collection_drop:GlassblowingTube2:GlassblowingTube:home`: Стеклорез
  - `collection_drop:GlassblowingTube3:GlassblowingTube:home`: Ножницы для резки стекла

### Task 33: TT-033 Передача предмета

- Task type: `action give`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## AutumnEquinox_2026_Story_12 — Скатерть всей Домовятии

Character: Алёнушка

### Task 34: TT-005 HOG в локациях дома

- Task type: `HOG clean_debris home_locations`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 35: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:FlapOfTissue`: Лоскут ткани
  - `garbage:Garbage_MilkyWay`: Рисунок млечного пути
  - `garbage:ThickFeltRag`: Лоскут войлока
  - `garbage:FrameBroken`: Фоторамка разбитая
  - `garbage:Frog`: Лягушка

### Task 36: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:SnowPatternCollection1:SnowPattern:guest`: Елка в шаре
  - `collection_drop:SnowPatternCollection2:SnowPattern:guest`: Звезда в шаре
  - `collection_drop:SnowPatternCollection3:SnowPattern:guest`: Месяц в шаре
  - `collection_drop:SnowPatternCollection4:SnowPattern:guest`: Дельфин в шаре
  - `collection_drop:SnowPatternCollection5:SnowPattern:guest`: Башня в шаре

## AutumnEquinox_2026_Story_13 — Песня из разных голосов

Character: Несмеяна

### Task 37: TT-012 Получить FA (экшен на площади у друга)

- Task type: `get_asset FA`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 38: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BigHome_Garbage_Nursery_MugNotShedding_Collection2:BigHome_Garbage_Nursery_MugNotShedding:home`: Первый локон
  - `collection_drop:BigHome_Garbage_Nursery_MugNotShedding_Collection3:BigHome_Garbage_Nursery_MugNotShedding:home`: Первый башмачок
  - `collection_drop:BigHome_Garbage_Nursery_MugNotShedding_Collection4:BigHome_Garbage_Nursery_MugNotShedding:home`: Первый зубик
  - `collection_drop:TassleYarmolkeCollection3:TassleYarmolke:home`: Берет
  - `collection_drop:BigHome_Garbage_Nursery_MugNotShedding_Collection2:BigHome_Garbage_Nursery_MugNotShedding:guest`: Первый локон

### Task 39: TT-019 Сбор цветов в гостях

- Task type: `action take_crop_in_guest`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## AutumnEquinox_2026_Story_14 — Лавка с секретом

Character: Все вместе

### Task 40: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:CandyWrapper:home`: Фантик
  - `gr_garbage:ClockRaffles:home`: Сломанный будильник
  - `gr_garbage:DollRaffles:home`: Перчаточная кукла
  - `gr_garbage:EmptyMoneyBag:home`: Пустой мешочек для денег
  - `gr_garbage:FeatherRaffles:home`: Гусиное перо

### Task 41: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:EmptyMoneyBag`: Пустой мешочек для денег
  - `garbage:HandsetRaffles`: Телефонная трубка
  - `garbage:MoneyRaffles`: Рваная купюра
  - `garbage:RustyLock`: Ржавый замок
  - `garbage:CocoShell`: Скорлупа кокоса

### Task 42: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:CandyWrapperCollection1:CandyWrapper:home`: Дунькина радость
  - `collection_drop:CandyWrapperCollection2:CandyWrapper:home`: Алёнка
  - `collection_drop:CandyWrapperCollection3:CandyWrapper:home`: Золотая нива
  - `collection_drop:CandyWrapperCollection4:CandyWrapper:home`: Мишка на севере
  - `collection_drop:CandyWrapperCollection5:CandyWrapper:home`: Леденец петушок

## AutumnEquinox_2026_Story_15 — Двор в золотых огнях

Character: Все вместе

### Task 43: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 44: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:CocoShell:home`: Скорлупа кокоса
  - `gr_garbage:Garbage_ArrowClockTower:home`: Стрелка от башенных часов
  - `gr_garbage:LeafPineapple:home`: Черенок ананаса
  - `gr_garbage:MasterSet:home`: Разбитый набор мастера
  - `gr_garbage:OrangeSkin:home`: Апельсиновая корка

### Task 45: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## AutumnEquinox_2026_Story_16 — Новая фотография

Character: Все вместе

### Task 46: TT-019 Сбор цветов в гостях

- Task type: `action take_crop_in_guest`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 47: TT-012 Получить FA (экшен на площади у друга)

- Task type: `get_asset FA`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 48: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
