# Quest Interactive Object Templates

Эти правила относятся к интерактивным объектам для квестового workflow: они выбираются в `campaigns/<campaign_id>/interactive_objects.json`, экспортируются через `src/interactive_objects.py` и потом могут попадать в craft-рецепты квестов как дополнительные `_R_`-ресурсы.

Не смешивать их с `docs/FunCollection/*.xlsx`: FunCollection-шаблоны нужны для Потех/Сказаний и не пишутся в campaign-level `interactive_objects.json`.

## `story_random_recipe` / `Story_RandomRecipe`

Донор структуры: `NY23_Chest_LadyDogState1.proto.js`.

Механика: объект `chest` с `generate_price`. При каждом открытии он выбирает несколько элементов из `price_elements`, тратит выбранные ресурсы и всегда выдает один итоговый ресурс `{campaign_id}_Story_RandomRecipe_N_R_1`. В отличие от коллекционных версий, здесь нет `CL`, `MB`, прогресс-счетчика и финальной смены награды.

### Что Заполнить По Теме

- `object_title`: сам объект, например `Огуречное хранилище`.
- `craft_resource_titles`: 8 ресурсов цены в порядке `ASK_1`, `PER_1`, `GR_1`, `GR_2`, `GR_3`, `GR_4`, `ASK_2`, `PER_2`.
- `result_resource_title`: итоговый ресурс `R_1`.
- `result_resource_description`: короткое описание итогового ресурса.
- `wnd_description`: текст окна объекта.
- `rule_title`, `rule_description`, `rule_window`: справка/правила окна.
- `price_amounts`: сколько каждого ресурса просит price element.
- `price_weights`: веса выбора price elements; это не проценты, а относительные веса.
- `price_elements_amount`: сколько элементов цены показывать за одно открытие.
- `tech_quest`, `source_action`, `location_tag`, `drop_probability`, `assets`: если `GR`-ресурсы должны выпадать через global_reward.

### Classname-Паттерны

- Объект: `{campaign_id}_Story_RandomRecipe_1`.
- Ресурсы цены: `{campaign_id}_Story_RandomRecipe_1_ASK_1`, `{campaign_id}_Story_RandomRecipe_1_PER_1`, `{campaign_id}_Story_RandomRecipe_1_GR_1` ... `{campaign_id}_Story_RandomRecipe_1_PER_2`.
- Итоговый ресурс: `{campaign_id}_Story_RandomRecipe_1_R_1`.

Если в campaign выбрано несколько таких объектов, они нумеруются как `Story_RandomRecipe_1`, `Story_RandomRecipe_2`, а итоговые ресурсы становятся `{campaign_id}_Story_RandomRecipe_1_R_1`, `{campaign_id}_Story_RandomRecipe_2_R_1`.

### Пример Fun13

- Объект: `Fun13_Story_RandomRecipe_1` - `Огуречное хранилище`.
- Ресурсы цены: `Fun13_Story_RandomRecipe_1_ASK_1` - `Хрустящий огурчик`, `Fun13_Story_RandomRecipe_1_PER_1` - `Пустая банка`, `Fun13_Story_RandomRecipe_1_GR_1` - `Укроп`, `Fun13_Story_RandomRecipe_1_GR_2` - `Горчица`, `Fun13_Story_RandomRecipe_1_GR_3` - `Чеснок`, `Fun13_Story_RandomRecipe_1_GR_4` - `Лавровый лист`, `Fun13_Story_RandomRecipe_1_ASK_2` - `Соль`, `Fun13_Story_RandomRecipe_1_PER_2` - `Душистый горошек`.
- Итоговый ресурс: `Fun13_Story_RandomRecipe_1_R_1` - `Домовячьи огурчики (3 шт.)`.

### Блоки CSV

- `Story_RandomRecipe object`: один `chest`-объект с `generate_price`, `price_elements` и единственным `extra.result_rewards.0.asset`.
- `Story_RandomRecipe resources`: 8 ресурсов цены и итоговый `R_1`.
- `Story_RandomRecipe GR global rewards`: способы выпадения `GR_1..GR_4`, если они нужны.
- `Story_RandomRecipe ASK/PER post actions`: просьбы для `ASK` и `PER`.
- `Story_RandomRecipe packages`: пакеты продажи ресурсов цены.

### Важные Проверки

- В `extra.result_rewards` должен остаться только один asset: итоговый `{campaign_id}_Story_RandomRecipe_N_R_1`, без условий.
- Не оставлять `NY23_Parallel_Box_*`, `NY23_Parallel_Box_Counter`, `progress_resource`, `progress_total` и `after_open_actions` из донора: награда теперь ресурс, а не появляющийся на карте объект.
- Суффиксы ресурсов писать с подчеркиванием: `GR_2`, `GR_3`, `GR_4`, а не `GR2`, `GR3`, `GR4`.
- `price_elements_amount` не должен превышать количество ресурсов в `price_elements`.

## `mixer_1` / `Story_Mixer`

Донор структуры: `raw/examples/Story_Mixer.xlsx`, лист `Лист1`.

Механика: игрок собирает два обычных ингредиента `GR_1` и `GR_2`, просит у друзей или покупает один `ASK_1`, затем использует объект-миксер. Правильное действие тратит ингредиенты и сразу выдает готовый квестовый ресурс `R_1`. Никаких `CL` и mystery box в квестовой версии нет.

### Что Заполнить По Теме

- `object_title`: сам миксер/автомат/станок.
- `ingredient_a_title`: первый ингредиент `GR_1`.
- `ingredient_a_description`: как получить первый ингредиент.
- `ingredient_b_title`: второй ингредиент `GR_2`.
- `ingredient_b_description`: как получить второй ингредиент.
- `ask_resource_title`: ресурс `ASK_1`, который просят у друзей.
- `ask_resource_description`: обычно “Попроси у друзей или купи.”, но лучше тематично.
- `result_resource_title`: готовый квестовый ресурс `R_1`.
- `result_resource_description`: коротко объяснить, что он получается из правильного смешивания.
- `tech_quest`: технический quest classname для `active_quest`.
- `location_tag_a`, `source_action_a`, `drop_probability_a`, `assets_a`, `assets_a_2`: способ выпадения `GR_1`.
- `location_tag_b`, `source_action_b`, `drop_probability_b`, `assets_b`, `assets_b_2`: способ выпадения `GR_2`.

### Classname-Паттерны

- Объект: `{campaign_id}_Mixer_1`.
- Ингредиенты: `{campaign_id}_Mixer_1_GR_1`, `{campaign_id}_Mixer_1_GR_2`.
- ASK: `{campaign_id}_Mixer_1_ASK_1`.
- Готовый результат: `{campaign_id}_Mixer_1_R_1`.
- Quest actions: `action_{campaign_id}_Mixer_1_Right`, `action_{campaign_id}_Mixer_1_Wrong`, `action_{campaign_id}_Mixer_1_Hint2`, `action_{campaign_id}_Mixer_1_Hint3`.

Если в campaign выбрано несколько миксеров, они нумеруются как `Mixer_1`, `Mixer_2`, а result resources становятся `{campaign_id}_Mixer_1_R_1`, `{campaign_id}_Mixer_2_R_1`.

### Блоки CSV

- `Mixer object`: один furniture-объект. `output` и `classname` должны совпадать с `{campaign_id}_Mixer_1`.
- `Mixer resources GR`: `GR_1`, `GR_2`, `R_1`.
- `Mixer global rewards`: способы выпадения `GR_1` и `GR_2`, оба с `conditions=active_quest=<tech_quest>`.
- `Mixer resources ASK`: один `ASK_1`.
- `Post action ASK Mixer`: post_action для просьбы `ASK_1` у друзей.
- `Mixer packages`: пакеты продажи для `ASK_1`, `GR_1`, `GR_2`.
- `right_action Mixer`: правильное смешивание.
- `wrong_action Mixer`: неправильное смешивание.
- `action_Hint2 Mixer`, `action_Hint3 Mixer`: платные подсказки.

### Количества По Умолчанию

- Правильное действие: `GR_1:5 + GR_2:7 + ASK_1:3 -> R_1`.
- Неправильное действие: `GR_1:1 + GR_2:1 + ASK_1:1`.
- `ASK_1` post_action: `clicks_limit=5`, `life_time=43200`, `send_interval=7200`.
- Пакет `ASK_1`: 1 ресурс за 3.
- Пакеты `GR_1` и `GR_2`: 2 ресурса за 5.
- Подсказки: `money_crown=20` и `money_crown=30`.

### Важные Проверки

- В квестовом `Story_Mixer` результатом `right_action` всегда является готовый `{campaign_id}_Mixer_1_R_1`, а не `MB`.
- В `open_price` второго ингредиента должен стоять `GR_2`, не укороченный classname вида `{campaign_id}_Mixer_1_2`.
- `output`, `classname`, `file_name`, `identifier`, `poster_reward`, `open_price`, `pack_asset`, `stuff_icon` используют текущий `campaign_id`.
- Donor `input`-пути можно оставлять старыми; generated `output` не должен вести в `Downloads` или старый prefix.
- Такой объект не упоминать в текстах квестов как сюжетную “цель”: он технически дает ресурс для craft/quest data.
