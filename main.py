from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import datetime
import telebot
import threading

chats = []
class Chat():
    idNow = 0
    def __init__(self, id_chat):
        self.id = Chat.idNow
        self.id_chat = id_chat
        self.chat_info = bot.get_chat(self.id_chat)
        self.title = self.chat_info.title
        self.premium = False
        Chat.idNow += 1

SECRET_TOKEN = "[TOKEN_TG]"
bot = telebot.TeleBot(SECRET_TOKEN)

class Admin():
    id_admin = 0
    def __init__(self, user_id):
        user_info = bot.get_chat(user_id)
        self.id = Admin.id_admin
        self.user_id = user_id
        self.user_info = user_info
        self.username = user_info.username
        self.first_name = user_info.first_name
        Admin.id_admin += 1

admin = Admin(5051312064)


@bot.message_handler(commands=['start'])
def startBot(message):
    chat_id = message.chat.id
    chats.append(Chat(chat_id))
    bot.send_message(chat_id, "Это канал по тревогам в Одессе!")

now = datetime.datetime.now()
trevogaNow = False

firefox_options = Options()
firefox_options.add_argument("--headless")  # Запуск в режиме "без графического интерфейса"

# regionAlert 
browser = webdriver.Firefox(options=firefox_options)
browser.implicitly_wait(5)
browser.get('https://map.ukrainealarm.com/')
time.sleep(5)
# #\\31 8

def cheking():
    global trevogaNow
    breakWhile = False
    while not breakWhile:
        odesObl = browser.find_element(By.CSS_SELECTOR, '#\\31 8')
        if "regionAlert" in odesObl.get_attribute("class") and not trevogaNow:
            trevogaNow = True
            print("Тревога!")
            for chat in chats:
                mess = "🔴 Увага! Повітряна тривога! 🔴 📣\nПереходьте до найближчого укриття❕"
                if not chat.premium:
                    mess += f"\nРозробник бота - {admin.username}"
                bot.send_message(chat.id_chat, mess, parse_mode="HTML")
        elif "regionAlert" not in odesObl.get_attribute("class") and trevogaNow:
            trevogaNow = False
            print("Отбой тревоги!")
            for chat in chats:
                mess = "✅ Відбій повітряної тривоги ✅"
                if not chat.premium:
                    mess += f"\nРозробник бота - {admin.username}"
                bot.send_message(chat.id_chat, mess, parse_mode="HTML")
        
        time.sleep(30)

@bot.message_handler(commands=['set'])
def set(mess):
    global admin
    if admin.user_id != mess.from_user.id:
        return
    messCommands = """/add_premium
/remove_chat
/remove_premium"""
    bot.send_message(mess.from_user.id, messCommands)

@bot.message_handler(commands=['add_premium'])
def add_premium(mess):
    global admin
    if admin.user_id != mess.from_user.id:
        return
    chatsString = ""
    
    for chat in chats:
        if not chat.premium:
            chatsString += chat.title + "\n" + chat.chat_info.invite_link + "\n\n"

    bot.send_message(mess.from_user.id, chatsString)

threading1 = threading.Thread(target=cheking)
threading1.start()

bot.polling()
