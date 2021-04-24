import json

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from account import TOKEN
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from stations import station_distributor, tunnels, geocoder, fight_distributor
from classes import User


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
            2: [MessageHandler(Filters.text, station_distributor)],
            3: [MessageHandler(Filters.text, tunnels)],
            5: [MessageHandler(Filters.text, fight_distributor)],

            4: [MessageHandler(Filters.text, stop)]
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

    return 1


reply_keyboard_user_answer = [['Начать']]
markup_user_answer = ReplyKeyboardMarkup(reply_keyboard_user_answer, one_time_keyboard=True)


def start_choose(update, context):
    with open(f'main_hero{update.message.chat_id}.json', 'w') as f:
        f.write(json.dumps(
            dict(name=update.message.text, health=100, armor=15, attack=15, bullets=250,
                 food=15, trade_item_1=0, trade_item_2=0, trade_item_3=0, trade_item_4=0, costume=0, weapon=0,
                 station='Новочеркасская', owner='под контролем Альянса Оккервиль', question_output=True)))

    User(update, context).inventory(update, context)
    geocoder(update, context)
    update.message.reply_text(
        'Введите "Начать", когда будете готовы начинать.', reply_markup=markup_user_answer)

    return 2


def stop(update, context):
    update.message.reply_text("Игра окончена, спасибо за прохождение демки)))")
    return ConversationHandler.END


if __name__ == '__main__':
    main()
