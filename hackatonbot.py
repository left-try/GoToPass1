import telebot
import random
import requests
import json
from telebot import types
token = "985696524:AAEsN_PwKCJuGr7LlZGIAcRW8ydxwYBa3Gc"

# Обходим блокировку с помощью прокси
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

# подключаемся к телеграму
bot = telebot.TeleBot(token=token)
admin_dos=0
uid = 0
passw = ""

def REQ(message):
    r = requests.get('http://192.168.0.92:8000/api/get?pass='+passw)
    if r!=None:
        return(r.json())
@bot.message_handler(commands=['start'])
def start(message):
    
    base = """
команды:
/ticket - запрос на получение тикета
/check_ban - проверить в бане ли вы
            """
    admin="""
/admin - даёт доступ к админ командам
/ban - позволяет забанить кого-либо
/unbun - позволяет разбанить кого-либо
"""
    if message.chat.type == "private":
        bot.send_message(message.chat.id,base)
    if message.chat.type == "group":
        bot.send_message(message.chat.id,admin)
    
def check_reg(id):
    return 1

def check_ban(id):
    banlist=json.load(open('banlist.json','r'))    
    banlist_keys=list(banlist.keys())
    ban_count = banlist_keys.count(id)
    if ban_count == 0:
        return 1
    elif ban_count == 1:
        return 0

def confirm_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    kb1 = types.InlineKeyboardButton(text="да", callback_data="yes")
    kb2 = types.InlineKeyboardButton(text="нет", callback_data="no")
    keyboard.add(kb1, kb2)
    msg = bot.send_message(-357457307, REQ(0)['name']+" "+ REQ(0)['surname']+" "+"запрашивает тикет, потвердить?", reply_markup=keyboard)

    
@bot.callback_query_handler(func=lambda c:True)
def ans(c):
    global uid
    keyboard = types.InlineKeyboardMarkup()
    if c.data == "yes":
        bot.send_message(-357457307, "Тикет поттверждён", reply_markup=keyboard)
        print(uid)
        bot.send_message(uid,"Ваш тикет поттверждён")
    elif c.data == "no":
        bot.send_message(-357457307, "Тикет отклонён", reply_markup=keyboard)
        

pasw = ''    
@bot.message_handler(commands=['ticket'])    
def ticket_hand (message):
    global uid
    uid= message.chat.id
    pass_zap = bot.send_message(message.chat.id, 'Введите свой "pass"')
    bot.register_next_step_handler(pass_zap, ticket)

def ticket(message):
    global passw
    passw = message.text
    if check_ban(message.chat.id):
            confirm_keyboard()
        
    
    
        
@bot.message_handler(commands=['check_ban'])    
def check_ban_com(message):
    if check_ban(message.chat.id):
        check_ban_responce="Вы не забанены"
    else:
        check_ban_responce="Вы забанены"
    bot.send_message(message.chat.id,check_ban_responce) 
#@bot.message_handler(commands=['admin'])
#def admin_handler(message):
#    pass_zap = bot.send_message(message.chat.id, 'Введте пароль')
#    bot.register_next_step_handler(pass_zap, admin_act)
#def admin_act(message):
 #   if(message.text=='110106'):
  #      admin_dos=1
   #     bot.send_message(-357457307,"Вы активировали админ фукции")
@bot.message_handler(commands=['ban'])
def ban_hand(message):
    if(message.chat.id == -357457307):
        sent = bot.send_message(message.chat.id, 'Ведите ФИО человека которого хотите забанить')
        bot.register_next_step_handler(sent, ban)
        
def ban(message):
    #добавить api
    #FIO = message.text
    #F = FIO.split()[0]
    #I = FIO.split()[1]
    #O = FIO.split()[2]
    
    banlist=json.load(open('banlist.json','r'))
    banlist.update({FIO : 1})
    json.dump(banlist,open('banlist.json','w'))
    bot.send_message(-357457307, "Нарушитель забанен!")
    
        

# content_types=['text'] - сработает, если нам прислали текстовое сообщение
@bot.message_handler(content_types=['text'])
def echo(message):
    
    user = message.chat.id
    #отправляем картинку 
    #bot.send_photo(user, "https://i.ytimg.com/vi/R-RbmqzRC9c/maxresdefault.jpg")
    bot.send_message(user, 'Введите /start')



# поллинг - вечный цикл с обновлением входящих сообщений
bot.polling(none_stop=True)
