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

## Theologians and teachers (`theologians/`)

The texts under `theologians/` are public-domain English editions, transcribed
verbatim from the sources below and fetched 2026-10-11. Each file's opening
table gives the full edition, the URLs used, exactly which sections are
included, how page numbers are marked, and any corrections made. The general
method was:

- **Clean digital texts** (CCEL's ThML editions of the Schaff Fathers,
  Hazlitt's *Table Talk* and Hodge; Project Gutenberg's Whiston) were converted
  by script, keeping the editions' footnotes and page anchors.
- **Scanned books** (archive.org) were built from the OCR of one or more
  independent scans of the same edition, compared word by word, and checked
  against the page images wherever the readings disagreed or the text was
  Greek, Hebrew or a footnote. Ames and Wollebius, whose seventeenth-century
  type defeats OCR, were transcribed by hand from the page images and
  proofread a second time.
- **Only obvious OCR errors were corrected.** The editions' own spelling,
  punctuation and misprints are kept. Where Hebrew or Greek could not be read
  with confidence it is given as `[Hebrew]` or `[Greek]`. Marginal side-notes,
  and footnotes that could not be read reliably, are omitted, and each file
  says when that is so.
- **newadvent.org was not used**, because it claims copyright in its edition
  of the Fathers; the same translations were taken from CCEL.

| Files | Edition | Source | Public domain because |
| --- | --- | --- | --- |
| `jewish-antiquity/josephus/` | Whiston, *Genuine Works of Flavius Josephus* | Project Gutenberg #2848, #2849 (checked against CCEL) | 1737 |
| `jewish-antiquity/aristeas/` | Thackeray, *The Letter of Aristeas* (SPCK, 1917) | archive.org `theletterofarist00unknuoft` | Published 1917 |
| `jewish-antiquity/philo/` | Yonge, *Works of Philo Judaeus* III (Bohn, 1855) | archive.org `theworksofphiloj03yonguoft` | 1855 |
| `early-church/eusebius/`, `origen/`, `athanasius/`, `cyril-of-jerusalem/`, `councils/`, `rufinus/`, `jerome/`, `augustine/`, `john-of-damascus/` | *Ante-Nicene Fathers* IV and VII (1885–86); *Nicene and Post-Nicene Fathers* I.1–2 and II.1, 3, 4, 6, 7, 9, 14 (1886–1900) | CCEL ThML volumes (`anf04`, `anf07`, `npnf101`, `npnf102`, `npnf201`, `npnf203`, `npnf204`, `npnf206`, `npnf207`, `npnf209`, `npnf214`) | 1885–1900 |
| `early-church/gregory-the-great/` | *Morals on the Book of Job* II (Library of the Fathers, Oxford, 1845) | archive.org `moralsonbookofjo02greguoft` | 1845 |
| `lutheran/martin-luther/prefaces-to-the-bible.md` | *Works of Martin Luther* VI, tr. C. M. Jacobs (Philadelphia: A. J. Holman, 1932) | archive.org `in.ernet.dli.2015.180138` | Copyright not renewed (see below) |
| `lutheran/martin-luther/table-talk.md` | Hazlitt, *The Table-Talk of Martin Luther* (1857; Lutheran Publication Society printing) | CCEL `luther/tabletalk` | 1857 |
| `lutheran/martin-luther/to-the-councilmen-on-the-languages.md` | Painter, *Luther on Education* (Lutheran Publication Society, 1889) | archive.org `lutheroneduatio00pain` | 1889 |
| `lutheran/heinrich-schmid/` | Schmid, *Doctrinal Theology*, tr. Hay and Jacobs, 4th ed. (1899) | archive.org `doctrinaltheolog00schmuoft` | 1899 |
| `lutheran/henry-eyster-jacobs/` | Jacobs, *A Summary of the Christian Faith* (1905); *The Lutheran Cyclopedia* (Scribner's, 1899) | archive.org `summaryofchristi00jaco`, `cu31924029466533` | 1905; 1899 |
| `reformed/continental/calvin/` | Calvin Translation Society: *Institutes*, tr. Beveridge (1845); *Tracts* III, tr. Beveridge (1851); commentaries on Hebrews (Owen, 1853), the Catholic Epistles (Owen, 1855), Timothy (Pringle, 1856) | archive.org scans named in each file, collated with CCEL | 1845–1856 |
| `reformed/continental/bullinger/` | *The Decades* I (Parker Society, 1849) | archive.org `decadesofbulling01bulluoft`, `decadeshenrybul04britgoog` | 1849 |
| `reformed/continental/ursinus/` | *Commentary on the Heidelberg Catechism*, tr. Williard (Columbus, 1852) | archive.org `commdrza00ursi` and two later printings from the same plates | 1852 |
| `reformed/continental/ames/` | *The Marrow of Sacred Divinity* (London, 1638/39) | archive.org `marrowsacdi00ames` (page images) | 1638/39 |
| `reformed/continental/wollebius/` | *The Abridgment of Christian Divinity*, tr. Ross, 3rd ed. (London, 1660) | archive.org `abridgmentofchri00woll`, checked against a 1656 scan | 1660 |
| `reformed/british/whitaker/` | *A Disputation on Holy Scripture*, tr. Fitzgerald (Parker Society, 1849) | archive.org `disputationonhol00whituoft` and nine other scans | 1849 |
| `reformed/british/owen/` | *Works of John Owen* XVI, ed. Goold (1850–53; 1862 issue) | archive.org `owensworks16owenuoft` and three other scans | 1850–62 |
| `reformed/british/cosin/` | *Works of John Cosin* III (Library of Anglo-Catholic Theology, Oxford, 1849) | archive.org `workscos03cosiuoft` and three other scans | 1849 |
| `reformed/british/gill/` | *A Complete Body of Doctrinal and Practical Divinity* I (Tegg, 1839); *A Dissertation concerning the Antiquity of the Hebrew-Language* (London, 1767) | archive.org `completebodyofdo01gill`, `dissertationconc00gill` | 1839; 1767 |
| `reformed/british/westcott/` | *A General Survey of the History of the Canon of the New Testament*, 6th ed. (Macmillan, 1889); *The Bible in the Church*, revised text (Macmillan, 1901 printing) | archive.org scans named in each file | 1889; 1901 |
| `reformed/princeton/archibald-alexander/` | *The Canon of the Old and New Testaments Ascertained*, new ed. (Presbyterian Board of Publication, 1851) | archive.org `canonofoldnewtes00alex` and three other scans | 1851 |
| `reformed/princeton/hodge/` | *Systematic Theology* I (Scribner, 1871) | CCEL `hodge/theology1`, transcribed from a 1940 facsimile reprint of the 1871 text | 1871 |
| `reformed/princeton/green/` | *General Introduction to the Old Testament: The Canon* (Scribner, 1898) and *The Text* (1899) | archive.org scans named in each file | 1898; 1899 |
| `reformed/princeton/warfield/` | "The Formation of the Canon of the New Testament" (1892), as reprinted in *Revelation and Inspiration* (Oxford University Press, 1927) | archive.org `revelationinspir00warf` | 1927 |

### Copyright renewal search: *Works of Martin Luther*, vol. VI

Volume VI of the Philadelphia edition was published in 1932, so it is in the
public domain in the United States only if its copyright was not renewed in its
28th year. The renewal records for January 1958 through June 1961 (the Catalog
of Copyright Entries as transcribed by Project Gutenberg, eBooks #11817–11823)
were searched for "Luther", "Works of Martin Luther", "Holman", "Muhlenberg",
"United Lutheran" and "Board of Publication". Volume V (1931) *was* renewed
(R238530, 26 June 1959), and is therefore not used. No renewal of volume VI
appears. Luther's letter to the councilmen is taken from Painter's 1889
translation rather than from volume IV (1931).

### Left out on purpose

- **Modern translations** of Turretin (Giger and Dennison, 1992; Beardslee,
  1981), Chemnitz (Kramer, 1971), Gerhard (Concordia, 2006 onward), the Leiden
  *Synopsis* (Brill, 2014 onward) and *Luther's Works* (American Edition) are
  under copyright and are not used or paraphrased. Chemnitz and Gerhard appear
  only as quoted in Schmid's 1899 translation.
- **Summaries in place of texts.** The *Nicene and Post-Nicene Fathers* gives
  only editorial summaries of several of Jerome's prefaces, and omits part of
  his *Apology* (II.26–32); those summaries and notes are reproduced as
  printed, and labelled.
