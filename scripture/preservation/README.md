# The preservation passages

The passages of Scripture in which a claim is made about God's word enduring,
not passing away, not failing, not being annulled, not being altered, or
being kept; with the passages that show how it was kept and those that admit
its corruption or withdrawal among men.

| File | |
| --- | --- |
| [passages.md](passages.md) | Every passage, with the Hebrew and Greek of the Old Testament or three Greek editions of the New, English translations, and notes. **Generated.** |
| [passages.json](passages.json) | The same data, machine-readable, with every verse of every edition. **Generated.** |
| [passages.yaml](passages.yaml) | The curated input: references, speaker, role, categories, summary of the claim, and notes on the Hebrew and Greek. **Edit this one.** |

The study of these passages, and of the confessions' use of them, is in
[analysis/preservation-of-scripture/](../../analysis/preservation-of-scripture/README.md).
The companion study, on the strength of the claims if grounded in the Hebrew
text or in the Septuagint, is
[analysis/preservation-hebrew-and-greek.md](../../analysis/preservation-hebrew-and-greek.md).

## What is included

A passage is included if it makes a claim, gives a command, or narrates an
event about the endurance, reliability or keeping of God's word. The criteria,
the speaker and role tags, the categories, and the passages considered and
left out are set out in the study's
[Scope and method](../../analysis/preservation-of-scripture/README.md#scope-and-method).

## Editions

All texts are downloaded from [eBible.org](https://ebible.org/) as
verse-per-line files and cached in `.cache/ebible/` (not committed).

| Use | Edition | eBible.org id | License |
| --- | --- | --- | --- |
| Hebrew Old Testament | Westminster Leningrad Codex (Masoretic Text) | `hboWLC` | Public domain |
| Greek Old Testament | Brenton's Septuagint (Greek text, 1844–1851, after the Sixtine edition of Codex Vaticanus) | `grcbrent` | Public domain |
| English of the Greek Old Testament | L. C. L. Brenton, *The Septuagint Version of the Old Testament* (1851) | `eng-Brenton` | Public domain |
| English of the Hebrew Old Testament, and of the New Testament | King James Version, 1769 text | `eng-kjv2006` | Public domain |
| Greek New Testament | Textus Receptus: the majority reading of Stephanus 1550, Elzevir 1624 and Scrivener 1881 | `grctr` | Public domain |
| Greek New Testament | Byzantine text: the 1904 Patriarchal edition | `grcbyz` | Public domain |
| Greek New Testament | *The Greek New Testament: SBL Edition*, ed. Michael W. Holmes (2010) | `grcsbl` | CC BY 4.0 |

Notes on the texts:

- Cantillation marks, and the paragraph markers פ and ס after verses, are
  removed from the Hebrew; vowel points are kept.
- Brenton's Septuagint has its own chapter and verse numbering, which often
  differs from the Hebrew and English (most Psalms are one lower; Jeremiah
  25–51 is arranged differently; Proverbs 30:1–14 is placed in chapter 24).
  The `lxx` field of each passage gives Brenton's reference. Brenton prints
  Ezra and Nehemiah as one book, 2 Esdras (`EZR`), so that Nehemiah 1–13 is
  `EZR` 11–23; and Joshua 8:30–35 stands after 9:2, as 9:2a–f.
- Brenton's Daniel is Theodotion's Greek version, not the Old Greek.
- The SBL edition's text-critical signs (⸀ ⸁ ⸂ ⸃) are removed.
- The eBible.org files differ in where they print the doxology of Romans
  (16:25–27 in the Textus Receptus, 14:24–26 in the Byzantine text); the
  SBL file does not include it, so no passage quotes it.

## Regenerating

```
pip install pyyaml
python3 tools/build_preservation.py            # uses the cache
python3 tools/build_preservation.py --refresh  # downloads the editions again
python3 tools/build_index.py                   # updates INDEX.md
```

`build_preservation.py` writes `passages.md`, `passages.json`, and
[analysis/preservation-of-scripture/confessional-citations.md](../../analysis/preservation-of-scripture/confessional-citations.md),
which lists every place a document in [catalog.yaml](../../catalog.yaml)
marked `scan: true` cites a verse of one of the passages.

## Adding a passage

1. Add an entry to `passages.yaml`, following the field notes at the top of
   that file. Give the reference in English versification in `kjv`, and add
   `mt` or `lxx` where the Hebrew or Brenton's numbering differs.
2. Run the tools above. The tool stops with an error if a category or
   speaker is not one it knows.
3. Update the counts and lists in the study
   ([README.md](../../analysis/preservation-of-scripture/README.md)), and,
   for an Old Testament passage, the comparison in
   [hebrew-and-greek.md](../../analysis/preservation-of-scripture/hebrew-and-greek.md).
4. If a confession cites the new passage, it now appears in
   `confessional-citations.md`; reflect it in
   [confessions.md](../../analysis/preservation-of-scripture/confessions.md).
