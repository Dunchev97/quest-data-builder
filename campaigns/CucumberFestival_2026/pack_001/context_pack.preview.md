# Context Pack Preview

Quests found: 3
Tasks found: 9
Candidate limit: 12
Candidates emitted: 60
Unique candidates emitted: 60
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## CucumberFestival_2026_Story_1 — Слёзы в рассоле

Character: Царевна Несмияна

### Task 1: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 2: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 3: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:Cucumber`: Надкусанный огурец
  - `garbage:Garbage_Zoo_1`: Следы птиц
  - `garbage:Garbage_Zoo_2`: Следы копыт
  - `garbage:Garbage_Zoo_3`: Следы лапок
  - `garbage:Anvil`: Наковаленка

## CucumberFestival_2026_Story_2 — Парад зелёного хруста

Character: Чинг

### Task 4: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 5: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 6: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

## CucumberFestival_2026_Story_3 — Дело о Главном Огурце

Character: Кот Детектив Котовски

### Task 7: TT-024 Загадка на мусор в гостях

- Task type: `garbage classname in_guest mystery`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Guest/world guardrail excluded 92 garbage or collection candidates tied to world locations.
  - `garbage:Garbage_WarmBlanket`: Тёплое покрывало
  - `garbage:BigHome_Garbage_Nursery_Flags`: Флажки
  - `garbage:BigHome_Garbage_Nursery_MatildasCage`: Клетка Матильды
  - `garbage:BigHome_Garbage_Nursery_MomsPortrait`: Мамочкин портрет
  - `garbage:BigHome_Garbage_Nursery_MugNotShedding`: Кружка-непроливашка

### Task 8: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:BrokenBarrelCollection1:BrokenBarrel:home`: Чарка
  - `collection_drop:BrokenBarrelCollection2:BrokenBarrel:home`: Лайм
  - `collection_drop:BrokenBarrelCollection3:BrokenBarrel:home`: Трубка
  - `collection_drop:BrokenBarrelCollection4:BrokenBarrel:home`: Пиратский флаг
  - `collection_drop:BrokenBarrelCollection5:BrokenBarrel:home`: Черная метка

### Task 9: TT-022 Загадка на цветок в гостях

- Task type: `action take_crop_in_guest mystery`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerLaysPotato`: Картошечка
  - `flower:FlowerMagazine4_Hippeastrum`: Гиппеаструм
  - `flower:FlowerMagazine5_RainbowCalla`: Радужная калла
  - `flower:FlowerMagazine6_TerryMallow`: Мальва махровая
  - `flower:FlowerMagazine7_Lupinus`: Люпин
