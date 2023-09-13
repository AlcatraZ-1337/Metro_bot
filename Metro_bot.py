import json
import os.path

from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup

from stations import station_distributor, geocoder
from classes import User
from started_functions import delete, markup_keyboard_start, name_input
from account import TOKEN


def info(update, context):
    update.message.reply_text(
        "Чтобы начать введите команду: /start\n"
        "Для того, чтобы удалить свою предыдущую игру введите команду: /delete", reply_markup=markup_keyboard_start)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('delete', delete))

    text_handler = MessageHandler(Filters.text, info)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, start_choose)],
            2: [MessageHandler(Filters.text, station_distributor)],

            6: [MessageHandler(Filters.text, stop)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(conv_handler)

    dp.add_handler(text_handler)
    updater.start_polling()

    updater.idle()


def start(update, context):
    if os.path.exists(f'JSON-data\main_hero{update.message.chat_id}.json'):
        try:
            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'r') as f:
                data = json.load(f)

            with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
                data['question_output'] = True
                data['fight_output'] = False
                data['trade_output'] = False
                data['rat_game_output'][0] = False
                f.write(json.dumps(data))

            print(f'Пользователь: {update.message.chat_id} Продолжает игру! Его имя: {data["name"]}. \n'
                  'Надеюсь он не найдёт много багов ;)')

            update.message.reply_text(
                '✅ Файл с вашими данными  об игре найден ✅. \n'
                'Введите "Начать", когда будете готовы начинать.',
                reply_markup=markup_user_answer)
        except json.decoder.JSONDecodeError:
            update.message.reply_text("❌ Похоже, что ваше сохранение было повреждено! ❌")
            name_input(update, context)
            return 1

        return 2

    name_input(update, context)

    return 1


reply_keyboard_user_answer = [['Начать']]
markup_user_answer = ReplyKeyboardMarkup(reply_keyboard_user_answer, one_time_keyboard=False)


def start_choose(update, context):
    with open(f'JSON-data\main_hero{update.message.chat_id}.json', 'w') as f:
        f.write(json.dumps(
            dict(name=update.message.text, health=100, attack=30, bullets=150,
                 food=15, trade_item_1=0, trade_item_2=0, trade_item_3=0, trade_item_4=0, trade_item_5=0,
                 station='Новочеркасская', owner='🛡Под контролем Альянса Оккервиль🛡', danger='✅ Отсутствуют ✅',
                 question_output=True, fight_output=False, trade_output=False, rat_game_output=[False, False])))

    User(update, context).inventory(update, context)
    geocoder(update, context)

    name = update.message.text
    print(f'Пользователь: {update.message.chat_id} начал игру! Его имя: {name}. \n'
          'Надеюсь он не найдёт много багов ;)')

    update.message.reply_text(
        'Введите "Начать", когда будете готовы начинать.', reply_markup=markup_user_answer)

    return 2


def stop(update, context):
    print('работа закончена')
    return ConversationHandler.END


if __name__ == '__main__':
    main()
