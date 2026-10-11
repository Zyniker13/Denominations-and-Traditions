# Sources and licensing

This repository is public. It contains only texts that are in the public
domain, redistributed under the license of the collection they came from.

## Reformed Standards compendium (Reformed texts and ecumenical creeds)

- **Upstream:** <https://github.com/reformed-standards/compendium>, the data
  behind [reformedstandards.com](https://reformedstandards.com)
- **Commit vendored:** `c2f698ed3deaa50687b6dc1b14b4dbf71cb44fd8` (2026-09-21)
- **License of the collection:** Apache License 2.0, copied to
  [sources/reformed-standards-compendium/LICENSE](sources/reformed-standards-compendium/LICENSE)
- **Vendored files:** `sources/reformed-standards-compendium/data/`, unmodified
- **Changes made here:** the Markdown files under `confessions/` are generated
  from that data by `tools/build_reformed.py`. The text is unchanged; the
  script only lays it out as Markdown, reformats Scripture proof references
  (`Rom.14.7` becomes `Rom 14:7`, consecutive verses are joined), and labels
  the heads of doctrine in the Canons of Dort.

The documents themselves are all centuries old and in the public domain. The
compendium does not name the translation or edition behind each text; the notes
below say which one each text matches, and those identifications are inferred
from the wording rather than stated upstream.

| Document | Text as given |
| --- | --- |
| Nicene and Athanasian creeds | Traditional English forms |
| Belgic Confession | Traditional 19th-century English translation used by the Dutch Reformed churches in America ("We all believe with the heart, and confess with the mouth…") |
| Heidelberg Catechism | Traditional 19th-century English translation ("What is thy only comfort in life and death?") |
| Canons of Dort | Traditional 19th-century English translation, with the Rejection of Errors and the Conclusion |
| Westminster Confession of Faith | Original 1646 text as adopted by the Church of Scotland (not the American revision; see chapter 23.3) |
| Westminster Larger and Shorter Catechisms, Form of Government, Directories, companion documents | Original 17th-century texts |
| Scots Confession | 1560 text in modernized spelling |
| Thirty-Nine Articles | 1571 English text |
| Second London Baptist Confession | 1677/1689 text in modernized spelling |
| Keach's Catechism | 1693 text |
| Savoy Declaration | 1658 text |

### Left out on purpose

- **Apostles' Creed.** The compendium gives the 1988 English Language
  Liturgical Consultation (ELLC) text, which is under copyright. The
  public-domain Triglotta translation is included with the
  [Book of Concord](confessions/lutheran/book-of-concord/ecumenical-creeds.md).
- **Chalcedonian Definition.** The compendium's translation matches Henry
  Bettenson's *Documents of the Christian Church* (1943), which is under
  copyright.
- **Second Helvetic Confession.** The compendium's English text appears to be
  the modern translation printed in the Presbyterian Church (U.S.A.) *Book of
  Confessions*, which is not public domain. It will be added once a
  public-domain translation is sourced.
- **Church Order of Dort.** Not a confessional document, and the compendium's
  English translation could not be dated with confidence.

## Book of Concord

- **Source:** <https://thebookofconcord.org/>, fetched 2026-10-11
- **Text:** *Concordia Triglotta* English translation (St. Louis: Concordia
  Publishing House, 1921), edited by F. Bente and W. H. T. Dau
- **License:** public domain. The site's
  [legal page](https://thebookofconcord.org/legal/) says the Triglotta text "is
  no longer covered by copyright" and "may be freely copied, shared, et
  cetera." The same page notes that some *other* material on the site, such as
  modern Scripture translations, belongs to its owners; none of that material is
  included here. Only the confessional texts were taken, not the site's
  introductions, the Roman Confutation, or the German and Latin pages.
- **Documents:** Preface to the Christian Book of Concord; the three ecumenical
  creeds; Augsburg Confession; Apology; Smalcald Articles; Treatise on the
  Power and Primacy of the Pope; Small Catechism (with the Daily Prayers, Table
  of Duties, and Christian Questions and Answers the site gives with it); Large
  Catechism; Formula of Concord, Epitome and Solid Declaration.
- **Changes made here:** the Markdown under
  `confessions/lutheran/book-of-concord/` is generated from the site's pages by
  `tools/build_book_of_concord.py`. The text is unchanged. The script keeps the
  Triglotta paragraph numbers as superscripts, joins paragraphs the site splits
  mid-sentence at a paragraph number, and drops the site's navigation, copy
  buttons, and hover notes. Bracketed passages are as given on the site. A few
  Greek words
  in the Apology appear as the site gives them, either transliterated
  ("latreiva") or as the placeholder "((greek))".
