# Context Pack Preview

Quests found: 12
Tasks found: 36
Candidate limit: 6
Candidates emitted: 126
Unique candidates emitted: 126
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## VelesNight_2026_Story_1 — Снова Велесова ночь

Character: Ведятя

### Task 1: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 2: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:RustyNail:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:RustyNail:home`: Ржавый гвоздь
  - `gr_garbage:LukomorieSole:home`: Подметка сапога
  - `gr_garbage:Megaphone:home`: Рупор граммофона
  - `gr_garbage:MirrorFragment:home`: Осколки зеркала
  - `gr_garbage:MoneyRaffles:home`: Рваная купюра

### Task 3: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 6
- Note: Manual override prefers candidates: garbage:DeadLeaf.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:DeadLeaf`: Засохший листочек
  - `garbage:FragmentaryCard`: Фрагмент карты
  - `garbage:FrameBroken`: Фоторамка разбитая
  - `garbage:Frog`: Лягушка
  - `garbage:FrozenFlower`: Ледяной цветок

## VelesNight_2026_Story_2 — Нарядный хозяин

Character: Баба Зина

### Task 4: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:BrokenPlowCollection2:BrokenPlow:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:BrokenPlowCollection2:BrokenPlow:home`: Лопата
  - `collection_drop:BirchLeafCollection4:BirchLeaf:home`: Кувшинчик
  - `collection_drop:BirchLeafCollection5:BirchLeaf:home`: Кадушка
  - `collection_drop:BitternCollection1:Bittern:home`: Лунь
  - `collection_drop:BitternCollection2:Bittern:home`: Подорлик

### Task 5: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:BrokenPlowCollection4:BrokenPlow:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:BrokenPlowCollection4:BrokenPlow:home`: Грабли
  - `collection_drop:BitternCollection4:Bittern:home`: Пастушок
  - `collection_drop:BitternCollection5:Bittern:home`: Лысуха
  - `collection_drop:BoarsTuskCollection1:BoarsTusk:home`: Корешок
  - `collection_drop:BoarsTuskCollection2:BoarsTusk:home`: Символ мужества

### Task 6: TT-033 Передача предмета

- Task type: `action give`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_3 — Телега без возницы

Character: Дед Домовед

### Task 7: TT-006 HOG в виде скрытого предмета

- Task type: `HOG clean_debris hidden_object`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:Chips:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:Chips:home`: Стружка
  - `gr_garbage:NibbledCutlet:home`: Надкусанная котлета
  - `gr_garbage:NibbledDoughnut:home`: Надкусанный пончик
  - `gr_garbage:Nightie:home`: Сорочка
  - `gr_garbage:OracleBook:home`: Книга с гаданиями

### Task 9: TT-030 Силуэт мусора дома

- Task type: `garbage classname is_silhouette`
- Candidate domain: `garbage`
- Candidates: 6
- Note: Manual override prefers candidates: garbage:Anvil.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:Anvil`: Наковаленка
  - `garbage:FurHat`: Меховая шапка
  - `garbage:GarbageCrumbs`: Крошки
  - `garbage:GarbageFirefly`: Светлячок
  - `garbage:GarbageJuicer`: Соковыжималка

## VelesNight_2026_Story_4 — Гости ходят кругами

Character: Куйгорож

### Task 10: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:WagonWheel:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:WagonWheel:home`: Колесо от телеги
  - `gr_garbage:PaintJar:home`: Баночка с рассыпавшейся краской
  - `gr_garbage:PalmBranch:home`: Пальмовая ветка
  - `gr_garbage:Pawn:home`: Пешка
  - `gr_garbage:Pick:home`: Кирка

### Task 11: TT-025 Загадка на мусор дома

- Task type: `garbage classname mystery`
- Candidate domain: `garbage`
- Candidates: 6
- Note: Manual override prefers candidates: garbage:Snag.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:Snag`: Коряга
  - `garbage:GarbageSphere`: Сфера
  - `garbage:GarbageSpoon`: Половник
  - `garbage:Garbage_Armor`: Доспех с гербом
  - `garbage:Garbage_ArrowClockTower`: Стрелка от башенных часов

### Task 12: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:YarnLump:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:YarnLump:home`: Комок спутавшейся пряжи
  - `gr_garbage:Pill:home`: Пилюля
  - `gr_garbage:Pinions:home`: Горстка перьев
  - `gr_garbage:Pounder:home`: Ступка
  - `gr_garbage:PreciousStone:home`: Минерал

## VelesNight_2026_Story_5 — Беглец из Нави

Character: Королева Подземного Царства

### Task 13: TT-005 HOG в локациях дома

- Task type: `HOG clean_debris home_locations`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 14: TT-006 HOG в виде скрытого предмета

- Task type: `HOG clean_debris hidden_object`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 15: TT-007 HOG поиск истинного среди ложного

- Task type: `HOG clean_debris true_among_false`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_6 — Верная дорога

Character: Ведятя

### Task 16: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 17: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:MasterSet:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:MasterSet:home`: Разбитый набор мастера
  - `gr_garbage:RodentStone:home`: Косточка грызуна
  - `gr_garbage:RustyLock:home`: Ржавый замок
  - `gr_garbage:SamovarBoot:home`: Сапог от самовара 
  - `gr_garbage:Shards:home`: Черепки

### Task 18: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_7 — Королева взаперти

Character: Баба Зина

### Task 19: TT-006 HOG в виде скрытого предмета

- Task type: `HOG clean_debris hidden_object`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 20: TT-007 HOG поиск истинного среди ложного

- Task type: `HOG clean_debris true_among_false`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 21: TT-006 HOG в виде скрытого предмета

- Task type: `HOG clean_debris hidden_object`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_8 — Бунт инструментов

Character: Куйгорож

### Task 22: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:WashboardCollection4:Washboard:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:WashboardCollection4:Washboard:home`: Бельевая веревка
  - `collection_drop:BoarsTuskCollection4:BoarsTusk:home`: Золотой желудь
  - `collection_drop:BoarsTuskCollection5:BoarsTusk:home`: Щетка для одежды
  - `collection_drop:BoneCollection1:Bone:home`: Череп гепарда
  - `collection_drop:BoneCollection2:Bone:home`: Коготь тигра

### Task 23: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:BrokenOarCollection1:BrokenOar:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:BrokenOarCollection1:BrokenOar:home`: Канат
  - `collection_drop:BoneCollection4:Bone:home`: Ребро льва
  - `collection_drop:BoneCollection5:Bone:home`: Череп зубра
  - `collection_drop:BottleWithNoteCollection1:BottleWithNote:home`: Морской узел
  - `collection_drop:BottleWithNoteCollection2:BottleWithNote:home`: Бескозырка

### Task 24: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:WickerBasket:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:WickerBasket:home`: Дно корзинки
  - `gr_garbage:SilverClutch:home`: Серебристый клатч
  - `gr_garbage:Skalka:home`: Скалка
  - `gr_garbage:SkinBanana:home`: Кожура банана
  - `gr_garbage:SmashedEarthenwareTeaPot:home`: Разбитая чашка

## VelesNight_2026_Story_9 — Лестница для Домоведа

Character: Дед Домовед

### Task 25: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 26: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:TrowelCollection2:Trowel:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:TrowelCollection2:Trowel:home`: Брус
  - `collection_drop:BottleWithNoteCollection5:BottleWithNote:home`: Корабельный колокол
  - `collection_drop:BoxOfBiscuitsCollection1:BoxOfBiscuits:home`: Безе
  - `collection_drop:BoxOfBiscuitsCollection2:BoxOfBiscuits:home`: Крем с торта
  - `collection_drop:BoxOfBiscuitsCollection3:BoxOfBiscuits:home`: Сладкая вата

### Task 27: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:ChipsCollection3:Chips:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:ChipsCollection3:Chips:home`: Струбцина
  - `collection_drop:BoxOfBiscuitsCollection5:BoxOfBiscuits:home`: Коробка конфет
  - `collection_drop:BrokenBarrelCollection1:BrokenBarrel:home`: Чарка
  - `collection_drop:BrokenBarrelCollection2:BrokenBarrel:home`: Лайм
  - `collection_drop:BrokenBarrelCollection3:BrokenBarrel:home`: Трубка

## VelesNight_2026_Story_10 — Зина, отойди от окна!

Character: Баба Зина

### Task 28: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:BrokenPlow:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:BrokenPlow:home`: Сломанный плуг
  - `gr_garbage:SnailReel:home`: Улитка-катушка
  - `gr_garbage:SnowPattern:home`: Снежный узор
  - `gr_garbage:SoapBubble:home`: Мыльный пузырь
  - `gr_garbage:SockWithHole:home`: Грязный носок

### Task 29: TT-028 Силуэт элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection is_silhouette`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:ChipsCollection4:Chips:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:ChipsCollection4:Chips:home`: Киянка
  - `collection_drop:BrokenBarrelCollection5:BrokenBarrel:home`: Черная метка
  - `collection_drop:BrokenJugCollection1:BrokenJug:home`: Амфора
  - `collection_drop:BrokenJugCollection2:BrokenJug:home`: Кувшин с росписью
  - `collection_drop:BrokenJugCollection3:BrokenJug:home`: Фляга

### Task 30: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 6
- Note: Manual override prefers candidates: garbage:StrawPinch.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:StrawPinch`: Щепотка соломы
  - `garbage:Garbage_Bread`: Кусочек хлеба
  - `garbage:Garbage_Bulb`: Опрокинутая колба
  - `garbage:Garbage_Candlestick`: Подсвечник
  - `garbage:Garbage_Chandelier`: Канделябр

## VelesNight_2026_Story_11 — Барину пора домой

Character: Королева Подземного Царства

### Task 31: TT-009 Получить PER

- Task type: `get_asset PER`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 32: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 6
- Note: Manual override prefers candidates: gr_garbage:HoleRiddenBag:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:HoleRiddenBag:home`: Дырявый мешок
  - `gr_garbage:Starfish:home`: Морская звезда
  - `gr_garbage:SwarovskiCrystals:home`: Кристаллы Сваровски
  - `gr_garbage:SwoonedCaterpillar:home`: Гусеница в обмороке
  - `gr_garbage:TassleYarmolke:home`: Кисточка от ермолки

### Task 33: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## VelesNight_2026_Story_12 — Один Дед — и хватит

Character: Дед Домовед

### Task 34: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 6
- Note: Manual override prefers candidates: garbage:YarnLump.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:YarnLump`: Комок спутавшейся пряжи
  - `garbage:Garbage_Collapsar`: Чёрная дыра
  - `garbage:Garbage_Crescent`: Полумесяц
  - `garbage:Garbage_DarkenedBust`: Потемневший бюст
  - `garbage:Garbage_FoldingChair`: Складной стул

### Task 35: TT-006 HOG в виде скрытого предмета

- Task type: `HOG clean_debris hidden_object`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 36: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 6
- Note: Manual override prefers candidates: collection_drop:BrokenPlowCollection1:BrokenPlow:home.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:BrokenPlowCollection1:BrokenPlow:home`: Мотыга
  - `collection_drop:BrokenJugCollection5:BrokenJug:home`: Кувшин с орнаментом
  - `collection_drop:BrokenMaskCollection1:BrokenMask:home`: Маска жирафа
  - `collection_drop:BrokenMaskCollection2:BrokenMask:home`: Маска льва
  - `collection_drop:BrokenMaskCollection3:BrokenMask:home`: Маска бегемота
