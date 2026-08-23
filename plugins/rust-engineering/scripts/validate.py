#!/usr/bin/env python3
"""Validate the dual-host Rust engineering plugin with the standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
import huiali_coverage as huiali


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
AGENTS = {"rust-scout", "rust-researcher", "rust-reviewer", "rust-verifier"}
ENTRY_SKILLS = {"rust-workflow", "rust-review", "rust-verify"}
RULEBOOK_SKILL = "rust-coding-rules"
ACTIONBOOK_SKILLS = {"rust-design-protocol", "rust-research"}
HU_NEW_SKILLS = {"rust-pin", "rust-gpu", "rust-systems-networking", "rust-distributed-systems"}
HU_KINDS = {"new_profile": 16, "merged": 16, "conflict": 8, "negative": 8}
HU_BLOCK_MARKER = re.compile(r"<!-- huiali-source: .*; sha256=([0-9a-f]{64}) -->")
ACTIONBOOK_STATUSES = {"pending", "in_progress", "adapted", "merged", "conditional", "excluded"}
ACTIONBOOK_KINDS = {
    "model_routing": 14,
    "cross_layer": 8,
    "navigation": 6,
    "research_dynamic": 6,
    "unsafe": 6,
    "ml": 2,
    "negative": 2,
}
ACTIONBOOK_REFERENCES = {
    "m01-ownership", "m02-resource", "m03-mutability", "m04-zero-cost",
    "m05-type-driven", "m06-error-handling", "m07-concurrency", "m09-domain",
    "m10-performance", "m11-ecosystem", "m12-lifecycle", "m13-domain-error",
    "m14-mental-model", "m15-anti-pattern", "cognitive-protocol", "domain-iot",
    "domain-embedded", "domain-cloud-native", "domain-ml", "rust-code-navigator",
    "rust-symbol-analyzer", "rust-trait-explorer", "rust-deps-visualizer",
    "rust-call-graph", "rust-refactor-helper", "rust-learner",
    "core-dynamic-skills", "rust-daily", "unsafe-checker",
}
RULE_CATEGORIES = {
    "own": {"rust-ownership"},
    "err": {"rust-errors"},
    "mem": {"rust-performance"},
    "unsafe": {"rust-unsafe"},
    "api": {"rust-api-design"},
    "async": {"rust-concurrency"},
    "conc": {"rust-concurrency"},
    "opt": {"rust-performance"},
    "num": {"rust-idioms"},
    "type": {"rust-traits"},
    "trait": {"rust-traits"},
    "conv": {"rust-api-design"},
    "const": {"rust-stable"},
    "serde": {"rust-api-design"},
    "pat": {"rust-idioms"},
    "macro": {"rust-macros"},
    "closure": {"rust-traits"},
    "coll": {"rust-stdlib"},
    "name": {"rust-api-design", "rust-style-clippy"},
    "test": {"rust-testing"},
    "doc": {"rust-documentation"},
    "obs": {"rust-observability"},
    "perf": {"rust-performance"},
    "proj": {"rust-module-layout", "rust-workspace", "rust-cargo-build", "rust-stable"},
    "lint": {"rust-style-clippy"},
    "anti": {"rust-idioms"},
}
RULE_STATUSES = {"pending", "in_progress", "adapted", "conditional", "alias", "rejected"}
RULE_SECTIONS = {
    "Decision", "Apply When", "Avoid When", "Algorithm", "Bad", "Good",
    "Trade-offs", "Prerequisites", "Verification", "Related Rules",
}
RULE_EXAMPLE = re.compile(
    r"<!--\s*rust-example:\s*(standalone|fixture|compile_fail|fragment)\s*(?:;\s*(.*?))?\s*-->"
)
EXPECTED_ALIASES = {
    "anti-clone-excessive": "own-borrow-over-clone",
    "anti-collect-intermediate": "perf-collect-once",
    "anti-expect-lazy": "err-expect-bugs-only",
    "anti-format-hot-path": "mem-write-over-format",
    "anti-index-over-iter": "perf-iter-over-index",
    "anti-lock-across-await": "async-no-lock-await",
    "anti-panic-expected": "err-result-over-panic",
    "anti-premature-optimize": "perf-profile-first",
    "anti-string-for-str": "own-slice-over-vec",
    "anti-vec-for-slice": "own-slice-over-vec",
    "anti-stringly-typed": "type-no-stringly",
    "anti-type-erasure": "trait-dyn-vs-generic",
    "anti-unwrap-abuse": "err-no-unwrap-prod",
    "err-doc-errors": "doc-errors-section",
    "doc-link-types": "doc-intra-links",
    "name-iter-method": "name-iter-convention",
}
DISALLOWED_HOOK_COMMANDS = re.compile(
    r"\bcargo\s+(?:fmt|test|check|clippy|build|run|update|fetch|install|publish|bench|doc|fix)\b"
    r"|\bnix\s+(?:build|flake\s+(?:check|update)|develop)\b"
    r"|\b(?:curl|wget|Invoke-WebRequest)\b",
    re.IGNORECASE,
)
OFFLINE_CACHE_MISS = re.compile(
    r"no matching package named|failed to download|attempting to make an HTTP request.*offline|"
    r"not found in package cache|was not found in the cache|could not find.*registry",
    re.IGNORECASE | re.DOTALL,
)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and lines[0] == "---", f"missing frontmatter: {path}"
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise AssertionError(f"unclosed frontmatter: {path}") from error
    values = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, separator, value = line.partition(":")
        assert separator and key and value.strip(), f"invalid frontmatter line in {path}: {line!r}"
        values[key.strip()] = value.strip().strip('"')
    return values


def validate_links() -> None:
    link = re.compile(r"\[[^]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        for target in link.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative:
                continue
            if (
                "::" in relative
                or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:<[^>]+>)?", relative)
                or re.fullmatch(r"(?:fn|struct|enum|trait|type|macro|mod|const|static|method|prim)@[A-Za-z_][A-Za-z0-9_]*", relative)
            ):
                continue  # Rust intra-doc item target, not a filesystem path.
            target_path = (path.parent / relative).resolve()
            assert target_path.exists(), f"broken link in {path}: {target}"


def validate_manifests() -> None:
    claude = load_json(ROOT / ".claude-plugin" / "plugin.json")
    codex = load_json(ROOT / ".codex-plugin" / "plugin.json")
    assert (ROOT / "LICENSE").is_file()
    assert claude["name"] == codex["name"] == "rust-engineering"
    assert claude["version"] == codex["version"] == "0.5.0"
    assert re.fullmatch(r"\d+\.\d+\.\d+", claude["version"])
    assert tuple(map(int, claude["version"].split("."))) >= (0, 2, 0)
    assert claude["author"]["name"] and codex["author"]["name"]
    assert all(isinstance(keyword, str) and keyword for keyword in claude["keywords"])
    assert all(isinstance(keyword, str) and keyword for keyword in codex["keywords"])
    assert "50" in claude["description"] and "265" in claude["description"] and "Huiali" in claude["description"]
    assert "50" in codex["description"] and "265" in codex["description"] and "Huiali" in codex["description"]
    assert set(claude) <= {
        "$schema", "name", "version", "description", "author", "license", "keywords", "hooks",
    }
    assert claude["hooks"] == "./hooks/claude.json"
    assert (ROOT / claude["hooks"]).is_file()
    assert codex["skills"] == "./skills/"
    assert "hooks" not in codex
    interface = codex["interface"]
    assert interface["displayName"] and interface["shortDescription"] and interface["longDescription"]
    assert "265" in interface["longDescription"]
    assert "Actionbook" in interface["longDescription"]
    assert "Huiali" in interface["longDescription"]
    assert interface["defaultPrompt"] and "$rust-workflow" in interface["defaultPrompt"][0]
    assert "$rust-coding-rules" in interface["defaultPrompt"][0]

    assert not list(ROOT.rglob(".mcp.json")), "Huiali integration must not add MCP configuration"
    assert not list(ROOT.rglob(".app.json")), "Huiali integration must not add app configuration"
    assert not any((ROOT / name).exists() for name in ("Cargo.toml", "package.json", "pyproject.toml", "requirements.txt")), (
        "plugin runtime must not gain a package/dependency manifest"
    )

    unwanted = [
        path for path in ROOT.rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc" or (path.is_dir() and path.name == "target")
    ]
    assert not unwanted, f"generated build artifacts in plugin: {unwanted}"


def validate_source_coverage() -> tuple[dict, set[str], set[str]]:
    coverage = load_json(ROOT / "provenance" / "source-coverage.json")
    assert coverage["schema_version"] == 1
    entries = coverage["entries"]
    assert len(entries) == coverage["summary"]["source_skills"] == 61
    assert sum(entry["status"] == "adapted" for entry in entries) == coverage["summary"]["adapted"] == 46
    assert sum(entry["status"] == "out-of-scope" for entry in entries) == coverage["summary"]["out_of_scope"] == 15
    assert sum(len(entry["support_files"]) for entry in entries) == coverage["summary"]["support_files"] == 385

    source_keys = [(entry["source"], entry["source_skill"]) for entry in entries]
    assert len(source_keys) == len(set(source_keys)), "duplicate source coverage entries"
    owners = {entry["knowledge_owner"] for entry in entries if entry["status"] == "adapted"}
    assert None not in owners and len(owners) == 41, f"expected 41 source-derived owners, got {len(owners)}"
    targets = owners | {target for entry in entries for target in entry["supporting_targets"]}
    assert targets <= owners | {"rust-workflow", "rust-verify"}
    for entry in entries:
        if entry["status"] == "adapted":
            assert entry["knowledge_owner"] and entry["coverage_notes"] and not entry["exclusion_reason"]
        else:
            assert not entry["knowledge_owner"] and entry["exclusion_reason"]

    # The plugin remains standalone. Verify pinned comparative evidence only when
    # the source corpora are present in this development repository.
    for source_name, source in coverage["sources"].items():
        source_root = REPOSITORY / source["relative_path"]
        if not source_root.exists():
            continue
        actual_names = {path.name for path in source_root.iterdir() if path.is_dir()}
        recorded_names = {entry["source_skill"] for entry in entries if entry["source"] == source_name}
        assert actual_names == recorded_names, f"source skill drift in {source_name}"
        for entry in (item for item in entries if item["source"] == source_name):
            skill_root = source_root / entry["source_skill"]
            skill_md = skill_root / "SKILL.md"
            assert sha256(skill_md) == entry["skill_md"]["sha256"], f"source changed: {skill_md}"
            for support in entry["support_files"]:
                path = skill_root / support["path"]
                assert path.is_file() and sha256(path) == support["sha256"], f"source changed: {path}"

    example_owners = {
        entry["knowledge_owner"]
        for entry in entries
        if entry["status"] == "adapted"
        and any(re.match(r"examples/golden[^/]*/Cargo\.toml$", item["path"]) for item in entry["support_files"])
    }
    return coverage, owners, example_owners


def validate_actionbook_coverage(skills: set[str]) -> dict:
    coverage = load_json(ROOT / "provenance" / "actionbook-coverage.json")
    assert coverage["schema_version"] == 1
    source = coverage["source"]
    assert source == {
        "name": "actionbook/rust-skills",
        "relative_path": "references/rust-skills_actionbook",
        "revision": "fa60f7931223646fb71c4586b4a6c8545016076a",
        "commit_date": "2026-05-25T07:33:30+08:00",
        "version_file": "2.0.9",
        "plugin_manifest_version": "2.1.0",
        "license_declared": "MIT",
        "standalone_license_file": False,
    }
    assert set(coverage["statuses"]) == ACTIONBOOK_STATUSES
    entries = coverage["entries"]
    assert len(entries) == 242
    paths = [entry["source_path"] for entry in entries]
    assert len(paths) == len(set(paths)), "duplicate Actionbook source paths"
    counts = Counter(entry["status"] for entry in entries)
    assert coverage["summary"] == {
        "source_files": 242,
        **{status: counts[status] for status in sorted(ACTIONBOOK_STATUSES)},
    }
    unfinished = [entry["source_path"] for entry in entries if entry["status"] in {"pending", "in_progress"}]
    assert not unfinished, f"unfinished Actionbook entries: {unfinished[:10]}"

    for entry in entries:
        assert entry["status"] in ACTIONBOOK_STATUSES
        assert entry["baseline_action"] and entry["reason"]
        targets = entry["target_paths"]
        if entry["status"] == "excluded":
            assert not targets, f"excluded Actionbook entry has target: {entry['source_path']}"
        else:
            assert targets, f"integrated Actionbook entry has no target: {entry['source_path']}"
        for target in targets:
            target_path = ROOT / target
            assert target_path.is_file(), f"missing Actionbook target: {target_path}"

    source_root = REPOSITORY / source["relative_path"]
    if source_root.exists():
        actual = sorted(
            path for path in source_root.rglob("*")
            if path.is_file()
            and ".git" not in path.relative_to(source_root).parts
            and "graphify-out" not in path.relative_to(source_root).parts
        )
        assert len(actual) == 242, "Actionbook source inventory drift"
        assert {path.relative_to(source_root).as_posix() for path in actual} == set(paths)
        by_path = {entry["source_path"]: entry for entry in entries}
        for path in actual:
            entry = by_path[path.relative_to(source_root).as_posix()]
            assert sha256(path) == entry["source_sha256"], f"Actionbook source changed: {path}"
            assert path.stat().st_size == entry["source_bytes"]
            try:
                assert len(path.read_text(encoding="utf-8").splitlines()) == entry["source_lines"]
            except UnicodeDecodeError:
                assert entry["source_lines"] is None

    unsafe_roots = (
        ROOT / "skills" / "rust-unsafe" / "references" / "actionbook-checks" / "rules",
        ROOT / "skills" / "rust-unsafe-ffi" / "references" / "actionbook-checks" / "rules",
    )
    rule_files = sorted(path for root in unsafe_roots for path in root.glob("*.md"))
    assert len(rule_files) == 47
    rule_ids = [frontmatter(path)["id"] for path in rule_files]
    assert len(rule_ids) == len(set(rule_ids)) == 47
    prefixes = Counter(rule_id.split("-", 1)[0] for rule_id in rule_ids)
    assert prefixes == {"general": 3, "safety": 11, "ptr": 6, "union": 2, "mem": 6, "ffi": 18, "io": 1}
    examples: Counter = Counter()
    for path in rule_files:
        content = path.read_text(encoding="utf-8")
        assert "Product adaptation for" in "\n".join(content.splitlines()[:14])
        examples.update(validate_rule_examples(path, content))
    assert examples == {"fragment": 123}

    excluded_profiles = {"domain-iot", "domain-embedded", "domain-cloud-native", "core-agent-browser"}
    assert not (excluded_profiles & skills)
    return coverage


def validate_huiali_coverage(skills: set[str]) -> dict:
    coverage = load_json(ROOT / "provenance" / "huiali-coverage.json")
    assert coverage["schema_version"] == 1
    assert coverage["source"] == {
        "name": "huiali/rust-skills",
        "relative_path": "references/rust-skills_huiali",
        "revision": "947bf77509d9b421035037e983da6662d08cbb8e",
        "commit_date": "2026-02-09T15:36:33+08:00",
        "license": "MIT",
        "copyright": "Copyright (c) 2026 Li Pianpian <huiali@hotmail.com>",
    }
    assert set(coverage["statuses"]) == huiali.STATUSES
    assert set(coverage["rust_block_statuses"]) == huiali.BLOCK_STATUSES
    assert coverage["family_order"] == huiali.FAMILY_ORDER
    assert coverage["source_metrics"] == {
        "canonical_markdown_files": 111,
        "canonical_markdown_lines": 25175,
        "source_rust_blocks": 500,
        "unique_rust_blocks": 423,
        "rust_block_aliases": 77,
    }

    entries = coverage["entries"]
    assert len(entries) == 348
    paths = [entry["source_path"] for entry in entries]
    assert len(paths) == len(set(paths)) == 348
    counts = Counter(entry["status"] for entry in entries)
    assert counts == {"duplicate": 150, "adapted": 39, "merged": 100, "excluded": 59}
    assert coverage["summary"]["source_files"] == 348
    assert coverage["summary"]["exact_duplicate_files"] == 150
    assert coverage["summary"]["pending"] == coverage["summary"]["in_progress"] == 0
    assert coverage["summary"]["example_decisions"] == {
        "corrected": 1, "pending": 0, "rejected": 8, "retained": 414,
    }
    by_path = {entry["source_path"]: entry for entry in entries}
    for entry in entries:
        assert entry["status"] in huiali.STATUSES and entry["reason"]
        if entry["status"] in {"adapted", "merged"}:
            assert entry["target_paths"], f"integrated Huiali source has no target: {entry['source_path']}"
        else:
            assert not entry["target_paths"], f"non-integrated Huiali source has target: {entry['source_path']}"
        for target in entry["target_paths"]:
            assert (ROOT / target).is_file(), f"missing Huiali target: {target}"
        if entry["status"] == "duplicate":
            assert entry["source_path"].startswith(".codex/skills/")
            assert entry["duplicate_of"] == entry["source_path"].removeprefix(".codex/")
            canonical = by_path[entry["duplicate_of"]]
            assert canonical["source_sha256"] == entry["source_sha256"]

    source_root = REPOSITORY / coverage["source"]["relative_path"]
    if source_root.exists():
        actual = sorted(
            path for path in source_root.rglob("*")
            if path.is_file()
            and ".git" not in path.relative_to(source_root).parts
            and "graphify-out" not in path.relative_to(source_root).parts
        )
        assert len(actual) == 348, "Huiali source inventory drift"
        assert {path.relative_to(source_root).as_posix() for path in actual} == set(paths)
        for path in actual:
            entry = by_path[path.relative_to(source_root).as_posix()]
            assert sha256(path) == entry["source_sha256"], f"Huiali source changed: {path}"
            assert path.stat().st_size == entry["source_bytes"]
            try:
                assert len(path.read_text(encoding="utf-8").splitlines()) == entry["source_lines"]
            except UnicodeDecodeError:
                assert entry["source_lines"] is None

    blocks = coverage["rust_blocks"]
    assert len(blocks) == 423
    assert len({block["source_sha256"] for block in blocks}) == 423
    assert sum(len(block["occurrences"]) for block in blocks) == 500
    block_counts = Counter(block["status"] for block in blocks)
    assert block_counts == {"retained": 414, "rejected": 8, "corrected": 1}
    known_hashes = {block["source_sha256"] for block in blocks}
    for block in blocks:
        assert block["status"] in huiali.BLOCK_STATUSES and block["reason"]
        if block["status"] in {"retained", "corrected"}:
            assert block["classification"] == "fragment" and block["target_paths"]
        else:
            assert block["classification"] is None and not block["target_paths"]

    target_files = sorted((ROOT / "skills").glob("*/references/huiali/*.md"))
    assert len(target_files) == 39
    target_blocks = 0
    for path in target_files:
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if line.strip() != "```rust":
                continue
            target_blocks += 1
            assert index >= 2
            assert RULE_EXAMPLE.fullmatch(lines[index - 1].strip()), f"unclassified Huiali block: {path}:{index + 1}"
            marker = HU_BLOCK_MARKER.fullmatch(lines[index - 2].strip())
            assert marker and marker.group(1) in known_hashes, f"missing Huiali marker: {path}:{index + 1}"
    assert target_blocks == 415

    for family, config in huiali.FAMILY_CONFIG.items():
        owner = config["owner"]
        assert owner in skills
        target = huiali.target_for_family(family)
        assert (ROOT / target).is_file()
        source_entry = by_path[f"skills/{family}/SKILL.md"]
        assert source_entry["target_paths"] == [target]
        for profile in [owner, *config["supporting"]]:
            index = ROOT / "skills" / profile / "references" / "huiali-index.md"
            assert index.is_file() and f"`{family}`" in index.read_text(encoding="utf-8")

    merged_names = {family for family, config in huiali.FAMILY_CONFIG.items() if config["owner"] != family}
    assert not (merged_names & skills), f"standalone merged Huiali profiles leaked into product: {sorted(merged_names & skills)}"
    assert HU_NEW_SKILLS <= skills
    return coverage


def validate_rule_examples(path: Path, content: str) -> Counter:
    lines = content.splitlines()
    counts: Counter = Counter()
    annotations = sum(1 for line in lines if RULE_EXAMPLE.fullmatch(line.strip()))
    in_rust = False
    for index, line in enumerate(lines):
        if line.strip() == "```rust":
            previous = lines[index - 1].strip() if index else ""
            match = RULE_EXAMPLE.fullmatch(previous)
            assert match, f"unclassified Rust block in {path}:{index + 1}"
            kind, attributes = match.group(1), match.group(2) or ""
            counts[kind] += 1
            if kind == "fragment":
                assert re.search(r"(?:^|;)\s*missing\s*:", attributes), (
                    f"fragment lacks missing context in {path}:{index + 1}"
                )
            elif kind == "fixture":
                assert re.search(r"(?:^|;)\s*dependencies\s*:", attributes), (
                    f"fixture lacks dependencies in {path}:{index + 1}"
                )
            elif kind == "compile_fail":
                assert re.search(r"(?:^|;)\s*harness=(?:rustc|cargo)(?:;|$)", attributes)
                assert re.search(r"(?:^|;)\s*expected=\"[^\"]+\"(?:;|$)", attributes)
            in_rust = True
        elif line.strip() == "```" and in_rust:
            in_rust = False
    assert not in_rust, f"unclosed Rust block in {path}"
    assert annotations == sum(counts.values()), f"orphan example annotation in {path}"
    return counts


def validate_rulebook(skills: set[str], only_rule: str | None = None) -> tuple[int, Counter]:
    coverage = load_json(ROOT / "provenance" / "rule-coverage.json")
    assert coverage["schema_version"] == 1
    source = coverage["source"]
    assert source["snapshot"] == "1.5.1"
    assert source["revision"] == "fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9"
    assert source["license"] == "MIT" and "Leonardo Maldonado" in source["copyright"]
    assert set(coverage["statuses"]) == RULE_STATUSES
    summary = coverage["summary"]
    assert summary == {
        "rules": 265,
        "categories": 26,
        "source_lines": 33654,
        "source_rust_blocks": 1131,
        "source_top_level_rust_blocks": 1127,
    }

    entries = coverage["entries"]
    assert len(entries) == 265
    ids = [entry["source_id"] for entry in entries]
    assert len(ids) == len(set(ids)), "duplicate rule coverage IDs"
    by_id = {entry["source_id"]: entry for entry in entries}
    assert only_rule is None or only_rule in by_id, f"unknown rule ID: {only_rule}"
    assert {entry["category"] for entry in entries} == set(RULE_CATEGORIES)
    assert all(entry["status"] in RULE_STATUSES for entry in entries)
    if only_rule is None:
        unfinished = [entry["source_id"] for entry in entries if entry["status"] in {"pending", "in_progress"}]
        assert not unfinished, f"unfinished rulebook entries: {unfinished[:10]}"

    actual_aliases = {
        entry["source_id"]: entry["canonical_id"]
        for entry in entries
        if entry["status"] == "alias"
    }
    assert actual_aliases == EXPECTED_ALIASES
    for alias, canonical in actual_aliases.items():
        assert canonical in by_id and canonical != alias
        assert by_id[canonical]["status"] in {"adapted", "conditional"}
        assert by_id[alias]["owner"] == by_id[canonical]["owner"]
        seen = {alias}
        cursor = canonical
        while by_id[cursor]["status"] == "alias":
            assert cursor not in seen, f"alias cycle at {alias}"
            seen.add(cursor)
            cursor = by_id[cursor]["canonical_id"]

    rule_root = ROOT / "skills" / RULEBOOK_SKILL / "references" / "rules"
    actual_paths = sorted(rule_root.glob("*.md"))
    assert {path.stem for path in actual_paths} == set(ids), "rule file coverage mismatch"
    selected = [by_id[only_rule]] if only_rule else entries
    example_counts: Counter = Counter()
    for entry in selected:
        rule_id = entry["source_id"]
        assert entry["category"] == rule_id.split("-", 1)[0]
        assert entry["owner"] in skills - {RULEBOOK_SKILL}
        assert len(entry["supporting_profiles"]) <= 2
        assert set(entry["supporting_profiles"]) <= skills - {RULEBOOK_SKILL}
        if entry["status"] != "alias":
            assert entry["owner"] in RULE_CATEGORIES[entry["category"]], (
                f"invalid owner for {rule_id}: {entry['owner']}"
            )
            assert entry["canonical_id"] == rule_id
        assert entry["reason"] and entry["reason"] != "Awaiting one-rule adaptation."
        path = ROOT / entry["target_path"]
        assert path == rule_root / f"{rule_id}.md" and path.is_file()
        assert sha256(path) == entry["target_sha256"], f"target rule changed: {path}"
        content = path.read_text(encoding="utf-8")
        lines = content.splitlines()
        assert lines and lines[0] == f"# {rule_id}"
        assert any(line.startswith("> ") for line in lines[:8]), f"missing rule summary: {rule_id}"
        assert all(entry["facets"].values()), f"rule facets not preserved: {rule_id}"
        if entry["status"] in {"adapted", "conditional"}:
            headings = set(re.findall(r"^## (.+?)\s*$", content, re.MULTILINE))
            assert RULE_SECTIONS <= headings, f"missing rule sections in {rule_id}: {sorted(RULE_SECTIONS - headings)}"
        elif entry["status"] == "alias":
            canonical = entry["canonical_id"]
            assert "## Canonical Rule" in content and "## Alias Reason" in content
            assert f"]({canonical}.md)" in content
            assert "## Preserved Source Guidance" in content
        elif entry["status"] == "rejected":
            assert "## Rejection Reason" in content
        example_counts.update(validate_rule_examples(path, content))

    source_root = REPOSITORY / source["relative_path"] / "rules"
    if source_root.exists():
        assert {path.stem for path in source_root.glob("*.md")} == set(ids), "Leonardomso source inventory drift"
        for entry in selected:
            path = source_root / f"{entry['source_id']}.md"
            text = path.read_text(encoding="utf-8")
            assert sha256(path) == entry["source_sha256"], f"source rule changed: {path}"
            assert len(text.splitlines()) == entry["source_lines"]
            assert re.findall(r"^##+\s+(.+)$", text, re.MULTILINE) == entry["source_headings"]
            assert sum(line.strip() == "```rust" for line in text.splitlines()) == entry["source_rust_blocks"]
            assert len(re.findall(r"^```rust\s*$", text, re.MULTILINE)) == entry["source_top_level_rust_blocks"]

    if only_rule is None:
        assert example_counts == {"compile_fail": 1, "fixture": 6, "fragment": 1131, "standalone": 3}
        category_root = rule_root.parent / "categories"
        indexes = {path.stem: path for path in category_root.glob("*.md")}
        assert set(indexes) == set(RULE_CATEGORIES), "category index parity mismatch"
        routing = (rule_root.parent / "routing.md").read_text(encoding="utf-8")
        for category, index in indexes.items():
            assert f"(categories/{category}.md)" in routing
            content = index.read_text(encoding="utf-8")
            category_ids = {entry["source_id"] for entry in entries if entry["category"] == category}
            linked = set(re.findall(r"\]\(\.\./rules/([a-z0-9-]+)\.md\)", content))
            assert linked == category_ids, f"category index mismatch: {category}"
    return len(entries), example_counts


def validate_skills(expected_skills: set[str], example_owners: set[str]) -> None:
    skill_root = ROOT / "skills"
    skill_dirs = {path.name for path in skill_root.iterdir() if path.is_dir()}
    assert skill_dirs == expected_skills, f"unexpected skills: {sorted(skill_dirs ^ expected_skills)}"
    assert len(skill_dirs) == 50
    assert not (skill_root / "rust-workflow" / "references" / "engineering-domains.md").exists()

    descriptions = []
    for skill in sorted(skill_dirs):
        root = skill_root / skill
        skill_md = root / "SKILL.md"
        metadata = frontmatter(skill_md)
        assert metadata.get("name") == skill
        description = metadata.get("description", "")
        assert 80 <= len(description) <= 1024, f"description length for {skill}: {len(description)}"
        descriptions.append(description)

        content = skill_md.read_text(encoding="utf-8")
        assert len(content.splitlines()) >= 25, f"thin SKILL.md: {skill}"
        assert len(re.findall(r"^## ", content, re.MULTILINE)) >= 3, f"insufficient workflow structure: {skill}"
        reference_files = list((root / "references").glob("*.md"))
        assert reference_files, f"missing detailed reference: {skill}"
        combined = content + "\n" + "\n".join(path.read_text(encoding="utf-8") for path in reference_files)
        assert len(re.findall(r"\b[\w'-]+\b", combined, re.UNICODE)) >= 350, f"insufficient profile detail: {skill}"

        ui_path = root / "agents" / "openai.yaml"
        ui = ui_path.read_text(encoding="utf-8")
        assert re.search(r"^interface:\s*$", ui, re.MULTILINE), f"invalid UI metadata: {skill}"
        assert re.search(r"^  display_name: \"[^\"]+\"$", ui, re.MULTILINE), f"missing display name: {skill}"
        assert re.search(r"^  short_description: \"[^\"]+\"$", ui, re.MULTILINE), f"missing short description: {skill}"
        assert re.search(r"^  default_prompt: \"[^\"]+\"$", ui, re.MULTILINE), f"missing default prompt: {skill}"
        assert f"${skill}" in ui, f"default prompt does not invoke {skill}"
        assert re.search(r"^policy:\s*\n  allow_implicit_invocation: true$", ui, re.MULTILINE), f"implicit routing disabled: {skill}"

    assert len(descriptions) == len(set(descriptions)), "duplicate skill descriptions"

    routing = (skill_root / "rust-workflow" / "references" / "routing-index.md").read_text(encoding="utf-8")
    for skill in skill_dirs:
        assert f"`{skill}`" in routing or f"${skill}" in routing, f"skill missing from routing index: {skill}"

    actual_examples = {path.parents[2].name for path in skill_root.glob("*/examples/golden/Cargo.toml")}
    assert actual_examples == example_owners, f"golden example coverage mismatch: {sorted(actual_examples ^ example_owners)}"
    assert len(actual_examples) == 25
    for skill in actual_examples:
        assert "## Compiling Example" in "\n".join(
            path.read_text(encoding="utf-8") for path in (skill_root / skill / "references").glob("*.md")
        ), f"golden example not linked from reference: {skill}"


def validate_agents() -> None:
    agent_files = list((ROOT / "agents").glob("*.md"))
    assert {frontmatter(path)["name"] for path in agent_files} == AGENTS
    assert len(agent_files) == len(AGENTS)
    for path in agent_files:
        content = path.read_text(encoding="utf-8").lower()
        assert "read-only" in content and "do not edit" in content, f"agent is not explicitly read-only: {path.name}"


def validate_hooks() -> None:
    assert {path.name for path in (ROOT / "hooks").glob("*.json")} == {"claude.json", "hooks.json"}
    claude_hooks = load_json(ROOT / "hooks" / "claude.json")
    codex_hooks = load_json(ROOT / "hooks" / "hooks.json")
    assert "CLAUDE_PLUGIN_ROOT" in json.dumps(claude_hooks)
    encoded_codex_hooks = json.dumps(codex_hooks)
    assert "PLUGIN_ROOT" in encoded_codex_hooks and "CLAUDE_PLUGIN_ROOT" not in encoded_codex_hooks
    for config in (claude_hooks, codex_hooks):
        assert set(config["hooks"]) == {"SessionStart"}, "automatic hooks must be SessionStart-only"
        handlers = config["hooks"]["SessionStart"]
        assert len(handlers) == 1 and len(handlers[0]["hooks"]) == 1
        hook = handlers[0]["hooks"][0]
        assert hook["type"] == "command" and 0 < hook["timeout"] <= 10

    for path in (ROOT / "scripts" / "session-context.sh", ROOT / "scripts" / "session-context.ps1"):
        content = path.read_text(encoding="utf-8")
        assert not DISALLOWED_HOOK_COMMANDS.search(content), f"mutating or expensive automatic hook command: {path}"
        assert "cargo locate-project" in content and "rustc --version" in content and "cargo --version" in content
        assert all(
            skill in content
            for skill in ("rust-workflow", "rust-review", "rust-verify", "rust-design-protocol", "rust-research")
        )


def validate_evals(skills: set[str]) -> int:
    evals = load_json(ROOT / "evals" / "evals.json")
    assert evals["schema_version"] == 5
    assert evals["actionbook_cases_file"] == "actionbook-cases.json"
    assert evals["huiali_cases_file"] == "huiali-cases.json"
    cases = evals["cases"]
    ids = [case["id"] for case in cases]
    assert len(cases) == 108 and len(ids) == len(set(ids)), "routing corpus must have 108 unique cases"
    modes = Counter(case["mode"] for case in cases)
    assert modes == {"manual": 44, "automatic": 44, "contrast": 8, "negative": 12}

    profile_skills = skills - {RULEBOOK_SKILL}
    legacy_profile_skills = profile_skills - ACTIONBOOK_SKILLS - HU_NEW_SKILLS
    manual_profiles = set()
    automatic_profiles = set()
    manual_overlay = automatic_overlay = 0
    for case in cases:
        expected = case["expected"]
        entry = expected["entry_skill"]
        primary = expected["primary_profile"]
        supporting = expected["supporting_profiles"]
        forbidden = expected["forbidden_primary_profiles"]
        overlays = expected["overlays"]
        assert entry in skills | {None}
        assert primary in profile_skills | {None}
        assert len(supporting) <= 2 and set(supporting) <= profile_skills
        assert set(forbidden) <= profile_skills and primary not in forbidden
        assert set(overlays) <= {RULEBOOK_SKILL} and len(overlays) <= 1
        assert RULEBOOK_SKILL not in supporting and RULEBOOK_SKILL not in forbidden
        assert case["prompt"] and isinstance(case["mutation"], bool) and case["tags"]
        if case["mode"] == "manual":
            if entry == RULEBOOK_SKILL:
                assert primary is None and overlays == [RULEBOOK_SKILL]
                manual_overlay += 1
            else:
                assert entry == primary and primary is not None
                manual_profiles.add(primary)
        elif case["mode"] == "automatic":
            assert primary is not None
            automatic_profiles.add(primary)
            if case["mutation"]:
                assert entry == "rust-workflow"
            if overlays:
                automatic_overlay += 1
        elif case["mode"] == "negative":
            assert entry is None and primary is None and not supporting and not forbidden and not overlays
    assert manual_profiles == automatic_profiles == legacy_profile_skills
    assert manual_overlay == automatic_overlay == 1

    rulebook_cases = evals["rulebook_cases"]
    rulebook_ids = [case["id"] for case in rulebook_cases]
    assert len(rulebook_cases) == 44 and len(rulebook_ids) == len(set(rulebook_ids))
    assert not (set(ids) & set(rulebook_ids))
    kinds = Counter(case["kind"] for case in rulebook_cases)
    assert kinds == {"prefix": 26, "context_conflict": 12, "negative": 6}
    known_rule_ids = {
        entry["source_id"] for entry in load_json(ROOT / "provenance" / "rule-coverage.json")["entries"]
    }
    prefix_categories = set()
    for case in rulebook_cases:
        expected = case["expected"]
        assert case["prompt"] and case["tags"]
        assert isinstance(expected["activate"], bool)
        assert set(expected["categories"]) <= set(RULE_CATEGORIES)
        assert set(expected["owner_profiles"]) <= profile_skills
        assert set(expected["rule_ids"]) <= known_rule_ids
        assert set(expected["rejected_rule_ids"]) <= known_rule_ids
        assert not (set(expected["rule_ids"]) & set(expected["rejected_rule_ids"]))
        assert expected["reason_contains"] and all(isinstance(item, str) and item for item in expected["reason_contains"])
        if case["kind"] == "prefix":
            assert expected["activate"] and len(expected["categories"]) == 1
            assert expected["max_rules"] == 8
            prefix_categories.update(expected["categories"])
        elif case["kind"] == "context_conflict":
            assert expected["activate"] and 1 <= expected["max_rules"] <= 8
            assert expected["categories"] and expected["owner_profiles"]
        else:
            assert not expected["activate"]
            assert expected["max_rules"] == 0
            assert (
                not expected["categories"] and not expected["owner_profiles"]
                and not expected["rule_ids"] and not expected["rejected_rule_ids"]
            )
    assert prefix_categories == set(RULE_CATEGORIES)
    actionbook = load_json(ROOT / "evals" / evals["actionbook_cases_file"])
    assert actionbook["schema_version"] == 1
    actionbook_cases = actionbook["cases"]
    actionbook_ids = [case["id"] for case in actionbook_cases]
    assert len(actionbook_cases) == 44 and len(actionbook_ids) == len(set(actionbook_ids))
    assert not (set(ids) & set(rulebook_ids) or set(ids) & set(actionbook_ids) or set(rulebook_ids) & set(actionbook_ids))
    assert Counter(case["kind"] for case in actionbook_cases) == ACTIONBOOK_KINDS

    unsafe_rule_ids = {
        frontmatter(path)["id"]
        for root in (
            ROOT / "skills" / "rust-unsafe" / "references" / "actionbook-checks" / "rules",
            ROOT / "skills" / "rust-unsafe-ffi" / "references" / "actionbook-checks" / "rules",
        )
        for path in root.glob("*.md")
    }
    actionbook_primary = set()
    for case in actionbook_cases:
        expected = case["expected"]
        assert case["prompt"] and case["tags"] and expected["forbidden"]
        assert isinstance(expected["activate"], bool)
        assert set(expected["references"]) <= ACTIONBOOK_REFERENCES
        assert len(expected["supporting_profiles"]) <= 2
        assert set(expected["supporting_profiles"]) <= profile_skills
        assert set(expected.get("unsafe_rule_ids", [])) <= unsafe_rule_ids
        assert set(expected.get("navigation_modes", [])) <= {
            "definition", "references", "implementations", "type-hierarchy",
            "dependency-graph", "incoming-calls", "outgoing-calls", "cfg",
            "rename-impact", "graphify", "rg", "cargo",
        }
        assert expected.get("research_mode") in {None, "rust", "crate", "news"}
        assert isinstance(expected.get("requires_cargo_metadata", False), bool)
        if expected["activate"]:
            assert expected["entry_layer"] in {"Mechanics", "Design", "Domain"}
            assert expected["primary_profile"] in profile_skills
            assert expected["references"]
            actionbook_primary.add(expected["primary_profile"])
        else:
            assert case["kind"] == "negative"
            assert expected["entry_layer"] is None and expected["primary_profile"] is None
            assert not expected["supporting_profiles"] and not expected["references"]
            assert not expected.get("unsafe_rule_ids", [])
            assert not expected.get("navigation_modes", [])

        if case["kind"] == "navigation":
            assert expected.get("navigation_modes")
        elif case["kind"] == "research_dynamic":
            assert expected.get("research_mode") in {"rust", "crate", "news"}
        elif case["kind"] == "unsafe":
            assert expected.get("unsafe_rule_ids")
            assert expected["primary_profile"] in {"rust-unsafe", "rust-unsafe-ffi"}
        elif case["kind"] == "ml":
            assert expected["primary_profile"] == "rust-ml"

    assert ACTIONBOOK_SKILLS <= actionbook_primary

    huiali_evals = load_json(ROOT / "evals" / evals["huiali_cases_file"])
    assert huiali_evals["schema_version"] == 1
    assert huiali_evals["source"] == {
        "name": "huiali/rust-skills",
        "revision": "947bf77509d9b421035037e983da6662d08cbb8e",
    }
    huiali_cases = huiali_evals["cases"]
    huiali_ids = [case["id"] for case in huiali_cases]
    assert len(huiali_cases) == 48 and len(huiali_ids) == len(set(huiali_ids))
    assert Counter(case["kind"] for case in huiali_cases) == HU_KINDS
    all_id_sets = [set(ids), set(rulebook_ids), set(actionbook_ids), set(huiali_ids)]
    assert all(not left & right for index, left in enumerate(all_id_sets) for right in all_id_sets[index + 1 :])

    family_names = set(huiali.FAMILY_CONFIG)
    new_profile_primary: Counter = Counter()
    huiali_primary = set()
    for case in huiali_cases:
        expected = case["expected"]
        assert case["prompt"] and case["tags"] and expected["forbidden"]
        assert isinstance(expected["activate"], bool)
        assert len(expected["supporting_profiles"]) <= 2
        assert set(expected["supporting_profiles"]) <= profile_skills
        assert set(expected["references"]) <= family_names
        fallback = expected.get("fallback_profile")
        assert fallback in profile_skills | {None}
        if expected["activate"]:
            assert expected["primary_profile"] in profile_skills
            assert expected["references"]
            huiali_primary.add(expected["primary_profile"])
            if case["kind"] == "new_profile":
                assert expected["primary_profile"] in HU_NEW_SKILLS
                new_profile_primary[expected["primary_profile"]] += 1
            elif case["kind"] == "merged":
                assert expected["primary_profile"] not in HU_NEW_SKILLS
            else:
                assert case["kind"] == "conflict"
        else:
            assert case["kind"] == "negative"
            assert expected["primary_profile"] is None
            assert not expected["supporting_profiles"] and not expected["references"]

    assert new_profile_primary == {skill: 4 for skill in HU_NEW_SKILLS}
    assert HU_NEW_SKILLS <= huiali_primary
    return len(cases) + len(actionbook_cases) + len(huiali_cases)


def validate_metadata_fixture() -> None:
    fixture = ROOT / "checks" / "metadata-workspace"
    manifest = fixture / "Cargo.toml"
    assert manifest.is_file() and (fixture / "Cargo.lock").is_file()
    assert 'resolver = "3"' in manifest.read_text(encoding="utf-8")
    cargo = shutil.which("cargo")
    assert cargo, "cargo is required for the metadata fixture"
    command = [
        cargo, "metadata", "--format-version", "1", "--locked", "--offline",
        "--manifest-path", str(manifest), "--no-deps",
    ]
    result = subprocess.run(command, cwd=fixture, text=True, capture_output=True, check=False)
    assert result.returncode == 0, f"cargo metadata fixture failed:\n{result.stdout}\n{result.stderr}"
    metadata = json.loads(result.stdout)
    packages = {package["name"]: package for package in metadata["packages"]}
    assert set(packages) == {"metadata-app", "metadata-local-util"}
    app = packages["metadata-app"]
    assert app["edition"] == "2024" and app["rust_version"] == "1.85"
    assert app["features"] == {"default": [], "util": ["dep:renamed-util"]}
    dependencies = {dependency["rename"]: dependency for dependency in app["dependencies"]}
    assert dependencies["renamed-util"]["name"] == "metadata-local-util"
    assert dependencies["renamed-util"]["optional"] is True
    assert dependencies["renamed-util"]["target"] is None
    assert dependencies["unix-util"]["name"] == "metadata-local-util"
    assert dependencies["unix-util"]["optional"] is False
    assert dependencies["unix-util"]["target"] == "cfg(unix)"


def validate_examples(example_owners: set[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="rust-engineering-examples-") as target:
        for skill in sorted(example_owners):
            manifest = ROOT / "skills" / skill / "examples" / "golden" / "Cargo.toml"
            commands = [[
                "cargo", "test", "--quiet", "--offline", "--locked", "--manifest-path", str(manifest),
                "--target-dir", str(Path(target) / skill),
            ]]
            if skill == "rust-cargo-build":
                commands.append(commands[0] + ["--features", "fast"])
            for command in commands:
                completed = subprocess.run(command, cwd=manifest.parent, text=True, capture_output=True, check=False)
                assert completed.returncode == 0, (
                    f"golden example failed: {skill}\ncommand: {' '.join(command)}\n"
                    f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
                )


def validate_rulebook_examples(rule_id: str | None = None) -> tuple[Counter, str | None]:
    generator = ROOT / "checks" / "rulebook" / "gen.py"
    with tempfile.TemporaryDirectory(prefix="rust-engineering-rulebook-") as target:
        root = Path(target)
        output = root / "generated"
        selection = ["--rule", rule_id] if rule_id else ["--all"]
        command = [sys.executable, str(generator), *selection, "--out", str(output)]
        generated = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        assert generated.returncode == 0, (
            f"rulebook generator failed\ncommand: {' '.join(command)}\n"
            f"stdout:\n{generated.stdout}\nstderr:\n{generated.stderr}"
        )
        manifest = load_json(output / "manifest.json")
        counts = Counter(manifest["counts"])

        binaries = root / "standalone-bin"
        binaries.mkdir()
        for path in sorted((output / "standalone").glob("*.rs")):
            rustc = ["rustc", "--edition=2024", str(path), "-o", str(binaries / path.stem)]
            completed = subprocess.run(rustc, cwd=output, text=True, capture_output=True, check=False)
            assert completed.returncode == 0, (
                f"standalone rule example failed: {path.name}\ncommand: {' '.join(rustc)}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            )

        fixture_paths = sorted((output / "examples").glob("*.rs"))
        fixture_skip = None
        if fixture_paths:
            cargo = [
                "cargo", "check", "--quiet", "--locked", "--offline", "--examples",
                "--manifest-path", str(output / "Cargo.toml"),
                "--target-dir", str(root / "cargo-target"),
            ]
            completed = subprocess.run(cargo, cwd=output, text=True, capture_output=True, check=False)
            if completed.returncode != 0 and OFFLINE_CACHE_MISS.search(completed.stderr + completed.stdout):
                fixture_skip = (
                    "environment skip: locked rulebook fixtures require a crate absent from the local Cargo cache; "
                    "ask before running `cargo fetch --locked --manifest-path "
                    f"{ROOT / 'checks' / 'rulebook' / 'Cargo.toml'}`"
                )
            else:
                assert completed.returncode == 0, (
                    f"locked rulebook fixtures failed\ncommand: {' '.join(cargo)}\n"
                    f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
                )

        records = {record["generated"]: record for record in manifest["records"] if "generated" in record}
        for path in sorted((output / "compile_fail").glob("*.rs")):
            record = records[f"compile_fail/{path.name}"]
            attributes = record["attributes"]
            expected = str(attributes["expected"])
            if attributes["harness"] == "rustc":
                command = ["rustc", "--edition=2024", str(path), "-o", str(binaries / path.stem)]
            else:
                destination = output / "examples" / path.name
                shutil.copy2(path, destination)
                command = [
                    "cargo", "check", "--quiet", "--locked", "--offline", "--example", path.stem,
                    "--manifest-path", str(output / "Cargo.toml"),
                    "--target-dir", str(root / "cargo-target-compile-fail"),
                ]
            completed = subprocess.run(command, cwd=output, text=True, capture_output=True, check=False)
            diagnostic = completed.stderr + completed.stdout
            assert completed.returncode != 0, f"compile_fail unexpectedly compiled: {path.name}"
            assert expected.lower() in diagnostic.lower(), (
                f"compile_fail diagnostic mismatch: {path.name}\nexpected substring: {expected}\n"
                f"diagnostic:\n{diagnostic}"
            )
        return counts, fixture_skip


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--examples", action="store_true", help="compile and test all dependency-free golden examples")
    parser.add_argument("--rule", help="validate one addressable rule ID and optionally its classified examples")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    coverage, owners, example_owners = validate_source_coverage()
    expected_skills = owners | {"rust-workflow", "rust-verify", RULEBOOK_SKILL} | ACTIONBOOK_SKILLS | HU_NEW_SKILLS
    golden_owners = example_owners | HU_NEW_SKILLS
    assert ENTRY_SKILLS <= expected_skills
    if args.rule:
        _, counts = validate_rulebook(expected_skills, only_rule=args.rule)
        fixture_skip = None
        if args.examples:
            counts, fixture_skip = validate_rulebook_examples(args.rule)
        print(
            f"OK: rule {args.rule}, {sum(counts.values())} classified Rust blocks"
            + (" compiled where declared" if args.examples else " statically checked")
        )
        if fixture_skip:
            print(fixture_skip)
        return

    validate_manifests()
    validate_skills(expected_skills, golden_owners)
    actionbook = validate_actionbook_coverage(expected_skills)
    huiali_ledger = validate_huiali_coverage(expected_skills)
    rule_count, rule_examples = validate_rulebook(expected_skills)
    validate_links()
    validate_agents()
    validate_hooks()
    eval_count = validate_evals(expected_skills)
    validate_metadata_fixture()
    fixture_skip = None
    if args.examples:
        validate_examples(golden_owners)
        rule_examples, fixture_skip = validate_rulebook_examples()
    print(
        f"OK: {len(expected_skills)} skills, {len(AGENTS)} read-only agents, "
        f"{eval_count} routing, Actionbook, and Huiali evals, {coverage['summary']['adapted']} adapted source skills, "
        f"{coverage['summary']['out_of_scope']} explicit exclusions, {rule_count} coding rules, "
        f"{sum(rule_examples.values())} classified rule examples, {len(golden_owners)} golden examples, "
        f"{actionbook['summary']['source_files']} accounted Actionbook files, "
        f"{huiali_ledger['summary']['source_files']} accounted Huiali files"
        + (" compiled" if args.examples else " statically checked")
    )
    if fixture_skip:
        print(fixture_skip)


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
