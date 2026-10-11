#!/usr/bin/env python3
"""Fetch the Book of Concord from thebookofconcord.org and render it as Markdown.

Source: https://thebookofconcord.org/, the Concordia Triglotta English
translation (1921), which the site's legal page describes as no longer under
copyright. See SOURCES.md.

The page list is read from the site's navigation menu, in menu order. Fetched
pages are cached in a directory (default: .cache/book-of-concord, git-ignored)
so the rendering can be re-run without hitting the site again.

Usage: python3 tools/build_book_of_concord.py [--cache DIR] [--refresh]
"""
import argparse
import html
import os
import re
import time
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "confessions", "lutheran", "book-of-concord")
SITE = "https://thebookofconcord.org/"

# (site slug, output file, display title), in the order of the Book of Concord.
DOCUMENTS = [
    ("preface-to-the-christian-book-of-concord", "preface", "Preface to the Christian Book of Concord (1580)"),
    ("three-universal-or-ecumenical-creeds", "ecumenical-creeds", "The Three Universal or Ecumenical Creeds"),
    ("augsburg-confession", "augsburg-confession", "The Augsburg Confession (1530)"),
    ("apology-of-the-augsburg-confession", "apology-of-the-augsburg-confession", "The Apology of the Augsburg Confession (1531)"),
    ("smalcald-articles", "smalcald-articles", "The Smalcald Articles (1537)"),
    ("power-and-primacy-of-the-pope", "treatise-on-the-power-and-primacy-of-the-pope", "Treatise on the Power and Primacy of the Pope (1537)"),
    ("small-catechism", "small-catechism", "The Small Catechism (1529)"),
    ("large-catechism", "large-catechism", "The Large Catechism (1529)"),
    ("formula-of-concord-epitome", "formula-of-concord-epitome", "The Formula of Concord: Epitome (1577)"),
    ("formula-of-concord-solid-declaration", "formula-of-concord-solid-declaration", "The Formula of Concord: Solid Declaration (1577)"),
]

# Pages that only list links to the pages below them.
TABLES_OF_CONTENTS = {
    "augsburg-confession",
    "augsburg-confession/chief-articles-of-faith",
    "apology-of-the-augsburg-confession",
    "smalcald-articles",
    "small-catechism",
    "large-catechism",
    "formula-of-concord-epitome",
    "formula-of-concord-solid-declaration",
}

# Pages that embed the full text of every page below them. The embedding page
# is rendered and the embedded pages are skipped.
CONTAINERS = {
    "three-universal-or-ecumenical-creeds",
    "small-catechism/part-i",
    "small-catechism/part-ii",
    "small-catechism/part-iii",
    "small-catechism/part-iv",
    "large-catechism/part-i",
    "large-catechism/part-ii",
    "large-catechism/part-iii",
    "large-catechism/part-iv",
}

SKIP_CLASSES = ("cross-reference-link", "wtr-time-wrap", "outlined-box", "wp-block-buttons")
VOID = {"br", "hr", "img", "input", "meta", "link"}


class Node:
    def __init__(self, tag, attrs, parent=None):
        self.tag, self.attrs, self.parent, self.children = tag, dict(attrs), parent, []


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", {})
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag == "br":  # the site writes some line breaks as </br>
            self.cur.children.append(Node("br", {}, self.cur))
            return
        node = self.cur
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.cur = node.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def fetch(url, cache, refresh):
    name = re.sub(r"[^a-z0-9]+", "_", url[len(SITE):].strip("/") or "index") + ".html"
    path = os.path.join(cache, name)
    if refresh or not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": "Denominations-and-Traditions/1.0"})
        with urllib.request.urlopen(req) as resp:
            data = resp.read().decode("utf-8")
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)
        time.sleep(0.3)
    with open(path, encoding="utf-8") as f:
        return f.read()


def menu_slugs(index_html):
    slugs = []
    for url in re.findall(r'href="(https://thebookofconcord\.org/[^"#?]+)"', index_html):
        slug = url[len(SITE):].strip("/")
        if slug and slug not in slugs:
            slugs.append(slug)
    return slugs


def has_class(node, names):
    cls = node.attrs.get("class") or ""
    return any(n in cls for n in names)


def inline(node, in_heading=False):
    """Render a node's inline content to Markdown text."""
    out = []
    for child in node.children:
        if isinstance(child, str):
            out.append(re.sub(r"\s+", " ", child))
        elif child.tag == "br":
            out.append(" " if in_heading else "<br>\n")
        elif child.tag == "sup":
            num = inline(child).strip()
            if not in_heading and num:
                if num.isdigit():
                    num = str(int(num))
                out.append(f"<sup>{num}</sup> ")
        elif child.tag in ("em", "i") and not has_class(child, ("fa-",)):
            text = inline(child, in_heading)
            out.append(wrap(text, "*"))
        elif child.tag in ("strong", "b"):
            out.append(wrap(inline(child, in_heading), "**"))
        elif child.tag in ("button", "script", "style"):
            continue
        else:
            out.append(inline(child, in_heading))
    return "".join(out)


def wrap(text, mark):
    stripped = text.strip()
    if not stripped:
        return text
    lead = text[: len(text) - len(text.lstrip())]
    trail = text[len(text.rstrip()):]
    return f"{lead}{mark}{stripped}{mark}{trail}"


def clean(text):
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *<br>\n *", "<br>\n", text)
    text = re.sub(r"^(\s*<br>\s*)+|(\s*<br>\s*)+$", "", text.strip())
    return text.strip()


def blocks(node, level, out):
    """Collect (kind, text) blocks from a container node."""
    for child in node.children:
        if isinstance(child, str):
            if child.strip():
                out.append(("p", clean(child)))
            continue
        tag = child.tag
        if tag in ("button", "script", "style") or has_class(child, SKIP_CLASSES):
            continue
        if tag == "h1" and has_class(child, ("insert-page-title",)):
            out.append(("h", (level + 1, clean(inline(child, True)))))
        elif tag in ("h2", "h3", "h4", "h5"):
            depth = {"h2": 1, "h3": 2, "h4": 3, "h5": 4}[tag]
            text = clean(inline(child, True))
            if text:
                out.append(("h", (min(level + depth, 6), text)))
        elif tag == "p":
            text = clean(inline(child))
            if text:
                out.append(("p", text))
        elif tag in ("ul", "ol"):
            items = []
            for i, li in enumerate(c for c in child.children if not isinstance(c, str) and c.tag == "li"):
                bullet = f"{i + 1}." if tag == "ol" else "-"
                items.append(f"{bullet} {clean(inline(li))}")
            if items:
                out.append(("list", "\n".join(items)))
        elif tag == "blockquote":
            inner = []
            blocks(child, level, inner)
            if not inner:
                inner = [("p", clean(inline(child)))]
            text = "\n>\n".join("> " + t.replace("\n", "\n> ") for k, t in inner if k == "p")
            out.append(("quote", text))
        elif tag == "hr":
            continue
        else:
            blocks(child, level, out)


TERMINAL = re.compile(r"""[.!?:;"”’')\]]\s*(\*+)?$""")


def join_verses(items):
    """Join a verse paragraph to the next when the site splits a sentence across them."""
    merged = []
    for kind, text in items:
        if (
            kind == "p"
            and merged
            and merged[-1][0] == "p"
            and text.startswith("<sup>")
            and merged[-1][1].startswith("<sup>")
            and not TERMINAL.search(merged[-1][1])
            and not merged[-1][1].endswith("<br>")
        ):
            merged[-1] = ("p", merged[-1][1] + " " + text)
        else:
            merged.append((kind, text))
    return merged


def page(html_text):
    title = re.search(r'<h1 class="entry-title"[^>]*>(.*?)</h1>', html_text, re.S)
    start = html_text.find('<div class="entry-content"')
    end = html_text.rfind("</article>")
    builder = TreeBuilder()
    builder.feed(html_text[start:end])
    items = []
    blocks(builder.root, 2, items)
    return html.unescape(re.sub(r"<[^>]+>", "", title.group(1))).strip(), join_verses(items)


def render(slug, out_name, doc_title, pages):
    lines = [
        f"# {doc_title}",
        "",
        f"> **Source:** [thebookofconcord.org/{slug}/]({SITE}{slug}/), *Concordia Triglotta* English "
        "translation (St. Louis: Concordia Publishing House, 1921), which is in the public domain. "
        "Superscript numbers are the Triglotta's paragraph numbers. Generated by "
        "`tools/build_book_of_concord.py`; see [SOURCES.md](/SOURCES.md).",
        "",
    ]
    single = len(pages) == 1
    for page_slug, (title, items) in pages:
        # Pages nested under another page (Smalcald Articles II.i) get a deeper heading.
        depth = max(page_slug.count("/"), 1)
        if not single:
            lines += ["#" * (1 + depth) + f" {title}", ""]
        # Shift the page's headings so the shallowest sits one level below the page title.
        levels = [text[0] for kind, text in items if kind == "h"]
        shift = (2 if single else 2 + depth) - min(levels, default=0)
        for kind, text in items:
            if kind == "h":
                lvl, htext = text
                lines += ["#" * min(lvl + shift, 6) + " " + htext, ""]
            else:
                lines += [text, ""]
    with open(os.path.join(OUT, out_name + ".md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=os.path.join(ROOT, ".cache", "book-of-concord"))
    ap.add_argument("--refresh", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    slugs = menu_slugs(fetch(SITE, args.cache, args.refresh))
    for slug, out_name, doc_title in DOCUMENTS:
        doc_slugs = [s for s in slugs if s == slug or s.startswith(slug + "/")]
        pages = []
        for s in doc_slugs:
            if s in TABLES_OF_CONTENTS:
                continue
            if any(s.startswith(c + "/") for c in CONTAINERS):
                continue
            pages.append((s, page(fetch(SITE + s + "/", args.cache, args.refresh))))
        render(slug, out_name, doc_title, pages)
        print(f"{out_name}: {len(pages)} pages")


if __name__ == "__main__":
    main()
