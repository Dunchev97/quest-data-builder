# Context Pack Preview

Quests found: 3
Tasks found: 9
Candidate limit: 12
Candidates emitted: 5
Unique candidates emitted: 5
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 226
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## Next Generated Numbers

- `MeatballRain_2026`: ASK_2, GR_3, HOG_2, R_2

## MeatballRain_2026_Story_4 — Огуречный раскат

Character: Леший

### Task 10: TT-001 Диалог

- Task type: `action dialog`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 11: TT-004 HOG на локации

- Task type: `HOG clean_debris location`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 12: TT-020 Уборка конкретного мусора в гостях

- Task type: `garbage classname in_guest`
- Candidate domain: `garbage`
- Candidates: 1
- Note: Manual override forced candidate: garbage:PieceOfChain.
- Note: Manual instruction: Выбрать физический след облачного замка: Кусочек цепи.
- Note: Only 1 candidates available for this task.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `garbage:PieceOfChain`: Кусочек цепи

## MeatballRain_2026_Story_5 — Помидорная осада

Character: Кощей

### Task 13: TT-026 Загадка на коллекцию (зависит от редкости)

- Task type: `get_asset Collection mystery`
- Candidate domain: `collection_drop`
- Candidates: 1
- Note: Manual override forced candidate: collection_drop:CucumberCollection1:Cucumber:home.
- Note: Manual instruction: Выбрать предмет с прямой связью с соленьями: Огуречный рассол из источника Надкусанный огурец.
- Note: Only 1 candidates available for this task.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:CucumberCollection1:Cucumber:home`: Огуречный рассол

### Task 14: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 1
- Note: Manual override forced candidate: collection_drop:BigHome_Garbage_Overview_Silver_Collection2:BigHome_Garbage_Overview_Silver:home.
- Note: Manual instruction: Выбрать предмет с прямой связью с соленьями: Поваренная соль.
- Note: Only 1 candidates available for this task.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `collection_drop:BigHome_Garbage_Overview_Silver_Collection2:BigHome_Garbage_Overview_Silver:home`: Поваренная соль

### Task 15: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 1
- Note: Manual override forced candidate: gr_garbage:BrokenBarrel:guest.
- Note: Manual instruction: Выбрать источник с прямой связью с бочками и заготовками: Разбитая бочка.
- Note: Only 1 candidates available for this task.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `gr_garbage:BrokenBarrel:guest`: Разбитая бочка

## MeatballRain_2026_Story_6 — Грибной рассольник

Character: Баба яга

### Task 16: TT-008 Получить ASK

- Task type: `get_asset ASK`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.

### Task 17: TT-016 GR с цветов в гостях

- Task type: `get_asset GR in_guest flower`
- Candidate domain: `flower`
- Candidates: 1
- Note: Manual override forced candidate: flower:FlowerSeaBuckthorn.
- Note: Manual instruction: Выбрать съедобно-растительный источник для подготовки бобового стебля: Облепиха.
- Note: Only 1 candidates available for this task.
- Note: Some candidates were used in previous context packs because fresh candidates were not enough.
  - `flower:FlowerSeaBuckthorn`: Облепиха

### Task 18: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
