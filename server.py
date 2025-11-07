import os
from flask import Flask, request
from telegram_bot import bot
from telebot.types import Update

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set")

@app.route("/", methods=["GET"])
def home():
    return "✅ PumpScannerReloaded alive!"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_string = request.data.decode("utf-8")
    update = Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.before_request
def set_webhook():
    if not getattr(app, "_hook_set", False):
        app._hook_set = True
        render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
        if render_host:
            url = f"https://{render_host}/{BOT_TOKEN}"
            bot.remove_webhook()
            bot.set_webhook(url=url)
            print(f"🌐 Webhook set: {url}")
        else:
            print("⚠️ No RENDER_EXTERNAL_HOSTNAME available.")
    return None

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
