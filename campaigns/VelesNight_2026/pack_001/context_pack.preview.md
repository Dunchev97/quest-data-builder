# Context Pack Preview

Quests found: 12
Tasks found: 36
Candidate limit: 300
Candidates emitted: 4761
Unique candidates emitted: 2644
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## VelesNight_2026_Story_1 — Снова Велесова ночь

Character: Ведятя

### Task 1: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 190
- Note: Only 190 candidates available for this task.
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:CocoShell:home`: Скорлупа кокоса
  - `gr_garbage:LeafPineapple:home`: Черенок ананаса
  - `gr_garbage:OrangeSkin:home`: Апельсиновая корка
  - `gr_garbage:Prickle:home`: Игла

### Task 2: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 190
- Note: Only 190 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:CocoShell:home`: Скорлупа кокоса
  - `gr_garbage:LeafPineapple:home`: Черенок ананаса
  - `gr_garbage:OrangeSkin:home`: Апельсиновая корка
  - `gr_garbage:Prickle:home`: Игла

### Task 3: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 220
- Note: Only 220 candidates available for this task.
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:CocoShell`: Скорлупа кокоса
  - `garbage:LeafPineapple`: Черенок ананаса
  - `garbage:OrangeSkin`: Апельсиновая корка
  - `garbage:Prickle`: Игла

## VelesNight_2026_Story_2 — Нарядный хозяин

Character: Баба Зина

### Task 4: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 190
- Note: Only 190 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:ArmorOfSnail:home`: Панцирь улитки
  - `gr_garbage:Ashes:home`: Пепел
  - `gr_garbage:BagOfFertilizer:home`: Мешок от удобрения
  - `gr_garbage:Barometer:home`: Разбитый барометр

### Task 5: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 6: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_3 — Телега без возницы

Character: Дед Домовед

### Task 7: TT-005 HOG в локациях дома

- Task type: `HOG clean_debris home_locations`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-019 Сбор цветов в гостях

- Task type: `action take_crop_in_guest`
- Candidate domain: `flower`
- Candidates: 36
- Note: Only 36 candidates available for this task.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 9: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:GarbageCupCoffeeCollection1:GarbageCupCoffee:home`: Набор сладкоежки
  - `collection_drop:GarbageCupCoffeeCollection2:GarbageCupCoffee:home`: Кофейное дерево
  - `collection_drop:GarbageCupCoffeeCollection3:GarbageCupCoffee:home`: Подставка под горячее
  - `collection_drop:GarbageCupCoffeeCollection4:GarbageCupCoffee:home`: Чизкейк
  - `collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home`: Турка

## VelesNight_2026_Story_4 — Гости ходят кругами

Character: Куйгорож

### Task 10: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:GarbageCupCoffeeCollection1:GarbageCupCoffee:guest`: Набор сладкоежки
  - `collection_drop:GarbageCupCoffeeCollection2:GarbageCupCoffee:guest`: Кофейное дерево
  - `collection_drop:GarbageCupCoffeeCollection3:GarbageCupCoffee:guest`: Подставка под горячее
  - `collection_drop:GarbageCupCoffeeCollection4:GarbageCupCoffee:guest`: Чизкейк
  - `collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:guest`: Турка

### Task 11: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 128
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Only 128 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками

### Task 12: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 128
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Only 128 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками

## VelesNight_2026_Story_5 — Беглец из Нави

Character: Королева Подземного Царства

### Task 13: TT-025 Загадка на мусор дома

- Task type: `garbage classname mystery`
- Candidate domain: `garbage`
- Candidates: 220
- Note: Only 220 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:CocoShell`: Скорлупа кокоса
  - `garbage:LeafPineapple`: Черенок ананаса
  - `garbage:OrangeSkin`: Апельсиновая корка
  - `garbage:Prickle`: Игла

### Task 14: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:LeafPineappleCollection1:LeafPineapple:home`: Ананасовый пудинг
  - `collection_drop:LeafPineappleCollection2:LeafPineapple:home`: Ананасовый пирог
  - `collection_drop:LeafPineappleCollection3:LeafPineapple:home`: Ананасовое пирожное
  - `collection_drop:LeafPineappleCollection4:LeafPineapple:home`: Ананасовое мороженое
  - `collection_drop:LeafPineappleCollection5:LeafPineapple:home`: Ананасовое варенье

### Task 15: TT-027 Загадка задом наперед на коллекцию (зависит от редкости)

- Task type: `get_asset Collection reverse_mystery`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:ThickFeltRagCollection5:ThickFeltRag:home`: Шапка викинга
  - `collection_drop:TireServiceCollection1:BrokenTyre:home`: Диск от колеса
  - `collection_drop:TireServiceCollection2:BrokenTyre:home`: Оторванный дворник
  - `collection_drop:TireServiceCollection3:BrokenTyre:home`: Трос
  - `collection_drop:TireServiceCollection4:BrokenTyre:home`: Руль

## VelesNight_2026_Story_6 — Верная дорога

Character: Ведятя

### Task 16: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 36
- Note: Only 36 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 17: TT-009 Получить PER

- Task type: `get_asset PER`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 18: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_7 — Королева взаперти

Character: Баба Зина

### Task 19: TT-005 HOG в локациях дома

- Task type: `HOG clean_debris home_locations`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 20: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:BigHome_Garbage_Overview_Silver_Collection5:BigHome_Garbage_Overview_Silver:guest`: Ванадий
  - `collection_drop:BigHome_Garbage_Server_BrokenBobine_Collection1:BigHome_Garbage_Server_BrokenBobine:guest`: Супермышь
  - `collection_drop:BigHome_Garbage_Server_BrokenBobine_Collection2:BigHome_Garbage_Server_BrokenBobine:guest`: Грушевый моноблок
  - `collection_drop:BigHome_Garbage_Server_BrokenBobine_Collection3:BigHome_Garbage_Server_BrokenBobine:guest`: USB-вентилятор
  - `collection_drop:BigHome_Garbage_Server_BrokenBobine_Collection4:BigHome_Garbage_Server_BrokenBobine:guest`: Умная вебкамера

### Task 21: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 36
- Note: Only 36 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## VelesNight_2026_Story_8 — Бунт инструментов

Character: Куйгорож

### Task 22: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:Garbage_FoldingChair_Collection5:Garbage_FoldingChair:guest`: Пуфик
  - `collection_drop:Garbage_HelmetCollection1:Garbage_Helmet:guest`: Шлем Древнего Востока
  - `collection_drop:Garbage_HelmetCollection2:Garbage_Helmet:guest`: Римский шлем
  - `collection_drop:Garbage_HelmetCollection3:Garbage_Helmet:guest`: Шлем кочевника
  - `collection_drop:Garbage_HelmetCollection4:Garbage_Helmet:guest`: Шлем викинга

### Task 23: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 36
- Note: Only 36 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 24: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 128
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Only 128 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками
  - `garbage:BigButton`: Пуговица

## VelesNight_2026_Story_9 — Лестница для Домоведа

Character: Дед Домовед

### Task 25: TT-003 HOG в мире

- Task type: `HOG clean_debris world`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 26: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 128
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Only 128 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками
  - `garbage:BigButton`: Пуговица

### Task 27: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 300
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `collection_drop:BottleWithNoteCollection3:BottleWithNote:home`: Веревочная лестница
  - `collection_drop:Garbage_PentagramCollection3:Garbage_Pentagram:home`: Лестница ведьмы
  - `collection_drop:ApricotStoneCollection1:ApricotStone:home`: Абрикосовый пирог
  - `collection_drop:ApricotStoneCollection2:ApricotStone:home`: Абрикосовое варенье
  - `collection_drop:ApricotStoneCollection3:ApricotStone:home`: Абрикосовый пудинг

## VelesNight_2026_Story_10 — Зина, отойди от окна!

Character: Баба Зина

### Task 28: TT-022 Загадка на цветок в гостях

- Task type: `action take_crop_in_guest mystery`
- Candidate domain: `flower`
- Candidates: 36
- Note: Only 36 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 29: TT-024 Загадка на мусор в гостях

- Task type: `garbage classname in_guest mystery`
- Candidate domain: `garbage`
- Candidates: 128
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Only 128 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками

### Task 30: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 300
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `collection_drop:SamovarBootCollection1:SamovarBoot:guest`: Туфелька
  - `collection_drop:SamovarBootCollection2:SamovarBoot:guest`: Сапожок
  - `collection_drop:SamovarBootCollection3:SamovarBoot:guest`: Кхусса
  - `collection_drop:SamovarBootCollection4:SamovarBoot:guest`: Сафьяновые черевички
  - `collection_drop:SamovarBootCollection5:SamovarBoot:guest`: Лапоть

## VelesNight_2026_Story_11 — Барину пора домой

Character: Королева Подземного Царства

### Task 31: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 103
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
- Note: Only 103 candidates available for this task.
  - `gr_garbage:GarbageCupCoffee:guest`: Смятый стаканчик из-под кофе
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BagOfFertilizer:guest`: Мешок от удобрения
  - `gr_garbage:BigButton:guest`: Пуговица
  - `gr_garbage:BigHome_Garbage_Bar_BrokenCocktail:guest`: Разлитый коктейль

### Task 32: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 33: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_12 — Один Дед — и хватит

Character: Дед Домовед

### Task 34: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 128
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Only 128 candidates available for this task.
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками
  - `garbage:BigButton`: Пуговица

### Task 35: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 300
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `collection_drop:ApricotStoneCollection1:ApricotStone:home`: Абрикосовый пирог
  - `collection_drop:ApricotStoneCollection2:ApricotStone:home`: Абрикосовое варенье
  - `collection_drop:ApricotStoneCollection3:ApricotStone:home`: Абрикосовый пудинг
  - `collection_drop:ApricotStoneCollection4:ApricotStone:home`: Абрикосовый сок
  - `collection_drop:ApricotStoneCollection5:ApricotStone:home`: Абрикосовое мороженое

### Task 36: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
