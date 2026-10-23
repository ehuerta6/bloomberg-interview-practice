#!/usr/bin/env python3
"""Fail CI for stale/nondeterministic output or broken site/repository links."""

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[3]
REPOSITORY = "https://github.com/ehuerta6/bloomberg-interview-practice"
COUNTS = {"round-1": 25, "round-2": 25, "system-design": 15}


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.references = []
        self.problems = []
        self.feed(text)
        if len(self.ids) != len(set(self.ids)):
            raise ValueError("duplicate HTML ids")

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        for attribute in ("href", "src"):
            if attribute in attrs:
                self.references.append(attrs[attribute])
        if "data-problem-id" in attrs:
            self.problems.append(attrs["data-problem-id"])


def confined(path, boundary):
    target = path.resolve()
    if not target.is_relative_to(boundary.resolve()):
        raise ValueError(f"path escapes {boundary}: {path}")
    return target


def check_reference(reference, source, site, root, pages):
    parts = urlsplit(reference)
    if reference.startswith(REPOSITORY + "/"):
        match = re.fullmatch(r"/ehuerta6/bloomberg-interview-practice/(blob|tree|raw)/main/(.+)", parts.path)
        if not match:
            raise ValueError(f"unsupported repository reference: {reference}")
        target = confined(root / unquote(match[2]), root)
        exists = target.is_dir() if match[1] == "tree" else target.is_file()
        if not exists:
            raise ValueError(f"missing repository target: {reference}")
        return
    if parts.scheme in ("https", "http", "mailto"):
        return  # External availability is independent of this offline build gate.
    if parts.scheme or parts.netloc or "\\" in unquote(parts.path):
        raise ValueError(f"unsupported reference: {reference}")
    if parts.path.startswith("/"):
        raise ValueError(f"root-relative path breaks project-site hosting: {reference}")
    target = confined(source.parent / unquote(parts.path), site) if parts.path else source
    if target.is_dir():
        target = target / "index.html"
    if not target.is_file():
        raise ValueError(f"{source.relative_to(site)}: missing local target: {reference}")
    if parts.fragment and target.suffix == ".html":
        if unquote(parts.fragment) not in pages[target].ids:
            raise ValueError(f"{source.relative_to(site)}: missing fragment: {reference}")


def validate_site(root):
    root = root.resolve()
    site = root / "docs"
    problems = json.loads((root / "scripts/problem-manifest.json").read_text(encoding="utf-8"))["problems"]
    if Counter(problem["category"] for problem in problems) != COUNTS:
        raise ValueError("manifest must contain 25/25/15 problems")
    expected = {site / "problems" / f"{problem['slug']}.html" for problem in problems}
    if len(expected) != 65 or set((site / "problems").glob("*.html")) != expected:
        raise ValueError("generated problem pages must exactly match all 65 manifest entries")
    pages = {path: Page(path.read_text(encoding="utf-8")) for path in site.rglob("*.html")}
    catalog = pages[site / "index.html"]
    catalog_links = [link for link in catalog.references if link.startswith("problems/")]
    if Counter(catalog_links) != Counter(f"problems/{problem['slug']}.html" for problem in problems):
        raise ValueError("catalog must link to each of the 65 problem pages exactly once")
    for problem in problems:
        path = site / "problems" / f"{problem['slug']}.html"
        page = pages[path]
        if page.problems != [problem["id"]]:
            raise ValueError(f"{path.name}: wrong problem identity")
        resources = [REPOSITORY + "/blob/main/" + problem["source_path"]]
        resources.append(REPOSITORY + ("/blob/main/" if problem["category"] == "system-design" else "/tree/main/") + problem["solution_path"])
        if problem["starter_path"]:
            resources.append(REPOSITORY + "/tree/main/" + problem["starter_path"])
        if any(page.references.count(resource) != 1 for resource in resources):
            raise ValueError(f"{path.name}: missing or duplicate manifest resource link")
        for asset in ("../assets/site.css", "../assets/cic-logo.png"):
            if asset not in page.references:
                raise ValueError(f"{path.name}: missing shared asset: {asset}")
    for path, page in pages.items():
        for reference in page.references:
            check_reference(reference, path, site, root, pages)
    for css in site.rglob("*.css"):
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css.read_text(encoding="utf-8")):
            check_reference(match[2], css, site, root, pages)
    for asset in (site / "assets/site.css", site / "assets/cic-logo.png"):
        if not asset.is_file() or not asset.stat().st_size:
            raise ValueError(f"missing or empty shared asset: {asset}")
    print(f"PASS links: catalog, 65 problem pages, fragments, assets, and manifest resource paths ({len(pages)} HTML files)")


def generated_snapshot(output):
    return {path.relative_to(output): path.read_bytes() for path in output.rglob("*") if path.is_file()}


def verify(root):
    subprocess.run([sys.executable, "-B", str(root / "scripts/generate_manifest.py"), "--check"], check=True)
    subprocess.run([sys.executable, "-B", str(root / "scripts/build-site.py"), "--check"], check=True)
    with tempfile.TemporaryDirectory(prefix="cic-ci-site-") as temporary:
        first, second = Path(temporary) / "first", Path(temporary) / "second"
        for output in (first, second):
            subprocess.run([sys.executable, "-B", str(root / "scripts/build-site.py"), "--output", str(output)], check=True)
        if generated_snapshot(first) != generated_snapshot(second):
            raise ValueError("two clean site builds produced different bytes")
    print("PASS generation: committed output current; two clean builds identical")
    validate_site(root)


if __name__ == "__main__":
    try:
        verify(ROOT)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"FAIL site: {error}", file=sys.stderr)
        sys.exit(1)
