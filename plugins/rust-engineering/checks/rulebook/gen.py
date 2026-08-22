#!/usr/bin/env python3
"""Generate only explicitly classified rulebook examples into a temp tree."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parents[1]
RULES = PLUGIN / "skills" / "rust-coding-rules" / "references" / "rules"
ANNOTATION = re.compile(
    r"<!--\s*rust-example:\s*(standalone|fixture|compile_fail|fragment)\s*(?:;\s*(.*?))?\s*-->"
)


def parse_attributes(kind: str, raw: str, path: Path, line: int) -> dict[str, object]:
    values: dict[str, object] = {}
    for part in (piece.strip() for piece in raw.split(";") if piece.strip()):
        if ":" in part and "=" not in part.split(":", 1)[0]:
            key, value = part.split(":", 1)
        elif "=" in part:
            key, value = part.split("=", 1)
        else:
            raise ValueError(f"invalid annotation attribute in {path}:{line}: {part}")
        values[key.strip()] = value.strip().strip('"')
    if kind == "fragment" and not values.get("missing"):
        raise ValueError(f"fragment lacks missing context in {path}:{line}")
    if kind == "fixture":
        dependencies = [item.strip() for item in str(values.get("dependencies", "")).split(",") if item.strip()]
        if not dependencies:
            raise ValueError(f"fixture lacks dependencies in {path}:{line}")
        values["dependencies"] = dependencies
    if kind == "compile_fail":
        if values.get("harness") not in {"rustc", "cargo"} or not values.get("expected"):
            raise ValueError(f"compile_fail lacks harness or expected diagnostic in {path}:{line}")
    return values


def examples(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    found: list[dict[str, object]] = []
    section = ""
    rust_ordinal = 0
    index = 0
    while index < len(lines):
        heading = re.match(r"^##+\s+(.+)$", lines[index])
        if heading:
            section = heading.group(1)
        if lines[index].strip() != "```rust":
            index += 1
            continue
        previous = lines[index - 1].strip() if index else ""
        match = ANNOTATION.fullmatch(previous)
        if not match:
            raise ValueError(f"unclassified Rust block in {path}:{index + 1}")
        end = index + 1
        while end < len(lines) and lines[end].strip() != "```":
            end += 1
        if end == len(lines):
            raise ValueError(f"unclosed Rust block in {path}:{index + 1}")
        kind = match.group(1)
        found.append(
            {
                "rule_id": path.stem,
                "ordinal": rust_ordinal,
                "line": index + 1,
                "section": section,
                "kind": kind,
                "attributes": parse_attributes(kind, match.group(2) or "", path, index + 1),
                "code": "\n".join(lines[index + 1 : end]).rstrip() + "\n",
            }
        )
        rust_ordinal += 1
        index = end + 1
    return found


def copy_harness(output: Path) -> None:
    shutil.copy2(HERE / "Cargo.toml", output / "Cargo.toml")
    shutil.copy2(HERE / "Cargo.lock", output / "Cargo.lock")
    (output / "src").mkdir(parents=True)
    shutil.copy2(HERE / "src" / "lib.rs", output / "src" / "lib.rs")


def generate(rule_id: str | None, output: Path) -> None:
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"output directory must be empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    paths = [RULES / f"{rule_id}.md"] if rule_id else sorted(RULES.glob("*.md"))
    if not paths or any(not path.is_file() for path in paths):
        raise SystemExit(f"unknown rule: {rule_id}")
    records = [record for path in paths for record in examples(path)]
    copy_harness(output)
    for directory in ("standalone", "compile_fail", "examples"):
        (output / directory).mkdir()
    for record in records:
        kind = str(record["kind"])
        if kind == "fragment":
            continue
        stem = f"{str(record['rule_id']).replace('-', '_')}__{record['ordinal']}"
        directory = "examples" if kind == "fixture" else kind
        (output / directory / f"{stem}.rs").write_text(str(record["code"]), encoding="utf-8")
        record["generated"] = f"{directory}/{stem}.rs"
    serializable = [{key: value for key, value in record.items() if key != "code"} for record in records]
    counts = Counter(str(record["kind"]) for record in records)
    manifest = {
        "rules": len(paths),
        "examples": len(records),
        "counts": dict(sorted(counts.items())),
        "records": serializable,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        f"generated {len(records)} classified blocks from {len(paths)} rule(s): "
        + ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--rule")
    selection.add_argument("--all", action="store_true")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    generate(args.rule, args.out.resolve())


if __name__ == "__main__":
    main()
