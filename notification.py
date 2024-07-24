import time
import logic
import requests
import json
import os

from dotenv import load_dotenv

# загружаем переменные окружения
load_dotenv()

while True:
    data = logic.read_data('users.json')
    not_list = []
    for i in list(data):
        if 'status' not in data[i]:
            if len(data[i]['time']) % 2 != 0:
                not_list.append(i)
    for user in not_list:
        markup = reply_markup = {
            'inline_keyboard': [
                [{
                    'text': 'удалить напоминание❎',
                    'callback_data': 'del_not'
                }]
            ]
        }

        requests.get(f'https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage?',
                     data={
                         'chat_id': user,
                         'text': 'У вас есть не законченный проект!',
                         'reply_markup': json.dumps(reply_markup)
                     })

    time.sleep(60*30)
