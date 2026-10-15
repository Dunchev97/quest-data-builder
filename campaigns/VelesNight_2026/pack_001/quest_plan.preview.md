# Quest Plan Preview

Quests found: 12
Tasks found: 36
Issues: 0

## Quest 1 — Снова Велесова ночь

- classname_quests: `VelesNight_2026_Story_1`
- character: Ведятя
- task_numbers: 1, 2, 3

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 1 | `TT-001` | Диалог | `action dialog` |
| 2 | `TT-013` | GR с мусора в локации дома | `get_asset GR garbage location_tags` |
| 3 | `TT-021` | Уборка конкретного мусора дома | `garbage classname` |

Description: Помоги собрать завязки и крепления оберегов. Заодно уберём мусор, чтобы к приходу гостей двор был чистым.

Congratulation: Всё собрали, спасибо. Крепления отложим — пригодятся, когда будем проверять ограду.

## Quest 2 — Нарядный хозяин

- classname_quests: `VelesNight_2026_Story_2`
- character: Баба Зина
- task_numbers: 4, 5, 6

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 4 | `TT-015` | GR с конкретного мусора дома | `get_asset GR garbage classname` |
| 5 | `TT-008` | Получить ASK | `get_asset ASK` |
| 6 | `TT-033` | Передача предмета | `action give` |

Description: Подбери выброшенные инструменты и принеси мне. На земле оставлять нельзя — растеряем.

Congratulation: Всё на месте. Уберу инструменты в дом, там целее будут.

## Quest 3 — Телега без возницы

- classname_quests: `VelesNight_2026_Story_3`
- character: Дед Домовед
- task_numbers: 7, 8, 9

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 7 | `TT-005` | HOG в локациях дома | `HOG clean_debris home_locations` |
| 8 | `TT-015` | GR с конкретного мусора дома | `get_asset GR garbage classname` |
| 9 | `TT-011` | Получить элемент коллекции (зависит от редкости) | `get_asset Collection` |

Description: Найди деревянные упоры и что-нибудь тяжёлое под колесо. Я пока телегу придержу!

Congratulation: Упоры подошли. Можно отпустить колесо — дальше телега не покатится.

## Quest 4 — Гости ходят кругами

- classname_quests: `VelesNight_2026_Story_4`
- character: Куйгорож
- task_numbers: 10, 11, 12

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 10 | `TT-028` | Силуэт элемент коллекции (зависит от редкости) | `get_asset Collection is_silhouette` |
| 11 | `TT-021` | Уборка конкретного мусора дома | `garbage classname` |
| 12 | `TT-013` | GR с мусора в локации дома | `get_asset GR garbage location_tags` |

Description: Помоги убрать обломки с дороги. И под лавку загляни: оттуда завязки торчат, надо проверить, что там лежит.

Congratulation: Дорожка свободна. А найденные связки отложим отдельно — пусть Ведятя посмотрит.

## Quest 5 — Беглец из Нави

- classname_quests: `VelesNight_2026_Story_5`
- character: Королева Подземного Царства
- task_numbers: 13, 14, 15

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 13 | `TT-025` | Загадка на мусор дома | `garbage classname mystery` |
| 14 | `TT-026` | Загадка на коллекцию (зависит от редкости) | `get_asset Collection mystery` |
| 15 | `TT-027` | Загадка задом наперед на коллекцию (зависит от редкости) | `get_asset Collection reverse_mystery` |

Description: Осмотри двор у дома и за сараем. По следам проверь, не осталось ли там кого-нибудь из гостей, и вернись ко мне.

Congratulation: Обход закончен. Теперь можно заняться проводами, никого по двору искать не придётся.

## Quest 6 — Верная дорога

- classname_quests: `VelesNight_2026_Story_6`
- character: Ведятя
- task_numbers: 16, 17, 18

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 16 | `TT-013` | GR с мусора в локации дома | `get_asset GR garbage location_tags` |
| 17 | `TT-009` | Получить PER | `get_asset PER` |
| 18 | `TT-002` | Крафт | `get_and_decrease_asset craft` |

Description: Собери крепёжные детали и подготовь крепления для указателей. Поставим их на прежние места.

Congratulation: Крепления готовы, можно закреплять указатели. Проверю, всё ли крепко держится.

## Quest 7 — Королева взаперти

- classname_quests: `VelesNight_2026_Story_7`
- character: Баба Зина
- task_numbers: 19, 20, 21

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 19 | `TT-007` | HOG поиск истинного среди ложного | `HOG clean_debris true_among_false` |
| 20 | `TT-028` | Силуэт элемент коллекции (зависит от редкости) | `get_asset Collection is_silhouette` |
| 21 | `TT-011` | Получить элемент коллекции (зависит от редкости) | `get_asset Collection` |

Description: Осмотри заграждённые окна снаружи. Найди то, к которому Домовед сможет подойти, и покажи мне.

Congratulation: Вижу, какое окно ты выбрал. До этой ставни я изнутри дотянусь.

## Quest 8 — Бунт инструментов

- classname_quests: `VelesNight_2026_Story_8`
- character: Куйгорож
- task_numbers: 22, 23, 24

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 22 | `TT-014` | GR с конкретного мусора в гостях | `get_asset GR in_guest garbage classname` |
| 23 | `TT-016` | GR с цветов в гостях | `get_asset GR in_guest flower` |
| 24 | `TT-021` | Уборка конкретного мусора дома | `garbage classname` |

Description: Нужны крепкие верёвки. Найди их и выбери целые связки — порванные эту стражу не удержат.

Congratulation: Эти выдержат. Давай сюда, пока я грабли держу!

## Quest 9 — Лестница для Домоведа

- classname_quests: `VelesNight_2026_Story_9`
- character: Дед Домовед
- task_numbers: 25, 26, 27

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 25 | `TT-015` | GR с конкретного мусора дома | `get_asset GR garbage classname` |
| 26 | `TT-017` | GR с цветов дома | `get_asset GR flower` |
| 27 | `TT-011` | Получить элемент коллекции (зависит от редкости) | `get_asset Collection` |

Description: Найди принадлежности для лестницы и опорные бруски. Подготовим всё у боковой стены.

Congratulation: Всё принесли. Поставлю лестницу на эти опоры, потом проверим её ещё раз.

## Quest 10 — Зина, отойди от окна!

- classname_quests: `VelesNight_2026_Story_10`
- character: Баба Зина
- task_numbers: 28, 29, 30

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 28 | `TT-006` | HOG в виде скрытого предмета | `HOG clean_debris hidden_object` |
| 29 | `TT-030` | Силуэт мусора  дома | `garbage classname is_silhouette` |
| 30 | `TT-021` | Уборка конкретного мусора дома | `garbage classname` |

Description: Найди деревянные клинья для лестницы и убери солому с места спуска. Нельзя, чтобы под ногами скользило.

Congratulation: Клинья на месте, внизу чисто. Теперь можно подниматься к окну.

## Quest 11 — Барину пора домой

- classname_quests: `VelesNight_2026_Story_11`
- character: Королева Подземного Царства
- task_numbers: 31, 32, 33

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 31 | `TT-014` | GR с конкретного мусора в гостях | `get_asset GR in_guest garbage classname` |
| 32 | `TT-008` | Получить ASK | `get_asset ASK` |
| 33 | `TT-002` | Крафт | `get_and_decrease_asset craft` |

Description: Подготовь крепления для оберегов, которые нашли под лавкой. Домовед вернёт их на ограду.

Congratulation: Крепления подошли, обереги держатся. Благодарю за помощь.

## Quest 12 — Один Дед — и хватит

- classname_quests: `VelesNight_2026_Story_12`
- character: Дед Домовед
- task_numbers: 34, 35, 36

| № | Template ID | Template name | Task type |
|---|-------------|---------------|-----------|
| 34 | `TT-030` | Силуэт мусора  дома | `garbage classname is_silhouette` |
| 35 | `TT-021` | Уборка конкретного мусора дома | `garbage classname` |
| 36 | `TT-034` | Фото предмета | `action post_photo` |

Description: Помоги убрать остатки связок и вернуть инструменты на места. Доски с двери я сниму сам.

Congratulation: Всё прибрали. Спасибо тебе — сегодня ты нас очень выручил.
