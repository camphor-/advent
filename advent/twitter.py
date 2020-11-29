from datetime import date, datetime
from pathlib import Path
import sys

from advent import data, models


data_dir = Path(__file__).parent.parent / "data"


def build_tweet(entry: models.Entry) -> str:
    return (
        f"CAMPHOR- Advent Calendar {entry.date.year} "
        f"(https://advent.camph.net/) の本日の記事は、"
        f"{entry.author} ({entry.author_url}) による「{entry.title}」です。\n"
        f"{entry.url}"
    )


def main(day: date) -> int:
    authors = data.load_authors(data_dir / "authors.yml")
    entries = data.load_entries(data_dir / "entries.yml", authors)
    entry = data.get_entry_for_day(entries, day)
    if entry is None:
        print(f"Could not find an entry for {day}")
        return 1
    elif entry.url is None:
        print(f"The entry for {day} is empty or not published yet")
        return 1
    print(build_tweet(entry))
    return 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        today = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    else:
        today = datetime.now(data.TIMEZONE).date()
    sys.exit(main(today))
