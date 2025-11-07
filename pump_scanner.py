import threading
import time

SCANNERS = {}

def start_user_scanner(chat_id, send_message):
    """Запуск "сканера" у фоновому потоці"""
    if chat_id in SCANNERS:
        return
    stop_flag = threading.Event()

    def scanner():
        while not stop_flag.is_set():
            # Тут буде логіка пампу Binance
            send_message(chat_id, "🚀 Сканер працює...")
            time.sleep(60)

    t = threading.Thread(target=scanner, daemon=True)
    t.start()
    SCANNERS[chat_id] = stop_flag

def stop_user_scanner(chat_id):
    if chat_id in SCANNERS:
        SCANNERS[chat_id].set()
        del SCANNERS[chat_id]

def is_scanner_running(chat_id):
    return chat_id in SCANNERS

def get_today_counts():
    return {"BTC": 2, "ETH": 1}  # приклад
