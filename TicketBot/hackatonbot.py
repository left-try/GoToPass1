from io import BytesIO

import qrtools
import telebot
from PIL import Image
from pyzbar.pyzbar import decode
import random
import requests
import json



token = '843233261:AAG6YiNyV1IZy8xKnQm7CkQzwRPQbAnAGuw'

proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = proxy
# подключаемся к телеграму
bot = telebot.TeleBot(token=token)
admin_dos=0
uid = 0
passw = ""
@bot.message_handler(content_types=['photo'])
def task_handler(message):
    print('I started')
    user_id = message.chat.id

    file_id = message.photo[-1].file_id
    path = bot.get_file(file_id)
    p = 'https://api.telegram.org/file/bot{0}/'.format(token) + path.file_path
    data = requests.get(p, proxies=proxy)
    try:
        # Расшифровывание QR кода с фотки
        data = decode(Image.open(BytesIO(data.content)))
        print(data)
        r = requests.get('http://193.124.117.173:8000/api/set?tg={}&pass={}'.format(user_id, data[0].data.decode('ascii')))
        print(data[0].data.decode('ascii'))
        bot.send_message(message.chat.id, 'Вы зарегистрированы')
    except:
        # Если человек плохо сфоткал QR код плохо
        bot.send_message(message.chat.id, 'QR код не видно. Сфоткайте QR ещё раз так, чтобы QR был чётким и помещался в кадр')
# поллинг - вечный цикл с обновлением входящих сообщений
bot.polling(none_stop=True)
