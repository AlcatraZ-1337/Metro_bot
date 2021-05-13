import json
import random

from telegram import ReplyKeyboardMarkup


class User:
    def __init__(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.name = data['name']

        self.health = data['health']
        self.attack = data['attack']

        self.bullets = data['bullets']
        self.food = data['food']

        self.trade_item_1 = data['trade_item_1']
        self.trade_item_2 = data['trade_item_2']
        self.trade_item_3 = data['trade_item_3']
        self.trade_item_4 = data['trade_item_4']

        self.station = data['station']
        self.owner = data['owner']

    def inventory(self, update, context):
        update.message.reply_text(
            "Ваш инвентарь: \n"
            "\n"
            f"🧍 Ваше имя: {self.name} 🧍\n"
            f"♥ Ваше здоровье: {self.health} ♥\n"
            f"🔪Ваш урон: {self.attack} 🔪\n"
            "\n"
            f"🔫 Ваши патроны: {self.bullets} 🔫\n"
            f"🍖 Ваш запас еды: {self.food} 🍖\n"
            "\n"
            "♼ Ваши предметы для бартера: ♼\n"
            f"🍄 Кислик: {self.trade_item_1} 🍄\n"
            f"🧼 Тунельный камень: {self.trade_item_2} 🧼\n"
            f"🌿 Ржавая трава: {self.trade_item_3} 🌿\n"
            f"🛢 Керосин: {self.trade_item_4} 🛢\n"
            f"\n"
            f"Текущая станция: {self.station}")


class Station:
    def __init__(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.station_name = data['station']
        self.owner = data['owner']
        self.question_output = data['question_output']
        self.fight_output = data['fight_output']

    def init_station(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        if self.question_output:
            if data['station'] != 'Лиговский проспект':
                update.message.reply_text(f'Вы находитесь на станции: {self.station_name}.\n'
                                          f'Статус станции: {self.owner}.\n'
                                          f'Что вы хотите сделать?', reply_markup=markup_station)
            else:
                update.message.reply_text(f'Вы находитесь на станции: {self.station_name}.\n'
                                          f'Статус станции: {self.owner}.\n'
                                          f'Что вы хотите сделать?', reply_markup=markup_dead_station)

            with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = False
                f.write(json.dumps(data))
        else:
            pass


class Fight:
    def __init__(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        enemy_dict = {'ghoul': (random.randint(40, 80), 'Упыря'),
                      'guardian': (random.randint(50, 90), 'Стража'),
                      'marauder': (random.randint(60, 100), 'Мародёра'),
                      'nosey': (random.randint(60, 100), 'Носача')}

        self.health = data['health']
        self.damage = data['attack']

        if 15 <= self.damage < 20:
            self.enemy_mutant, self.enemy = enemy_dict['ghoul']
        elif 20 <= self.damage <= 25:
            self.enemy_mutant, self.enemy = enemy_dict['guardian']
        else:
            self.enemy_mutant, self.enemy = enemy_dict['marauder']

    def init_fight(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        choice = update.message.text

        if data['question_output'] and choice != 'Идти дальше':
            update.message.reply_text(f'🐾Вы встретили {self.enemy}🐾. \n'
                                      f'♥Его текущее здоровье: {self.enemy_mutant}♥. \n'
                                      f'♥Ваше текущее здоровье: {self.health}♥. \n'
                                      f'Что вы будете делать?', reply_markup=markup_fight_choice)

            with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = False
                f.write(json.dumps(data))

        elif choice == 'Идти дальше':
            update.message.reply_text('Вы прошли через тоннель.',
                                      reply_markup=ReplyKeyboardMarkup([['Выйти на станцию']], one_time_keyboard=False))

            with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                data['fight_output'] = False
                data['question_output'] = True
                f.write(json.dumps(data))

    def attack(self, update, context):
        pay_for_life = False

        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        while self.enemy_mutant > 0:
            if self.enemy_mutant > 0:
                self.enemy_mutant -= self.damage
                damage = random.randint(0, 5)
                self.health -= damage

            if self.enemy_mutant <= 0 and data['fight_output']:
                stations = {'Площадь Александра Невского 1': ['trade_item_1', 'trade_item_2'],
                            'Площадь Александра Невского 2': ['trade_item_1', 'trade_item_2'],
                            'Новочеркасская': ['trade_item_1', 'trade_item_2'],
                            'Маяковская': ['trade_item_3', 'trade_item_4'],
                            'Площадь восстания': ['trade_item_3', 'trade_item_4'],
                            'Лиговский проспект': ['bullets', 'food'],
                            'Владимирская': ['trade_item_3', 'trade_item_4']}
                item_name = {'trade_item_1': '🍄Кислик🍄', 'trade_item_2': '🧼Тунельный камень🧼',
                             'trade_item_3': '🌿Ржавая трава🌿', 'trade_item_4': '🛢Керосин🛢', 'bullets': '🔫Патроны🔫',
                             'food': '🍖Еда🍖'}
                trade_item_1, trade_item_2 = stations[data["station"]]

                if self.enemy == 'Упыря':
                    if data["station"] != 'Лиговский проспект':
                        quantity_trade_item_1_from_battle = random.randint(5, 12)
                        quantity_trade_item_2_from_battle = random.randint(3, 8)
                    else:
                        quantity_trade_item_1_from_battle = random.randint(5, 12)
                        quantity_trade_item_2_from_battle = random.randint(1, 3)
                    enemy_class = 'мутантом'
                elif self.enemy == 'Стража':
                    if data["station"] != 'Лиговский проспект':
                        quantity_trade_item_1_from_battle = random.randint(8, 16)
                        quantity_trade_item_2_from_battle = random.randint(6, 12)
                    else:
                        quantity_trade_item_1_from_battle = random.randint(8, 16)
                        quantity_trade_item_2_from_battle = random.randint(1, 3)
                    enemy_class = 'мутантом'
                elif self.enemy == 'Мародёра':
                    if data["station"] != 'Лиговский проспект':
                        quantity_trade_item_1_from_battle = random.randint(12, 20)
                        quantity_trade_item_2_from_battle = random.randint(10, 16)
                    else:
                        quantity_trade_item_1_from_battle = random.randint(12, 20)
                        quantity_trade_item_2_from_battle = random.randint(3, 5)
                    enemy_class = 'мародёром'

                quantity_trade_item_1, quantity_trade_item_2 = \
                    data[trade_item_1] + quantity_trade_item_1_from_battle, \
                    data[trade_item_2] + quantity_trade_item_2_from_battle
                trade_item_1, trade_item_2 = item_name[trade_item_1], item_name[trade_item_2]
                update.message.reply_text(f'Вы успешно справились с {enemy_class}.\n'
                                          f'Вы получили: {quantity_trade_item_1_from_battle} {trade_item_1} и '
                                          f'{quantity_trade_item_2_from_battle} {trade_item_2}.\n'
                                          f'♥ Ваше здоровье после битвы: {self.health} ♥.')

                with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                    item_name = {'🍄Кислик🍄': 'trade_item_1', '🧼Тунельный камень🧼': 'trade_item_2',
                                 '🌿Ржавая трава🌿': 'trade_item_3', '🛢Керосин🛢': 'trade_item_4',
                                 '🔫Патроны🔫': 'bullets', '🍖Еда🍖': 'food'}
                    data['health'] = self.health
                    data[item_name[trade_item_1]] = quantity_trade_item_1
                    data[item_name[trade_item_2]] = quantity_trade_item_2
                    data['fight_output'] = False
                    data['question_output'] = True
                    f.write(json.dumps(data))

            if self.health <= 0 and not pay_for_life:
                pay_for_life = True
                update.message.reply_text('Во время битвы вы потеряли сознание, из-за полученных ранений.\n'
                                          'Вас нашли сталкеры с Новочеркасской и доставили к себе на станцию.\n'
                                          '🔫Вы потеряли: 50 патронов.🔫')
                with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                    self.health = 100
                    data['health'] = self.health
                    data['bullets'] = data['bullets'] - 50
                    if data['bullets'] < 0:
                        data['bullets'] = 0
                    data['station'] = 'Новочеркасская'
                    data['owner'] = 'Альянс Оккервиль'
                    data['fight_output'] = False
                    data['question_output'] = True
                    f.write(json.dumps(data))

    def escape(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        if data['fight_output']:
            update.message.reply_text(f'Вы успешно сбежали.')
            self.enemy_mutant = 0

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['fight_output'] = False
            data['question_output'] = True
            f.write(json.dumps(data))

    def exit_from_tunnel(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        if data['fight_output']:
            update.message.reply_text(f'Вы пришли на станцию.')
            self.enemy_mutant = 0

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['fight_output'] = False
            data['question_output'] = True
            f.write(json.dumps(data))


class Trade:
    def __init__(self, update, context):

        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.station = data['station']

        self.bullets = data['bullets']
        self.food = data['food']

        self.trade_item_1 = data['trade_item_1']
        self.trade_item_2 = data['trade_item_2']
        self.trade_item_3 = data['trade_item_3']
        self.trade_item_4 = data['trade_item_4']

    def init_trade(self, update, context):
        normal_stations = ['Маяковская', 'Лиговский проспект', 'Владимирская', 'Площадь восстания']
        if self.station not in normal_stations:
            update.message.reply_text(f'Жители станции {self.station} могут обменять следующие товары: \n'
                                      '\n'
                                      'Улучшение пистолета: \n'
                                      '🔫40 патронов🔫, 🍖10 еды🍖, 🍄30 Кисликов🍄 и '
                                      '🧼15 Тунельных камней🧼. \n'
                                      '🍖Еда🍖: \n'
                                      '🔫10 патронов🔫 и 🍄5 Кисликов🍄. \n'
                                      '🔫Пять Патронов🔫: \n'
                                      '🍄5 Кисликов🍄 и 🧼5 Тунельных камней🧼. \n'
                                      'Что вы будете делать?', reply_markup=markup_trade_things_simple_stations)
        else:
            update.message.reply_text(f'Жители станции {self.station} могут обменять следующие товары: \n'
                                      '\n'
                                      'Улучшение обреза: \n'
                                      '🔫30 патронов🔫, 🍖10 еды🍖, 🌿15 Ржавой травы🌿 и '
                                      '🛢20 Керосина🛢. \n'
                                      '🍖Три еды🍖: \n'
                                      '🔫12 патронов🔫 и 🌿6 Ржавой травы🌿. \n'
                                      '🔫Десять Патронов🔫: \n'
                                      '🌿6 Ржавой травы🌿 и 🛢6 Керосина🛢. \n'
                                      'Что вы будете делать?', reply_markup=markup_trade_things_normal_stations)


reply_keyboard_trade_things_simple_stations = [['🍖Еда🍖', '🔫Пять Патронов🔫'], ['Улучшение пистолета']]
markup_trade_things_simple_stations = ReplyKeyboardMarkup(reply_keyboard_trade_things_simple_stations,
                                                          one_time_keyboard=False)

reply_keyboard_trade_things_normal_stations = [['🍖Три еды🍖', '🔫Десять Патронов🔫'], ['Улучшение обреза']]
markup_trade_things_normal_stations = ReplyKeyboardMarkup(reply_keyboard_trade_things_normal_stations,
                                                          one_time_keyboard=False)

reply_keyboard_station = [['Поменяться предметами с жителями', 'Выйти со станции'],
                          ['Осмотреть инвентарь', 'Арендовать домик на ночь: 35 патронов'],
                          ['Посмотреть карту']]
markup_station = ReplyKeyboardMarkup(reply_keyboard_station, one_time_keyboard=False)

reply_keyboard_dead_station = [['Выйти со станции', 'Осмотреть инвентарь'], ['Посмотреть карту']]
markup_dead_station = ReplyKeyboardMarkup(reply_keyboard_dead_station, one_time_keyboard=False)

reply_keyboard_fight_choice = [['Атаковать'], ['Сбежать']]
markup_fight_choice = ReplyKeyboardMarkup(reply_keyboard_fight_choice, one_time_keyboard=False)
