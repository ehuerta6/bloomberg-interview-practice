# Static problem pages

The 65 problem Markdown files remain the maintained assignment sources. The
site generator reads `scripts/problem-manifest.json`, validates it against the
source bank, and renders one HTML page per manifest entry. Edit Markdown, then
regenerate; do not edit generated HTML.

Use Python 3.10 or later. Install the two pinned build dependencies in a virtual
environment outside the checkout, then run from the repository root:

```sh
python3 -m venv /tmp/bloomberg-site-venv
/tmp/bloomberg-site-venv/bin/python -m pip install -r scripts/build-site-requirements.txt
/tmp/bloomberg-site-venv/bin/python scripts/build-site.py
/tmp/bloomberg-site-venv/bin/python scripts/build-site.py --check
/tmp/bloomberg-site-venv/bin/python -m unittest discover -s scripts -p 'test_build_site.py' -v
```

If the manifest is stale after metadata changes, first run
`python3 scripts/generate_manifest.py`. The site builder never updates it.
Commands accept `--root PATH` and `--output PATH`; defaults are this script's
repository and `<root>/docs`. An explicit relative output directory is relative
to the current working directory. Invocation works from any working directory.
`--check` compares bytes and detects missing, changed, or obsolete pages without
writing. Generation uses no timestamps, absolute output paths, or build-time
network requests. Identical sources and pinned dependencies produce identical
output bytes. Old pages bearing the generator marker are removed; unexpected
unowned HTML files in `docs/problems/` cause an error.

## Output contract

- `docs/problems/<manifest slug>.html`: 25 Round 1, 25 Round 2, 15 System Design.
- `docs/renderer/mermaid.mjs`: generated copy of `scripts/site/mermaid.mjs`.
- Shared CSS and logo: `../assets/site.css`, `../assets/cic-logo.png` from each
  problem page. Shared assets are maintained separately and never overwritten.
- Catalog navigation: `../index.html`, supplied by the catalog feature.

The generator owns only problem pages and the Mermaid module. It preserves
catalog, export, and shared asset files. `scripts/site/page.html` is the common
template; `scripts/site_renderer.py` renders Markdown. The manifest and all
assignment, starter, and reference solution files remain untouched.

CommonMark headings, paragraphs, lists, blockquotes, inline/fenced code, links,
images, tables, and strikethrough are supported. Heading IDs use a `heading-`
prefix and unique suffixes. In-page and cross-problem fragment links use the same
prefix. Relative links to another generated problem point to its local HTML.
Other repository links resolve against the Markdown source directory to GitHub
`main` (`tree` for directories, `blob` for files, `raw` for images). Thus starter
and solution links keep working when only `docs/` is hosted, and viewing a
reference remains an explicit link choice. Query strings and external fragments
are preserved. Missing local targets or links escaping the repository fail the
build. GitHub resource links follow `main`, independently of a deployed snapshot.

## HTML and Mermaid safety

Raw Markdown HTML is escaped. The Markdown parser blocks executable URLs; the
site further restricts links to HTTP, HTTPS, mailto, and repository/fragment
destinations. Template metadata and Mermaid source are escaped before insertion.
Ordinary fenced code stays text; no frontend framework or syntax highlighter is
required.

Only pages with Mermaid fences load the local renderer module and download the
exact pinned Mermaid 12.2.0 ES module
from jsDelivr at viewing time. Rendering uses strict security, text labels,
bounded diagram size, no click callback binding, and locked security settings.
Diagram configuration directives and frontmatter are refused; site configuration
belongs in the module. A successfully rendered diagram retains its original text
under a “Diagram source” disclosure. Invalid diagrams, refused configuration,
JavaScript being disabled, or CDN/network failure leave escaped source readable.
The HTML build is reproducible offline after dependency installation; SVG
rendering requires JavaScript and network access to the pinned CDN dependency.

`scripts/site/fixtures/renderer.md` exercises formats and hostile input without
changing assignments. The unit suite checks that fixture, links, escaping,
Mermaid source handling, page counts, deterministic output, stale checks, and
preservation of adjacent site files. Browser checks should additionally confirm
SVG rendering and the source fallback when the CDN is blocked.

Serve `docs/` for a local browser check:

```sh
python3 -m http.server 8000 --directory docs
# Open http://localhost:8000/problems/round-1-01-code-validator.html
```
