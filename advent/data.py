from datetime import date, datetime
from operator import attrgetter
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

import pytz
import yaml

from advent.models import Author, Entry

TIMEZONE = pytz.timezone("Asia/Tokyo")


def load_authors(authors_file: Path) -> Dict[str, Author]:
    """Load a list of authors from the given file"""
    with open(authors_file) as f:
        authors_list = yaml.load(f, Loader=yaml.SafeLoader)
    authors = [Author(**d) for d in authors_list]
    return {author.name: author for author in authors}


def load_entries(
        entries_file: Path,
        authors: Mapping[str, Author]
) -> List[Entry]:
    """Load a list of entries from the given file

    This method replaces url of entries which are not published yet with None.
    """
    today = datetime.now(tz=TIMEZONE).date()

    def load_entry(d: Dict[str, Any]) -> Entry:
        entry = Entry(**d)

        if entry.author is not None:
            entry.author_url = authors[entry.author].url

        if entry.date > today:
            # Not ready
            entry.url = None

        return entry

    with open(entries_file) as f:
        return list(map(load_entry, yaml.load(f, Loader=yaml.SafeLoader)))


def group_entries_by_year(entries: Iterable[Entry]) -> Dict[int, List[Entry]]:
    """Groups entries by year in descending order"""
    entries_by_year = {}
    years = list({e.date.year for e in entries})
    for year in sorted(years, reverse=True):
        entries_by_year[year] = [e for e in entries if e.date.year == year]
    return entries_by_year


def get_last_published_entries(
        entries: Iterable[Entry],
        n: int
) -> List[Entry]:
    """Get last N published entries in descending order"""
    return sorted(
        filter(lambda e: e.url, entries), reverse=True, key=attrgetter("date")
    )[:n]


def get_entry_for_day(
        entries: Iterable[Entry],
        day: date
) -> Optional[Entry]:
    """Find an entry on the given day if it exists"""
    for entry in entries:
        if entry.date == day:
            return entry
    return None
