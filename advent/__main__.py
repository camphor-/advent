from pathlib import Path
import sys
from typing import Any, Dict

from jinja2 import Environment, FileSystemLoader

from advent import data


NUMBER_OF_LATEST_PUBLISHED_ENTRIES = 10

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"
source_dir = root_dir / "source"
output_dir = root_dir / "output"
loader = FileSystemLoader(str(source_dir), encoding="utf-8")
env = Environment(loader=loader)


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
    authors = data.load_authors(data_dir / "authors.yml")
    entries = data.load_entries(data_dir / "entries.yml", authors)
    entries_by_year = data.group_entries_by_year(entries)
    latest_published_entries = data.get_last_published_entries(
        entries,
        NUMBER_OF_LATEST_PUBLISHED_ENTRIES,
    )
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
    render_and_write("atom.xml", context)


def main() -> None:
    debug = "--debug" in sys.argv[1:]
    run(debug=debug)


main()
