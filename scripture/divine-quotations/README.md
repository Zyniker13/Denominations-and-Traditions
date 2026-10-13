# Where God quotes Scripture

Every place in Scripture where God himself speaks words of earlier Scripture:
Jesus in the Gospels and in Revelation, the Father's voice from heaven, God
on the throne in Revelation, and in the Old Testament the LORD, in his own
person or by a prophet's "thus says the LORD", repeating an earlier book.

| File | |
| --- | --- |
| [quotations.md](quotations.md) | Every quotation, with the Greek of the SBL edition, the Textus Receptus and the Byzantine text, the Hebrew, Brenton's and Swete's Septuagint, and the readings that decide which text it stands closer to. Opens with the counts. **Generated.** |
| [quotations.json](quotations.json) | The same data, machine-readable, with every verse of every edition and the counts. **Generated.** |
| [quotations.yaml](quotations.yaml) | The curated input: where, who speaks, the source, the formula, the type, the affinity, and the readings with the witnesses that support them. **Edit this one.** |

The study of these quotations is in
[analysis/god-quoting-scripture/](../../analysis/god-quoting-scripture/README.md).
It sets out the criteria, the counts, the analysis of the affinities, and the
passages considered and left out.

## What is included

A New Testament entry is a place where Jesus (before or after the
resurrection), the Father, or God on the throne speaks words that reproduce
the wording of an Old Testament text, whether introduced as Scripture or not.
An Old Testament entry is a place where the LORD speaks words that reproduce
an earlier book. Allusions, appeals to Scripture that quote nothing, and
quotations by human speakers are listed in the study, not here. Each entry
has a type (direct, adapted, paraphrase), and is flagged when it has a
formula, fuses two or more texts, or is borderline. The definitions are at
the top of `quotations.yaml`.

## Editions

The Hebrew, Brenton's Septuagint and the three Greek New Testaments are the
eBible.org files described in
[scripture/preservation/](../preservation/README.md#editions), cached in
`.cache/ebible/`. The Septuagint is also compared with:

| Use | Edition | Where from |
| --- | --- | --- |
| Septuagint, the text of Codex Vaticanus (B), with A in Genesis 1:1–46:28 and ℵ in Psalms 105:27–137:6, where B is lost; in Daniel, the Old Greek | H. B. Swete, *The Old Testament in Greek according to the Septuagint* (Cambridge, 1887–1894) | [lxx.confident.faith](https://lxx.confident.faith/), cached in `.cache/swete/` |
| Readings of A, ℵ, Q, F, Γ and the other uncials | Swete's apparatus | the scanned volumes at archive.org |
| Readings of Aquila, Symmachus and Theodotion | F. Field, *Origenis Hexaplorum quae supersunt* (Oxford, 1875) | the scanned volumes at archive.org |
| Readings of the Göttingen edition | cited from the notes at lxx.confident.faith; not copied | |

Licenses and archive.org identifiers are in [SOURCES.md](../../SOURCES.md).

Notes on the texts:

- Brenton's Daniel is Theodotion's version. Swete prints the Old Greek and
  Theodotion; lxx.confident.faith gives the Old Greek, which the tool
  locates by the `og_find` words of each entry.
- In Genesis and the Psalms lxx.confident.faith prints the Göttingen
  reading where it differs from Swete, and notes Swete's. The tool restores
  Swete's reading from that note, so that the Swete column is Swete's text,
  and lists the Göttingen reading beside it.
- Brenton numbers Jeremiah 25–51 in the Septuagint's order, Joel 3–4 and
  Malachi 3:19–24 by the Hebrew chapters, and Deuteronomy 29 by the English
  verses. The `mt`, `lxx` and `lxx_source` fields give the references where
  they differ from the English. lxx.confident.faith numbers Joel and
  Malachi by the English chapters.
- The Septuagint lacks some passages the Hebrew has (Jeremiah 8:11–12,
  30:10–11, 33:14–26 and 48:45–47 among those used here). Entries that
  depend on them say so.

## Regenerating

```
pip install pyyaml
python3 tools/build_divine_quotations.py            # uses the caches
python3 tools/build_divine_quotations.py --refresh  # downloads the editions again
```

The tool stops with an error if a quotation is not found in its verse, if a
reading given for Brenton, Swete or the Hebrew is not in that text, or if a
speaker, type, affinity or witness is one it does not know.

## Adding a quotation

1. Add an entry to `quotations.yaml`, following the field notes at the top
   of that file. Give the readings that decide the affinity under `points`,
   with the witnesses the New Testament agrees with there.
2. Run the tool, and correct anything it reports.
3. Update the counts and the lists in the study
   ([README.md](../../analysis/god-quoting-scripture/README.md)).
