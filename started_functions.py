import os

from telegram import ReplyKeyboardMarkup


reply_keyboard_start = [['/start'], ['/delete']]
markup_keyboard_start = ReplyKeyboardMarkup(reply_keyboard_start, one_time_keyboard=False)


def delete(update, context):
    try:
        os.remove(f'JSON-data\main_hero{update.message.chat_id}.json')

        print(f'Пользователь: {update.message.chat_id} удалил своё сохранение ;(')

        update.message.reply_text(
            "✅ Удаление файла сохранения прошло успешно. ✅", reply_markup=markup_keyboard_start)
    except FileNotFoundError:
        update.message.reply_text(
            "❌ У вас отсутствует файл сохранения! ❌", reply_markup=markup_keyboard_start)


def txt_reader(filename):
    names = []
    with open(filename, 'r', encoding='utf-8') as f:
        not_sorted_names = f.readlines()
        for i in range(len(not_sorted_names)):
            names.append(not_sorted_names[i].replace("\n", ""))
        return names
