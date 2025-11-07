import threading
import time

# Зберігаємо стан сканера
scanners = {}
today_counts = {"BTC": 0, "ETH": 0}

def start_user_scanner(chat_id, send_message):
    if chat_id in scanners and scanners[chat_id]['running']:
        return

    scanners[chat_id] = {'running': True}
    
    def scan_loop():
        while scanners[chat_id]['running']:
            # Тут твоя логіка памп сканера
            # Для тесту відправляємо повідомлення кожні 10 секунд
            send_message(chat_id, "💹 Тестовий памп BTC +5%")
            today_counts["BTC"] += 1
            time.sleep(10)
    
    thread = threading.Thread(target=scan_loop, daemon=True)
    scanners[chat_id]['thread'] = thread
    thread.start()

def stop_user_scanner(chat_id):
    if chat_id in scanners:
        scanners[chat_id]['running'] = False

def is_scanner_running(chat_id):
    return scanners.get(chat_id, {}).get('running', False)

def get_today_counts():
    return today_counts
