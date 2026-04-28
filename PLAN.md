# PLAN.md — план разработки системы генерации квестовых тасков

## 1. Назначение системы

Система нужна для автоматической подготовки квестовых тасков для легаси-игры.

Главная конечная цель:

1. Пользователь дает системе набор квестов после этапа 3.
2. В каждом квесте уже есть:
   - `Classname quests`
   - `title_quest`
   - `№ quest`
   - `№ task`
   - `Task type`
   - `description`
   - `congratulation`
   - `Character`
3. Система выбирает нужные шаблоны тасков по `Task type`.
4. Система заполняет шаблоны реальными игровыми данными:
   - реальные `classname`
   - реальные `title`
   - реальные локации
   - реальные теги локаций
   - реальные связи мусор → коллекция
   - реальные связи цветок → коллекция
5. Система формирует task objects.
6. Система разворачивает task objects в CSV строго по рабочему формату.
7. CSV передается в существующий pipeline, который создает XLSX/prototype-файлы.

Важно:

- Система не должна выдумывать игровые факты.
- Система не должна менять `raw/` файлы автоматически.
- Система должна использовать только quest-ready данные.
- Финальный формат для пользователя — CSV, а не markdown и не JSON.
- JSON task object — только промежуточный формат внутри системы.

---

## 2. Текущее состояние проекта

Первый этап уже реализован.

Проект умеет:

- читать raw-данные из:
  - `raw/locations/`
  - `raw/garbage/`
  - `raw/flowers/`
  - `raw/collections/`
- строить базовые индексы:
  - `data/master_index.json`
  - `data/garbage.index.json`
  - `data/flowers.index.json`
  - `data/collections.index.json`
  - `data/drops.index.json`
  - `data/validation_report.json`
- строить quest-ready индексы:
  - `data/quest_ready_index.json`
  - `data/quest_ready_drops.index.json`
  - `data/non_critical_issues.json`
  - `data/critical_issues.json`
  - `data/excluded_entities.json`
  - `data/validation_summary.md`
- отделять критичные проблемы от некритичных
- исключать ненужные сущности из quest-ready базы
- строить связи:
  - мусор → элемент коллекции
  - цветок → элемент коллекции
  - мусор → локация

Текущее состояние:

- `critical_issues.json` должен быть пустым.
- Если появляются новые critical issues, сначала нужно исправить данные или правила фильтрации, и только потом продолжать генерацию квестов.

---

## 3. Главная архитектура

Общая схема:

```text
raw game data
  ↓
src/build_index.py
  ↓
quest-ready indexes
  ↓
stage 3 quest input
  ↓
task type resolver
  ↓
task template filler
  ↓
task objects
  ↓
CSV exporter
  ↓
generated CSV
  ↓
existing XLSX/prototype pipeline
```

---

## 3.1. Важное уточнение: роль ИИ и роль кода

Финальная система не должна быть полностью детерминированным генератором, который сам случайно или по очереди выбирает мусор, цветы и коллекции.

Правильная архитектура для задумки:

```text
ИИ создает этапы 1-2
  ↓
ИИ выбирает Task type на этапе 3 по контексту сюжета
  ↓
код парсит stage3 в QuestPlan
  ↓
код готовит quest-ready context pack для ИИ
  ↓
ИИ заполняет task objects этапа 4 по шаблонам и контексту
  ↓
код валидирует task objects против quest-ready indexes
  ↓
код экспортирует валидные task objects в CSV этапа 5
```

То есть:

- ИИ отвечает за творческий выбор: какие механики подходят к description/congratulation и какие игровые данные лучше подходят по смыслу.
- Код отвечает за факты: проверяет, что classname/title/location/collection реально существуют в `quest_ready_index.json` и `quest_ready_drops.index.json`.
- Код не должен выдумывать игровые факты и не должен подменять творческий выбор ИИ слепым round-robin выбором.
- Детерминированный `fill_tasks.py` может существовать как ранний технический прототип, но не должен считаться финальной моделью этапа 4.

Ключевая идея: ИИ заполняет JSON task object, а код выступает как data guardrail, validator и CSV exporter.

---

## 4. Как пользователь будет общаться с ИИ через систему

Пользователь не должен вручную искать classname, title, location, collection или garbage.

Предполагаемый рабочий процесс:

### Шаг 1. Подготовить raw-данные

Пользователь кладет игровые данные в папки:

```text
raw/locations/
raw/garbage/
raw/flowers/
raw/collections/
```

### Шаг 2. Собрать quest-ready базу

Пользователь запускает:

```bash
python src/build_index.py
```

Система обновляет:

```text
data/quest_ready_index.json
data/quest_ready_drops.index.json
data/critical_issues.json
data/non_critical_issues.json
data/validation_summary.md
```

Если `critical_issues.json` не пустой, пользователь сначала исправляет raw-данные или правила фильтрации.

### Шаг 3. Дать системе квесты после этапа 3

Пользователь кладет входной файл, например:

```text
input/stage3_quests.txt
```

Формат похож на:

```text
Classname quests: Event_2026_Story_1
title_quest: Название квеста
№ quest: 1
№ task: 1 2 3
Task type: garbage classname in_guest / get_asset Collection / action take_crop_in_guest
description: "..."
Tasks:
[пусто]
congratulation: "..."
Character: Персонаж
```

### Шаг 4. Запустить генерацию task objects

Пользователь запускает:

```bash
python src/fill_tasks.py input/stage3_quests.txt
```

Система создает промежуточный файл:

```text
output/generated_task_objects.json
```

В нем каждый task уже заполнен реальными данными.

### Шаг 5. Проверить task objects

Пользователь может открыть:

```text
output/generated_task_objects.preview.md
```

Там должна быть человекочитаемая проверка:

- какой task type был выбран
- какой шаблон использован
- какие игровые данные подставлены
- почему выбрана именно эта локация/мусор/коллекция/цветок
- были ли fallback-решения

### Шаг 6. Экспортировать CSV

Пользователь запускает:

```bash
python src/export_csv.py output/generated_task_objects.json
```

Система создает:

```text
output/generated_quests.csv
```

Этот CSV идет в существующий XLSX/prototype pipeline.

### Шаг 7. При необходимости попросить ИИ поправить

Пользователь может сказать Codex:

```text
Проверь output/generated_task_objects.preview.md.
Мне не нравится, что часто используется одна и та же локация.
Добавь правило разнообразия локаций в пределах одного пакета квестов.
Обнови PLAN.md, если меняешь архитектуру.
```

Или:

```text
Добавь поддержку нового task type из инструкции этапа 4:
get_asset Collection mystery.
Сначала добавь шаблон, тесты, preview, потом CSV export.
Обнови PLAN.md.
```

---

## 5. Как будут использоваться подготовленные quest-ready данные

Генератор должен использовать только:

```text
data/quest_ready_index.json
data/quest_ready_drops.index.json
```

Не использовать напрямую:

```text
data/master_index.json
data/drops.index.json
data/validation_report.json
```

Причина:

- raw-индексы содержат все найденные игровые данные
- quest-ready индексы содержат только то, что пригодно для генерации квестов

---

## 6. Основные типы данных

### 6.1. Локации

Используются для:

- `garbage location_tags`
- `garbage location_index`
- hints с местом поиска
- фильтрации мусора
- разнообразия квестов

Важные поля:

```text
code
title
tags
garbage_assets
```

### 6.2. Мусор

Используется для:

- `garbage classname`
- `garbage classname in_guest`
- `get_asset Collection`, если collection выпадает из мусора
- `get_asset GR garbage`, если будущий GR будет привязан к мусору

Важные поля:

```text
classname
title
id
locations
drops_home
drops_guest
```

### 6.3. Цветы

Используются для:

- `action take_crop`
- `action take_crop_in_guest`
- `get_asset Collection`, если collection выпадает из цветка
- `get_asset GR flower`, если будущий GR будет привязан к цветку

Важные поля:

```text
classname
title
id
tags
req_user_level
drops_home
drops_guest
```

### 6.4. Элементы коллекций

Используются для:

- `get_asset Collection`
- `get_asset Collection is_silhouette`
- `get_asset Collection mystery`

Важные поля:

```text
classname
title
id
drop_from
```

---

## 7. Правила выбора данных

### 7.1. Общие правила

1. Не выдумывать факты.
2. Если нет подходящей quest-ready связи, создать warning.
3. Не использовать excluded entities.
4. Не использовать missing title.
5. Избегать повторов внутри одного квеста.
6. Избегать повторов в соседних квестах, если это возможно.
7. Для одного квеста не использовать одинаковый task type дважды, кроме mystery-исключений.
8. При прочих равных выбирать данные, лучше подходящие к контексту `description` и `congratulation`.
9. Если контекст не дает явной подсказки, использовать разнообразие:
   - разные локации
   - разные виды мусора
   - разные коллекции
   - разные цветы

### 7.2. Выбор мусора

Для `garbage classname`:

- выбрать quest-ready мусор
- у мусора должен быть `title`
- у мусора должна быть хотя бы одна quest-ready location
- hint должен содержать название локации

Для `garbage classname in_guest`:

- то же, но добавить `in_guest: 1`

### 7.3. Выбор коллекции из мусора

Для `get_asset Collection`, если нужен мусорный источник:

- брать из `quest_ready_drops.index.json`
- `source_type = "garbage"`
- `collection_title` заполнен
- `garbage_title` заполнен
- `locations` не пустой
- mode:
  - `home`, если task без `in_guest`
  - `guest`, если task связан с гостями

### 7.4. Выбор коллекции из цветка

Для collection, выпадающей из цветка:

- брать из `quest_ready_drops.index.json`
- `source_type = "flower"`
- `collection_title` заполнен
- `flower_title` заполнен
- mode:
  - `home`, если `take_crop`
  - `guest`, если `take_crop_in_guest`

### 7.5. Выбор цветка

Для `take_crop` и `take_crop_in_guest`:

- брать из `quest_ready_index.json.quest_ready_flowers`
- у цветка должен быть `title`
- у цветка должен быть `classname`
- `param` = classname цветка
- если task in_guest, action = `take_crop_in_guest`
- иначе action = `take_crop`

---

## 8. Task type resolver

Нужно создать компонент, который принимает строку `Task type` и определяет, какой шаблон использовать.

Пример:

```text
garbage classname in_guest
```

должен превратиться в:

```json
{
  "template_id": "garbage_classname_in_guest",
  "source_kind": "garbage",
  "guest_mode": true
}
```

Пример:

```text
get_asset Collection is_silhouette
```

должен превратиться в:

```json
{
  "template_id": "get_asset_collection_silhouette",
  "source_kind": "collection",
  "silhouette": true
}
```

Нужно поддерживать разные варианты написания:

```text
garbage classname in_guest
Garbage classname in_guest
get_asset Collection
action clean_debris HOG
action take_crop_in_guest
get_asset GR in_guest garbage
get_asset GR in_guest Flower
```

Для неизвестного task type:

- не падать
- добавить warning
- оставить task незаполненным или заполнить placeholder с ошибкой
- записать в `output/generation_report.json`

---

## 9. Task templates

Нужно создать:

```text
data/task_templates.json
```

или Python-модуль:

```text
src/task_templates.py
```

Рекомендуется начать с Python-модуля, чтобы проще обрабатывать условия.

Минимальный первый набор шаблонов:

1. `garbage classname in_guest`
2. `garbage classname`
3. `garbage location_tags in_guest`
4. `garbage location_tags`
5. `get_asset Collection`
6. `get_asset Collection is_silhouette`
7. `action take_crop_in_guest`
8. `action take_crop`
9. `get_asset GR in_guest garbage`
10. `get_asset GR garbage`

Не нужно сразу делать все 20+ шаблонов.

---

## 10. Минимальный набор шаблонов для первого рабочего прототипа

### 10.1. garbage classname in_guest

Task object:

```json
{
  "type": "garbage",
  "classname": "<garbage_classname>",
  "in_guest": 1,
  "amount": 1,
  "price": 1,
  "title": "Убери <garbage_title>",
  "hint": "Чтобы убрать мусор - нажми на него мышкой в гостях друга. Место поиска: <location_title>."
}
```

### 10.2. garbage classname

```json
{
  "type": "garbage",
  "classname": "<garbage_classname>",
  "amount": 1,
  "price": 1,
  "title": "Убери <garbage_title>",
  "hint": "Чтобы убрать мусор - нажми на него мышкой дома. Место поиска: <location_title>."
}
```

### 10.3. get_asset Collection

```json
{
  "type": "get_asset",
  "classname": "<collection_classname>",
  "icon": "<collection_classname>",
  "amount": 1,
  "price": 1,
  "title": "Найди <collection_title>",
  "hint": "<collection_title> - элемент коллекции, выпадает при уборке мусора <garbage_title> дома. Место поиска: <location_title>"
}
```

### 10.4. get_asset Collection is_silhouette

```json
{
  "type": "get_asset",
  "classname": "<collection_classname>",
  "icon": "<collection_classname>",
  "amount": 1,
  "price": 1,
  "is_silhouette": 1,
  "title": "Угадай, элемент коллекции",
  "hint": "Угадай, загаданный элемент коллекции и найди его"
}
```

### 10.5. action take_crop_in_guest

```json
{
  "type": "action",
  "action": "take_crop_in_guest",
  "title": "Собери <flower_title> в гостях",
  "hint": "Собирай <flower_title> в гостях. Чтобы собрать растение, кликни на горшок с нужным растением в гостях у друга",
  "param": "<flower_classname>",
  "amount": 1,
  "price": 1
}
```

### 10.6. action take_crop

```json
{
  "type": "action",
  "action": "take_crop",
  "title": "Собери <flower_title>",
  "hint": "Собирай <flower_title> дома. Чтобы собрать растение, кликни на горшок с нужным растением",
  "param": "<flower_classname>",
  "amount": 1,
  "price": 1
}
```

---

## 11. GR, PER, ASK, Craft — отдельный этап

Некоторые шаблоны требуют данных, которых пока нет в quest-ready index:

- GR resources
- PER
- ASK
- recipes
- characters
- craft actions
- free gifts
- HOG objects
- dialog actions

Поэтому их нельзя полноценно делать на первом шаге task generation.

Для них нужно будет добавить новые raw-папки:

```text
raw/resources/
raw/requests/
raw/recipes/
raw/characters/
raw/hog/
raw/free_gifts/
```

И затем расширить `build_index.py`.

До этого момента можно поддержать такие task types в режиме placeholder:

```json
{
  "status": "needs_data_source",
  "task_type": "get_asset GR in_guest garbage",
  "missing_source": "raw/resources"
}
```

---

## 12. CSV exporter

CSV exporter должен принимать task objects и раскладывать их в рабочую CSV-структуру.

Нужно создать:

```text
src/export_csv.py
```

Вход:

```text
output/generated_task_objects.json
```

Выход:

```text
output/generated_quests.csv
```

CSV должен:

- использовать `;` как разделитель
- сохранять структуру примера
- не ломать кириллицу
- желательно поддерживать encoding:
  - `utf-8-sig`
  - или `cp1251`, если это нужно текущему XLSX pipeline
- массивы и вложенные объекты записывать как JSON-строку в значение поля

Пример разворота task object:

```json
{
  "type": "garbage",
  "classname": "Ashes",
  "in_guest": 1,
  "amount": 1,
  "price": 1,
  "title": "Убери Пепел",
  "hint": "..."
}
```

должен стать CSV-блоком:

```text
;;;type;garbage
;;;classname;Ashes
;;;in_guest;1
;;;amount;1
;;;price;1
;;;title;Убери Пепел
;;;hint;...
;;;identifier
```

---

## 13. Входные и выходные файлы будущего этапа

### Вход

```text
input/stage3_quests.txt
data/quest_ready_index.json
data/quest_ready_drops.index.json
raw/examples/Инструкция этап 4.txt
raw/examples/Пример квестов по шаблону в csv.csv
```

### Промежуточный выход

```text
output/generated_task_objects.json
output/generated_task_objects.preview.md
output/generation_report.json
```

### Финальный выход

```text
output/generated_quests.csv
```

---

## 14. Preview-файл

Нужно обязательно делать preview-файл, чтобы пользователь мог проверять результат до CSV.

Файл:

```text
output/generated_task_objects.preview.md
```

В нем для каждого квеста:

```markdown
# Quest 1 — Название

## Task 1

Task type: garbage classname in_guest
Template: garbage_classname_in_guest

Selected data:
- garbage: Ashes / Пепел
- location: Котельная
- mode: guest

Generated task:

```json
{
  "type": "garbage",
  "classname": "Ashes",
  "in_guest": 1,
  "amount": 1,
  "price": 1,
  "title": "Убери Пепел",
  "hint": "..."
}
```

Warnings:
- none
```

---

## 15. Generation report

Нужно создать:

```text
output/generation_report.json
```

В нем хранить:

- unknown task types
- missing data
- repeated entities
- fallback choices
- skipped tasks
- unsupported templates

Пример:

```json
{
  "summary": {
    "quests": 10,
    "tasks": 30,
    "filled_tasks": 24,
    "placeholder_tasks": 6,
    "warnings": 8,
    "errors": 0
  },
  "warnings": [
    {
      "quest": 3,
      "task": 8,
      "code": "unsupported_task_type",
      "task_type": "get_asset PER",
      "message": "No data source for PER yet"
    }
  ]
}
```

---

## 16. Правила обновления PLAN.md

Codex должен обновлять этот файл, если:

1. Добавлен новый этап разработки.
2. Изменилась структура папок.
3. Добавлен новый источник raw-данных.
4. Добавлен новый task type.
5. Изменилась логика quest-ready фильтрации.
6. Изменился CSV-формат.
7. Добавлен новый CLI.
8. Изменился пользовательский workflow.

Codex не должен переписывать план полностью без необходимости.

Лучше добавлять раздел:

```markdown
## Changelog

### YYYY-MM-DD

- Что изменено
- Почему изменено
- Какие файлы затронуты
```

---

## 17. Рекомендуемый порядок разработки дальше

Важно: порядок ниже нужно читать с учетом раздела 3.1. После `parse_stage3` главный следующий шаг — не расширять слепой filler, а добавить слой подготовки данных для ИИ и валидации ИИ-заполненных task objects.

### Этап 2. Parser для stage3 quests

Цель:

- прочитать текст этапа 3
- распарсить квесты
- получить структуру `QuestPlan`

Файлы:

```text
src/parse_stage3.py
tests/test_parse_stage3.py
```

Выход:

```text
output/quest_plan.json
```

### Этап 3. Task type resolver

Цель:

- разобрать строку `Task type`
- сопоставить каждый task type с template_id
- подготовить понятную структуру для ИИ и валидатора: какой шаблон нужен каждому task

Файлы:

```text
src/task_type_resolver.py
tests/test_task_type_resolver.py
```

### Этап 4. Context pack для ИИ

Цель:

- по каждому квесту и task type подготовить ограниченный набор подходящих quest-ready кандидатов
- включить description, congratulation, character и title_quest как контекст выбора
- не выбирать финальные данные вместо ИИ, а дать ИИ безопасный набор фактов

Файлы:

```text
src/build_context_pack.py
tests/test_build_context_pack.py
```

Выход:

```text
output/context_pack.json
output/context_pack.preview.md
```

### Этап 5. AI-filled task object validator

Цель:

- принять task objects, заполненные ИИ по инструкции этапа 4
- проверить каждый classname/title/location/collection против quest-ready данных
- проверить соответствие шаблону
- создать actionable ошибки, если ИИ выбрал несуществующий или неподходящий asset

Файлы:

```text
src/task_templates.py
src/validate_task_objects.py
tests/test_validate_task_objects.py
```

### Этап 6. Preview

Цель:

- создать человекочитаемый preview
- показать, что ИИ выбрал, почему это прошло или не прошло валидацию
- показать warning-и и ошибки

Файлы:

```text
src/render_preview.py
tests/test_render_preview.py
```

### Этап 7. CSV exporter

Цель:

- развернуть task objects в CSV
- повторить структуру рабочего CSV-примера

Файлы:

```text
src/export_csv.py
tests/test_export_csv.py
```

### Этап 8. Поддержка всех шаблонов этапа 4

Цель:

- постепенно добавить остальные task types
- не добавлять шаблон без теста
- не добавлять шаблон без preview
- не добавлять шаблон без validator-правил

### Этап 9. Новые raw-источники

Цель:

- добавить GR
- добавить PER/ASK
- добавить recipes
- добавить characters
- добавить HOG
- добавить free gifts

---

## 18. Следующий конкретный prompt для Codex

Первый следующий prompt после завершенного build_index этапа:

```text
Мы завершили первый этап: quest-ready индексы собраны, critical_issues.json пустой.

Теперь нужно начать второй этап — парсинг входного файла этапа 3.

Не делай генерацию тасков и CSV пока.

Задача:

1. Создать папку input/, если ее нет.
2. Создать модуль src/parse_stage3.py.
3. Модуль должен читать текстовый файл input/stage3_quests.txt.
4. Нужно распарсить квесты в структуру QuestPlan.

Каждый квест должен содержать:
- classname_quests
- title_quest
- quest_number
- task_numbers
- task_types
- description
- congratulation
- character
- raw_text

5. Поле Task type содержит несколько типов через "/".
   Нужно разбить их в список task_types.

6. Создать CLI:
   python src/parse_stage3.py input/stage3_quests.txt

7. CLI должен сохранить:
   output/quest_plan.json

8. Также создать:
   output/quest_plan.preview.md

9. Добавить тесты:
   tests/test_parse_stage3.py

10. Тест должен проверять минимум:
   - один квест
   - несколько квестов
   - корректное разбиение Task type по "/"
   - корректное чтение description и congratulation
   - корректное чтение Character

11. Обновить README.md.
12. Обновить PLAN.md, добавив changelog.

Важно:
- Не реализовывать fill_tasks.
- Не реализовывать CSV export.
- Все ответы и комментарии писать на русском.
```

---

## 19. Definition of Done для следующего этапа

Этап `parse_stage3` считается готовым, если:

1. Команда работает:

```bash
python src/parse_stage3.py input/stage3_quests.txt
```

2. Создаются файлы:

```text
output/quest_plan.json
output/quest_plan.preview.md
```

3. Тесты проходят:

```bash
python -m unittest discover -s tests
```

4. README обновлен.
5. PLAN.md обновлен.
6. Генерация тасков и CSV еще не добавлена.

---

## 20. Changelog

### 2026-04-28

- Уточнена архитектура этапов 3-5: финальный путь должен использовать ИИ для творческого выбора task types и игровых данных по контексту, а код должен готовить quest-ready context pack, валидировать AI-filled task objects и экспортировать CSV.
- Зафиксировано, что детерминированный `fill_tasks.py` является техническим прототипом, а не финальной моделью этапа 4.
- Рекомендуемый порядок разработки изменен: после `parse_stage3` нужно делать `task_type_resolver`, `context_pack`, `validate_task_objects`, preview и только потом CSV exporter.

- Реализован этап `parse_stage3`: добавлены `src/parse_stage3.py`, `tests/test_parse_stage3.py`, папка `input/`.
- CLI `python src/parse_stage3.py input/stage3_quests.txt` сохраняет `output/quest_plan.json` и `output/quest_plan.preview.md`.
- README обновлен инструкцией по парсингу входного файла этапа 3.
- Генерация task objects и CSV в рамках этого изменения не расширялась.

- Сформирован полный план разработки после завершения этапа build_index.
- Зафиксирована архитектура: quest-ready indexes → task objects → CSV.
- Зафиксирован будущий пользовательский workflow.
- Определен следующий этап: `parse_stage3`.
