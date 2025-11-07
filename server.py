import telebot
from flask import Flask, request
import logging

# --------------------
# Налаштування
# --------------------
BOT_TOKEN = "8243222112:AAGL6uhM2S7ZEg2DAWtyKqH5Yq5rFdZXOx8"
WEBHOOK_URL = f"https://pump-scanner-bot.onrender.com/{BOT_TOKEN}"

# --------------------
# Логи
# --------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# --------------------
# Ініціалізація
# --------------------
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --------------------
# Обробка /start
# --------------------
@bot.message_handler(commands=['start'])
def start(message):
    logging.info(f"Отримано /start від {message.from_user.id}")
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🟢 Увімкнути Сканер', '🔴 Вимкнути Сканер', '📊 Статистика')
    bot.send_message(message.chat.id, "Привіт! Вибери опцію:", reply_markup=markup)

# --------------------
# Обробка кнопок
# --------------------
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    logging.info(f"Отримано повідомлення: {message.text} від {message.from_user.id}")
    if message.text == '🟢 Увімкнути Сканер':
        bot.send_message(message.chat.id, "Сканер увімкнено ✅")
    elif message.text == '🔴 Вимкнути Сканер':
        bot.send_message(message.chat.id, "Сканер вимкнено ❌")
    elif message.text == '📊 Статистика':
        bot.send_message(message.chat.id, "Статистика: ...")
    else:
        bot.send_message(message.chat.id, "Я не розумію цю команду 😅")

# --------------------
# Flask webhook
# --------------------
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# --------------------
# Головна сторінка
# --------------------
@app.route('/')
def index():
    return "Bot is running ✅"

# ❌ Для Render app.run не потрібен
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=10000)
