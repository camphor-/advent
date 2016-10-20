import datetime
from typing import Optional


class Author:
    name: str
    url: str

    def __init__(self, *, name: str, url: str) -> None:
        self.name = name
        self.url = url


class Entry:
    author: Optional[str]
    author_url: Optional[str] = None
    date: datetime.date
    title: Optional[str]
    url: Optional[str]

    def __init__(self, *, author: Optional[str], date: datetime.date,
                 title: Optional[str], url: Optional[str]) -> None:
        self.author = author
        self.date = date
        self.title = title
        self.url = url
