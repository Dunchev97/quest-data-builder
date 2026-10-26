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
- `docs/QUEST_INTERACTIVE_OBJECT_TEMPLATES.md` - понятные правила заполнения quest interactive objects, включая `mixer_1`.
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

Записать approval можно только через review-aware wrapper:

```bash
python src/workflow_fast.py approve --stage <stage> --campaign <campaign_id> --pack <pack_id>
```

Прямой `workflow_context.py approve` отключен: он обходил применение review, пересборку и validation.

## Единственная Папка Для Ручных Правок

Человек вручную правит только файлы внутри:

```text
campaigns/<campaign_id>/<pack_id>/review/
```

- Stage 1-5: `stage1_review.md` ... `stage5_review.md`.
- Stage 6: конечные `review/proto/*.xlsx`, по одному `conf` в файле.
- Все остальные файлы pack — машинные source/build/validation артефакты. Человеку не нужно и не следует править их вручную.
- Approval Stage 1-5 применяет соответствующий review обратно в machine source, пересобирает и валидирует производные артефакты, затем сохраняет SHA-256 review.
- Если review изменился после approval, следующий gate откажет в работе до повторного approval.
- Approval выполняется строго по порядку Stage 1 → 2 → 3 → 4 → 5; Stage 6 проверяет всю цепочку, а не только последний gate.
- Существующий review не перезаписывается автоматически. Осознанная замена требует `review --force` или `stage6 --force-review`.

## Быстрый Маршрут

Для рутинной работы использовать `src/workflow_fast.py`: он берет стандартные pack-пути, читает `active_context` при отсутствии `--campaign/--pack` и не заставляет вручную перечислять одинаковые аргументы.

При старте новой campaign Codex сам придумывает `campaign_id` по теме пользователя. При старте нового pack Codex сам берет следующий `pack_id` по порядку из campaign metadata, начиная с `pack_001`; не нужно задавать пользователю отдельные вопросы про эти id.

```bash
python src/workflow_fast.py status --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py interactive-objects --campaign <campaign_id> --pack <pack_id> --select chest_1 --select help_1
python src/workflow_fast.py review --stage 1 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 1 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py review --stage 2 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 2 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py stage3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py context --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py fill --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py quest-group --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
```

`stage6` также автоматически агрегирует ресурсы campaign в `review/proto/<campaign_id>_resources.xlsx`. Команда `resource-table` остается только как ручной fallback для отдельной пересборки/отладки, но в обычном workflow после Stage 6 ее запускать не нужно.

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
review/proto/<campaign_id>_quests.xlsx
review/proto/<campaign_id>_actions.xlsx
review/proto/quest_<campaign_id>_accomplished.xlsx
review/stage1_review.md
review/stage2_review.md
review/stage3_review.md
review/stage4_review.md
review/stage5_review.md
review/proto/*.xlsx
```

Campaign-level files:

```text
campaigns/<campaign_id>/interactive_objects.json
campaigns/<campaign_id>/interactive_objects.preview.md
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
- автоматически создает review Stage 3-6 и запрещает переходы без обязательных review;
- применяет ручные изменения только из `review/`, пересобирает Stage 3-5 и хранит контрольную сумму утвержденного review;
- экспортирует обзор XLSX и отдельные conf-файлы;
- экспортирует XLSX/conf интерактивных объектов по `data/interactive_object_templates.json`;
- экспортирует actions XLSX/conf для персонажей, Give и HOG search;
- агрегирует ресурсы всех pack campaign в `review/proto/<campaign_id>_resources.xlsx` как обязательную часть Stage 6;
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
python src/workflow_fast.py approve --stage 1 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 2 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 3 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 4 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
```

Скрипты должны отказываться работать, если gate отсутствует:

- `workflow_fast.py context` всегда требует действующий approval Stage 3 и неизмененный `stage3_review.md`.
- `build_quest_group.py` требует approval stage 4.
- `export_csv.py` требует approval stage 5.
- `workflow_fast.py stage6` дополнительно требует полный семантически непустой комплект review и действующую цепочку approval Stage 1-5.

## Workflow 1-6

### Перед Stage 1 - Интерактивные Объекты

Перед началом новой campaign Codex должен спросить пользователя, какие 2 или больше интерактивных объекта выбрать на всю campaign. Меньше двух в базовом сценарии выбирать нельзя. `Chest_*_Home/Guest` и `HELP_*_Home/Guest` считаются одним объектом. Сейчас поддержаны:

- `exchanger` - Exchanger / обмен ресурсами с друзьями; источник ресурсов может быть `generator` или `gr`.
- `chest_1` - парный `Chest_1_Home` + `Chest_1_Guest`; пара считается одним интерактивным объектом.
- Для `chest_1` Home/Guest используют donors `Dacha_2025` с `find=Dacha_2025`, `replace=<campaign_id>`; GR, R, package и global reward используют donors `Fun12_FunCollection_1`. Все `id` остаются пустыми.
- `help_1` - парный `HELP_1_Home` + `HELP_1_Guest`; пара считается одним интерактивным объектом.
- `friend_action_1` - `Story_FriendAction_1`: действие у друзей с шансом, дневным лимитом, флагом доступности и двумя `FA`-ресурсами (`reward_for_action`, `reward_on_receive`).
- `story_random_recipe` - `Story_RandomRecipe`: chest-объект с `generate_price`, случайным набором ресурсов цены и одним итоговым `R_1` без `CL`/`MB`.
- Для `story_random_recipe` donor объекта всегда `/chest/Fun/Fun13/Fun13_Story_RandomRecipe_1.proto.js`; `rule_window` заполняется видимым тематическим текстом, а не техническим classname.
- `mixer_1` - `Story_Mixer`: миксер для квестов, тратит два `GR`-ингредиента и один `ASK_1`, правильное действие сразу выдает готовый `R_1` без mystery box и без `CL`.

Выбор фиксировать в:

```text
campaigns/<campaign_id>/interactive_objects.json
```

Быстрая команда для первичной фиксации выбранных шаблонов:

```bash
python src/workflow_fast.py interactive-objects --campaign <campaign_id> --select chest_1 --select help_1
```

Перед Stage 1 Codex задает короткую анкету: какие механики выбрать, как должен выглядеть каждый объект, какой ресурс он дает, какой ресурс нужен для активации/обмена, и что делать, если пользователь хочет оставить детали на ИИ. Если пользователь оставляет выбор за ИИ, названия и сущности заполняются по общей теме campaign.

Если пользователь выбирает несколько объектов одной механики, они нумеруются последовательно: `Chest_1`, `Chest_2`, `HELP_1`, `HELP_2`, `Exchanger_1`, `Exchanger_2`, `Story_FriendAction_1`, `Story_FriendAction_2`, `Mixer_1`, `Mixer_2`. Если механика выбрана один раз, используется обычное имя из шаблона. Ресурсы выбранных объектов не меняются от pack к pack внутри campaign.

Result resources выбранных объектов используются как 3-й и 4-й ингредиенты craft recipe в таблице ресурсов. Для `Chest`, `HELP`, `Exchanger`, `story_random_recipe` и `mixer_1` это ресурсы с суффиксом `_R_`; для `friend_action_1` по умолчанию это `Story_FA_2` (`reward_on_receive`). При 3+ объектах ингредиенты идут по кругу: 1-й craft берет объекты 1+2, 2-й craft берет 3+4, если 4-го нет - 3+1, дальше продолжается тот же круг.

### Stage 1 - Сюжетная Структура

Цель: создать основу pack: тема, конфликт, герои, ход серии.

Выход:

```text
campaigns/<campaign_id>/<pack_id>/stage1_story.txt
campaigns/<campaign_id>/<pack_id>/review/stage1_review.md
```

`stage1_story.txt` — машинный source. Перед показом результата обязательно создать `stage1_review.md`; пользователь правит только его:

```bash
python src/workflow_fast.py review --stage 1 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 1 --campaign <campaign_id> --pack <pack_id>
```

### Stage 2 - Реплики

Цель: подготовить начало и завершение квестов, сохранить тон campaign.

Выход:

```text
campaigns/<campaign_id>/<pack_id>/stage2_story.txt
campaigns/<campaign_id>/<pack_id>/review/stage2_review.md
```

`stage2_story.txt` — машинный source. Перед показом результата обязательно создать `stage2_review.md`; пользователь правит только его:

```bash
python src/workflow_fast.py review --stage 2 --campaign <campaign_id> --pack <pack_id>
python src/workflow_fast.py approve --stage 2 --campaign <campaign_id> --pack <pack_id>
```

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
- Загадки в Stage 4 можно сохранять с буквальным `\n` внутри `hint`, если переносы помогают стихотворной форме или читаемости загадки.
- Для русских `title` и `hint` использовать падежные формы: персонажи после `с` в творительном падеже, предмет после `Найди/Получи/Создай/получить` в винительном, объект после `в` в винительном, мусор в игровых заданиях в форме, которая читается естественно для множественного сбора.

Быстрая команда:

```bash
python src/workflow_fast.py stage3 --campaign <campaign_id> --pack <pack_id>
```

Команда автоматически создает `review/stage3_review.md`. Если файл уже существует, он сохраняется без перезаписи ручных правок.

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

`workflow_fast.py context` запускается только после действующего approval Stage 3. Если `stage3_review.md` изменен после approval, context pack не собирается до повторного approval.

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

Команда автоматически создает `review/stage4_review.md`. Пользователь проверяет и правит только этот review; approval применяет его в `task_choices.json`, заново собирает `filled_tasks.json` и запускает validation.

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

Команда автоматически создает `review/stage5_review.md`. Пользователь правит только review; approval применяет его в `quest_group_choices.json`, заново собирает `quest_group.json` и запускает validation.

Выход:

```text
campaigns/<campaign_id>/<pack_id>/quest_group.json
campaigns/<campaign_id>/<pack_id>/quest_group_choices.json
campaigns/<campaign_id>/<pack_id>/quest_group.validation.json
campaigns/<campaign_id>/<pack_id>/quest_group.preview.md
```

Важно:

- `quest_group.json` привязан к pack, а не к `output/`.
- Проверенный donor для quest group — `Night_2026`: `input` всегда `/quest_group/event/Night_2026/Night_2026_Story.proto.js`.
- `output` строится как `/quest_group/event/<campaign_id>/<campaign_id>_Story.proto.js`; `pack_id` в classname не добавляется. Техническая группа лежит рядом: `<campaign_id>_Tech.proto.js`.
- Служебные поля quest group: `id` пустой, `find=Night_2026`, `replace=<campaign_id>`.
- Старый объект `extra` (`quest_reward_prewiew`, `description_condition`, `description_complete`) больше не входит в этот шаблон.

После approval пользователя записать:

```bash
python src/workflow_fast.py approve --stage 5 --campaign <campaign_id> --pack <pack_id>
```

### Stage 6 - Конечные XLSX/conf, список package и дополнение к станку

После ручной проверки основных таблиц обязательно выполнить подэтап **6.1 «Подключение диалогов»** по [DIALOGUE_WORKFLOW.md](DIALOGUE_WORKFLOW.md), используя `quest-dialog-proto` и `python src/workflow_fast.py dialogs`. Сценарий готовится на творческих этапах; техническое подключение выполняется после Stage 6. Команда `stage6` напоминает об этом шаге, но не запускает его до готовности реестра, утверждённых реплик и предоставленных ID. Финальная поставка включает подключённые разговоры и повторную проверку текущих XLSX.

Обязательная защита GR от противоречий (21.10.2026): hint квеста и description ресурса должны совпадать с фактическими actions/assets/location_tags. При конкретном мусоре применять TT-014/TT-015, например `Убирай Ржавый гвоздь в гостях, чтобы найти. Место поиска: Котельная.` Старый TT-013 с конкретным кандидатом автоматически разрешается в правильный шаблон при сборке Stage 4. После изменения кандидата в stage4_review.md approval заново применяет choices и пересобирает filled_tasks; источник и mode должны обновить текст. Ручные XLSX Stage 6 автоматически не пересобирать. Для них проверять `src/gr_table_review.py <campaign_id> --tables-dir <актуальная папка>`; адресная правка только текстов — отдельный `--apply`. Эта проверка также обязательна в Stage 6 и при реальной конвертации пары quests/resources. Подробнее — раздел «GR: текст обязан совпадать с реальным выпадением» в `PROTO_EXPORT_WORKFLOW.md`.

Всегда включать отдельный `MB_RECIPEMB_POTS_<campaign_id>.xlsx`: 3 MB + 3 recipe + 3 pot. Все `R_MB_N_Recipe.ingredients` равны первому `R_1_Recipe.ingredients` текущей campaign, без изменения порядка/количеств; названия могут быть тестовыми. Stage 6 создаёт файл через `src/mystery_rewards.py` до технической очистки. Существующий ручной файл не пересобирать; изменения ingredients применять адресно. Полный контракт — в `PROTO_EXPORT_WORKFLOW.md`, раздел «Обязательные мистери-боксы и горшочки».

Дополнение пользователя от 20.10.2026: рядом с XLSX всегда создавать `<campaign_id>_shop_invisible_packages.txt` для ручного заполнения `shop_invisible.proto.js`. Сверху пути к `d:\domovoy\trunk\server\prototypes\context_shop\` и самому файлу магазина, далее все package из актуальных XLSX по одной строке `"<classname>",`, без дублей. Этот обязательный TXT — исключение из прежнего «только XLSX». Конечный conf writer обновляет его автоматически; после ручных правок использовать `workflow_fast.py package-list --campaign <id> --pack <pack> --tables-dir <актуальная папка>`. Сам магазин не редактировать. Полный контракт: `PROTO_EXPORT_WORKFLOW.md`, раздел «Список покупок для невидимого магазина».

Дополнение пользователя от 21.10.2026: всегда создавать ещё `<campaign_id>_DayOfDomovoyCaldron.txt` в той же папке. Сверху путь к `d:\domovoy\trunk\server\prototypes\workbench\DayOfDomovoyCaldron.proto.js`, затем готовый объект для `extra.set`: campaign id/title/icon, `attention="Изготавливать можно"`, `conditions="active_quest_group=<campaign_id>_Tech"`, все рецепты из актуальных XLSX (включая MB и интерактивные объекты), без дублей. Не ограничивать список фиксированными номерами и не собирать donor input. Общий conf writer обновляет TXT автоматически; после ручных правок — `workflow_fast.py workbench-addition --campaign <id> --pack <pack> --tables-dir <актуальная папка>`. Станок и ручные таблицы не изменять. Для VelesNight_2026 читать рабочую папку первой и сохранять копию TXT рядом с репозиторными XLSX. Оба TXT — обязательные исключения из «только XLSX». Полный контракт — раздел «Дополнение к станку DayOfDomovoyCaldron» в `PROTO_EXPORT_WORKFLOW.md`.

Пустые `id` и `tasks.N.identifier` относятся к первичной выдаче на проверку. После сообщения пользователя со свободными proto/task ID выполнять отдельное назначение через `src/proto_ids.py` в текущих ручных XLSX. Не регенерировать pack; сохранять уже назначенные значения. Проверка всей назначенной поставки — `validate_proto_exports.py --assigned-ids`. Правила уникальности и команды: `PROTO_EXPORT_WORKFLOW.md`, раздел «Назначение предоставленных пользователем ID».

Согласовано 19.10.2026: вся конечная выдача находится в `campaigns/<campaign_id>/<pack_id>/review/proto/`, в каждом XLSX один лист `conf`. Подробный контракт: `workflows/PROTO_EXPORT_WORKFLOW.md`.

```bash
python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>
```

Команда проверяет действующие approval/review Stage 1–5 и validation, затем сразу создаёт `<campaign_id>_quests.xlsx`, `<campaign_id>_actions.xlsx`, `<campaign_id>_resources.xlsx`, `<campaign_id>_interactive_<mechanic>.xlsx`, `quest_<campaign_id>_accomplished.xlsx` и учитывает выбранные FunCollection, например `<campaign_id>_funcollection_4.xlsx`, в этой же папке. После них создаёт `<campaign_id>_technical_quests.xlsx` с технической группой и Tech_1/Tech_2. Очистка Tech_2 берётся из текущих XLSX всех pack: все собственные ресурсы, персонажи, HOG, интерактивы и состояния/эффекты потех. Все identifier задач и id при первичной генерации пустые для последующего назначения пользователем; имена самих прототипов заполнены. Срок события `spoil_conditions` требует заполнения до импорта. Детали и отдельная команда добавления технической таблицы — в `PROTO_EXPORT_WORKFLOW.md`. Ресурсы агрегируют все pack campaign. Необходимая campaign memory обновляется.

CSV, ZIP, manifests, validation_report, экспортные summary JSON и дополнительный многолистовой обзор не создаются. Результаты обязательных проверок выводятся в консоль. Технические временные данные проверки разрешены только в `output/`, когда они действительно нужны.

Пользователь сейчас вручную проверяет конечные XLSX. Не перезаписывать их. После его сообщения о завершении закрепить подтверждённые исправления в генераторах, шаблонах, документации и проверках. После проверки таблиц оформить скилл создания квестов. `stage6 --force` допустим только для намеренной регенерации; FunCollection сохраняется даже при общем force. Старый `stage6-split` оставлен для миграции старого обзора и не создаёт manifest.

`<campaign_id>_actions.xlsx` содержит actions текущего pack и всех helper-персонажей, включая блок `ПЕРСОНАЖИ БЕЗ ЭКШЕНОВ`. Для каждого персонажа нужен свой `ml` блок; нумерация учитывает предыдущие pack campaign.

Контракт `<campaign_id>_quests.xlsx` / `conf`:

- quest group использует `ml`; quest использует `sl`; task использует `ml`. Значения `temp`, `temp_01`, `temp_02` в этом листе запрещены;
- у quest group и quest нет колонок `extra.*`; вместо них используются `id`, `find`, `replace`;
- quest N берет `input` из `/quest/event/Night_2026/Night_2026_Story_N.proto.js`, а новый `output` — `/quest/event/<campaign_id>/<campaign_id>_Story_N.proto.js`; все Story и Tech квесты лежат прямо в папке campaign внутри `event`, без подкаталогов `story_N` или `tech`;
- каждый task quest N берет и `input`, и `output` из нового output этого quest, а не из `Night_2026`;
- `id` quest N при первичной генерации пустой, `find=Night_2026`, `replace=<campaign_id>`; после отдельного назначения пользователя содержит выделенный proto id;
- для `TT-033` использовать classname `<campaign_id>_Give_<character_number>_<give_number>`, а не classname на основе глобального `task_number`.

Контракт `<campaign_id>_actions.xlsx` / `conf`:

- entity/furniture блоки используют `ml`, action блоки используют `sl`; значения `temp`, `temp_01`, `temp_02` запрещены;
  - `id` всех персонажей, квестов, quest group и action оставлять пустыми; ID не резервировать и не назначать;
- персонажи без экшенов берут `input` из `/furniture/Fun/Fun13/Character/Fun13_Character_23.proto.js`, персонажи с экшенами — из `/furniture/Fun/Fun13/Character/Fun13_Character_18.proto.js`;
- Give action берет `input` из `/quest_action/Fun/Fun13/Fun13_Character_18_Give_1.proto.js`;
- у `TT-033` identifier action строится от classname предмета `Give_*`, а action добавляется в `behaviour.0.actions` персонажа-получателя из `person`/`hint`; отдельная furniture-сущность с classname предмета не создается;
- строки листа не закреплять (общее правило пользователя от 19.10.2026).

Контракт `<campaign_id>_resources.xlsx` / `conf`:

- все ресурсные блоки используют `sl`; значения `temp`, `temp_01`, `temp_02` запрещены;
- `id` всегда остается пустым, даже если в файле-доноре есть числовые ID;
- поля, объявленные как `int`, записываются в XLSX числами, а не строками;
- строки листа не закреплять.

Контракт `<campaign_id>_interactive_story_randomrecipe.xlsx` / `conf`:

- все блоки используют `sl`, числовые поля записываются числами;
- GR probability по умолчанию равна `35`;
- обе объектные колонки `id` и все остальные `id` остаются пустыми;
- финальная колонка `id` после `price_elements.7.price` обязательна;
- строки листа не закреплять.

Контракт дополнительного `quest_<campaign_id>_accomplished.xlsx`:

- файл создаётся всегда при Stage 6 в `review/proto/` текущего pack;
- лист называется `conf` и содержит один блок `quest_<campaign_id>_Story_accomplished`;
- одна строка создается для каждого `classname_quests` из `filled_tasks.json`, без ручного списка и пропусков;
- тип блока `sl`, donor `/post_action/quest_Night_2026_Story_1_accomplished.proto.js`;
- `output` и `identifier` строятся как `quest_<classname_quests>_accomplished`;
- `title=Задание выполнено!`, `text=ТЫ МОЛОДЕЦ!`, `img_url=icon/post_new/quest_Night_2026_Story.jpg`, `photo_id=456244744`, `link_text=Получить {0}`, `clicker_reward=money_alt=50`;
- `clicks_limit=5` и `life_time=43200` записываются числами, `id` остается пустым;
- `freeze_panes` не используется.

`<campaign_id>_resources.xlsx` на Stage 6 собирается автоматически вместе с остальными conf-файлами по всем `pack_*`. CSV не создавать. Проверка и ограничения конвертера описаны в `workflows/PROTO_EXPORT_WORKFLOW.md`.

Экспорт не создаётся, если:

- отсутствует или пуст хотя бы один review Stage 1-5;
- отсутствует любой approval Stage 1-5;
- любой `stage1_review.md`-`stage5_review.md` изменен после approval;
- validation stage 4 содержит errors;
- validation stage 5 содержит errors;
- `interactive_objects.json` есть и заполнен, но в нем неизвестный template id или противоречивые данные. Пустой файл выбора не должен жестко блокировать нестандартные сценарии;
- validation-файл устарел относительно входного JSON.

`workflow_fast.py stage6` после успешного экспорта сам обновляет campaign memory. Если использовался низкоуровневый `export_csv.py`, обновить память отдельно:

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
- писать XLSX для всей campaign в `campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_resources.xlsx`;
- в обычном quest workflow XLSX/conf ресурсов собирает `python src/workflow_fast.py stage6 --campaign <campaign_id> --pack <pack_id>` вместе с остальными XLSX; отдельная команда `python src/workflow_fast.py resource-table --campaign <campaign_id> --pack <pack_id>` нужна только для ручной пересборки/отладки;
- даже при ручном фильтре по входным pack сохранять итоговый XLSX в `review/proto/` текущего pack, если пользователь явно не указал другой `--output-xlsx`;
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
