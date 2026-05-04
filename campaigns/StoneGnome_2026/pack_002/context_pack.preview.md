# Context Pack Preview

Quests found: 5
Tasks found: 15
Candidate limit: 12
Candidates emitted: 120
Unique candidates emitted: 120
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## Next Generated Numbers

- `StoneGnome_2026`: ASK_2, Character_6, FA_3, GR_9, HOG_4, PER_3, R_3

## StoneGnome_2026_Story_13 — Кто опрокинул суп?

Character: Шапокляк

### Task 37: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 38: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Campaign memory excluded 5 already used candidates.
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:Garbage_Zoo_1`: Следы птиц
  - `garbage:Garbage_Zoo_2`: Следы копыт
  - `garbage:Garbage_Zoo_3`: Следы лапок
  - `garbage:LeakyBucket`: Дырявое ведро

### Task 39: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
- Note: Campaign memory excluded 42 already used candidates.
  - `collection_drop:GarbageCupCoffeeCollection1:GarbageCupCoffee:home`: Набор сладкоежки
  - `collection_drop:GarbageCupCoffeeCollection2:GarbageCupCoffee:home`: Кофейное дерево
  - `collection_drop:GarbageCupCoffeeCollection3:GarbageCupCoffee:home`: Подставка под горячее
  - `collection_drop:GarbageCupCoffeeCollection4:GarbageCupCoffee:home`: Чизкейк
  - `collection_drop:GarbageCupCoffeeCollection5:GarbageCupCoffee:home`: Турка

## StoneGnome_2026_Story_14 — Куда делся молоток?

Character: Мирослав Щербатый

### Task 40: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 41: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Campaign memory excluded 9 already used candidates.
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:Barometer`: Разбитый барометр
  - `garbage:BasketOfBerries`: Корзинка с ягодами
  - `garbage:BigHome_Garbage_Nursery_MatildasCage`: Клетка Матильды
  - `garbage:BigHome_Garbage_Nursery_MomsPortrait`: Мамочкин портрет

### Task 42: TT-017 GR с цветов дома

- Task type: `get_asset GR flower`
- Candidate domain: `flower`
- Candidates: 12
- Note: Campaign memory excluded 6 already used candidates.
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик
  - `flower:FlowerElewen`: Ландыш
  - `flower:FlowerFive`: Роза
  - `flower:FlowerFour`: Лилия

## StoneGnome_2026_Story_15 — Почему гаснут фонари?

Character: Дед Домовед

### Task 43: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 44: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
- Note: Campaign memory excluded 5 already used candidates.
  - `garbage:BigHome_Garbage_Server_TornPunchCard`: Рваная перфокарта
  - `garbage:BrokenBall`: Рваный мяч
  - `garbage:BrokenBank`: Разбитая банка
  - `garbage:BrokenBasketForNeedlework`: Сломанная корзиночка для рукоделия
  - `garbage:BrokenBear`: Мишка с оторванной лапой

### Task 45: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Campaign memory excluded 8 already used candidates.
  - `gr_garbage:SwarovskiCrystals:home`: Кристаллы Сваровски
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:Ashes:home`: Пепел
  - `gr_garbage:Barometer:home`: Разбитый барометр
  - `gr_garbage:BasketOfBerries:home`: Корзинка с ягодами

## StoneGnome_2026_Story_16 — Перепутанные драгоценности

Character: Гордон Рубиновый

### Task 46: TT-018 Сбор цветов дома (зависит от времени роста)

- Task type: `action take_crop`
- Candidate domain: `flower`
- Candidates: 12
- Note: Campaign memory excluded 6 already used candidates.
  - `flower:FlowerMagazine8_Anthurium`: Антуриум
  - `flower:FlowerMagazine9_Plumeria`: Плюмерия
  - `flower:FlowerMatrix`: Матричка
  - `flower:FlowerNine`: Гербера
  - `flower:FlowerOne`: Нарцисс

### Task 47: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
- Note: Campaign memory excluded 42 already used candidates.
  - `collection_drop:PickCollection2:Pick:home`: Янтарь
  - `collection_drop:ApricotStoneCollection3:ApricotStone:home`: Абрикосовый пудинг
  - `collection_drop:ApricotStoneCollection4:ApricotStone:home`: Абрикосовый сок
  - `collection_drop:ApricotStoneCollection5:ApricotStone:home`: Абрикосовое мороженое
  - `collection_drop:AshesCollection1:Ashes:home`: Огненная саламандра

### Task 48: TT-015 GR с конкретного мусора дома

- Task type: `get_asset GR garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Campaign memory excluded 8 already used candidates.
  - `gr_garbage:Pick:home`: Кирка
  - `gr_garbage:BigHome_Garbage_Nursery_MummyShadow:home`: Муми-тень
  - `gr_garbage:BigHome_Garbage_Nursery_Sleeping:home`: Сплюша
  - `gr_garbage:BigHome_Garbage_Overview_LizardTooth:home`: Зуб ящера
  - `gr_garbage:BigHome_Garbage_Overview_Silver:home`: Родированное серебро

## StoneGnome_2026_Story_17 — Механизм встал — дело раскрыто

Character: Борька Тихий Ход

### Task 49: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 50: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 51: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
- Note: Campaign memory excluded 4 already used candidates.
  - `gr_garbage:GarbageSpoon:guest`: Половник
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BigButton:guest`: Пуговица
  - `gr_garbage:BigHome_Garbage_Bar_BrokenCocktail:guest`: Разлитый коктейль
  - `gr_garbage:BigHome_Garbage_Bar_BrokenDiscoBall:guest`: Разбитый диско-шар
