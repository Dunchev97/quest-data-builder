# AGENTS.md

Короткие правила для Codex в этом проекте. Подробный пользовательский workflow живет в `workflows/WORKFLOW_GUIDE.md`, машинная карта режимов - в `workflows/workflow_modes.json`.

## Язык

- Всегда отвечать пользователю на русском.
- Не переводить code identifiers, JSON keys, CSV headers, classnames, paths и Python identifiers.

## Главные источники правды

- `workspace/active_context.json` - локальный, некоммитящийся контекст текущего пользователя: `mode`, `campaign_id`, `pack_id`, `stage`, `quest_number`, `task_number`.
- `campaigns/<campaign_id>/<pack_id>/` - постоянные артефакты конкретного pack.
- `data/quest_ready_index.json` и `data/quest_ready_drops.index.json` - единственные игровые индексы для генерации quest/task data.
- `raw/` - исходные игровые данные. Никогда не редактировать.
- `workflows/WORKFLOW_GUIDE.md` - порядок работы по этапам 1-6.
- `workflows/POT_DESCRIPTION_WORKFLOW.md` - workflow описания горшков по картинке.
- `workflows/RESOURCE_TABLE_WORKFLOW.md` - workflow CSV-таблицы ресурсов для дева.
- `workflows/workflow_modes.json` - ключевики и режимы для `workflow_context.py`.

## Локальная среда и скорость

- Не использовать `rg`: в этой среде `rg.exe` стабильно падает с `Access is denied`.
- Для поиска по файлам использовать PowerShell: `Get-ChildItem ... | Select-String ...`.
- Не тратить время на очистку `__pycache__/` и `*.pyc` после каждого запуска скриптов или тестов.
- `__pycache__/` и `*.pyc` не являются контентными артефактами; их не коммитить и чистить только перед commit/release или по явной просьбе пользователя.

## Active Context

Если пользователь спрашивает про текущую сессию, campaign, pack, stage, quest, task, выбранные шаблоны, текущий CSV, `quest_group` или текущий режим описания горшков, сначала читать:

```bash
python src/workflow_context.py show
```

или сам файл:

```text
workspace/active_context.json
```

Не отвечать по памяти, если вопрос зависит от текущего контекста.

`workspace/active_context.json` не коммитить: у каждого участника команды он свой локальный.

## Quest Workflow

Рабочий workflow создания pack утвержден пользователем и состоит из этапов 1-6:

1. Сюжетная структура pack.
2. Реплики начала/завершения.
3. План квестов и task templates.
3.1. Context pack для заполнения task objects.
4. Заполненные task objects и validation.
5. Quest group для pack.
6. CSV export.

Правила:

- Выполнять только один этап за раз.
- После каждого творческого этапа показывать результат пользователю и ждать явный approval.
- Stage 3.1 нельзя собирать до approval stage 3.
- Stage 5 нельзя собирать до approval stage 4.
- Stage 6 нельзя запускать до approval stage 5.
- Approval записывать через `src/workflow_context.py approve`.

## Pot Description Workflow

Если пользователь прислал изображение и просит описать горшок, короб или грибницу:

- переключить режим на `pot_description` через `src/workflow_context.py detect --text "<запрос>" --apply` или вручную через `set`;
- читать правила из `workflows/POT_DESCRIPTION_WORKFLOW.md`;
- спросить вид горшка, если пользователь не указал: `Обычный`, `Волшебный`, `Короб для овощей`, `Грибница для грибов`;
- описывать только видимое на изображении плюс мягкую стилизацию;
- не выдумывать бонусы, проценты, ускорение роста, валюту или игровые свойства;
- финальный текст должен заканчиваться правильным постфиксом по виду горшка;
- при сохранении JSON проверять результат командой `python src/validate_pot_description.py output/pot_description.json`.

## Resource Table Workflow

Если пользователь просит собрать таблицу ресурсов, `*_Res.csv` или CSV ресурсов для дева:

- переключить режим на `resource_table` через `src/workflow_context.py detect --text "<запрос>" --apply` или вручную через `set`;
- читать правила из `workflows/RESOURCE_TABLE_WORKFLOW.md`;
- использовать `docs/resource_table_template.csv` как эталон блоков и заголовков;
- собирать таблицу командой `python src/build_resource_table.py <campaign_id>`;
- по умолчанию читать все pack из `campaigns/<campaign_id>/pack_*`;
- один pack использовать только если пользователь явно попросил фильтр по pack;
- создавать только блоки, для которых есть ресурсы в выбранной campaign или явно выбранных pack;
- сохранять минимум одну пустую строку между блоками;
- не использовать `Fun12`, если текущий prefix другой.

## Где Хранить Артефакты

- `output/` - локальный временный рабочий прогон, не источник правды для campaign и не место для коммита.
- `campaigns/<campaign_id>/<pack_id>/` - постоянное место для файлов pack.
- Для quest workflow все постоянные артефакты этапов 1-6 хранить в `campaigns/<campaign_id>/<pack_id>/`, включая `quest_plan.json`, `quest_plan.resolved.json` и `context_pack.json`.
- `quest_group.json` всегда хранить в папке pack:

```text
campaigns/<campaign_id>/<pack_id>/quest_group.json
```

Stage 6 должен брать `filled_tasks.json` и `quest_group.json` из папки pack и писать:

```text
campaigns/<campaign_id>/<pack_id>/generated_quests.csv
```

## Роли ИИ И Кода

- ИИ отвечает за творческие решения: сюжет, реплики, выбор task types, заполнение task objects по контексту, тексты quest group.
- Код отвечает за guardrails: parsing, context pack, validation, approval gates, CSV export, campaign memory.
- Не выдумывать игровые факты. Classname, title, location, collection, garbage, flower и связи должны приходить из parsed/generated/quest-ready data.
- Для задач `in_guest` нельзя предлагать мусор, локации, `collection_drop` или `gr_garbage`, привязанные к локациям с тегом `world`; такие кандидаты допустимы только для домашних задач.

## Проверки

Перед финальным ответом после изменений запускать релевантные тесты. Для широких изменений:

```bash
python -m unittest discover -s tests
```

Не коммитить `__pycache__`/`*.pyc`.
