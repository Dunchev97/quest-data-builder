# Context Pack Preview

Quests found: 3
Tasks found: 9
Candidate limit: 12
Candidates emitted: 60
Unique candidates emitted: 60
Issues: 0
Campaign memory used: yes

## Candidate Pools

- garbage: 226
- flower: 36
- collection_drop: 2095
- gr_garbage: 357

## Next Generated Numbers

- `MeatballRain_2026`: ASK_2, GR_3, HOG_2, R_2

## MeatballRain_2026_Story_4 — Огуречный гром

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
- Candidates: 12
- Note: Campaign memory excluded 4 already used candidates.
  - `garbage:GarbageCupCoffee`: Смятый стаканчик из-под кофе
  - `garbage:Garbage_Zoo_1`: Следы птиц
  - `garbage:Garbage_Zoo_2`: Следы копыт
  - `garbage:Garbage_Zoo_3`: Следы лапок
  - `garbage:MushroomCommon`: Грибы

## MeatballRain_2026_Story_5 — Помидорная осада

Character: Кощей

### Task 13: TT-021 Уборка конкретного мусора дома

- Task type: `garbage classname`
- Candidate domain: `garbage`
- Candidates: 12
- Note: Campaign memory excluded 4 already used candidates.
  - `garbage:BottleWithNote`: Бутылка с запиской
  - `garbage:BoxOfBiscuits`: Коробка печенья
  - `garbage:BrokenBall`: Рваный мяч
  - `garbage:BrokenBank`: Разбитая банка
  - `garbage:BrokenBarrel`: Разбитая бочка

### Task 14: TT-011 Получить элемент коллекции (зависит от редкости)

- Task type: `get_asset Collection`
- Candidate domain: `collection_drop`
- Candidates: 12
- Note: Campaign memory excluded 20 already used candidates.
  - `collection_drop:BigHome_Garbage_Overview_Silver_Collection1:BigHome_Garbage_Overview_Silver:home`: Золото
  - `collection_drop:GarbageCupCoffeeCollection1:GarbageCupCoffee:home`: Набор сладкоежки
  - `collection_drop:GarbageCupCoffeeCollection2:GarbageCupCoffee:home`: Кофейное дерево
  - `collection_drop:GarbageCupCoffeeCollection3:GarbageCupCoffee:home`: Подставка под горячее
  - `collection_drop:GarbageCupCoffeeCollection4:GarbageCupCoffee:home`: Чизкейк

### Task 15: TT-014 GR с конкретного мусора в гостях

- Task type: `get_asset GR in_guest garbage classname`
- Candidate domain: `gr_garbage`
- Candidates: 12
- Note: Campaign memory excluded 3 already used candidates.
  - `gr_garbage:BigHome_Garbage_Overview_Silver:guest`: Родированное серебро
  - `gr_garbage:GarbageCupCoffee:guest`: Смятый стаканчик из-под кофе
  - `gr_garbage:BigHome_Garbage_Nursery_MugNotShedding:guest`: Кружка-непроливашка
  - `gr_garbage:BigHome_Garbage_Nursery_MummyShadow:guest`: Муми-тень
  - `gr_garbage:BigHome_Garbage_Nursery_Sleeping:guest`: Сплюша

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
- Candidates: 12
- Note: Campaign memory excluded 1 already used candidates.
  - `flower:FlowerLaysPotato`: Картошечка
  - `flower:FlowerMagazine4_Hippeastrum`: Гиппеаструм
  - `flower:FlowerMagazine5_RainbowCalla`: Радужная калла
  - `flower:FlowerMagazine6_TerryMallow`: Мальва махровая
  - `flower:FlowerMagazine7_Lupinus`: Люпин

### Task 18: TT-002 Крафт

- Task type: `get_and_decrease_asset craft`
- Candidate domain: `generated`
- Candidates: 0
- Note: No real quest-ready candidates are needed for this generated/story template.
