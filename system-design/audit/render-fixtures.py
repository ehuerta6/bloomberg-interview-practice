#!/usr/bin/env python3
"""Render the 15 prompts and 15 references for a local, category-only audit."""

import argparse
from html import escape
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from site_renderer import render_markdown


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="external directory for disposable browser fixtures")
    output = parser.parse_args().output.resolve()
    if output.is_relative_to(ROOT):
        parser.error("use an output directory outside the checkout")
    output.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "docs/assets", output / "assets", dirs_exist_ok=True)
    shutil.copy(ROOT / "scripts/site/mermaid.mjs", output / "mermaid.mjs")
    paths = []
    for folder, kind in (("system-design", "prompt"), ("solutions/system-design", "solution")):
        sources = sorted((ROOT / folder).glob("[0-9][0-9]-*.md"))
        if len(sources) != 15:
            raise ValueError(f"expected 15 {kind}s, found {len(sources)}")
        for source in sources:
            text = source.read_text(encoding="utf-8")
            body = render_markdown(text, source.relative_to(ROOT), ROOT, {})
            name = f"{kind}-{source.stem}.html"
            script = '<script type="module" src="mermaid.mjs"></script>' if kind == "solution" else ""
            page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(source.stem)} · {kind} audit</title><link rel="stylesheet" href="assets/site.css">{script}</head>
<body><main class="container"><article class="prose">{body}</article></main></body></html>
'''
            (output / name).write_text(page, encoding="utf-8")
            paths.append(name)
    print(f"Rendered {len(paths)} audit pages in {output}")


if __name__ == "__main__":
    main()
