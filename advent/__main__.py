from datetime import datetime
from operator import attrgetter
from pathlib import Path
import sys
from typing import Any, Dict, Iterable, List

from jinja2 import Environment, FileSystemLoader
import pytz
import yaml

from .models import Author, Entry


NUMBER_OF_LATEST_PUBLISHED_ENTRIES = 10

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
source_dir = root_dir / "source"
output_dir = root_dir / "output"
loader = FileSystemLoader(str(source_dir), encoding="utf-8")
env = Environment(loader=loader)

today = datetime.now(pytz.timezone("Asia/Tokyo")).date()


def load_authors() -> Dict[str, Author]:
    with open(data_dir / "authors.yml") as f:
        authors_list = yaml.load(f, Loader=yaml.SafeLoader)
    authors = [Author(**d) for d in authors_list]
    return {author.name: author for author in authors}


def load_entries() -> List[Entry]:
    authors = load_authors()

    def load_entry(d: Dict[str, Any]) -> Entry:
        entry = Entry(**d)

        if entry.author is not None:
            entry.author_url = authors[entry.author].url

        if entry.date > today:
            # Not ready
            entry.url = None

        return entry

    with open(data_dir / "entries.yml") as f:
        return list(map(load_entry, yaml.load(f, Loader=yaml.SafeLoader)))


def group_entries_by_year(entries: Iterable[Entry]) -> Dict[int, List[Entry]]:
    entries_by_year = {}
    years = list({e.date.year for e in entries})
    for year in sorted(years, reverse=True):
        entries_by_year[year] = [e for e in entries if e.date.year == year]
    return entries_by_year


def minify_html(html: str) -> str:
    lines = iter(html.split("\n"))
    lines = filter(lambda line: line != "", map(lambda l: l.strip(), lines))
    return "\n".join(lines)


def render_and_write(
        filename: str,
        context: Dict[str, Any],
        minify: bool = True) -> None:
    template = env.get_template(filename)
    result = template.render(**context)
    if minify:
        result = minify_html(result)
    with open(output_dir / filename, "w") as f:
        f.write(result)


def run(debug: bool = False) -> None:
    entries = load_entries()
    entries_by_year = group_entries_by_year(entries)
    latest_published_entries = sorted(
        filter(lambda e: e.url, entries), reverse=True, key=attrgetter("date")
    )[:NUMBER_OF_LATEST_PUBLISHED_ENTRIES]
    context = {
        "debug": debug,
        "description": (
            "京都の学生コミュニティ CAMPHOR- の Advent Calendar 特設ページです。"
            "様々な記事を毎日追加していきます。"),
        "entries_for_years": entries_by_year,
        "latest_published_entries": latest_published_entries,
        "root": "https://advent.camph.net/",
        "title": "CAMPHOR- Advent Calendar"
    }

    render_and_write("index.html", context)
    render_and_write("amp.html", context)
    render_and_write("atom.xml", context)


def main() -> None:
    debug = "--debug" in sys.argv[1:]
    run(debug=debug)


main()
