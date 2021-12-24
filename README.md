advent
======

![GitHub Actions](https://github.com/camphor-/advent/actions/workflows/build-and-sync.yml/badge.svg?branch=master)

CAMPHOR- Advent Calendar

Requirements
------------
- Docker
- docker-compose

Edit
----
1. Edit [data/authors.yml](data/authors.yml)
2. Edit [data/entries.yml](data/entries.yml)

If author, title, or url of an entry is not decided, set null.

Compile & Development
---------------------
1. Run `docker-compose up -d`
2. Open http://localhost:8000

Generate Tweet & Post
---------------------
Tweet:
```
$ docker-compose exec advent python -m advent.twitter
OR
$ docker-compose exec advent python -m advent.twitter YYYY-MM-DD
```

Facebook Post (一部):
```
$ cat data/entries.yml | sed -E "s;- date: [0-9]{4}-([0-9]{2})-([0-9]{2});\1/\2;" | sed -E "s;  author: (.*)$;  \1 による;" | sed -E "s;  title: (.*)$;  「\1」;" | sed -E "s;  url: (.*)$;  \1;"
```
