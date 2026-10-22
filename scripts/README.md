# Canonical problem manifest

Generate the inventory with Python 3.9 or later, using only the standard library:

```sh
python3 scripts/generate_manifest.py
python3 scripts/generate_manifest.py --check
python3 -m unittest discover -s scripts -p 'test_manifest.py' -v
```

The first command writes `scripts/problem-manifest.json`. The second validates
all sources and fails if the committed artifact is missing or stale, without
writing it. Both commands work from any directory when given the script's path.
`--root` selects another repository root; `--output` selects another JSON file.
An explicit relative output path is relative to the current working directory.

Edit the existing Markdown and exercise files, then regenerate the manifest.
Do not hand-edit the JSON. The generator reads the 25 problem files in each of
`problems/round-1/` and `problems/round-2/`, plus the 15 numbered Markdown files in
`system-design/`. Category README files are excluded. Titles and difficulty come
from each problem's heading and difficulty line. Resource paths come from its
Starter Code and Reference Solution links. The generator reads no solution
content and copies no assignment text into the manifest.

## Schema version 1

The top-level object has `schema_version: 1` and a `problems` array. This committed
shape is the contract for the exporter and site generator. Each entry has:

| Field | Meaning |
|---|---|
| `id` | Category plus two-digit number, for example `round-1-01`. |
| `category` | Canonical source category: `round-1`, `round-2`, or `system-design`. |
| `number` | Integer number within its category. |
| `slug` | Category plus numbered source filename stem, for example `round-1-01-code-validator`. |
| `title` | Problem heading with its `PR #01 —`, `Ticket #01 —`, or `Problem 01 —` prefix removed. |
| `difficulty` | Source value, one of `Easy`, `Medium`, or `Hard`. |
| `source_path` | Repository-relative Markdown file path. |
| `starter_path` | Repository-relative coding exercise directory; `null` for System Design. |
| `solution_path` | Repository-relative coding reference directory or System Design reference Markdown file. |

All paths use POSIX separators, with no leading slash or trailing directory
slash. Consumers resolve them against the repository root. `solution_path` is
reference metadata; consumers should keep opening reference content an explicit
learner choice.

Entries are ordered by `round-1`, `round-2`, then `system-design`, and by number
within each category. IDs and slugs do not depend on display titles. Renaming a
numbered source file changes its slug; changing its category or number changes
its ID. Keep those filenames stable when editing problem wording.

The generator requires exact 25/25/15 counts, contiguous category numbers,
unique IDs/slugs/source paths, valid filename/heading metadata, and existing
resource links that point to the matching exercise. It rejects external links,
repository escapes, wrong resource types, and mismatched exercise targets.
Serialization uses UTF-8, two-space indentation and a final newline, without
timestamps or machine-specific paths.
