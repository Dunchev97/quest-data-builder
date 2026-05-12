# Fun Interactive Object Workflow

Workflow для шаблонов потешных интерактивных объектов `FunCollection_*` и отдельного `Workbench`.

## Когда Использовать

Использовать этот workflow, если пользователь просит:

- собрать новые интерактивные объекты для потех;
- сделать `FunCollection_*` по теме;
- подготовить CSV-шаблон, похожий на доноры `Fun12_FunCollection_*.xlsx`;
- подготовить новый `Workbench`.

Не использовать этот workflow для quest interactive objects из `campaigns/<campaign_id>/interactive_objects.json`. Те объекты участвуют в quest craft-рецептах и собираются через `src/interactive_objects.py`.

## Источник Шаблонов

Машинная карта шаблонов:

```text
data/fun_interactive_object_templates.json
```

Доноры, по которым снята структура:

```text
C:/Users/user/Downloads/Fun12_FunCollection_1.xlsx
C:/Users/user/Downloads/FunCollection_2.xlsx
C:/Users/user/Downloads/Fun12_FunCollection_3.xlsx
C:/Users/user/Downloads/Fun12_FunCollection_4.xlsx
C:/Users/user/Downloads/Fun12_FunCollection_5.xlsx
C:/Users/user/Downloads/FunCollection_6.xlsx
C:/Users/user/Downloads/FunCollection_9.xlsx
C:/Users/user/Downloads/Fun12_Workbench.xlsx
```

## Общие Правила

- `prefix` брать текущий, например `Fun13`; не оставлять `Fun12`, если это не donor/input path.
- `input` оставлять донорским path из примера.
- `output`, `classname`, `file_name`, `identifier`, `asset`, `stuff_icon`, `rand_reward.asset`, `pack_asset` строить с текущим `prefix`.
- `id` оставлять пустым, если пользователь не дал конкретный id.
- `collection_rewards` всегда содержит 10 CL-наград.
- Тексты писать в стиле Домовят: тепло, предметно, без формального "необходимо/требуется".
- Интерактивные объекты для потех не включать в quest workflow и не записывать в campaign-level `interactive_objects.json`.
- Workbench не считать потешной FunCollection-механикой: у него отдельный шаблон `workbench_single`.

## Как Заполнять По Теме

1. Определить `prefix`, `collection_number`, `source_prefix`, `tech_quest`.
2. Выбрать template id из JSON.
3. Заполнить `required_theme_fields`.
4. Для падежей явно написать отдельные значения там, где шаблон просит `*_accusative`, `*_genitive`, `*_instrumental`.
5. Сверить все classnames по `classname_patterns`.
6. Развернуть `repeat`-строки: `collection_rewards[1..10]`, negative effects или resource package rows.
7. Сохранить CSV с `;` и `cp1251`, если downstream ожидает Excel-friendly файл.

Если пользователь дает точный ID объекта, например `FunCollection_9`, выбирать template с exact `id` из `data/fun_interactive_object_templates.json`. В таком случае не заменять его на похожий абстрактный template, даже если механика похожа на другой объект.

## Шаблоны

### `fun_collection_chest_home_guest`

Донор: `Fun12_FunCollection_1.xlsx`.

Механика: Home/Guest chest открывается одним GR-ресурсом и выдает одну из 10 CL-наград.

Ключевые поля:

- `object_title`: объект, по которому кликают дома и в гостях.
- `activation_resource_title`: ресурс для открытия.
- `reward_group_title`: общее имя набора из 10 CL-наград.
- `location_tag`: где добывается GR.
- `tech_quest_home` и `tech_quest_guest`: условия активности.

Блоки:

- `Ресурсы FunCollection_<n>`: 1 GR + 10 CL.
- `Способ получения GR`: global_reward для GR.
- `FunCollection_<n>_Guest`.
- `FunCollection_<n>_Home`.
- `Пакеты продажи ресурсов FunCollection_<n>`.

### `fun_collection_prediction_chest`

Донор: `Fun12_FunCollection_3.xlsx`.

Механика: одиночный платный chest/предсказатель с 10 CL-наградами и `reward_time_interval`.

Ключевые поля:

- `object_title`: персонаж или объект.
- `collection_rewards`: 10 CL-наград.
- `window_description`: текст окна, объясняющий случайную награду.
- `use_for_money_price`, `reward_time_interval`: можно оставить default из JSON.

Блоки:

- `Ресурсы FunCollection_<n>`: 10 CL.
- `FunCollection_<n>`: один chest-объект.

### `fun_collection_state_feeder`

Донор: `Fun12_FunCollection_4.xlsx`.

Механика: нейтральный объект, который после кормления/использования ресурса превращается в хорошее или плохое состояние. Хорошее состояние дает одну из 10 CL-наград, плохое состояние может включать негативные эффекты.

Ключевые поля:

- `neutral_title`, `good_state_title`, `bad_state_title`.
- `feeding_resource_title`.
- `reward_owner_name`: от кого получает игрок CL-награды.
- `negative_effect_titles`: названия эффектов по suffix.
- `location_tag`, `tech_quest`.

Блоки:

- `Нейтральное состояние FunCollection_<n>`.
- `Хорошее состояние FunCollection_<n>`.
- `Плохое состояние FunCollection_<n>`.
- `Ресурсы FunCollection_<n>`: 1 GR + 10 CL.
- `Пакеты ресурсов FunCollection_<n>`.
- `Способы получения ресурсов FunCollection_<n>`.
- `Негативные эффекты FunCollection_<n>`.

### `fun_collection_friend_contribution`

Донор: `Fun12_FunCollection_5.xlsx`.

Механика: игрок добывает ресурс анлока, друг добывает ресурс дарения и вкладывает его в Guest-объект; вклад превращается в ресурс подарка/результата. `Unlock` не выдает CL-награды сам: загрузка `Unlock` ресурсами разрешает пользоваться объектом, открыть его окно и дальше тратить подарки от друзей на коллекционный ресурс.

Ключевые поля:

- `object_title`: общий объект Home/Guest/Unlock.
- `unlock_resource_title`: ресурс для подношения/анлока.
- `gift_resource_title`: ресурс, который друг вкладывает.
- `contribution_result_title`: ресурс, полученный из вклада друга.
- `collection_rewards`: 10 CL-наград.
- `unlock_source_action`, `gift_source_action`, `unlock_location_tag`, `gift_location_tag`.

Блоки:

- `Ресурсы FunCollection_<n>`: 10 CL + result GR + unlock GR.
- `Ресурс дарения FunCollection_<n>`.
- `Способ получения ресурса анлока FunCollection_<n>`.
- `Способ получения ресурса дарения FunCollection_<n>`.
- `Пакеты продажи ресурсов FunCollection_<n>`.
- `Пост экшен FunCollection_<n>`.
- `FunCollection_<n>_Guest`.
- `FunCollection_<n>_Unlock`: gate/разблокировка использования объекта, а не источник наград.
- `FunCollection_<n>_Home`: окно, где игрок тратит результат помощи друзей на коллекционный ресурс.

Важно: donor row для `FunCollection_5_Guest.behaviour.0.lock.availability_conditions` содержит `source_prefix` в условии. Перед выдачей dev-ready CSV нужно уточнить или проверить, должен ли этот condition тоже перейти на текущий `prefix`.

### `fun_collection_story_help_groups`

База: `data/interactive_object_templates.json#help_1`.

Старый источник информации: `C:/Users/user/Downloads/FunCollection_2.xlsx`.

Механика: актуальный `help_1` / `Story_HELP`-объект, расширенный до 10 Home/Guest пар и 10 групповых `CL`-ресурсов. Игроки делятся по последней цифре ID: группы 1-9 получают `multiplicity=1..9`, группа 10 получает `multiplicity=0`.

Ключевые поля:

- `object_title`: общий объект Home/Guest, например `Старинные часы`.
- `path_resource_title`: ресурс помощи, который приходит через взаимодействие друзей, например `Часовая шестирёнка`.
- `result_resource_title`: основной ресурс объекта, который собирается из помощи, например `Жетон времени`.
- `collection_rewards`: 10 цветовых/групповых ресурсов, например `Желтая батарейка`, `Красная батарейка` и так далее.
- `location_tag`, `source_action`, `tech_quest`: способ выпадения группового `CL`.

Блоки:

- `FunCollection_<n>_Home x10`: 10 chest-объектов по форме `help_1`, каждый тратит свой `CL_i` в `open_price`.
- `FunCollection_<n>_Guest x10`: 10 furniture-объектов по форме `help_1`, каждый указывает на свой `Home_i`.
- `HELP resources`: общие `HELP_OpenerPath` и `HELP_Opener`.
- `Collection reward assets x10`: 10 `CL_i` ресурсов.
- `Collection reward global_rewards x10`: 10 способов выпадения с `active_quest=<tech_quest>+multiplicity=<digit>`.
- `Packages`: 10 пакетов `CL_i` + пакеты для `HELP_OpenerPath` и `HELP_Opener`.
- `HELP_Opener recipe`: рецепт `HELP_Opener` из `HELP_OpenerPath`.

Правила:

- `input` брать из `Fun11`: `/.../Fun11/...`.
- `output` строить с целевым prefix, например `/.../Fun13/...`.
- Для `CL_10` использовать `multiplicity=0`, потому что это последняя цифра ID `0`.
- Не добавлять этот объект в `campaigns/<campaign_id>/interactive_objects.json`: это potekha/FunCollection-механика, а не quest craft interactive object.

### `fun_collection_mystery_swap_halves`

Донор: `C:/Users/user/Downloads/FunCollection_6.xlsx`.

Механика: игроки делятся на две половины по последней цифре ID. Четные `0,2,4,6,8` получают ресурс A (`GR_1`), нечетные `1,3,5,7,9` получают ресурс B (`GR_2`). Всем нужны оба ресурса: игрок дарит друзьям свой ресурс и рассчитывает получить недостающий в ответ. Recipe тратит `GR_1 + GR_2` и выдает mystery box (`MB`), а mystery box дает один случайный элемент из 10 `CL`-частей коллекции.

Ключевые поля:

- `object_title_a`, `object_title_b`: две визуальные версии Home/Guest объекта.
- `resource_a_title`, `resource_b_title`: два взаимных ресурса для разных половин игроков.
- `mystery_box_title`, `mystery_box_description`: коробка/сюрприз, из которой выпадает случайный `CL`.
- `collection_rewards`: 10 элементов коллекции, которые игрок постепенно собирает через `MB`.
- `location_tag`, `source_action`, `tech_quest`: способ выпадения `GR_1`/`GR_2`.

Блоки:

- `FunCollection_<n>_Guest halves`: 2 Guest-объекта. Guest A просит/дарит ресурс B, Guest B просит/дарит ресурс A.
- `FunCollection_<n>_Home halves`: 2 Home-объекта, оба используют общий `charging_recipe`.
- `FunCollection_<n>_Recipe`: `GR_1 + GR_2 -> MB`.
- `FunCollection_<n> resources`: два `GR`-ресурса.
- `Collection reward assets FunCollection_<n>`: 10 `CL`-ресурсов.
- `Resource global_rewards FunCollection_<n>`: `GR_1` падает с `multiplicity=0,2,4,6,8`, `GR_2` падает с `multiplicity=1,3,5,7,9`.
- `Packages FunCollection_<n>`: пакеты продажи для обоих `GR`.
- `MB FunCollection_<n>`: mystery box с `find/replace` по prefix; содержимое коробки должно вести к 10 `CL`-элементам.

Правила:

- `input` брать из `Fun11` или ближайшего старого donor path, если Fun11-донора физически нет.
- `output`, `classname`, `file_name`, `identifier`, `reward`, `ingredients`, `guest_resource`, `view_classname`, `pack_asset` строить с целевым prefix.
- Не копировать старые битые package reward из `FunCollection_6.xlsx`, где пакеты указывают на `Fun13_FunCollection_2_CL_*`: пакеты должны выдавать свои `GR_1` и `GR_2`.
- В descriptions явно держать цель: получить два взаимных ресурса, собрать `MB`, открыть его ради одного из 10 элементов коллекции.
- Не добавлять этот объект в `campaigns/<campaign_id>/interactive_objects.json`: это potekha/FunCollection-механика, а не quest craft interactive object.

### `FunCollection_9`

Донор: `C:/Users/user/Downloads/FunCollection_9.xlsx`.

Механика: potekha/Skazaniya-объект на базе friend action. Игрок ходит к другу и делает действие с дневным лимитом и шансом успеха. За свое успешное действие игрок получает `FA_1`, а хозяин дома получает `FA_2`, когда друзья успешно делают действие у него. Затем `FA_1 + FA_2` крафтятся в `MB`, mystery box выдает один случайный элемент из 10 `CL`-частей коллекции.

Ключевые поля:

- `available_title`: флаг доступности `FunCollection_9_Available`.
- `action_title`: название friend action.
- `reward_for_action_title`, `reward_for_action_description`: ресурс `FA_1`, который получает действующий игрок.
- `reward_on_receive_title`, `reward_on_receive_description`: ресурс `FA_2`, который получает хозяин дома.
- `action_start_time`, `action_end_time`: временное окно для `viewer_conditions`, `friend_conditions`, `bot_conditions`.
- `craft_station_title`, `craft_station_hint`, `craft_station_description`: станок/объект, где игрок собирает `MB`.
- `mystery_box_title`, `mystery_box_description`: mystery box.
- `collection_rewards`: 10 элементов коллекции.
- `tech_quest`: условие recipe.

Блоки:

- `Availability object FunCollection_9`: furniture-флаг `{prefix}_FunCollection_9_Available`.
- `Friend action FunCollection_9`: объект `{prefix}_FunCollection_9`, `day_limit`, `probability`, `reward_for_action`, `reward_on_receive`, time-conditions.
- `Resources FunCollection_9`: `FA_1` и `FA_2`.
- `Packages FunCollection_9`: пакеты для `FA_1` и `FA_2`.
- `Recipe FunCollection_9`: `FA_1 + FA_2 -> MB`.
- `Mystery box FunCollection_9`: mystery box с заменой prefix.
- `Craft station FunCollection_9`: Home/станок с `extra.window_spec.charging_recipe`.
- `Collection reward assets FunCollection_9`: 10 `CL`-ресурсов.

Правила:

- Использовать этот template только когда пользователь явно называет exact ID `FunCollection_9`.
- Не добавлять объект в `campaigns/<campaign_id>/interactive_objects.json`: это potekha/Skazaniya FunCollection, не quest interactive object.
- Не оставлять смешанные donor prefix (`Fun12`/`Fun13`) в output/classname/reward/ingredients/view_classname.
- Держать `FA_1` и `FA_2` разными по смыслу: `FA_1` за действие у друга, `FA_2` от друзей у себя дома.
- Recipe reward и mystery_box classname должны быть согласованы с актуальным proto-ожиданием; donor XLSX содержит старые разнобои, их нельзя слепо копировать.

### `workbench_single`

Донор: `Fun12_Workbench.xlsx`.

Механика: одиночный workbench, не FunCollection.

Ключевые поля:

- `workbench_title`.
- `description`.
- `hint`.

Блок:

- `Workbench`: один объект `/workbench/Fun/<prefix>/<prefix>_Workbench_<n>.proto.js`.

## Мини-Чек Перед Выдачей

- Все `output` и generated classnames с текущим `prefix`.
- В `input` остался donor prefix.
- Все 10 CL-наград заполнены и тематически связаны.
- GR/подарочные ресурсы имеют понятный способ получения.
- `pack_asset=<classname>_Package` совпадает с package classname.
- `find/replace` строки оставлены там, где они были у донора.
- Workbench не попал в FunCollection CSV.
