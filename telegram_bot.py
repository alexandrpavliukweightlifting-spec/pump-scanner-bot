import os
import json
import traceback
import telebot
from telebot import types
from pump_scanner import start_user_scanner, stop_user_scanner, is_scanner_running, get_today_counts

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
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
        print(traceback.format_exc())
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
