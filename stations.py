import json
from random import random

from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup

reply_keyboard_novocherkasskaya = [['Взять заказ на доставку', 'Выйти со станции'],
                                   ['Осмотреть инвентарь', 'Арендовать домик на ночь: 35 патронов'],
                                   ['Посмотреть карту']]
markup_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_novocherkasskaya, one_time_keyboard=True)

reply_keyboard_trade_novocherkasskaya = [['Купить', 'Продать'], ['Уйти']]
markup_trade_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_trade_novocherkasskaya, one_time_keyboard=True)

reply_novocherkasskaya_buy = [['Еда', 'Нож', 'Обрез'], ['Костюм солдата Оккервильского альянса']]
markup_novocherkasskaya_buy = ReplyKeyboardMarkup(reply_novocherkasskaya_buy, one_time_keyboard=True)

reply_novocherkasskaya_sell = [['Еда', 'Кислик', 'Тунельный камень'], ['Ржавая трава', 'Керосин']]
markup_novocherkasskaya_sell = ReplyKeyboardMarkup(reply_novocherkasskaya_sell, one_time_keyboard=True)

reply_tunnels_move = [['Идти дальше']]
markup_tunnels_move = ReplyKeyboardMarkup(reply_tunnels_move, one_time_keyboard=True)


class User:
    def __init__(self):
        with open('main_hero.json', 'r') as f:
            data = json.load(f)
        self.id = None
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

    def inventory(self, update, context):
        update.message.reply_text(
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
            f"🛢 Керосин: {self.trade_item_4} 🛢")


class Fight:
    def __init__(self):
        pass

    def tunnels(self, update, context):
        update.message.reply_text("Вы идёте по тоннелям.")
        # random_tunnel = random.randint(0, 2)
        update.message.reply_text("Вы без проблем проходите через тоннель.", reply_markup=markup_tunnels_move)


def sleep(update, content):
    update.message.reply_text("Во время сна вы восстановили всё своё здоровье.")
    User.health = 100


def novocherkasskaya(update, context):
    novocherkasskaya_choice_check(update, context)
    choice = update.message.text

    if choice == reply_keyboard_novocherkasskaya[0][0]:
        pass
    elif choice == reply_keyboard_novocherkasskaya[0][1]:
        Fight().tunnels(update, context)
        return 4

    answer = update.message.text
    if answer == 'Нет':
        update.message.reply_text("Ну и пожалуйста! Ну и не нужно! Ну и очень то мне нужно!")
        update.message.reply_text("Игра окончена, спасибо за прохождение самой первой демки)))")
        return ConversationHandler.END
    update.message.reply_text("Вы находитесь на станции: Новочеркасская.\n"
                              "Станция под контролем Оккервильского альянса.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)


def novocherkasskaya_choice_check(update, context):
    with open('main_hero.json', 'r') as f:
        data = json.load(f)
    choice = update.message.text

    if choice == reply_keyboard_novocherkasskaya[1][0]:
        User().inventory(update, context)
    elif choice == reply_keyboard_novocherkasskaya[1][1]:
        update.message.reply_text("Вы заплатили 35 патронов за домик на станции Новочеркасская.")
        with open('main_hero.json', 'w') as f:
            data['bullets'] = data['bullets'] - 35
            f.write(json.dumps(data))
        sleep(update, context)
    elif choice == reply_keyboard_novocherkasskaya[2][0]:
        geocoder_novocherkasskaya(update, context, False)


def geocoder_novocherkasskaya(update, context, caption):
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn=0.5,0.5&l=map&pt=30.411310," \
                         f"59.929214,pm2rdl"
    if caption:
        context.bot.send_photo(
            update.message.chat_id,
            static_api_request,
            caption=f'Вы начинаете игру на станции: Новочеркасская.'
        )
    else:
        context.bot.send_photo(
            update.message.chat_id,
            static_api_request,
        )


def geocoder_alexander_nevsky_square(update, context):
    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn=0.5,0.5&l=map&pt=30.385229," \
                         f"59.924287,pm2rdl"
    context.bot.send_photo(
        update.message.chat_id,
        static_api_request,
    )


def alexander_nevsky_square_1(update, context):
    with open('main_hero.json', 'r') as f:
        data = json.load(f)
    choice = update.message.text

    if choice == reply_keyboard_novocherkasskaya[0][0]:
        pass
    elif choice == reply_keyboard_novocherkasskaya[0][1]:
        Fight().tunnels(update, context)
        return 4
    elif choice == reply_keyboard_novocherkasskaya[1][0]:
        User().inventory(update, context)
    elif choice == reply_keyboard_novocherkasskaya[1][1]:
        update.message.reply_text("Вы заплатили 15 патронов за домик на станции площадь Александра Невского 1.")
        with open('main_hero.json', 'w') as f:
            data['bullets'] = data['bullets'] - 15
            f.write(json.dumps(data))
        sleep(update, context)
    elif choice == reply_keyboard_novocherkasskaya[2][0]:
        geocoder_alexander_nevsky_square(update, context)

    update.message.reply_text("Вы находитесь на станции: Площадь Александра Невского 1.\n"
                              "Станция под контролем Империи Веган.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)


def alexander_nevsky_square_2(update, context):
    update.message.reply_text("Вы находитесь на станции: Площадь Александра Невского 2.\n"
                              "Станция под контролем Империи Веган.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)

    return 7


def mayakovskaya(update, context):
    update.message.reply_text("Вы находитесь на станции: Новочеркасская.\n"
                              "Станция под контролем Оккервильского альянса.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)

    return 7
