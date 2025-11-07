import requests

BOT_TOKEN = "8243222112:AAGL6uhM2S7ZEg2DAWtyKqH5Yq5rFdZXOx8"
WEBHOOK_URL = f"https://pump-scanner-bot.onrender.com/{BOT_TOKEN}"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

response = requests.post(url, data={"url": WEBHOOK_URL})

print(response.json())
