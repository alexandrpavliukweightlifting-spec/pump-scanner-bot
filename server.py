# server.py
from flask import Flask, request
import telebot
import os
import logging

# =======================
# Налаштування
# =======================
BOT_TOKEN = "8243222112:AAGL6uhM2S7ZEg2DAWtyKqH5Yq5rFdZXOx8"
WEBHOOK_URL = f"https://pump-scanner-bot.onrender.com/{BOT_TOKEN}"

bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

# Логування всіх повідомлень
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# =======================
# Кнопки меню
# =======================
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("🟢 Увімкнути Сканер"),
        KeyboardButton("🔴 Вимкнути Сканер")
    )
    markup.add(
        KeyboardButton("📊 Статистика"),
        KeyboardButton("⚙️ Фільтри")
    )
    return markup

# =======================
# Команди бота
# =======================
@bot.message_handler(commands=['start'])
def handle_start(message):
    logging.info(f"Отримано /start від {message.from_user.id}")
    bot.send_message(
        message.chat.id,
        "Привіт! Я PumpScanner Reloaded 🤖\nОбери дію:",
        reply_markup=main_menu()
    )

# Обробка кнопок
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    logging.info(f"Отримано повідомлення від {message.from_user.id}: {message.text}")
    text = message.text

    if text == "🟢 Увімкнути Сканер":
        bot.send_message(message.chat.id, "Сканер увімкнено ✅")
    elif text == "🔴 Вимкнути Сканер":
        bot.send_message(message.chat.id, "Сканер вимкнено ❌")
    elif text == "📊 Статистика":
        bot.send_message(message.chat.id, "Тут буде статистика 📊")
    elif text == "⚙️ Фільтри":
        bot.send_message(message.chat.id, "Налаштуй фільтри: % росту, періоди ⏱️")
    else:
        bot.send_message(message.chat.id, "Не зрозумів команду. Використовуй кнопки меню.")

# =======================
# Webhook
# =======================
@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    logging.info(f"Отримано оновлення: {json_str}")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

# =======================
# Render ping / test
# =======================
@app.route("/", methods=['GET'])
def index():
    return "PumpScannerReloaded alive!", 200

# =======================
# Старт
# =======================
if __name__ == "__main__":
    # Встановлюємо webhook при запуску (тільки перший раз)
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
