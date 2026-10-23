#!/usr/bin/env python3
"""Verify Round 1 article text, inline code, labels, and resource links.

Run with the pinned site-build environment; see README.md beside this file.
This reads assignments and generated pages without opening starter or solution code.
"""

from html.parser import HTMLParser
import json
from pathlib import Path
import re

from markdown_it import MarkdownIt


ROOT = Path(__file__).resolve().parents[3]
REPOSITORY = "https://github.com/ehuerta6/bloomberg-interview-practice/tree/main/"


class Article(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.active = False
        self.text = []
        self.codes = []
        self.code = None
        self.links = []
        self.tags = []
        self.headings = []
        self.heading = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag == "article":
            self.active = True
        if not self.active:
            return
        self.tags.append(tag)
        if tag == "code":
            self.code = []
        if tag in ("h1", "h2"):
            self.heading = []
        if tag == "a":
            self.links.append(dict(attrs)["href"])

    def handle_data(self, text):
        if not self.active:
            return
        self.text.append(text)
        if self.code is not None:
            self.code.append(text)
        if self.heading is not None:
            self.heading.append(text)

    def handle_endtag(self, tag):
        if not self.active:
            return
        if tag == "code":
            self.codes.append("".join(self.code))
            self.code = None
        if tag in ("h1", "h2"):
            self.headings.append("".join(self.heading))
            self.heading = None
        if tag in ("p", "h1", "h2", "li", "pre", "tr"):
            self.text.append("\n")
        if tag == "article":
            self.active = False


def normalize(value):
    return re.sub(r"\s+", " ", value).strip()


def plain_inline(token):
    return "".join(
        "\n" if child.type in ("softbreak", "hardbreak") else child.content
        for child in token.children
    )


def audit(problem):
    markdown = (ROOT / problem["source_path"]).read_text(encoding="utf-8")
    html = (ROOT / "docs/problems" / f"{problem['slug']}.html").read_text(encoding="utf-8")
    article = Article(html)
    tokens = MarkdownIt("commonmark", {"html": False}).parse(markdown)
    inline = [token for token in tokens if token.type == "inline"]
    expected = "\n".join(plain_inline(token) for token in inline)
    problem_id = problem["id"]
    assert normalize("".join(article.text)) == normalize(expected), problem_id + " text"
    codes = [child.content for token in inline for child in token.children if child.type == "code_inline"]
    assert article.codes == codes, problem_id + " code"
    allowed_tags = {"article", "h1", "h2", "p", "strong", "ul", "li", "code", "a"}
    assert set(article.tags) <= allowed_tags, problem_id + " unexpected content"
    assert article.links == [
        REPOSITORY + problem["starter_path"],
        REPOSITORY + problem["solution_path"],
    ], problem_id + " links"
    assert f'Round 1 · Code Review · {problem["difficulty"]}' in html, problem_id + " label"
    assert f'data-problem-id="{problem_id}"' in html, problem_id + " identity"
    assert "<script" not in html, problem_id + " unexpected script"
    assert len([heading for heading in article.headings if heading.startswith("PR #")]) == 1
    return {
        "id": problem_id,
        "difficulty": problem["difficulty"],
        "list_items": sum(token.type == "list_item_open" for token in tokens),
        "code_spans": len(codes),
    }


if __name__ == "__main__":
    manifest = json.loads((ROOT / "scripts/problem-manifest.json").read_text(encoding="utf-8"))
    entries = [problem for problem in manifest["problems"] if problem["category"] == "round-1"]
    assert len(entries) == 25, "expected 25 Round 1 problems"
    print(json.dumps([audit(problem) for problem in entries], indent=2))
    print("PASS: 25 pages preserve full source text, code, labels, and explicit resource links")
