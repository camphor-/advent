#!/usr/bin/env python3
from collections import OrderedDict
from datetime import date
from operator import itemgetter
from os import path
import sys
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader
import yaml


root_dir = path.dirname(path.abspath(__file__))
data_dir = path.join(root_dir, "data")
source_dir = path.join(root_dir, "source")
output_dir = path.join(root_dir, "output")
loader = FileSystemLoader(source_dir, encoding="utf-8")
env = Environment(loader=loader)


def load_authors() -> Dict[str, Any]:
    with open(path.join(data_dir, "authors.yml")) as f:
        authors_list = yaml.load(f)

    authors = {}
    for author in authors_list:
        authors[author["name"]] = author

    return authors


def load_entries() -> OrderedDict:
    today = date.today()
    authors = load_authors()

    with open(path.join(data_dir, "entries.yml")) as f:
        entries_list = yaml.load(f)
    entries_list.sort(key=itemgetter("date"))

    for entry in entries_list:
        # Set author_url
        if entry["author"] is not None:
            author = authors[entry["author"]]
        else:
            author = {
                "name": None,
                "url": None
            }
        entry["author_url"] = author["url"]

        if entry["date"] > today:
            # Not ready
            entry["url"] = None

    # Aggregate
    entries: OrderedDict = OrderedDict()
    years = list({entry["date"].year for entry in entries_list})
    for year in sorted(years, reverse=True):
        entries[year] = [e for e in entries_list if e["date"].year == year]

    return entries


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
