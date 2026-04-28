# quest-data-builder

Парсер raw-данных легаси-игры для построения игровых индексов и подготовки quest-ready данных. Проект также содержит рабочий пайплайн для этапов 3-5: разбор плана квестов, сбор компактного context pack, валидация заполненных task objects и CSV-экспорт.

Полная творческая генерация квестов остается ручным/ИИ-этапом. Код не придумывает сюжет и не выбирает task object творчески без ИИ.

## Запуск

```bash
python src/build_index.py
```

Команда читает файлы из:

- `raw/locations/`
- `raw/garbage/`
- `raw/flowers/`
- `raw/collections/`

Файлы в `raw/` не изменяются.

## Выходные файлы

Базовые индексы:

- `data/master_index.json`
- `data/garbage.index.json`
- `data/flowers.index.json`
- `data/collections.index.json`
- `data/drops.index.json`
- `data/validation_report.json`

Quest-ready файлы:

- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`
- `data/critical_issues.json`
- `data/non_critical_issues.json`
- `data/excluded_entities.json`
- `data/validation_summary.md`

`quest_ready_index.json` содержит только данные, пригодные для будущей генерации: локации с известным мусором, активный мусор, валидные цветы и коллекции, реально используемые в quest-ready drops.

`critical_issues.json` содержит только проблемы, которые нужно исправлять руками перед генерацией.

`non_critical_issues.json` содержит проблемы, которые можно игнорировать для quest-ready генерации: пустые локации, неизвестный мусор из `location.garbage_assets`, неиспользуемый мусор и missing collection assets из игнорируемых паттернов `Cocoon/Web/Common/Mold`.

## Анализ существующего отчета

Обычно отдельный запуск не нужен, потому что `python src/build_index.py` уже создает `data/validation_summary.md`.

Если нужно пересобрать только Markdown summary из уже созданных JSON-файлов:

```bash
python src/analyze_validation.py
```

## Парсинг квестов этапа 3

Положи текстовый результат этапа 3 в:

```text
input/stage3_quests.txt
```

Запуск:

```bash
python src/parse_stage3.py input/stage3_quests.txt
```

Команда создает:

- `output/quest_plan.json`
- `output/quest_plan.preview.md`

`quest_plan.json` содержит список QuestPlan. Для каждого квеста сохраняются:

- `classname_quests`
- `title_quest`
- `quest_number`
- `task_numbers`
- `task_template_ids`
- `task_template_names`
- `task_types`
- `tasks` — связанный список заданий с `task_number`, `task_template_id`, `task_template_name`, `task_type`
- `description`
- `congratulation`
- `character`
- `raw_text`

Актуальный формат этапа 3 должен содержать синхронные строки:

```text
Task template ID: TT-020 / TT-014 / TT-033
Task template name: Уборка конкретного мусора в гостях / GR с конкретного мусора в гостях / Передача предмета
Task type: garbage classname in_guest / get_asset GR in_guest garbage classname / action give
```

Парсер проверяет, что количество `№ task`, `Task template ID`, `Task template name` и `Task type` совпадает. Шаблон `TT-035` считается `not_ready` и будет записан в issues.

## Проверка шаблонов этапа 3

После парсинга можно проверить, что выбранные ID, русские названия и `Task type` совпадают с актуальным каталогом шаблонов:

```bash
python src/task_type_resolver.py output/quest_plan.json
```

Команда читает:

- `output/quest_plan.json`
- `data/task_templates.json`

И создает:

- `output/quest_plan.resolved.json`
- `output/quest_plan.resolved.preview.md`

`data/task_templates.json` содержит актуальный машинный каталог `TT-001` ... `TT-035`. Шаблон `TT-035` помечен как `not_ready` и не должен использоваться в этапе 3.

## Ручные правки этапов 3 и 4

Если после просмотра этапа 3 нужно заменить конкретный тип задания или дать указания для выбора кандидатов на этапе 4, используй overrides.

Пример лежит здесь:

```text
input/manual_overrides.example.json
```

Рабочий файл по умолчанию:

```text
input/manual_overrides.json
```

Применение:

```bash
python src/apply_overrides.py output/quest_plan.json input/manual_overrides.json
```

Команда создает:

- `output/quest_plan.overridden.json`
- `output/manual_overrides_report.md`

Пример замены шаблона этапа 3:

```json
{
  "classname_quests": "CosmoDay_2025_Story_4",
  "task_number": 11,
  "replace_template": {
    "task_template_id": "TT-026",
    "task_template_name": "Загадка на коллекцию (зависит от редкости)",
    "task_type": "get_asset Collection mystery"
  }
}
```

Пример указаний для этапа 4:

```json
{
  "classname_quests": "CosmoDay_2025_Story_4",
  "task_number": 12,
  "avoid_candidates": ["garbage:Ashes"],
  "prefer_candidates": ["garbage:BrokenPlate"],
  "prefer_instruction": "Выбери более магический или музыкальный вариант."
}
```

После stage3-правок запускай resolver уже на overridden-файле:

```bash
python src/task_type_resolver.py output/quest_plan.overridden.json
```

## Сбор context pack для этапа 4

После проверки шаблонов можно собрать компактный пакет реальных кандидатов для ИИ:

```bash
python src/build_context_pack.py output/quest_plan.resolved.json
```

Команда читает:

- `output/quest_plan.resolved.json`
- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`

И создает:

- `output/context_pack.json`
- `output/context_pack.preview.md`
- `output/context_candidate_history.json`

`context_pack.json` не заполняет task object автоматически. Он дает ИИ короткий список реальных кандидатов по каждому заданию: мусор, цветы, collection drops или GR-источники. По умолчанию используется до 12 кандидатов на task.

История кандидатов нужна, чтобы похожие задания в следующих запусках не получали один и тот же первый набор вариантов. Если нужно начать подбор заново:

```bash
python src/build_context_pack.py output/quest_plan.resolved.json --reset-history
```

## Валидация заполненных task objects этапа 4

После того как ИИ заполнит task objects по `output/context_pack.json`, результат нужно сохранить в:

```text
output/filled_tasks.json
```

Пример формата:

```text
output/filled_tasks.example.json
```

Проверка:

```bash
python src/validate_task_objects.py output/filled_tasks.json
```

Команда читает:

- `output/filled_tasks.json`
- `output/context_pack.json`
- `data/task_templates.json`

И создает:

- `output/filled_tasks.validation.json`
- `output/filled_tasks.preview.md`

Валидатор проверяет:

- task существует в `context_pack`;
- `task_template_id` совпадает с контекстом;
- `selected_candidate_id` есть среди кандидатов этого task;
- `task_object` содержит обязательные поля для своего `TT-...`;
- garbage/flower/collection classname не выдуманы и совпадают с выбранным кандидатом;
- `TT-035` не используется;
- базовые поля `type`, `action`, `in_guest`, `is_hide`, `is_silhouette` соответствуют шаблону.

## CSV-экспорт этапа 5

CSV создается только из валидного `output/filled_tasks.json`.

Сначала обязательно запусти проверку этапа 4:

```bash
python src/validate_task_objects.py output/filled_tasks.json
```

После успешной проверки:

```bash
python src/export_csv.py output/filled_tasks.json
```

Команда читает:

- `output/filled_tasks.json`
- `output/filled_tasks.validation.json`

И создает:

- `output/generated_quests.csv`

Если в `output/filled_tasks.validation.json` есть errors или validation-файл старее `filled_tasks.json`, CSV не будет создан. Этап 5 не меняет `title`, `hint`, `classname`, `param`, `icon`, локации и нумерацию generated-сущностей; он раскладывает готовые данные в структуру `Квест N -> Таск 1..N`.

Для каждого квеста CSV теперь содержит верхний `sl`-блок с полями `title`, `description`, `congratulation`, `helper`, `extra.sequence_icon`, а затем локальные task-блоки `tasks.0`, `tasks.1`, `tasks.2`. Заголовки задач в CSV нумеруются внутри каждого квеста: второй квест снова начинается с `Таск 1`, даже если `task_number` во входном JSON глобальный.

Для диалоговых задач (`TT-001`/`Диалог`) в `filled_tasks.json` должно быть поле `dialogue_replica` на уровне task-записи. Валидатор проверяет, что реплика есть и не длиннее 360 символов с пробелами, а CSV exporter пишет ее в заголовочную строку таска: `;Таск 1;Диалог;;;РЕПЛИКА ДИАЛОГА: ...`.

## Заполнение первых task templates

Первый проход генератора task object поддерживает 5 базовых типов:

- `garbage classname in_guest`
- `garbage classname`
- `get_asset Collection`
- `get_asset GR in_guest garbage`
- `action take_crop_in_guest`

Положи результат этапа 3 в `data/stage3_quests.txt` или передай путь явно:

```bash
python src/fill_tasks.py --input data/stage3_quests.txt
```

Команда читает только quest-ready данные:

- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`
- `data/task_templates.json`

И создает:

- `output/generated_tasks.json` — промежуточный JSON task object
- `output/generated_quests.csv` — CSV в структуре рабочего примера

Если встречается неподдержанный `Task type`, он попадает в `issues` в `output/generated_tasks.json`. Такой task не заполняется автоматически.

## Тесты

```bash
python -m unittest discover -s tests
```

Тесты используют временные raw-данные и проверяют построение базовых индексов, quest-ready индексов, excluded entities, critical issues и non-critical issues.

## Ограничения текущего этапа

- Файлы в `raw/` не изменяются.
- Сгенерированные файлы пишутся только в `data/`.
- Полная творческая генерация квестов не реализована в коде и выполняется через ИИ по инструкциям этапов.
- CSV-экспорт реализован только для уже валидного `output/filled_tasks.json`.
- Используется только стандартная библиотека Python.
