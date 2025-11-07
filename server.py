from flask import Flask, request
from telebot import TeleBot, types
from telebot.types import Update
import json

BOT_TOKEN = "8243222112:AAGL6uhM2S7ZEg2DAWtyKqH5Yq5rFdZXOx8"
bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=["start"])
def start_handler(message):
    print("🔹 /start отримано від:", message.chat.id, message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🟢 Увімкнути Сканер", "🔴 Вимкнути Сканер", "📊 Статистика")
    bot.send_message(message.chat.id, "🚀 PumpScannerReloaded активний!", reply_markup=markup)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.data.decode("utf-8")
    print("🔹 Отримано оновлення:", json_string)
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "✅ PumpScannerReloaded alive!", 200
