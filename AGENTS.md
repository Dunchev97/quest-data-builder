# AGENTS.md

Короткие правила для Codex в этом проекте. Подробный пользовательский workflow живет в `workflows/WORKFLOW_GUIDE.md`, машинная карта режимов - в `workflows/workflow_modes.json`.

## Язык

- Всегда отвечать пользователю на русском.
- Не переводить code identifiers, JSON keys, CSV headers, classnames, paths и Python identifiers.

## Excel: Без Закрепления Строк

- По указанию пользователя от 19.10.2026 не закреплять строки в Excel-таблицах. Это общее правило для всех XLSX проекта, включая quests, actions, resources, интерактивные объекты, FunCollection и технические квесты.
- Прежние требования `freeze_panes=A4`, `A22`, `A76` отменены. При дальнейшей генерации не задавать закрепление строк.
- 20.10.2026 правило внедрено в код: общий XLSX writer и дополнительные генераторы создают листы с `freeze_panes=None`; split старого master не переносит его закрепление в новые conf. Проверки Stage 6 требуют отсутствие закрепления во всех новых XLSX. Существующие ручные файлы не пересохранять только ради этого правила без отдельного поручения.

## Главные источники правды

Для **VelesNight_2026** пользователь вручную правит XLSX в `D:/domovoy/trunk/data_ingenering/GD/Quests_Story/VelesNight_2026/` (подтверждено 20.10.2026). `campaigns/VelesNight_2026/pack_001/review/proto/` содержит синхронизированные копии. Перед разбором ручных правок читать рабочую папку пользователя и сверять копии; при расхождении не делать вывод о несохранённых правках только по репозиторию. Обе версии не пересобирать и не перезаписывать без поручения. Это уточнение имеет приоритет над общим описанием `review/` как единственного места ручного редактирования.

### Обязательный TXT для shop_invisible

По запросу пользователя от 20.10.2026 всегда создавать рядом с конечными таблицами `<campaign_id>_shop_invisible_packages.txt`. Это обязательное исключение из прежнего правила «только XLSX». Сверху две ссылки-пути: `d:\domovoy\trunk\server\prototypes\context_shop\` и `d:\domovoy\trunk\server\prototypes\context_shop\shop_invisible.proto.js`, затем пустая строка и все package текущей campaign по одной строке строго `"<classname>",`, включая запятую в последней строке. Брать определения из output семейства `/asset_package/` на листах `conf` текущих XLSX (ресурсы, quest interactive objects, FunCollection и другие таблицы), предпочитать ручной `classname`, убирать дубли. Donor input и простые упоминания package не включать. Сам `shop_invisible.proto.js` пользователь наполняет вручную; не изменять его по запросу на список. Генерация конечных XLSX через `export_xlsx.write_workbook` автоматически обновляет TXT; после ручных правок отдельно запускать `workflow_fast.py package-list --campaign <id> --pack <pack> --tables-dir <актуальная папка>`. Рабочую папку пользователя проверять прежде копий репозитория. Дополнительные manifest/ZIP/CSV/отчёты по-прежнему не создавать.

### Обязательный TXT для DayOfDomovoyCaldron

По запросу пользователя от 21.10.2026 всегда создавать рядом с конечными XLSX отдельный `<campaign_id>_DayOfDomovoyCaldron.txt`. В первой строке `d:\domovoy\trunk\server\prototypes\workbench\DayOfDomovoyCaldron.proto.js`, затем пустая строка и готовый объект для `extra.set` с завершающей запятой: `id=<campaign_id>`, `attention="Изготавливать можно"`, `title` из ручной Story-группы (при отсутствии — campaign_id), `icon=<campaign_id>_R_1`, `conditions="active_quest_group=<campaign_id>_Tech"`, `recipes` — **все** определения `/recipe/` из текущих XLSX, включая основные, MB, интерактивы и добавленные вручную рецепты. Не ограничивать список R_1..3/MB_1..3; не включать donor input и простые упоминания. Предпочитать явный `classname`, удалять дубли, сохранять естественный порядок номеров. Генератор `src/workbench_addition.py` автоматически вызывается общим conf writer; после ручных правок запускать `workflow_fast.py workbench-addition --campaign <id> --pack <pack> --tables-dir <актуальная папка>`. Допустимо прочитать старый ручной `Conf` для сбора списка, но это не подтверждает его совместимость с конвертером. Для VelesNight_2026 читать рабочую папку пользователя первой и сохранять TXT также в `review/proto`. Станок и ручные XLSX при этом не изменять. Этот TXT и список shop_invisible — два обязательных исключения из правила «только XLSX».

### Обязательные мистери-боксы и горшочки

По указанию пользователя от 20.10.2026 для каждого quest pack всегда создавать отдельный `MB_RECIPEMB_POTS_<campaign_id>.xlsx`, один `conf`: 3 мистери-бокса `<campaign_id>_R_MB_1..3`, 3 `R_MB_N_Recipe`, 3 наградных `<campaign_id>_Pot_Multi_Magic_1..3`. Образец — актуальная ручная таблица в рабочей папке VelesNight_2026. **У всех R_MB_N_Recipe брать ingredients точь-в-точь из первого `<campaign_id>_R_1_Recipe` текущих XLSX**, включая порядок и количества. Не копировать ingredients из Night_2026/старой campaign и не брать R_2/R_3 по номеру бокса. Если первого рецепта нет или источники конфликтуют — ошибка, ингредиенты не придумывать. Тестовые title разрешены, пользователь заменит вручную. Генератор `src/mystery_rewards.py` запускается Stage 6 перед технической очисткой; существующий ручной файл не пересобирать. Для адресной синхронизации только ингредиентов использовать `--update-ingredients`. При первичной генерации id пустые, без формул, каждый MB — отдельный ml; reward соответствующего MB содержит горшочек с тем же номером. Не удалять наградные горшки при on_spoil; временные MB включать в remove_asset. Подробности — `workflows/PROTO_EXPORT_WORKFLOW.md`.

- `workspace/active_context.json` - локальный, некоммитящийся контекст текущего пользователя: `mode`, `campaign_id`, `pack_id`, `stage`, `quest_number`, `task_number`.
- `campaigns/<campaign_id>/campaign_tone.md` - тон, стиль, запреты и словарь campaign. Если файла нет, уточнить у пользователя; ИИ пишет его сам только при явном разрешении пользователя.
- `campaigns/<campaign_id>/<pack_id>/` - постоянные артефакты конкретного pack.
- `data/quest_ready_index.json` и `data/quest_ready_drops.index.json` - единственные игровые индексы для генерации quest/task data.
- `raw/` - исходные игровые данные. Никогда не редактировать.
- `workflows/WORKFLOW_GUIDE.md` - порядок работы по этапам 1-6.
- `workflows/PROTO_EXPORT_WORKFLOW.md` - обязательный контракт XLSX/conf, реальные ограничения конвертера и regression-проверки Stage 6/FunCollection.
- `workflows/POT_DESCRIPTION_WORKFLOW.md` - workflow описания горшков по картинке.
- `workflows/RESOURCE_TABLE_WORKFLOW.md` - workflow XLSX/conf таблицы ресурсов для дева.
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

### Обязательный подэтап 6.1 Диалоги

После ручной проверки основных XLSX подключать диалоги через `quest-dialog-proto` и `workflow_fast.py dialogs`; единый контракт — `workflows/DIALOGUE_WORKFLOW.md`. Реестр `dialogue_characters.json` хранится на уровне campaign, `dialogue_plan.json` — в pack. По умолчанию один разговор первым таском первого квеста и по одному последним таском каждого квеста, без ограничений порядка выполнения; у экшенов только `active_quest`. Существующие ручные XLSX не регенерировать. `helper` — графический класс из реестра; физические ссылки `icon/go_to_location/behaviour` используют игровой classname. Согласованные реплики показывать до сборки; спрашивать только недостающие данные.

### Соответствие GR-подсказок механике

Ошибка устранена 21.10.2026: нельзя соединять TT-013 («любой мусор в локации») с выпадением из конкретного `assets` вроде `RustyNail`. При выборе конкретного `garbage_classname` сборщик Stage 4 разрешает TT-013 в TT-015 (дома) или TT-014 (в гостях) по mode кандидата; в filled_tasks сохраняет исходный requested_task_template_id и фактические id/name/type шаблона. Явные amount/price из choices сохраняются. Текст для конкретного мусора единый: `Убирай Ржавый гвоздь в гостях, чтобы найти. Место поиска: Котельная.` Не подставлять title собираемого GR вместо названия мусора, не терять полный список мест, не использовать общий «Убирай мусор в локации…» при конкретном источнике. `hint` квеста и `description` GR строятся одним formatter `src/gr_sources.py`; описание не копирует устаревший hint. Настоящий TT-013 допускается только для выпадения без конкретных assets с явными location_tags.

Stage 6 и реальная converter-проверка пары quests/resources дополнительно сверяют тексты с фактическими `actions/assets/location_tags` текущего XLSX; несоответствие останавливает проверку. После ручных правок проверять `python src/gr_table_review.py <campaign_id> --tables-dir <актуальная папка>`. `--apply` адресно исправляет только hint/description и служебные подписи шаблонов, с резервной копией в output и reopen-проверкой; сохраняет ID, identifier, количества, механику выпадения, формулы и настройки ручных листов. В VelesNight_2026 подтверждены ручные источники: GR_1=YarnLump дома, GR_2=RustyNail в гостях, GR_3=Chips в гостях, GR_5=BigHome_Garbage_Nursery_Flags в гостях. При дальнейшей сверке исходить из актуальной рабочей папки, не откатывать mode по старым task_choices/context_pack/копиям репозитория.

### Назначение ID после ручной проверки

При первичной генерации proto `id` и `tasks.N.identifier` пустые. Если пользователь затем сообщает следующие свободные proto/task ID и просит их проставить, это отдельная разрешённая стадия: назначать их адресно в текущих ручных XLSX через `src/proto_ids.py`, без регенерации. Правила пустых ID ниже относятся к первичной генерации. Один уникальный output path получает один proto ID; повторные task-блоки не расходуют новый proto ID. Задачи идентифицируются парой `(quest output, tasks.N)` и получают уникальные `e...`. Имена самих квестов и ссылки не менять. Существующие назначенные ID сохранять, коллизии запрещать. Проверять полную поставку с `--assigned-ids`: обязательны все proto/task ID, уникальность между файлами и сохранение после реальной конвертации. Новый режим не является обходом проверки. Диапазоны не придумывать: использовать явно переданные пользователем стартовые значения, сообщать следующие свободные после текущего назначения.

Рабочий workflow создания pack утвержден пользователем и состоит из этапов 1-6:

1. Сюжетная структура pack.
2. Реплики начала/завершения.
3. План квестов и task templates.
3.1. Context pack для смыслового заполнения task choices.
4. `task_choices.json`, автоматическая сборка `filled_tasks.json`, validation и вывод пути к файлу для проверки.
5. Quest group для pack.
6. Конечные XLSX в `review/proto/`, по одному листу `conf` в каждом, и два обязательных TXT: все package для shop_invisible и дополнение ко всем рецептам DayOfDomovoyCaldron.

Правила:

- Выполнять только один этап за раз.
- При создании новой campaign не спрашивать `campaign_id`: придумать стабильный англоязычный id по теме пользователя, например `<Theme>_2026`.
- При создании нового pack не спрашивать `pack_id`: брать следующий номер по порядку через campaign metadata, начиная с `pack_001`.
- Перед Stage 1 новой campaign спросить пользователя, какие минимум 2 интерактивных объекта выбрать на всю campaign; `Chest_*_Home/Guest` и `HELP_*_Home/Guest` считаются одним объектом.
- В той же анкете спросить сущность выбранных объектов и ресурсов; если пользователь оставляет выбор за ИИ, заполнять тематически по сути campaign.
- Выбранные интерактивные объекты фиксировать в `campaigns/<campaign_id>/interactive_objects.json`.
- Если пользователь выбирает несколько объектов одной механики, нумеровать их последовательно (`Chest_1`, `Chest_2`, `HELP_1`, `HELP_2`, `Exchanger_1`, `Exchanger_2`, `Story_FriendAction_1`, `Story_FriendAction_2`, `Mixer_1`, `Mixer_2`). В остальных случаях ресурсы выбранных объектов не менять на протяжении campaign.
- Для quest mixer использовать template `mixer_1` / `Story_Mixer`: читать `docs/QUEST_INTERACTIVE_OBJECT_TEMPLATES.md`; квестовая версия тратит `GR_1+GR_2+ASK_1` и сразу выдает готовый `{campaign_id}_Mixer_N_R_1`, без `MB` и без `CL`.
- Для `chest_1` использовать donors семейства `Fun12_FunCollection_1` для GR, R, package и global reward; Home/Guest берут donors `Dacha_2025` и обязательно получают `find=Dacha_2025`, `replace=<campaign_id>`. Все блоки используют `sl`, числовые поля пишутся числами, все `id` пустые; `Fun12` допустим только в donor `input`, но не в generated `output`.
- Для `story_random_recipe` использовать donor `/chest/Fun/Fun13/Fun13_Story_RandomRecipe_1.proto.js`; все пять блоков используют `sl`, числовые поля пишутся как числа, GR probability по умолчанию равна `35`, все `id` пустые. `rule_window` является видимым тематическим текстом для игрока, а не classname вида `RecipeRule_*_Window`; строки листа Stage 6 не закреплять.
- После каждого творческого этапа показывать результат пользователю и ждать явный approval.
- После Stage 3 в сводке по каждому квесту показывать не только `Task template ID`, но и `task_template_names` / русские названия шаблонов, например: `TT-001 Диалог / TT-008 Получить ASK / TT-004 HOG на локации`.
- Stage 3.1 - технический подготовительный шаг без отдельного approval; запускать после утвержденного stage 3 перед stage 4.
- Stage 5 нельзя собирать до approval stage 4.
- Stage 6 нельзя запускать до approval stage 5.
- Для листа `КВЕСТЫ` на Stage 6 использовать только проверенный donor `Night_2026`:
  - блок quest group: `ml`, поля `input/output/title/description/description_complete/description_spoil/id/find/replace`, `id` пустой, `find=Night_2026`, `replace=<campaign_id>`;
  - `input` quest group: `/quest_group/event/Night_2026/Night_2026_Story.proto.js`, `output`: `/quest_group/event/<campaign_id>/<campaign_id>_Story.proto.js`;
  - техническая группа: `/quest_group/event/<campaign_id>/<campaign_id>_Tech.proto.js`; группы также хранятся в своей папке campaign внутри `event`;
  - блок каждого quest: `sl`, те же служебные поля `id/find/replace`; `id` — пустая ячейка;
  - `input` quest N: `/quest/event/Night_2026/Night_2026_Story_N.proto.js`, `output`: `/quest/event/<campaign_id>/<campaign_id>_Story_N.proto.js`;
  - все квесты campaign, включая Tech_1/Tech_2, лежат непосредственно в `/quest/event/<campaign_id>/`; отдельные папки `story_1`, `story_2`, `tech` не создавать. `input/output` task-блоков совпадают с новым путём соответствующего квеста. Ручное исправление пользователя в `VelesNight_2026_quests.xlsx` от 20.10.2026 закреплено в генераторах; существующие XLSX не пересобирать;
  - блок каждого task: `ml`; его `input` и `output` оба равны новому output текущего quest, а не donor-пути `Night_2026`;
  - в quest group и quest не экспортировать старые `extra.*`; в листе `КВЕСТЫ` не использовать `temp`, `temp_01` или `temp_02`.
- Для `TT-033` classname предмета передачи строить как `<campaign_id>_Give_<character_number>_<give_number>`, например `MagicSchool_2026_Give_3_1`, а action как `<classname>_Give`. Не использовать глобальный `task_number` в classname Give.
- Для листа `ЭКШЕНЫ` на Stage 6:
  - использовать только `ml` для furniture/entity блоков и `sl` для action блоков; `temp*` не использовать;
  - `id` всех персонажей, квестов, quest group и action оставлять пустыми; ID не резервировать и не назначать;
  - для персонажей без экшенов использовать donor `/furniture/Fun/Fun13/Character/Fun13_Character_23.proto.js`, для персонажей с экшенами — `/furniture/Fun/Fun13/Character/Fun13_Character_18.proto.js`;
  - для Give использовать donor `/quest_action/Fun/Fun13/Fun13_Character_18_Give_1.proto.js`;
  - для `TT-033` identifier action строить от classname предмета `Give_*`, но записывать action в `behaviour.0.actions` персонажа-получателя, найденного по `person`/`hint`; не создавать furniture-сущность с classname предмета;
  - строки таблицы `ЭКШЕНЫ` / `<campaign_id>_actions.xlsx` не закреплять.
- Stage 6 обязательно собирает `review/proto/<campaign_id>_resources.xlsx` с единственным `conf`: ресурсы агрегируют все `pack_*` campaign по `docs/resource_table_template.csv`. CSV и экспортные summary JSON не создавать. `resource-table` по умолчанию также создаёт XLSX.
- Stage 6 всегда создает `review/proto/quest_<campaign_id>_accomplished.xlsx` с листом `conf` и одной строкой на каждый quest из `filled_tasks.json`. Использовать `sl`, donor `/post_action/quest_Night_2026_Story_1_accomplished.proto.js`, фиксированные тексты/награду из утвержденного шаблона, числовые `clicks_limit=5` и `life_time=43200`; `id` оставлять пустым.
- Stage 6 всегда создаёт отдельный `review/proto/<campaign_id>_technical_quests.xlsx`: техническую группу и Tech_1/Tech_2 из доноров Night_2026. Собирать после всех остальных XLSX, включая FunCollection, командой `src/technical_quest_tables.py`. `on_spoil` Tech_2 перечисляет все собственные ресурсы (`remove_asset`, ключ `classname`) и объекты (`remove_stuff`, ключ `classname`) из текущих ручных XLSX всех pack campaign, включая персонажей с эмоциями, HOG, интерактивы, их ресурсы и все состояния/эффекты потех. Общие игровые ингредиенты и служебные prototype definitions не удалять. Срок `spoil_conditions` вынести явно; без указанного срока оставить пустым с комментарием о необходимости заполнить до импорта, не копировать старую дату. Подробности: `workflows/PROTO_EXPORT_WORKFLOW.md`.
- В первичных таблицах все `tasks.N.identifier` оставлять пустыми: пользователь назначит уникальные identifier задач после проверки, как и id. Имена прототипов (`<campaign_id>_Tech_1` и т.п.) заполняются сразу; их пользователь не просил обнулять. Ручные значения после назначения не стирать пересборкой.
- В `review/proto/<campaign_id>_actions.xlsx` создавать и персонажей без экшенов: отдельный блок с заголовком `ПЕРСОНАЖИ БЕЗ ЭКШЕНОВ`, строки персонажей без параметра `behaviour.0.actions`.
- Approval записывать только через `python src/workflow_fast.py approve ...`. Прямой `src/workflow_context.py approve` запрещен, потому что он не применяет review и не пересобирает производные артефакты.
- На Stage 3 task templates `TT-008` (`get_asset ASK`) и `TT-009` (`get_asset PER`) использовать только внутри квестов, где в этом же квесте есть `TT-002` (`get_and_decrease_asset craft`) или `TT-033` (`action give`). В обычных поисковых/сюжетных квестах без craft/give не ставить ASK/PER.
- На Stage 3 любой HOG template (`TT-003`-`TT-007`) нельзя ставить в квест, если в предыдущем квесте в любом task уже был HOG.
- В крафтовых квестах чередовать `ASK` и `PER` между собой: если предыдущий крафтовый квест использовал `ASK`, следующий крафтовый должен использовать `PER`, и наоборот.
- После каждого этапа (1-6) обязательно генерировать review-документ командой `python src/workflow_fast.py review --campaign <campaign_id> --pack <pack_id> --stage <N>`. Review-файлы сохраняются в `campaigns/<campaign_id>/<pack_id>/review/stageN_review.md` (для Stage 6 проверяется комплект конечных XLSX в `review/proto/`, отдельный обзор не создаётся). Review генерируется всегда, до approval, чтобы пользователь мог проверить результат.
- `review/` — единственное место, где человек вручную правит quest pack: Stage 1-5 правятся в `stageN_review.md`, Stage 6 — только в `review/proto/*.xlsx`. Эти XLSX — актуальная ручная версия; не пересобирать её без явного указания пользователя. Старый `stage6_review.xlsx` не является источником актуальных правок после перехода на conf. `stage1_story.txt`, `stage2_story.txt`, `stage3_quests.txt`, `task_choices.json`, `quest_group_choices.json` и остальные файлы pack являются машинными артефактами и вручную человеком не редактируются.
- Команды `stage3`, `fill`, `quest-group` и `stage6` создают review автоматически. Для Stage 1-2, у которых нет отдельного build-wrapper, review обязательно создать явной командой `workflow_fast.py review` до approval.
- Approval Stage 1-5 запрещен, если соответствующий review отсутствует или пуст. Перед записью approval review автоматически применяется к машинному source, а Stage 3-5 заново собираются и валидируются.
- Approval хранит SHA-256 соответствующего review. Любая правка review после approval аннулирует gate до повторного `workflow_fast.py approve`.
- Approval записывается строго по порядку Stage 1 → 2 → 3 → 4 → 5; следующий этап нельзя утвердить, пока отсутствует или устарел любой предыдущий gate.
- Существующий review по умолчанию не перезаписывать: это защита ручных правок. Осознанная регенерация текстового review требует `review --force`, перезапись `stage6_review.xlsx` — `stage6 --force-review`.
- Stage 6 запрещен без полного семантически непустого комплекта `stage1_review.md`-`stage5_review.md` и без действующей цепочки approval Stage 1-5 с неизмененными review.
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
- собирать XLSX командой `python src/workflow_fast.py resource-table --campaign <campaign_id> --pack <pack_id>`; низкоуровневый старый CSV CLI не запускать по умолчанию;
- по умолчанию читать все pack из `campaigns/<campaign_id>/pack_*`;
- один pack использовать только если пользователь явно попросил фильтр по pack;
- создавать только блоки, для которых есть ресурсы в выбранной campaign или явно выбранных pack;
- сохранять минимум одну пустую строку между блоками;
- не использовать `Fun12`, если текущий prefix другой;
- во всех строках типов ресурсов использовать `sl`; `temp`, `temp_01`, `temp_02` запрещены;
- `id` оставлять пустым во всех ресурсных блоках;
- значения полей с типом `int` писать как числа, а не как текстовые строки;
- строки таблицы `РЕСУРСЫ` / `<campaign_id>_resources.xlsx` не закреплять.
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

Stage 6 берёт `filled_tasks.json` и `quest_group.json` из pack. Вся конечная выдача располагается в одной папке:

```text
campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_quests.xlsx
campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_actions.xlsx
campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_resources.xlsx
campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_interactive_<mechanic>.xlsx
campaigns/<campaign_id>/<pack_id>/review/proto/quest_<campaign_id>_accomplished.xlsx
campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_technical_quests.xlsx
campaigns/<campaign_id>/<pack_id>/review/proto/<campaign_id>_funcollection_4.xlsx (если выбран FunCollection_4)
```

В каждом XLSX ровно один лист `conf`. Не создавать CSV, ZIP, `bundle_manifest.json`, `manifest.json`, `validation_report.json`, экспортные summary JSON и дополнительный многолистовой обзор. Проверки остаются обязательными, результат — в консоли. Только действительно необходимые источники, validation gates Stage 1–5 и campaign memory остаются внутренними JSON вне `review/proto/`.

## Роли ИИ И Кода

- ИИ отвечает за творческие решения: сюжет, реплики, выбор task types, смысловые `task_choices` по контексту, загадки, `choice_reason`, тексты quest group.
- Код отвечает за guardrails: parsing, context pack, сборку strict `filled_tasks.json` из `task_choices.json`, validation, approval gates, XLSX/conf export, actions export, обязательную агрегацию ресурсов Stage 6, campaign memory.
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

- Stage 6 сразу создаёт конечные conf-файлы без промежуточного workbook. `stage6-split` оставлен только для миграции старого обзора; не запускать его поверх актуальных ручных conf-правок. Существующие XLSX защищены до намеренного `--force`.
- Для generated-нумерации текущего pack учитывать только предыдущие pack-и campaign. Более поздние pack-и не должны создавать ошибки validation для раннего pack.

## Обязательная Проверка Прототипных Таблиц

- Перед поставкой прочитать `workflows/PROTO_EXPORT_WORKFLOW.md` и применить `proto`.
- Допустимы только `sl`/`ml`; `ml` — один прототип на блок; `sl` с `replace` — также один прототип на блок из-за сброса замен в реальном конвертере.
- Объединения `object`/`replace`, настоящие пустые клетки, числовые `int`, отсутствие duplicate keys и корректные индексы массивов проверяет `src/converter_tables.py`. Обходить эти ошибки ручной правкой только готового файла запрещено.
- Использовать `src/validate_proto_exports.py`: реальный конвертер, реальные доноры, изолированный output, проверка количества прототипов и сохранённых значений. Успешный exit code без проверки JSON недостаточен.
- Учесть выбранные потехи из `fun_interactive_objects.selection.json` отдельно от quest objects. Для FunCollection_4 popup и description_window — разные поля; INVITE-состояния не должны переименовывать GR/CL.
- Пустой `id` в таблице наследует donor ID при конвертации. Производственные IDs назначает разработчик отдельно; не объявлять такую выгрузку готовой к импорту в игру только на основании dry run.

### Adventure: подтверждённые правки дева 19.10.2026

Для Adventure читать `.agents/skills/proto/references/adventure-template.md`. Ручной эталон — `D:/domovoy/trunk/data_ingenering/GD/Adventure/Adventure_4_2_pack_tables/`. Вынести `tasks.0.identifier` и `tasks.0.title` у всех не-наградных QuestPrototype, включая root/restarter/tech и trophy; полный pack содержит 17 задач. Существующие ручные ID сохранять. Сначала создать rewards quest из донора, затем во всех его task-блоках читать и писать новый quest path. Уже созданные `Adventure_GR_4` (`quest_item.xlsx`) и `Adventure_4_Box_1` повторно не поставлять; reward-ссылки на Box_1 сохранять. Окна — FairyTale из эталонного `quest_group.xlsx`; текст правил сохранять. Каждый mystery box — отдельный `ml`, каждый restarter с `replace` — отдельный блок. В trophy заменять pet classname, чтобы обновлялись также task param и conditions. Генератор — `tools/build_adventure_pack_from_brief.py`, адресное применение к ручным XLSX с резервированием и реальной конвертацией — `tools/apply_adventure_developer_review.py`. Эти правила относятся к Adventure и не меняют donors/окна обычного quest workflow.

## Полировка Пайплайна И Будущий Скилл Квестов

Согласовано пользователем 19.10.2026: сначала он проверяет и вручную правит все конечные XLSX в `review/proto/`. По его сообщению о завершении правок ИИ читает именно эти файлы, фиксирует подтверждённые исправления в соответствующем генераторе/машинном шаблоне/документации, добавляет необходимые regression checks и повторяет проверку конвертером. Ручной эталон не заменять регенерацией во время этой работы. Только после проверки таблиц и закрепления исправлений оформлять корректный скилл создания квеста. Полировать постепенно, по фактически найденным ошибкам; не объявлять скилл финальным заранее.

## Имена Конечных Таблиц

Каждый файл XLSX в `campaigns/<campaign_id>/<pack_id>/review/proto/` обязан содержать точный prefix текущей campaign в имени. По умолчанию добавлять `<campaign_id>_` перед названием таблицы: `VelesNight_2026_quests.xlsx`, `VelesNight_2026_actions.xlsx`, `VelesNight_2026_resources.xlsx`, `VelesNight_2026_interactive_chest.xlsx`, `VelesNight_2026_funcollection_4.xlsx`. Если prefix уже есть, не дублировать: `quest_VelesNight_2026_accomplished.xlsx` уже соответствует правилу. Это относится к Stage 6, отдельной сборке ресурсов, интерактивным объектам, потехам и миграции старого обзора. Переименование не должно пересобирать или менять содержимое ручных XLSX.

## Generated Character, Output И Пустые ID

Исправлено по ревью пользователя 19.10.2026:

- Выходные пути generated `furniture` и `quest_action` строятся прямо под campaign, без `/Fun/`: `/furniture/<campaign_id>/Character/<campaign_id>_Character_1_1.proto.js`, `/quest_action/<campaign_id>/search_<campaign_id>_HOG_1.proto.js`. Донорские `input` не менять: их реальная `/Fun/Fun13/` структура сохраняется.
- Каждый generated character имеет два числовых компонента: `<campaign_id>_Character_<character_number>_<emotion_number>`. Если эмоция не задана, использовать `1`: `VelesNight_2026_Character_1_1`. Явно выбранную эмоцию сохранять.
- Новое имя персонажа согласовать во всех физических ссылках: classname, output, icon, param, action и go_to_location, включая JSON внутри ячейки. `helper` квеста и `view_class` диалога брать из графического класса в `dialogue_characters.json`. Для Give первый номер берётся из номера персонажа, а не эмоции.
- `id` во всех конечных таблицах всегда оставлять настоящей пустой клеткой (`None`), включая quest group, quests, персонажей и actions. Не выделять диапазоны, не копировать ID донора в таблицу, не сохранять переданные reference IDs и не писать 0/пустую строковую формулу. Старые правила 125xxx отменены.
- Исправления текущего review вносить адресно, сохраняя остальные ручные значения и оформление; затем закрепить поведение в генераторах и проверках.
