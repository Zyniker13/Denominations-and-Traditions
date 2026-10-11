# The Book of Concord (1580)

The texts are taken from [thebookofconcord.org](https://thebookofconcord.org/),
whose English text is the *Concordia Triglotta* translation (St. Louis:
Concordia Publishing House, 1921). The site's
[legal page](https://thebookofconcord.org/legal/) states that the Triglotta is
no longer under copyright. Superscript numbers in the text are the Triglotta's
paragraph numbers, the ones used in standard citations (e.g. "SD VII 12").
See [SOURCES.md](/SOURCES.md) for details.

One file per document, in the order of the Book of Concord:

- [Preface to the Christian Book of Concord (1580)](preface.md)
- [The Three Universal or Ecumenical Creeds](ecumenical-creeds.md) (Apostles', Nicene, Athanasian)
- [The Augsburg Confession (1530)](augsburg-confession.md)
- [The Apology of the Augsburg Confession (1531)](apology-of-the-augsburg-confession.md)
- [The Smalcald Articles (1537)](smalcald-articles.md)
- [Treatise on the Power and Primacy of the Pope (1537)](treatise-on-the-power-and-primacy-of-the-pope.md)
- [The Small Catechism (1529)](small-catechism.md)
- [The Large Catechism (1529)](large-catechism.md)
- [The Formula of Concord: Epitome (1577)](formula-of-concord-epitome.md)
- [The Formula of Concord: Solid Declaration (1577)](formula-of-concord-solid-declaration.md)

To regenerate the files from the site:

```
python3 tools/build_book_of_concord.py
```
