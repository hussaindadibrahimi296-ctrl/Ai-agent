import json
import os


DATABASE_FILE = "seen_news.json"


def load_seen_news():
    if not os.path.exists(DATABASE_FILE):
        return set()

    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as file:
            return set(json.load(file))
    except Exception:
        return set()


def save_seen_news(seen_news):
    with open(DATABASE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            list(seen_news),
            file,
            ensure_ascii=False,
            indent=2
        )
