from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup

reply_keyboard_novocherkasskaya = [['Пойти к торговцу', 'Выйти со станции'],
                                   ['Осмотреть инвентарь', 'Арендовать домик на ночь: 35 патронов'],
                                   ['Посмотреть карту']]
markup_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_novocherkasskaya, one_time_keyboard=True)

reply_keyboard_trade_novocherkasskaya = [['Купить', 'Продать'], ['Уйти']]
markup_trade_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_trade_novocherkasskaya, one_time_keyboard=True)

reply_novocherkasskaya_buy = [['Еда', 'Нож', 'Обрез'], ['Костюм солдата Оккервильского альянса']]
markup_novocherkasskaya_buy = ReplyKeyboardMarkup(reply_novocherkasskaya_buy, one_time_keyboard=True)

reply_novocherkasskaya_sell = [['Еда', 'Кислик', 'Тунельный камень'], ['Ржавая трава', 'Керосин']]
markup_novocherkasskaya_sell = ReplyKeyboardMarkup(reply_novocherkasskaya_sell, one_time_keyboard=True)


class User:
    name = None

    health = 0
    armor = 0
    attack = 0

    bullets = 0
    food = 0

    trade_item_1 = 0
    trade_item_2 = 0
    trade_item_3 = 0
    trade_item_4 = 0

    costume = 0
    weapon = 0


def inventory(update, context):
    update.message.reply_text(
        f"🧍 Ваше имя: {User.name} 🧍\n"
        f"♥ Ваше здоровье: {User.health} ♥\n"
        f"🛡 Ваша броня: {User.armor} 🛡\n"
        f"🔪Ваш урон: {User.attack} 🔪\n"
        "\n"
        f"🔫 Ваши патроны: {User.bullets} 🔫\n"
        f"🍖 Ваш запас еды: {User.food} 🍖\n"
        "\n"
        "♼ Ваши предметы для бартера: ♼\n"
        f"🍄 Кислик: {User.trade_item_1} 🍄\n"
        f"🧼 Тунельный камень: {User.trade_item_2} 🧼\n"
        f"🌿 Ржавая трава: {User.trade_item_3} 🌿\n"
        f"🛢 Керосин: {User.trade_item_4} 🛢")


def sleep(update, content):
    update.message.reply_text("Во время сна вы восстановили всё своё здоровье.")
    User.health = 100


def novocherkasskaya(update, context):
    novocherkasskaya_choice_check(update, context)
    choice = update.message.text

    if choice == reply_keyboard_novocherkasskaya[0][0]:
        return 3.4
    elif choice == reply_keyboard_novocherkasskaya[0][1]:
        pass

    answer = update.message.text
    if answer == 'Нет':
        update.message.reply_text("Ну и пожалуйста! Ну и не нужно! Ну и очень то мне нужно!")
        update.message.reply_text("Игра окончена, спасибо за прохождение самой первой демки)))")
        return ConversationHandler.END
    update.message.reply_text("Вы находитесь на станции: Новочеркасская.\n"
                              "Станция под контролем Оккервильского альянса.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)


def novocherkasskaya_choice_check(update, context):
    choice = update.message.text

    if choice == reply_keyboard_novocherkasskaya[1][0]:
        inventory(update, context)
    elif choice == reply_keyboard_novocherkasskaya[1][1]:
        update.message.reply_text("Вы заплатили 35 патронов за домик на станции Новочеркасская.")
        User.bullets -= 35
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


def trade_novocherkasskaya(update, context):
    update.message.reply_text("Товары на продажу: \n"
                              "1)🍖Еда (1шт.)🍖: 25 патронов. \n"
                              "\n"
                              "🔫Оружие🔫:\n"
                              "2)🔪Нож🔪: 150 патронов. \n"
                              "3)🔫Обрез🔫: 300 патронов, 35 кисликов🍄 и 10 тунельных камней🧼. \n"
                              "\n"
                              "🛡Броня🛡:\n"
                              "4)🧥Костюм солдата Оккервильского альянса🧥: 250 патронов, 15 кисликов🍄 и 25 тунельных "
                              "камней🧼."
                              "\n"
                              "Товары, покупаемые торговцем: \n"
                              "1)🍖Еда🍖: 12 патронов. \n"
                              "2)🍄Кислик🍄: 5 патронов. \n"
                              "3)🧼Тунельный камень🧼: 10 патронов. \n"
                              "4)🌿Ржавая трава🌿: 20 патронов. \n"
                              "5)🛢Керосин🛢: 25 патронов.",
                              reply_markup=markup_trade_novocherkasskaya)
    return 3.5


def trade_novocherkasskaya_check(update, context):
    choice = update.message.text

    if choice == reply_keyboard_trade_novocherkasskaya[0][0]:
        return 3.6
    elif choice == reply_keyboard_trade_novocherkasskaya[0][1]:
        return 3.7
    elif choice == reply_keyboard_trade_novocherkasskaya[1][0]:
        trade_novocherkasskaya_exit(update, context)

    if choice == reply_novocherkasskaya_buy[0][0]:
        if User.bullets >= 25:
            User.bullets -= 25
            User.food += 1

            update.message.reply_text("Вы успешно купили еду.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает патронов для покупки еды!")
    elif choice == reply_novocherkasskaya_buy[0][1]:
        if User.bullets >= 150:
            User.bullets -= 150
            User.attack += 25

            update.message.reply_text("Вы успешно купили нож.")
            update.message.reply_text("Ваш урон увеличился на 25 единиц.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает патронов для покупки ножа!")
    elif choice == reply_novocherkasskaya_buy[0][2]:
        if User.bullets >= 300 and User.trade_item_1 >= 35 and User.trade_item_2 >= 10:
            User.bullets -= 300
            User.trade_item_1 -= 35
            User.trade_item_2 -= 10
            User.attack += 45

            update.message.reply_text("Вы успешно купили обрез.")
            update.message.reply_text("Ваш урон увеличился на 45 единиц.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает предметов для покупки обреза!")
    elif choice == reply_novocherkasskaya_buy[1][0]:
        if User.bullets >= 250 and User.trade_item_1 >= 15 and User.trade_item_2 >= 25:
            User.bullets -= 250
            User.trade_item_1 -= 15
            User.trade_item_2 -= 25
            User.armor += 25

            update.message.reply_text("Вы успешно купили костюм солдата Оккервильского альянса.")
            update.message.reply_text("Ваша броня увеличилась на 25 единиц.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает предметов для покупки костюм солдата Оккервильского "
                                      "альянса!")
    return 3


def trade_novocherkasskaya_sell_1(update, context):
    choice = update.message.text

    if choice == reply_novocherkasskaya_sell[0][0]:
        if User.food >= 1:
            User.food -= 1
            User.bullets += 12
            update.message.reply_text("Вы успешно продали еду.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает еды, чтобы её продать!")
    elif choice == reply_novocherkasskaya_sell[0][1]:
        if User.trade_item_1 >= 1:
            User.trade_item_1 -= 1
            User.bullets += 5
            update.message.reply_text("Вы успешно продали Кислик.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает Кисликов, чтобы её продать!")
    elif choice == reply_novocherkasskaya_sell[0][2]:
        if User.trade_item_2 >= 1:
            User.trade_item_2 -= 1
            User.bullets += 10
            update.message.reply_text("Вы успешно продали Тунельный камень.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает Тунельных камней, чтобы их продать!")
    elif choice == reply_novocherkasskaya_sell[1][0]:
        if User.trade_item_3 >= 1:
            User.trade_item_3 -= 1
            User.bullets += 20
            update.message.reply_text("Вы успешно продали Ржавую траву.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает Ржавой травы, чтобы её продать!")
    elif choice == reply_novocherkasskaya_sell[1][1]:
        if User.trade_item_4 >= 1:
            User.trade_item_4 -= 1
            User.bullets += 25
            update.message.reply_text("Вы успешно продали керосин.")
        else:
            update.message.reply_text("Ошибка! Вам нехватает керосина, чтобы его продать!")
    return 3


def trade_novocherkasskaya_buy(update, context):
    update.message.reply_text("Выберите товар, который хотите купить.",
                              reply_markup=markup_novocherkasskaya_buy)
    return 3.5


def trade_novocherkasskaya_sell(update, context):
    update.message.reply_text("Выберите товар, который хотите продать.",
                              reply_markup=markup_novocherkasskaya_buy)
    return 3.71


def trade_novocherkasskaya_exit(update, context):
    return 3


def alexander_nevsky_square_1(update, context):
    update.message.reply_text("Вы находитесь на станции: Площадь Александра Невского 1.\n"
                              "Станция под контролем Империи Веган.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)

    return 7


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
