#!/usr/bin/env python3
"""Generate the problem inventory from Markdown. See scripts/README.md for its contract."""

import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


# These are acceptance counts, not a second inventory of problem content.
CATEGORIES = (
    ("round-1", "problems/round-1", 25, "PR #"),
    ("round-2", "problems/round-2", 25, "Ticket #"),
    ("system-design", "system-design", 15, "Problem "),
)
FILENAME = re.compile(r"([0-9]{2})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md")
DEFAULT_ROOT = Path(__file__).resolve().parents[1]


class ManifestError(ValueError):
    """The source bank cannot produce a valid manifest."""


def resource_path(root, source, text, section, expected, directory=False):
    """Read the resource link in a named section and validate its destination."""
    sections = re.findall(
        rf"^## {re.escape(section)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    if len(sections) != 1:
        raise ManifestError(f"{source}: expected one {section} section")
    links = re.findall(r"\[[^\]\n]+\]\(([^)\n]+)\)", sections[0])
    if len(links) != 1:
        raise ManifestError(f"{source}: expected one link in {section}")
    link = urlsplit(links[0])
    if link.scheme or link.netloc or link.query or link.fragment or "\\" in link.path:
        raise ManifestError(f"{source}: {section} must use a local relative path")
    relative = Path(unquote(link.path))
    if relative.is_absolute():
        raise ManifestError(f"{source}: {section} must use a relative path")
    target = (source.parent / relative).resolve()
    if not target.is_relative_to(root):
        raise ManifestError(f"{source}: {section} link escapes the repository")
    path = target.relative_to(root).as_posix()
    if path != expected:
        raise ManifestError(f"{source}: {section} links to {path}; expected {expected}")
    valid = target.is_dir() if directory else target.is_file()
    if not valid:
        raise ManifestError(f"{source}: missing {section} target: {path}")
    return path


def generate_manifest(root):
    """Return schema v1, ordered by category then numbered source filename."""
    root = Path(root).resolve()
    problems = []
    ids, slugs, sources = set(), set(), set()
    for category, directory, count, heading_prefix in CATEGORIES:
        files = sorted(p for p in (root / directory).glob("*.md") if p.name != "README.md")
        if len(files) != count:
            raise ManifestError(f"{category}: expected {count} Markdown problems, found {len(files)}")
        numbers = []
        for source in files:
            match = FILENAME.fullmatch(source.name)
            if not match:
                raise ManifestError(f"{source}: invalid numbered filename")
            number = int(match[1])
            if number in numbers:
                raise ManifestError(f"{category}: duplicate problem number {number:02d}")
            numbers.append(number)
        if numbers != list(range(1, count + 1)):
            raise ManifestError(f"{category}: problem numbers must be 01 through {count:02d}")
        for source, number in zip(files, numbers):
            text = source.read_text(encoding="utf-8")
            headings = re.findall(r"^# (.+)$", text, re.MULTILINE)
            prefix = f"{heading_prefix}{number:02d} — "
            if len(headings) != 1 or not headings[0].startswith(prefix) or not headings[0][len(prefix):].strip():
                raise ManifestError(f"{source}: expected heading '# {prefix}<title>'")
            difficulties = re.findall(r"^\*\*Difficulty:\*\* (.+)$", text, re.MULTILINE)
            if len(difficulties) != 1 or difficulties[0] not in ("Easy", "Medium", "Hard"):
                raise ManifestError(f"{source}: expected one difficulty: Easy, Medium or Hard")
            source_path = source.relative_to(root).as_posix()
            problem_id = f"{category}-{number:02d}"
            slug = f"{category}-{source.stem}"
            if problem_id in ids or slug in slugs or source_path in sources:
                raise ManifestError(f"{source}: duplicate ID, slug or source path")
            ids.add(problem_id)
            slugs.add(slug)
            sources.add(source_path)
            starter = None
            if category != "system-design":
                starter = resource_path(root, source, text, "Starter Code", f"{category}/{source.stem}", directory=True)
            solution = f"solutions/{category}/{source.stem}"
            if category == "system-design":
                solution += ".md"
            problems.append({
                "id": problem_id,
                "category": category,
                "number": number,
                "slug": slug,
                "title": headings[0][len(prefix):].strip(),
                "difficulty": difficulties[0],
                "source_path": source_path,
                "starter_path": starter,
                "solution_path": resource_path(root, source, text, "Reference Solution", solution, directory=category != "system-design"),
            })
    return {"schema_version": 1, "problems": problems}


def render_manifest(manifest):
    """Stable UTF-8 JSON with a final newline and no timestamps or absolute paths."""
    return json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repository root (defaults to this script's repository)")
    parser.add_argument("--output", type=Path, help="output JSON (defaults to <root>/scripts/problem-manifest.json)")
    parser.add_argument("--check", action="store_true", help="validate sources and fail if the output is missing or stale; do not write")
    args = parser.parse_args()
    output = args.output if args.output is not None else args.root / "scripts/problem-manifest.json"
    try:
        rendered = render_manifest(generate_manifest(args.root)).encode("utf-8")
        if args.check:
            if not output.is_file():
                raise ManifestError(f"manifest missing: {output}; run the generator")
            if output.read_bytes() != rendered:
                raise ManifestError(f"manifest stale: {output}; run the generator")
            print("Manifest current: 65 problems (25 round-1, 25 round-2, 15 system-design)")
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(rendered)
            print(f"Wrote 65 problems to {output}")
    except (ManifestError, OSError, ValueError) as error:
        print(f"Manifest error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
