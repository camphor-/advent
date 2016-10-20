#!/usr/bin/env python3
from collections import OrderedDict
from datetime import date
from operator import attrgetter, itemgetter
from os import path
import sys
from typing import Any, Dict, List

from jinja2 import Environment, FileSystemLoader
import yaml

from advent.models import Author, Entry

root_dir = path.dirname(path.abspath(__file__))
data_dir = path.join(root_dir, "data")
source_dir = path.join(root_dir, "source")
output_dir = path.join(root_dir, "output")
loader = FileSystemLoader(source_dir, encoding="utf-8")
env = Environment(loader=loader)


def load_authors() -> Dict[str, Author]:
    with open(path.join(data_dir, "authors.yml")) as f:
        authors_list = yaml.load(f)

    authors = {}
    for author_dict in authors_list:
        author = Author(**author_dict)
        authors[author.name] = author

    return authors


def load_entries() -> OrderedDict:
    today = date.today()
    authors = load_authors()

    def load_entry(d: Dict[str, Any]) -> Entry:
        entry = Entry(**d)

        if entry.author is not None:
            entry.author_url = authors[entry.author].url

        if entry.date > today:
            # Not ready
            entry.url = None

        return entry

    with open(path.join(data_dir, "entries.yml")) as f:
        entries = [load_entry(d) for d in yaml.load(f)]

    # Aggregate
    entries_by_year: OrderedDict = OrderedDict()
    years = list({e.date.year for e in entries})
    for year in sorted(years, reverse=True):
        entries_by_year[year] = [e for e in entries if e.date.year == year]

    return entries_by_year


def minify_html(html: str) -> str:
    lines = iter(html.split("\n"))
    lines = map(lambda l: l.strip(), lines)
    lines = filter(lambda l: l != "", lines)
    return "\n".join(lines)


def run(debug: bool = False):
    filename = "index.html"
    template = env.get_template(filename)
    context = {
        "debug": debug,
        "description": (
            "京都の学生コミュニティ CAMPHOR- の Advent Calendar 特設ページです。"
            "様々な記事を毎日追加していきます。"),
        "entries_for_years": load_entries(),
        "root": "http://advent.camph.net/",
        "title": "CAMPHOR- Advent Calendar"
    }
    html = minify_html(template.render(**context))

    with open(path.join(output_dir, filename), "w") as f:
        f.write(html)


if __name__ == "__main__":
    debug = "--debug" in sys.argv[1:]
    run(debug=debug)
