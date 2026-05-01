# quest-data-builder

Проект собирает quest-ready индексы из legacy game data и помогает вести поэтапный workflow создания quest pack: от сюжета до CSV.

## Быстрый Старт

Пересобрать игровые индексы:

```bash
python src/build_index.py
```

Показать текущий рабочий контекст:

```bash
python src/workflow_context.py show
```

Запустить тесты:

```bash
python -m unittest discover -s tests
```

## Документы

- `AGENTS.md` - короткие обязательные правила для Codex.
- `README.md` - краткая карта проекта и команды.
- `workflows/WORKFLOW_GUIDE.md` - основной подробный workflow создания квестов.
- `workflows/POT_DESCRIPTION_WORKFLOW.md` - workflow описания горшков по картинке.
- `workflows/RESOURCE_TABLE_WORKFLOW.md` - workflow CSV-таблицы ресурсов для дева.
- `workflows/workflow_modes.json` - машинная карта режимов и ключевиков.
- `Инструкция этап 1.txt` ... `Инструкция этап 6.txt` - подробные playbook-и конкретных этапов.

`PLAN.md` удален: это был устаревший roadmap разработки, а не рабочая инструкция.

## Основные Папки

- `raw/` - исходные игровые данные, не редактировать.
- `data/` - generated indexes и quest-ready данные.
- `input/` - временный ручной ввод для текущего прогона.
- `output/` - временный рабочий прогон.
- `campaigns/` - постоянные campaign/pack артефакты.
- `workspace/` - локальный active context, не коммитится.
- `src/` - CLI и Python-код.
- `tests/` - unit tests.

Постоянным источником правды для quest pack является:

```text
campaigns/<campaign_id>/<pack_id>/
```

`output/` можно использовать как временную витрину, но не как место хранения актуального pack.

## Quest-Ready Индексы

`python src/build_index.py` читает:

- `raw/locations/`
- `raw/garbage/`
- `raw/flowers/`
- `raw/collections/`

И создает:

- `data/master_index.json`
- `data/garbage.index.json`
- `data/flowers.index.json`
- `data/collections.index.json`
- `data/drops.index.json`
- `data/validation_report.json`
- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`
- `data/critical_issues.json`
- `data/non_critical_issues.json`
- `data/excluded_entities.json`
- `data/validation_summary.md`

Генерация quest/task data должна использовать только:

```text
data/quest_ready_index.json
data/quest_ready_drops.index.json
```

## Campaign И Pack

Создать или открыть campaign:

```bash
python src/start_campaign.py MeatballRain_2026 --title "У нас дождь из фрикаделек" --tone "юмор" --characters "Дедушка Домовед,Баба яга,Царевна медной горы"
```

Создать следующий pack:

```bash
python src/create_pack.py MeatballRain_2026 --title "Пак 1"
```

Обновить память campaign по готовому pack:

```bash
python src/update_campaign_memory.py MeatballRain_2026 --pack pack_002
```

Если часть артефактов была сделана во временном `output/`, их можно скопировать в pack и обновить память:

```bash
python src/update_campaign_memory.py MeatballRain_2026 --pack pack_002 --from-output
```

## Workflow 1-6

Подробные правила и точки approval описаны в `workflows/WORKFLOW_GUIDE.md`. Краткая карта:

| Этап | Что Делает | Главный Результат | Approval |
| --- | --- | --- | --- |
| Перед 1 | Выбор интерактивных объектов | `interactive_objects.json` | не нужен, но нужен выбор пользователя |
| 1 | Сюжетная структура pack | `stage1_story.txt` | нужен |
| 2 | Реплики начала/завершения | `stage2_story.txt` | нужен |
| 3 | План квестов и task templates | `stage3_quests.txt`, `quest_plan*.json` | нужен |
| 3.1 | Context pack для ИИ | `context_pack.json` | не нужен |
| 4 | Task choices, filled task objects + validation | `task_choices.json`, `filled_tasks.json`, `filled_tasks.validation.json` | нужен |
| 5 | Quest group pack | `quest_group.json` | нужен |
| 6 | CSV export | `generated_quests.csv`, `generated_actions.csv`, `generated_interactive_objects_*.csv` | запускается только после approval stage 5 |

Технические gates:

```bash
python src/workflow_context.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_context.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
python src/workflow_context.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
```

## Основные Команды Этапов

Быстрый маршрут через wrapper. Если `workspace/active_context.json` уже содержит нужные `campaign_id` и `pack_id`, параметры `--campaign` и `--pack` можно не писать.

Перед этапом 1:

```bash
python src/workflow_fast.py interactive-objects --campaign <campaign_id> --select chest_1 --select help_1
```

Интерактивные объекты выбираются на всю campaign и сохраняются в `campaigns/<campaign_id>/interactive_objects.json`.
Перед Stage 1 Codex должен спросить минимум 2 объекта и короткую анкету по их сущности: как выглядит объект, какой ресурс дает, чем он тематически является. Если пользователь оставляет выбор за ИИ, Codex заполняет это по теме campaign.

Фиксирует выбранные интерактивные объекты pack в `interactive_objects.json`. Перед новым pack нужно выбрать минимум два объекта; `Chest_1_Home/Guest` и `HELP_1_Home/Guest` считаются одним объектом.

Этап 3:

```bash
python src/workflow_fast.py stage3 --campaign <campaign_id> --pack <pack_id>
```

Этап 3.1:

```bash
python src/workflow_fast.py context --campaign <campaign_id> --pack <pack_id>
```

Этап 4:

```bash
python src/workflow_fast.py fill --campaign <campaign_id> --pack <pack_id>
```

Этап 5:

```bash
python src/workflow_fast.py quest-group --campaign <campaign_id> --pack <pack_id>
```

Этап 6:

```bash
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
```

Stage 6 читает `filled_tasks.json` и `quest_group.json` из папки pack, пишет CSV и сразу обновляет `campaign_memory.json`:

```text
campaigns/<campaign_id>/<pack_id>/generated_quests.csv
campaigns/<campaign_id>/<pack_id>/generated_actions.csv
campaigns/<campaign_id>/<pack_id>/generated_actions.summary.json
campaigns/<campaign_id>/generated_interactive_objects_*.csv
campaigns/<campaign_id>/generated_interactive_objects.summary.json
```

`generated_actions.csv` содержит actions текущего pack, а нумерация диалогов и Give учитывает предыдущие pack-и campaign.

## Описание Горшков

Для режима описания горшков по картинке:

```bash
python src/workflow_context.py detect --text "опиши горшок по картинке" --apply
```

Правила workflow:

```text
workflows/POT_DESCRIPTION_WORKFLOW.md
```

Если результат сохранен в JSON:

```bash
python src/validate_pot_description.py output/pot_description.json
```

## Таблица Ресурсов

Для режима сборки CSV ресурсов по всей campaign:

```bash
python src/workflow_context.py detect --text "собери таблицу ресурсов для дева по всей компании" --apply
```

Правила workflow:

```text
workflows/RESOURCE_TABLE_WORKFLOW.md
```

Собрать таблицу:

```bash
python src/build_resource_table.py <campaign_id>
```

Шаблон блоков CSV:

```text
docs/resource_table_template.csv
```

По умолчанию таблица собирается из всех `campaigns/<campaign_id>/pack_*`. Сборка одного pack - только если это явно попросили.

## Жесткие Ограничения

- Не изменять `raw/`.
- Не выдумывать игровые факты.
- Новый pack делается поэтапно, с approval после каждого творческого этапа.
- `quest_group.json` хранится в папке конкретного pack.
- Generated-объекты (`HOG`, `GR`, `ASK`, `PER`, `CL`, `FA`, `R`) нумеруются в пределах всей campaign.
- `TT-035` помечен как `not_ready` и не должен использоваться.
- Используется только стандартная библиотека Python.
