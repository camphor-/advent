advent
======

[![Circle CI](https://circleci.com/gh/camphor-/advent.svg?style=shield&circle-token=b81bec23b8042e1a5cdd85f15fedcdc6bd3058b3)](https://circleci.com/gh/camphor-/advent)

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
$ python gen_tweet.py
```

Facebook Post (一部):
```
$ cat data/entries.yml | sed -E "s;- date: [0-9]{4}-([0-9]{2})-([0-9]{2});\1/\2;" | sed -E "s;  author: (.*)$;  \1 による;" | sed -E "s;  title: (.*)$;  「\1」;" | sed -E "s;  url: (.*)$;  \1;"
```
