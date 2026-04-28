# quest-data-builder

Парсер raw-данных легаси-игры для построения игровых индексов, quest-ready данных и рабочих файлов квестового пайплайна.

Код индексирует реальные игровые данные, проверяет их и помогает вести этапы 3-5. Полная творческая генерация квестов остается ручным/ИИ-этапом: код не должен сам придумывать сюжет или task object без отдельного указания.

## Быстрый старт

Пересобрать игровые индексы:

```bash
python src/build_index.py
```

Запустить тесты:

```bash
python -m unittest discover -s tests
```

Файлы в `raw/` не изменяются.

## Активный контекст

Актуальная рабочая сессия хранится здесь:

```text
workspace/active_context.json
```

Если пользователь спрашивает про текущую сессию, campaign, pack, stage, quest, task или выбранные шаблоны, сначала смотри этот файл.

Показать активный контекст:

```bash
python src/workflow_context.py show
```

Выставить контекст вручную:

```bash
python src/workflow_context.py set --mode quest_edit --campaign MeatballRain_2026 --pack pack_001 --stage 4 --quest 2 --task 1
```

Определить режим по тексту запроса и записать его:

```bash
python src/workflow_context.py detect --text "создай csv для текущего пака" --apply --campaign MeatballRain_2026 --pack pack_001
```

Подробный порядок workflow, режимы и approval gates описаны в:

- `workflows/WORKFLOW_GUIDE.md`
- `workflows/workflow_modes.json`

## Основные папки

- `raw/` — исходные игровые данные, не редактировать.
- `data/` — generated indexes и quest-ready данные.
- `input/` — ручной ввод для текущего прогона.
- `output/` — последний рабочий прогон.
- `campaigns/` — сохраненные campaign/pack артефакты.
- `workspace/` — активный контекст локальной сессии.
- `src/` — CLI и Python-код.
- `tests/` — unit-тесты.

## Индексы

`python src/build_index.py` читает:

- `raw/locations/`
- `raw/garbage/`
- `raw/flowers/`
- `raw/collections/`

И создает базовые файлы:

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

`quest_ready_index.json` и `quest_ready_drops.index.json` — единственные индексы, которые будущая генерация квестов и CSV должна использовать как источник игровых данных.

Если нужно пересобрать только Markdown summary из уже созданных JSON:

```bash
python src/analyze_validation.py
```

## Квестовый пайплайн

Этап 3: распарсить текстовый план квестов:

```bash
python src/parse_stage3.py input/stage3_quests.txt
```

Проверить выбранные `Task template ID`, русские названия и `Task type`:

```bash
python src/task_type_resolver.py output/quest_plan.json
```

После показа результата этапа 3 и явного апрува пользователя записать approval gate:

```bash
python src/workflow_context.py approve --stage 3 --campaign MeatballRain_2026 --pack pack_002
```

Применить ручные overrides, если нужны:

```bash
python src/apply_overrides.py output/quest_plan.json input/manual_overrides.json
```

Этап 3.1: собрать compact context pack для заполнения task objects:

```bash
python src/build_context_pack.py output/quest_plan.resolved.json --campaign MeatballRain_2026 --current-pack pack_002
```

`build_context_pack.py` не собирает `context_pack` без записанного approval stage 3 для того же `campaign_id/pack_id`.

Этап 4: проверить заполненный `output/filled_tasks.json`:

```bash
python src/validate_task_objects.py output/filled_tasks.json --campaign MeatballRain_2026 --current-pack pack_002
```

После показа результата этапа 4 и явного апрува пользователя записать gate:

```bash
python src/workflow_context.py approve --stage 4 --campaign MeatballRain_2026 --pack pack_002
```

Этап 5: создать квестовую группу по контексту всего pack:

```bash
python src/build_quest_group.py --campaign MeatballRain_2026 --current-pack pack_002 --title "..." --description "..." --description-complete "..." --description-spoil "..."
```

Поля `title`, `description`, `description_complete`, `description_spoil` пишет ИИ по смыслу всех квестов pack. `quest_group.json`, validation и preview сохраняются в `campaigns/<campaign_id>/<pack_id>/`, потому что квестовая группа привязана к pack. После показа `campaigns/<campaign_id>/<pack_id>/quest_group.json` и preview нужен явный апрув пользователя:

```bash
python src/workflow_context.py approve --stage 5 --campaign MeatballRain_2026 --pack pack_002
```

Этап 6: экспортировать CSV после approval stage 5:

```bash
python src/export_csv.py --campaign MeatballRain_2026 --current-pack pack_002
```

CSV не создается, если `campaigns/<campaign_id>/<pack_id>/filled_tasks.validation.json` или `campaigns/<campaign_id>/<pack_id>/quest_group.validation.json` содержит errors, устарел относительно входных JSON, либо approval stage 5 не записан.

## Кампании и паки

`output/` — последний рабочий прогон. Долгая сюжетная линия хранится в `campaigns/`.

Создать или открыть campaign:

```bash
python src/start_campaign.py MeatballRain_2026 --title "У нас дождь из фрикаделек" --tone "юмор" --characters "Дедушка Домовед,Баба яга,Царевна медной горы"
```

Создать следующий pack:

```bash
python src/create_pack.py MeatballRain_2026 --title "Пак 1"
```

Если этапы 3-4 делались во временном `output/`, сохранить текущий `output/` в campaign и обновить память:

```bash
python src/update_campaign_memory.py MeatballRain_2026 --pack pack_001 --from-output
```

Generated-объекты (`HOG`, `GR`, `ASK`, `PER`, `CL`, `FA`, `R`) нумеруются в пределах всей campaign, а не отдельного pack.

## Ограничения

- Не изменять `raw/`.
- Не придумывать игровые факты: classname, title, tags и связи берутся из parsed/generated data.
- Новый pack делается поэтапно и требует approval после каждого этапа.
- CSV создается только из валидного `output/filled_tasks.json`.
- `quest_group.json` хранится в папке конкретного pack: `campaigns/<campaign_id>/<pack_id>/quest_group.json`.
- `TT-035` помечен как `not_ready` и не должен использоваться.
- Используется только стандартная библиотека Python.
