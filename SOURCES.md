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

### Added for the study of the last things

The files below were added for
[analysis/heaven-and-resurrection/](analysis/heaven-and-resurrection/README.md)
and fetched 2026-10-23. Each file's opening table gives the details, as
above. Two further methods were used:

- **Keyed texts of the Text Creation Partnership** (EEBO-TCP and Evans-TCP),
  released by the TCP into the public domain (CC0), were rendered from the TEI
  XML at `github.com/textcreationpartnership/<id>`. The keyers' conventions,
  and the printers' spelling and punctuation, are kept.
- **Hebrew and Aramaic** printed beside the rabbinic and Maimonidean texts
  were fetched by the Sefaria API (v3) and are used only where the edition is
  public domain or openly licensed, as listed. They are not part of the
  English editions and are marked off from them.

| Files | Edition | Source | Public domain or license |
| --- | --- | --- | --- |
| `jewish-antiquity/second-temple-on-heaven-and-resurrection.md` | *Ante-Nicene Fathers* VIII (1886): Testament of Levi, tr. Sinker; *Apocalypse of Moses*, tr. Walker. *The Book of the Secrets of Enoch*, tr. Morfill, ed. Charles (Clarendon, 1896). *The Apocalypse of Baruch*, tr. Charles (Black, 1896). *The Book of Enoch*, tr. Charles (SPCK, 1917). Josephus, tr. Whiston | CCEL `anf08`; archive.org `bookofsecretsofe00morf`, `theapocalypseofb00charuoft`; Wikisource, *The Book of Enoch (Charles)*; Project Gutenberg #2848–2850 | 1737–1917 |
| `rabbinic/mishnah-and-talmud-on-the-world-to-come.md` | Rodkinson, *New Edition of the Babylonian Talmud*, Sanhedrin (Boston, 1918); Streane, *Chagigah* (Cambridge, 1891); Cohen, *Berakot* (Cambridge, 1921) | archive.org `neweditionofbaby191816rodk` (collated with `neweditionbabyl17taubgoog`), `translationoftre00streuoft`, `babyloniantalmud00coheuoft` | 1891–1921 |
| the same, Hebrew and Aramaic | The Vilna Mishnah (Romm, 1913); the Babylonian Talmud as transcribed on Hebrew Wikisource | Sefaria API | Public domain; CC BY-SA 3.0 (attribution: Hebrew Wikisource contributors, via Sefaria) |
| `rabbinic/midrash-and-prayer-book-on-the-resurrection.md` | Friedlander, *Pirkê de Rabbi Eliezer* (London, 1916); Singer, *The Authorised Daily Prayer Book* (London, 1904); *The Sefaria Midrash Rabbah* (2022) for *Bereshit Rabbah* 28:3 | Sefaria's digitization of archive.org `pirkderabbieli00frieuoft`, checked against the scan; archive.org `authoriseddailyp00sing`; Sefaria API | 1904–1916; *Sefaria Midrash Rabbah*, CC BY (attribution: Sefaria) |
| the same, Hebrew | *Bereshit Rabbah* as transcribed on Hebrew Wikisource; *The Metsudah Siddur* (New York, 1981) | Sefaria API | CC BY-SA 3.0; CC BY |
| `jewish-medieval/maimonides/` | Abelson, "Maimonides on the Jewish Creed", *Jewish Quarterly Review* 19 (1906); Glazer, *Mishnah Torah* I (New York, 1927), with the Raavad's criticisms; Soloweyczik, *Yad-Hachazakah* (London, 1863); Friedländer, *The Guide for the Perplexed*, 2nd ed. (Routledge, 1904) | archive.org `sim_jewish-quarterly-review_1906-10_19`; Sefaria's digitizations of Glazer and Friedländer, checked against archive.org `boofofmishnahtor0001maim` and `guideforperplexe00maimiala`; Sefaria API (Soloweyczik) | 1863–1927 (Glazer: published 1927, in the public domain in the United States) |
| the same, Hebrew | The commentary on the Mishnah in Hebrew translation (Vilna Talmud, Romm); the *Mishneh Torah* and the Raavad in the Torat Emet edition | Sefaria API | Public domain |
| `jewish-modern/` | The Philadelphia (1869) and Pittsburgh (1885) principles, and the article "Resurrection", in *The Jewish Encyclopedia* (Funk & Wagnalls, 1901–1906); Kohler, *Jewish Theology* (Macmillan, 1918) | jewishencyclopedia.com, articles 4592 and 12697; archive.org `jewishtheologysy01kohl` | 1903–1918 |
| `lutheran/heinrich-schmid/doctrinal-theology-last-things.md` | Schmid, *Doctrinal Theology*, tr. Hay and Jacobs, 4th ed. (1899) | archive.org `doctrinaltheolog00schmuoft`, `doctrinaltheolog0000hein_o8t5` | 1899 |
| `reformed/continental/calvin/institutes-book-3-chapter-25.md`, `commentaries-on-the-last-things.md` | Calvin Translation Society: *Institutes* II, tr. Beveridge (1845); commentaries on Isaiah IV (Pringle, 1853), Romans (Owen, 1849), Corinthians II (Pringle, 1849), Philippians (Pringle, 1851), the Catholic Epistles (Owen, 1855) | archive.org scans named in each file, collated with CCEL | 1845–1855 |
| `reformed/continental/calvin/sermon-on-job-19-26-29.md` | *Sermons … vpon the Booke of Iob*, tr. Golding (London, 1574) | EEBO-TCP A69056 | 1574; TCP text CC0 |
| `reformed/continental/bullinger/decades-decade-1-sermon-9-…` | *Fiftie godlie and learned sermons* (London, 1577) | EEBO-TCP A17183 | 1577; CC0 |
| `reformed/continental/ames/marrow-of-sacred-divinity-exaltation-…` | *The Marrow of Sacred Divinity* (London, 1642) | EEBO-TCP A25291 | 1642; CC0 |
| `reformed/continental/wollebius/abridgment-of-christian-divinity-last-things.md` | *The Abridgment of Christian Divinitie*, tr. Ross (London, 1660) | EEBO-TCP A66823 | 1660; CC0 |
| `reformed/british/perkins/` | *An Exposition of the Symbole or Creed of the Apostles* (Cambridge, 1595) | EEBO-TCP A09411 | 1595; CC0 |
| `reformed/british/ussher/` | *A Body of Divinitie* (London, 1645) | EEBO-TCP A64622 | 1645; CC0 |
| `reformed/british/owen/shaking-and-translating-of-heaven-and-earth.md` | *The Shaking and Translating of Heaven and Earth* (London, 1649) | EEBO-TCP A53716 | 1649; CC0 |
| `reformed/british/goodwin/` | *The World to Come* (London, 1655) | EEBO-TCP A85442 | 1655; CC0 |
| `reformed/british/vincent/` | *An Explicatory Catechism* (London, 1675) | EEBO-TCP A64986 | 1675; CC0 |
| `reformed/british/dickson/` | *Truths Victory over Error*, tr. Sinclair (Edinburgh, 1684) | EEBO-TCP A35959 | 1684; CC0 |
| `reformed/british/poole/` | *Annotations upon the Holy Bible* II (London, 1685) | EEBO-TCP A55368 | 1685; CC0 |
| `reformed/british/watson/` | *A Body of Practical Divinity* (London, 1692) | EEBO-TCP A65285 | 1692; CC0 |
| `reformed/british/boston/` | *Human Nature in its Fourfold State* (American printing, 1787) | Evans-TCP N34404 | 1787; CC0 |
| `reformed/american/edwards/` | *True Saints … Present with the Lord* (Boston, 1747); *A History of the Work of Redemption* (Boston reprint, 1782) | Evans-TCP N04758, N13864 | 1747; 1782; CC0 |
| `reformed/princeton/hodge/systematic-theology-vol-3-last-things.md` | *Systematic Theology* III (Scribner, 1872) | CCEL `hodge/theology3`, checked against archive.org `systematictheolo03hodguoft` | 1872 |

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
- **Modern translations of the Jewish texts.** The Soncino Talmud and
  Midrash, Danby's Mishnah, the Koren Steinsaltz Talmud (the William Davidson
  edition, CC BY-NC), Rosner's translation of Maimonides' *Treatise on the
  Resurrection*, Chavel's Nachmanides and Rosenblatt's Saadia are under
  copyright or licensed only for non-commercial use, and are not quoted.
  Sefaria texts are used only where their license is CC BY or CC BY-SA, or
  the text is public domain.
- **Summaries in place of texts.** The *Nicene and Post-Nicene Fathers* gives
  only editorial summaries of several of Jerome's prefaces, and omits part of
  his *Apology* (II.26–32); those summaries and notes are reproduced as
  printed, and labelled.

## Biblical texts (`scripture/` and `analysis/`)

The collection in [scripture/preservation/](scripture/preservation/README.md)
prints its passages in full from the editions below, and the studies in
`analysis/` quote them for comment. All are downloaded from eBible.org's
verse-per-line files by `tools/build_preservation.py`.

| Text | Edition | Source | License |
| --- | --- | --- | --- |
| Hebrew Old Testament | Westminster Leningrad Codex (transcription of the Leningrad Codex, 1008/1009) | eBible.org, `hboWLC` | Public domain |
| Greek Old Testament (Septuagint) | Greek text of L. C. L. Brenton, *The Septuagint Version of the Old Testament* (London: Bagster, 1844–1851), after the Sixtine edition of Codex Vaticanus | eBible.org, `grcbrent` | Public domain |
| English of the Septuagint | L. C. L. Brenton, *The Septuagint Version of the Old Testament* (London: Bagster, 1851) | eBible.org, `eng-Brenton` | Public domain |
| English Bible | King James Version, 1769 Oxford text | eBible.org, `eng-kjv2006` | Public domain |
| Greek New Testament (Textus Receptus) | The majority reading of Stephanus 1550, Elzevir 1624 and Scrivener 1881 | eBible.org, `grctr` | Public domain |
| Greek New Testament (Byzantine) | The 1904 Patriarchal (Antoniades) edition | eBible.org, `grcbyz` | Public domain |
| Greek New Testament (critical) | *The Greek New Testament: SBL Edition*, ed. Michael W. Holmes (Society of Biblical Literature and Logos Bible Software, 2010) | eBible.org, `grcsbl` | CC BY 4.0 |

The SBL Greek New Testament is used under the Creative Commons Attribution
4.0 license: *The Greek New Testament: SBL Edition*, copyright 2010 Society of
Biblical Literature and Logos Bible Software, http://www.sblgnt.com. In
[passages.md](scripture/preservation/passages.md) and
[passages.json](scripture/preservation/passages.json) its text-critical signs
are removed; the words are unchanged. The Hebrew is printed without
cantillation marks.

The collection in [scripture/divine-quotations/](scripture/divine-quotations/README.md)
uses the same editions, downloaded by `tools/build_divine_quotations.py`, and
compares them with the following.

| Text | Edition | Source | License |
| --- | --- | --- | --- |
| Septuagint (Swete) | H. B. Swete, *The Old Testament in Greek according to the Septuagint*, 3 vols. (Cambridge University Press, 1887–1894; later editions to 1909–1912). Its text is Codex Vaticanus (B), with Alexandrinus (A) in Genesis 1:1–46:28 and Sinaiticus (ℵ) in Psalms 105:27–137:6, where B is lost; in Daniel it prints both the Old Greek and Theodotion | Transcription at [lxx.confident.faith](https://lxx.confident.faith/), fetched page by page and cached in `.cache/swete/` (not committed) | Public domain |
| Swete's apparatus | The critical notes of the same edition, giving the readings of A, ℵ, Q, F, Γ and the other uncials | Scans and OCR text at archive.org: `oldtestamentingr0001henr` (vol. 1), `oldtestamenting02swet` (vol. 2), `oldtestamentingr0003henr` (vol. 3) | Public domain |
| Aquila, Symmachus and Theodotion | F. Field, *Origenis Hexaplorum quae supersunt*, 2 vols. (Oxford: Clarendon, 1875) | Scans and OCR text at archive.org: `origenishexaplor01origuoft`, `origenishexaplor02origuoft` | Public domain |
| Göttingen Septuagint | *Septuaginta: Vetus Testamentum Graecum auctoritate Academiae Scientiarum Gottingensis editum* | Readings as noted at lxx.confident.faith, where the site's text follows Göttingen (parts of Genesis and the Psalms) | In copyright. Readings are cited, a word or phrase at a time, for comparison; no Göttingen text is copied into the repository. Where the site prints Göttingen's reading, the tool restores Swete's from the site's own note |

Swete's Greek is quoted in
[quotations.md](scripture/divine-quotations/quotations.md) and
[quotations.json](scripture/divine-quotations/quotations.json) a verse at a
time. Readings of the apparatus and of Field are cited, not reproduced in
bulk, and were checked against the scanned pages' OCR text, which is not
committed.

The collection in [scripture/last-things/](scripture/last-things/README.md)
prints its 45 passages from the same editions, with Swete's Septuagint beside
Brenton's, built by `tools/build_last_things.py` from the same caches.

Translations of passages in the analyses, where not from the KJV or Brenton,
are the analyses' own, and are printed in italics rather than quoted. In the
earlier studies, passages of the Talmud are paraphrased and cited by folio;
the study of the last things quotes them from the public-domain translations
in `theologians/rabbinic/`.
