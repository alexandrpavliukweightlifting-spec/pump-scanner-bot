import threading
import time
import random

# словник для стану сканера по chat_id
_scanners = {}

def start_user_scanner(chat_id, send_message):
    if chat_id in _scanners:
        return
    running = True
    _scanners[chat_id] = running

    def scanner_loop():
        while _scanners.get(chat_id):
            # Тут ваша логіка памп-сканера
            coin = random.choice(["BTC", "ETH", "DOGE"])
            price = round(random.uniform(1, 100), 2)
            send_message(chat_id, f"📈 {coin} памп! Ціна: {price}$")
            time.sleep(10)  # пауза між перевірками
    t = threading.Thread(target=scanner_loop, daemon=True)
    t.start()

def stop_user_scanner(chat_id):
    _scanners[chat_id] = False

def is_scanner_running(chat_id):
    return _scanners.get(chat_id, False)

def get_today_counts():
    # Повертає тестову статистику
    return {"BTC": random.randint(0, 5), "ETH": random.randint(0, 5), "DOGE": random.randint(0, 5)}
