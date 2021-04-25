import json
from random import random

from telegram import ReplyKeyboardMarkup

from classes import User, Station, markup_station, Fight

reply_keyboard_tunnel_novocherkasskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2']]
markup_tunnel_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_novocherkasskaya,
                                                     one_time_keyboard=False)

reply_keyboard_tunnel_alexander_nevsky_square_1 = [['Новочеркасская', 'Площадь Александра Невского 2'], ['Маяковская']]
markup_tunnel_alexander_nevsky_square_1 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_1,
                                                              one_time_keyboard=False)

reply_keyboard_tunnel_alexander_nevsky_square_2 = [['Новочеркасская', 'Площадь Александра Невского 1'], ['Маяковская']]
markup_tunnel_alexander_nevsky_square_2 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_2,
                                                              one_time_keyboard=False)

reply_keyboard_tunnel_mayakovskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2']]
markup_tunnel_mayakovskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_mayakovskaya,
                                                 one_time_keyboard=False)

reply_tunnels_move = [['Идти дальше'], ['🐾Искать мутантов в тех. помещениях🐾', '🤬Искать мародёров в тех. помещениях🤬']]
markup_tunnels_move = ReplyKeyboardMarkup(reply_tunnels_move,
                                          one_time_keyboard=False)


def station_distributor(update, context):
    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
    current_fight = Fight(update, context)
    if data['fight_output']:
        fight_distributor(update, context)
    activities = {'Взять заказ на доставку': None, 'Выйти со станции': tunnels_choice,
                  'Осмотреть инвентарь': User(update, context).inventory,
                  'Арендовать домик на ночь: 35 патронов': sleep,
                  'Посмотреть карту': geocoder,

                  'Площадь Александра Невского 1': tunnels,
                  'Площадь Александра Невского 2': tunnels,
                  'Новочеркасская': tunnels,
                  'Маяковская': tunnels,

                  'Атаковать': current_fight.attack, 'Сбежать': current_fight.escape,

                  '🐾Искать мутантов в тех. помещениях🐾': Fight(update, context).init_fight,
                  'Идти дальше': Fight(update, context).init_fight
                  }

    current_station = Station(update, context)
    current_station.init_station(update, context)
    choice = update.message.text
    try:
        if choice == '🐾Искать мутантов в тех. помещениях🐾':
            with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
                data['fight_output'] = True
                data['question_output'] = True
                f.write(json.dumps(data))
        activities[choice](update, context)
    except TypeError:
        pass
    except KeyError:
        pass


def fight_distributor(update, context):
    current_fight = Fight(update, context)
    activities_fight = {'Атаковать': current_fight.attack, 'Сбежать': current_fight.escape}
    current_fight.init_fight(update, context)
    choice = update.message.text
    try:
        activities_fight[choice](update, context)
    except TypeError:
        pass
    except KeyError:
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
    owners = {'Новочеркасская': 'под контролем Альянса Оккервиль',
              'Площадь Александра Невского 1': 'под контролем Империи Веган',
              'Площадь Александра Невского 2': 'под контролем Империи Веган',
              'Маяковская': 'Независимая станция'}

    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
    station_choice = update.message.text
    if (data['station'] == 'Площадь Александра Невского 1' and station_choice == 'Площадь Александра Невского 2') or \
            (data['station'] == 'Площадь Александра Невского 2' and station_choice == 'Площадь Александра Невского 1'):
        update.message.reply_text("Вы без проблем проходите переход между станциями.",
                                  reply_markup=markup_station)

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['station'] = station_choice
            data['owner'] = owners[station_choice]
            f.write(json.dumps(data))
    else:
        update.message.reply_text("Вы идёте по тоннелям.")
        # random_tunnel = random.randint(0, 2)
        update.message.reply_text("Вы без проблем проходите через тоннель.", reply_markup=markup_tunnels_move)

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['station'] = station_choice
            data['owner'] = owners[station_choice]
            data['question_output'] = False
            f.write(json.dumps(data))


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
        api_requests[data['station']]
    )
