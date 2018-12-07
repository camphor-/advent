from pathlib import Path
import sys
from datetime import datetime

import pytz
import yaml

from advent import models

root_dir = Path(__file__).parent
data_dir = root_dir / "data"

today = datetime.now(pytz.timezone("Asia/Tokyo")).date()

def get_today_entry():
    with open(data_dir / "entries.yml") as f:
        entries_list = yaml.load(f)
    [today_entry] = [models.Entry(**d) for d in entries_list if d["date"] == today]
    return today_entry

def get_author(name):
    with open(data_dir / "authors.yml") as f:
        authors_list = yaml.load(f)
    [author] = [models.Author(**d) for d in authors_list if d["name"] == name]
    return author

def build_tweet(entry, author):
    tweet = '''CAMPHOR- Advent Calendar {year} の本日の記事は、 {name} ({author_url}) による 「{title}」 です。
{url}

https://advent.camph.net/'''.format(year = today.year, name = author.name, author_url = author.url, title = entry.title, url = entry.url)
    return tweet

def main():
    today_entry = get_today_entry()
    author = get_author(today_entry.author)
    tweet = build_tweet(today_entry, author)
    print(tweet)

if __name__ == '__main__':
    main()
