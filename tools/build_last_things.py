#!/usr/bin/env python3
"""Build the collection of passages on the heavens, the final state, the new
heavens and earth, and the resurrection of the body.

Inputs
  scripture/last-things/passages.yaml   the curated list

Texts
  The eBible.org editions used by tools/build_preservation.py (Masoretic Text,
  Brenton's Septuagint and his English, the KJV, the Textus Receptus, the
  Byzantine text of 1904, the SBL Greek New Testament), cached in .cache/ebible;
  and Swete's Septuagint (public domain) from lxx.confident.faith, cached in
  .cache/swete, with the Göttingen substitutions on that site reversed as in
  tools/build_divine_quotations.py.

Fields of passages.yaml: id, ref (display), kjv (USFM reference, KJV
numbering), mt / lxx / lxx_en (where the numbering or book code differs),
skip (editions to leave out: mt, kjv, swete), topics, claim, terms (words the
notes rely on, as "edition: word"), mt_lxx, variants, words, notes.

Outputs
  scripture/last-things/passages.md     every passage with its texts and notes
  scripture/last-things/passages.json   the same, machine-readable

Every Hebrew or Greek word that an entry's notes put in its `terms` list must
occur in the text of the edition named with it; the tool stops otherwise.

Usage: python3 tools/build_last_things.py [--refresh]
"""
import argparse
import json
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_preservation import (  # noqa: E402
    BOOK_NAMES, EDITIONS, NT_BOOKS, NT_EDITIONS, OT_EDITIONS, clean, display_ref, expand, fetch_edition,
)
from build_divine_quotations import MARKUP, SWETE_BOOKS, Swete, contains  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "scripture", "last-things", "passages.yaml")
OUT_MD = os.path.join(ROOT, "scripture", "last-things", "passages.md")
OUT_JSON = os.path.join(ROOT, "scripture", "last-things", "passages.json")

TOPICS = {
    "heavens": "The heavens and the “third heaven”",
    "destination": "The final destination of the Christian",
    "new-creation": "The new heavens and the new earth",
    "resurrection": "The resurrection of the body",
}
EDITION_FOR = {"mt": "hboWLC", "lxx": "grcbrent", "tr": "grctr", "byz": "grcbyz", "sbl": "grcsbl"}


def verses(texts, code, refs):
    out = []
    for key in expand(refs):
        text = texts[code].get(key)
        if text is None:
            raise SystemExit(f"{key} not found in {code}")
        out.append({"ref": key, "text": clean(code, MARKUP.sub("", text))})
    return out


def swete_text(swete, lxx_refs, brenton):
    """Swete's text for each run of consecutive verses of the Septuagint reference."""
    runs, prev = [], None
    for v in brenton:
        book, cv = v["ref"].split()
        ch, vn = (int(x) for x in cv.split(":"))
        if prev != (book, ch, vn - 1):
            runs.append(((book, ch), []))
        runs[-1][1].append(v)
        prev = (book, ch, vn)
    out, readings = [], []
    for (book, ch), vs in runs:
        if book not in SWETE_BOOKS:
            return None, []
        target = re.sub(r"([Δδ])ιατοῦτο", r"\1ιὰ τοῦτο", " ".join(v["text"] for v in vs))  # Swete divides the word
        text, rd = swete.span(book, ch, target)
        if not text:
            return None, []
        first, last = vs[0]["ref"], vs[-1]["ref"]
        label = display_ref(first) + ("" if first == last else "–" + last.split(":")[1])
        out.append({"ref": label, "text": text})
        readings += rd
    return out, readings


def build(entries, texts, swete):
    records, errors = [], []
    for e in entries:
        r = dict(e)
        for t in e["topics"]:
            if t not in TOPICS:
                errors.append(f"{e['id']}: bad topic {t}")
        nt = e["kjv"].split()[0] in NT_BOOKS
        r["testament"] = "NT" if nt else "OT"
        r["texts"] = {}
        skip = e.get("skip", [])
        for ed in (NT_EDITIONS if nt else OT_EDITIONS):
            if ed in skip:
                continue
            code = EDITIONS[ed][0]
            refs = e.get(ed) or (e.get("lxx") if ed == "lxx_en" else None) or e["kjv"]
            r["texts"][ed] = verses(texts, code, refs)
        if not nt and "swete" not in skip:
            sw, rd = swete_text(swete, e.get("lxx") or e["kjv"], r["texts"]["lxx"])
            if sw:
                r["texts"]["swete"] = sw
                r["goettingen"] = [{"swete": a, "goettingen": b} for a, b in rd]
        for term in e.get("terms", []):
            ed, word = term.split(":", 1)
            ed, word = ed.strip(), word.strip()
            src = r["texts"].get(ed)
            if src is None:
                errors.append(f"{e['id']}: no {ed} text for term {word}")
                continue
            if not contains(" ".join(v["text"] for v in src), word, hebrew=(ed == "mt")):
                errors.append(f"{e['id']}: {word!r} not in {ed}")
        records.append(r)
    if errors:
        raise SystemExit("\n".join(errors))
    return records


TITLES = dict((k, v[1]) for k, v in EDITIONS.items())
TITLES["swete"] = "Greek (Septuagint, Swete's edition)"
OT_ORDER = ["mt", "kjv", "lxx", "swete", "lxx_en"]


def render(records):
    lines = [
        "# The last things: passages",
        "",
        "The passages of Scripture on which the Reformed, Lutheran and Jewish",
        "teaching about the heavens and the “third heaven”, the final destination",
        "of the Christian, the new heavens and the new earth, and the resurrection",
        "of the body is argued. The study of them is in",
        "[analysis/heaven-and-resurrection/](../../analysis/heaven-and-resurrection/README.md).",
        "",
        "> **Generated** by `tools/build_last_things.py` from",
        "> [passages.yaml](passages.yaml). Edit that file and re-run the tool; do not",
        "> edit this one. The same data is in [passages.json](passages.json).",
        "",
        "For each Old Testament passage the Hebrew (Masoretic Text) is given with the",
        "King James Version, and the Greek (Septuagint) in Brenton's and in Swete's",
        "editions with Brenton's English. Swete's text is taken from",
        "lxx.confident.faith, which in some books prints the Göttingen reading; those",
        "places are put back to Swete's and the Göttingen reading is reported, not",
        "quoted (it is under copyright). For each New Testament passage the Textus",
        "Receptus, the Byzantine text of 1904 and the SBL Greek New Testament are",
        "given with the KJV. Editions and licences are listed in",
        "[SOURCES.md](../../SOURCES.md).",
        "",
        "## Contents",
        "",
    ]
    for t, title in TOPICS.items():
        rs = [r for r in records if r["topics"][0] == t]
        lines.append(f"- **{title}:** " + ", ".join(f"[{r['ref']}](#{r['id']})" for r in rs))
    for t, title in TOPICS.items():
        lines += ["", f"## {title}", ""]
        for r in [r for r in records if r["topics"][0] == t]:
            lines += [f"### {r['ref']}", "", f"<a id=\"{r['id']}\"></a>", ""]
            also = [TOPICS[x] for x in r["topics"][1:]]
            lines.append(f"**Claim.** {r['claim'].strip()}" + (f" *(Also: {'; '.join(also)}.)*" if also else ""))
            lines.append("")
            order = NT_EDITIONS if r["testament"] == "NT" else OT_ORDER
            for ed in order:
                if ed not in r["texts"]:
                    continue
                lines += [f"**{TITLES[ed]}**", ""]
                for v in r["texts"][ed]:
                    text = v["text"]
                    if ed == "mt":
                        text = f"<span dir=\"rtl\" lang=\"he\">{text}</span>"
                    ref = v["ref"] if ed == "swete" else display_ref(v["ref"])
                    lines += [f"> {ref} — {text}", ">"]
                lines.pop()
                lines.append("")
            if r.get("goettingen"):
                g = "; ".join(f"Swete {x['swete']}, Göttingen {x['goettingen']}" for x in r["goettingen"])
                lines += [f"*Swete and Göttingen differ here:* {g}.", ""]
            for key, head in (("mt_lxx", "Hebrew and Greek compared."), ("variants", "The Greek editions compared."),
                              ("words", "The words."), ("notes", "Notes.")):
                if r.get(key):
                    lines += [f"**{head}**", "", r[key].strip(), ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    entries = yaml.safe_load(open(DATA, encoding="utf-8"))["passages"]
    codes = sorted({EDITIONS[e][0] for e in OT_EDITIONS + NT_EDITIONS})
    texts = {c: fetch_edition(c, args.refresh) for c in codes}
    records = build(entries, texts, Swete(args.refresh))
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(render(records))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{len(records)} passages -> {os.path.relpath(OUT_MD, ROOT)}")


if __name__ == "__main__":
    main()
