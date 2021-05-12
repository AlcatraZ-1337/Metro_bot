import json

from telegram import ReplyKeyboardMarkup

from classes import User, Station, markup_station, Fight, Trade

reply_keyboard_tunnel_novocherkasskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2']]
markup_tunnel_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_novocherkasskaya,
                                                     one_time_keyboard=False)

reply_keyboard_tunnel_alexander_nevsky_square_1 = [['Новочеркасская', 'Площадь Александра Невского 2'],
                                                   ['Маяковская']]
markup_tunnel_alexander_nevsky_square_1 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_1,
                                                              one_time_keyboard=False)

reply_keyboard_tunnel_alexander_nevsky_square_2 = [['Новочеркасская', 'Площадь Александра Невского 1'],
                                                   ['Лиговский проспект', 'Маяковская']]
markup_tunnel_alexander_nevsky_square_2 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_2,
                                                              one_time_keyboard=False)

reply_keyboard_tunnel_mayakovskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2']]
markup_tunnel_mayakovskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_mayakovskaya,
                                                 one_time_keyboard=False)

reply_keyboard_tunnel_vosstaniya_square = [['Маяковская', 'Владимирская']]
markup_tunnel_vosstaniya_square = ReplyKeyboardMarkup(reply_keyboard_tunnel_vosstaniya_square,
                                                      one_time_keyboard=False)

reply_keyboard_tunnel_ligovsky_avenue = [['Площадь Александра Невского 2', 'Владимирская']]
markup_tunnel_ligovsky_avenue = ReplyKeyboardMarkup(reply_keyboard_tunnel_ligovsky_avenue,
                                                    one_time_keyboard=False)

reply_keyboard_tunnel_vladimirskaya = [['Лиговский проспект', 'Площадь восстания']]
markup_tunnel_vladimirskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_vladimirskaya,
                                                  one_time_keyboard=False)

reply_tunnels_move = [['Идти дальше'], ['🐾Осмотреть тоннель🐾']]
markup_tunnels_move = ReplyKeyboardMarkup(reply_tunnels_move,
                                          one_time_keyboard=False)


def station_distributor(update, context):
    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    current_fight = Fight(update, context)
    if data['fight_output']:
        fight_distributor(update, context)
    if data['trade_output']:
        trade_distributor(update, context)
    activities = {'Поменяться предметами с жителями': trade_choice, 'Выйти со станции': tunnels_choice,
                  'Осмотреть инвентарь': User(update, context).inventory,
                  'Арендовать домик на ночь: 35 патронов': sleep,
                  'Посмотреть карту': geocoder,

                  'Площадь Александра Невского 1': tunnels,
                  'Площадь Александра Невского 2': tunnels,
                  'Новочеркасская': tunnels,
                  'Маяковская': tunnels,
                  'Площадь восстания': tunnels,
                  'Лиговский проспект': tunnels,
                  'Владимирская': tunnels,

                  'Атаковать': current_fight.attack, 'Сбежать': current_fight.escape,

                  '🐾Осмотреть тоннель🐾': Fight(update, context).init_fight,
                  'Идти дальше': Fight(update, context).init_fight
                  }

    current_station = Station(update, context)
    current_station.init_station(update, context)
    choice = update.message.text
    try:
        if choice == '🐾Осмотреть тоннель🐾':
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
                'Маяковская': markup_tunnel_mayakovskaya,
                'Площадь восстания': markup_tunnel_vosstaniya_square,
                'Лиговский проспект': markup_tunnel_ligovsky_avenue,
                'Владимирская': markup_tunnel_vladimirskaya}

    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    update.message.reply_text("Куда вы хотите пойти?", reply_markup=stations[data['station']])

    return 3


def tunnels(update, context):
    owners = {'Новочеркасская': 'под контролем Альянса Оккервиль',
              'Площадь Александра Невского 1': 'под контролем Империи Веган',
              'Площадь Александра Невского 2': 'под контролем Империи Веган',
              'Маяковская': 'под контролем Приморского альянса',
              'Площадь восстания': 'под контролем Бордюрщиков',
              'Лиговский проспект': 'Заброшенная станция',
              'Владимирская': 'Независимая станция'}

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
        update.message.reply_text("Вы идёте по тоннелям.", reply_markup=markup_tunnels_move)

        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['station'] = station_choice
            data['owner'] = owners[station_choice]
            data['question_output'] = False
            f.write(json.dumps(data))


def trade_distributor(update, context):
    trade_things_simple_stations = {'Улучшение пистолета': [40, 10, 30, 15, 0, 0],
                                    '🍖Еда🍖': [10, 0, 5, 0, 0, 0],
                                    '🔫Пять Патронов🔫': [0, 0, 5, 5, 0, 0]}
    trade_things_mayakovskaya = {'Улучшение обреза': [30, 10, 0, 0, 15, 20],
                                 '🍖Три еды🍖': [12, 0, 0, 0, 6, 0],
                                 '🔫Десять Патронов🔫': [0, 0, 0, 0, 6, 6]}
    items_exchange = {'🍖Еда🍖': 'food',
                      '🍖Три еды🍖': 'food',
                      '🔫Пять Патронов🔫': 'bullets',
                      '🔫Десять Патронов🔫': 'bullets',
                      'Улучшение пистолета': 'attack',
                      'Улучшение обреза': 'attack'}
    number_items_exchange = {'🍖Еда🍖': 1,
                             '🍖Три еды🍖': 3,
                             '🔫Пять Патронов🔫': 5,
                             '🔫Десять Патронов🔫': 10,
                             'Улучшение пистолета': 5,
                             'Улучшение обреза': 10}

    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    choice = update.message.text

    if data['station'] != 'Маяковская':
        cost = trade_things_simple_stations[choice]
        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['question_output'] = True
            data['trade_output'] = False

            if data['bullets'] >= cost[0] and data['food'] >= cost[1] and data['trade_item_1'] >= cost[2] and \
                    data['trade_item_2'] >= cost[3]:
                data[items_exchange[choice]] = data[items_exchange[choice]] + number_items_exchange[choice]

                data['bullets'] = data['bullets'] - cost[0]
                data['food'] = data['food'] - cost[1]

                data['trade_item_1'] = data['trade_item_1'] - cost[2]
                data['trade_item_2'] = data['trade_item_2'] - cost[3]
                update.message.reply_text(f"Вы успешно купили: {choice}")

            else:
                update.message.reply_text(f"Обмен не удался!!! Нехватает предметов.")
            f.write(json.dumps(data))

    else:
        cost = trade_things_mayakovskaya[choice]
        with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
            data['question_output'] = True
            data['trade_output'] = False

            if data['bullets'] >= cost[0] and data['food'] >= cost[1] and data['trade_item_3'] >= cost[4] and \
                    data['trade_item_4'] >= cost[5]:
                data[items_exchange[choice]] = data[items_exchange[choice]] + number_items_exchange[choice]

                data['bullets'] = data['bullets'] - cost[0]
                data['food'] = data['food'] - cost[1]

                data['trade_item_3'] = data['trade_item_3'] - cost[4]
                data['trade_item_4'] = data['trade_item_4'] - cost[5]
                update.message.reply_text(f"Вы успешно купили: {choice}")

            else:
                update.message.reply_text(f"Обмен не удался!!! Нехватает предметов.")
            f.write(json.dumps(data))


def trade_choice(update, context):
    current_trade = Trade(update, context)
    current_trade.init_trade(update, context)

    with open(f'main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
        data['question_output'] = False
        data['trade_output'] = True
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
                                  f"0.5,0.5&l=map&pt=30.355314,59.931386,pm2rdl",
                    'Площадь восстания': f'http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn='
                                         f'0.5,0.5&l=map&pt=30.361534,59.931057,pm2rdl',
                    'Лиговский проспект': f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn="
                                          f"0.5,0.5&l=map&pt=30.342606,59.971093,pm2rdl",
                    'Владимирская': f'http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn='
                                    f'0.5,0.5&l=map&pt=30.348208,59.927432,pm2rdl'}
    context.bot.send_photo(
        update.message.chat_id,
        api_requests[data['station']]
    )
