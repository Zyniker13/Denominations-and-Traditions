# Denominations and Traditions

A reference library of the confessional documents of the major Protestant
traditions, kept as plain Markdown so the texts are easy to read, search, diff,
and cite. Alongside the confessions it collects the writings of the major
theologians and teachers of those traditions, and of the early church they
appeal to, on the canon of Scripture, the Apocrypha, the Hebrew text, and the
Greek and Latin versions, and on the heavens, the final state and the
resurrection of the body, with the Jewish teachers who read the same Hebrew
Bible.

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

## Theologians and teachers

See [theologians/README.md](theologians/README.md) for the full index, and
[analysis/canon-in-the-theologians.md](analysis/canon-in-the-theologians.md)
for the study of them on the canon. It is separate from the study of the confessions,
[analysis/canon-in-the-confessions.md](analysis/canon-in-the-confessions.md).

| Tradition | Teachers |
| --- | --- |
| Jewish antiquity | Josephus, the Letter of Aristeas, Philo; the Testament of Levi, 1 and 2 Enoch, the Apocalypse of Moses, 2 Baruch |
| Rabbinic, medieval and modern Jewish | The Mishnah and Talmud, *Pirke de Rabbi Eliezer*, *Bereshit Rabbah*, the daily prayer book; Maimonides and the Raavad; the Reform platforms of 1869 and 1885, the *Jewish Encyclopedia*, Kohler |
| Early church | Eusebius (Melito, Origen), Origen and Africanus, Athanasius, Cyril of Jerusalem, Rufinus, Jerome, Augustine, Gregory the Great, John of Damascus; the canon lists of Laodicea, Carthage and Trullo |
| Lutheran | Luther; Chemnitz, Gerhard, Quenstedt, Calov, Hollaz and others as collected by Schmid; H. E. Jacobs |
| Continental Reformed | Calvin, Bullinger, Ursinus, Ames, Wollebius |
| British Reformed and Anglican | Perkins, Whitaker, Ussher, Owen, Goodwin, Cosin, Vincent, Dickson, Poole's *Annotations*, Watson, Boston, Gill, Westcott |
| American Reformed | Jonathan Edwards |
| American Presbyterian (Princeton) | Archibald Alexander, Charles Hodge, W. H. Green, B. B. Warfield |

## Preservation of Scripture

[scripture/preservation/](scripture/preservation/README.md) collects every
passage in which Scripture claims that God's word endures, does not pass
away, cannot be annulled, or is kept, with the Hebrew and Greek of the Old
Testament and three Greek editions of the New.

- [analysis/preservation-of-scripture/](analysis/preservation-of-scripture/README.md)
  categorizes and assesses those claims, compares the Hebrew with the Greek
  and the Greek of the two Testaments, and measures every confession in the
  repository against them.
- [analysis/preservation-hebrew-and-greek.md](analysis/preservation-hebrew-and-greek.md)
  weighs the same claims against the history of the Old Testament text, and
  compares how strong they are when grounded in the Hebrew (Masoretic) text
  and when grounded in the Greek Septuagint.

## God Quoting Scripture

[scripture/divine-quotations/](scripture/divine-quotations/README.md) lists
every place where God himself speaks the words of earlier Scripture: Jesus in
the Gospels and in Revelation, the Father's voice from heaven, God on the
throne, and in the Old Testament the LORD repeating an earlier book. Each
entry gives the Greek of three editions of the New Testament, the Hebrew,
Brenton's and Swete's Septuagint, and the readings of the other Greek
witnesses where they decide the match.
[analysis/god-quoting-scripture/](analysis/god-quoting-scripture/README.md)
counts them by speaker and type, and sets out which text each one stands
closer to: the Septuagint, another Greek witness, or the Hebrew.

## Heaven, the New Earth and the Resurrection of the Body

[analysis/heaven-and-resurrection/](analysis/heaven-and-resurrection/README.md)
sets out the historical Reformed teaching on the “third heaven”, the final
destination of the Christian, the new heavens and the new earth, and the
resurrection of the body or “flesh”, from Calvin to Hodge and the Reformed
confessions. It tests that teaching against the Greek and Hebrew, sets it
beside the Jewish reading of the same Hebrew Bible (the Second Temple
writers, the Talmud and Midrash, Maimonides and the Raavad, Mendelssohn and
Reform), and contrasts it with the orthodox Lutheran position.
[scripture/last-things/](scripture/last-things/README.md) prints the 45
passages it argues from, in Hebrew, Greek and English.

## Index

[INDEX.md](INDEX.md) lists every confession, collection and study, and shows
which studies cover which confessions. It is generated from
[catalog.yaml](catalog.yaml); when a confession is added to the catalog, the
index lists the studies that have not yet taken it into account.

## Layout

```
confessions/          rendered Markdown, one file per document, by tradition
theologians/          the teachers' writings on the canon, the text and the last things, by tradition and author
scripture/            collections of Scripture passages, with Hebrew, Greek and English texts
analysis/             studies of the canon, of the preservation of the text, of God's quotations of Scripture, and of heaven and the resurrection
sources/              vendored upstream data the Markdown is built from, with its license
tools/                scripts that regenerate the generated files
catalog.yaml          every document, collection and study, and what each study covers
INDEX.md              the master index, generated from catalog.yaml
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

To regenerate the preservation passages, their confessional citations, and
the index:

```
python3 tools/build_preservation.py
python3 tools/build_index.py
```

To regenerate the divine quotations:

```
python3 tools/build_divine_quotations.py
```
