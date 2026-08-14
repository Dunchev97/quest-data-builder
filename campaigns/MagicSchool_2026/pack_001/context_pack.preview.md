# Context Pack Preview

Quests found: 12
Tasks found: 36
Candidate limit: 12
Candidates emitted: 264
Unique candidates emitted: 264
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## MagicSchool_2026_Story_1 — Прибытие в школу

Character: Кот Учёный

### Task 1: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:FrozenFlower`: Ледяной цветок
  - `garbage:FrozenTwig`: Замороженная веточка
  - `garbage:FurHat`: Меховая шапка
  - `garbage:Garbage_Collapsar`: Чёрная дыра
  - `garbage:Garbage_Crescent`: Полумесяц

### Task 2: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:Garbage_Makeup`: Косметика
  - `garbage:Garbage_MilkyWay`: Рисунок млечного пути
  - `garbage:Garbage_NailPolish`: Разлитый лак
  - `garbage:Garbage_PaintedTeapot`: Расписной чайник
  - `garbage:Garbage_Perch`: Насест

### Task 3: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:BigHome_Garbage_Nursery_MummyShadow:guest`: Муми-тень
  - `gr_garbage:BigHome_Garbage_Nursery_Sleeping:guest`: Сплюша
  - `gr_garbage:BigHome_Garbage_Overview_Ammonit:guest`: Аммонит
  - `gr_garbage:BigHome_Garbage_Overview_LizardTooth:guest`: Зуб ящера
  - `gr_garbage:BigHome_Garbage_Overview_Silver:guest`: Родированное серебро

## MagicSchool_2026_Story_2 — Волшебные улики

Character: Полицейский

### Task 4: TT-030 Силуэт мусора дома

- Task type: `garbage classname is_silhouette`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:Garbage_Spot`: Пятно
  - `garbage:Garbage_TornStrap`: Порванный ремешок часов
  - `garbage:Garbage_TurkishDelight`: Рахат-лукум
  - `garbage:Garbage_Ufo`: НЛО
  - `garbage:Garbage_WarmBlanket`: Тёплое покрывало

### Task 5: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 6: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `flower:FlowerLaysPotato`: Картошечка
  - `flower:FlowerMagazine4_Hippeastrum`: Гиппеаструм
  - `flower:FlowerMagazine5_RainbowCalla`: Радужная калла
  - `flower:FlowerMagazine6_TerryMallow`: Мальва махровая
  - `flower:FlowerMagazine7_Lupinus`: Люпин

## MagicSchool_2026_Story_3 — Допрос волшебных свидетелей

Character: Полицейский

### Task 7: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:Garbage_TornPictureCollection5:Garbage_TornPicture:home`: Кисти в пенале
  - `collection_drop:OracleBookCollection1:OracleBook:home`: Кофейная гуща
  - `collection_drop:OracleBookCollection2:OracleBook:home`: Ромашка
  - `collection_drop:OracleBookCollection3:OracleBook:home`: Хрустальный шар
  - `collection_drop:OracleBookCollection4:OracleBook:home`: Иголка с ниткой

### Task 8: TT-024 Загадка на мусор в гостях

- Task type: `garbage classname in_guest mystery`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:HoleRiddenBag`: Дырявый мешок
  - `garbage:LeakyBucket`: Дырявое ведро
  - `garbage:LeakyShoe`: Дырявая калоша
  - `garbage:Log`: Обгорелое бревно
  - `garbage:MasterSet`: Разбитый набор мастера

### Task 9: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BigHome_Garbage_Nursery_MomsPortrait_Collection4:BigHome_Garbage_Nursery_MomsPortrait:guest`: Поделка
  - `collection_drop:BigHome_Garbage_Nursery_MomsPortrait_Collection5:BigHome_Garbage_Nursery_MomsPortrait:guest`: Носовой платочек
  - `collection_drop:EmptyMoneyBagCollection3:EmptyMoneyBag:guest`: Амбарная книга
  - `collection_drop:Garbage_PictureBook_Collection3:Garbage_PictureBook:guest`: Панорамная книга
  - `collection_drop:Garbage_ShieldCollection2:Garbage_Shield:guest`: Полицейский щит

## MagicSchool_2026_Story_4 — Экзамен — Дело о пропавшем гримуаре

Character: Ректор

### Task 10: TT-003 HOG в мире

- Task type: `HOG clean_debris world`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 11: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 12: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## MagicSchool_2026_Story_5 — Знакомство с огоньками

Character: Игнис

### Task 13: TT-018 Сбор цветов дома (зависит от времени роста)

- Task type: `action take_crop`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `flower:FlowerPetunia`: Петунья
  - `flower:FlowerPinkRose`: Роза Нежная страсть
  - `flower:FlowerPrimula`: Примула
  - `flower:FlowerSeaBuckthorn`: Облепиха
  - `flower:FlowerSeven`: Мак

### Task 14: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:RustyNail`: Ржавый гвоздь
  - `garbage:SaltShakerWithSpilledSalt`: Солонка
  - `garbage:SamovarBoot`: Сапог от самовара 
  - `garbage:Shards`: Черепки
  - `garbage:SmashedEarthenwarePot`: Разбитая крынка

### Task 15: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:BirchLeaf:home`: Березовый лист
  - `gr_garbage:Bittern:home`: Выпь
  - `gr_garbage:BoarsTusk:home`: Кабаний клык
  - `gr_garbage:Bone:home`: Кость
  - `gr_garbage:BottleWithNote:home`: Бутылка с запиской

## MagicSchool_2026_Story_6 — Неукротимый дракончик

Character: Пожарный

### Task 16: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:AshesCollection2:Ashes:home`: Огонь
  - `collection_drop:ApricotStoneCollection1:ApricotStone:home`: Абрикосовый пирог
  - `collection_drop:ApricotStoneCollection2:ApricotStone:home`: Абрикосовое варенье
  - `collection_drop:ApricotStoneCollection3:ApricotStone:home`: Абрикосовый пудинг
  - `collection_drop:ApricotStoneCollection4:ApricotStone:home`: Абрикосовый сок

### Task 17: TT-031 Силуэт цветка в гостях

- Task type: `action take_crop_in_guest is_silhouette`
- Candidate domain: `flower`
- Candidates: 12
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 18: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
  - `gr_garbage:Bulletin:guest`: Бюллетень
  - `gr_garbage:CandyWrapper:guest`: Фантик
  - `gr_garbage:Chips:guest`: Стружка
  - `gr_garbage:CircassianWalnutShell:guest`: Скорлупки грецкого ореха
  - `gr_garbage:ClayLump:guest`: Комок глины

## MagicSchool_2026_Story_7 — Экзамен — Контроль пламени

Character: Ректор

### Task 19: TT-007 HOG поиск истинного среди ложного

- Task type: `HOG clean_debris true_among_false`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 20: TT-009 Получить PER

- Task type: `get_asset PER`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 21: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## MagicSchool_2026_Story_8 — Тайная тропа

Character: Засоня

### Task 22: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:FadedAlgaCollection2:FadedAlga:home`: Морской мох
  - `collection_drop:Garbage_PentagramCollection4:Garbage_Pentagram:home`: Руны
  - `collection_drop:Garbage_PentagramCollection5:Garbage_Pentagram:home`: Бедный Йорик
  - `collection_drop:FadedAlgaCollection2:FadedAlga:guest`: Морской мох
  - `collection_drop:Garbage_PentagramCollection1:Garbage_Pentagram:guest`: Сушеные пауки

### Task 23: TT-024 Загадка на мусор в гостях

- Task type: `garbage classname in_guest mystery`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:Valve`: Вентиль
  - `garbage:WebCommon`: Паутина
  - `garbage:WickerBasket`: Дно корзинки
  - `garbage:WornGloves`: Дырявые перчатки
  - `garbage:YarnLump`: Комок спутавшейся пряжи

### Task 24: TT-029 Силуэт мусора в гостях

- Task type: `garbage classname is_silhouette in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:BigButton`: Пуговица
  - `garbage:BigHome_Garbage_Bar_BrokenCocktail`: Разлитый коктейль
  - `garbage:BigHome_Garbage_Bar_BrokenDiscoBall`: Разбитый диско-шар
  - `garbage:BigHome_Garbage_Bar_NeonStick`: Неоновая палочка 
  - `garbage:BigHome_Garbage_Nursery_Flags`: Флажки

## MagicSchool_2026_Story_9 — Волшебная руда

Character: Шахтер

### Task 25: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:TricornCollection5:Tricorn:guest`: Повязка на глаз
  - `collection_drop:AshesCollection5:Ashes:home`: Тлеющие угольки
  - `collection_drop:BagOfFertilizerCollection1:BagOfFertilizer:home`: Мать-и-мачеха
  - `collection_drop:BagOfFertilizerCollection2:BagOfFertilizer:home`: Чабрец
  - `collection_drop:BagOfFertilizerCollection3:BagOfFertilizer:home`: Зверобой

### Task 26: TT-007 HOG поиск истинного среди ложного

- Task type: `HOG clean_debris true_among_false`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 27: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:BrokenOar:home`: Сломанное весло
  - `gr_garbage:BrokenPlow:home`: Сломанный плуг
  - `gr_garbage:BrokenStick:home`: Сломанный посох
  - `gr_garbage:BrokenSword:home`: Сломанная сабля
  - `gr_garbage:BrokenTyre:home`: Рваная шина

## MagicSchool_2026_Story_10 — Экзамен — Корни мандрагоры

Character: Ректор

### Task 28: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:ClockRaffles:home`: Сломанный будильник
  - `gr_garbage:Cockleshell:home`: Раковина
  - `gr_garbage:CocoShell:home`: Скорлупа кокоса
  - `gr_garbage:CrownSnowstorm:home`: Корона Метелицы
  - `gr_garbage:CrystalSnowflake:home`: Хрустальная снежинка

### Task 29: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 30: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## MagicSchool_2026_Story_11 — Подготовка к выпуску

Character: Кот Учёный

### Task 31: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:FishboneCollection2:Fishbone:home`: Колокольчик
  - `collection_drop:PawnCollection1:Pawn:home`: Конь
  - `collection_drop:PawnCollection2:Pawn:home`: Слон
  - `collection_drop:PawnCollection3:Pawn:home`: Ладья
  - `collection_drop:PawnCollection4:Pawn:home`: Ферзь

### Task 32: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 33: TT-033 Передача предмета

- Task type: `action give`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## MagicSchool_2026_Story_12 — Торжественный выпуск

Character: Ректор

### Task 34: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BasketOfBerriesCollection1:BasketOfBerries:home`: Кустик малины
  - `collection_drop:BasketOfBerriesCollection2:BasketOfBerries:home`: Костяника
  - `collection_drop:BasketOfBerriesCollection3:BasketOfBerries:home`: Кустик земляники
  - `collection_drop:BasketOfBerriesCollection4:BasketOfBerries:home`: Ежевичка
  - `collection_drop:BasketOfBerriesCollection5:BasketOfBerries:home`: Клюковка

### Task 35: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 36: TT-034 Фото предмета

- Task type: `action post_photo`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
