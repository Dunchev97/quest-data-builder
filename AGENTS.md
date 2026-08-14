# AGENTS.md

Короткие правила для Codex в этом проекте. Подробный пользовательский workflow живет в `workflows/WORKFLOW_GUIDE.md`, машинная карта режимов - в `workflows/workflow_modes.json`.

## Язык

- Всегда отвечать пользователю на русском.
- Не переводить code identifiers, JSON keys, CSV headers, classnames, paths и Python identifiers.

## Главные источники правды

- `workspace/active_context.json` - локальный, некоммитящийся контекст текущего пользователя: `mode`, `campaign_id`, `pack_id`, `stage`, `quest_number`, `task_number`.
- `campaigns/<campaign_id>/campaign_tone.md` - тон, стиль, запреты и словарь campaign. Если файла нет, уточнить у пользователя; ИИ пишет его сам только при явном разрешении пользователя.
- `campaigns/<campaign_id>/<pack_id>/` - постоянные артефакты конкретного pack.
- `data/quest_ready_index.json` и `data/quest_ready_drops.index.json` - единственные игровые индексы для генерации quest/task data.
- `raw/` - исходные игровые данные. Никогда не редактировать.
- `workflows/WORKFLOW_GUIDE.md` - порядок работы по этапам 1-6.
- `workflows/POT_DESCRIPTION_WORKFLOW.md` - workflow описания горшков по картинке.
- `workflows/RESOURCE_TABLE_WORKFLOW.md` - workflow CSV-таблицы ресурсов для дева.
- `workflows/FUN_INTERACTIVE_OBJECT_WORKFLOW.md` - workflow potekha/FunCollection интерактивных объектов и отдельного Workbench.
- `docs/FunCollection/FUN_COLLECTION_TEMPLATES.md` - понятные шаблоны FunCollection по exact ID; структура снимается только с листа `conf` в `docs/FunCollection/*.xlsx`.
- `docs/QUEST_INTERACTIVE_OBJECT_TEMPLATES.md` - понятные шаблоны quest interactive objects, включая `mixer_1` / `Story_Mixer`; структура `Story_Mixer` снята с `raw/examples/Story_Mixer.xlsx`.
- `data/fun_interactive_object_templates.json` - машинные шаблоны для генерации FunCollection/Workbench объектов по теме.
- `workflows/workflow_modes.json` - ключевики и режимы для `workflow_context.py`.
- `docs/domovata_style_guide.md` - базовый стиль текстов Домовят.

## Справочные Подборки

- Если пользователь просит в режиме справочника найти элементы коллекций, мусор, цветы, локации или другие игровые сущности по теме, брать рабочие данные из `data/quest_ready_index.json`.
- Для элементов коллекций использовать секцию `quest_ready_collections`, для мусора - `quest_ready_garbage`, для цветов - `quest_ready_flowers`, для локаций - `quest_ready_locations`.
- `data/quest_ready_drops.index.json` использовать дополнительно только когда нужны связи выпадения и drop-кандидаты.
- `raw/` не использовать как первичный источник для справочных подборок и не редактировать.

## Локальная среда и скорость

- Не использовать `rg`: в этой среде `rg.exe` стабильно падает с `Access is denied`.
- Для поиска по файлам использовать PowerShell: `Get-ChildItem ... | Select-String ...`.
- Не тратить время на очистку `__pycache__/` и `*.pyc` после каждого запуска скриптов или тестов.
- `__pycache__/` и `*.pyc` не являются контентными артефактами; их не коммитить и чистить только перед commit/release или по явной просьбе пользователя.
- Для рутинных этапов предпочитать короткий wrapper `python src/workflow_fast.py ...`, а не длинные команды с ручным перечислением всех путей.
- В content workflow не запускать полный `python -m unittest discover -s tests` после каждого квестового этапа; использовать stage validator конкретного этапа. Полный набор тестов запускать после изменений кода, шаблонов или workflow-инструкций.
- `git status` проверять в начале/конце работы или перед коммитом, а не после каждой промежуточной команды.

## Кириллица И Кодировки

- Не передавать Python/Node/другим внешним процессам скрипты или данные с кириллицей через PowerShell pipe вида `@'...'@ | python -`: в этой среде PowerShell может заменить русские буквы на `?`, и файл будет реально испорчен.
- Если нужно сгенерировать CSV/XLSX/JSON с кириллицей, сначала сохранить кириллические данные в UTF-8 файл через `apply_patch` или PowerShell `Set-Content -Encoding UTF8`, затем запускать ASCII-only скрипт, который читает этот UTF-8 файл.
- Для Excel-friendly CSV писать `cp1251` только из уже проверенных Unicode-строк; не использовать `errors="replace"` и не маскировать ошибки кодировки.
- После генерации CSV/XLSX с кириллицей обязательно прочитать файл обратно и проверить, что в `title`, `description`, русских заголовках и текстовых окнах нет `????`, а контрольные русские строки из анкеты присутствуют.
- Если консоль показывает кракозябры, не считать это доказательством порчи файла: проверять чтением файла с правильной кодировкой и точечными assertions.

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
3.1. Context pack для смыслового заполнения task choices.
4. `task_choices.json`, автоматическая сборка `filled_tasks.json`, validation и вывод пути к файлу для проверки.
5. Quest group для pack.
6. CSV export.

Правила:

- Выполнять только один этап за раз.
- При создании новой campaign не спрашивать `campaign_id`: придумать стабильный англоязычный id по теме пользователя, например `<Theme>_2026`.
- При создании нового pack не спрашивать `pack_id`: брать следующий номер по порядку через campaign metadata, начиная с `pack_001`.
- Перед Stage 1 новой campaign спросить пользователя, какие минимум 2 интерактивных объекта выбрать на всю campaign; `Chest_*_Home/Guest` и `HELP_*_Home/Guest` считаются одним объектом.
- В той же анкете спросить сущность выбранных объектов и ресурсов; если пользователь оставляет выбор за ИИ, заполнять тематически по сути campaign.
- Выбранные интерактивные объекты фиксировать в `campaigns/<campaign_id>/interactive_objects.json`.
- Если пользователь выбирает несколько объектов одной механики, нумеровать их последовательно (`Chest_1`, `Chest_2`, `HELP_1`, `HELP_2`, `Exchanger_1`, `Exchanger_2`, `Story_FriendAction_1`, `Story_FriendAction_2`, `Mixer_1`, `Mixer_2`). В остальных случаях ресурсы выбранных объектов не менять на протяжении campaign.
- Для quest mixer использовать template `mixer_1` / `Story_Mixer`: читать `docs/QUEST_INTERACTIVE_OBJECT_TEMPLATES.md`; квестовая версия тратит `GR_1+GR_2+ASK_1` и сразу выдает готовый `{campaign_id}_Mixer_N_R_1`, без `MB` и без `CL`.
- После каждого творческого этапа показывать результат пользователю и ждать явный approval.
- После Stage 3 в сводке по каждому квесту показывать не только `Task template ID`, но и `task_template_names` / русские названия шаблонов, например: `TT-001 Диалог / TT-008 Получить ASK / TT-004 HOG на локации`.
- Stage 3.1 - технический подготовительный шаг без отдельного approval; запускать после утвержденного stage 3 перед stage 4.
- Stage 5 нельзя собирать до approval stage 4.
- Stage 6 нельзя запускать до approval stage 5.
- Stage 6 обязательно вместе с остальными CSV пересобирает campaign-level `campaigns/<campaign_id>/resource_table.csv` и `resource_table.summary.json`: таблица ресурсов агрегирует все `pack_*` текущей campaign по `docs/resource_table_template.csv` / `workflows/RESOURCE_TABLE_WORKFLOW.md`, а не создается отдельным ручным шагом после экспорта.
- В `generated_actions.csv` создавать и персонажей без экшенов: отдельный блок с заголовком `ПЕРСОНАЖИ БЕЗ ЭКШЕНОВ`, строки персонажей без параметра `behaviour.0.actions`.
- Approval записывать через `src/workflow_context.py approve`.
- На Stage 3 task templates `TT-008` (`get_asset ASK`) и `TT-009` (`get_asset PER`) использовать только внутри квестов, где в этом же квесте есть `TT-002` (`get_and_decrease_asset craft`) или `TT-033` (`action give`). В обычных поисковых/сюжетных квестах без craft/give не ставить ASK/PER.
- На Stage 3 любой HOG template (`TT-003`-`TT-007`) нельзя ставить в квест, если в предыдущем квесте в любом task уже был HOG.
- В крафтовых квестах чередовать `ASK` и `PER` между собой: если предыдущий крафтовый квест использовал `ASK`, следующий крафтовый должен использовать `PER`, и наоборот.
- После каждого этапа (1-6) обязательно генерировать review-документ командой `python src/workflow_fast.py review --campaign <campaign_id> --pack <pack_id> --stage <N>`. Review-файлы сохраняются в `campaigns/<campaign_id>/<pack_id>/review/stageN_review.md` (для stage 6 — `stage6_review.xlsx`). Review генерируется всегда, до approval, чтобы пользователь мог проверить результат.
- Stage 2 `stage2_story.txt` писать в формате `N. Персонаж: Название` с нумерацией квестов в первой строке блока, чтобы парсер `review_docs.parse_stage2_source` находил заголовки. Поле `Суть:` писать без префикса `Суть задания:`, чтобы review stage 4 корректно подхватывал суть квеста в свой раздел.

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
- В recipe craft 3-й и 4-й ингредиенты брать из выбранных интерактивных `_R_` ресурсов campaign по кругу: 1-й craft = объекты 1+2, 2-й craft = 3+4, если 4-го нет = 3+1, дальше продолжать по кругу. Не дублировать 1-й и 2-й ингредиенты, если есть выбранные interactive resources.

## Fun Interactive Object Workflow

Если пользователь просит собрать potekha/FunCollection интерактивные объекты, новые `FunCollection_*`, объект для потех или XLSX/CSV по FunCollection-механике:

- читать `workflows/FUN_INTERACTIVE_OBJECT_WORKFLOW.md`;
- читать `docs/FunCollection/FUN_COLLECTION_TEMPLATES.md` перед генерацией FunCollection по теме;
- использовать машинные шаблоны из `data/fun_interactive_object_templates.json`;
- доноры брать из `docs/FunCollection/*.xlsx`; для структуры использовать только лист `conf`, не `Downloads` и не старые вспомогательные вкладки;
- при генерации CSV/XLSX с русскими текстами соблюдать правила раздела `Кириллица И Кодировки` и делать smoke-check на отсутствие `????`;
- не смешивать эти объекты с quest interactive objects из `campaigns/<campaign_id>/interactive_objects.json`;
- `Workbench` считать отдельным шаблоном, а не FunCollection-потехой;
- если пользователь дает точный ID объекта (`FunCollection_9` и т.п.), использовать template с этим exact `id`, а не подбирать похожую механику;
- по теме пользователя подбирать названия объекта, ресурсов, составных частей и 10 `CL`-наград в стиле Домовят;
- если пользователь не дал конкретный объект, выбрать объект по сути темы и явно показать, как он мапится на выбранную механику;
- для `FunCollection_5` помнить: `Unlock` не выдает CL-награды сам; загрузка `Unlock` ресурсами разрешает пользоваться объектом/окном, а подарки друзей потом тратятся на коллекционный ресурс.
- для `FunCollection_2` / `Story_HELP`-подобной механики использовать template `FunCollection_2`: база `data/interactive_object_templates.json#help_1`, 10 Home/Guest пар, 10 `CL`-ресурсов и `multiplicity` по последней цифре ID.
- для `FunCollection_6` / чет-нечет mystery box механики использовать template `FunCollection_6`: две половины игроков по последней цифре ID, два взаимных `GR`-ресурса, обмен/подарки друзьям, recipe `GR_1+GR_2 -> MB` и 10 случайных `CL`-элементов коллекции.
- для exact ID `FunCollection_7` использовать template `FunCollection_7`: потешный миксер, два `GR`-ингредиента + `ASK_1`, right_action выдает `MB_1`, а `MB_1` дает 1 из 10 случайных `CL`; не оставлять donor-ошибки `FunCollection_6_MB_1`, `FunCollection_7_2` без `_GR_` и `Fun12` в CL outputs.
- для exact ID `FunCollection_9` использовать template `FunCollection_9`: friend_action у друзей, `FA_1` игроку за действие, `FA_2` хозяину дома при получении действия, recipe `FA_1+FA_2 -> MB`, станок крафта и 10 случайных `CL`-элементов коллекции.

## Где Хранить Артефакты

- `output/` - локальный временный рабочий прогон, не источник правды для campaign и не место для коммита.
- `campaigns/<campaign_id>/<pack_id>/` - постоянное место для файлов pack.
- Для quest workflow все постоянные артефакты этапов 1-6 хранить в `campaigns/<campaign_id>/<pack_id>/`, включая `quest_plan.json`, `quest_plan.resolved.json` и `context_pack.json`. Campaign-level `interactive_objects.json` хранить отдельно в `campaigns/<campaign_id>/interactive_objects.json`.
- `quest_group.json` всегда хранить в папке pack:

```text
campaigns/<campaign_id>/<pack_id>/quest_group.json
```

Stage 6 должен брать `filled_tasks.json` и `quest_group.json` из папки pack и писать:

```text
campaigns/<campaign_id>/<pack_id>/generated_quests.csv
campaigns/<campaign_id>/<pack_id>/generated_actions.csv
campaigns/<campaign_id>/<pack_id>/generated_actions.summary.json
campaigns/<campaign_id>/generated_interactive_objects_*.csv
campaigns/<campaign_id>/generated_interactive_objects.summary.json
campaigns/<campaign_id>/resource_table.csv
campaigns/<campaign_id>/resource_table.summary.json
```

## Роли ИИ И Кода

- ИИ отвечает за творческие решения: сюжет, реплики, выбор task types, смысловые `task_choices` по контексту, загадки, `choice_reason`, тексты quest group.
- Код отвечает за guardrails: parsing, context pack, сборку strict `filled_tasks.json` из `task_choices.json`, validation, approval gates, CSV export, actions CSV export, обязательный Stage 6 export campaign-level `resource_table.csv`, campaign memory.
- Не выдумывать игровые факты. Classname, title, location, collection, garbage, flower и связи должны приходить из parsed/generated/quest-ready data.
- Для задач `in_guest` нельзя предлагать мусор, локации, `collection_drop` или `gr_garbage`, привязанные к локациям с тегом `world`; такие кандидаты допустимы только для домашних задач.
- `TT-010` / `Получить CL (награда за коллекцию)` не использовать: у workflow нет достоверного списка наград за коллекции.
- Загадки можно писать в несколько строк, используя буквальный `\n` внутри `hint`, если переносы помогают стихотворной форме или читаемости загадки.
- В русских `title` и `hint` использовать нужные падежи, а не сырые названия из индекса: `с Журналисткой Гердой`, `Барабанные палочки`, `в Бочку`, `получить Хрустящую реликвию`.
- **Интерактивные объекты (Chest, HELP, Exchanger, Story_FriendAction, Mixer) не упоминаются в текстах квестов как сюжетные элементы.** Они участвуют в крафтовых заданиях автоматически через свои result resources и не должны быть "сердцевиной" квеста. Не делать квесты про "открыть сундук", "зажечь фонарь", "наполнить обменник", "нажать friend action" или "смешать в миксере" — эти механики уже встроены в игру. Тексты квестов должны описывать бытовой/сюжетный конфликт, а не интерактивные объекты.

## Стиль текста Домовят

Все тексты, которые пишет ИИ (description, congratulation, dialogue_replica, quest group, загадки), должны соответствовать базовому стилю игры "Домовята".

Краткий чек-лист:
- **Тёплое обращение**: домовёнок, дружок, друг мой — никаких "игрок", "Вам необходимо".
- **Description — история, не инструкция**: объясняет, что случилось и почему нужна помощь.
- **Congratulation — благодарность + итог**: всегда благодарит, даёт позитивный или смешной финал.
- **Персонажи говорят по-разному**: у каждого свой голос (Яга — экспериментаторша, Леший — простой и боязливый, Кощей — тщеславный, старик — мудрый и спокойный).
- **Конфликт — добродушный хаос**: перепутанные рецепты, забывчивость, бытовой хаос. Никогда злобных угроз или депрессии.
- **Магия через быт**: лунные кристаллы увеличили яйцо → не влезает в котёл.
- **Никаких формальных слов**: убрать "необходимо", "требуется", "цель", "миссия".

Полный гайд: `docs/domovata_style_guide.md`.

Перед генерацией текстов на этапах 1, 2, 4, 5 ИИ должен прочитать этот гайд.
Если существует `campaigns/<campaign_id>/campaign_tone.md`, стиль Домовят остаётся базой, а `campaign_tone.md` добавляет campaign-specific словарь и рамки.

## Проверки

Перед финальным ответом после изменений запускать релевантные тесты. Для контентных этапов достаточно профильного validator-а. Для широких изменений кода или инструкций:

```bash
python -m unittest discover -s tests
```

Не коммитить `__pycache__`/`*.pyc`.

## Оптимизация Workflow

- Stage 6 работает инкрементально: не пересобирать `resource_table.csv` и interactive-object CSV, если выходные файлы свежее всех входных pack/campaign файлов.
- Для generated-нумерации текущего pack учитывать только предыдущие pack-и campaign. Более поздние pack-и не должны создавать ошибки validation для раннего pack.
