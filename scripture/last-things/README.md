# The last things: passages

The passages of Scripture on which the teaching about the heavens and the
"third heaven", the final destination of the Christian, the new heavens and
the new earth, and the resurrection of the body is argued: by the Reformed
writers, by the Lutheran dogmaticians who differ from them, and, for the Old
Testament passages, by the Jewish writers collected in
[theologians/](../../theologians/README.md).

| File | |
| --- | --- |
| [passages.md](passages.md) | Every passage, with the Hebrew and Greek of the Old Testament or three Greek editions of the New, the English, and notes on the words and on how the passage is used. **Generated.** |
| [passages.json](passages.json) | The same data, machine-readable, with every verse of every edition. **Generated.** |
| [passages.yaml](passages.yaml) | The curated input: references, topics, the claim, the words the notes rely on, and the notes. **Edit this one.** |

The study of these passages, and of the Reformed, Lutheran and Jewish
teaching built on them, is in
[analysis/heaven-and-resurrection/](../../analysis/heaven-and-resurrection/README.md).

## What is included

Forty-five passages, under four topics: the heavens and the "third heaven"
(9), the final destination of the Christian (10), the new heavens and the new
earth (13), and the resurrection of the body (13). A passage is listed under
its first topic, and the others it bears on are named with it. They are the
passages that the confessions and the theologians in this repository cite on
these questions, with the Old Testament texts the New Testament ones take up,
and 2 Maccabees 7, which is not in the Hebrew canon or the canon of the
Reformed and Lutheran confessions but is cited by the Jewish and Christian
writers as the plainest pre-Christian statement of the resurrection of the
body.

## Editions

The Hebrew, Brenton's Septuagint, the KJV and the three Greek New Testaments
are the eBible.org files described in
[scripture/preservation/](../preservation/README.md#editions), cached in
`.cache/ebible/`. Swete's Septuagint is taken from
[lxx.confident.faith](https://lxx.confident.faith/), cached in
`.cache/swete/`, as in
[scripture/divine-quotations/](../divine-quotations/README.md#editions):
where that site prints the Göttingen reading, the tool restores Swete's from
the site's note and reports the Göttingen reading without quoting the text.

Notes on the texts:

- Brenton numbers most Psalms one lower than the Hebrew and English, and
  prints Nehemiah as 2 Esdras 11–23 (Nehemiah 9:6 is `EZR 19:6`). The `mt`,
  `lxx` and `lxx_en` fields give the references where they differ.
- Brenton's Daniel is Theodotion's. lxx.confident.faith gives only the Old
  Greek of Daniel, so Swete's text is not given for Daniel 12.
- 2 Maccabees was written in Greek; it has no Hebrew, and the KJV of this
  repository has no Apocrypha. Swete's text is not given for it.
- Every Hebrew or Greek word or phrase on which a note relies is listed in
  the entry's `terms`, and the tool checks that it is in the edition named.

## Regenerating

```
pip install pyyaml
python3 tools/build_last_things.py            # uses the caches
python3 tools/build_last_things.py --refresh  # downloads the editions again
```

The tool stops with an error if a reference is not in an edition, if a topic
is one it does not know, or if a word listed in `terms` is not in the edition
named with it.
