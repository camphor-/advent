from dataclasses import dataclass
import datetime
from typing import List, Optional


@dataclass
class Author:
    name: str
    url: str


@dataclass
class Entry:
    date: datetime.date
    title: Optional[str]
    url: Optional[str]
    author: Optional[str]
    author_url: Optional[str] = None
    tags: Optional[List[str]] = None
