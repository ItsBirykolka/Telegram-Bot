import os
import time
import random
import requests
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

messages = [
    "Лескин сын хуйни",
    "Лескин сын шлюхи",
    "Лескин сын пидора",
    "Лескин сын бляди",
    "Лескин сын пизды",
    "Лескин сын проститутки",
    "Лескин сын максима",
    "Лескин сын долбоеба",
]

print("NEW VERSION DEPLOYED")

def send(text, chat_id=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": chat_id or CHAT_ID, "text": text})

def delete_message(chat_id, message_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteMessage"
    requests.post(url, data={"chat_id": chat_id, "message_id": message_id})

def hourly_sender():
    while True:
        msg = random.choice(messages)
        send(msg)
        print("Отправлено (hourly):", msg)
        time.sleep(60 * 60)

t = threading.Thread(target=hourly_sender, daemon=True)
t.start()

def clear_old_updates():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    resp = requests.get(url, params={"timeout": 0}).json()
    updates = resp.get("result", [])
    if updates:
        return updates[-1]["update_id"] + 1
    return None

offset = clear_old_updates()
while True:
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"timeout": 30, "offset": offset}
        resp = requests.get(url, params=params, timeout=35).json()

        for update in resp.get("result", []):
            offset = update["update_id"] + 1
            msg = update.get("message", {})
            text = msg.get("text", "")
            chat_id = msg.get("chat", {}).get("id")
            message_id = msg.get("message_id")

            if text.startswith("/les"):
                delete_message(chat_id, message_id)
                reply = random.choice(messages)
                send(reply)
                print(f"Команда /les, отправлено: {reply}")
            elif "напоминание" in text.lower() or "лескин" in text.lower():
                reply = random.choice(messages)
                send(reply, chat_id)
                print(f"Слово 'напоминание' или 'лескин', отправлено: {reply}")

    except Exception as e:
        print("Ошибка polling:", e)
        time.sleep(5)
