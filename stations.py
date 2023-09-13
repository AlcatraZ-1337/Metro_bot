import json
import random
import time
import pymorphy2
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from classes import User, Station, markup_station, Fight, Trade, Rat_game, markup_vladimirskaya
from started_functions import name_input

reply_keyboard_tunnel_novocherkasskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2'],
                                          ['Весёлый посёлок']]
markup_tunnel_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_tunnel_novocherkasskaya,
                                                     one_time_keyboard=False)

reply_keyboard_tunnel_alexander_nevsky_square_1 = [['Новочеркасская', 'Площадь Александра Невского 2'],
                                                   ['Маяковская']]
markup_tunnel_alexander_nevsky_square_1 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_1,
                                                              one_time_keyboard=False)

reply_keyboard_tunnel_alexander_nevsky_square_2 = [['Новочеркасская', 'Площадь Александра Невского 1'],
                                                   ['Лиговский проспект']]
markup_tunnel_alexander_nevsky_square_2 = ReplyKeyboardMarkup(reply_keyboard_tunnel_alexander_nevsky_square_2,
                                                              one_time_keyboard=False)

reply_keyboard_tunnel_mayakovskaya = [['Площадь Александра Невского 1', 'Площадь Александра Невского 2'],
                                      ['Площадь восстания']]
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

reply_keyboard_tunnel_merry_village = [['Новочеркасская']]
markup_tunnel_merry_village = ReplyKeyboardMarkup(reply_keyboard_tunnel_merry_village,
                                                  one_time_keyboard=False)

reply_tunnels_move = [['Идти дальше'], ['🐾Осмотреть тоннель🐾']]
markup_tunnels_move = ReplyKeyboardMarkup(reply_tunnels_move,
                                          one_time_keyboard=False)


def station_distributor(update, context):
    try:
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        update.message.reply_text("❌ Похоже, что вы удалили свой файл сохранения! ❌")
        name_input(update, context)
        return 1

    if data['fight_output']:
        fight_distributor(update, context)
    if data['trade_output']:
        trade_distributor(update, context)
    if data['rat_game_output'][0]:
        if data['rat_game_output'][1]:
            primary_rat_game_distributor(update, context)
        else:
            rat_game_distributor(update, context)

    activities = {'Поменяться предметами с жителями': trade_choice,
                  'Выйти со станции': tunnels_choice,
                  'Осмотреть инвентарь': User(update, context).inventory,
                  'Арендовать домик: 35 патронов': sleep,
                  'Посмотреть карту': geocoder,
                  'Постоять на станции (Послушать музыку)': station_music,
                  'Сыграть в Кости: 25 патронов': dice,
                  'Сделать ставку на крысиных бегах': rat_game_choice,

                  'Новочеркасская': tunnels,
                  'Площадь Александра Невского 1': tunnels,
                  'Площадь Александра Невского 2': tunnels,
                  'Маяковская': tunnels,
                  'Площадь восстания': tunnels,
                  'Лиговский проспект': tunnels,
                  'Владимирская': tunnels,
                  'Весёлый посёлок': tunnels,

                  '🐾Осмотреть тоннель🐾': Fight(update, context).init_fight,
                  'Осмотреть станцию': Fight(update, context).init_fight,
                  'Идти дальше': Fight(update, context).init_fight}

    current_station = Station(update, context)
    current_station.init_station(update, context)
    choice = update.message.text
    try:
        if choice == '🐾Осмотреть тоннель🐾':
            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['fight_output'] = True
                data['question_output'] = True
                f.write(json.dumps(data))
        activities[choice](update, context)
    except TypeError:
        pass
    except KeyError:
        pass


def station_music(update, context):
    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)
        with open(f'Audio-data\{data["station"]}.mp3', 'rb') as ambient:
            update.message.reply_audio(ambient, title=data['station'])


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
                'Владимирская': markup_tunnel_vladimirskaya,
                'Весёлый посёлок': markup_tunnel_merry_village}

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    update.message.reply_text("Куда вы хотите пойти?", reply_markup=stations[data['station']])


def tunnels(update, context):
    owners = {'Новочеркасская': '🛡Под контролем Альянса Оккервиль🛡',
              'Площадь Александра Невского 1': '🛡Под контролем Империи Веган🛡',
              'Площадь Александра Невского 2': '🛡Под контролем Империи Веган🛡',
              'Маяковская': '🛡Под контролем Приморского альянса🛡',
              'Площадь восстания': '🛡Под контролем Бордюрщиков🛡',
              'Лиговский проспект': '☠Заброшенная станция☠',
              'Владимирская': '🪖Независимая станция🪖',
              'Весёлый посёлок': '🍄Под контролем Грибников🍄'}

    dangers = {'Новочеркасская': '✅ Отсутствуют ✅',
               'Площадь Александра Невского 1': '✅ Отсутствуют ✅',
               'Площадь Александра Невского 2': '✅ Отсутствуют ✅',
               'Маяковская': '✅ Отсутствуют ✅',
               'Площадь восстания': '✅ Отсутствуют ✅',
               'Лиговский проспект': '⚠ Биологическая опасность ⚠',
               'Владимирская': '✅ Отсутствуют ✅',
               'Весёлый посёлок': '✅ Отсутствуют ✅'}

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    station_choice = update.message.text
    if (data['station'] == 'Площадь Александра Невского 1' and station_choice == 'Площадь Александра Невского 2') or \
            (data['station'] == 'Площадь Александра Невского 2' and station_choice == 'Площадь Александра Невского 1') \
            or (data['station'] == 'Маяковская' and station_choice == 'Площадь восстания') \
            or (data['station'] == 'Площадь восстания' and station_choice == 'Маяковская') \
            or (data['station'] == 'Новочеркасская' and station_choice == 'Весёлый посёлок') \
            or (data['station'] == 'Весёлый посёлок' and station_choice == 'Новочеркасская'):
        update.message.reply_text("Вы без проблем проходите переход между станциями.",
                                  reply_markup=markup_station)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['station'] = station_choice
            data['owner'] = owners[station_choice]
            data['danger'] = dangers[station_choice]
            f.write(json.dumps(data))

    elif ((data['station'] == 'Площадь Александра Невского 1' and station_choice == 'Маяковская') or
          (data['station'] == 'Площадь Александра Невского 2' and station_choice == 'Лиговский проспект')) and \
            data['attack'] < 20:
        update.message.reply_text("🚷 У вас слишком слабое снаряжение, чтобы идти дальше! 🚷\n"
                                  "Чтобы пройти вам необходимо повысить ваш показатель\n"
                                  "урона минимум до: 🔪20 ед.\n"
                                  f"Текущий показатель урона: 🔪{data['attack']} ед.",
                                  reply_markup=markup_station)
    else:
        update.message.reply_text("Вы идёте по тоннелям.", reply_markup=markup_tunnels_move)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['station'] = station_choice
            data['owner'] = owners[station_choice]
            data['danger'] = dangers[station_choice]
            data['question_output'] = False
            f.write(json.dumps(data))


def trade_distributor(update, context):
    normal_trade_stations = ['Маяковская', 'Владимирская', 'Площадь восстания']
    drug_station = 'Весёлый посёлок'

    trade_things_simple_stations = {'Улучшение пистолета': [40, 10, 30, 15, 0, 0],
                                    '🍖Еда🍖': [10, 0, 5, 0, 0, 0],
                                    '🔫Пять Патронов🔫': [0, 0, 5, 5, 0, 0]}
    trade_things_mayakovskaya = {'Улучшение обреза': [30, 10, 0, 0, 15, 20],
                                 '🍖Три еды🍖': [12, 0, 0, 0, 6, 0],
                                 '🔫Десять Патронов🔫': [0, 0, 0, 0, 6, 6]}
    trade_things_drug_station = {
        '💊Витаминки💊 🪴': [0, 0, 15, 0, 15, 0],
        'Витаминки💊 \U0001fab5': [0, 0, 0, 10, 0, 10],
        '💊Витаминки💊 🥩': [0, 20, 0, 0, 0, 0]}

    items_exchange = {'🍖Еда🍖': 'food',
                      '🍖Три еды🍖': 'food',
                      '🔫Пять Патронов🔫': 'bullets',
                      '🔫Десять Патронов🔫': 'bullets',
                      'Улучшение пистолета': 'attack',
                      'Улучшение обреза': 'attack',
                      '💊Витаминки💊 🪴': 'trade_item_5',
                      'Витаминки💊 \U0001fab5': 'trade_item_5',
                      '💊Витаминки💊 🥩': 'trade_item_5'}
    number_items_exchange = {'🍖Еда🍖': 1,
                             '🍖Три еды🍖': 3,
                             '🔫Пять Патронов🔫': 5,
                             '🔫Десять Патронов🔫': 10,
                             'Улучшение пистолета': 5,
                             'Улучшение обреза': 10,
                             '💊Витаминки💊 🪴': 1,
                             'Витаминки💊 \U0001fab5': 1,
                             '💊Витаминки💊 🥩': 1}

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    choice = update.message.text

    if choice != 'Ничего не покупать':
        if data['station'] not in normal_trade_stations:
            if data['station'] != drug_station:
                cost = trade_things_simple_stations[choice]

                with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                    data['question_output'] = True
                    data['trade_output'] = False

                    if data['bullets'] >= cost[0] and data['food'] >= cost[1] and data['trade_item_1'] >= cost[2] and \
                            data['trade_item_2'] >= cost[3]:
                        data[items_exchange[choice]] = data[items_exchange[choice]] + number_items_exchange[choice]

                        data['bullets'] = data['bullets'] - cost[0]
                        data['food'] = data['food'] - cost[1]

                        data['trade_item_1'] = data['trade_item_1'] - cost[2]
                        data['trade_item_2'] = data['trade_item_2'] - cost[3]
                        update.message.reply_text(f"✅ Вы успешно купили: {choice}. ✅")

                    else:
                        update.message.reply_text(f"⚠ Обмен не удался!!! Нехватает предметов. ⚠")
                    f.write(json.dumps(data))
            else:
                cost = trade_things_drug_station[choice]

                with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                    data['question_output'] = True
                    data['trade_output'] = False

                    if data['bullets'] >= cost[0] and data['food'] >= cost[1] and data['trade_item_1'] >= cost[2] and \
                            data['trade_item_2'] >= cost[3] and data['trade_item_3'] >= cost[4] and \
                            data['trade_item_4'] >= cost[5]:
                        data[items_exchange[choice]] = data[items_exchange[choice]] + number_items_exchange[choice]

                        data['bullets'] = data['bullets'] - cost[0]
                        data['food'] = data['food'] - cost[1]

                        data['trade_item_1'] = data['trade_item_1'] - cost[2]
                        data['trade_item_2'] = data['trade_item_2'] - cost[3]
                        data['trade_item_3'] = data['trade_item_3'] - cost[4]
                        data['trade_item_4'] = data['trade_item_4'] - cost[5]

                        update.message.reply_text(f"✅ Вы успешно купили: {choice}. ✅")

                    else:
                        update.message.reply_text(f"⚠ Обмен не удался!!! Нехватает предметов. ⚠")
                    f.write(json.dumps(data))

        else:
            cost = trade_things_mayakovskaya[choice]
            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = True
                data['trade_output'] = False

                if data['bullets'] >= cost[0] and data['food'] >= cost[1] and data['trade_item_3'] >= cost[4] and \
                        data['trade_item_4'] >= cost[5]:
                    data[items_exchange[choice]] = data[items_exchange[choice]] + number_items_exchange[choice]

                    data['bullets'] = data['bullets'] - cost[0]
                    data['food'] = data['food'] - cost[1]

                    data['trade_item_3'] = data['trade_item_3'] - cost[4]
                    data['trade_item_4'] = data['trade_item_4'] - cost[5]

                    update.message.reply_text(f"✅ Вы успешно купили: {choice}. ✅")

                else:
                    update.message.reply_text(f"⚠ Обмен не удался!!! Нехватает предметов. ⚠")
                f.write(json.dumps(data))
    else:
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['question_output'] = True
            data['trade_output'] = False
            update.message.reply_text(f"❌ Вы отказались поменяться вещами. ❌")
            f.write(json.dumps(data))


def trade_choice(update, context):
    current_trade = Trade(update, context)
    current_trade.init_trade(update, context)

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
        data['question_output'] = False
        data['trade_output'] = True
        f.write(json.dumps(data))


def primary_rat_game_distributor(update, context):
    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data1 = json.load(f)

    with open(f'JSON-data\games_in_metro{update.message.chat_id}.json', 'r') as g:
        data2 = json.load(g)

    choice = update.message.text
    if choice == 'Ни на кого не ставить':
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data1['question_output'] = True
            data1['rat_game_output'][0] = False
            data1['rat_game_output'][1] = False
            update.message.reply_text(f"❌ Вы отказались делать ставку. ❌")
            f.write(json.dumps(data1))
    else:
        update.message.reply_text("Выберите размер ставки.",
                                  reply_markup=ReplyKeyboardMarkup([['🔫 25 патронов 🔫', '🔫 50 патронов 🔫',
                                                                     '🔫 100 патронов 🔫'], ['🔫 150 патронов 🔫']],
                                                                   one_time_keyboard=True))
        with open(f'JSON-data\games_in_metro{update.message.chat_id}.json', 'w') as g:
            data2['player_choice'] = choice
            g.write(json.dumps(data2))
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data1['rat_game_output'][1] = False
            f.write(json.dumps(data1))


def rat_game_distributor(update, context):
    choice = update.message.text

    bets = {'🔫 25 патронов 🔫': 25, '🔫 50 патронов 🔫': 50, '🔫 100 патронов 🔫': 100, '🔫 150 патронов 🔫': 150}

    if choice in bets:
        update.message.reply_text(f"Вы поставили: {choice}.")

        player_bet = bets[choice]

        with open(f'JSON-data\games_in_metro{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)
            first_rat, second_rat, third_rat, fourth_rat, fifth_rat, player_choice = \
                (data[i] for i in data)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['bullets'] = data['bullets'] - bets[choice]
            f.write(json.dumps(data))

        race_time = random.randint(15, 35)
        update.message.reply_text(f"Данный забег будет длиться: ⏰ {race_time} секунд ⏰\n"
                                  f"Возращайтесь, когда забег будет завершён.")
        time.sleep(race_time)
        rat_game_calculation(update, context, first_rat, second_rat, third_rat, fourth_rat, fifth_rat,
                             player_choice, player_bet)
    else:
        update.message.reply_text("У вас недостаточно патронов, чтобы сделать ставку!!!")

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['question_output'] = True
            data['rat_game_output'][0] = False
            data['rat_game_output'][1] = False
            f.write(json.dumps(data))


def rat_game_choice(update, context):
    current_rat_game = Rat_game(update, context)
    current_rat_game.init_rat_game(update, context)

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
        data['question_output'] = False
        data['rat_game_output'][0] = True
        data['rat_game_output'][1] = True
        f.write(json.dumps(data))


def rat_game_calculation(update, content, first_rat, second_rat, third_rat, fourth_rat, fifth_rat, player_choice,
                         player_bet):
    morph = pymorphy2.MorphAnalyzer()
    bets_on_rats = {
        f'Поставить на {morph.parse("".join(c for c in first_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}':
            first_rat[0],
        f'Поставить на {morph.parse("".join(c for c in second_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}':
            second_rat[0],
        f'Поставить на {morph.parse("".join(c for c in third_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}':
            third_rat[0],
        f'Поставить на {morph.parse("".join(c for c in fourth_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}':
            fourth_rat[0],
        f'Поставить на {morph.parse("".join(c for c in fifth_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}':
            fifth_rat[0]
    }
    rats_names = [first_rat[0], second_rat[0], third_rat[0], fourth_rat[0], fifth_rat[0]]
    rats_chances = [first_rat[1], second_rat[1], third_rat[1], fourth_rat[1], fifth_rat[1]]

    first_place, second_place, third_place = '', '', ''
    coincidence = True
    while coincidence:
        first_place, second_place, third_place = (random.choices(rats_names, weights=rats_chances) for _ in range(3))
        places_check = [first_place[0], second_place[0], third_place[0]]
        unique_places_check = set(places_check)
        if len(unique_places_check) == len(places_check):
            coincidence = False
        else:
            coincidence = True

    if first_place[0] == bets_on_rats[player_choice]:
        update.message.reply_text("Крысиные бега завершены.\n"
                                  "🥇 Ваша крыса пришла к финишу первой 🥇\n"
                                  f"Ваш выигрыш составляет: 🔫 {player_bet * 3} патронов🔫.",
                                  reply_markup=markup_vladimirskaya)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['bullets'] = data['bullets'] + (player_bet * 3)
            data['question_output'] = True
            data['rat_game_output'][0] = False
            f.write(json.dumps(data))

    elif second_place[0] == bets_on_rats[player_choice]:
        update.message.reply_text("Крысиные бега завершены.\n"
                                  "🥈 Ваша крыса пришла к финишу второй 🥈\n"
                                  f"Ваш выигрыш составляет: 🔫 {player_bet * 2} патронов🔫.",
                                  reply_markup=markup_vladimirskaya)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['bullets'] = data['bullets'] + (player_bet * 2)
            data['question_output'] = True
            data['rat_game_output'][0] = False
            f.write(json.dumps(data))

    elif third_place[0] == bets_on_rats[player_choice]:
        update.message.reply_text("Крысиные бега завершены.\n"
                                  "🥉 Ваша крыса пришла к финишу третьей 🥉\n"
                                  f"Вы смогли лишь отбить свою ставку в 🔫  {player_bet} патронов🔫.",
                                  reply_markup=markup_vladimirskaya)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['bullets'] = data['bullets'] + player_bet
            data['question_output'] = True
            data['rat_game_output'][0] = False
            f.write(json.dumps(data))

    else:
        update.message.reply_text("Крысиные бега завершены.\n"
                                  "Ваша крыса не заняла никаких призовых мест.", reply_markup=markup_vladimirskaya)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['question_output'] = True
            data['rat_game_output'][0] = False
            f.write(json.dumps(data))

    update.message.reply_text(f"🥇 1 место: {first_place[0]}\n"
                              f"🥈 2 место: {second_place[0]}\n"
                              f"🥉 3 место: {third_place[0]}")

    os.remove(f'JSON-data\games_in_metro{update.message.chat_id}.json')


def sleep(update, content):
    update.message.reply_text("♥ Во время сна вы полностью восстановили своё здоровье ♥")

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
        data['health'] = 100
        data['bullets'] = data['bullets'] - 35
        f.write(json.dumps(data))


def geocoder(update, context):
    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
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
                                    f'0.5,0.5&l=map&pt=30.348208,59.927432,pm2rdl',
                    'Весёлый посёлок': f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn=0.5,0.5&l=map&pt="
                                       f"30.483364,59.907439,pm2rdl"}
    context.bot.send_photo(
        update.message.chat_id,
        api_requests[data['station']], f"Текущая станция:\n"
                                       f"☢ {data['station']} ☢")


def dice(update, context):
    update.message.reply_text("🎲 Вы решили сыграть в Кости с местными жителями 🎲.\n", reply_markup=ReplyKeyboardRemove())

    time.sleep(2)
    update.message.reply_text("🔴 Ваш бросок: 🔴\n")
    player_result = update.message.reply_dice()
    player_result = player_result['dice']['value']
    time.sleep(5)

    update.message.reply_text("🔵 Бросок соперника: 🔵\n")
    ai_result = update.message.reply_dice()
    ai_result = ai_result['dice']['value']
    time.sleep(5)

    update.message.reply_text(f"🔴 Ваш результат: {player_result} 🔴.\n"
                              f"🔵 Результат соперника: {ai_result} 🔵.\n")

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
        data = json.load(f)

    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
        if player_result < ai_result:
            data['bullets'] = data['bullets'] - 25
            update.message.reply_text("🔵 Вы проиграли! 🔵\n"
                                      "🔫 Вы потеряли: 25 патронов 🔫.", reply_markup=markup_station)
        elif player_result > ai_result:
            data['bullets'] = data['bullets'] + 25
            update.message.reply_text("🔴 Вы выиграли! 🔴 \n"
                                      "🔫 Вы получили: 25 патронов 🔫.", reply_markup=markup_station)
        else:
            update.message.reply_text("🔴 Ничья 🔵.", reply_markup=markup_station)

        time.sleep(1)
        f.write(json.dumps(data))
