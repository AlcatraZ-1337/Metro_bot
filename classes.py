import json
import random
import time

import datetime

import pymorphy2
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

from started_functions import txt_reader


class User:
    def __init__(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
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
        self.trade_item_5 = data['trade_item_5']

        self.station = data['station']

    def inventory(self, update, context):
        update.message.reply_text(
            "Ваш инвентарь: \n"
            "\n"
            f"Ваше имя: {self.name} \n"
            f"♥ Ваше здоровье: {self.health} ♥\n"
            f"🔪 Ваш урон: {self.attack} 🔪\n"
            "\n"
            f"🔫 Ваши патроны: {self.bullets} 🔫\n"
            f"🍖 Ваш запас провианта: {self.food} 🍖\n"
            "\n"
            "Ваши предметы для бартера: \n"
            f"🍄 Кислик: {self.trade_item_1} 🍄\n"
            f"🧼 Тунельный камень: {self.trade_item_2} 🧼\n"
            f"🌿 Ржавая трава: {self.trade_item_3} 🌿\n"
            f"🛢 Керосин: {self.trade_item_4} 🛢\n"
            f"💊 Витаминки: {self.trade_item_5} 💊\n"
            f"\n"
            f"☢ Текущая станция: {self.station} ☢")


class Station:
    def __init__(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.station_name = data['station']
        self.owner = data['owner']
        self.danger = data['danger']
        self.question_output = data['question_output']
        self.fight_output = data['fight_output']

    def init_station(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        time = int(str(datetime.datetime.time(datetime.datetime.today())).split(':')[0])
        if (time >= 18) or (time <= 7):
            time = '🌙 Ночь 🌙'
        else:
            time = '☀ День ☀'

        if self.question_output:
            if data['station'] != 'Лиговский проспект':
                if data['station'] == 'Владимирская':
                    update.message.reply_text(f'Вы находитесь на станции:\n'
                                              f'☢ {self.station_name} ☢.\n'
                                              f'Статус станции: {self.owner}.\n'
                                              f'Угрозы жизни на станции: {self.danger}. \n'
                                              f'Текущее время: ⏰ {str(datetime.datetime.time(datetime.datetime.today())).split(".")[0]} ⏰.\n'
                                              f'В данный момент на станции {time}.\n'
                                              f'Что вы хотите сделать?')
                    update.message.reply_text('🐀 На станции проводятся крысиные бега!!! 🐀',
                                              reply_markup=markup_vladimirskaya)
                else:
                    update.message.reply_text(f'Вы находитесь на станции:\n'
                                              f'☢ {self.station_name} ☢.\n'
                                              f'Статус станции: {self.owner}.\n'
                                              f'Угрозы жизни на станции: {self.danger}. \n'
                                              f'Текущее время: ⏰ {str(datetime.datetime.time(datetime.datetime.today())).split(".")[0]} ⏰.\n'
                                              f'В данный момент на станции {time}.\n'
                                              f'Что вы хотите сделать?', reply_markup=markup_station)
            else:
                update.message.reply_text(f'Вы находитесь на станции:\n'
                                          f'☢ {self.station_name} ☢.\n'
                                          f'Статус станции: {self.owner}.\n'
                                          f'Угрозы жизни на станции: {self.danger}. \n'
                                          f'Текущее время: ⏰ {str(datetime.datetime.time(datetime.datetime.today())).split(".")[0]} ⏰.\n'
                                          f'В данный момент на станции {time}.\n'
                                          f'Что вы хотите сделать?', reply_markup=markup_dead_station)

            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = False
                f.write(json.dumps(data))
        else:
            pass


class Fight:
    def __init__(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        time = int(str(datetime.datetime.time(datetime.datetime.today())).split(':')[0])
        if (time >= 18) or (time <= 7):
            enemy_dict = {'ghoul': (random.randint(60, 100), 'Ночного Упыря'),
                          'guardian': (random.randint(70, 110), 'Ночного Стража'),
                          'marauder': (random.randint(40, 80), 'Сонного Мародёра'),
                          'nosey': (random.randint(80, 120), 'Ночного Носача'),
                          'toxic_ghoul': (random.randint(80, 90), '🟢 Плевуна 🟢')}
        else:
            enemy_dict = {'ghoul': (random.randint(40, 80), 'Упыря'),
                          'guardian': (random.randint(50, 90), 'Стража'),
                          'marauder': (random.randint(60, 100), 'Мародёра'),
                          'nosey': (random.randint(60, 100), 'Носача'),
                          'toxic_ghoul': (random.randint(70, 80), '🟢 Плевуна 🟢')}

        self.health = data['health']
        self.damage = data['attack']

        if data['danger'] != '⚠ Биологическая опасность ⚠':
            if 15 <= self.damage < 20:
                self.enemy_mutant, self.enemy = enemy_dict['ghoul']
            elif 20 <= self.damage <= 25:
                self.enemy_mutant, self.enemy = enemy_dict['guardian']
            else:
                enemy_choice = random.choice(['marauder', 'nosey'])
                self.enemy_mutant, self.enemy = enemy_dict[enemy_choice]
        else:
            if 15 <= self.damage < 20:
                self.enemy_mutant, self.enemy = enemy_dict['guardian']
            else:
                self.enemy_mutant, self.enemy = enemy_dict['toxic_ghoul']

    def init_fight(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        choice = update.message.text

        if choice == 'Осмотреть станцию' and data['station'] == 'Лиговский проспект':
            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = True
                data['fight_output'] = True
                f.write(json.dumps(data))

        if data['question_output'] and choice != 'Идти дальше':
            update.message.reply_text(f'🐾Вы встретили {self.enemy}🐾. \n'
                                      f'♥Его текущее здоровье: {self.enemy_mutant}♥. \n'
                                      f'♥Ваше текущее здоровье: {self.health}♥. \n'
                                      f'Что вы будете делать?', reply_markup=markup_fight_choice)

            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = False
                f.write(json.dumps(data))

        elif choice == 'Идти дальше':
            update.message.reply_text('Вы прошли через тоннель.',
                                      reply_markup=ReplyKeyboardMarkup([['Выйти на станцию']], one_time_keyboard=False))

            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['fight_output'] = False
                data['question_output'] = True
                f.write(json.dumps(data))

    def attack(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        while self.enemy_mutant > 0 and self.health > 0:
            if self.enemy_mutant > 0:
                self.enemy_mutant -= self.damage
                if self.enemy != '🟢 Плевуна 🟢':
                    enemy_damage = random.randint(0, 5)
                else:
                    enemy_damage = random.randint(5, 10)
                self.health -= enemy_damage

            if self.enemy_mutant <= 0 and data['fight_output']:
                if self.enemy == '🟢 Плевуна 🟢':
                    self.health -= 10
                    update.message.reply_text(f'Вы получили урон от яда в размере: 💚 10 ед. 💚\n')
                if self.health > 0:
                    stations = {'Площадь Александра Невского 1': ['trade_item_1', 'trade_item_2'],
                                'Площадь Александра Невского 2': ['trade_item_1', 'trade_item_2'],
                                'Новочеркасская': ['trade_item_1', 'trade_item_2'],
                                'Маяковская': ['trade_item_3', 'trade_item_4'],
                                'Площадь восстания': ['trade_item_3', 'trade_item_4'],
                                'Лиговский проспект': ['bullets', 'food'],
                                'Владимирская': ['trade_item_3', 'trade_item_4']}
                    item_name = {'trade_item_1': '🍄Кислик🍄', 'trade_item_2': '🧼Тунельный камень🧼',
                                 'trade_item_3': '🌿Ржавая трава🌿', 'trade_item_4': '🛢Керосин🛢',
                                 'bullets': '🔫Патроны🔫',
                                 'food': '🍖Еда🍖'}
                    trade_item_1, trade_item_2 = stations[data["station"]]

                    if data['station'] != 'Лиговский проспект':
                        if self.enemy == 'Упыря' or 'Ночного Упыря':
                            quantity_trade_item_1_from_battle = random.randint(5, 12)
                            quantity_trade_item_2_from_battle = random.randint(3, 8)

                        elif self.enemy == 'Стража' or 'Ночного Стража':
                            quantity_trade_item_1_from_battle = random.randint(8, 16)
                            quantity_trade_item_2_from_battle = random.randint(6, 12)

                        elif (self.enemy == 'Мародёра' or 'Сонного Мародёра') or \
                                (self.enemy == 'Носача' or 'Ночного Носача'):
                            quantity_trade_item_1_from_battle = random.randint(12, 20)
                            quantity_trade_item_2_from_battle = random.randint(10, 16)
                    else:
                        if self.enemy == 'Упыря' or 'Ночного Упыря':
                            quantity_trade_item_1_from_battle = random.randint(5, 12)
                            quantity_trade_item_2_from_battle = random.randint(1, 3)

                        elif self.enemy == 'Стража' or 'Ночного Стража':
                            quantity_trade_item_1_from_battle = random.randint(8, 16)
                            quantity_trade_item_2_from_battle = random.randint(2, 4)

                        elif (self.enemy == 'Мародёра' or 'Сонного Мародёра') or \
                                (self.enemy == 'Носача' or 'Ночного Носача'):
                            quantity_trade_item_1_from_battle = random.randint(12, 20)
                            quantity_trade_item_2_from_battle = random.randint(3, 5)

                        elif self.enemy == '🟢 Плевуна 🟢':
                            quantity_trade_item_1_from_battle = random.randint(20, 26)
                            quantity_trade_item_2_from_battle = random.randint(5, 8)

                    quantity_trade_item_1, quantity_trade_item_2 = \
                        data[trade_item_1] + quantity_trade_item_1_from_battle, \
                        data[trade_item_2] + quantity_trade_item_2_from_battle
                    trade_item_1, trade_item_2 = item_name[trade_item_1], item_name[trade_item_2]
                    update.message.reply_text(f'Вы успешно справились с противником.\n'
                                              f'Вы получили: {quantity_trade_item_1_from_battle} {trade_item_1} и '
                                              f'{quantity_trade_item_2_from_battle} {trade_item_2}.\n'
                                              f'♥ Ваше здоровье после битвы: {self.health} ♥.')

                    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                        item_name = {'🍄Кислик🍄': 'trade_item_1', '🧼Тунельный камень🧼': 'trade_item_2',
                                     '🌿Ржавая трава🌿': 'trade_item_3', '🛢Керосин🛢': 'trade_item_4',
                                     '🔫Патроны🔫': 'bullets', '🍖Еда🍖': 'food'}
                        data['health'] = self.health
                        data[item_name[trade_item_1]] = quantity_trade_item_1
                        data[item_name[trade_item_2]] = quantity_trade_item_2
                        data['fight_output'] = False
                        data['question_output'] = True
                        f.write(json.dumps(data))

            if self.health <= 0:
                update.message.reply_text('Во время битвы вы потеряли сознание, из-за полученных ранений.\n'
                                          'Вас нашли сталкеры с Новочеркасской и доставили к себе на станцию.\n'
                                          '🔫Вы потеряли: 50 патронов.🔫')

                with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                    self.health = 100
                    data['health'] = self.health
                    data['bullets'] = data['bullets'] - 50
                    if data['bullets'] < 0:
                        data['bullets'] = 0
                    data['station'] = 'Новочеркасская'
                    data['owner'] = 'Альянс Оккервиль'
                    data['danger'] = '✅ Отсутствуют ✅'
                    data['fight_output'] = False
                    data['question_output'] = True
                    f.write(json.dumps(data))

    def escape(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        if data['fight_output']:
            update.message.reply_text(f'Вы успешно сбежали.')
            self.enemy_mutant = 0

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
            data['fight_output'] = False
            data['question_output'] = True
            f.write(json.dumps(data))


class Trade:
    def __init__(self, update, context):

        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.station = data['station']

    def init_trade(self, update, context):
        normal_stations = ['Маяковская', 'Владимирская', 'Площадь восстания']
        drug_station = 'Весёлый посёлок'
        if self.station not in normal_stations:
            if self.station != drug_station:
                update.message.reply_text(f'Жители станции ☢ {self.station} ☢ могут обменять следующие товары: \n'
                                          '\n'
                                          'Улучшение пистолета: \n'
                                          '🔫40 патронов🔫, 🍖10 еды🍖, 🍄30 Кисликов🍄\n'
                                          'и 🧼15 Тунельных камней🧼. \n'
                                          '🔫Пять Патронов🔫: \n'
                                          '🍄5 Кисликов🍄 и 🧼5 Тунельных камней🧼. \n'
                                          '\n'
                                          'Что вы будете делать?', reply_markup=markup_trade_things_simple_stations)
            else:
                update.message.reply_text(f'Барыги станции ☢ {self.station} ☢ могут предложить следующие товары: \n'
                                          '\n'
                                          '💊Витаминки💊 🪴: \n'
                                          '🍄15 Кисликов🍄 и 🌿15 Ржавой травы🌿. \n'
                                          '💊Витаминки💊 🪵: \n'
                                          '🧼10 Тунельных камней🧼 и 🛢10 Керосина🛢. \n'
                                          '💊Витаминки💊 🥩: \n'
                                          '🍖20 Провианта🍖 \n'
                                          '\n'
                                          'Что вы будете делать?', reply_markup=markup_trade_things_drug_station)
        else:
            update.message.reply_text(f'Жители станции ☢ {self.station} ☢ могут обменять следующие товары: \n'
                                      '\n'
                                      'Улучшение обреза: \n'
                                      '🔫30 патронов🔫, 🍖10 еды🍖,\n'
                                      '🌿15 Ржавой травы🌿 и 🛢20 Керосина🛢. \n'
                                      '🔫Десять Патронов🔫: \n'
                                      '🌿6 Ржавой травы🌿 и 🛢6 Керосина🛢. \n'
                                      '\n'
                                      'Что вы будете делать?', reply_markup=markup_trade_things_normal_stations)


class Rat_game:
    def __init__(self, update, context):
        with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
            data = json.load(f)

        self.station = data['station']

    def init_rat_game(self, update, context):
        coincidence = True
        rat_game_stations = ['Владимирская']
        if self.station in rat_game_stations:
            rat_names = txt_reader('TXT-data\personal_names.txt')

            while coincidence:
                first_rat, second_rat, third_rat, fourth_rat, fifth_rat = \
                    ([random.choice(rat_names), random.randint(1, 50)] for _ in range(5))
                rats_check = [first_rat[0], second_rat[0], third_rat[0], fourth_rat[0], fifth_rat[0]]
                unique_rats_check = set(rats_check)
                if len(unique_rats_check) == len(rats_check):
                    coincidence = False
                else:
                    coincidence = True

            morph = pymorphy2.MorphAnalyzer()

            reply_rat_games = [[
                                   f'Поставить на {morph.parse("".join(c for c in first_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}',
                                   f'Поставить на {morph.parse("".join(c for c in second_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}',
                                   f'Поставить на {morph.parse("".join(c for c in third_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}'],
                               [
                                   f'Поставить на {morph.parse("".join(c for c in fourth_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}',
                                   f'Поставить на {morph.parse("".join(c for c in fifth_rat[0] if c.isalpha()))[0].inflect({"gent"}).word.capitalize()}'],
                               ['Ни на кого не ставить']]
            markup_rat_games = ReplyKeyboardMarkup(reply_rat_games, one_time_keyboard=False)

            update.message.reply_text('✅ Вы решили принять участие в крысиных бегах. ✅',
                                      reply_markup=ReplyKeyboardRemove())
            time.sleep(2)
            update.message.reply_text('В сегодняшнем забеге участвуют следующие крысы:\n'
                                      f'1. {first_rat[0]}. Шанс на победу: {first_rat[1]}%\n'
                                      f'2. {second_rat[0]}. Шанс на победу: {second_rat[1]}%\n'
                                      f'3. {third_rat[0]}. Шанс на победу: {third_rat[1]}%\n'
                                      f'4. {fourth_rat[0]}. Шанс на победу: {fourth_rat[1]}%\n'
                                      f'5. {fifth_rat[0]}. Шанс на победу: {fifth_rat[1]}%\n'
                                      'На какую крысу вы готовы поставить?', reply_markup=markup_rat_games)

            with open(f'JSON-data\games_in_metro{update.message.chat_id}.json', 'w') as f:
                f.write(json.dumps(
                    dict(first_rat=first_rat, second_rat=second_rat, third_rat=third_rat, fourth_rat=fourth_rat,
                         fifth_rat=fifth_rat, player_choice='')))

        else:
            update.message.reply_text('❌ На данной станции не проводятся крысиные бега. ❌')


reply_keyboard_trade_things_simple_stations = [['🔫Пять Патронов🔫'], ['Улучшение пистолета'],
                                               ['Ничего не покупать']]
markup_trade_things_simple_stations = ReplyKeyboardMarkup(reply_keyboard_trade_things_simple_stations,
                                                          one_time_keyboard=False)

reply_keyboard_trade_things_normal_stations = [['🔫Десять Патронов🔫'], ['Улучшение обреза'],
                                               ['Ничего не покупать']]
markup_trade_things_normal_stations = ReplyKeyboardMarkup(reply_keyboard_trade_things_normal_stations,
                                                          one_time_keyboard=False)

reply_keyboard_trade_things_drug_station = [['💊Витаминки💊 🪴', 'Витаминки💊 🪵', '💊Витаминки💊 🥩'],
                                            ['🍵Настойка из Кисликов🍵', '🍃Зелёный отвар🍃'], ['Ничего не покупать']]
markup_trade_things_drug_station = ReplyKeyboardMarkup(reply_keyboard_trade_things_drug_station,
                                                       one_time_keyboard=False)

reply_keyboard_station = [['Поменяться предметами с жителями', 'Выйти со станции'],
                          ['Осмотреть инвентарь', 'Арендовать домик: 35 патронов',
                           'Сыграть в Кости: 25 патронов'],
                          ['Посмотреть карту'], ['Постоять на станции (Послушать музыку)']]
markup_station = ReplyKeyboardMarkup(reply_keyboard_station, one_time_keyboard=False)

reply_keyboard_vladimirskaya = [['Поменяться предметами с жителями', 'Выйти со станции'],
                                ['Осмотреть инвентарь', 'Арендовать домик: 35 патронов',
                                 'Сделать ставку на крысиных бегах'],
                                ['Посмотреть карту'], ['Постоять на станции (Послушать музыку)']]
markup_vladimirskaya = ReplyKeyboardMarkup(reply_keyboard_vladimirskaya, one_time_keyboard=False)

reply_keyboard_dead_station = [['Осмотреть станцию', 'Выйти со станции'], ['Осмотреть инвентарь'], ['Посмотреть карту'],
                               ['Постоять на станции (Послушать музыку)']]
markup_dead_station = ReplyKeyboardMarkup(reply_keyboard_dead_station, one_time_keyboard=False)

reply_keyboard_fight_choice = [['Атаковать'], ['Сбежать']]
markup_fight_choice = ReplyKeyboardMarkup(reply_keyboard_fight_choice, one_time_keyboard=False)
