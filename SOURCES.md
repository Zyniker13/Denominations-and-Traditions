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
  public-domain Triglotta translation will arrive with the Book of Concord.
- **Chalcedonian Definition.** The compendium's translation matches Henry
  Bettenson's *Documents of the Christian Church* (1943), which is under
  copyright.
- **Second Helvetic Confession.** The compendium's English text appears to be
  the modern translation printed in the Presbyterian Church (U.S.A.) *Book of
  Confessions*, which is not public domain. It will be added once a
  public-domain translation is sourced.
- **Church Order of Dort.** Not a confessional document, and the compendium's
  English translation could not be dated with confidence.

## Book of Concord (pending)

- **Source:** <https://thebookofconcord.org/>
- **Text:** *Concordia Triglotta* English translation (1921), which the site's
  [legal page](https://thebookofconcord.org/legal/) describes as no longer
  under copyright.
