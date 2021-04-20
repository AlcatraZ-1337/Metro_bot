import json

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from account import TOKEN
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup
from stations import novocherkasskaya, alexander_nevsky_square_1, alexander_nevsky_square_2, mayakovskaya, inventory, \
    User, novocherkasskaya_choice_check, geocoder_novocherkasskaya, trade_novocherkasskaya_check, \
    trade_novocherkasskaya_buy, trade_novocherkasskaya_sell, trade_novocherkasskaya_exit, trade_novocherkasskaya, \
    trade_novocherkasskaya_sell_1


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
            3: [MessageHandler(Filters.text, novocherkasskaya)],
            3.3: [MessageHandler(Filters.text, novocherkasskaya_choice_check)],
            3.4: [MessageHandler(Filters.text, trade_novocherkasskaya)],
            3.5: [MessageHandler(Filters.text, trade_novocherkasskaya_check)],
            3.6: [MessageHandler(Filters.text, trade_novocherkasskaya_buy)],
            3.7: [MessageHandler(Filters.text, trade_novocherkasskaya_sell)],
            3.71: [MessageHandler(Filters.text, trade_novocherkasskaya_sell_1)],
            3.8: [MessageHandler(Filters.text, trade_novocherkasskaya_exit)],
            4: [MessageHandler(Filters.text, alexander_nevsky_square_1)],
            5: [MessageHandler(Filters.text, alexander_nevsky_square_2)],
            6: [MessageHandler(Filters.text, mayakovskaya)],

            7: [MessageHandler(Filters.text, stop)]
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


reply_keyboard_user_answer = [['Да', 'Нет']]
markup_user_answer = ReplyKeyboardMarkup(reply_keyboard_user_answer, one_time_keyboard=True)


def start_choose(update, context):
    with open('main_hero.json', 'w') as f:
        f.write(json.dumps(
            dict(id=update.message.from_user.id, name=update.message.text, health=100, armor=15, attack=15, bullets=250, food=15,
                 trade_item_1=0, trade_item_2=0, trade_item_3=0, trade_item_4=0, costume=0, weapon=0)))

    inventory(update, context)
    geocoder_novocherkasskaya(update, context, True)
    update.message.reply_text(
        "Вы готовы начинать?", reply_markup=markup_user_answer)
    return 3


def stop(update, context):
    update.message.reply_text("Игра окончена, спасибо за прохождение демки)))")
    return ConversationHandler.END


if __name__ == '__main__':
    main()
