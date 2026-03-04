import requests
import time
import os

TARGET = "DJ SHIGE"

API = "https://suki-kira.com/api/comment/list"

WEBHOOK_URL = "ここにDiscordWebhookURL"

SAVE_FILE = "last_id.txt"


def load_last_id():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        return f.read()


def save_last_id(cid):
    with open(SAVE_FILE, "w") as f:
        f.write(str(cid))


def send_discord(comment):

    payload = {
        "embeds": [
            {
                "title": "🆕 好き嫌い.com 新コメント",
                "description": comment["comment"],
                "url": f"https://suki-kira.com/people/result/{TARGET}",
                "color": 65280,
                "footer": {
                    "text": "好き嫌い.com"
                }
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=payload)


print("BOT START")

while True:

    try:

        payload = {
            "target": TARGET,
            "page": 1
        }

        r = requests.post(API, json=payload)

        data = r.json()

        if "comments" not in data:
            time.sleep(60)
            continue

        comments = data["comments"]

        if not comments:
            time.sleep(60)
            continue

        newest = comments[0]

        last_id = load_last_id()

        if str(newest["id"]) != last_id:

            print("新コメント検知")

            send_discord(newest)

            save_last_id(newest["id"])

        else:
            print("更新なし")

    except Exception as e:
        print("ERROR:", e)

    time.sleep(60)
