from telebot import types
from logic import get_all_departments


def admin_board() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    bt1 = types.InlineKeyboardButton('Загрузить проект', callback_data='add_project')
    bt2 = types.InlineKeyboardButton('Посмотреть проекты', callback_data='see_deps')
    bt3 = types.InlineKeyboardButton('Добавить нового админа', callback_data='add_admin')
    bt4 = types.InlineKeyboardButton('Список админов', callback_data='list_admin')
    bt5 = types.InlineKeyboardButton('Выгрузить данные', callback_data='get_file')
    markup.add(bt1, bt2, bt3, bt4, bt5)
    return markup


def project_info(num: int, dep_i) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Удалить', callback_data=f'del<>{num}<>{dep_i}')
    markup.add(bt1)
    return markup


def user_board() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=1)
    bt1 = types.InlineKeyboardButton('Начать', callback_data='start')
    markup.add(bt1)
    return markup


def project_info_for_user(num: int, dep: int, n=None, count=None) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()
    if n is not None:
        bt1 = types.InlineKeyboardButton('Показать узлы', callback_data=f'see_knots<>{num}<>{dep}<>{n}<>{count}')
    else:
        bt1 = types.InlineKeyboardButton('Показать узлы', callback_data=f'see_knots<>{num}<>{dep}')
    markup.add(bt1)
    return markup


def knot_btn(project_n: int, knot: int, dep: int):
    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Начать работу', callback_data=f'select<>{project_n}<>{knot}<>{dep}')
    markup.add(bt1)
    return markup


def knot_menu(status='go'):
    markup = types.InlineKeyboardMarkup()
    if status == 'pause':
        bt1 = types.InlineKeyboardButton('продолжить', callback_data=f'resume')
    else:
        bt1 = types.InlineKeyboardButton('пауза', callback_data=f'pause')
    bt2 = types.InlineKeyboardButton('закончить', callback_data=f'end?<>{status}')
    bt3 = types.InlineKeyboardButton('узнать время', callback_data=f'update<>{status}')
    markup.add(bt1, bt2, bt3)
    return markup


def choice_dep(rights, del_p=False):
    markup = types.InlineKeyboardMarkup()
    list_dep = get_all_departments()

    for n, dep in enumerate(list_dep):
        if not del_p:
            callback = f'{rights}_choice_dep<>{n}'
        else:
            callback = f'{rights}_choice_dep_for_del<>{n}'
        markup.add(
            types.InlineKeyboardButton(dep, callback_data=callback)
        )
    markup.add(
        types.InlineKeyboardButton('назад', callback_data=f'{rights}_choice_dep_back')
    )
    return markup
