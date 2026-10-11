#!/usr/bin/env python3
"""Render the vendored Reformed Standards compendium YAML into Markdown.

Source data: sources/reformed-standards-compendium/data (Apache-2.0, see
sources/reformed-standards-compendium/LICENSE and SOURCES.md).

Usage: python3 tools/build_reformed.py
"""
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "reformed-standards-compendium", "data")
OUT = os.path.join(ROOT, "confessions")
UPSTREAM = "https://github.com/reformed-standards/compendium/blob/{commit}/data/{path}"
COMMIT = "c2f698ed3deaa50687b6dc1b14b4dbf71cb44fd8"

# (source yaml, output markdown, display title)
DOCUMENTS = [
    ("ancient-church/nicene-creed", "ecumenical-creeds/nicene-creed", "The Nicene Creed"),
    ("ancient-church/athanasian-creed", "ecumenical-creeds/athanasian-creed", "The Athanasian Creed"),
    ("three-forms-of-unity/belgic-confession", "reformed/continental/three-forms-of-unity/belgic-confession", "The Belgic Confession (1561)"),
    ("three-forms-of-unity/heidelberg-catechism", "reformed/continental/three-forms-of-unity/heidelberg-catechism", "The Heidelberg Catechism (1563)"),
    ("three-forms-of-unity/canons-of-dort", "reformed/continental/three-forms-of-unity/canons-of-dort", "The Canons of Dort (1618–1619)"),
    ("westminster/wcf", "reformed/presbyterian/westminster-standards/westminster-confession-of-faith", "The Westminster Confession of Faith (1646)"),
    ("westminster/wlc", "reformed/presbyterian/westminster-standards/westminster-larger-catechism", "The Westminster Larger Catechism (1647)"),
    ("westminster/wsc", "reformed/presbyterian/westminster-standards/westminster-shorter-catechism", "The Westminster Shorter Catechism (1647)"),
    ("westminster/government", "reformed/presbyterian/westminster-standards/form-of-presbyterial-church-government", "The Form of Presbyterial Church Government (1645)"),
    ("westminster/directory-for-publick-worship", "reformed/presbyterian/westminster-standards/directory-for-the-publick-worship-of-god", "The Directory for the Publick Worship of God (1645)"),
    ("westminster/directory-for-family-worship", "reformed/presbyterian/westminster-standards/directory-for-family-worship", "The Directory for Family Worship (1647)"),
    ("westminster/sum-of-saving-knowledge", "reformed/presbyterian/westminster-standards/sum-of-saving-knowledge", "The Sum of Saving Knowledge (c. 1650)"),
    ("westminster/solemn-league-and-covenant", "reformed/presbyterian/westminster-standards/solemn-league-and-covenant", "The Solemn League and Covenant (1643)"),
    ("westminster/to-the-christian-reader", "reformed/presbyterian/westminster-standards/to-the-christian-reader", "To the Christian Reader, Especially Heads of Families"),
    ("westminster/epistle-to-the-reader", "reformed/presbyterian/westminster-standards/epistle-to-the-reader", "Mr. Thomas Manton's Epistle to the Reader"),
    ("scottish/scots-confession", "reformed/presbyterian/scots-confession", "The Scots Confession (1560)"),
    ("anglican/39-articles", "reformed/anglican/thirty-nine-articles", "The Thirty-Nine Articles of Religion (1571)"),
    ("second-london/1689-confession", "reformed/reformed-baptist/second-london-baptist-confession-1689", "The Second London Baptist Confession of Faith (1677/1689)"),
    ("second-london/keach", "reformed/reformed-baptist/keachs-catechism", "Keach's Catechism (1693)"),
    ("british/savoy", "reformed/congregational/savoy-declaration", "The Savoy Declaration of Faith and Order (1658)"),
]

# Chapter labels where the source's sequential numbering would mislead.
CHAPTER_LABELS = {
    "three-forms-of-unity/canons-of-dort": [
        "First Head of Doctrine",
        "Second Head of Doctrine",
        "Third and Fourth Heads of Doctrine",
        "Fifth Head of Doctrine",
    ],
}

REF = re.compile(r"^([1-3]?)([A-Za-z]+)\.(\d+)(?:\.(\d+))?$")


def book_name(num, book):
    return f"{num} {book}" if num else book


def fmt_other(ref):
    """Format a chapter-only ref ("Ps.23") or a range ("Matt.28.19-Matt.28.20")."""
    start, _, end = ref.partition("-")
    a, b = REF.match(start), REF.match(end) if end else None
    if not a or (end and not b):
        return ref
    out = f"{book_name(a.group(1), a.group(2))} {a.group(3)}" + (f":{a.group(4)}" if a.group(4) else "")
    if b:
        if b.group(1, 2) != a.group(1, 2):
            out += f"–{book_name(b.group(1), b.group(2))} {b.group(3)}" + (f":{b.group(4)}" if b.group(4) else "")
        elif b.group(3) == a.group(3) and b.group(4):
            out += f"–{b.group(4)}"
        else:
            out += f"–{b.group(3)}" + (f":{b.group(4)}" if b.group(4) else "")
    return out


def fmt_refs(refs):
    """Format OSIS-style refs ("Rom.14.7") as "Rom 14:7", collapsing runs of verses."""
    parts, run = [], None  # run = [book, chapter, first_verse, last_verse]

    def flush():
        if run:
            book, ch, first, last = run
            parts.append(f"{book} {ch}:{first}" + (f"–{last}" if last != first else ""))

    for ref in refs:
        if ref is None:
            continue
        ref = str(ref)
        m = REF.match(ref)
        if not m or m.group(4) is None:
            flush()
            run = None
            parts.append(fmt_other(ref))
            continue
        book, ch, vs = book_name(m.group(1), m.group(2)), m.group(3), int(m.group(4))
        if run and run[0] == book and run[1] == ch and vs == run[3] + 1:
            run[3] = vs
        else:
            flush()
            run = [book, ch, vs, vs]
    flush()
    return "; ".join(parts)


def proofs(verses):
    if not verses:
        return ""
    lines = ["", "<details><summary>Scripture proofs</summary>", ""]
    if isinstance(verses, dict):
        for key, refs in verses.items():
            refs = [r for r in (refs if isinstance(refs, list) else [refs]) if r is not None]
            if not refs:
                continue
            lines.append(f"- **[{key}]** " + fmt_refs(refs))
    else:
        refs = [r for r in verses if r is not None]
        if not refs:
            return ""
        lines.append("- " + fmt_refs(refs))
    if len(lines) == 3:
        return ""
    lines += ["", "</details>"]
    return "\n".join(lines)


def text(t):
    return (t or "").strip()


def render_questions(questions, out, prefix="Q."):
    for q in questions:
        out.append(f"### {prefix} {q['number']}. {text(q['question'])}\n")
        out.append(f"**A.** {text(q['answer'])}")
        out.append(proofs(q.get("verses")))
        out.append("")


def render(data, labels=None):
    out = []
    if "text" in data:
        out += [text(data["text"]), proofs(data.get("verses")), ""]
    if "days" in data:
        for day in data["days"]:
            out.append(f"## Lord's Day {day['number']}\n")
            render_questions(day["questions"], out, "Q.")
    if "questions" in data:
        render_questions(data["questions"], out, "Q.")
    for ch in data.get("chapters", []) or []:
        if isinstance(ch, str):
            out += [text(ch), ""]
            continue
        num = ch.get("number")
        name = text(ch.get("name"))
        if labels:
            out.append(f"## {labels[num - 1]}: {name}\n")
        elif num is not None:
            out.append(f"## {num}. {name}".rstrip() + "\n")
        elif name:
            out.append(f"## {name}\n")
        if "text" in ch:
            out += [text(ch["text"]), proofs(ch.get("verses")), ""]
        for art in ch.get("articles", []) or []:
            out.append(f"**{art['number']}.** {text(art['text'])}")
            out.append(proofs(art.get("verses")))
            out.append("")
        if ch.get("rejections"):
            out.append("### Rejection of Errors\n")
            for rej in ch["rejections"]:
                out.append(f"**Error {rej['number']}.** {text(rej['text'])}\n")
    if data.get("conclusion"):
        out += ["## Conclusion\n", text(data["conclusion"]), ""]
    body = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"


def main():
    for src, dst, title in DOCUMENTS:
        with open(os.path.join(SRC, src + ".yaml"), encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        upstream = UPSTREAM.format(commit=COMMIT, path=src + ".yaml")
        header = (
            f"# {title}\n\n"
            f"> **Source:** Reformed Standards compendium, [`data/{src}.yaml`]({upstream}) "
            f"(Apache License 2.0). The underlying text is in the public domain. "
            f"Generated by `tools/build_reformed.py`; see [SOURCES.md](/SOURCES.md).\n\n"
        )
        path = os.path.join(OUT, dst + ".md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(header + render(data, CHAPTER_LABELS.get(src)))
        print(f"wrote {os.path.relpath(path, ROOT)}")


if __name__ == "__main__":
    main()
