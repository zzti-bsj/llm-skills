#!/usr/bin/env python3
"""Interview question extractor for tech-knowledge-tree skill.

Usage:
    interview.py scan [--topic <topic>]
    interview.py set-difficulty <title> <difficulty>
"""

import argparse
import csv
import os
import sys
from pathlib import Path


def get_docs_root() -> Path:
    """Get knowledge tree root from TECH_DOCS_PATH env var."""
    return Path(os.environ.get("TECH_DOCS_PATH", os.path.expanduser("~/Project/docs")))


def extract_title(filepath: Path) -> str:
    """Extract title from first non-empty line of a deepen document.

    Deepen docs open with a conclusion statement that serves as the question.
    Skips markdown headings (lines starting with #) to get the actual content.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped and not stripped.startswith("#"):
                return stripped.rstrip("。！？") + "？"
    return filepath.stem


def derive_tags(deepen_dir: Path, root: Path) -> str:
    """Derive tags from direct parent directory name of the deepen directory.

    Example: root/authentication/jwt/deepen/ -> 'jwt'
    """
    parent = deepen_dir.parent
    return parent.name


def derive_category(deepen_dir: Path, root: Path) -> str:
    """Derive category from top-level directory name.

    Example: root/authentication/jwt/deepen/ -> 'authentication'
    """
    try:
        return deepen_dir.relative_to(root).parts[0]
    except ValueError:
        return ""


def find_deepen_dirs(root: Path, topic: str | None = None) -> list[Path]:
    """Find all deepen/ directories, optionally filtered by topic."""
    deepen_dirs = []
    if topic:
        # Search for a directory named <topic> anywhere under root
        for dirpath, dirnames, filenames in os.walk(root):
            if os.path.basename(dirpath) == topic or dirpath.endswith(f"/{topic}"):
                candidate = Path(dirpath) / "deepen"
                if candidate.is_dir():
                    deepen_dirs.append(candidate)
    else:
        for dirpath, dirnames, filenames in os.walk(root):
            if os.path.basename(dirpath) == "deepen":
                deepen_dirs.append(Path(dirpath))
    return deepen_dirs


def load_existing_titles(csv_path: Path) -> set[str]:
    """Load existing titles from CSV for dedup."""
    if not csv_path.exists():
        return set()
    titles = set()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            titles.add(row["title"])
    return titles


def cmd_scan(args):
    """Scan deepen directories and append new questions to CSV."""
    root = get_docs_root()
    csv_path = root / "questions.csv"

    deepen_dirs = find_deepen_dirs(root, args.topic)
    if not deepen_dirs:
        print(f"No deepen directories found{' for topic: ' + args.topic if args.topic else ''}.")
        return

    existing_titles = load_existing_titles(csv_path)
    new_entries = []

    for deepen_dir in deepen_dirs:
        tags = derive_tags(deepen_dir, root)
        category = derive_category(deepen_dir, root)

        for md_file in sorted(deepen_dir.glob("*.md")):
            title = extract_title(md_file)
            if title in existing_titles:
                continue

            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read().strip()

            new_entries.append({
                "title": title,
                "content": content,
                "tags": tags,
                "category": category,
                "difficulty": "",
            })
            existing_titles.add(title)

    if not new_entries:
        print("No new interview questions found.")
        return

    file_exists = csv_path.exists()
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        fieldnames = ["title", "content", "tags", "category", "difficulty"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerows(new_entries)

    print(f"Added {len(new_entries)} interview question(s) to {csv_path}")


def cmd_set_difficulty(args):
    """Set difficulty for a specific question by title."""
    root = get_docs_root()
    csv_path = root / "questions.csv"

    if not csv_path.exists():
        print(f"No questions.csv found at {csv_path}")
        sys.exit(1)

    rows = []
    updated = False
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row["title"] == args.title:
                row["difficulty"] = args.difficulty
                updated = True
            rows.append(row)

    if not updated:
        print(f"Title not found: {args.title}")
        sys.exit(1)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Updated difficulty for: {args.title}")


def main():
    parser = argparse.ArgumentParser(description="Interview question extractor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan deepen docs and extract questions")
    scan_parser.add_argument("--topic", help="Only scan a specific topic")

    diff_parser = subparsers.add_parser("set-difficulty", help="Set difficulty for a question")
    diff_parser.add_argument("title", help="Question title to update")
    diff_parser.add_argument("difficulty", help="Difficulty level")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "set-difficulty":
        cmd_set_difficulty(args)


if __name__ == "__main__":
    main()
