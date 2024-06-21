import telebot
import os
import logic
import keyboards

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


@bot.message_handler(content_types=['sticker'])
def stick(message):
    print(message)


bot.infinity_polling()
