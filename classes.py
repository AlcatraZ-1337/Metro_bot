import json

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
        update.message.reply_text(f'Вы встретили 🐾Упыря🐾. \n'
                                  f'Его текущее здоровье: ♥{self.enemy_mutant}♥. \n'
                                  f'Ваше текущее здоровье: ♥{self.health}♥. \n'
                                  f'Что вы будете делать?', reply_markup=markup_fight_choice)

    def attack(self, update, context):
        while self.enemy_mutant >= 1:
            self.enemy_mutant -= self.damage
            if self.enemy_mutant <= 0:
                update.message.reply_text('Вы успешно справились с мутантом.')
                with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
                    data = json.load(f)

                with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                    data['question_output'] = True
                    f.write(json.dumps(data))

    def escape(self, update, context):
        update.message.reply_text(f'Вы убежали от мутанта.')
        self.enemy_mutant = 0
        with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['question_output'] = True
            f.write(json.dumps(data))


reply_keyboard_station = [['Взять заказ на доставку', 'Выйти со станции'],
                          ['Осмотреть инвентарь', 'Арендовать домик на ночь: 35 патронов'],
                          ['Посмотреть карту']]
markup_station = ReplyKeyboardMarkup(reply_keyboard_station, one_time_keyboard=False)

reply_fight_choice = [['Атаковать'], ['Сбежать']]
markup_fight_choice = ReplyKeyboardMarkup(reply_fight_choice, one_time_keyboard=False)
