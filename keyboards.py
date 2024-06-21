from telebot import types


def admin_board() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    bt1 = types.InlineKeyboardButton('Загрузить проект', callback_data='load_project')
    bt2 = types.InlineKeyboardButton('Посмотреть проекты', callback_data='see_projects')
    bt3 = types.InlineKeyboardButton('Добавить нового админа', callback_data='add_admin')
    markup.add(bt1, bt2, bt3)
    return markup
