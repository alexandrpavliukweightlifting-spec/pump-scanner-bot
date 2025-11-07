import telebot
from flask import Flask
import threading
import time
import logging
import os
import json
from pump_scanner import start_user_scanner, stop_user_scanner, is_scanner_running, get_today_counts

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Ініціалізація бота
SETTINGS_PATH = "settings.json"

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

data = load_json(SETTINGS_PATH)
BOT_TOKEN = os.getenv("BOT_TOKEN") or data.get("bot_token")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def get_user_settings(chat_id):
    data = load_json(SETTINGS_PATH)
    key = str(chat_id)
    if key not in data:
        data[key] = {"enabled": False}
        save_json(SETTINGS_PATH, data)
    return data[key]

def save_user_settings(chat_id, settings):
    data = load_json(SETTINGS_PATH)
    data[str(chat_id)] = settings
    save_json(SETTINGS_PATH, data)

def main_menu(chat_id):
    s = get_user_settings(chat_id)
    from telebot import types
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if s.get("enabled"):
        markup.add("🔴 Вимкнути Сканер")
    else:
        markup.add("🟢 Увімкнути Сканер")
    markup.add("📊 Статистика")
    return markup

@bot.message_handler(commands=['start'])
def on_start(m):
    bot.send_message(m.chat.id, "🚀 PumpScannerReloaded активний!", reply_markup=main_menu(m.chat.id))

@bot.message_handler(func=lambda m: m.text in ["🟢 Увімкнути Сканер", "🔴 Вимкнути Сканер"])
def toggle_scanner(m):
    chat_id = m.chat.id
    s = get_user_settings(chat_id)
    try:
        if m.text == "🟢 Увімкнути Сканер":
            s['enabled'] = True
            start_user_scanner(chat_id, send_message)
        else:
            s['enabled'] = False
            stop_user_scanner(chat_id)
        save_user_settings(chat_id, s)
        bot.send_message(chat_id, "✅ Оновлено стан сканера", reply_markup=main_menu(chat_id))
    except Exception as e:
        print(e)
        bot.send_message(chat_id, "❌ Помилка при перемиканні сканера", reply_markup=main_menu(chat_id))

@bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def show_stats(m):
    stats = get_today_counts()
    lines = [f"{k}: {v}" for k, v in stats.items()]
    bot.send_message(m.chat.id, "📊 Статистика:\n" + "\n".join(lines), reply_markup=main_menu(m.chat.id))

def send_message(chat_id, text):
    try:
        bot.send_message(chat_id, text)
    except:
        print(f"Помилка при відправці повідомлення {chat_id}: {text}")

@app.route('/')
def index():
    return "Bot is running ✅"

def polling():
    while True:
        try:
            logging.info("Polling запущено...")
            bot.infinity_polling(timeout=60)
        except Exception as e:
            logging.error(f"Помилка polling: {e}")
            time.sleep(5)

if __name__ == "__main__":
    thread = threading.Thread(target=polling, daemon=True)
    thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
