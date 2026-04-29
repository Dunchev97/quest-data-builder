# Resource Table Workflow

Workflow для подготовки CSV-таблицы ресурсов по всей campaign: по всем pack внутри `campaigns/<campaign_id>/`.

## Когда Включать

Переключай active context в `resource_table`, если пользователь просит:

- собрать таблицу ресурсов;
- сделать CSV ресурсов для дева;
- подготовить `*_Res.csv`;
- собрать описания всех ресурсов из campaign.

Команда для фиксации режима:

```bash
python src/workflow_context.py detect --text "<запрос пользователя>" --apply
```

Команда сборки:

```bash
python src/build_resource_table.py <campaign_id>
```

`workspace/active_context.json` локальный и не коммитится.

## Вход

Основной сценарий - читать все pack внутри campaign:

```text
campaigns/<campaign_id>/pack_*/
```

В каждом pack использовать:

- `filled_tasks.json`;
- `context_pack.json`;
- `quest_plan.resolved.json`.

Один pack или список pack можно использовать только как явный ручной фильтр, если пользователь отдельно попросил собрать таблицу не по всей campaign.

Пример формата-донора:

```text
C:/Users/user/Downloads/Fun12_Res.csv
```

Файл-донор использует `;` как CSV-разделитель и блочную структуру.

## Выход

Основной выход для всей campaign:

```text
campaigns/<campaign_id>/resource_table.csv
campaigns/<campaign_id>/resource_table.summary.json
```

Если пользователь явно попросил только один pack:

```text
campaigns/<campaign_id>/<pack_id>/resource_table.csv
```

CSV должен сохранять блочный формат:

1. строка названия блока;
2. строка типов;
3. строка заголовков;
4. строки данных;
5. минимум одна пустая строка между блоками.

Точное количество пустых строк из примера повторять не нужно. Один пустой разделитель между блоками обязателен.

## Prefix

`Fun12` в примере - это prefix конкретного event. Для текущего workflow использовать фактический prefix из созданных classnames.

Пример:

```text
CucumberFestival_2026_GR_1
CucumberFestival_2026_ASK_1
CucumberFestival_2026_R_1
```

Не заменять его на `Fun12`.

## Какие Блоки Создавать

Создавать только блоки, для которых есть ресурсы в выбранных pack.

Порядок блоков, если они нужны:

1. `HOG`
2. `GR ассет`
3. `GR способы получения`
4. `GR ПАКЕТЫ`
5. `ASK`
6. `ASK пост экшен`
7. `ASK ПАКЕТЫ`
8. `PER`
9. `PER пост экшен`
10. `PER ПАКЕТЫ`
11. `FG АССЕТ`
12. `FG МЕХАНИКА`
13. `FG ПАКЕТЫ`
14. `R ассет`
15. `Рецепты 4 ингридиента`
16. `FA ассет`
17. `FA Пакеты`

Шаблон блоков лежит в:

```text
docs/resource_table_template.csv
```

## Общие Правила Полей

- `view_classname` для новых generated-ресурсов заполнять тем же значением, что и `classname`, если пользователь явно не дал другой визуал.
- `id` оставлять пустым.
- `output` строить с текущим prefix и classname.
- `title` брать из task object, убирая служебные глаголы: `Попроси у друзей`, `Получи`, `Создай`, `Найди`.
- Если title нельзя надежно извлечь, оставить как в task object и отметить в preview.
- Финальный CSV для передачи деву должен быть с разделителем `;`. Пример `Fun12_Res.csv` прочитан как `cp1251`; при автоматическом экспорте сохранять `cp1251`, если downstream-скрипт не требует другое. Шаблон `docs/resource_table_template.csv` тоже хранится в `cp1251`, чтобы нормально открываться в табличном редакторе без каши в кириллице.

## Path Templates

`input` - proto-донор из примера. `output` - новый proto текущего prefix.

Для первого прототипа использовать такие шаблоны:

| Блок | input | output |
| --- | --- | --- |
| `HOG` | `/debris/Dacha_2025/Dacha_2025_HOG_1.proto.js` | `/debris/<prefix>/<classname>.proto.js` |
| `GR ассет` | `/quest_item/Fun/Fun11/resource/Fun11_GR_1.proto.js` | `/quest_item/<prefix>/<classname>.proto.js` |
| `GR способы получения` | donor по action из примера `Fun12_Res.csv` | `/global_reward/<prefix>/<classname>.proto.js` |
| `GR ПАКЕТЫ` | `/asset_package/Fun/Fun10/resource/Fun10_GR_10_Package.proto.js` | `/asset_package/Fun/<prefix>/<classname>.proto.js` |
| `ASK` | `/quest_item/Fun/Fun10/resource/Fun10_ASK_1.proto.js` | `/quest_item/<prefix>/<classname>.proto.js` |
| `ASK пост экшен` | `/post_action/ask_for_Fun10_ASK_10.proto.js` | `/post_action/ask_for_<classname>.proto.js` |
| `ASK ПАКЕТЫ` | `/asset_package/Fun/Fun10/resource/Fun10_ASK_1_Package.proto.js` | `/asset_package/Fun/<prefix>/<classname>.proto.js` |
| `PER` | `/quest_item/Fun/Fun10/resource/Fun10_PER_1.proto.js` | `/quest_item/<prefix>/<classname>.proto.js` |
| `PER пост экшен` | `/post_action/ask_for_Fun10_PER_1.proto.js` | `/post_action/ask_for_<classname>.proto.js` |
| `PER ПАКЕТЫ` | `/asset_package/Fun/Fun10/resource/Fun10_PER_1_Package.proto.js` | `/asset_package/Fun/<prefix>/<classname>.proto.js` |
| `FG АССЕТ` | `/quest_item/Fun/Fun10/resource/Fun10_FG_1.proto.js` | `/quest_item/Fun/<prefix>/resource/<classname>.proto.js` |
| `FG МЕХАНИКА` | `/free_gift/Fun/Fun10/Fun10_FG_1.proto.js` | `/free_gift/<classname>.proto.js` |
| `FG ПАКЕТЫ` | `/asset_package/Fun/Fun10/resource/Fun10_FG_1_Package.proto.js` | `/asset_package/Fun/<prefix>/<classname>.proto.js` |
| `R ассет` | `/quest_item/Fun/Fun11/repair/Fun11_R_1.proto.js` | `/quest_item/<prefix>/<classname>.proto.js` |
| `Рецепты 4 ингридиента` | `/recipe/Dacha_2025/Dacha_2025_R_1_Recipe.proto.js` | `/recipe/<prefix>/<identifier>.proto.js` |
| `FA ассет` | `/quest_item/Fun/Fun11/repair/Fun11_R_1.proto.js` | `/quest_item/<prefix>/<classname>.proto.js` |
| `FA Пакеты` | `/asset_package/Fun/Fun10/resource/Fun10_FG_1_Package.proto.js` | `/asset_package/Fun/<prefix>/<classname>.proto.js` |

## Asset Blocks

### GR Ассет

Источник: task object с classname вида `*_GR_<n>`.

Поля:

- `classname`: generated classname.
- `view_classname`: тот же classname.
- `title`: название ресурса.
- `description`: описание способа получения из hint/task type.
- `meta_info`: `pack_asset=<classname>_Package`.

Описание:

- мусор дома: `Убирай мусор <мусор> дома, чтобы найти. Место поиска: <локации>.`
- мусор в гостях: `Убирай мусор <мусор> в гостях, чтобы найти. Место поиска: <локации>.`
- цветы в гостях: `Собирай цветы <цветок> в гостях, чтобы найти. Чтобы собрать растение, кликни на горшок с нужным растением в гостях у друга.`
- если source только location, без конкретного мусора: `Убирай мусор в <локация> дома/в гостях, чтобы найти.`

### ASK Ассет

Источник: task object с classname вида `*_ASK_<n>`.

Описание строго:

```text
Попроси у друзей или купи.
```

`meta_info`: `pack_asset=<classname>_Package`.

### PER Ассет

Источник: task object с classname вида `*_PER_<n>`.

Описание строго:

```text
Отправь личные просьбы друзьям или купи.
```

`meta_info`: `pack_asset=<classname>_Package`.

### FG Ассет

Создавать только если в pack есть FG-ресурсы.

Описание строго:

```text
Получи в качестве бесплатного подарка от друзей или купи.
```

`meta_info`: `pack_asset=<classname>_Package`.

### FA Ассет

Создавать только если в pack есть FA-ресурсы.

`meta_info`: `pack_asset=<classname>_Package`.

### R Ассет

Источник: craft task object с classname вида `*_R_<n>`.

Описание брать из hint craft task, обычно:

```text
Для создания используй Станок.
```

`tags.0`: текущий prefix, например `CucumberFestival_2026`.

## Способы Получения GR

Для каждого GR создать строку в блоке `GR способы получения`.

`conditions`:

```text
active_quest=<classname_quests>
```

`classname_quests` - story quest, где ресурс впервые нужен, например:

```text
CucumberFestival_2026_Story_2
```

`actions`:

- `clean_garbage` - мусор дома;
- `clean_garbage_in_guest` - мусор в гостях;
- `take_crop_in_guest` - цветы в гостях.

`rand_reward.asset`:

```text
<GR_classname>
```

`assets` заполнять конкретным source asset, если он есть: garbage classname, flower classname, multi flower classname.

`location_tags` заполнять location tag, если источник задан через location.

Default `rand_reward.p` по примеру:

- `take_crop_in_guest`: `30`;
- `clean_garbage` по location: `40`;
- `clean_garbage_in_guest` по location: `50`;
- `clean_garbage` по конкретному garbage: `60`;
- `clean_garbage_in_guest` по конкретному garbage: `40`.

## Post Action Blocks

Для каждого ASK/PER создать строку в соответствующем блоке пост экшена.

Поля:

- `identifier`: `ask_for_<classname>`;
- `classname`: `<classname>`;
- `title`: название ресурса;
- `poster_reward`: `asset=<classname>:1`;
- `clicks_limit`: `5`;
- `life_time`: `43200`;
- `send_interval`: `7200`.

## Package Blocks

Для каждого покупаемого ресурса создать package.

Общие поля:

- `classname`: `<asset_classname>_Package`;
- `asset`: `<asset_classname>`;
- `title`: название ресурса;
- `reward`: `asset=<asset_classname>:<amount>`;
- `stuff_icon`: `<asset_classname>`;
- `id`: пусто.

Amounts и prices:

- ASK: `reward=asset=<classname>:1`, `Количество ассетов=1`, `price=2`;
- PER: `reward=asset=<classname>:1`, `Количество ассетов=1`, `price=2`;
- FG: `reward=asset=<classname>:10`, `Количество ассетов=10`, `price=2`;
- FA: `reward=asset=<classname>:2`, `Количество ассетов=2`, `price=3`;
- GR: для прототипа `reward=asset=<classname>:1`, `Количество ассетов=1`, `price=1`.

## Recipes

Для каждого craft/R создать строку в блоке `Рецепты 4 ингридиента`.

Поля:

- `identifier`: `<R_classname>_Recipe`;
- `lifespan`: `2400`;
- `tags`: текущий prefix;
- `conditions`: `active_quest=<classname_quests>+asset!=<R_classname>:1`;
- `reward`: `asset=<R_classname>:1`.

Ингредиенты:

1. Найти соседние resource tasks в том же quest рядом с craft task.
2. Взять первый и второй ингредиент из этих task.
3. Количество взять из `task_object.amount`.
4. Для прототипа 3-й ингредиент = копия 1-го, 4-й ингредиент = копия 2-го.

Пример:

```text
ingredient_1_asset=CucumberFestival_2026_ASK_1
ingredient_1_asset_amount=1
ingredient_2_asset=CucumberFestival_2026_GR_1
ingredient_2_asset_amount=1
ingredient_3_asset=CucumberFestival_2026_ASK_1
ingredient_3_asset_amount=1
ingredient_4_asset=CucumberFestival_2026_GR_1
ingredient_4_asset_amount=1
ingredients=asset=CucumberFestival_2026_ASK_1:1+asset=CucumberFestival_2026_GR_1:1+asset=CucumberFestival_2026_ASK_1:1+asset=CucumberFestival_2026_GR_1:1
```

Не создавать `CL`, `Exchanger`, `Story_HELP_Opener` и другие сложные ингредиенты на этом этапе.

## Валидация Перед Выдачей

Проверить:

- блоки идут в правильном порядке;
- есть минимум одна пустая строка между блоками;
- у всех generated ресурсов prefix текущей campaign;
- нет `Fun12`, если это не текущий prefix;
- `view_classname == classname` для generated ресурсов;
- ASK/PER/FG descriptions строго совпадают с шаблонами;
- package amounts/prices соответствуют правилам;
- recipe conditions имеют `+` между условиями;
- recipe ingredients содержат 4 ингредиента;
- `id` пустой во всех строках.
