import os
import time
import random
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

messages = [
    "Лескин сын хуйни",
    "Лескин сын шлюхи",
    "Лескин сын пидора",
    "Лескин сын бляди",
]

print("NEW VERSION DEPLOYED")

def send(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})

while True:
    msg = random.choice(messages)
    send(msg)
    print("Отправлено:", msg)
    time.sleep(60 * 60)
