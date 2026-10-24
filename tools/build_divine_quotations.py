#!/usr/bin/env python3
"""Build the collection of places where God quotes Scripture.

Inputs
  scripture/divine-quotations/quotations.yaml   the curated list

Texts
  The eBible.org editions used by tools/build_preservation.py (Masoretic Text,
  Brenton's Septuagint, Textus Receptus, Byzantine 1904, SBL Greek New
  Testament), cached in .cache/ebible.

  Swete's Septuagint (Cambridge, 1887-1894; public domain), taken from
  lxx.confident.faith and cached in .cache/swete. In Genesis and the Psalms
  that site prints the Göttingen reading where the two editions differ and
  lists each difference ("Swete ἔχει X · followed Y"). The tool reverses those
  substitutions inside each quoted span, so the text shown is Swete's, and
  reports the Göttingen readings it reversed as citations only. In Daniel the
  site prints the Old Greek, which Swete gives beside Theodotion; Brenton's
  Daniel is Theodotion.

Outputs
  scripture/divine-quotations/quotations.md     every entry with its texts
  scripture/divine-quotations/quotations.json   the same, machine-readable

The tool checks every quotation and every recorded reading against the
texts: a quoted phrase must occur in the New Testament edition it is taken
from, a Septuagint reading in Brenton (or, for a reading of Swete's, in
Swete), and a Hebrew reading in the Masoretic Text. It stops on any
mismatch.

Usage: python3 tools/build_divine_quotations.py [--refresh]
"""
import argparse
import collections
import html
import json
import os
import re
import sys
import unicodedata
import urllib.request

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_preservation import (  # noqa: E402
    BOOK_NAMES, anchor, clean, expand, fetch_edition,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "scripture", "divine-quotations", "quotations.yaml")
OUT_MD = os.path.join(ROOT, "scripture", "divine-quotations", "quotations.md")
OUT_JSON = os.path.join(ROOT, "scripture", "divine-quotations", "quotations.json")
SWETE_CACHE = os.path.join(ROOT, ".cache", "swete")
SWETE_SITE = "https://lxx.confident.faith"

NT_CODES = {"sbl": "grcsbl", "tr": "grctr", "byz": "grcbyz"}
NT_TITLES = {"sbl": "SBL", "tr": "TR", "byz": "Byz"}

# lxx.confident.faith's directory for each book (USFM code as eBible uses it)
SWETE_BOOKS = {
    "GEN": "01.GEN", "EXO": "02.EXD", "LEV": "03.LEV", "NUM": "04.NUM", "DEU": "05.DET",
    "JOS": "06.JSH", "JDG": "07.JDG", "1SA": "09.1SM", "2SA": "10.2SM", "1KI": "11.1KG",
    "2KI": "12.2KG", "1CH": "13.1CH", "2CH": "14.2CH", "PSA": "18.PSL", "PRO": "19.PRV",
    "JOB": "22.JOB", "HOS": "23.HOS", "AMO": "24.AMS", "MIC": "25.MCH", "JOE": "26.JOL",
    "OBA": "27.OBD", "JON": "28.JNH", "NAH": "29.NHM", "HAB": "30.HBK", "ZEP": "31.ZPH",
    "HAG": "32.HAG", "ZEC": "33.ZEC", "MAL": "34.MLC", "ISA": "35.ISA", "JER": "36.JER",
    "LAM": "37.LAM", "EZE": "38.EZK", "DAN": "39.DAN",
}

SPEAKERS = {
    "jesus": "Jesus",
    "jesus-risen": "Jesus, risen and exalted",
    "father": "The Father (voice from heaven)",
    "god": "God (the one on the throne)",
    "god-ot": "The LORD, in his own first person",
    "god-through-prophet": "The LORD, through a prophet's oracle",
    "angel-of-the-lord": "The Angel of the LORD",
}
TYPES = {
    "direct": "Direct quotation",
    "adapted": "Adapted quotation",
    "paraphrase": "Paraphrase or summary",
}
AFFINITIES = {
    "lxx": "Septuagint against the Hebrew",
    "lxx-wording": "Septuagint wording, Hebrew agreeing in sense",
    "other-greek": "Another Greek witness against Brenton and Swete's text",
    "mt": "Hebrew against the Septuagint",
    "mixed": "Mixed (Septuagint at one point, the Hebrew or another witness at another)",
    "independent": "Independent of both",
    "undetermined": "Undetermined (the Septuagint and the Hebrew agree)",
    "semitic": "Given in a Semitic form, with a Greek rendering",
    "varies": "Depends on the edition of the New Testament",
}
OT_GROUPS = {
    "headline": "The LORD quotes an earlier book",
    "torah": "The LORD restates his own earlier words within the Pentateuch",
    "intra-book": "The LORD repeats an oracle within the same book",
    "parallel": "Parallel oracles whose direction cannot be read from the text",
}
GREEK_KEEPS = {
    "yes": "kept",
    "partly": "partly kept",
    "no": "not kept",
    "nolink": "no shared wording in the Hebrew either",
    "absent": "quoting passage not in the Septuagint",
    "source-absent": "earlier passage not in the Septuagint",
}
# lxx.confident.faith numbers Joel and Malachi by the English chapters; Brenton
# (like the Hebrew) has Joel 3-4 and Malachi 3:19-24 for English Joel 2:28-3:21
# and Malachi 4.
def site_chapter(book, ch, verse):
    if book == "JOE":
        return {3: 2, 4: 3}.get(ch, ch)
    if book == "MAL" and ch == 3 and verse >= 19:
        return 4
    return ch


# Sigla used in a reading's `with` list
SIGLA = {
    "lxx": "the Septuagint (Brenton and Swete's text agreeing)",
    "brenton": "Brenton",
    "B": "Codex Vaticanus (Swete's text)",
    "A": "Codex Alexandrinus",
    "S": "Codex Sinaiticus (ℵ)",
    "Q": "Codex Marchalianus",
    "F": "Codex Ambrosianus",
    "OG": "the Old Greek of Daniel",
    "Th": "Theodotion",
    "three": "Aquila, Symmachus and Theodotion",
    "aquila": "Aquila",
    "symmachus": "Symmachus",
    "gottingen": "the Göttingen edition",
    "mt": "the Masoretic Text",
    "none": "no witness",
}


# ---------------------------------------------------------------- text helpers

def norm_token(word):
    w = unicodedata.normalize("NFD", word.lower())
    w = "".join(c for c in w if not unicodedata.combining(c))
    w = w.replace("ς", "σ").replace("ʼ", "").replace("᾽", "").replace("᾿", "").replace("’", "")
    return re.sub(r"[^\w]", "", w)


def tokens(text):
    return [t for t in (norm_token(w) for w in text.split()) if t]


def hebrew_norm(text):
    """Consonants only: points, accents and punctuation removed, final forms normalized."""
    text = re.sub(r"[\u0591-\u05C7]", "", text.replace("־", " ").replace("׀", " "))
    text = text.translate(str.maketrans("ךםןףץ", "כמנפצ"))
    return " ".join(re.sub(r"[^\u05D0-\u05EA]", "", w) for w in text.split() if re.sub(r"[^\u05D0-\u05EA]", "", w))


def contains(text, phrase, hebrew=False):
    """True if every '…'-separated piece of phrase occurs in text, in order."""
    if hebrew:
        hay = " " + hebrew_norm(text) + " "
        pieces = [" " + hebrew_norm(p) + " " for p in phrase.split("…") if p.strip()]
    else:
        hay = " " + " ".join(tokens(text)) + " "
        pieces = [" " + " ".join(tokens(p)) + " " for p in phrase.split("…") if tokens(p)]
    pos = 0
    for p in pieces:
        i = hay.find(p, pos)
        if i < 0:
            return False
        pos = i + len(p) - 1
    return True


def lcs(a, b):
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b):
            cur.append(prev[j] + 1 if x == y else max(prev[j + 1], cur[j]))
        prev = cur
    return prev[-1]


def agreement(quote, text):
    """How many words of the quotation occur, in order, in the text."""
    q = tokens(quote.replace("…", " "))
    return lcs(q, tokens(text)), len(q)


# ---------------------------------------------------------------- Swete

def swete_page(book, ch, kind, refresh):
    """Fetch a chapter page from lxx.confident.faith: kind 00 is the Greek, 02 the notes."""
    d = SWETE_BOOKS[book]
    num, code = d.split(".")
    for cc in (f"{ch:02d}", f"{ch:03d}"):
        fn = f"{num}.{ch:03d}.{kind}-{code}.{cc}.md"
        path = os.path.join(SWETE_CACHE, d, fn)
        if os.path.exists(path) and not refresh:
            return open(path, encoding="utf-8").read()
        try:
            req = urllib.request.Request(f"{SWETE_SITE}/{d}/{fn}", headers={"User-Agent": "curl/8.5.0"})
            data = urllib.request.urlopen(req, timeout=60).read().decode("utf-8")
        except Exception:
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        return data
    return None


class Swete:
    def __init__(self, refresh):
        self.refresh = refresh
        self.chapters = {}

    def chapter(self, book, ch):
        key = (book, ch)
        if key not in self.chapters:
            page = swete_page(book, ch, "00", self.refresh)
            words, notes, source = [], [], None
            if page:
                m = re.search(r'<div class="psalm-reading"[^>]*>(.*?)</div>', page, re.S)
                body = re.sub(r"</?p[^>]*>", "\n", m.group(1)) if m else ""
                for line in re.split(r"<br\s*/?>|\n", body):
                    line = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
                    words += line.split()
                notes_page = swete_page(book, ch, "02", self.refresh) or ""
                text = html.unescape(re.sub(r"<[^>]+>", " ", notes_page))
                s = re.search(r"\*\*Greek source:\*\*([^\n]*)", text)
                source = s.group(1).strip() if s else None
                if source and "differences noted" in source:
                    for line in text.split("\n"):
                        n = re.match(r"\s*- Swete ἔχει (.+?) · followed (.+?)\s*$", line)
                        if n:
                            notes.append((n.group(1).strip(), n.group(2).strip()))
            self.chapters[key] = (words, notes, source)
        return self.chapters[key]

    def span(self, book, ch, target, find=None):
        """Swete's words for the passage whose Brenton text is `target`.

        Returns (text, goettingen_readings) or (None, []) when the chapter
        cannot be had. With `find`, the span is the site's sentence that
        contains those words (used for the Old Greek of Daniel)."""
        words, notes, _ = self.chapter(book, ch)
        if not words:
            return None, []
        norm = [norm_token(w) for w in words]
        if find:
            f = tokens(find)
            for i in range(len(norm) - len(f) + 1):
                if norm[i:i + len(f)] == f:
                    a = i
                    while a > 0 and not re.search(r"[.·;:]$", words[a - 1]):
                        a -= 1
                    b = i + len(f)
                    while b < len(words) and not re.search(r"[.·;:]$", words[b - 1]):
                        b += 1
                    return " ".join(words[a:b]), []
            return None, []
        t = [w for w in tokens(target)]
        tc = collections.Counter(t)
        n = len(t)
        best = (-1.0, 0, 0)
        for length in range(max(1, n - 4), n + 5):
            for i in range(0, max(1, len(norm) - length + 1)):
                c = collections.Counter(norm[i:i + length])
                score = sum((c & tc).values()) - 0.01 * abs(length - n)
                # break ties (the same words at both ends of a verse) by where the span starts and ends
                score += 0.001 * ((norm[i] == t[0]) + (norm[min(i + length, len(norm)) - 1] == t[-1]))
                if score > best[0]:
                    best = (score, i, length)
        _, i, length = best
        text = " ".join(words[i:i + length])
        readings = []
        for swete_has, followed in notes:
            for cand in (followed, followed.rstrip(".")):
                if cand and cand in text:
                    text = text.replace(cand, swete_has.rstrip(".") if cand != followed else swete_has, 1)
                    if tokens(swete_has) != tokens(cand):  # not punctuation only
                        readings.append((swete_has.rstrip("."), cand))
                    break
        return text, readings


# ---------------------------------------------------------------- records

# A few verses of the eBible Hebrew carry leftover markup ('l s="H8085"', 'seg … ')
MARKUP = re.compile(r"'[^'\u0590-\u05FF]*'")


def refs_text(texts, code, refs):
    return " ".join(clean(code, MARKUP.sub("", texts[code][k])) for k in expand(refs) if texts[code].get(k))


def check(cond, msg, errors):
    if not cond:
        errors.append(msg)


def build_nt(entries, texts, swete, errors):
    records = []
    for e in entries:
        r = dict(e)
        eds = e.get("only") or ["sbl", "tr", "byz"]
        r["texts"] = {}
        for ed in ("sbl", "tr", "byz"):
            at = e.get("byz_at", e["at"]) if ed == "byz" else e["at"]
            r["texts"][ed] = refs_text(texts, NT_CODES[ed], at)
        base = eds[0]
        check(r["texts"][base], f"{e['id']}: no {base} text for {e['at']}", errors)
        check(contains(r["texts"][base], e["quote"]), f"{e['id']}: quote not in {base} {e['at']}", errors)
        r["in_editions"] = [ed for ed in ("sbl", "tr", "byz") if contains(r["texts"][ed], e["quote"])]
        mt = e.get("mt") or e["source"]
        lxx = e.get("lxx") or e["source"]
        r["mt_text"] = refs_text(texts, "hboWLC", mt)
        r["lxx_text"] = refs_text(texts, "grcbrent", lxx)
        check(r["mt_text"], f"{e['id']}: no Hebrew for {mt}", errors)
        check(r["lxx_text"] or e.get("lxx_absent"), f"{e['id']}: no Brenton text for {lxx}", errors)
        # Swete, by chapter
        r["swete"] = []
        groups = []  # runs of consecutive verses, each looked up in one chapter page
        for k in expand(lxx):
            book, cv = k.split(" ")
            ch, v = (int(x) for x in cv.split(":"))
            key = (book, site_chapter(book, ch, v))
            last = groups[-1] if groups else None
            if last and last[0] == key and int(last[1][-1].split(":")[1]) == v - 1:
                last[1].append(k)
            else:
                groups.append((key, [k]))
        for (book, ch), keys in groups:
            if book == "DNG":
                for find in e.get("og_find", []):
                    sw, _ = swete.span("DAN", ch, None, find)
                    if sw and not any(x["text"] == sw for x in r["swete"]):
                        r["swete"].append({"ref": f"DAN {ch}", "old_greek": True, "text": sw, "goettingen": []})
                continue
            if book not in SWETE_BOOKS:
                continue
            target = " ".join(clean("grcbrent", texts["grcbrent"].get(k, "")) for k in keys)
            sw, readings = swete.span(book, ch, target)
            if sw:
                ref = keys[0] + (f"-{keys[-1].split(':')[1]}" if len(keys) > 1 else "")
                r["swete"].append({"ref": ref, "old_greek": False, "text": sw, "goettingen": readings})
        for find in e.get("og_find", []):
            check(any(find in s["text"] for s in r["swete"] if s["old_greek"]),
                  f"{e['id']}: Old Greek {find!r} not found", errors)
        swete_all = " ".join(s["text"] for s in r["swete"])
        r["agreement"] = {
            "brenton": agreement(e["quote"], r["lxx_text"]),
            "swete": agreement(e["quote"], swete_all) if swete_all else None,
        }
        for p in e.get("points", []):
            nt_all = " ".join(r["texts"].values())
            check(contains(nt_all, p["nt"]), f"{e['id']}: reading {p['nt']!r} not in the NT text", errors)
            if p.get("lxx") and p["lxx"] != "—":
                check(contains(r["lxx_text"], p["lxx"]), f"{e['id']}: LXX reading {p['lxx']!r} not in Brenton {lxx}", errors)
            if p.get("swete") and p["swete"] != "—":
                check(contains(swete_all, p["swete"]), f"{e['id']}: Swete reading {p['swete']!r} not in Swete", errors)
            if p.get("mt") and p["mt"] != "—":
                check(contains(r["mt_text"], p["mt"], hebrew=True), f"{e['id']}: Hebrew {p['mt']!r} not in MT {mt}", errors)
            for s in p.get("with", []):
                check(s in SIGLA, f"{e['id']}: unknown siglum {s!r}", errors)
        check(e["type"] in TYPES, f"{e['id']}: bad type", errors)
        check(e["affinity"] in AFFINITIES, f"{e['id']}: bad affinity", errors)
        check(e["speaker"] in SPEAKERS, f"{e['id']}: bad speaker", errors)
        records.append(r)
    return records


def build_ot(entries, texts, errors):
    records = []
    for e in entries:
        r = dict(e)
        if isinstance(e.get("greek"), bool):  # YAML reads a bare yes/no as a boolean
            e["greek"] = r["greek"] = "yes" if e["greek"] else "no"
        r["at_text"] = refs_text(texts, "hboWLC", e["at"])
        r["source_text"] = refs_text(texts, "hboWLC", e["source"])
        lx, ls = e.get("lxx") or e["at"], e.get("lxx_source") or e["source"]
        r["lxx_text"] = "" if lx == "—" else refs_text(texts, "grcbrent", lx)
        r["lxx_source_text"] = "" if ls == "—" else refs_text(texts, "grcbrent", ls)
        check(r["lxx_text"] or e.get("greek") == "absent", f"{e['id']}: no Brenton text for {lx}", errors)
        check(r["lxx_source_text"] or e.get("greek") == "source-absent", f"{e['id']}: no Brenton text for {ls}", errors)
        check(contains(r["at_text"], e["quote"], hebrew=True), f"{e['id']}: quote not in {e['at']}", errors)
        check(contains(r["source_text"], e["source_words"], hebrew=True), f"{e['id']}: source words not in {e['source']}", errors)
        check(e["type"] in TYPES, f"{e['id']}: bad type", errors)
        check(e["speaker"] in SPEAKERS, f"{e['id']}: bad speaker", errors)
        check(e["group"] in OT_GROUPS, f"{e['id']}: bad group", errors)
        check(e.get("greek", "yes") in GREEK_KEEPS, f"{e['id']}: bad greek", errors)
        records.append(r)
    return records


# ---------------------------------------------------------------- counts

def counts(nt, ot):
    c = {}
    headline = [r for r in nt if not r.get("only")]
    c["nt_total"] = len(headline)
    c["nt_strict"] = sum(1 for r in headline if not r.get("borderline"))
    c["nt_sayings"] = len({r["saying"] for r in headline})
    c["nt_sayings_strict"] = len({r["saying"] for r in headline if not r.get("borderline")})
    c["nt_only"] = collections.Counter(tuple(r["only"]) for r in nt if r.get("only"))
    c["by_speaker"] = collections.Counter(r["speaker"] for r in headline)
    c["by_book"] = collections.Counter(r["at"].split(" ")[0] for r in headline)
    c["by_type"] = collections.Counter(r["type"] for r in headline)
    c["by_type_strict"] = collections.Counter(r["type"] for r in headline if not r.get("borderline"))
    c["by_formula"] = collections.Counter(("formula" if r.get("formula") else "none", r["type"]) for r in headline)
    c["by_affinity"] = collections.Counter(r["affinity"] for r in headline)
    c["by_affinity_strict"] = collections.Counter(r["affinity"] for r in headline if not r.get("borderline"))
    sayings = {}
    for r in headline:
        sayings.setdefault(r["saying"], []).append(r["affinity"])
    c["sayings_affinity"] = collections.Counter(
        (a[0] if len(set(a)) == 1 else "parallels-differ") for a in sayings.values())
    witnesses = collections.Counter()
    for r in headline:
        for p in r.get("points", []):
            for s in p.get("with", []):
                witnesses[s] += 1
    c["witnesses"] = witnesses
    c["ot_by_group"] = collections.Counter(r["group"] for r in ot)
    hl = [r for r in ot if r["group"] == "headline"]
    c["ot_headline"] = len(hl)
    c["ot_strict"] = sum(1 for r in hl if not r.get("borderline"))
    c["ot_by_type"] = collections.Counter(r["type"] for r in hl)
    c["ot_by_formula"] = collections.Counter("formula" if r.get("formula") else "none" for r in hl)
    c["ot_greek"] = collections.Counter(r.get("greek", "yes") for r in hl)
    return c


# ---------------------------------------------------------------- rendering

def ref_display(refs):
    out = []
    last_book = None
    for part in refs.split(","):
        part = part.strip()
        book, cv = part.split(" ")
        name = "Daniel (Theodotion)" if book == "DNG" else BOOK_NAMES.get(book, book)
        out.append(cv if book == last_book else f"{name} {cv}")
        last_book = book
    return "; ".join(out)


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def flags(r):
    f = []
    if r.get("formula"):
        f.append("formula")
    if r.get("composite"):
        f.append("composite")
    if r.get("borderline"):
        f.append("borderline")
    if r.get("only"):
        f.append("only in " + " and ".join(NT_TITLES[o] for o in r["only"]))
    return ", ".join(f)


def render(nt, ot, c):
    out = []
    w = out.append
    w("# Where God quotes Scripture\n")
    w("Every place in Scripture where God himself, the Father, the Son or the Holy Spirit, "
      "speaks words of earlier Scripture: Jesus in the Gospels and in Revelation, the Father's "
      "voice from heaven, God on the throne in Revelation, and in the Old Testament the LORD "
      "quoting an earlier book. The study of them is in "
      "[analysis/god-quoting-scripture/](../../analysis/god-quoting-scripture/README.md).\n")
    w("> **Generated** by `tools/build_divine_quotations.py` from "
      "[quotations.yaml](quotations.yaml). Edit that file and re-run the tool; do not edit "
      "this one. The same data, with every text, is in [quotations.json](quotations.json).\n")
    w("For each New Testament entry the verse is given in the SBL Greek New Testament, and in "
      "the Textus Receptus (TR) and the Byzantine text of 1904 (Byz) where they differ from it. "
      "The Septuagint is given in Brenton's edition and in Swete's (whose text is Codex "
      "Vaticanus, B, except where B is lost: in Genesis 1:1 to 46:28 it is Alexandrinus, A, "
      "and in Psalms 105:27 to 137:6 of the Greek numbering it is Sinaiticus, ℵ), and the "
      "Hebrew in the "
      "Masoretic Text (Westminster Leningrad Codex). The Septuagint is cited by Brenton's "
      "chapter and verse and the Hebrew by its own; the source column gives the English "
      "chapter and verse. In Daniel Brenton prints Theodotion's version, and Swete's Old Greek "
      "is given beside it.\n")
    w("**Agreement** counts how many words of the quotation occur, in the same order, in the "
      "Septuagint verse (accents, case and elision ignored). It measures wording only. The "
      "readings listed under each entry are what decide its affinity.\n")
    w("**Readings** list the points at which the witnesses differ and the quotation sides with "
      "one of them. `with` names the witnesses the New Testament agrees with there: "
      + "; ".join(f"`{k}` {v}" for k, v in SIGLA.items()) + ". Readings of A, ℵ, Q and F come "
      "from Swete's apparatus; readings of Aquila, Symmachus and Theodotion outside Daniel from "
      "Field's *Origenis Hexaplorum quae supersunt* (1875); Göttingen readings are cited from "
      "lxx.confident.faith. See [SOURCES.md](../../SOURCES.md).\n")

    w("## Counts\n")
    w("Each place where a quotation is spoken counts once (two texts fused in one citation count "
      "once; texts quoted one after another count separately). **Strict** leaves out the entries "
      "marked borderline. **Sayings** merge the Gospel parallels of one saying. Counts are on the "
      "text common to the three editions; the TR and Byz have "
      f"{sum(c['nt_only'].values())} more (Mark 9:44 and 9:46).\n")
    sp = collections.Counter()
    for r in nt:
        if not r.get("only"):
            sp[(r["speaker"], r["saying"])] += 1
    w("| New Testament | Occurrences | Strict | Sayings |")
    w("| --- | --- | --- | --- |")
    for k in ("jesus", "jesus-risen", "father", "god"):
        rows = [r for r in nt if r["speaker"] == k and not r.get("only")]
        w(f"| {SPEAKERS[k]} | {len(rows)} | {sum(1 for r in rows if not r.get('borderline'))} | "
          f"{len({r['saying'] for r in rows})} |")
    w(f"| **All** | **{c['nt_total']}** | **{c['nt_strict']}** | **{c['nt_sayings']}** |\n")
    w("| Type | With a formula | Without | All | Strict |")
    w("| --- | --- | --- | --- | --- |")
    for t in TYPES:
        w(f"| {TYPES[t]} | {c['by_formula'][('formula', t)]} | {c['by_formula'][('none', t)]} | "
          f"{c['by_type'][t]} | {c['by_type_strict'][t]} |")
    w("")
    w("| Affinity | All | Strict | Sayings |")
    w("| --- | --- | --- | --- |")
    for a in AFFINITIES:
        w(f"| {AFFINITIES[a]} | {c['by_affinity'][a]} | {c['by_affinity_strict'][a]} | {c['sayings_affinity'][a]} |")
    w(f"| The Gospel parallels of one saying differ | | | {c['sayings_affinity']['parallels-differ']} |\n")
    w("| Old Testament | Entries | Direct | Adapted | Paraphrase | With a formula |")
    w("| --- | --- | --- | --- | --- | --- |")
    for g, title in OT_GROUPS.items():
        rows = [r for r in ot if r["group"] == g]
        tc = collections.Counter(r["type"] for r in rows)
        w(f"| {title} | {len(rows)} | {tc['direct']} | {tc['adapted']} | {tc['paraphrase']} | "
          f"{sum(1 for r in rows if r.get('formula'))} |")
    w("")
    w("## Contents\n")
    w("| Where | Speaker | Source | Type | Affinity | Notes |")
    w("| --- | --- | --- | --- | --- | --- |")
    seen = {}
    anchors = {}
    for r in nt:
        anchors[r["id"]] = anchor(f"{ref_display(r['at'])} — {ref_display(r['source'])}", seen)
        w(f"| [{ref_display(r['at'])}](#{anchors[r['id']]}) | {SPEAKERS[r['speaker']]} | "
          f"{ref_display(r['source'])} | {r['type']} | {r['affinity']} | {flags(r)} |")
    w("")
    w("Old Testament entries are listed after the New Testament ones, [here](#the-old-testament).\n")

    w("## The New Testament\n")
    for r in nt:
        w(f"### {ref_display(r['at'])} — {ref_display(r['source'])}\n")
        meta = [f"**Speaker:** {SPEAKERS[r['speaker']]}",
                f"**Type:** {TYPES[r['type']]}",
                f"**Affinity:** {AFFINITIES[r['affinity']]}"]
        if r.get("formula"):
            meta.append(f"**Formula:** {r['formula']}")
        else:
            meta.append("**Formula:** none")
        fl = [x for x in ("composite", "borderline") if r.get(x)]
        if fl:
            meta.append("**Flags:** " + ", ".join(fl))
        if r.get("only"):
            meta.append("**Only in:** " + ", ".join(NT_TITLES[o] for o in r["only"]))
        w(" · ".join(meta) + "\n")
        w(f"**Quoted words:** {r['quote']}\n")
        base = (r.get("only") or ["sbl"])[0]
        w(f"- **{NT_TITLES[base]}** {r['texts'][base]}")
        shown = {tokens_key(r['texts'][base])}
        for ed in ("sbl", "tr", "byz"):
            if ed == base or not r["texts"][ed]:
                continue
            k = tokens_key(r["texts"][ed])
            if k not in shown:
                w(f"- **{NT_TITLES[ed]}** {r['texts'][ed]}")
                shown.add(k)
        others = [NT_TITLES[ed] for ed in ("sbl", "tr", "byz") if ed != base and tokens_key(r['texts'][ed]) == tokens_key(r['texts'][base])]
        if others:
            w(f"- {', '.join(others)}: as {NT_TITLES[base]}")
        lxx = r.get("lxx") or r["source"]
        mt = r.get("mt") or r["source"]
        w(f"- **Septuagint, Brenton** ({ref_display(lxx)}): {r['lxx_text'] or '(not in Brenton)'}")
        for s in r["swete"]:
            label = "Swete, Old Greek" if s["old_greek"] else "Swete"
            w(f"- **{label}** ({ref_display(s['ref'])}): {s['text']}")
            if s["goettingen"]:
                w("  - Göttingen reads " + "; ".join(f"{g} for Swete's {sw}" for sw, g in s["goettingen"]))
        w(f"- **Hebrew** ({ref_display(mt)}): {r['mt_text']}")
        ab, nb = r["agreement"]["brenton"]
        ag = f"{ab} of {nb} words with Brenton"
        if r["agreement"]["swete"]:
            a2, n2 = r["agreement"]["swete"]
            ag += f", {a2} of {n2} with Swete"
        w(f"- **Agreement:** {ag}\n")
        if r.get("points"):
            w("| New Testament | Brenton | Swete | Hebrew | Other witnesses | With |")
            w("| --- | --- | --- | --- | --- | --- |")
            for p in r["points"]:
                sw = p.get("swete") or ("as Brenton" if p.get("lxx") and r["swete"] else "")
                w(f"| {cell(p['nt'])} | {cell(p.get('lxx', ''))} | {cell(sw)} | "
                  f"{cell(p.get('mt', ''))} | {cell(p.get('other', ''))} | {', '.join(p.get('with', []))} |")
            w("")
        if r.get("editions"):
            w(f"**Editions:** {r['editions']}\n")
        if r.get("note"):
            w(f"{r['note']}\n")

    w("## The Old Testament\n")
    w("Places where the LORD, speaking in his own first person or through a prophet's "
      "\"thus says the LORD\", repeats the words of an earlier passage. The Hebrew of each is "
      "given; **Greek** says whether the Septuagint of the quoting passage keeps the verbal "
      "link with its source.\n")
    for g, title in OT_GROUPS.items():
        rows = [r for r in ot if r["group"] == g]
        if not rows:
            continue
        w(f"### {title}\n")
        w("| Where | Speaker | Source | Formula | Type | Greek | Notes |")
        w("| --- | --- | --- | --- | --- | --- | --- |")
        for r in rows:
            fl = "borderline" if r.get("borderline") else ""
            w(f"| [{ref_display(r['at'])}](#{r['id']}) | {SPEAKERS[r['speaker']]} | {ref_display(r['source'])} | "
              f"{cell(r.get('formula', '—'))} | {r['type']} | {GREEK_KEEPS[r.get('greek', 'yes')]} | {fl} |")
        w("")
    for r in ot:
        w(f'<a id="{r["id"]}"></a>\n')
        w(f"#### {ref_display(r['at'])} — {ref_display(r['source'])}\n")
        w(f"- **Quoting** ({ref_display(r['at'])}): {r['at_text']}")
        w(f"- **Source** ({ref_display(r['source'])}): {r['source_text']}")
        w(f"- **Words shared:** {r['quote']} / {r['source_words']}")
        lx, ls = r.get("lxx") or r["at"], r.get("lxx_source") or r["source"]
        w(f"- **Septuagint, Brenton** ({ref_display(lx) if lx != '—' else ref_display(r['at'])}): {r['lxx_text'] or '(not in the Septuagint)'}")
        w(f"- **Septuagint of the source** ({ref_display(ls) if ls != '—' else ref_display(r['source'])}): {r['lxx_source_text'] or '(not in the Septuagint)'}")
        w(f"- **Link in the Greek:** {GREEK_KEEPS[r.get('greek', 'yes')]}\n")
        if r.get("note"):
            w(f"{r['note']}\n")
    return "\n".join(out).rstrip() + "\n"


def tokens_key(text):
    return " ".join(tokens(text))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="download the texts again")
    args = ap.parse_args()
    with open(DATA, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    texts = {code: fetch_edition(code, args.refresh) for code in
             ("hboWLC", "grcbrent", "grcsbl", "grctr", "grcbyz")}
    swete = Swete(args.refresh)
    errors = []
    nt = build_nt(data["new_testament"], texts, swete, errors)
    ot = build_ot(data["old_testament"], texts, errors)
    ids = [r["id"] for r in nt + ot]
    for i in {x for x in ids if ids.count(x) > 1}:
        errors.append(f"duplicate id {i}")
    if errors:
        for e in errors:
            print("ERROR", e)
        raise SystemExit(f"{len(errors)} errors")
    c = counts(nt, ot)
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write(render(nt, ot, c))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump({
            "generated_by": "tools/build_divine_quotations.py",
            "speakers": SPEAKERS, "types": TYPES, "affinities": AFFINITIES,
            "sigla": SIGLA, "ot_groups": OT_GROUPS,
            "counts": {k: (dict((" / ".join(x) if isinstance(x, tuple) else x, n) for x, n in v.items())
                           if isinstance(v, collections.Counter) else v) for k, v in c.items()},
            "new_testament": nt, "old_testament": ot,
        }, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{c['nt_total']} New Testament quotations ({c['nt_strict']} without the borderline), "
          f"{c['nt_sayings']} distinct sayings; {c['ot_headline']} Old Testament")


if __name__ == "__main__":
    main()
