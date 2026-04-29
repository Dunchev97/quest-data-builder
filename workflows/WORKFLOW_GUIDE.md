# Workflow Guide

Единая подробная памятка по рабочему процессу создания quest pack.

## Карта Документов

- `AGENTS.md` - короткие обязательные правила для Codex.
- `README.md` - краткая карта проекта и команды.
- `workflows/WORKFLOW_GUIDE.md` - подробный workflow 1-6.
- `workflows/POT_DESCRIPTION_WORKFLOW.md` - workflow описания горшков по изображению.
- `workflows/RESOURCE_TABLE_WORKFLOW.md` - workflow CSV-таблицы ресурсов для дева.
- `workflows/workflow_modes.json` - машинная карта режимов, ключевиков и entrypoints.
- `Инструкция этап 1.txt` ... `Инструкция этап 6.txt` - подробные playbook-и этапов.

## Active Context

Текущий контекст всегда брать из локального файла:

```text
workspace/active_context.json
```

Этот файл не коммитится. У каждого участника команды он свой, поэтому локальные сессии не сбивают друг друга через git.

Если пользователь спрашивает про текущий campaign, pack, stage, quest, task, выбранные шаблоны, `context_pack`, `filled_tasks`, `quest_group` или CSV:

1. Сначала читать `workspace/active_context.json`.
2. Взять `campaign_id`, `pack_id`, `stage`, `quest_number`, `task_number`.
3. Искать постоянные артефакты в `campaigns/<campaign_id>/<pack_id>/`.
4. Смотреть `output/` только как fallback для текущего временного прогона.
5. Если active context неполный, сказать это явно.

Если пользователь прикрепил картинку и просит описать горшок, переключить режим на `pot_description`:

```bash
python src/workflow_context.py detect --text "<запрос пользователя>" --apply
```

Показать контекст:

```bash
python src/workflow_context.py show
```

Выставить контекст:

```bash
python src/workflow_context.py set --mode quest_generation --campaign <campaign_id> --pack <pack_id> --stage <stage>
```

Записать approval:

```bash
python src/workflow_context.py approve --stage <stage> --campaign <campaign_id> --pack <pack_id>
```

Быстрый вариант approval:

```bash
python src/workflow_fast.py approve --stage <stage> --campaign <campaign_id> --pack <pack_id>
```

## Быстрый Маршрут

Для рутинной работы использовать `src/workflow_fast.py`: он берет стандартные pack-пути, читает `active_context` при отсутствии `--campaign/--pack` и не заставляет вручную перечислять одинаковые аргументы.

```bash
python src/workflow_fast.py status --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py stage3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py context --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py fill --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py quest-group --campaign <campaign_id> --pack <pack_id> --title "..." --description "..." --description-complete "..." --description-spoil "..."
python src/workflow_fast.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py resource-table --campaign <campaign_id>
```

Старые низкоуровневые команды остаются fallback для отладки, но в обычном workflow их не нужно набирать вручную.

## Где Лежат Артефакты

Постоянное место pack:

```text
campaigns/<campaign_id>/<pack_id>/
```

Типовые файлы pack:

```text
pack.json
stage1_story.txt
stage2_story.txt
stage3_quests.txt
quest_plan.json
quest_plan.resolved.json
context_pack.json
context_pack.preview.md
task_choices.json
filled_tasks.build.json
filled_tasks.json
filled_tasks.validation.json
filled_tasks.preview.md
quest_group.json
quest_group.validation.json
quest_group.preview.md
generated_quests.csv
```

`output/` - локальная временная витрина. Нельзя считать файлы из `output/` актуальными для campaign, если эти файлы не перенесены в папку pack. Для основного quest workflow предпочитай сразу писать постоянные артефакты в `campaigns/<campaign_id>/<pack_id>/`.

## Роли ИИ И Кода

ИИ делает творческие решения:

- пишет этапы 1-2;
- выбирает task types на этапе 3;
- заполняет смысловые `task_choices` на этапе 4 по `context_pack`;
- пишет тексты `quest_group` на этапе 5.
- пишет названия и описания горшков по изображению в режиме `pot_description`.

Код делает guardrails:

- парсит stage 3;
- готовит context pack;
- собирает strict `filled_tasks.json` из `task_choices.json`;
- валидирует task objects;
- валидирует quest group;
- проверяет approval gates;
- экспортирует CSV;
- обновляет campaign memory.
- валидирует JSON результата pot description, если результат сохраняется.

Игровые факты нельзя выдумывать. Classname, title, location, collection, garbage, flower и связи должны приходить из parsed/generated/quest-ready data.

## Approval Gates

Codex выполняет один этап за раз и останавливается после результата.

Обязательные gates:

- После stage 1: показать сюжетную структуру, ждать approval.
- После stage 2: показать реплики начала/завершения, ждать approval.
- После stage 3: показать quest plan и выбранные task templates, ждать approval.
- После approval stage 3: записать gate; stage 3.1 можно запускать как техническую подготовку перед stage 4.
- После stage 3.1: отдельный approval не нужен, но перед stage 4 важно просмотреть context pack/кандидатов.
- После stage 4: показать task choices, filled tasks и validation, ждать approval.
- После approval stage 4: записать gate, только потом stage 5.
- После stage 5: показать quest group, ждать approval.
- После approval stage 5: записать gate, только потом stage 6.

Технические gates:

```bash
python src/workflow_context.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_context.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
python src/workflow_context.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
```

Скрипты должны отказываться работать, если gate отсутствует:

- `build_context_pack.py` по умолчанию не требует approval stage 3; старый строгий режим доступен через `--require-stage3-approval`.
- `build_quest_group.py` требует approval stage 4.
- `export_csv.py` требует approval stage 5.

## Workflow 1-6

### Stage 1 - Сюжетная Структура

Цель: создать основу pack: тема, конфликт, герои, ход серии.

Выход:

```text
campaigns/<campaign_id>/<pack_id>/stage1_story.txt
```

После показа результата нужен approval пользователя.

### Stage 2 - Реплики

Цель: подготовить начало и завершение квестов, сохранить тон campaign.

Выход:

```text
campaigns/<campaign_id>/<pack_id>/stage2_story.txt
```

После показа результата нужен approval пользователя.

### Stage 3 - План Квестов И Task Templates

Цель: получить `stage3_quests.txt`, распарсить его и сопоставить task types с template ids.

Быстрая команда:

```bash
python src/workflow_fast.py stage3 --campaign <campaign_id> --pack <pack_id>
```

Основные выходы:

```text
campaigns/<campaign_id>/<pack_id>/quest_plan.json
campaigns/<campaign_id>/<pack_id>/quest_plan.preview.md
campaigns/<campaign_id>/<pack_id>/quest_plan.resolved.json
campaigns/<campaign_id>/<pack_id>/quest_plan.resolved.preview.md
```

После проверки пользователем записать:

```bash
python src/workflow_fast.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
```

Stage 3 артефакты должны оставаться в папке pack, чтобы параллельные сессии не делили общий `output/`.

### Stage 3.1 - Context Pack

Цель: собрать компактный набор quest-ready кандидатов для ИИ, не выбирая финальные игровые данные вместо него.

Быстрая команда:

```bash
python src/workflow_fast.py context --campaign <campaign_id> --pack <pack_id>
```

Выход:

```text
campaigns/<campaign_id>/<pack_id>/context_candidate_history.json
campaigns/<campaign_id>/<pack_id>/context_pack.json
campaigns/<campaign_id>/<pack_id>/context_pack.preview.md
```

`build_context_pack.py` запускается без отдельного approval stage 3. Это техническая подготовка перед stage 4; процессный approval stage 3 всё равно нужен перед переходом к творческому заполнению.

### Stage 4 - Task Choices And Filled Tasks

Цель: ИИ заполняет смысловые `task_choices.json` по `context_pack`, а код собирает strict `filled_tasks.json` и проверяет результат.

Постоянные файлы stage 4 должны лежать в pack:

```text
campaigns/<campaign_id>/<pack_id>/task_choices.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.build.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.validation.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.preview.md
```

Сборка и validation:

```bash
python src/workflow_fast.py fill --campaign <campaign_id> --pack <pack_id>
```

Нужно показать пользователю `task_choices`, собранные `filled_tasks` и validation summary. После approval записать:

```bash
python src/workflow_fast.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
```

### Stage 5 - Quest Group

Цель: ИИ анализирует все квесты pack и пишет общий блок quest group для страницы журнала.

Быстрая команда:

```bash
python src/workflow_fast.py quest-group --campaign <campaign_id> --pack <pack_id> --title "..." --description "..." --description-complete "..." --description-spoil "..."
```

Выход:

```text
campaigns/<campaign_id>/<pack_id>/quest_group.json
campaigns/<campaign_id>/<pack_id>/quest_group.validation.json
campaigns/<campaign_id>/<pack_id>/quest_group.preview.md
```

Важно:

- `quest_group.json` привязан к pack, а не к `output/`.
- `input` всегда `/quest_group/fun/Fun13_Story_1.proto.js`.
- `output` строится как `/quest_group/fun/<campaign_id>_<pack_id>.proto.js`.
- `extra.quest_reward_prewiew` содержит три пустые строки.
- `description_condition` совпадает с `description`.
- `extra.description_complete` совпадает с `description_complete`.

После approval пользователя записать:

```bash
python src/workflow_context.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
```

### Stage 6 - CSV Export

Цель: технически развернуть утвержденные `quest_group.json` и `filled_tasks.json` в CSV.

Быстрая команда:

```bash
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
```

Stage 6 читает из:

```text
campaigns/<campaign_id>/<pack_id>/filled_tasks.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.validation.json
campaigns/<campaign_id>/<pack_id>/quest_group.json
campaigns/<campaign_id>/<pack_id>/quest_group.validation.json
```

И пишет:

```text
campaigns/<campaign_id>/<pack_id>/generated_quests.csv
```

CSV не создается, если:

- approval stage 5 отсутствует;
- validation stage 4 содержит errors;
- validation stage 5 содержит errors;
- validation-файл устарел относительно входного JSON.

`workflow_fast.py stage6` после успешного CSV сам обновляет campaign memory. Если использовался низкоуровневый `export_csv.py`, обновить память отдельно:

```bash
python src/update_campaign_memory.py <campaign_id> --pack <pack_id>
```

## Campaign Memory

`campaign_memory.json` нужен, чтобы следующий pack не начинал generated numbering заново и не повторял игровые сущности без необходимости.

Generated-объекты нумеруются в пределах campaign:

```text
<campaign_id>_HOG_1
<campaign_id>_GR_1
<campaign_id>_ASK_1
<campaign_id>_R_1
```

Если `pack_001` уже использовал `MeatballRain_2026_HOG_1`, следующий pack продолжает с `HOG_2`.

## Pot Description

Отдельный workflow для описания горшков описан в:

```text
workflows/POT_DESCRIPTION_WORKFLOW.md
```

Включается, когда пользователь присылает изображение и просит описать горшок, короб, мини/подвесной горшок или грибницу.

Поддержанные виды:

- `Обычный`;
- `Волшебный`;
- `Короб для овощей`;
- `Грибница для грибов`.

`Подвесной` и `мини` считаются обычными для выбора постфикса.

Проверка JSON-результата:

```bash
python src/validate_pot_description.py output/pot_description.json
```

## Resource Table

Отдельный workflow для CSV-таблицы ресурсов описан в:

```text
workflows/RESOURCE_TABLE_WORKFLOW.md
```

Шаблон блоков:

```text
docs/resource_table_template.csv
```

Включается, когда пользователь просит собрать `*_Res.csv`, таблицу ресурсов campaign или CSV ресурсов для дева.

Основные правила:

- по умолчанию читать все pack-артефакты из `campaigns/<campaign_id>/pack_*`;
- писать CSV для всей campaign в `campaigns/<campaign_id>/resource_table.csv`;
- собирать быстрой командой `python src/workflow_fast.py resource-table --campaign <campaign_id>` или низкоуровневой командой `python src/build_resource_table.py <campaign_id>`;
- писать CSV для одного pack в `campaigns/<campaign_id>/<pack_id>/resource_table.csv` только если пользователь явно попросил фильтр по pack;
- создавать только блоки ресурсов, которые реально есть;
- отделять блоки минимум одной пустой строкой;
- не копировать prefix из примера `Fun12`, использовать текущий generated prefix.

## Проверки И Скорость

- Для обычного content workflow запускать только validator текущего этапа: `workflow_fast.py context`, `workflow_fast.py validate`, `workflow_fast.py stage6` уже делают нужные проверки.
- Полный `python -m unittest discover -s tests` нужен после изменений Python-кода, шаблонов, `workflow_modes.json` или инструкций.
- Не чистить `__pycache__/` после каждого теста: папка ignored и не является рабочим артефактом.
- Не запускать `rg`: локально он падает с `Access is denied`; для поиска использовать PowerShell `Get-ChildItem ... | Select-String ...`.
- Не гонять `git status` после каждой команды; достаточно начала/конца работы и момента перед commit/stage.

## Режимы

Машинный список режимов находится в:

```text
workflows/workflow_modes.json
```

Посмотреть режимы:

```bash
python src/workflow_context.py list-modes
```

Главные режимы:

- `quest_generation` - создание нового pack по этапам.
- `quest_edit` - правка конкретного quest/task.
- `quest_group_creation` - stage 5.
- `csv_export` - stage 6.
- `campaign_management` - campaign/pack/memory.
- `validation_review` - разбор ошибок.
- `raw_indexing` - пересборка индексов.
- `pot_description` - описание горшков по изображению.
- `resource_table` - CSV-таблица ресурсов для дева.
- `workflow_management` - правка workflow docs.

## Что Можно Чистить

Безопасно удалять:

- `__pycache__/`
- `*.pyc`
- `workspace/active_context.json`, если нужно сбросить локальную сессию; файл будет создан заново командами workflow context
- временные файлы в `output/`, если нужные артефакты уже сохранены в `campaigns/<campaign_id>/<pack_id>/`
- старые временные файлы в `input/`, если их содержимое уже перенесено в pack

Не удалять:

- `AGENTS.md`
- `README.md`
- `workflows/WORKFLOW_GUIDE.md`
- `workflows/POT_DESCRIPTION_WORKFLOW.md`
- `workflows/RESOURCE_TABLE_WORKFLOW.md`
- `workflows/workflow_modes.json`
- `Инструкция этап 1.txt` ... `Инструкция этап 6.txt`
- `campaigns/`
- `data/quest_ready_index.json`
- `data/quest_ready_drops.index.json`
- `raw/`
