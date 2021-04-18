import requests
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup


reply_keyboard_novocherkasskaya = [['Пойти к торговцу', 'Выйти со станции'], ['Осмотреть инвентарь', 'Лечь спать'],
                                   ['Посмотреть карту']]
markup_novocherkasskaya = ReplyKeyboardMarkup(reply_keyboard_novocherkasskaya, one_time_keyboard=False)


class User:
    name = None

    health = 0
    armor = 0

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
        f"Ваше имя: {User.name} 🧍\n"
        f"Ваше здоровье: {User.health} ♥\n"
        f"Ваша броня: {User.armor} 🛡\n"
        "\n"
        f"Ваши патроны: {User.bullets} 🔫\n"
        f"Ваш запас еды: {User.food} 🍖\n"
        "\n"
        "Ваши предметы для бартера: ♼\n"  
        f"Кислик: {User.trade_item_1} 🍄\n"
        f"Тунельный камень: {User.trade_item_2} 🧼\n"
        f"Ржавая трава: {User.trade_item_3} 🌿\n"
        f"Керосин: {User.trade_item_4} 🛢")


def sleep(update, content):
    update.message.reply_text("Во время сна вы восстановили всё своё здоровье.")
    User.health = 100


def novocherkasskaya(update, context):
    novocherkasskaya_choice_check(update, context)
    if update.message.text == 'Нет':
        update.message.reply_text("Ну и пожалуйста! Ну и не нужно! Ну и очень то мне нужно!")
        update.message.reply_text("Игра окончена, спасибо за прохождение самой первой демки)))")
        return ConversationHandler.END
    update.message.reply_text("Вы находитесь на станции: Новочеркасская.\n"
                              "Станция под контролем Оккервильского альянса.\n"
                              "Что вы хотите сделать?", reply_markup=markup_novocherkasskaya)


def novocherkasskaya_choice_check(update, context):
    choice = update.message.text
    if choice == reply_keyboard_novocherkasskaya[0][0]:
        trade_novocherkasskaya(update, context)
    elif choice == reply_keyboard_novocherkasskaya[1][0]:
        inventory(update, context)
    elif choice == reply_keyboard_novocherkasskaya[1][1]:
        sleep(update, context)
    elif choice == reply_keyboard_novocherkasskaya[2][0]:
        geocoder_novocherkasskaya(update, context, False)
    return 3


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
    update.message.reply_text("Здесь должна была быть торговля)))")


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
