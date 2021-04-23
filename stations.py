import json
from random import random

from telegram import ReplyKeyboardMarkup

reply_keyboard_station = [['Взять заказ на доставку', 'Выйти со станции'],
                                   ['Осмотреть инвентарь', 'Арендовать домик на ночь: 35 патронов'],
                                   ['Посмотреть карту']]
markup_station = ReplyKeyboardMarkup(reply_keyboard_station, one_time_keyboard=True)

# Переходы между станциями
reply_keyboard_tunnel_novocherkasskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2']]
markup_tunnel_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_novocherkasskaya, one_time_keyboard=True)

reply_keyboard_tunnel_alexander_nevsky_square_1 = [['Новочеркасская', 'Площадь Александра Невского 2'], ['Маяковская']]
markup_tunnel_alexander_nevsky_square_1 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_1,
                                                              one_time_keyboard=True)

reply_keyboard_tunnel_alexander_nevsky_square_2 = [['Новочеркасская', 'Площадь Александра Невского 1'], ['Маяковская']]
markup_tunnel_alexander_nevsky_square_2 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_2,
                                                              one_time_keyboard=True)

reply_keyboard_tunnel_mayakovskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2']]
markup_tunnel_mayakovskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_mayakovskaya, one_time_keyboard=True)

reply_tunnels_move = [['Идти дальше'], ['Искать мутантов в тех. помещениях', 'Искать мародёров в тех. помещениях']]
markup_tunnels_move = ReplyKeyboardMarkup(reply_tunnels_move, one_time_keyboard=True)


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

    def init_station(self, update, context):
        update.message.reply_text(f"Вы находитесь на станции: {self.station_name}.\n"
                                  f"Станция под контролем: {self.owner}.\n"
                                  f"Что вы хотите сделать?", reply_markup=markup_station)


def station_distributor(update, context):
    activities = {'Взять заказ на доставку': None, 'Выйти со станции': tunnels_choice,
                  'Осмотреть инвентарь': User(update, context).inventory,
                  'Арендовать домик на ночь: 35 патронов': sleep,
                  'Посмотреть карту': geocoder,

                  'Площадь Александра Невского 1': tunnels,
                  'Площадь Александра Невского 2': tunnels,
                  'Новочеркасская': tunnels,
                  'Маяковская': tunnels,

                  'Да': None, 'Идти дальше': None}
    current_station = Station(update, context)
    current_station.init_station(update, context)
    choice = update.message.text
    try:
        activities[choice](update, context)
    except TypeError:
        pass


class Fight:
    def __init__(self):
        pass


def tunnels_choice(update, context):
    stations = {'Новочеркасская': markup_tunnel_novocherkasskaya,
                'Площадь Александра Невского 1': markup_tunnel_alexander_nevsky_square_1,
                'Площадь Александра Невского 2': markup_tunnel_alexander_nevsky_square_2,
                'Маяковская': markup_tunnel_mayakovskaya}
    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
    update.message.reply_text("Куда вы хотите пойти?", reply_markup=stations[data['station']])

    return 3


def tunnels(update, context):
    owners = {'Новочеркасская': 'Альянс Оккервиль', 'Площадь Александра Невского 1': 'Империя Веган',
              'Площадь Александра Невского 2': 'Империя Веган', 'Маяковская': 'Независимая станция'}
    update.message.reply_text("Вы идёте по тоннелям.")
    # random_tunnel = random.randint(0, 2)
    station_choice = update.message.text
    update.message.reply_text("Вы без проблем проходите через тоннель.", reply_markup=markup_tunnels_move)
    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
    with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
        data['station'] = station_choice
        data['owner'] = owners[station_choice]
        f.write(json.dumps(data))
    return 2


def sleep(update, content):
    update.message.reply_text("Во время сна вы полностью восстановили своё здоровье.")
    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
    with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
        data['health'] = 100
        data['bullets'] = data['bullets'] - 35
        f.write(json.dumps(data))


def geocoder(update, context):
    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
    api_requests = {'Новочеркасская': f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn=0.5,0.5&l=map&pt="
                                      f"30.411310,59.929214,pm2rdl",
                    'Площадь Александра Невского 1': f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn="
                                                     f"0.5,0.5&l=map&pt=30.385229,59.924287,pm2rdl",
                    'Площадь Александра Невского 2': f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn="
                                                     f"0.5,0.5&l=map&pt=30.385229,59.924287,pm2rdl",
                    'Маяковская': f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn="
                                                     f"0.5,0.5&l=map&pt=30.355314,59.931386,pm2rdl"}
    context.bot.send_photo(
        update.message.chat_id,
        api_requests[data['station']],
    )
