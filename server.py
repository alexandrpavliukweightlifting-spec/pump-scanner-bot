from flask import Flask, request
from telebot import TeleBot, types
from telebot.types import Update

BOT_TOKEN = "8243222112:AAGL6uhM2S7ZEg2DAWtyKqH5Yq5rFdZXOx8"
bot = TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Хендлер для старту
@bot.message_handler(commands=["start"])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🟢 Увімкнути Сканер", "🔴 Вимкнути Сканер", "📊 Статистика")
    bot.send_message(message.chat.id, "🚀 PumpScannerReloaded активний!", reply_markup=markup)

# Webhook обробка
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.data.decode("utf-8")
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Тестова сторінка
@app.route("/")
def index():
    return "✅ PumpScannerReloaded alive!", 200

# Встановлюємо webhook
bot.remove_webhook()
bot.set_webhook(url=f"https://pump-scanner-bot.onrender.com/{BOT_TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
