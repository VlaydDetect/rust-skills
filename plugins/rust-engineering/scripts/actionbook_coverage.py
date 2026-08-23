#!/usr/bin/env python3
"""Create and update the pinned Actionbook source ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
REPOSITORY = PLUGIN.parents[1]
SOURCE = REPOSITORY / "references" / "rust-skills_actionbook"
LEDGER = PLUGIN / "provenance" / "actionbook-coverage.json"
STATUSES = {"pending", "in_progress", "adapted", "merged", "conditional", "excluded"}


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(SOURCE).parts
        and "graphify-out" not in path.relative_to(SOURCE).parts
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int | None:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return None


def refresh_summary(data: dict) -> None:
    counts = Counter(entry["status"] for entry in data["entries"])
    data["summary"] = {
        "source_files": len(data["entries"]),
        **{status: counts[status] for status in sorted(STATUSES)},
    }


def initialize(force: bool) -> None:
    if LEDGER.exists() and not force:
        raise SystemExit(f"ledger already exists: {LEDGER}")
    entries = []
    for path in source_files():
        entries.append(
            {
                "source_path": path.relative_to(SOURCE).as_posix(),
                "source_sha256": digest(path),
                "source_lines": line_count(path),
                "source_bytes": path.stat().st_size,
                "status": "pending",
                "target_paths": [],
                "baseline_action": "pending",
                "reason": "Awaiting one-file Actionbook review.",
            }
        )
    data = {
        "schema_version": 1,
        "source": {
            "name": "actionbook/rust-skills",
            "relative_path": "references/rust-skills_actionbook",
            "revision": "fa60f7931223646fb71c4586b4a6c8545016076a",
            "commit_date": "2026-05-25T07:33:30+08:00",
            "version_file": "2.0.9",
            "plugin_manifest_version": "2.1.0",
            "license_declared": "MIT",
            "standalone_license_file": False,
        },
        "statuses": sorted(STATUSES),
        "summary": {},
        "entries": entries,
    }
    refresh_summary(data)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def mark(args: argparse.Namespace) -> None:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    matches = [entry for entry in data["entries"] if entry["source_path"] == args.source_path]
    if len(matches) != 1:
        raise SystemExit(f"expected one ledger entry for {args.source_path!r}, found {len(matches)}")
    entry = matches[0]
    entry.update(
        status=args.status,
        target_paths=args.target,
        baseline_action=args.baseline_action,
        reason=args.reason,
    )
    refresh_summary(data)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    init = subparsers.add_parser("init")
    init.add_argument("--force", action="store_true")
    update = subparsers.add_parser("mark")
    update.add_argument("source_path")
    update.add_argument("--status", choices=sorted(STATUSES - {"pending", "in_progress"}), required=True)
    update.add_argument("--target", action="append", default=[])
    update.add_argument("--baseline-action", required=True)
    update.add_argument("--reason", required=True)
    args = parser.parse_args()
    if args.command == "init":
        initialize(args.force)
    else:
        mark(args)


if __name__ == "__main__":
    main()
