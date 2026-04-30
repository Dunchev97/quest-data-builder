# Context Pack Preview

Quests found: 3
Tasks found: 9
Candidate limit: 300
Candidates emitted: 813
Unique candidates emitted: 813
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 220
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## MusicBoxTown_2026_Story_1 — Порог размером с булавку

Character: Часовщик Тик-Так

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

### Task 3: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 220
- Note: Only 220 candidates available for this task.
  - `garbage:Anvil`: Наковаленка
  - `garbage:ApricotStone`: Абрикосовая косточка
  - `garbage:ArmorOfSnail`: Панцирь улитки
  - `garbage:Ashes`: Пепел
  - `garbage:BagOfFertilizer`: Мешок от удобрения

## MusicBoxTown_2026_Story_2 — Пружинный переполох

Character: Пружинка Фыр

### Task 4: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 5: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 6: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 103
- Note: Guest/world guardrail excluded 64 garbage or collection candidates tied to world locations.
- Note: Only 103 candidates available for this task.
  - `gr_garbage:Ashes:guest`: Пепел
  - `gr_garbage:BagOfFertilizer:guest`: Мешок от удобрения
  - `gr_garbage:BigButton:guest`: Пуговица
  - `gr_garbage:BigHome_Garbage_Bar_BrokenCocktail:guest`: Разлитый коктейль
  - `gr_garbage:BigHome_Garbage_Bar_BrokenDiscoBall:guest`: Разбитый диско-шар

## MusicBoxTown_2026_Story_3 — Большой перезвон

Character: Госпожа Молоточек

### Task 7: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 8: TT-013 GR с мусора в локации дома

- Task type: `get_asset GR garbage location_tags`
- Candidate domain: `gr_garbage`
- Candidates: 190
- Note: Only 190 candidates available for this task.
  - `gr_garbage:Garbage_MilkyWay:home`: Рисунок млечного пути
  - `gr_garbage:ApricotStone:home`: Абрикосовая косточка
  - `gr_garbage:ArmorOfSnail:home`: Панцирь улитки
  - `gr_garbage:Ashes:home`: Пепел
  - `gr_garbage:BagOfFertilizer:home`: Мешок от удобрения

### Task 9: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 300
  - `collection_drop:Garbage_MilkyWay_Collection1:Garbage_MilkyWay:home`: Макет Юпитера
  - `collection_drop:Garbage_MilkyWay_Collection2:Garbage_MilkyWay:home`: Макет Марса
  - `collection_drop:Garbage_MilkyWay_Collection3:Garbage_MilkyWay:home`: Макет Нептуна
  - `collection_drop:Garbage_MilkyWay_Collection4:Garbage_MilkyWay:home`: Макет Сатурна
  - `collection_drop:Garbage_MilkyWay_Collection5:Garbage_MilkyWay:home`: Макет Меркурия
