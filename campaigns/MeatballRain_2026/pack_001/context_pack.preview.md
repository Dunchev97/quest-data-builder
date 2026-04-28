# Context Pack Preview

Quests found: 3
Tasks found: 9
Candidate limit: 12
Candidates emitted: 60
Unique candidates emitted: 60
Issues: 0

## Candidate Pools

- garbage: 226
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## MeatballRain_2026_Story_1 — Первый мясной осадок

Character: Дедушка Домовед

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
  - `garbage:Anvil`: Наковаленка
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:ArmorOfSnail`: Панцирь улитки
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения

## MeatballRain_2026_Story_2 — Фрикадельковый фронт

Character: Царевна медной горы

### Task 4: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
  - `garbage:FoxTrail`: След от лисьей лапки
  - `garbage:BigHome_Garbage_Nursery_Flags`: Флажки
  - `garbage:BigHome_Garbage_Nursery_MatildasCage`: Клетка Матильды
  - `garbage:BigHome_Garbage_Nursery_MomsPortrait`: Мамочкин портрет
  - `garbage:BigHome_Garbage_Nursery_MugNotShedding`: Кружка-непроливашка

### Task 5: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
  - `collection_drop:EggShellCollection3:EggShell:home`: Долина зелени
  - `collection_drop:FoxTrailCollection1:FoxTrail:home`: Воротник лисий
  - `collection_drop:FoxTrailCollection2:FoxTrail:home`: Шапка егеря
  - `collection_drop:FoxTrailCollection3:FoxTrail:home`: Шуба
  - `collection_drop:FoxTrailCollection4:FoxTrail:home`: Маска лисы

### Task 6: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
  - `gr_garbage:EggShell:guest`: Яичная скорлупа
  - `gr_garbage:FoxTrail:guest`: След от лисьей лапки
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BagOfFertilizer:guest`: Мешок от удобрения
  - `gr_garbage:Barometer:guest`: Разбитый барометр

## MeatballRain_2026_Story_3 — Котёл с характером

Character: Баба яга

### Task 7: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 12
  - `flower:FlowerBlueRose`: Синяя роза
  - `flower:FlowerCvetikSemicvetik`: Цветик-семицветик
  - `flower:FlowerDahlia`: Георгин
  - `flower:FlowerEith`: Лютик
  - `flower:FlowerEith_ForTutorial`: Лютик

### Task 9: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
