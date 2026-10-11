#!/usr/bin/env python3
"""Build the preservation-passage collection and its confessional cross-reference.

Inputs
  scripture/preservation/passages.yaml   the curated passage list
  catalog.yaml                           the confessional documents to scan

Bible texts (all from eBible.org's verse-per-line downloads; see SOURCES.md)
  hboWLC       Westminster Leningrad Codex (Masoretic Text)         public domain
  grcbrent     Brenton's Greek Septuagint                           public domain
  eng-Brenton  Brenton's English translation of the Septuagint      public domain
  eng-kjv2006  King James Version (1769 text)                       public domain
  grctr        Textus Receptus (Stephanus 1550 / Elzevir 1624 /
               Scrivener 1881, majority of the three)               public domain
  grcbyz       1904 Patriarchal (Antoniades) Byzantine text         public domain
  grcsbl       SBL Greek New Testament (2010)                       CC BY 4.0

Outputs
  scripture/preservation/passages.md     every passage with its texts and notes
  scripture/preservation/passages.json   the same, machine-readable
  analysis/preservation-of-scripture/confessional-citations.md
                                         every place a scanned document cites
                                         one of the passages

Downloads are cached in .cache/ebible (git-ignored).

Usage: python3 tools/build_preservation.py [--refresh]
"""
import argparse
import io
import json
import os
import re
import urllib.request
import zipfile

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache", "ebible")
PASSAGES = os.path.join(ROOT, "scripture", "preservation", "passages.yaml")
OUT_MD = os.path.join(ROOT, "scripture", "preservation", "passages.md")
OUT_JSON = os.path.join(ROOT, "scripture", "preservation", "passages.json")
OUT_XREF = os.path.join(ROOT, "analysis", "preservation-of-scripture", "confessional-citations.md")
CATALOG = os.path.join(ROOT, "catalog.yaml")

EDITIONS = {
    "mt": ("hboWLC", "Hebrew (Masoretic Text, Westminster Leningrad Codex)"),
    "lxx": ("grcbrent", "Greek (Septuagint, Brenton's edition)"),
    "lxx_en": ("eng-Brenton", "English of the Greek (Brenton, 1851)"),
    "kjv": ("eng-kjv2006", "English of the Hebrew (KJV, 1769)"),
    "tr": ("grctr", "Greek (Textus Receptus)"),
    "byz": ("grcbyz", "Greek (Byzantine, 1904 Patriarchal text)"),
    "sbl": ("grcsbl", "Greek (SBL Greek New Testament, CC BY 4.0)"),
    "kjv_nt": ("eng-kjv2006", "English (KJV, 1769)"),
}
OT_EDITIONS = ["mt", "kjv", "lxx", "lxx_en"]
NT_EDITIONS = ["tr", "byz", "sbl", "kjv_nt"]

BOOK_NAMES = {
    "GEN": "Genesis", "EXO": "Exodus", "LEV": "Leviticus", "NUM": "Numbers", "DEU": "Deuteronomy",
    "JOS": "Joshua", "JDG": "Judges", "RUT": "Ruth", "1SA": "1 Samuel", "2SA": "2 Samuel",
    "1KI": "1 Kings", "2KI": "2 Kings", "1CH": "1 Chronicles", "2CH": "2 Chronicles", "EZR": "Ezra",
    "NEH": "Nehemiah", "EST": "Esther", "JOB": "Job", "PSA": "Psalm", "PRO": "Proverbs",
    "ECC": "Ecclesiastes", "SOL": "Song of Songs", "ISA": "Isaiah", "JER": "Jeremiah",
    "LAM": "Lamentations", "EZE": "Ezekiel", "DAN": "Daniel", "DNG": "Daniel (Greek)", "HOS": "Hosea",
    "JOE": "Joel", "AMO": "Amos", "OBA": "Obadiah", "JON": "Jonah", "MIC": "Micah", "NAH": "Nahum",
    "HAB": "Habakkuk", "ZEP": "Zephaniah", "HAG": "Haggai", "ZEC": "Zechariah", "MAL": "Malachi",
    "MAT": "Matthew", "MAR": "Mark", "LUK": "Luke", "JOH": "John", "ACT": "Acts", "ROM": "Romans",
    "1CO": "1 Corinthians", "2CO": "2 Corinthians", "GAL": "Galatians", "EPH": "Ephesians",
    "PHI": "Philippians", "PHP": "Philippians", "COL": "Colossians", "1TH": "1 Thessalonians",
    "2TH": "2 Thessalonians", "1TI": "1 Timothy", "2TI": "2 Timothy", "TIT": "Titus",
    "PHM": "Philemon", "HEB": "Hebrews", "JAM": "James", "1PE": "1 Peter", "2PE": "2 Peter",
    "1JO": "1 John", "2JO": "2 John", "3JO": "3 John", "JUD": "Jude", "REV": "Revelation",
}
NT_BOOKS = {"MAT", "MAR", "LUK", "JOH", "ACT", "ROM", "1CO", "2CO", "GAL", "EPH", "PHI", "PHP",
            "COL", "1TH", "2TH", "1TI", "2TI", "TIT", "PHM", "HEB", "JAM", "1PE", "2PE", "1JO",
            "2JO", "3JO", "JUD", "REV"}

# How the confessions abbreviate books, mapped to the USFM codes above.
CITATION_BOOKS = {
    "gen": "GEN", "genesis": "GEN", "ex": "EXO", "exod": "EXO", "exodus": "EXO", "lev": "LEV",
    "leviticus": "LEV", "num": "NUM", "numbers": "NUM", "deut": "DEU", "deuteronomy": "DEU",
    "josh": "JOS", "joshua": "JOS", "judg": "JDG", "judges": "JDG", "ruth": "RUT",
    "1 sam": "1SA", "2 sam": "2SA", "1 kgs": "1KI", "2 kgs": "2KI", "1 kings": "1KI", "2 kings": "2KI",
    "1 chr": "1CH", "2 chr": "2CH", "ezra": "EZR", "neh": "NEH", "nehemiah": "NEH", "esth": "EST",
    "job": "JOB", "ps": "PSA", "psa": "PSA", "psalm": "PSA", "psalms": "PSA", "prov": "PRO",
    "proverbs": "PRO", "eccl": "ECC", "eccles": "ECC", "song": "SOL", "isa": "ISA", "is": "ISA",
    "isaiah": "ISA", "jer": "JER", "jeremiah": "JER", "lam": "LAM", "ezek": "EZE", "ezekiel": "EZE",
    "dan": "DAN", "daniel": "DAN", "hos": "HOS", "hosea": "HOS", "joel": "JOE", "amos": "AMO",
    "obad": "OBA", "jonah": "JON", "mic": "MIC", "micah": "MIC", "nah": "NAH", "hab": "HAB",
    "zeph": "ZEP", "hag": "HAG", "zech": "ZEC", "zechariah": "ZEC", "mal": "MAL", "malachi": "MAL",
    "matt": "MAT", "matthew": "MAT", "mark": "MAR", "luke": "LUK", "john": "JOH", "acts": "ACT",
    "rom": "ROM", "romans": "ROM", "1 cor": "1CO", "2 cor": "2CO", "1 corinthians": "1CO",
    "2 corinthians": "2CO", "gal": "GAL", "galatians": "GAL", "eph": "EPH", "ephesians": "EPH",
    "phil": "PHI", "philippians": "PHI", "col": "COL", "colossians": "COL", "1 thess": "1TH",
    "2 thess": "2TH", "2 thessalonians": "2TH", "1 tim": "1TI", "2 tim": "2TI", "1 timothy": "1TI",
    "2 timothy": "2TI", "titus": "TIT", "phlm": "PHM", "heb": "HEB", "hebrews": "HEB", "jas": "JAM",
    "james": "JAM", "1 pet": "1PE", "2 pet": "2PE", "1 peter": "1PE", "2 peter": "2PE",
    "1 john": "1JO", "2 john": "2JO", "3 john": "3JO", "jude": "JUD", "rev": "REV",
    "revelation": "REV",
}

CATEGORY_TITLES = {
    "permanence": "Permanence",
    "fulfilment": "Fulfilment",
    "inviolability": "Inviolability",
    "purity": "Purity and truth",
    "transmission": "Transmission to later generations",
    "no-alteration": "Prohibition of alteration",
    "inscripturation": "Inscripturation",
    "custody": "Custody",
    "restoration": "Restoration after loss",
    "corruption": "Corruption among men",
    "withdrawal": "Withdrawal",
    "efficacy": "Efficacy",
    "exaltation": "Exaltation",
    "origin": "Origin",
}
SPEAKER_TITLES = {
    "god": "God",
    "god-through-prophet": "God, through a prophet",
    "jesus": "Jesus",
    "mediator": "Moses or a prophet, for God",
    "psalmist": "Psalmist",
    "sage": "Sage",
    "narrator": "Narrator",
    "apostle": "Apostle or evangelist",
    "heavenly-voice": "Heavenly voice",
    "other": "Another speaker",
}

SBL_MARKS = re.compile(r"[⸀-⸏]|‘[^’]*’")
# Hebrew cantillation accents (vowel points are kept), and the open/closed
# paragraph markers פ and ס that follow the end of a verse.
HEBREW_ACCENTS = re.compile(r"[\u0591-\u05AF]")
HEBREW_PARAGRAPH = re.compile(r"(׃)\s*[פס]\s*$")


def fetch_edition(code, refresh):
    path = os.path.join(CACHE, code, f"{code}_vpl.txt")
    if refresh or not os.path.exists(path):
        url = f"https://ebible.org/Scriptures/{code}_vpl.zip"
        print(f"fetching {url}")
        data = urllib.request.urlopen(url, timeout=120).read()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            z.extractall(os.path.join(CACHE, code))
    verses = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(" ", 2)
            if len(parts) == 3:
                verses[f"{parts[0]} {parts[1]}"] = parts[2]
    return verses


def clean(code, text):
    if code == "grcsbl":
        text = SBL_MARKS.sub("", text)
    if code == "hboWLC":
        text = HEBREW_PARAGRAPH.sub(r"\1", HEBREW_ACCENTS.sub("", text))
    return re.sub(r"\s+", " ", text).strip()


def expand(refs):
    """'PSA 12:6-7, DEU 10:2' -> ['PSA 12:6', 'PSA 12:7', 'DEU 10:2']"""
    out = []
    for ref in refs.split(","):
        ref = ref.strip()
        m = re.fullmatch(r"(\w{3}) (\d+):(\d+)-(\d+)", ref)
        if m:
            book, ch, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4))
            out += [f"{book} {ch}:{v}" for v in range(a, b + 1)]
        elif re.fullmatch(r"\w{3} \d+:\d+\w?", ref):
            out.append(ref)
        else:
            raise ValueError(f"bad reference {ref!r}")
    return out


def display_ref(key):
    book, cv = key.split(" ")
    return f"{BOOK_NAMES.get(book, book)} {cv}"


def anchor(text, seen):
    """GitHub's heading anchor."""
    a = text.strip().lower()
    a = re.sub(r"[^\w\- ]", "", a)
    a = a.replace(" ", "-")
    n = seen.get(a, 0)
    seen[a] = n + 1
    return a if n == 0 else f"{a}-{n}"


def build_passages(passages, texts):
    records = []
    for p in passages:
        nt = p["kjv"].split()[0] in NT_BOOKS
        rec = {k: p[k] for k in p}
        rec["testament"] = "NT" if nt else "OT"
        rec["texts"] = {}
        for ed in (NT_EDITIONS if nt else OT_EDITIONS):
            code, _ = EDITIONS[ed]
            field = {"mt": "mt", "lxx": "lxx", "lxx_en": "lxx"}.get(ed, "kjv")
            refs = expand(p.get(field) or p["kjv"])
            verses = []
            for key in refs:
                text = texts[code].get(key)
                if text is None:
                    raise SystemExit(f"{p['id']}: {key} not found in {code}")
                verses.append({"ref": key, "text": clean(code, text)})
            rec["texts"][ed] = verses
        records.append(rec)
    return records


def render_passages(records):
    lines = [
        "# The preservation passages",
        "",
        "Every passage of Scripture in which a claim is made about God's Word",
        "enduring, not passing away, not failing, being kept, or not being altered;",
        "with the passages that describe how it was kept, and those that admit its",
        "corruption or withdrawal among men. The study of them is in",
        "[analysis/preservation-of-scripture/](../../analysis/preservation-of-scripture/README.md).",
        "",
        "> **Generated** by `tools/build_preservation.py` from",
        "> [passages.yaml](passages.yaml). Edit that file and re-run the tool; do not",
        "> edit this one. The same data, with every verse, is in",
        "> [passages.json](passages.json).",
        "",
        "For each Old Testament passage the Hebrew (Masoretic Text) and the Greek",
        "(Septuagint) are always given, each with an English translation made from",
        "it: the King James Version for the Hebrew and Brenton's translation for the",
        "Greek. For each New Testament passage three Greek editions are given: the",
        "Textus Receptus, the Byzantine text of 1904, and the SBL Greek New Testament",
        "(a modern critical text). The editions and their licenses are listed in",
        "[README.md](README.md#editions) and [SOURCES.md](../../SOURCES.md).",
        "",
        "The Septuagint is cited by Brenton's chapter and verse, which often differ",
        "from the Hebrew (most Psalms are one lower; Jeremiah 25–51 is arranged",
        "differently). The Hebrew is cited by its own numbering, which sometimes",
        "differs from the English (the Psalm titles are counted as verses).",
        "",
        "## Contents",
        "",
        "| Passage | Speaker | Role | Categories |",
        "| --- | --- | --- | --- |",
    ]
    for r in records:
        cats = ", ".join(CATEGORY_TITLES[c] for c in r["categories"])
        lines.append(f"| [{r['ref']}](#{r['id']}) | {SPEAKER_TITLES[r['speaker']]} | {r['role']} | {cats} |")
    lines.append("")
    current = None
    for r in records:
        if r["testament"] != current:
            current = r["testament"]
            lines += ["", "## Old Testament" if current == "OT" else "## New Testament", ""]
        lines += [f"### {r['ref']}", "", f"<a id=\"{r['id']}\"></a>", ""]
        lines.append(f"**Claim.** {r['claim']}")
        lines.append("")
        cats = ", ".join(CATEGORY_TITLES[c] for c in r["categories"])
        lines.append(f"**Speaker:** {SPEAKER_TITLES[r['speaker']]} · **Role:** {r['role']} · "
                     f"**Categories:** {cats} · **Object:** {r['object']}")
        lines.append("")
        order = NT_EDITIONS if r["testament"] == "NT" else OT_EDITIONS
        for ed in order:
            lines.append(f"**{EDITIONS[ed][1]}**")
            lines.append("")
            for v in r["texts"][ed]:
                text = v["text"]
                if ed == "mt":
                    text = f"<span dir=\"rtl\" lang=\"he\">{text}</span>"
                lines.append(f"> {display_ref(v['ref'])} — {text}")
                lines.append(">")
            lines.pop()
            lines.append("")
        if r.get("mt_lxx"):
            lines += ["**Hebrew and Greek compared.**", "", r["mt_lxx"].strip(), ""]
        if r.get("variants"):
            lines += ["**The Greek editions compared.**", "", r["variants"].strip(), ""]
        if r.get("nt_use"):
            uses = ", ".join(display_ref_range(u) for u in r["nt_use"])
            lines += [f"**Used in the New Testament:** {uses}", ""]
        if r.get("notes"):
            lines += ["**Notes.**", "", r["notes"].strip(), ""]
    return "\n".join(lines).rstrip() + "\n"


def display_ref_range(ref):
    book, cv = ref.split(" ")
    return f"{BOOK_NAMES.get(book, book)} {cv}"


# ---------------------------------------------------------------- citations

CITE = re.compile(
    r"(?P<book>(?:[123] )?[A-Z][a-z]+)\.? (?P<ch>\d+)(?::|, ?)(?P<v1>\d+)(?:\s?[–-]\s?(?P<v2>\d+))?"
    r"|(?<=; )(?P<ch2>\d+):(?P<v3>\d+)(?:[–-](?P<v4>\d+))?"
)
PARA = re.compile(r"^\*\*(\d+)\.\*\*|<sup>(\d+)</sup>")


def passage_ranges(records):
    """[(id, book, chapter, first verse, last verse)] in English versification."""
    out = []
    for r in records:
        for key in expand(r["kjv"]):
            book, cv = key.split(" ")
            ch, v = cv.split(":")
            out.append((r["id"], book, int(ch), int(re.match(r"\d+", v).group()), r["ref"]))
    return out


def scan_document(doc, ranges):
    hits = []
    path = os.path.join(ROOT, doc["path"])
    seen = {}
    heading, slug, para = None, None, None
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^(#{1,6}) (.*)", line)
            if m:
                heading = m.group(2).strip()
                slug = anchor(heading, seen)
                para = None
                continue
            marks = [(pm.start(), pm.group(1) or pm.group(2)) for pm in PARA.finditer(line)]
            line_start_para = para
            if marks:
                para = marks[-1][1]
            last_book = None
            for cm in CITE.finditer(line):
                # the paragraph is the last number before the citation on this line
                here = [n for pos, n in marks if pos < cm.start()]
                cite_para = here[-1] if here else line_start_para
                if cm.group("book"):
                    name = cm.group("book").lower()
                    book = CITATION_BOOKS.get(name)
                    if not book:
                        last_book = None
                        continue
                    ch, v1, v2 = int(cm.group("ch")), int(cm.group("v1")), cm.group("v2")
                    last_book = book
                else:
                    if not last_book:
                        continue
                    book = last_book
                    ch, v1, v2 = int(cm.group("ch2")), int(cm.group("v3")), cm.group("v4")
                v2 = int(v2) if v2 else v1
                if v2 < v1:
                    v2 = v1
                for pid, pbook, pch, pv, pref in ranges:
                    if pbook == book and pch == ch and v1 <= pv <= v2:
                        cited = cm.group(0).strip()
                        hits.append({
                            "passage": pid, "passage_ref": pref, "document": doc["id"],
                            "heading": heading, "anchor": slug, "paragraph": cite_para,
                            "cited": cited,
                        })
    # one row per passage per location
    unique = {}
    for h in hits:
        unique.setdefault((h["passage"], h["anchor"], h["paragraph"]), h)
    return list(unique.values())


def render_citations(records, catalog, hits):
    docs = {d["id"]: d for d in catalog["documents"]}
    scanned = [d for d in catalog["documents"] if d.get("scan") and d.get("path")]
    by_passage = {}
    for h in hits:
        by_passage.setdefault(h["passage"], []).append(h)
    lines = [
        "# Where the confessions cite the preservation passages",
        "",
        "> **Generated** by `tools/build_preservation.py`. Do not edit by hand. It",
        "> lists every place where a document in [catalog.yaml](../../catalog.yaml)",
        "> marked `scan: true` cites a verse of one of the",
        "> [preservation passages](../../scripture/preservation/passages.md), whether",
        "> as a Scripture proof or in its running text. A citation counts when its",
        "> verse range overlaps the passage's. The study that interprets these",
        "> citations is [confessions.md](confessions.md).",
        "",
        "A citation is evidence that a document uses a passage, not of what it uses",
        "it for: Psalm 119:105, for instance, is cited for the sufficiency of",
        "Scripture, not its preservation. Passages not cited by any document are",
        "listed at the end.",
        "",
        f"Documents scanned: {len(scanned)}. Passages: {len(records)}.",
        "",
        "## By passage",
        "",
    ]
    for r in records:
        rows = by_passage.get(r["id"])
        if not rows:
            continue
        lines += [f"### {r['ref']}", "", "| Document | Place | Cited as |", "| --- | --- | --- |"]
        for h in sorted(rows, key=lambda h: [d["id"] for d in catalog["documents"]].index(h["document"])):
            d = docs[h["document"]]
            place = h["heading"] or ""
            if h["paragraph"]:
                place = f"{place}, ¶ {h['paragraph']}" if place else f"¶ {h['paragraph']}"
            link = f"../../{d['path']}" + (f"#{h['anchor']}" if h["anchor"] else "")
            lines.append(f"| {d['title']} | [{place}]({link}) | {h['cited']} |")
        lines.append("")
    lines += ["## By document", "", "| Document | Passages cited |", "| --- | --- |"]
    for d in scanned:
        ps = []
        for r in records:
            if any(h["document"] == d["id"] and h["passage"] == r["id"] for h in hits):
                ps.append(r["ref"])
        lines.append(f"| [{d['title']}](../../{d['path']}) | {'; '.join(ps) if ps else '—'} |")
    lines += ["", "## Passages no scanned document cites", ""]
    for r in records:
        if r["id"] not in by_passage:
            lines.append(f"- [{r['ref']}](../../scripture/preservation/passages.md#{r['id']})")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download the Bible texts")
    args = ap.parse_args()

    with open(PASSAGES, encoding="utf-8") as f:
        passages = yaml.safe_load(f)["passages"]
    ids = [p["id"] for p in passages]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit(f"duplicate ids: {sorted(dupes)}")
    for p in passages:
        bad = [c for c in p["categories"] if c not in CATEGORY_TITLES]
        if bad or p["speaker"] not in SPEAKER_TITLES:
            raise SystemExit(f"{p['id']}: unknown category or speaker {bad or p['speaker']}")

    codes = sorted({code for code, _ in EDITIONS.values()})
    texts = {code: fetch_edition(code, args.refresh) for code in codes}
    records = build_passages(passages, texts)

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(render_passages(records))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({
            "generated_by": "tools/build_preservation.py",
            "editions": {k: {"code": v[0], "title": v[1]} for k, v in EDITIONS.items()},
            "categories": CATEGORY_TITLES,
            "speakers": SPEAKER_TITLES,
            "passages": records,
        }, f, ensure_ascii=False, indent=1)
        f.write("\n")

    with open(CATALOG, encoding="utf-8") as f:
        catalog = yaml.safe_load(f)
    ranges = passage_ranges(records)
    hits = []
    for doc in catalog["documents"]:
        if doc.get("scan") and doc.get("path"):
            hits += scan_document(doc, ranges)
    os.makedirs(os.path.dirname(OUT_XREF), exist_ok=True)
    with open(OUT_XREF, "w", encoding="utf-8") as f:
        f.write(render_citations(records, catalog, hits))
    print(f"{len(records)} passages; {len(hits)} confessional citations")


if __name__ == "__main__":
    main()
