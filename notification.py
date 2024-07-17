import time
import logic
import requests
import json


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

        requests.get('https://api.telegram.org/bot7303708800:AAGTVKRg7AyGoCdrrmi-L8NpHSIlkzKdbFU/sendMessage?',
                     data={
                         'chat_id': user,
                         'text': 'У вас есть не законченный проект!',
                         'reply_markup': json.dumps(reply_markup)
                     })

    time.sleep(60*30)
