from datetime import datetime

import telebot
import os
import logic
import keyboards

from telebot import types
from dotenv import load_dotenv

# загружаем переменные окружения
load_dotenv()

bot = telebot.TeleBot(token=os.getenv('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    admins = logic.read_data('admins.json')
    if message.text == '/start':
        if user_id in admins:
            bot.send_sticker(user_id,
                             'CAACAgIAAxkBAAMKZnX2k_I9502g2ZCuN4nid7VlDQEAAmENAALxnVBLnuDECELUkK81BA')
            bot.send_message(user_id, 'Добро пожаловать в админ панель!',
                             reply_markup=keyboards.admin_board())
        else:
            data = logic.read_data('users.json')
            data[str(user_id)] = {'project': '',
                                  'knot': -1,
                                  'time': []}
            logic.wright_data('users.json', data)
            bot.send_sticker(user_id,
                             'CAACAgIAAxkBAAMqZnf-T4bvfowUTpccVFBcVXT97mEAAlUBAAIw1J0R6VElEe6M5tg1BA')
            bot.send_message(user_id, 'Добро пожаловать в бота по учету времени!',
                             reply_markup=keyboards.user_board())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    call_back = call.data
    user_id = call.message.chat.id
    if call_back.split('<>')[0] == 'add_project':
        markup = keyboards.choice_dep('admin')
        bot.send_message(user_id, 'Выберите отдел.',
                         reply_markup=markup)

    elif call_back.split('<>')[0] == 'admin_choice_dep':
        dep = int(call_back.split('<>')[1])
        bot.send_message(user_id, 'Отправьте файл в формате xlsx')
        bot.register_next_step_handler(call.message, load_project, dep)

    elif call_back == 'add_admin':
        bot.send_message(user_id, 'отправьте id юезра в телеграм')
        bot.register_next_step_handler(call.message, add_admin)

    elif call_back == 'list_admin':
        admins = logic.read_data('admins.json')
        if len(admins) > 0:
            for n, project in enumerate(admins, 1):
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(
                    types.InlineKeyboardButton('удалить', callback_data=f'del_admin<>{n}')
                )
                if n == len(admins):
                    markup.add(
                        types.InlineKeyboardButton('назад', callback_data=f'back<>{len(admins)}')
                    )
                bot.send_message(user_id, project,
                                 reply_markup=markup)
        else:
            bot.send_message(user_id, 'Проектов пока нет.',
                             reply_markup=keyboards.admin_board())

    elif call_back == 'admin_choice_dep_back':
        bot.send_message(user_id, 'Добро пожаловать в админ панель!',
                         reply_markup=keyboards.admin_board())

    elif call_back == 'see_deps':
        bot.send_message(user_id, 'Выберите отдел',
                         reply_markup=keyboards.choice_dep('admin', True))

    elif call_back.split('<>')[0] == 'admin_choice_dep_for_del':
        dep_i = int(call_back.split('<>')[1])
        dep = logic.get_all_departments()[dep_i]
        projects = logic.read_data('projects_list.json')[dep]
        if len(projects) > 0:
            for n, project in enumerate(projects, 1):
                markup = keyboards.project_info(n, dep_i)
                if n == len(projects):
                    markup.add(
                        types.InlineKeyboardButton('назад', callback_data=f'back<>{len(projects)}')
                    )
                bot.send_message(user_id, project,
                                 reply_markup=markup)
        else:
            bot.send_message(user_id, 'Проектов пока нет.',
                             reply_markup=keyboards.admin_board())

    elif call_back == 'get_file':
        logic.create_file()
        file = open('time.xlsx', 'rb')
        bot.send_document(user_id, file)

    elif call_back == 'user_choice_dep_back':
        bot.send_message(user_id, 'Добро пожаловать в бота по учету времени!',
                         reply_markup=keyboards.user_board())

    elif call_back == 'start':

        markup = keyboards.choice_dep('user')
        bot.send_message(user_id, 'Выберите отдел.',
                         reply_markup=markup)

    elif call_back.split('<>')[0] == 'user_choice_dep':
        dep_i = int(call_back.split('<>')[1])
        dep = logic.get_all_departments()[dep_i]
        projects = logic.read_data('projects_list.json')[dep]
        if len(list(projects)) != 0:
            for n, project in enumerate(projects):
                markup = keyboards.project_info_for_user(n, dep_i)
                bot.send_message(user_id, project,
                                 reply_markup=markup)
        else:
            markup = keyboards.user_board()
            bot.send_message(user_id, 'На данный момент нет доступных проектов в этом отделе',
                             reply_markup=markup)

    elif call_back.split('<>')[0] == 'back':
        admins_count = int(call_back.split('<>')[1])
        first = call.message.message_id - admins_count + 1
        for n in range(admins_count-1):
            bot.delete_message(user_id, first + n)

        bot.send_message(user_id, 'Админ панель!',
                         reply_markup=keyboards.admin_board())

    elif call_back.split('<>')[0] == 'del_admin':
        """удаляем все сообщения из списка, кроме нажатой кнопки"""
        admins = logic.read_data('admins.json')
        admin_n = int(call_back.split('<>')[1]) - 1
        first = call.message.message_id - admin_n
        if len(admins) > 0:
            for n in range(len(admins)):
                if n != admin_n:
                    bot.delete_message(user_id, first + n)

        admins.remove(admins[admin_n])
        logic.wright_data('admins.json', admins)
        bot.send_message(user_id, 'Админ панель!',
                         reply_markup=keyboards.admin_board())

    elif call_back.split('<>')[0] == 'del':

        """удаляем все сообщения из списка, кроме нажатой кнопки"""
        dep_i = int(call_back.split('<>')[2])
        dep = logic.get_all_departments()[dep_i]
        projects = list(logic.read_data('projects_list.json')[dep])
        project_n = int(call_back.split('<>')[1]) - 1
        first = call.message.message_id - project_n
        projects_count = len(list(logic.read_data('projects_list.json')[dep])) - 1
        if projects_count > 0:
            for n in range(projects_count + 1):
                if n != project_n:
                    bot.delete_message(user_id, first + n)

        data = logic.read_data('projects_list.json')
        num = project_n - 1
        del_prod = projects[num]
        data[dep].pop(del_prod, None)
        logic.wright_data('projects_list.json', data)
        bot.send_message(user_id, 'Админ панель!',
                         reply_markup=keyboards.admin_board())

    elif call_back.split('<>')[0] == 'see_knots':
        dep_i = int(call_back.split('<>')[2])
        dep = logic.get_all_departments()[dep_i]

        """удаляем все сообщения из списка, кроме нажатой кнопки"""
        projects = list(logic.read_data('projects_list.json')[dep])
        project_n = int(call_back.split('<>')[1])
        project_name = projects[project_n]
        first = call.message.message_id - project_n
        projects_count = len(list(logic.read_data('projects_list.json')[dep])) - 1
        if projects_count > 0:
            for n in range(projects_count + 1):
                if n != project_n:
                    bot.delete_message(user_id, first + n)

        """отправляем список узлов"""
        knots = logic.read_data('projects_list.json')[dep][project_name]
        for n, knot in enumerate(knots):
            markup = keyboards.knot_btn(project_n, n, dep_i)
            bot.send_message(user_id, knot,
                             reply_markup=markup)

    elif call_back.split('<>')[0] == 'select':
        dep_i = int(call_back.split('<>')[3])
        dep = logic.get_all_departments()[dep_i]
        projects = list(logic.read_data('projects_list.json')[dep])
        projects_n = int(call_back.split('<>')[1])
        project_name = projects[projects_n]
        knot = int(call_back.split('<>')[2])

        """удаляем все сообщения из списка, кроме нажатой кнопки"""
        first = call.message.message_id - knot
        knots_count = len(logic.read_data('projects_list.json')[dep][project_name]) - 1
        if knots_count > 0:
            for n in range(knots_count + 1):
                if n != knot:
                    bot.delete_message(user_id, first + n)

        """проверка работает ли кто-то над этим узлом"""
        status = False
        data = logic.read_data('users.json')
        for i in list(data):
            if (data[i]['project'] == project_name) and (data[i]['project'] == knot):
                status = True

        if not status:
            data = logic.read_data('users.json')
            now = datetime.now().timestamp()
            data[str(user_id)] = {'project': project_name,
                                  'dep': dep,
                                  'knot': knot,
                                  'time': [now]}
            logic.wright_data('users.json', data)
            knot = logic.read_data('projects_list.json')[dep][project_name][knot]
            markup = keyboards.knot_menu()
            bot.send_message(user_id, f'проект: {project_name}\nузел: {knot}',
                             reply_markup=markup)
        else:
            markup = keyboards.user_board()
            bot.send_message(user_id, f'извините над узлом уже работает другой сотрудник.',
                             reply_markup=markup)

    elif call_back == 'pause':
        """получаем данные юзера"""
        data = logic.read_data('users.json')
        dep = data[str(user_id)]['dep']
        project_name = data[str(user_id)]['project']
        knot = data[str(user_id)]['knot']

        """добавляем точку отсчета и получаем время занятости"""
        now = datetime.now().timestamp()
        data[str(user_id)]['time'].append(now)
        logic.wright_data('users.json', data)
        knot = logic.read_data('projects_list.json')[dep][project_name][knot]
        duration = logic.get_time(str(user_id))

        """отправляем сообщение"""
        markup = keyboards.knot_menu('pause')
        bot.send_message(user_id, f'проект: {project_name}\nузел: {knot}\n{duration} ч.',
                         reply_markup=markup)

    elif call_back == 'resume':
        """получаем данные юзера"""
        data = logic.read_data('users.json')
        dep = data[str(user_id)]['dep']
        project_name = data[str(user_id)]['project']
        knot = data[str(user_id)]['knot']

        """добавляем точку отсчета и получаем время занятости"""
        now = datetime.now().timestamp()
        data[str(user_id)]['time'].append(now)
        logic.wright_data('users.json', data)
        knot = logic.read_data('projects_list.json')[dep][project_name][knot]
        duration = logic.get_time(str(user_id))

        """отправляем сообщение"""
        markup = keyboards.knot_menu()
        bot.send_message(user_id, f'проект: {project_name}\nузел: {knot}\n{duration} ч.',
                         reply_markup=markup)

    elif call_back.split('<>')[0] == 'update':
        status = call_back.split('<>')[1]
        """получаем данные юзера"""
        data = logic.read_data('users.json')
        project_name = data[str(user_id)]['project']
        knot = data[str(user_id)]['knot']
        dep = data[str(user_id)]['dep']
        knot = logic.read_data('projects_list.json')[dep][project_name][knot]

        duration = logic.get_time(str(user_id))

        """отправляем сообщение"""
        markup = keyboards.knot_menu(status)
        bot.send_message(user_id, f'проект: {project_name}\nузел: {knot}\n{duration} ч.',
                         reply_markup=markup)

    elif call_back.split('<>')[0] == 'end?':
        status = call_back.split('<>')[1]
        markup = types.InlineKeyboardMarkup()
        bt1 = types.InlineKeyboardButton('да', callback_data=f'end<>{status}')
        bt2 = types.InlineKeyboardButton('нет', callback_data=f'update<>{status}')
        markup.add(bt1, bt2)
        bot.send_message(user_id, f'Вы уверены, что хотите завершить?',
                         reply_markup=markup)

    elif call_back.split('<>')[0] == 'end':
        duration = logic.get_time(str(user_id))
        data = logic.read_data('users.json')
        data[str(user_id)]['status'] = 'end'
        logic.wright_data('users.json', data)
        dep = data[str(user_id)]['dep']
        project_name = data[str(user_id)]['project']
        knot = data[str(user_id)]['knot']
        knot = logic.read_data('projects_list.json')[dep][project_name][knot]

        data = logic.read_data('data.json')
        data[project_name][knot].append([call.message.chat.first_name, duration, str(datetime.now())[:10], dep])

        logic.wright_data('data.json', data)
        logic.load_on_google()
        """отправляем сообщение"""
        markup = keyboards.user_board()
        bot.send_message(user_id, f'Работа завершена! Ушло времени -> \n{duration} ч.',
                         reply_markup=markup)

    # удаляем сообщение с нажатой кнопкой
    bot.delete_message(user_id, call.message.message_id)


def load_project(message, dep):
    user_id = message.chat.id

    if message.content_type == "document":
        if message.document.file_name.split('.')[-1] != 'xlsx':
            bot.send_message(user_id, 'Неверный формат, отправьте пожалуйста файл в расширении xlsx')
        else:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open('tabel.xlsx', 'wb') as f:
                f.write(downloaded_file)
            logic.load_project('tabel.xlsx', dep)
            os.remove('tabel.xlsx')
            markup = keyboards.admin_board()
            bot.send_message(user_id, 'Проект добавлен!',
                             reply_markup=markup)
    else:
        bot.send_message(user_id, 'Нужен файл,  попробуйте еще раз!')


def add_admin(message):
    user_id = message.chat.id

    admin = message.text

    data = logic.read_data('admins.json')
    data.append(int(admin))
    logic.wright_data('admins.json', data)
    markup = keyboards.admin_board()
    bot.send_message(user_id, 'Админ добавлен!', reply_markup=markup)


bot.infinity_polling()
