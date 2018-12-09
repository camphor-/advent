from datetime import datetime
from pathlib import Path

import pytz
import yaml

from advent import models

data_dir = Path(__file__).parent / "data"

today = datetime.now(pytz.timezone("Asia/Tokyo")).date()


def get_today_entry():
    with open(data_dir / "entries.yml") as f:
        entries_list = yaml.load(f)
    for d in entries_list:
        if d["date"] == today:
            return models.Entry(**d)
    return None


def get_author(name):
    with open(data_dir / "authors.yml") as f:
        authors_list = yaml.load(f)
    for d in authors_list:
        if d["name"] == name:
            return models.Author(**d)
    return None


def build_tweet(entry, author):
    tweet = f'''CAMPHOR- Advent Calendar {today.year} の本日の記事は、 {author.name} ({author.url}) による 「{entry.title}」 です。
{entry.url}

https://advent.camph.net/'''
    return tweet


def main():
    today_entry = get_today_entry()
    author = get_author(today_entry.author)
    tweet = build_tweet(today_entry, author)
    print(tweet)


if __name__ == '__main__':
    main()
