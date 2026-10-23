"""Safe Markdown rendering and repository link resolution for the static site."""

from html import escape
from pathlib import Path
import re
from string import Template
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token


REPOSITORY_URL = "https://github.com/ehuerta6/bloomberg-interview-practice"
SITE_FILES = Path(__file__).resolve().parent / "site"
CATEGORY_LABELS = {
    "round-1": "Round 1 · Code Review",
    "round-2": "Round 2 · Implementation",
    "system-design": "System Design",
}


def heading_slug(text):
    """Prefix content IDs so Markdown cannot shadow browser globals."""
    slug = re.sub(r"[^\w\-\s]", "", text.lower()).replace(" ", "-")
    return "heading-" + slug


def repository_link(path, directory=False, image=False):
    mode = "raw" if image else "tree" if directory else "blob"
    return f"{REPOSITORY_URL}/{mode}/main/{quote(path, safe='/')}"


def resolve_link(url, source, root, pages, image=False):
    """Resolve Markdown-relative links independently of the output directory."""
    parts = urlsplit(url)
    if parts.scheme:
        if parts.scheme.lower() not in ("https", "http", "mailto"):
            raise ValueError(f"{source}: unsupported link scheme")
        return url
    if parts.netloc or "\\" in unquote(parts.path):
        raise ValueError(f"{source}: unsupported link path: {url}")
    if not parts.path:
        fragment = heading_slug(unquote(parts.fragment)) if parts.fragment else ""
        return urlunsplit(("", "", "", parts.query, fragment))
    target = (root / source.parent / unquote(parts.path)).resolve()
    if not target.is_relative_to(root):
        raise ValueError(f"{source}: link escapes repository: {url}")
    if not target.exists():
        raise ValueError(f"{source}: missing link target: {url}")
    relative = target.relative_to(root).as_posix()
    fragment = parts.fragment
    if relative in pages and not image:
        destination = pages[relative] + ".html"
        fragment = heading_slug(unquote(fragment)) if fragment else ""
    else:
        destination = repository_link(relative, target.is_dir(), image)
    result = urlsplit(destination)
    return urlunsplit((result.scheme, result.netloc, result.path, parts.query, fragment))


def render_markdown(markdown, source, root, pages, *, reveal_solutions=False):
    """Render CommonMark plus tables/strikethrough; raw HTML is always text."""
    root, source = Path(root).resolve(), Path(source)
    parser = MarkdownIt("commonmark", {"html": False}).enable(["table", "strikethrough"])
    default_validate = parser.validateLink
    parser.validateLink = lambda url: (
        default_validate(url)
        and urlsplit(url).scheme.lower() in ("", "http", "https", "mailto")
        and not (not urlsplit(url).scheme and urlsplit(url).netloc)
    )
    tokens = parser.parse(markdown)
    headings = set()

    def visit(items):
        for token in items:
            for attribute in ("href", "src"):
                url = token.attrGet(attribute)
                if url is not None:
                    token.attrSet(attribute, resolve_link(url, source, root, pages, attribute == "src"))
            if token.children:
                visit(token.children)

    visit(tokens)
    for index, token in enumerate(tokens):
        if token.type == "heading_open":
            base = heading_slug(tokens[index + 1].content)
            slug, count = base, 0
            while slug in headings:
                count += 1
                slug = f"{base}-{count}"
            headings.add(slug)
            token.attrSet("id", slug)
        elif token.type == "fence" and token.info.strip().split(maxsplit=1)[:1] == ["mermaid"]:
            token.type = "html_block"
            token.content = '<pre class="mermaid" aria-label="Mermaid diagram source">' + escape(token.content) + "</pre>\n"
    parser.renderer.rules["table_open"] = lambda *_: '<div class="table-scroll"><table>\n'
    parser.renderer.rules["table_close"] = lambda *_: "</table></div>\n"
    if reveal_solutions:
        # Wrap the parsed section so fenced examples cannot trigger a disclosure.
        # Keep its original heading and links; solution files are never read.
        boundaries = []
        for index, token in enumerate(tokens):
            if token.type == "heading_open" and token.tag == "h2" and tokens[index + 1].content == "Reference Solution":
                end = next((position for position in range(index + 3, len(tokens))
                            if tokens[position].type == "heading_open" and tokens[position].tag in ("h1", "h2")), len(tokens))
                boundaries.append((index, end))
        for start, end in reversed(boundaries):
            opening = Token("html_block", "", 0)
            opening.content = '<details class="solution-reveal">\n<summary>Reveal reference solution link</summary>\n<div class="details-content">\n'
            closing = Token("html_block", "", 0)
            closing.content = '</div>\n</details>\n'
            tokens.insert(end, closing)
            tokens.insert(start, opening)
    return parser.renderer.render(tokens, parser.options, {})


def render_page(problem, root, pages):
    source = Path(problem["source_path"])
    body = render_markdown((root / source).read_text(encoding="utf-8"), source, root, pages, reveal_solutions=True)
    values = {
        "title": problem["title"],
        "category": CATEGORY_LABELS[problem["category"]],
        "difficulty": problem["difficulty"],
        "problem_id": problem["id"],
        "category_id": problem["category"],
        "number": f'{problem["number"]:02d}',
        "source_url": repository_link(source.as_posix()),
    }
    values = {key: escape(value, quote=True) for key, value in values.items()}
    values["body"] = body
    values["mermaid_script"] = (
        '  <script type="module" src="../renderer/mermaid.mjs"></script>\n'
        if '<pre class="mermaid" ' in body else ""
    )
    return Template((SITE_FILES / "page.html").read_text(encoding="utf-8")).substitute(values)
