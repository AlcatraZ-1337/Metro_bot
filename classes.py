import json
import random

from telegram import ReplyKeyboardMarkup


class User:
    def __init__(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)
        self.name = data['name']

        self.health = data['health']
        self.armor = data['armor']
        self.attack = data['attack']

        self.bullets = data['bullets']
        self.food = data['food']

        self.trade_item_1 = data['trade_item_1']
        self.trade_item_2 = data['trade_item_2']
        self.trade_item_3 = data['trade_item_3']
        self.trade_item_4 = data['trade_item_4']

        self.costume = 0
        self.weapon = 0

        self.station = data['station']
        self.owner = data['owner']

    def inventory(self, update, context):
        update.message.reply_text(
            "Ваш инвентарь: \n"
            "\n"
            f"🧍 Ваше имя: {self.name} 🧍\n"
            f"♥ Ваше здоровье: {self.health} ♥\n"
            f"🛡 Ваша броня: {self.armor} 🛡\n"
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
        if self.question_output:
            update.message.reply_text(f'Вы находитесь на станции: {self.station_name}.\n'
                                      f'Статус станции: {self.owner}.\n'
                                      f'Что вы хотите сделать?', reply_markup=markup_station)

            with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
                data = json.load(f)

            with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = False
                f.write(json.dumps(data))
        else:
            pass


class Fight:
    def __init__(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.health = data['health']
        self.damage = data['attack']

        self.enemy_mutant = 50
        self.enemy_human = 100

    def init_fight(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)
        choice = update.message.text

        if data['question_output'] and choice != 'Идти дальше':
            update.message.reply_text(f'🐾Вы встретили Упыря🐾. \n'
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
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)
        while self.enemy_mutant > 0:
            self.enemy_mutant -= self.damage
            self.health -= random.randint(0, 5)
            if self.enemy_mutant <= 0 and data['fight_output']:
                stations = {'Площадь Александра Невского 1': ['trade_item_1', 'trade_item_2'],
                            'Площадь Александра Невского 2': ['trade_item_1', 'trade_item_2'],
                            'Новочеркасская': ['trade_item_1', 'trade_item_2'],
                            'Маяковская': ['trade_item_3', 'trade_item_4']}
                item_name = {'trade_item_1': '🍄Кислик🍄', 'trade_item_2': '🧼Тунельный камень🧼',
                             'trade_item_3': '🌿Ржавая трава🌿', 'trade_item_4': '🛢Керосин🛢'}
                trade_item_1, trade_item_2 = stations[data["station"]]
                quantity_trade_item_1, quantity_trade_item_2 = data[trade_item_1] + 8, data[trade_item_2] + 4
                trade_item_1, trade_item_2 = item_name[trade_item_1], item_name[trade_item_2]
                update.message.reply_text('Вы успешно справились с мутантом.\n'
                                          f'Вы получили: {quantity_trade_item_1} {trade_item_1} и '
                                          f'{quantity_trade_item_2} {trade_item_2}.\n'
                                          f'♥ Ваше здоровье после битвы: {self.health} ♥.')

                with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                    data['health'] = self.health
                    data[trade_item_1] = quantity_trade_item_1
                    data[trade_item_2] = quantity_trade_item_2
                    data['fight_output'] = False
                    data['question_output'] = True
                    f.write(json.dumps(data))

    def escape(self, update, context):
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)
        if data['fight_output']:
            update.message.reply_text(f'Вы убежали от мутанта.')
            self.enemy_mutant = 0
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

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
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['fight_output'] = False
            data['question_output'] = True
            f.write(json.dumps(data))


reply_keyboard_station = [['Взять заказ на доставку', 'Выйти со станции'],
                          ['Осмотреть инвентарь', 'Арендовать домик на ночь: 35 патронов'],
                          ['Посмотреть карту']]
markup_station = ReplyKeyboardMarkup(reply_keyboard_station, one_time_keyboard=False)

reply_fight_choice = [['Атаковать'], ['Сбежать']]
markup_fight_choice = ReplyKeyboardMarkup(reply_fight_choice, one_time_keyboard=False)
