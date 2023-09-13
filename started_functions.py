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
        update.message.reply_text("Введите /start, чтобы создать новый файл.")


def txt_reader(filename):
    names = []
    with open(filename, 'r', encoding='utf-8') as f:
        not_sorted_names = f.readlines()
        for i in range(len(not_sorted_names)):
            names.append(not_sorted_names[i].replace("\n", ""))
        return names


def name_input(update, context):
    update.message.reply_text(
        "⭐Начало⭐")
    update.message.reply_text(
        "Введите своё имя. Вы можете использовать свой ник в телеграмме или ввести любой другой.",
        reply_markup=ReplyKeyboardMarkup(
            [[f'{update.message.from_user.first_name} {update.message.from_user.last_name}']
             if update.message.from_user.last_name is not None else [update.message.from_user.first_name]]))