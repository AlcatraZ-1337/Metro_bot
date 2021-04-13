import requests
from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from account import TOKEN
from telegram.ext import CallbackContext, CommandHandler


class User:
    name = None
    bullets = 0
    food = 0

    trade_item_1 = 0
    trade_item_2 = 0
    trade_item_3 = 0
    trade_item_4 = 0

    costume = 0
    weapon = 0


def info(update, context):
    update.message.reply_text(
        "Чтобы начать введите команду: /start")


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    text_handler = MessageHandler(Filters.text, info)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, start_choose)],
            1.1: [MessageHandler(Filters.text, start)],
            2: [MessageHandler(Filters.text, inventory)],
            3: [MessageHandler(Filters.text, stop)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


def start(update, context):
    update.message.reply_text(
        "⭐Начало⭐")
    update.message.reply_text(
        "Введите своё имя:")
    User.bullets = 250
    User.food = 15

    return 1


def inventory(update, context):
    update.message.reply_text(
        f"Ваше имя: {User.name} 🧍\n"
        f"Ваши патроны: {User.bullets} 🔫\n"
        f"Ваш запас еды: {User.food} 🍖\n"
        "\n"
        "Ваши предметы для бартера: ♼\n"  
        f"Кислик: {User.trade_item_1} 🍄\n"
        f"Тунельный камень: {User.trade_item_2} 🧼\n"
        f"Ржавая трава: {User.trade_item_3} 🌿\n"
        f"Керосин: {User.trade_item_4} 🛢")


def repeater(update, context):
    update.message.reply_text(
        "Ошибка!!!")
    update.message.reply_text(
        "Введите своё имя:")


def start_choose(update, context):
    User.name = update.message.text
    inventory(update, context)
    geocoder(update, context)
    update.message.reply_text(
        "Вы готовы начинать?")
    return 3


def stop(update, context):
    update.message.reply_text("Игра окончена, спасибо за прохождение самой первой демки)))")
    return ConversationHandler.END


def geocoder(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_uri, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "format": "json",
        "geocode": update.message.text
    })

    toponym = response.json()["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]

    static_api_request = f"http://static-maps.yandex.ru/1.x/?ll=30.315721,59.971093&spn=0.5,0.5&l=map&pt=30.411310,59.929214,pm2rdl"
    context.bot.send_photo(
        update.message.chat_id,  # Идентификатор чата. Куда посылать картинку.
        # Ссылка на static API, по сути, ссылка на картинку.
        # Телеграму можно передать прямо её, не скачивая предварительно карту.
        static_api_request,
        caption='Вы начинаете игру на станции: Новочеркасская'
    )


if __name__ == '__main__':
    main()
