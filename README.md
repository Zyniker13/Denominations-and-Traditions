# Denominations and Traditions

A reference library of the confessional documents of the major Protestant
traditions, kept as plain Markdown so the texts are easy to read, search, diff,
and cite. Alongside the confessions it collects the writings of the major
theologians and teachers of those traditions, and of the early church they
appeal to, on the canon of Scripture, the Apocrypha, the Hebrew text, and the
Greek and Latin versions.

Every text in this repository is in the public domain or redistributed under a
compatible open license. Where each text came from, and under what terms, is
recorded in [SOURCES.md](SOURCES.md).

## Contents

See [confessions/README.md](confessions/README.md) for the full index.

| Tradition | Documents |
| --- | --- |
| Ecumenical creeds | Nicene and Athanasian creeds; the Apostles', Nicene, and Athanasian creeds in the Book of Concord's translation |
| Continental Reformed | Three Forms of Unity: Belgic Confession, Heidelberg Catechism, Canons of Dort |
| Presbyterian | Westminster Standards (Confession, Larger and Shorter Catechisms, Form of Government, Directories for Publick and Family Worship, and companion documents); Scots Confession |
| Anglican | Thirty-Nine Articles of Religion |
| Reformed Baptist | Second London Baptist Confession (1677/1689); Keach's Catechism |
| Congregational | Savoy Declaration of Faith and Order |
| Lutheran | [Book of Concord](confessions/lutheran/book-of-concord/README.md): Preface, the three ecumenical creeds, Augsburg Confession, Apology, Smalcald Articles, Treatise on the Power and Primacy of the Pope, Small and Large Catechisms, Formula of Concord (Epitome and Solid Declaration) |

## Theologians on the Canon

See [theologians/README.md](theologians/README.md) for the full index, and
[analysis/canon-in-the-theologians.md](analysis/canon-in-the-theologians.md)
for the study of them. It is separate from the study of the confessions,
[analysis/canon-in-the-confessions.md](analysis/canon-in-the-confessions.md).

| Tradition | Teachers |
| --- | --- |
| Jewish antiquity | Josephus, the Letter of Aristeas, Philo |
| Early church | Eusebius (Melito, Origen), Origen and Africanus, Athanasius, Cyril of Jerusalem, Rufinus, Jerome, Augustine, Gregory the Great, John of Damascus; the canon lists of Laodicea, Carthage and Trullo |
| Lutheran | Luther; Chemnitz, Gerhard, Quenstedt, Calov, Hollaz and others as collected by Schmid; H. E. Jacobs |
| Continental Reformed | Calvin, Bullinger, Ursinus, Ames, Wollebius |
| British Reformed and Anglican | Whitaker, Owen, Cosin, Gill, Westcott |
| American Presbyterian (Princeton) | Archibald Alexander, Charles Hodge, W. H. Green, B. B. Warfield |

## Layout

```
confessions/          rendered Markdown, one file per document, by tradition
theologians/          the teachers' writings on the canon and text, by tradition and author
analysis/             studies of the canon in the confessions and in the theologians
sources/              vendored upstream data the Markdown is built from, with its license
tools/                scripts that regenerate confessions/ from sources/
SOURCES.md            provenance, translation, and license for every text
```

To regenerate the Reformed texts after updating `sources/`:

```
pip install pyyaml
python3 tools/build_reformed.py
```

To regenerate the Book of Concord from thebookofconcord.org:

```
python3 tools/build_book_of_concord.py
```
