# Workflow Guide

Единая подробная памятка по рабочему процессу создания quest pack.

## Карта Документов

- `AGENTS.md` - короткие обязательные правила для Codex.
- `README.md` - краткая карта проекта и команды.
- `workflows/WORKFLOW_GUIDE.md` - подробный workflow 1-6.
- `workflows/POT_DESCRIPTION_WORKFLOW.md` - workflow описания горшков по изображению.
- `workflows/RESOURCE_TABLE_WORKFLOW.md` - workflow CSV-таблицы ресурсов для дева.
- `workflows/workflow_modes.json` - машинная карта режимов, ключевиков и entrypoints.
- `data/interactive_object_templates.json` - поддержанные шаблоны интерактивных объектов.
- `Инструкция этап 1.txt` ... `Инструкция этап 6.txt` - подробные playbook-и этапов.
- `campaigns/<campaign_id>/campaign_tone.md` - тон campaign, стиль юмора, запреты на абсурдные формулировки и тематический словарь.

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

При старте новой campaign Codex сам придумывает `campaign_id` по теме пользователя. При старте нового pack Codex сам берет следующий `pack_id` по порядку из campaign metadata, начиная с `pack_001`; не нужно задавать пользователю отдельные вопросы про эти id.

```bash
python src/workflow_fast.py status --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py interactive-objects --campaign <campaign_id> --pack <pack_id> --select chest_1 --select help_1
python src/workflow_fast.py stage3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py context --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py fill --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py quest-group --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
```

`stage6` также автоматически пересобирает campaign-level таблицу ресурсов. Команда `resource-table` остается только как ручной fallback для отдельной пересборки/отладки, но в обычном workflow после Stage 6 ее запускать не нужно.

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
quest_group_choices.json
quest_group.validation.json
quest_group.preview.md
generated_quests.csv
generated_actions.csv
generated_actions.summary.json
```

Campaign-level files:

```text
campaigns/<campaign_id>/interactive_objects.json
campaigns/<campaign_id>/interactive_objects.preview.md
campaigns/<campaign_id>/generated_interactive_objects_*.csv
campaigns/<campaign_id>/generated_interactive_objects.summary.json
campaigns/<campaign_id>/resource_table.csv
campaigns/<campaign_id>/resource_table.summary.json
```

`output/` - локальная временная витрина. Нельзя считать файлы из `output/` актуальными для campaign, если эти файлы не перенесены в папку pack. Для основного quest workflow предпочитай сразу писать постоянные артефакты в `campaigns/<campaign_id>/<pack_id>/`.

## Роли ИИ И Кода

ИИ делает творческие решения:

- пишет этапы 1-2;
- перед Stage 1 новой campaign спрашивает, какие минимум 2 интерактивных объекта нужны на всю campaign, уточняет их сущность и фиксирует выбор в `campaigns/<campaign_id>/interactive_objects.json`;
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
- экспортирует CSV интерактивных объектов по `data/interactive_object_templates.json`;
- экспортирует actions CSV для персонажей, Give и HOG search;
- экспортирует campaign-level `resource_table.csv` по всем pack текущей campaign как обязательную часть Stage 6;
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

### Перед Stage 1 - Интерактивные Объекты

Перед началом новой campaign Codex должен спросить пользователя, какие 2 или больше интерактивных объекта выбрать на всю campaign. Меньше двух в базовом сценарии выбирать нельзя. `Chest_*_Home/Guest` и `HELP_*_Home/Guest` считаются одним объектом. Сейчас поддержаны:

- `exchanger` - Exchanger / обмен ресурсами с друзьями; источник ресурсов может быть `generator` или `gr`.
- `chest_1` - парный `Chest_1_Home` + `Chest_1_Guest`; пара считается одним интерактивным объектом.
- `help_1` - парный `HELP_1_Home` + `HELP_1_Guest`; пара считается одним интерактивным объектом.
- `friend_action_1` - `Story_FriendAction_1`: действие у друзей с шансом, дневным лимитом, флагом доступности и двумя `FA`-ресурсами (`reward_for_action`, `reward_on_receive`).

Выбор фиксировать в:

```text
campaigns/<campaign_id>/interactive_objects.json
```

Быстрая команда для первичной фиксации выбранных шаблонов:

```bash
python src/workflow_fast.py interactive-objects --campaign <campaign_id> --select chest_1 --select help_1
```

Перед Stage 1 Codex задает короткую анкету: какие механики выбрать, как должен выглядеть каждый объект, какой ресурс он дает, какой ресурс нужен для активации/обмена, и что делать, если пользователь хочет оставить детали на ИИ. Если пользователь оставляет выбор за ИИ, названия и сущности заполняются по общей теме campaign.

Если пользователь выбирает несколько объектов одной механики, они нумеруются последовательно: `Chest_1`, `Chest_2`, `HELP_1`, `HELP_2`, `Exchanger_1`, `Exchanger_2`, `Story_FriendAction_1`, `Story_FriendAction_2`. Если механика выбрана один раз, используется обычное имя из шаблона. Ресурсы выбранных объектов не меняются от pack к pack внутри campaign.

Result resources выбранных объектов используются как 3-й и 4-й ингредиенты craft recipe в таблице ресурсов. Для `Chest`, `HELP`, `Exchanger` это ресурсы с суффиксом `_R_`; для `friend_action_1` по умолчанию это `Story_FA_2` (`reward_on_receive`). При 3+ объектах ингредиенты идут по кругу: 1-й craft берет объекты 1+2, 2-й craft берет 3+4, если 4-го нет - 3+1, дальше продолжается тот же круг.

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

Жёсткая связь с Stage 2:

- `description` в Stage 3 всегда дословно берётся из `Старт:` соответствующего квеста в `stage2_story.txt`;
- `congratulation` в Stage 3 всегда дословно берётся из `Завершение:` соответствующего квеста в `stage2_story.txt`;
- Stage 3 выбирает механики по смыслу этих текстов, но не переписывает их.
- `TT-008` (`get_asset ASK`) и `TT-009` (`get_asset PER`) использовать только в квестах, где в этой же тройке task есть `TT-002` (`get_and_decrease_asset craft`) или `TT-033` (`action give`). Если квест не крафтовый и не содержит передачу предмета, выбирать другие механики вместо ASK/PER.
- `TT-010` (`Получить CL / награда за коллекцию`) не использовать, пока нет достоверного списка collection rewards. Вместо него выбирать обычные collection/drop templates, например `TT-011`, `TT-026` или `TT-028`, если они подходят по смыслу.
- Любой HOG template (`TT-003`, `TT-004`, `TT-005`, `TT-006`, `TT-007`) нельзя ставить в квест, если в предыдущем квесте уже был HOG в любом task.
- В крафтовых квестах чередовать `ASK` и `PER`: если предыдущий крафтовый квест использовал `ASK`, следующий крафтовый использует `PER`, и наоборот.
- Загадки в Stage 4 сохранять одной строкой без переносов строк.
- Для русских `title` и `hint` использовать падежные формы: персонажи после `с` в творительном падеже, предмет после `Найди/Получи/Создай/получить` в винительном, объект после `в` в винительном, мусор в игровых заданиях в форме, которая читается естественно для множественного сбора.

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

Сводку Stage 3 пользователю показывать по квестам с ID и русским названием шаблона одновременно:

```text
1. Название квеста: TT-001 Диалог / TT-008 Получить ASK / TT-004 HOG на локации
```

Stage 3 артефакты должны оставаться в папке pack, чтобы параллельные сессии не делили общий `output/`.

Перед творческими этапами проверять `campaigns/<campaign_id>/campaign_tone.md`. Если файла нет, уточнить тон у пользователя. ИИ может написать тон сам только если пользователь явно разрешил придумать его.

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

`amount` и `price` ИИ не подбирает вручную: `build_filled_tasks.py` берет средние значения из `data/task_templates.json`, которые перенесены из `Шаблоны тасков.csv`. Ручной override в `task_choices.json` допустим только если нужно сознательно отойти от среднего значения.

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

Цель: ИИ анализирует все квесты pack и пишет тексты quest group, а код собирает общий блок quest group для страницы журнала. `quest_group_choices.json` можно сохранить для истории и повторяемости, но быстрый wrapper также принимает тексты через CLI-параметры.

Быстрая команда:

```bash
python src/workflow_fast.py quest-group --campaign <campaign_id> --pack <pack_id>
```

Выход:

```text
campaigns/<campaign_id>/<pack_id>/quest_group.json
campaigns/<campaign_id>/<pack_id>/quest_group_choices.json
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

Цель: технически развернуть утвержденные `quest_group.json` и `filled_tasks.json` в CSV, собрать отдельный CSV персонажей и quest actions, выгрузить CSV выбранных интерактивных объектов и обязательно пересобрать campaign-level таблицу ресурсов по всем pack текущей campaign.

Быстрая команда:

```bash
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
```

Stage 6 работает инкрементально: если `resource_table.csv` / `resource_table.summary.json` свежее всех `filled_tasks.json`, `context_pack.json` и `interactive_objects.json` campaign, таблица ресурсов не пересобирается. Interactive-object CSV тоже пропускаются, если они свежее `interactive_objects.json`. Для ручной полной пересборки используй отдельные fallback-команды `resource-table` и `interactive-objects --export`.

Stage 6 читает из:

```text
campaigns/<campaign_id>/<pack_id>/filled_tasks.json
campaigns/<campaign_id>/<pack_id>/filled_tasks.validation.json
campaigns/<campaign_id>/<pack_id>/quest_group.json
campaigns/<campaign_id>/<pack_id>/quest_group.validation.json
campaigns/<campaign_id>/interactive_objects.json
```

И пишет:

```text
campaigns/<campaign_id>/<pack_id>/generated_quests.csv
campaigns/<campaign_id>/<pack_id>/generated_actions.csv
campaigns/<campaign_id>/<pack_id>/generated_actions.summary.json
campaigns/<campaign_id>/generated_interactive_objects_*.csv
campaigns/<campaign_id>/generated_interactive_objects.summary.json
campaigns/<campaign_id>/resource_table.csv
campaigns/<campaign_id>/resource_table.summary.json
```

`generated_actions.csv` содержит только actions текущего pack. Для нумерации `Dialog_N` и `Give_N` код просматривает предыдущие pack-и campaign, чтобы не создавать дубли. Персонажи, которые используются квестами как helper, но не имеют экшенов в текущем pack, все равно пишутся в этот же CSV отдельным блоком `ПЕРСОНАЖИ БЕЗ ЭКШЕНОВ` без колонки/параметра `behaviour.0.actions`.

`resource_table.csv` на Stage 6 не является отдельным ручным шагом: `workflow_fast.py stage6` собирает его вместе с остальными CSV на уровне `campaigns/<campaign_id>/`, читая все `campaigns/<campaign_id>/pack_*` и используя структуру из `docs/resource_table_template.csv` / `workflows/RESOURCE_TABLE_WORKFLOW.md`.

CSV не создается, если:

- approval stage 5 отсутствует;
- validation stage 4 содержит errors;
- validation stage 5 содержит errors;
- `interactive_objects.json` есть и заполнен, но в нем неизвестный template id или противоречивые данные. Пустой файл выбора не должен жестко блокировать нестандартные сценарии;
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

Для текущего pack нумерация считается только по предыдущим pack-ам campaign. Более поздние pack-и не должны влиять на validation или context pack раннего pack-а.

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
- в обычном quest workflow таблицу ресурсов собирает `python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>` вместе с остальными CSV; отдельная команда `python src/workflow_fast.py resource-table --campaign <campaign_id>` нужна только для ручной пересборки/отладки;
- даже при ручном фильтре по pack сохранять итоговый файл на уровне campaign, если пользователь явно не указал другой `--output-csv`;
- создавать только блоки ресурсов, которые реально есть;
- для recipe craft брать 1-й и 2-й ингредиенты из соседних resource tasks, а 3-й и 4-й - из выбранных интерактивных `_R_` ресурсов campaign по кругу: 1-й craft = объекты 1+2, 2-й craft = 3+4, если 4-го нет = 3+1;
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
