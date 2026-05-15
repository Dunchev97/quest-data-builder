# FunCollection Templates

Эти шаблоны нужны для генерации интерактивных объектов Потех/Сказаний по любой теме. Источник структуры - только лист `conf` в файлах `docs/FunCollection/FunCollection_*.xlsx`.

Не использовать вкладки `Способы`, `Значения` и файлы из `Downloads` как источник правды. Они могут быть старым черновиком.

## Общий Контракт

Пользователь может дать:

- `template_id`: exact ID, например `FunCollection_1`.
- `prefix`: целевой префикс, например `Fun13`.
- `theme`: тема, по которой нужно назвать объект, ресурсы и коллекционные элементы.
- `object`: конкретный объект, если он важен; если не дан, Codex выбирает объект по теме.
- `tech_quest`: технический quest classname для conditions.
- `location_tag`: где выпадает ресурс, если у механики есть global_reward.
- `action_start_time` / `action_end_time`: только для `FunCollection_9`.

Codex обязан:

- брать структуру из `docs/FunCollection/<template_id>.xlsx`, лист `conf`;
- сохранять порядок блоков и заголовки колонок как в donor;
- менять `output`, `classname`, `file_name`, `identifier`, `reward`, `ingredients`, `conditions`, `view_classname`, `stuff_icon`, `pack_asset` на целевой `prefix`;
- оставлять `input` donor-путями;
- оставлять `id` пустым, если пользователь не дал конкретные id;
- всегда создавать ровно 10 `CL`-ресурсов, если шаблон коллекционный;
- не подставлять `lawn` или другой дефолт вместо `location_tag`, если пользователь/контекст дал конкретную локацию;
- писать тексты предметно, в стиле Домовят, без формальных "необходимо" и "требуется".
- не передавать кириллицу в генератор через PowerShell pipe `@'...'@ | python -`; сначала сохранить данные анкеты в UTF-8 файл, затем запускать ASCII-only генератор;
- после генерации прочитать CSV/XLSX обратно и проверить, что нет `????` в русских полях.

Если пользователь дал exact ID (`FunCollection_1`, `FunCollection_2` и т.д.), не выбирать похожий шаблон вместо него.

## `FunCollection_1`

**Механика:** Home/Guest chest. Игрок добывает один `GR_1`, тратит его на открытие объекта дома или в гостях и получает один из 10 `CL`.

**Нужно заполнить по теме:**

- `object_title`: объект Home/Guest.
- `activation_resource_title`: ресурс для открытия `GR_1`.
- `activation_resource_description`: как получить/что это за ресурс.
- `reward_group_title`: общее название набора из 10 `CL`.
- `collection_rewards[1..10].title`: 10 частей коллекции.
- `collection_rewards[1..10].description`: обычно "Можно получить из <object_title> дома или в гостях".
- `location_tag`, `source_action`, `drop_probability`.
- `tech_quest_home`, `tech_quest_guest`.
- Тексты окна: `description_window`, `reward_description`, `instruction_title`, названия кнопок.

**CSV-блоки листа `conf`:**

- `ресурсы FunCollection_1`: 1 `GR_1` + 10 `CL`.
- `Способ получения ресурса FunCollection_1`: 1 global_reward для `GR_1`.
- `Объект FunCollection_1_Guest`: Guest chest, `action_availability_conditions=stuff=<Home>`.
- `Объект FunCollection_1_Home`: Home chest, `action_availability_conditions=active_quest=<tech_quest_home>`.
- `Пакет для продажи ресурсов FunCollection_1`: package для `GR_1`.

**Важно:** в donor есть старая опечатка `tuff=` в Guest condition; для dev-ready CSV использовать корректное `stuff=`.

## `FunCollection_2`

**Механика:** `Story_HELP` / `help_1`-подобный объект на 10 групп. Игроки делятся по последней цифре ID; каждая группа получает свой `CL_i` через `multiplicity`, а Home/Guest-пары помогают обменивать помощь друзей на итоговый ресурс.

**Нужно заполнить по теме:**

- `object_title`: общий объект для 10 Home/Guest.
- `path_resource_title`: ресурс помощи от действий друзей (`HELP_OpenerPath`).
- `result_resource_title`: итоговый ресурс (`HELP_Opener`).
- `collection_rewards[1..10].title`: 10 групповых `CL`.
- `collection_rewards[1..10].description`: текст для своей/чужой группы.
- `mark_1`, `mark_2`, `comment_1..4`.
- `guest_conditions_title`.
- `location_tag`, `source_action`, `drop_probability`, `tech_quest`.

**CSV-блоки листа `conf`:**

- `FunCollection_2_Home x10`: 10 Home-объектов, каждый тратит свой `CL_i`.
- `FunCollection_2_Guest x10`: 10 Guest-объектов, каждый смотрит на свой Home.
- `HELP resources`: `HELP_OpenerPath` и `HELP_Opener`.
- `Collection reward assets x10`: 10 `CL`.
- `Collection reward global_rewards x10`: 10 global_reward c `multiplicity`.
- `Packages`: 10 пакетов `CL` + пакеты `HELP_OpenerPath` и `HELP_Opener`.
- `HELP_Opener recipe`: рецепт из `HELP_OpenerPath` в `HELP_Opener`.

**Правило multiplicity:** `CL_1..CL_9` получают `multiplicity=1..9`, `CL_10` получает `multiplicity=0`.

## `FunCollection_3`

**Механика:** одиночный платный chest/предсказатель. Игрок открывает объект за валюту/цену и получает один случайный `CL` из 10.

**Нужно заполнить по теме:**

- `object_title`: объект или персонаж.
- `collection_rewards[1..10].title`.
- `collection_rewards[1..10].description`: обычно "Можно получить у <object_title_genitive>".
- `window_description`: объяснение, что под одним вариантом лежит коллекционный предмет, под другими - ресурсы.
- `use_for_money_price`, `reward_time_interval`, если нужно отличаться от donor.

**CSV-блоки листа `conf`:**

- `Ресурсы FunCollection_3`: 10 `CL`.
- `Объект FunCollection_3`: chest-объект с `use_for_money_price`, `extra.window_skin`, `find/replace`, `extra.text_description`, `reward_time_interval`.

## `FunCollection_4`

**Механика:** объект с состояниями. Нейтральный объект кормят/заряжают `GR_1`; после ожидания появляется хорошее или плохое состояние. Хорошее состояние дает один из 10 `CL`, плохое может запускать негативные эффекты.

**Нужно заполнить по теме:**

- `neutral_title`, `good_state_title`, `bad_state_title`.
- `feeding_resource_title`, `feeding_resource_description`.
- `reward_owner_name`: кто выдает `CL`.
- `good_popup`, `good_window_text`, `bad_popup`, `bad_window_text`.
- `wait_title`, `buy_spoil_icon`, location replace ids, если нужны.
- `collection_rewards[1..10].title`.
- `negative_effect_titles`: 6 названий негативных эффектов.
- `location_tag`, `source_action`, `drop_probability`, `tech_quest`.

**CSV-блоки листа `conf`:**

- `Нейтральное состояние FunCollection_4`.
- `Хорошоее состояние FunCollection_4`.
- `Плохое состояние FunCollection_4`.
- `Ресурсы FunCollection_4`: 1 `GR_1` + 10 `CL`.
- `Пакеты ресурсов FunCollection_4`: package для `GR_1`.
- `Способы получения ресурсов FunCollection_4`: global_reward для `GR_1`.
- `Негативные эффекты FunCollection_4`: 6 furniture effects.

## `FunCollection_5`

**Механика:** объект с Unlock и вкладами друзей. Игрок добывает ресурс анлока `GR_1`, загружает `Unlock` и открывает доступ к объекту. Друг добывает ресурс дарения `GR_2_1`, вкладывает его в Guest; при дарении он превращается в ресурс результата `GR_2_2`. Home тратит `GR_2_2` на коллекционный результат/награду.

**Нужно заполнить по теме:**

- `object_title`: общий объект Guest/Unlock/Home.
- `unlock_resource_title`: ресурс анлока `GR_1`.
- `gift_resource_title`: ресурс дарения `GR_2_1`.
- `contribution_result_title`: ресурс результата `GR_2_2`.
- `collection_rewards[1..10].title`.
- `collection_rewards[1..10].description`.
- `post_action_text`.
- Тексты Guest/Unlock/Home окон.
- `unlock_source_action`, `gift_source_action`, `unlock_location_tag`, `gift_location_tag`, `tech_quest`.

**CSV-блоки листа `conf`:**

- `Ресурсы FunCollection_5`: 10 `CL` + `GR_2_2` + `GR_1`.
- `Ресурс дарения FunCollection_5`: `GR_2_1` с `transformation_to_other_asset_while_gifting=<GR_2_2>`.
- `Способ получения ресурса анлока FunCollection_5`: global_reward для `GR_1`.
- `Способ получения ресурса дарения FunCollection_5`: global_reward для `GR_2_1`.
- `Пакеты продажи ресурсов FunCollection_5`: packages для `GR_2_2` и `GR_1`.
- `Пост экшен FunCollection_5`.
- `FunCollection_5_Guest`.
- `FunCollection_5_Unlock`.
- `FunCollection_5_Home`.

**Важно:** `Unlock` не выдает `CL` сам. Он только разрешает пользоваться окном объекта; подарки друзей потом тратятся в Home.

## `FunCollection_6`

**Механика:** две половины игроков по последней цифре ID. Четные получают `GR_1`, нечетные получают `GR_2`. Чтобы собрать `MB`, нужны оба ресурса, поэтому игроки дарят друзьям свой ресурс и получают недостающий в ответ. Recipe `GR_1 + GR_2 -> MB`, `MB` дает случайный `CL`.

**Нужно заполнить по теме:**

- `object_title_a`, `object_title_b`: две версии Home/Guest.
- `resource_a_title`, `resource_b_title`: `GR_1` и `GR_2`.
- `home_hint`, `home_description`, `home_help_text`.
- `guest_spend_description`, `guest_help_text_a`, `guest_help_text_b`.
- `mystery_box_title`, `mystery_box_description`.
- `collection_rewards[1..10].title` и descriptions.
- `location_tag`, `source_action`, `drop_probability`, `tech_quest`.

**CSV-блоки листа `conf`:**

- `FunCollection_6_Guest`: 2 Guest-объекта.
- `FunCollection_6_Home`: 2 Home-объекта.
- `Fun12_FunCollection_6_Recipe`: recipe `GR_1+GR_2 -> MB`.
- `FunCollection_6 resources`: `GR_1`, `GR_2`.
- `Collection reward assets FunCollection_6`: 10 `CL`.
- `Collection reward global_rewards FunCollection_6`: 2 global_reward с чет/нечет `multiplicity`.
- `Packages FunCollection_6`: packages для `GR_1`, `GR_2`.
- `MB FunCollection_6`: mystery box.

**Правило multiplicity:** `GR_1` для `0,2,4,6,8`, `GR_2` для `1,3,5,7,9`, если пользователь не сказал иначе.

## `FunCollection_7`

**Механика:** потешный/сказочный миксер. Игрок добывает два `GR`-ингредиента, получает `ASK_1` через просьбу друзьям или покупку, затем использует миксер. Правильное действие не выдает готовый квестовый `R_1`, а выдает `MB_1`; при открытии `MB_1` выпадает один случайный `CL` из 10 частей коллекции.

**Нужно заполнить по теме:**

- `object_title`: сам миксер/автомат/станок.
- `ingredient_a_title`, `ingredient_a_description`: первый ингредиент `GR_1`.
- `ingredient_b_title`, `ingredient_b_description`: второй ингредиент `GR_2`.
- `ask_resource_title`, `ask_resource_description`: ресурс `ASK_1`, который просят у друзей.
- `mystery_box_title`, `mystery_box_description`: коробка/напиток/сверток, который выдает миксер.
- `collection_rewards[1..10].title` и descriptions: 10 коллекционных элементов из `MB_1`.
- `tech_quest`.
- `location_tag_a`, `source_action_a`, `drop_probability_a`, `assets_a`, `assets_a_2`: способ выпадения `GR_1`.
- `location_tag_b`, `source_action_b`, `drop_probability_b`, `assets_b`, `assets_b_2`: способ выпадения `GR_2`.

**CSV-блоки листа `conf`:**

- `Объект FunCollection_7`: один furniture-миксер.
- `FunCollection_7 resources GR`: `GR_1`, `GR_2`.
- `FunCollection_7 global_rewards`: способы выпадения `GR_1` и `GR_2`.
- `FunCollection_7 resources ASK`: один `ASK_1`.
- `Post action ASK FunCollection_7`: просьба `ASK_1` у друзей.
- `Пакеты продажи FunCollection_7`: пакеты `ASK_1`, `GR_1`, `GR_2`.
- `right_action FunCollection_7`: правильное смешивание, результат `MB_1`.
- `wrong_action FunCollection_7`: неправильное смешивание.
- `action_Hint2 FunCollection_7`, `action_Hint3 FunCollection_7`: подсказки.
- `Лутбокс FunCollection_7`: `MB_1`.
- `Collection reward assets FunCollection_7`: 10 `CL`.

**Важные donor-fix правила:**

- `right_action.open_price` должен тратить `{prefix}_FunCollection_7_GR_1`, `{prefix}_FunCollection_7_GR_2`, `{prefix}_FunCollection_7_ASK_1`; не оставлять donor-ошибку `{prefix}_FunCollection_7_2`.
- `right_action` должен заменять `NY24_Mixer_R_1` на `{prefix}_FunCollection_7_MB_1`.
- В блоке mystery box `classname`, `output`, `view_classname` должны быть `{prefix}_FunCollection_7_MB_1`, не stale `FunCollection_6_MB_1`.
- Все `CL`-строки должны использовать target `prefix` и `FunCollection_7`, не donor `Fun12`.
- В этой версии нет готового `R_1`: цель игрока - получать `MB_1` и собирать 10 `CL`.

## `FunCollection_9`

**Механика:** FunCollection-версия friend action. Игрок делает действие у друга и получает `FA_1`; хозяин дома получает `FA_2`, когда друзья успешно делают действие у него. Recipe `FA_1 + FA_2 -> MB`, `MB` дает случайный `CL`.

**Нужно заполнить по теме:**

- `available_title`: флаг доступности.
- `action_title`: название friend action.
- `reward_for_action_title`, `reward_for_action_description`: `FA_1`.
- `reward_on_receive_title`, `reward_on_receive_description`: `FA_2`.
- `wall_block_title_success`, `wall_block_title_not_success`.
- `craft_station_title`, `craft_station_hint`, `craft_station_description`, `craft_station_help_text`.
- `mystery_box_title`, `mystery_box_description`.
- `collection_rewards[1..10].title` и descriptions.
- `action_start_time`, `action_end_time`, `tech_quest`.

**CSV-блоки листа `conf`:**

- `Объект доступности FunCollection_9_Available`.
- `Объект FunCollection_9`: friend action с `day_limit`, `probability`, rewards и time conditions.
- `Ресурсы FunCollection_9`: `FA_1`, `FA_2`.
- `Package FunCollection_9`: packages для `FA_1`, `FA_2`.
- `Fun12_FunCollection_9_Recipe`: recipe `FA_1+FA_2 -> MB`.
- `MB FunCollection_9`: mystery box.
- `Станок для крафта FunCollection_9`: Home/станок с `charging_recipe`.
- `Collection reward assets FunCollection_9`: 10 `CL`.

**Важно:** `FA_1` и `FA_2` должны различаться по смыслу. `FA_1` - награда за поход к другу, `FA_2` - то, что игрок получает от друзей у себя дома.

## Чек Перед Выдачей CSV/XLSX

- В итоговом файле нет `Downloads`.
- В `output`, `classname`, `file_name`, `identifier`, `reward`, `ingredients`, `conditions`, `view_classname`, `stuff_icon`, `pack_asset` нет старого префикса, кроме намеренных donor `input`.
- Количество строк блоков совпадает с donor `conf`.
- Для `FunCollection_1`, `3`, `4`, `5`, `6`, `7`, `9` есть ровно 10 `CL`.
- Для `FunCollection_2` есть 10 Home, 10 Guest, 10 `CL`, 10 global_reward и `CL_10` использует `multiplicity=0`.
- Пакеты выдают свои ресурсы, а не случайные старые `CL` из другого FunCollection.
- Все тексты тематически связаны с объектом, ресурсами и коллекцией.
- В русских `title`, `description`, заголовках и текстах окон нет `????`.
