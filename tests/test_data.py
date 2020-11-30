from datetime import date
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from advent.data import (
    get_entry_for_day, get_last_published_entries, group_entries_by_year,
    load_authors, load_entries,
)
from advent.models import Author, Entry

VALID_AUTHORS_YAML = """
- name: camphor
  url: https://example.com/camphor/
- name: house
  url: https://example.com/~house
"""
INVALID_AUTHORS_YAML = """
- name: no-url
"""
AUTHORS = {
    "camphor": Author(name="camphor", url="https://example.com/camphor/"),
    "house": Author(name="house", url="https://example.com/~house"),
}
VALID_ENTRIES_YAML = """
# Published
- date: 2014-12-01
  author: camphor
  title: CAMPHOR- アドベントカレンダー 2014 を始めます!
  url: https://example.com/news/advent-calendar-2014/

# To be published
- date: 2014-12-02
  author: house
  title: CAMPHOR- HOUSE
  url: https://example.com/news/house/

# Title/URL to be decided
- date: 2015-12-01
  author: camphor
  title: null
  url: null

# Author to be decided
- date: 2015-12-02
  author: null
  title: null
  url: null
"""
INVALID_ENTRIES_YAML = """
- date: today
"""
ENTRIES = [
    Entry(
        date=date(2014, 12, 1),
        title="CAMPHOR- アドベントカレンダー 2014 を始めます!",
        url="https://example.com/news/advent-calendar-2014/",
        author="camphor",
        author_url="https://example.com/camphor/",
    ),
    Entry(
        date=date(2014, 12, 2),
        title="CAMPHOR- HOUSE",
        url=None,
        author="house",
        author_url="https://example.com/~house",
    ),
    Entry(
        date=date(2015, 12, 1),
        title=None,
        url=None,
        author="camphor",
        author_url="https://example.com/camphor/",
    ),
    Entry(
        date=date(2015, 12, 2),
        title=None,
        url=None,
        author=None,
        author_url=None,
    ),
]


def test_load_authors_succeeds(mocker: MockerFixture) -> None:
    mocker.patch("advent.data.open",
                 mocker.mock_open(read_data=VALID_AUTHORS_YAML))
    assert load_authors(Path("authors.yml")) == AUTHORS


def test_load_authors_fails(mocker: MockerFixture) -> None:
    mocker.patch("advent.data.open",
                 mocker.mock_open(read_data=INVALID_AUTHORS_YAML))
    with pytest.raises(TypeError):
        load_authors(Path("authors.yml"))


@pytest.mark.freeze_time("2014-12-01T12:00:00Z")
def test_load_entries_succeeds(mocker: MockerFixture) -> None:
    mocker.patch("advent.data.open",
                 mocker.mock_open(read_data=VALID_ENTRIES_YAML))
    assert load_entries(Path("entries.yml"), AUTHORS) == ENTRIES


def test_load_entries_fails(mocker: MockerFixture) -> None:
    mocker.patch("advent.data.open",
                 mocker.mock_open(read_data=INVALID_ENTRIES_YAML))
    with pytest.raises(TypeError):
        load_entries(Path("entries.yml"), {})


def test_group_entries_by_year() -> None:
    # Verify insertion order as well
    assert list(group_entries_by_year(ENTRIES).items()) == [
        (2015, [ENTRIES[2], ENTRIES[3]]),
        (2014, [ENTRIES[0], ENTRIES[1]]),
    ]


def test_get_last_published_entries() -> None:
    entries = [
        Entry(
            date=date(2014, 12, i),
            title=f"Entry #{i}",
            url=f"https://example.com/news/entry-{i}",
            author="camphor",
            author_url="https://example.com/camphor/",
        ) for i in range(1, 4)
    ] + [
        Entry(
            date=date(2014, 12, i),
            title=f"Entry #{i}",
            url=None,
            author="camphor",
            author_url="https://example.com/camphor/",
        ) for i in range(4, 7)
    ]
    assert get_last_published_entries(entries, 2) == [
        Entry(
            date=date(2014, 12, 3),
            title="Entry #3",
            url="https://example.com/news/entry-3",
            author="camphor",
            author_url="https://example.com/camphor/",
        ),
        Entry(
            date=date(2014, 12, 2),
            title="Entry #2",
            url="https://example.com/news/entry-2",
            author="camphor",
            author_url="https://example.com/camphor/",
        ),
    ]


def test_get_entry_for_day() -> None:
    assert get_entry_for_day(ENTRIES, date(2014, 12, 1)) == ENTRIES[0]
    assert get_entry_for_day(ENTRIES, date(2014, 12, 31)) is None
