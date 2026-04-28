# Workflow Guide

Эта памятка нужна, чтобы несколько человек могли работать с проектом без путаницы в campaign, pack, quest и task.

## Быстрый Формат Запроса

```text
Mode: quest_edit
Campaign: MeatballRain_2026
Pack: pack_001
Stage: 4
Quest: 2
Task: 1
Правка: замени выбранный мусор на более смешной, без повторов campaign.
```

Если активный контекст уже выставлен, можно короче:

```text
В активном контексте: квест 2, таск 1, замени мусор Аммонит.
```

## Активный Контекст

Текущий контекст хранится здесь:

```text
workspace/active_context.json
```

Порядок ответа на вопросы про текущую сессию:

1. Сначала прочитать `workspace/active_context.json`.
2. Взять оттуда `mode`, `campaign_id`, `pack_id`, `stage`, `quest_number`, `task_number`.
3. Если пользователь спрашивает про выбранные шаблоны этапа 3, открыть `campaigns/<campaign_id>/<pack_id>/stage3_quests.txt`.
4. Если пользователь спрашивает про кандидатов, заполненные task objects или `quest_group`, искать соответствующие файлы в `campaigns/<campaign_id>/<pack_id>/` и затем в `output/`.
5. Если active context отсутствует или неполный, сказать это явно и только потом делать осторожный вывод по ближайшим campaign/output файлам.

Показать:

```bash
python src/workflow_context.py show
```

Выставить:

```bash
python src/workflow_context.py set --mode quest_edit --campaign MeatballRain_2026 --pack pack_001 --stage 4 --quest 2 --task 1
```

Определить режим по тексту:

```bash
python src/workflow_context.py detect --text "замени мусор в квесте 2 таске 1"
```

Определить и сразу применить:

```bash
python src/workflow_context.py detect --text "создай csv" --apply
```

## Список Режимов

Источник правды:

```text
workflows/workflow_modes.json
```

Посмотреть список:

```bash
python src/workflow_context.py list-modes
```

### quest_generation

Поэтапное создание нового pack квестов или продолжение campaign.

Обязательное уточнение перед стартом нового pack:

- нужно явно указать количество квестов, например `3 квеста`;
- или явно разрешить свободный объем: `придумай сколько хочешь`.

Если в запросе есть тема, персонажи и campaign/pack, но нет количества квестов и нет разрешения на свободный объем, генерацию надо остановить и коротко уточнить количество.

Обязательные human approval gates:

- Codex выполняет только один этап за раз.
- После этапа 1 нужно показать пользователю сюжетную структуру и ждать явный апрув в чате.
- После этапа 2 нужно показать реплики начала/завершения и ждать явный апрув.
- После этапа 3 нужно показать выбранные `Task template ID`, русские названия шаблонов и `Task type`, затем ждать апрув.
- После апрува этапа 3 нужно записать gate: `python src/workflow_context.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>`.
- `python src/build_context_pack.py ...` технически откажется собирать `context_pack`, если approval stage 3 не записан для того же campaign/pack.
- После этапа 3.1 нужно показать `context_pack`/подбор кандидатов и ждать апрув.
- После этапа 4 нужно показать `filled_tasks`, итог валидации и ждать апрув.
- После апрува этапа 4 нужно записать gate: `python src/workflow_context.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>`.
- Этап 5 создает `campaigns/<campaign_id>/<pack_id>/quest_group.json`: ИИ анализирует все квесты pack и пишет `title`, `description`, `description_complete`, `description_spoil`.
- После этапа 5 нужно показать `quest_group`/preview и ждать явный апрув пользователя.
- После апрува этапа 5 нужно записать gate: `python src/workflow_context.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>`.
- Этап 6 и CSV запускать только после апрува этапа 5; CSV берет `quest_group.json` из папки того же pack.
- Нельзя выполнять новый pack целиком одним прогоном, даже если технически все команды уже известны.

Нумерация generated-объектов внутри одной campaign не начинается заново в новом pack. Если `pack_001` уже использовал `MeatballRain_2026_HOG_1`, `MeatballRain_2026_GR_1`, `MeatballRain_2026_ASK_1` и `MeatballRain_2026_R_1`, то следующий pack продолжает с `HOG_2`, `GR_2`, `ASK_2` и `R_2` для того же campaign prefix. Для этого этап 4 и валидатор читают `campaign_memory.json`.

Ключевики:

- создай квест
- создай пак
- новый пак
- продолжаем campaign
- этап 1
- этап 3
- пройди этапы
- три квеста
- новая тема
- персонажи

### quest_edit

Правка конкретного квеста или таска.

Ключевики:

- поменяй таск
- замени таск
- замени мусор
- замени цветок
- замени коллекцию
- исправь квест
- квест 2
- таск 1
- этап 4 правка

### csv_export

Валидация и экспорт CSV на этапе 6.

Ключевики:

- создай csv
- экспорт csv
- этап 6
- сгенерируй таблицу
- generated_quests.csv

### quest_group_creation

Создание квестовой группы на этапе 5.

Ключевики:

- квестовая группа
- quest group
- quest_group
- этап 5
- описание квестовой группы
- журнал квестов

### campaign_management

Создание campaign/pack и обновление памяти.

Ключевики:

- создай кампанию
- создай campaign
- создай pack
- обнови память
- память кампании
- campaign_summary
- pack_001

### validation_review

Анализ ошибок и предупреждений.

Ключевики:

- валидация
- validation
- errors
- warnings
- critical issues
- validation_report
- validation_summary

### raw_indexing

Пересборка игровых индексов.

Ключевики:

- пересобери индексы
- raw данные
- quest-ready
- quest_ready_index
- drops.index

### pot_description

Будущий отдельный workflow: по картинке горшка написать описание в стиле проекта.

Ключевики:

- горшок
- картинка горшка
- фото горшка
- опиши горшок
- описание в нашем стиле
- стиль домовят

### workflow_management

Редактирование этой памятки, списка режимов и active context.

Ключевики:

- режимы работы
- активный контекст
- памятка
- workflow
- воркфлоу
- ключевики

## Правило Для Команды

Если запрос может относиться к нескольким campaign или pack, обязательно указывать:

- `Campaign`
- `Pack`
- `Quest`
- `Task`
- `Stage`

Если этих полей нет, сначала смотри `workspace/active_context.json`.
