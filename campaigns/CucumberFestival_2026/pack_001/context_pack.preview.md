# Context Pack Preview

Quests found: 12
Tasks found: 36
Candidate limit: 12
Candidates emitted: 264
Unique candidates emitted: 204
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## CucumberFestival_2026_Story_1 — Сенсация с первой полосы

Character: Журналистка Герда из журнала Домовита

### Task 1: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 2: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 3: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## CucumberFestival_2026_Story_2 — Дело о зеленом следе

Character: Кот детектив Котовски

### Task 4: TT-024 Загадка на мусор в гостях

- Task type: `garbage classname in_guest mystery`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:Garbage_Zoo_1`: Следы птиц
  - `garbage:Garbage_Zoo_2`: Следы копыт
  - `garbage:Garbage_Zoo_3`: Следы лапок
  - `garbage:Anvil`: Наковаленка
  - `garbage:Ashes`: Пепел

### Task 5: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:BigHome_Garbage_Overview_Silver:guest`: Родированное серебро
  - `gr_garbage:Cucumber:guest`: Надкусанный огурец
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BagOfFertilizer:guest`: Мешок от удобрения
  - `gr_garbage:BigButton:guest`: Пуговица

### Task 6: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BigHome_Garbage_Overview_Silver_Collection2:BigHome_Garbage_Overview_Silver:home`: Поваренная соль
  - `collection_drop:CucumberCollection1:Cucumber:home`: Огуречный рассол
  - `collection_drop:FoxTrailCollection1:FoxTrail:home`: Воротник лисий
  - `collection_drop:FoxTrailCollection2:FoxTrail:home`: Шапка егеря
  - `collection_drop:FoxTrailCollection3:FoxTrail:home`: Шуба

## CucumberFestival_2026_Story_3 — Рассол строгой выдержки

Character: Баба яга

### Task 7: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-017 GR с цветов дома

- Task type: `get_asset GR flower`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerLaysPotato`: Картошечка
  - `flower:FlowerMagazine4_Hippeastrum`: Гиппеаструм
  - `flower:FlowerMagazine5_RainbowCalla`: Радужная калла
  - `flower:FlowerMagazine6_TerryMallow`: Мальва махровая
  - `flower:FlowerMagazine7_Lupinus`: Люпин

### Task 9: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## CucumberFestival_2026_Story_4 — Золотая табличка мецената

Character: Кощей

### Task 10: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:Cucumber`: Надкусанный огурец
  - `garbage:BigHome_Garbage_Nursery_MatildasCage`: Клетка Матильды
  - `garbage:BigHome_Garbage_Nursery_MomsPortrait`: Мамочкин портрет
  - `garbage:BigHome_Garbage_Nursery_MugNotShedding`: Кружка-непроливашка
  - `garbage:BigHome_Garbage_Nursery_MummyShadow`: Муми-тень

### Task 11: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:CucumberCollection2:Cucumber:home`: Маска из огурца
  - `collection_drop:CucumberCollection4:Cucumber:home`: Салат из огурца
  - `collection_drop:CucumberCollection5:Cucumber:home`: Цветок огурца
  - `collection_drop:CucumberCollection2:Cucumber:guest`: Маска из огурца
  - `collection_drop:CucumberCollection4:Cucumber:guest`: Салат из огурца

### Task 12: TT-005 HOG в локациях дома

- Task type: `HOG clean_debris home_locations`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## CucumberFestival_2026_Story_5 — Интервью с бочкой

Character: Журналистка Герда из журнала Домовита

### Task 13: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:BittingPie`: Надкусанный пирожок
  - `garbage:BrokenBall`: Рваный мяч
  - `garbage:BrokenBank`: Разбитая банка
  - `garbage:BrokenBasketForNeedlework`: Сломанная корзиночка для рукоделия
  - `garbage:BrokenBear`: Мишка с оторванной лапой

### Task 14: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:BigHome_Garbage_Nursery_MummyShadow:guest`: Муми-тень
  - `gr_garbage:BigHome_Garbage_Nursery_Sleeping:guest`: Сплюша
  - `gr_garbage:BigHome_Garbage_Overview_Ammonit:guest`: Аммонит
  - `gr_garbage:BigHome_Garbage_Overview_LizardTooth:guest`: Зуб ящера
  - `gr_garbage:BigHome_Garbage_Server_BrokenBobine:guest`: Сломаная бобина

### Task 15: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerPetunia`: Петунья
  - `flower:FlowerPinkRose`: Роза Нежная страсть
  - `flower:FlowerPrimula`: Примула
  - `flower:FlowerSeaBuckthorn`: Облепиха
  - `flower:FlowerSeven`: Мак

## CucumberFestival_2026_Story_6 — Подозрительная хрусткость

Character: Кот детектив Котовски

### Task 16: TT-007 HOG поиск истинного среди ложного

- Task type: `HOG clean_debris true_among_false`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 17: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:GarbageNapkinsCollection1:GarbageNapkins:home`: Слюнявчик
  - `collection_drop:GarbageNapkinsCollection2:GarbageNapkins:home`: Циновка
  - `collection_drop:GarbageNapkinsCollection3:GarbageNapkins:home`: Салфетница
  - `collection_drop:GarbageNapkinsCollection4:GarbageNapkins:home`: Скатерка
  - `collection_drop:GarbageNapkinsCollection5:GarbageNapkins:home`: Поварской колпак

### Task 18: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## CucumberFestival_2026_Story_7 — Укропный переполох

Character: Баба яга

### Task 19: TT-009 Получить PER

- Task type: `get_asset PER`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 20: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:SnailReel:home`: Улитка-катушка
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:ArmorOfSnail:home`: Панцирь улитки
  - `gr_garbage:Ashes:home`: Пепел
  - `gr_garbage:BagOfFertilizer:home`: Мешок от удобрения

### Task 21: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## CucumberFestival_2026_Story_8 — Трон для Огуречного короля

Character: Кощей

### Task 22: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 23: TT-030 Силуэт мусора дома

- Task type: `garbage classname is_silhouette`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:ArmorOfSnail`: Панцирь улитки
  - `garbage:Barometer`: Разбитый барометр
  - `garbage:BasketOfBerries`: Корзинка с ягодами
  - `garbage:BirchBark`: Береста

### Task 24: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## CucumberFestival_2026_Story_9 — Фотография века

Character: Журналистка Герда из журнала Домовита

### Task 25: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 26: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 27: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BrokenBarrelCollection1:BrokenBarrel:home`: Чарка
  - `collection_drop:BrokenBarrelCollection2:BrokenBarrel:home`: Лайм
  - `collection_drop:BrokenBarrelCollection3:BrokenBarrel:home`: Трубка
  - `collection_drop:BrokenBarrelCollection4:BrokenBarrel:home`: Пиратский флаг
  - `collection_drop:BrokenBarrelCollection5:BrokenBarrel:home`: Черная метка

## CucumberFestival_2026_Story_10 — Парад ровного строя

Character: Кот детектив Котовски

### Task 28: TT-025 Загадка на мусор дома

- Task type: `garbage classname mystery`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:BrokenJug`: Разбитый кувшин
  - `garbage:BrokenMask`: Сломанная маска
  - `garbage:BrokenOar`: Сломанное весло
  - `garbage:BrokenPlow`: Сломанный плуг
  - `garbage:BrokenStick`: Сломанный посох

### Task 29: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:CocoShell`: Скорлупа кокоса
  - `garbage:CrownSnowstorm`: Корона Метелицы
  - `garbage:CrystalSnowflake`: Хрустальная снежинка
  - `garbage:CurveCammock`: Кривая клюка
  - `garbage:DeadFlower`: Засохший цветок

### Task 30: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

## CucumberFestival_2026_Story_11 — Огуречный оберег от скуки

Character: Баба яга

### Task 31: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 32: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were repeated inside this context pack because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 33: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## CucumberFestival_2026_Story_12 — Финальный хруст Домовятии

Character: Кощей

### Task 34: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 35: TT-003 HOG в мире

- Task type: `HOG clean_debris world`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 36: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:ApricotStoneCollection2:ApricotStone:home`: Абрикосовое варенье
  - `collection_drop:ApricotStoneCollection3:ApricotStone:home`: Абрикосовый пудинг
  - `collection_drop:ApricotStoneCollection4:ApricotStone:home`: Абрикосовый сок
  - `collection_drop:ApricotStoneCollection5:ApricotStone:home`: Абрикосовое мороженое
  - `collection_drop:ArmorOfSnailCollection1:ArmorOfSnail:home`: Улитка-золотушка
