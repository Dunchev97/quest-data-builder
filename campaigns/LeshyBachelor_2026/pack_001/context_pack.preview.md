# Context Pack Preview

Quests found: 12
Tasks found: 36
Candidate limit: 12
Candidates emitted: 276
Unique candidates emitted: 204
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## LeshyBachelor_2026_Story_1 — Камеры на пнях

Character: Шапокляк

### Task 1: TT-007 HOG поиск истинного среди ложного

- Task type: `HOG clean_debris true_among_false`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 2: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:GarbageCupCoffeeCollection1:GarbageCupCoffee:home`: Набор сладкоежки
  - `collection_drop:GarbageCupCoffeeCollection2:GarbageCupCoffee:home`: Кофейное дерево
  - `collection_drop:GarbageCupCoffeeCollection3:GarbageCupCoffee:home`: Подставка под горячее
  - `collection_drop:GarbageCupCoffeeCollection4:GarbageCupCoffee:home`: Чизкейк
  - `collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home`: Турка

### Task 3: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения
  - `garbage:BeetlePaws`: Жучок кверху лапками

## LeshyBachelor_2026_Story_2 — Первое появление холостяка

Character: Леший

### Task 4: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:ArmorOfSnailCollection1:ArmorOfSnail:home`: Улитка-золотушка
  - `collection_drop:ArmorOfSnailCollection2:ArmorOfSnail:home`: Улитка-серебрянка
  - `collection_drop:ArmorOfSnailCollection3:ArmorOfSnail:home`: Улитка-пучеглазик
  - `collection_drop:ArmorOfSnailCollection4:ArmorOfSnail:home`: Улитка-поцелуйчик
  - `collection_drop:ArmorOfSnailCollection5:ArmorOfSnail:home`: Улитка-рулетка

### Task 5: TT-017 GR с цветов дома

- Task type: `get_asset GR flower`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 6: TT-018 Сбор цветов дома (зависит от времени роста)

- Task type: `action take_crop`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerLaysPotato`: Картошечка
  - `flower:FlowerMagazine4_Hippeastrum`: Гиппеаструм
  - `flower:FlowerMagazine5_RainbowCalla`: Радужная калла
  - `flower:FlowerMagazine6_TerryMallow`: Мальва махровая
  - `flower:FlowerMagazine7_Lupinus`: Люпин

## LeshyBachelor_2026_Story_3 — Зелье первого впечатления

Character: Баба Яга

### Task 7: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 9: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BagOfFertilizer:guest`: Мешок от удобрения
  - `gr_garbage:BigButton:guest`: Пуговица
  - `gr_garbage:BigHome_Garbage_Bar_BrokenCocktail:guest`: Разлитый коктейль
  - `gr_garbage:BigHome_Garbage_Bar_BrokenDiscoBall:guest`: Разбитый диско-шар

## LeshyBachelor_2026_Story_4 — Болотный образ для свидания

Character: Кикимора

### Task 10: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 11: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerPetunia`: Петунья
  - `flower:FlowerPinkRose`: Роза Нежная страсть
  - `flower:FlowerPrimula`: Примула
  - `flower:FlowerSeaBuckthorn`: Облепиха
  - `flower:FlowerSeven`: Мак

### Task 12: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## LeshyBachelor_2026_Story_5 — Песня у пруда

Character: Русалка

### Task 13: TT-005 HOG в локациях дома

- Task type: `HOG clean_debris home_locations`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 14: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BagOfFertilizerCollection3:BagOfFertilizer:home`: Зверобой
  - `collection_drop:BagOfFertilizerCollection4:BagOfFertilizer:home`: Мята
  - `collection_drop:BagOfFertilizerCollection5:BagOfFertilizer:home`: Чистотел
  - `collection_drop:BarometerCollection1:Barometer:home`: Гидрокостюм
  - `collection_drop:BarometerCollection2:Barometer:home`: Баллон с газом

### Task 15: TT-030 Силуэт мусора дома

- Task type: `garbage classname is_silhouette`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:ArmorOfSnail`: Панцирь улитки
  - `garbage:Barometer`: Разбитый барометр
  - `garbage:BasketOfBerries`: Корзинка с ягодами
  - `garbage:BigHome_Garbage_Nursery_MugNotShedding`: Кружка-непроливашка

## LeshyBachelor_2026_Story_6 — Ручная работа

Character: Василиса

### Task 16: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:FloralWreathCollection1:FloralWreath:home`: Венок из одуванчиков
  - `collection_drop:FloralWreathCollection2:FloralWreath:home`: Венок из ромашек
  - `collection_drop:FloralWreathCollection3:FloralWreath:home`: Венок из колосков
  - `collection_drop:FloralWreathCollection4:FloralWreath:home`: Венок из роз
  - `collection_drop:FloralWreathCollection5:FloralWreath:home`: Венок с ягодками

### Task 17: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 18: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:BigHome_Garbage_Server_TornPunchCard`: Рваная перфокарта
  - `garbage:BittingPie`: Надкусанный пирожок
  - `garbage:BrokenBall`: Рваный мяч
  - `garbage:BrokenBank`: Разбитая банка
  - `garbage:BrokenBasketForNeedlework`: Сломанная корзиночка для рукоделия

## LeshyBachelor_2026_Story_7 — Романтический поход

Character: Марья Моревна

### Task 19: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 20: TT-009 Получить PER

- Task type: `get_asset PER`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 21: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:BigHome_Garbage_Overview_Ammonit:guest`: Аммонит
  - `gr_garbage:BigHome_Garbage_Overview_LizardTooth:guest`: Зуб ящера
  - `gr_garbage:BigHome_Garbage_Overview_Silver:guest`: Родированное серебро
  - `gr_garbage:BigHome_Garbage_Server_BrokenBobine:guest`: Сломаная бобина
  - `gr_garbage:BigHome_Garbage_Server_BrokenCable:guest`: Обрывок кабеля

## LeshyBachelor_2026_Story_8 — Пирожки для каждого сердечка

Character: Алёнушка

### Task 22: TT-022 Загадка на цветок в гостях

- Task type: `action take_crop_in_guest mystery`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 23: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:Garbage_PinkPetalsCollection3:Garbage_PinkPetals:home`: Крем с шиповником
  - `collection_drop:Garbage_PinkPetalsCollection3:Garbage_PinkPetals:guest`: Крем с шиповником
  - `collection_drop:BasketOfBerriesCollection5:BasketOfBerries:home`: Клюковка
  - `collection_drop:BigButtonCollection1:BigButton:home`: Хрюшкин пятачок
  - `collection_drop:BigButtonCollection2:BigButton:home`: Обычная пуговица

### Task 24: TT-024 Загадка на мусор в гостях

- Task type: `garbage classname in_guest mystery`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:Chips`: Стружка
  - `garbage:CircassianWalnutShell`: Скорлупки грецкого ореха
  - `garbage:ClayLump`: Комок глины
  - `garbage:Cucumber`: Надкусанный огурец
  - `garbage:DirtyPan`: Грязная сковорода

## LeshyBachelor_2026_Story_9 — Слишком драматичная пауза

Character: Шапокляк

### Task 25: TT-003 HOG в мире

- Task type: `HOG clean_debris world`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 26: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BigHome_Garbage_Bar_BrokenCocktail_Collection5:BigHome_Garbage_Bar_BrokenCocktail:home`: Рокс
  - `collection_drop:BigHome_Garbage_Bar_BrokenDiscoBall_Collection1:BigHome_Garbage_Bar_BrokenDiscoBall:home`: Диско очки
  - `collection_drop:BigHome_Garbage_Bar_BrokenDiscoBall_Collection2:BigHome_Garbage_Bar_BrokenDiscoBall:home`: Диско куртка
  - `collection_drop:BigHome_Garbage_Bar_BrokenDiscoBall_Collection3:BigHome_Garbage_Bar_BrokenDiscoBall:home`: Брюки клёш
  - `collection_drop:BigHome_Garbage_Bar_BrokenDiscoBall_Collection4:BigHome_Garbage_Bar_BrokenDiscoBall:home`: Парик

### Task 27: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:FeatherRaffles`: Гусиное перо
  - `garbage:FlapOfTissue`: Лоскут ткани
  - `garbage:FrameBroken`: Фоторамка разбитая
  - `garbage:Frog`: Лягушка
  - `garbage:GarbageCrumbs`: Крошки

## LeshyBachelor_2026_Story_10 — Букет от Лешего

Character: Леший

### Task 28: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 29: TT-018 Сбор цветов дома (зависит от времени роста)

- Task type: `action take_crop`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerFive`: Роза
  - `flower:FlowerPinkRose`: Роза Нежная страсть
  - `flower:MagicFlowerHome`: Цветок очага
  - `flower:MagicFlowerMiracle`: Цветок магии

### Task 30: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerFive`: Роза
  - `flower:FlowerPinkRose`: Роза Нежная страсть
  - `flower:MagicFlowerHome`: Цветок очага
  - `flower:MagicFlowerMiracle`: Цветок магии

## LeshyBachelor_2026_Story_11 — Разговор без камер

Character: Василиса

### Task 31: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 32: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 33: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## LeshyBachelor_2026_Story_12 — Первая церемония роз

Character: Леший

### Task 34: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 35: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:IcyHeartCollection4:IcyHeart:home`: Сухой лед
  - `collection_drop:IcyHeartCollection1:IcyHeart:home`: Ведерко со льдом
  - `collection_drop:IcyHeartCollection2:IcyHeart:home`: Щипчики для льда
  - `collection_drop:IcyHeartCollection3:IcyHeart:home`: Формочки для льда
  - `collection_drop:IcyHeartCollection5:IcyHeart:home`: Замороженный сок

### Task 36: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
