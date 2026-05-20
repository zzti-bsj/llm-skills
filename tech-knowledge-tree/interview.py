#!/usr/bin/env python3
"""Interview question manager for tech-knowledge-tree skill.

Usage:
    interview.py add <title> <tags> <category> <difficulty>
    interview.py set-difficulty <title> <difficulty>
"""

import argparse
import csv
import os
import sys
from pathlib import Path

FIELDNAMES = ["title", "tags", "category", "difficulty"]


def get_docs_root() -> Path:
    """Get knowledge tree root from TECH_DOCS_PATH env var."""
    return Path(os.environ.get("TECH_DOCS_PATH", os.path.expanduser("~/Project/docs")))


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


def cmd_add(args):
    """Add a single interview question to CSV."""
    root = get_docs_root()
    csv_path = root / "questions.csv"

    existing_titles = load_existing_titles(csv_path)
    if args.title in existing_titles:
        print(f"Duplicate (skipped): {args.title[:60]}...")
        return

    file_exists = csv_path.exists()
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "title": args.title,
            "tags": args.tags,
            "category": args.category,
            "difficulty": args.difficulty,
        })

    print(f"Added: {args.title[:60]}...")


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

    print(f"Updated difficulty for: {args.title[:60]}...")


def main():
    parser = argparse.ArgumentParser(description="Interview question manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add an interview question")
    add_parser.add_argument("title", help="Question title")
    add_parser.add_argument("tags", help="Tags (direct parent dir name)")
    add_parser.add_argument("category", help="Category (top-level dir name)")
    add_parser.add_argument("difficulty", help="Difficulty level")

    diff_parser = subparsers.add_parser("set-difficulty", help="Set difficulty for a question")
    diff_parser.add_argument("title", help="Question title to update")
    diff_parser.add_argument("difficulty", help="Difficulty level")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args)
    elif args.command == "set-difficulty":
        cmd_set_difficulty(args)


if __name__ == "__main__":
    main()
