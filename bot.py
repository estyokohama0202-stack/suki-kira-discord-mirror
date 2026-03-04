import requests
from bs4 import BeautifulSoup
import time
import json
import os

URL = "https://suki-kira.com/people/result/DJ%20SHIGE"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1478814308900278292/wgBbsBOuldG0ZdrbKYv9o9quySJlGGlJtmSFzbYW5CpHncf4o7yhWGEQTNqlkQCBkJK9"

SAVE_FILE = "last_comment.txt"


def get_last_comment():
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        return f.read()


def save_last_comment(text):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        f.write(text)


def send_discord(comment):

    payload = {
        "embeds": [
            {
                "title": "好き嫌い.com 新コメント",
                "description": comment[:2000],
                "url": URL,
                "color": 16711680
            }
        ]
    }

    requests.post(DISCORD_WEBHOOK, json=payload)


def get_comments():

    r = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0"
    })

    soup = BeautifulSoup(r.text, "html.parser")

    comments = []

    for c in soup.select(".comment-body"):
        text = c.get_text(strip=True)
        comments.append(text)

    return comments


print("BOT START")

while True:

    try:

        comments = get_comments()

        last_saved = get_last_comment()

        newest = comments[0] if comments else None

        if newest and newest != last_saved:

            print("新コメント検知")

            send_discord(newest)

            save_last_comment(newest)

        else:
            print("更新なし")

    except Exception as e:
        print("error:", e)

    time.sleep(60)
