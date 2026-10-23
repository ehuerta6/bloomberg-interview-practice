#!/usr/bin/env python3
"""Export one coding starter as a deterministic ZIP (Python 3.9+ and Git).

Usage: python3 scripts/export-exercise.py round-1-01
       python3 scripts/export-exercise.py round-2-01 --output /tmp/practice.zip

Extract the ZIP, then run Python tests from the selected exercise directory.
Starter bugs and failing tests are preserved. Only tracked Python files and
AGENTS.md policies are copied; assignments and reference solutions are omitted.
The default destination is the Git-ignored .local-context/exports/<id>.zip.
Existing outputs are never overwritten. Source bytes come from the working tree,
so export from a clean checkout when distributing the original starter.
"""

import argparse
import io
import json
from pathlib import Path
import re
import subprocess
import sys
from zipfile import ZIP_STORED, ZipFile, ZipInfo


DEFAULT_ROOT = Path(__file__).resolve().parents[1]


class ExportError(ValueError):
    """The selection cannot be exported without leaving its starter boundary."""


def read_regular_file(root, relative):
    """Reject links in every component before reading a repository file."""
    path = root
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ExportError(f"symlinks are not exportable: {relative}")
    if not path.is_file():
        raise ExportError(f"missing regular file: {relative}")
    return path.read_bytes()


def export_exercise(root, problem_id, output):
    root = root.resolve()
    match = re.fullmatch(r"(round-[12])-([0-9]{2})", problem_id)
    if not match:
        raise ExportError("select a coding exercise ID, e.g. round-1-01 or round-2-01")
    manifest = json.loads(read_regular_file(root, Path("scripts/problem-manifest.json")))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ExportError("expected manifest schema_version 1")
    problems = manifest.get("problems")
    if not isinstance(problems, list) or any(not isinstance(p, dict) for p in problems):
        raise ExportError("manifest problems must be an array of objects")
    selected = [p for p in problems if p.get("id") == problem_id]
    if len(selected) != 1:
        raise ExportError(f"expected exactly one manifest entry for {problem_id}")
    problem = selected[0]
    category, number = match.groups()
    starter_path = problem.get("starter_path")
    expected = rf"{category}/{number}-[a-z0-9]+(?:-[a-z0-9]+)*"
    if (problem.get("category") != category or not isinstance(starter_path, str)
            or not re.fullmatch(expected, starter_path)):
        raise ExportError(f"invalid starter_path for {problem_id}")
    starter = Path(starter_path)
    # Git's index excludes scratch files and generated artifacts. Restrict the
    # index further to this bank's flat Python starters and local policy.
    tracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "-z", "--", starter_path],
        check=True, capture_output=True,
    ).stdout.decode("utf-8").split("\0")
    files = {Path("AGENTS.md")}
    for name in filter(None, tracked):
        path = Path(name)
        if path.parent == starter and (path.suffix == ".py" or path.name == "AGENTS.md"):
            files.add(path)
    if not any(path.suffix == ".py" for path in files):
        raise ExportError(f"no tracked Python starter files: {starter_path}")
    archive = io.BytesIO()
    with ZipFile(archive, "w", compression=ZIP_STORED) as package:
        for path in sorted(files, key=lambda path: path.as_posix()):
            info = ZipInfo(path.as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            package.writestr(info, read_regular_file(root, path))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("xb") as destination:
        destination.write(archive.getvalue())
    return len(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("exercise_id", help="manifest ID: round-1-01 through round-1-25, or round-2-01 through round-2-25")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="repository root (defaults to this script's repository)")
    parser.add_argument("--output", type=Path, help="ZIP destination; relative paths use the current directory")
    args = parser.parse_args()
    output = args.output if args.output is not None else args.root / ".local-context/exports" / f"{args.exercise_id}.zip"
    try:
        count = export_exercise(args.root, args.exercise_id, output)
    except (ExportError, OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Export error: {error}", file=sys.stderr)
        return 1
    print(f"Exported {args.exercise_id}: {count} files to {output}")
    print("Extract the ZIP and run the tests from the selected exercise directory; starter failures are expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
