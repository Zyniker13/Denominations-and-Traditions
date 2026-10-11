# Denominations and Traditions

A reference library of the confessional documents of the major Protestant
traditions, kept as plain Markdown so the texts are easy to read, search, diff,
and cite.

Every text in this repository is in the public domain or redistributed under a
compatible open license. Where each text came from, and under what terms, is
recorded in [SOURCES.md](SOURCES.md).

## Contents

See [confessions/README.md](confessions/README.md) for the full index.

| Tradition | Documents |
| --- | --- |
| Ecumenical creeds | Nicene and Athanasian creeds (the Apostles' Creed will come with the Book of Concord) |
| Continental Reformed | Three Forms of Unity: Belgic Confession, Heidelberg Catechism, Canons of Dort |
| Presbyterian | Westminster Standards (Confession, Larger and Shorter Catechisms, Form of Government, Directories for Publick and Family Worship, and companion documents); Scots Confession |
| Anglican | Thirty-Nine Articles of Religion |
| Reformed Baptist | Second London Baptist Confession (1677/1689); Keach's Catechism |
| Congregational | Savoy Declaration of Faith and Order |
| Lutheran | Book of Concord (pending; see [its folder](confessions/lutheran/book-of-concord/README.md)) |

## Layout

```
confessions/          rendered Markdown, one file per document, by tradition
sources/              vendored upstream data the Markdown is built from, with its license
tools/                scripts that regenerate confessions/ from sources/
SOURCES.md            provenance, translation, and license for every text
```

To regenerate the Reformed texts after updating `sources/`:

```
pip install pyyaml
python3 tools/build_reformed.py
```
