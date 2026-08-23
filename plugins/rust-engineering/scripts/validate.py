#!/usr/bin/env python3
"""Validate the release contracts of the dual-host Rust Engineering plugin."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import types
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
SKILLS = set(
    """
    addressing-findings codebase-onboarding debugging nix-dev-env nix-flakes
    nix-packaging nix-review nixos refactoring rust-api-design
    rust-architecture rust-architecture-review rust-by-example rust-cargo-build
    rust-coding-rules rust-concurrency rust-crate-discovery rust-data
    rust-database rust-dependencies rust-design-protocol rust-distributed-systems
    rust-documentation rust-ecosystem rust-errors rust-gpu rust-idioms
    rust-lombok-macros rust-macros rust-ml rust-module-layout rust-navigation
    rust-observability rust-ownership rust-performance rust-pin rust-platforms
    rust-research rust-review rust-semver rust-serialization rust-stable
    rust-stdlib rust-style-clippy rust-systems-networking rust-tauri rust-testing
    rust-traits rust-uniffi-building rust-unsafe rust-unsafe-ffi rust-verify
    rust-workflow rust-workspace specs
    """.split()
)
AGENTS = {"rust-scout", "rust-researcher", "rust-reviewer", "rust-verifier"}
GOLDEN_OWNERS = set(
    """
    rust-api-design rust-by-example rust-cargo-build rust-concurrency
    rust-crate-discovery rust-dependencies rust-distributed-systems
    rust-documentation rust-gpu rust-lombok-macros rust-macros
    rust-module-layout rust-observability rust-performance rust-pin rust-review
    rust-semver rust-stable rust-stdlib rust-style-clippy
    rust-systems-networking rust-testing rust-uniffi-building rust-unsafe-ffi
    rust-workspace
    """.split()
)
RULE_CATEGORIES = set(
    """
    anti api async closure coll conc const conv doc err lint macro mem name num
    obs opt own pat perf proj serde test trait type unsafe
    """.split()
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
RULE_SECTIONS = {
    "Decision", "Apply When", "Avoid When", "Algorithm", "Bad", "Good",
    "Trade-offs", "Prerequisites", "Verification", "Related Rules",
}
RULE_EXAMPLE = re.compile(
    r"<!--\s*rust-example:\s*(standalone|fixture|compile_fail|fragment)\s*(?:;\s*(.*?))?\s*-->"
)
SUITE_COUNTS = {
    "workflow": 125,
    "rulebook": 44,
    "design_protocol": 44,
    "specialized_rust": 48,
    "low_level": 48,
    "cargo_tooling": 32,
}
KIND_COUNTS = {
    "rulebook": {"prefix": 26, "context_conflict": 12, "negative": 6},
    "design_protocol": {
        "model_routing": 14, "cross_layer": 8, "navigation": 6,
        "research_dynamic": 6, "unsafe": 6, "ml": 2, "negative": 2,
    },
    "specialized_rust": {"new_profile": 16, "merged": 16, "conflict": 8, "negative": 8},
    "low_level": {
        "debugging_profiling": 8, "cargo_build_time": 8,
        "cross_linker_target": 8, "sanitizer_miri_security": 8,
        "async_system_hardware": 8, "safety_conflict_negative": 8,
    },
    "cargo_tooling": {
        "cargo_generate": 4, "cargo_nextest": 4, "cargo_llvm_cov": 4,
        "cargo_machete": 4, "worktree_builds": 4, "clippy_advanced": 4,
        "ownership_conflict": 4, "negative_safety": 4,
    },
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
TICK = chr(96)
RUST_FENCE = TICK * 3 + "rust"
FENCE = TICK * 3


def load_json(path: Path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


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
    paths = list(ROOT.rglob("*.md")) + [REPOSITORY_ROOT / "README.md", REPOSITORY_ROOT / "AGENTS.md"]
    for path in paths:
        for raw_target in link.findall(path.read_text(encoding="utf-8")):
            target = raw_target.strip().strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if not relative:
                continue
            if (
                "::" in relative
                or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(?:<[^>]+>)?", relative)
                or re.fullmatch(
                    r"(?:fn|struct|enum|trait|type|macro|mod|const|static|method|prim)@[A-Za-z_][A-Za-z0-9_]*",
                    relative,
                )
            ):
                continue
            assert (path.parent / relative).resolve().exists(), f"broken link in {path}: {raw_target}"


def validate_manifests_and_catalogs() -> dict:
    config = load_json(REPOSITORY_ROOT / "installers" / "config.json")
    assert set(config) == {"marketplace", "plugin", "repository", "ref", "targets", "scopes"}
    assert config["ref"].startswith("v")
    version = config["ref"].removeprefix("v")
    assert re.fullmatch(
        r"\d+\.\d+\.\d+(?:-[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?(?:\+[0-9A-Za-z]+(?:[.-][0-9A-Za-z]+)*)?",
        version,
    )

    claude = load_json(ROOT / ".claude-plugin" / "plugin.json")
    codex = load_json(ROOT / ".codex-plugin" / "plugin.json")
    assert claude["name"] == codex["name"] == config["plugin"] == "rust-engineering"
    assert claude["version"] == codex["version"] == version
    assert claude["description"] == codex["description"]
    assert all(term in claude["description"] for term in ("55", "265"))
    assert claude["homepage"] == codex["homepage"] == claude["repository"] == codex["repository"]
    assert claude["hooks"] == "./hooks/claude.json"
    assert codex["skills"] == "./skills/" and "hooks" not in codex
    assert {"55", "265"} <= set(re.findall(r"\d+", codex["interface"]["longDescription"]))
    assert "$rust-workflow" in codex["interface"]["defaultPrompt"][0]
    assert "$rust-coding-rules" in codex["interface"]["defaultPrompt"][0]
    assert (ROOT / "LICENSE").is_file()
    assert not list(ROOT.rglob(".mcp.json")) and not list(ROOT.rglob(".app.json"))
    assert not any((ROOT / name).exists() for name in ("Cargo.toml", "package.json", "pyproject.toml", "requirements.txt"))

    scripts = {path.name for path in (ROOT / "scripts").iterdir() if path.is_file()}
    assert scripts == {"validate.py", "session-context.sh", "session-context.ps1"}, scripts
    provenance = ROOT / "provenance"
    assert not provenance.exists() or not any(provenance.rglob("*")), "provenance must not ship"
    generated = [
        path for path in ROOT.rglob("*")
        if path.name == "__pycache__" or path.suffix == ".pyc" or (path.is_dir() and path.name == "target")
    ]
    assert not generated, f"generated product artifacts: {generated}"

    assert config["marketplace"] == "rust-skills" and config["plugin"] == codex["name"]
    assert config["targets"] == ["codex-cli", "chatgpt-desktop", "claude-code", "claude-desktop"]
    assert config["scopes"] == ["user", "project", "local"]
    expected_repository = codex["repository"].removeprefix("https://github.com/")
    assert config["repository"] == expected_repository

    codex_market = load_json(REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_market = load_json(REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json")
    assert codex_market["name"] == claude_market["name"] == config["marketplace"]
    assert len(codex_market["plugins"]) == len(claude_market["plugins"]) == 1
    codex_entry, claude_entry = codex_market["plugins"][0], claude_market["plugins"][0]
    assert codex_entry["name"] == claude_entry["name"] == config["plugin"]
    assert codex_entry["source"] == {"source": "local", "path": "./plugins/rust-engineering"}
    assert claude_entry["source"] == "./plugins/rust-engineering"
    assert codex_entry["policy"] == {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}
    assert codex_entry["category"] == "Productivity"

    package = load_json(REPOSITORY_ROOT / "package.json")
    assert package["version"] == version and package["private"] is True and package["type"] == "module"
    assert package["bin"] == {"rust-engineering-install": "./installers/install.mjs"}
    assert not any(key in package for key in ("dependencies", "devDependencies", "optionalDependencies"))
    assert all(
        config["ref"] in path.read_text(encoding="utf-8") and version in path.read_text(encoding="utf-8")
        for path in (REPOSITORY_ROOT / "README.md", REPOSITORY_ROOT / "AGENTS.md")
    )
    return config


def validate_notices_and_identity() -> None:
    notice_path = ROOT / "THIRD_PARTY_NOTICES.md"
    notice = notice_path.read_text(encoding="utf-8")
    urls = re.findall(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", notice)
    assert len(urls) == len(set(urls)) == 7
    revision_pattern = re.escape(TICK) + r"[0-9a-f]{40}" + re.escape(TICK)
    assert len(re.findall(revision_pattern, notice)) == 7
    assert notice.count("Permission is hereby granted, free of charge") == 1
    assert notice.count("Version 2.0, January 2004") == 1
    copyright_lines = re.findall(r"^Copyright \(c\) .+$", notice, re.MULTILINE)
    assert len(copyright_lines) == len(set(copyright_lines)) == 4
    assert all(name in notice for name in ("Leonardo Maldonado", "chessMan", "Lauri Gates"))

    markers = {owner.casefold() for owner, _ in urls}
    markers |= {repo.casefold() for _, repo in urls if repo.casefold() != "rust-skills"}
    patterns = {
        marker: re.compile(rf"(?<![a-z0-9]){re.escape(marker)}(?![a-z0-9])", re.IGNORECASE)
        for marker in markers
    }
    candidates = [
        path for path in ROOT.rglob("*")
        if path.is_file() and path != notice_path and path.suffix.lower() in {
            ".md", ".json", ".py", ".mjs", ".sh", ".ps1", ".yaml", ".yml", ".toml"
        }
    ]
    candidates += [
        REPOSITORY_ROOT / "AGENTS.md",
        REPOSITORY_ROOT / "CLAUDE.md",
        REPOSITORY_ROOT / "package.json",
        REPOSITORY_ROOT / ".agents" / "plugins" / "marketplace.json",
        REPOSITORY_ROOT / ".claude-plugin" / "marketplace.json",
        *sorted((REPOSITORY_ROOT / "installers").glob("*")),
    ]
    for path in candidates:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(REPOSITORY_ROOT).as_posix()
        for marker, pattern in patterns.items():
            assert not pattern.search(relative), f"external identity in path: {relative}"
            assert not pattern.search(text), f"external identity in runtime file {relative}: {marker}"

    readme = (REPOSITORY_ROOT / "README.md").read_text(encoding="utf-8")
    heading = "## Источники"
    assert heading in readme and readme.rfind("## ") == readme.index(heading), "sources must be the final README section"
    product_text = readme[: readme.index(heading)]
    for marker, pattern in patterns.items():
        assert not pattern.search(product_text), f"external identity before README sources: {marker}"


def validate_references() -> None:
    extras = {
        "rust-coding-rules": {"rules", "categories", "guidelines"},
        "rust-design-protocol": {"analysis", "cognition", "negotiation", "routing", "examples"},
        "rust-research": {"lenses", "commands", "dossiers", "news"},
        "rust-unsafe": {"rules", "checklists", "workflows", "examples"},
        "rust-unsafe-ffi": {"rules", "checklists", "workflows", "examples"},
        "rust-navigation": {"modes"},
        "rust-architecture": {"domains"},
    }
    for skill in sorted(SKILLS):
        root = ROOT / "skills" / skill / "references"
        assert root.is_dir(), f"missing references: {skill}"
        files = [path for path in root.rglob("*") if path.is_file()]
        assert files and any(path.parent == root and path.suffix == ".md" for path in files), f"missing root reference: {skill}"
        assert all(path.suffix == ".md" for path in files), f"non-Markdown reference: {skill}"
        for path in files:
            assert len(path.relative_to(root).parts) <= 2, f"reference nesting exceeds one theme: {path}"
        allowed = {"low-level", "cargo-tooling"} | extras.get(skill, set())
        actual = {path.name for path in root.iterdir() if path.is_dir()}
        assert actual <= allowed, f"unexpected reference themes for {skill}: {sorted(actual - allowed)}"


def validate_skills() -> None:
    skill_root = ROOT / "skills"
    actual = {path.name for path in skill_root.iterdir() if path.is_dir()}
    assert actual == SKILLS, f"skill inventory mismatch: {sorted(actual ^ SKILLS)}"
    descriptions = []
    for skill in sorted(SKILLS):
        root = skill_root / skill
        skill_md = root / "SKILL.md"
        metadata = frontmatter(skill_md)
        assert metadata.get("name") == skill
        description = metadata.get("description", "")
        assert 80 <= len(description) <= 1024, f"description length for {skill}: {len(description)}"
        descriptions.append(description)
        content = skill_md.read_text(encoding="utf-8")
        assert len(content.splitlines()) >= 25, f"thin SKILL.md: {skill}"
        assert len(re.findall(r"^## ", content, re.MULTILINE)) >= 3, f"insufficient SKILL structure: {skill}"
        references = list((root / "references").rglob("*.md"))
        combined = content + "\n" + "\n".join(path.read_text(encoding="utf-8") for path in references)
        assert len(re.findall(r"\b[\w'-]+\b", combined, re.UNICODE)) >= 350, f"insufficient profile detail: {skill}"

        ui = (root / "agents" / "openai.yaml").read_text(encoding="utf-8")
        assert re.search(r"^interface:\s*$", ui, re.MULTILINE)
        assert re.search(r'^  display_name: "[^"]+"$', ui, re.MULTILINE)
        assert re.search(r'^  short_description: "[^"]+"$', ui, re.MULTILINE)
        assert re.search(r'^  default_prompt: "[^"]+"$', ui, re.MULTILINE)
        assert "$" + skill in ui
        assert re.search(r"^policy:\s*\n  allow_implicit_invocation: true$", ui, re.MULTILINE)
    assert len(descriptions) == len(set(descriptions)), "duplicate skill descriptions"

    routing = (skill_root / "rust-workflow" / "references" / "routing-index.md").read_text(encoding="utf-8")
    for skill in SKILLS:
        assert f"{TICK}{skill}{TICK}" in routing or "$" + skill in routing, f"missing workflow route: {skill}"

    golden = {path.parents[2].name for path in skill_root.glob("*/examples/golden/Cargo.toml")}
    assert golden == GOLDEN_OWNERS, f"golden example mismatch: {sorted(golden ^ GOLDEN_OWNERS)}"
    for skill in golden:
        reference_text = "\n".join(
            path.read_text(encoding="utf-8") for path in (skill_root / skill / "references").rglob("*.md")
        )
        assert "## Compiling Example" in reference_text, f"golden example not documented: {skill}"


def validate_agents() -> None:
    agent_files = list((ROOT / "agents").glob("*.md"))
    assert {frontmatter(path)["name"] for path in agent_files} == AGENTS
    for path in agent_files:
        content = path.read_text(encoding="utf-8").casefold()
        assert "read-only" in content and "do not edit" in content, f"agent is not read-only: {path.name}"


def run_powershell_hook(cwd: Path) -> str:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    assert shell, "PowerShell is required for hook scenarios"
    command = [
        shell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
        str(ROOT / "scripts" / "session-context.ps1"),
    ]
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    assert result.returncode == 0, f"SessionStart hook failed:\n{result.stdout}\n{result.stderr}"
    return result.stdout.strip()


def validate_hooks() -> None:
    assert {path.name for path in (ROOT / "hooks").glob("*.json")} == {"claude.json", "hooks.json"}
    claude = load_json(ROOT / "hooks" / "claude.json")
    codex = load_json(ROOT / "hooks" / "hooks.json")
    assert "CLAUDE_PLUGIN_ROOT" in json.dumps(claude)
    assert "PLUGIN_ROOT" in json.dumps(codex) and "CLAUDE_PLUGIN_ROOT" not in json.dumps(codex)
    for config in (claude, codex):
        assert set(config["hooks"]) == {"SessionStart"}
        handlers = config["hooks"]["SessionStart"]
        assert len(handlers) == 1 and len(handlers[0]["hooks"]) == 1
        hook = handlers[0]["hooks"][0]
        assert hook["type"] == "command" and 0 < hook["timeout"] <= 10

    setup_offer = "Rust setup is available on request; no tools or files were changed."
    nix_offer = "Nix/NixOS setup is available as a separate opt-in workflow"
    for path in (ROOT / "scripts" / "session-context.sh", ROOT / "scripts" / "session-context.ps1"):
        content = path.read_text(encoding="utf-8")
        assert not DISALLOWED_HOOK_COMMANDS.search(content), f"unsafe automatic hook command: {path}"
        assert setup_offer in content and nix_offer in content
        assert "locate-project" in content and "rustc" in content and "cargo" in content
        assert all(name in content for name in ("rust-workflow", "rust-review", "rust-verify"))
        assert "flake.nix" in content and "shell.nix" in content and "/etc/os-release" in content

    with tempfile.TemporaryDirectory(prefix="rust-engineering-hooks-") as temp:
        root = Path(temp)
        assert run_powershell_hook(root) == "", "non-Rust directory must be silent"
        rust = root / "rust-files"
        (rust / "src").mkdir(parents=True)
        (rust / "src" / "lib.rs").write_text("pub fn marker() {}\n", encoding="utf-8")
        assert setup_offer in run_powershell_hook(rust)
        (rust / "flake.nix").write_text("{}\n", encoding="utf-8")
        assert nix_offer in run_powershell_hook(rust)
    workspace_output = run_powershell_hook(ROOT / "checks" / "metadata-workspace")
    assert "Rust workspace detected:" in workspace_output and setup_offer in workspace_output


def validate_rule_examples(path: Path, content: str) -> Counter:
    lines = content.splitlines()
    counts: Counter = Counter()
    annotations = sum(1 for line in lines if RULE_EXAMPLE.fullmatch(line.strip()))
    in_rust = False
    for index, line in enumerate(lines):
        if line.strip() == RUST_FENCE:
            previous = lines[index - 1].strip() if index else ""
            match = RULE_EXAMPLE.fullmatch(previous)
            assert match, f"unclassified Rust block in {path}:{index + 1}"
            kind, attributes = match.group(1), match.group(2) or ""
            counts[kind] += 1
            if kind == "fragment":
                assert re.search(r"(?:^|;)\s*missing\s*:", attributes)
            elif kind == "fixture":
                assert re.search(r"(?:^|;)\s*dependencies\s*:", attributes)
            elif kind == "compile_fail":
                assert re.search(r"(?:^|;)\s*harness=(?:rustc|cargo)(?:;|$)", attributes)
                assert re.search(r'(?:^|;)\s*expected="[^"]+"(?:;|$)', attributes)
            in_rust = True
        elif line.strip() == FENCE and in_rust:
            in_rust = False
    assert not in_rust, f"unclosed Rust block in {path}"
    assert annotations == sum(counts.values()), f"orphan example annotation in {path}"
    return counts


def validate_rulebook(only_rule: str | None = None) -> tuple[int, Counter]:
    root = ROOT / "skills" / "rust-coding-rules" / "references"
    rule_root = root / "rules"
    paths = sorted(rule_root.glob("*.md"))
    ids = {path.stem for path in paths}
    assert len(ids) == len(paths) == 265
    assert {rule_id.split("-", 1)[0] for rule_id in ids} == RULE_CATEGORIES
    assert only_rule is None or only_rule in ids, f"unknown rule ID: {only_rule}"
    selected = [rule_root / f"{only_rule}.md"] if only_rule else paths
    counts: Counter = Counter()
    actual_aliases = {}
    for path in selected:
        rule_id = path.stem
        content = path.read_text(encoding="utf-8")
        assert content.splitlines()[0] == f"# {rule_id}"
        headings = set(re.findall(r"^## (.+?)\s*$", content, re.MULTILINE))
        alias_match = re.search(r"\]\(([a-z0-9-]+)\.md\)", content) if "## Canonical Rule" in content else None
        if alias_match:
            actual_aliases[rule_id] = alias_match.group(1)
            assert {"Canonical Rule", "Alias Reason", "Preserved Guidance"} <= headings
        else:
            assert RULE_SECTIONS <= headings, f"missing sections in {rule_id}: {sorted(RULE_SECTIONS - headings)}"
        counts.update(validate_rule_examples(path, content))
    if only_rule is None:
        assert actual_aliases == EXPECTED_ALIASES
        assert counts == {"compile_fail": 1, "fixture": 6, "fragment": 1131, "standalone": 3}
        indexes = {path.stem: path for path in (root / "categories").glob("*.md")}
        assert set(indexes) == RULE_CATEGORIES
        routing = (root / "routing.md").read_text(encoding="utf-8")
        for category, index in indexes.items():
            assert f"(categories/{category}.md)" in routing
            linked = set(re.findall(r"\]\(\.\./rules/([a-z0-9-]+)\.md\)", index.read_text(encoding="utf-8")))
            expected = {rule_id for rule_id in ids if rule_id.startswith(f"{category}-")}
            assert linked == expected, f"category index mismatch: {category}"
    unsafe_count = sum(
        1
        for skill in ("rust-unsafe", "rust-unsafe-ffi")
        for _ in (ROOT / "skills" / skill / "references" / "rules").glob("*.md")
    )
    assert unsafe_count == 47
    return len(paths), counts


def validate_evals(rule_ids: set[str]) -> int:
    evals = load_json(ROOT / "evals" / "evals.json")
    assert evals["schema_version"] == 8 and set(evals["suites"]) == set(SUITE_COUNTS)
    ids = []
    for suite, expected_count in SUITE_COUNTS.items():
        cases = evals["suites"][suite]
        assert len(cases) == expected_count
        if suite in KIND_COUNTS:
            assert Counter(case["kind"] for case in cases) == KIND_COUNTS[suite]
        for case in cases:
            ids.append(case["id"])
            assert case["prompt"] and case["tags"]
            expected = case["expected"]
            for key in ("entry_skill", "primary_profile", "fallback_profile"):
                value = expected.get(key)
                assert value is None or value in SKILLS, f"unknown profile in {case['id']}: {value}"
            for key in ("supporting_profiles", "forbidden_primary_profiles", "owner_profiles"):
                values = expected.get(key, [])
                assert set(values) <= SKILLS, f"unknown profiles in {case['id']}: {values}"
            assert len(expected.get("supporting_profiles", [])) <= 2
            if "max_rules" in expected:
                assert 0 <= expected["max_rules"] <= 8
            assert set(expected.get("rule_ids", [])) <= rule_ids
            assert set(expected.get("rejected_rule_ids", [])) <= rule_ids
            assert set(expected.get("categories", [])) <= RULE_CATEGORIES
    assert len(ids) == len(set(ids)) == 341

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                assert key not in {"source", "source_id", "source_file", "origin", "provenance"}
                yield from walk(item)
        elif isinstance(value, list):
            for item in value:
                yield from walk(item)
        else:
            yield value

    list(walk(evals))
    return len(ids)


def validate_installer(config: dict) -> None:
    python_installer = REPOSITORY_ROOT / "installers" / "install.py"
    node_installer = REPOSITORY_ROOT / "installers" / "install.mjs"
    for path in (python_installer, node_installer):
        assert path.is_file()
        text = path.read_text(encoding="utf-8")
        assert "config.json" in text
        assert not re.search(r'^(?:MARKETPLACE|PLUGIN|REPOSITORY|REF|TARGETS|SCOPES)\s*=\s*["\']', text, re.MULTILINE)
    python_text = python_installer.read_text(encoding="utf-8")
    expected_url = f"https://raw.githubusercontent.com/{config['repository']}/{config['ref']}/installers/config.json"
    match = re.search(r'^CONFIG_URL = "([^"]+)"$', python_text, re.MULTILINE)
    assert match and match.group(1) == expected_url

    node = shutil.which("node")
    assert node, "Node.js is required to validate the npx installer"
    for target, scope in (("all", "user"), ("claude-code", "local")):
        common = ["--target", target, "--scope", scope, "--dry-run"]
        py = subprocess.run([sys.executable, str(python_installer), *common], text=True, capture_output=True, check=False)
        js = subprocess.run([node, str(node_installer), *common], text=True, capture_output=True, check=False)
        assert py.returncode == js.returncode == 0, f"installer dry-run failed:\n{py.stderr}\n{js.stderr}"
        assert py.stdout.replace("\r\n", "\n") == js.stdout.replace("\r\n", "\n"), "installer plans differ"

    empty_path = dict(os.environ)
    empty_path["PATH"] = ""
    for command in (
        [sys.executable, str(python_installer), "--target", "claude-code", "--yes"],
        [node, str(node_installer), "--target", "claude-code", "--yes"],
    ):
        result = subprocess.run(command, text=True, capture_output=True, check=False, env=empty_path)
        assert result.returncode == 2 and "not found" in result.stderr.casefold()

    if os.name == "nt":
        with tempfile.TemporaryDirectory() as directory:
            shim_directory = Path(directory) / "cli shims"
            shim_directory.mkdir()
            (shim_directory / "claude.cmd").write_text(
                '@echo off\nif "%~3"=="--json" echo {}\nif "%~4"=="--json" echo {}\n',
                encoding="utf-8",
            )
            shim_path = dict(os.environ)
            shim_path["PATH"] = str(shim_directory)
            result = subprocess.run(
                [node, str(node_installer), "--target", "claude-code", "--scope", "local", "--yes"],
                text=True,
                capture_output=True,
                check=False,
                env=shim_path,
            )
            assert result.returncode == 0, f"Node installer could not run a Windows command shim:\n{result.stderr}"

    spec = importlib.util.spec_from_file_location("rust_engineering_installer", python_installer)
    assert spec and spec.loader
    installer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(installer)
    installer.shutil = types.SimpleNamespace(which=lambda name: name)
    commands = []
    installer.run = commands.append
    responses = iter([
        {"marketplaces": [{"name": config["marketplace"], "source": f"https://github.com/{config['repository']}"}]},
        {"installed": [{"name": config["plugin"], "marketplaceName": config["marketplace"], "installed": True}]},
    ])
    installer.run_json = lambda _: next(responses)
    installer.install_codex()
    assert commands == [
        ["codex", "plugin", "marketplace", "upgrade", config["marketplace"]],
    ]

    responses = iter([
        {"marketplaces": []},
        {"installed": []},
    ])
    commands.clear()
    installer.run_json = lambda _: next(responses)
    installer.install_codex()
    assert commands == [
        ["codex", "plugin", "marketplace", "add", config["repository"], "--ref", config["ref"]],
        ["codex", "plugin", "add", f"{config['plugin']}@{config['marketplace']}"],
    ]

    responses = iter([
        {"marketplaces": [{"name": config["marketplace"], "source": config["repository"]}]},
        [{"name": config["plugin"], "marketplaceName": config["marketplace"]}],
    ])
    commands.clear()
    installer.run_json = lambda _: next(responses)
    installer.install_claude("local")
    assert commands == [
        ["claude", "plugin", "marketplace", "update", config["marketplace"]],
        ["claude", "plugin", "update", f"{config['plugin']}@{config['marketplace']}", "--scope", "local"],
    ]
    try:
        installer.assert_expected_source({"name": config["marketplace"], "source": "another/location"})
    except RuntimeError as error:
        assert "collision" in str(error)
    else:
        raise AssertionError("marketplace source collision was accepted")


def validate_metadata_fixture() -> None:
    fixture = ROOT / "checks" / "metadata-workspace"
    cargo = shutil.which("cargo")
    assert cargo, "cargo is required for the metadata fixture"
    command = [
        cargo, "metadata", "--format-version", "1", "--locked", "--offline",
        "--manifest-path", str(fixture / "Cargo.toml"), "--no-deps",
    ]
    result = subprocess.run(command, cwd=fixture, text=True, capture_output=True, check=False)
    assert result.returncode == 0, f"cargo metadata fixture failed:\n{result.stdout}\n{result.stderr}"
    metadata = json.loads(result.stdout)
    packages = {package["name"]: package for package in metadata["packages"]}
    assert set(packages) == {"metadata-app", "metadata-local-util"}
    app = packages["metadata-app"]
    assert app["edition"] == "2024" and app["rust_version"] == "1.85"
    assert app["features"] == {"default": [], "util": ["dep:renamed-util"]}


def validate_json_fixtures() -> None:
    low = ROOT / "checks" / "low-level"
    assert {path.name for path in low.glob("*.json")} == {
        "timings-path.json", "sanitizer-matrix.json", "cross-resolution.json", "command-effects.json",
    }
    effects = load_json(low / "command-effects.json")["cases"]
    assert len(effects) == 6
    assert [case for case in effects if case["automatic_allowed"]] == [{
        "command": "cargo metadata --format-version 1 --locked --offline",
        "effects": ["read-only-host"],
        "automatic_allowed": True,
    }]
    cross = load_json(low / "cross-resolution.json")
    assert cross["host"] != cross["target"] and set(cross["expected_missing"]) == {
        "linker", "runner-or-target-execution-environment", "target-native-dependencies",
    }

    cargo = ROOT / "checks" / "cargo-tooling"
    assert {path.name for path in cargo.glob("*.json")} == {
        "generate-effects.json", "nextest-coverage-matrix.json", "machete-contract.json",
        "worktree-layout.json", "clippy-policy.json",
    }
    assert not any(case["automatic_allowed"] for case in load_json(cargo / "generate-effects.json")["cases"])
    machete = load_json(cargo / "machete-contract.json")
    assert machete["exit_codes"] == {"0": "clean", "1": "findings", "2": "processing-error"}
    clippy = load_json(cargo / "clippy-policy.json")
    assert not clippy["remediation"]["automatic_source_fix"]


def validate_examples() -> None:
    cargo = shutil.which("cargo")
    assert cargo, "cargo is required for golden examples"
    with tempfile.TemporaryDirectory(prefix="rust-engineering-examples-") as target:
        for skill in sorted(GOLDEN_OWNERS):
            manifest = ROOT / "skills" / skill / "examples" / "golden" / "Cargo.toml"
            commands = [[
                cargo, "test", "--quiet", "--offline", "--locked", "--manifest-path", str(manifest),
                "--target-dir", str(Path(target) / skill),
            ]]
            if skill == "rust-cargo-build":
                commands.append(commands[0] + ["--features", "fast"])
            for command in commands:
                result = subprocess.run(command, cwd=manifest.parent, text=True, capture_output=True, check=False)
                assert result.returncode == 0, (
                    f"golden example failed: {skill}\ncommand: {' '.join(command)}\n"
                    f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                )


def validate_rulebook_examples(rule_id: str | None = None) -> tuple[Counter, str | None]:
    generator = ROOT / "checks" / "rulebook" / "gen.py"
    with tempfile.TemporaryDirectory(prefix="rust-engineering-rulebook-") as target:
        root = Path(target)
        output = root / "generated"
        selection = ["--rule", rule_id] if rule_id else ["--all"]
        generated = subprocess.run(
            [sys.executable, str(generator), *selection, "--out", str(output)],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        assert generated.returncode == 0, f"rulebook generator failed:\n{generated.stdout}\n{generated.stderr}"
        manifest = load_json(output / "manifest.json")
        counts = Counter(manifest["counts"])

        rustc = shutil.which("rustc")
        cargo = shutil.which("cargo")
        assert rustc and cargo, "Rust toolchain is required for rule examples"
        binaries = root / "standalone-bin"
        binaries.mkdir()
        for path in sorted((output / "standalone").glob("*.rs")):
            command = [rustc, "--edition=2024", str(path), "-o", str(binaries / path.stem)]
            result = subprocess.run(command, cwd=output, text=True, capture_output=True, check=False)
            assert result.returncode == 0, f"standalone rule example failed: {path.name}\n{result.stderr}"

        fixture_skip = None
        if list((output / "examples").glob("*.rs")):
            command = [
                cargo, "check", "--quiet", "--locked", "--offline", "--examples",
                "--manifest-path", str(output / "Cargo.toml"), "--target-dir", str(root / "cargo-target"),
            ]
            result = subprocess.run(command, cwd=output, text=True, capture_output=True, check=False)
            if result.returncode != 0 and OFFLINE_CACHE_MISS.search(result.stderr + result.stdout):
                fixture_skip = "environment skip: a locked rulebook fixture dependency is absent from the local Cargo cache"
            else:
                assert result.returncode == 0, f"rulebook fixtures failed:\n{result.stdout}\n{result.stderr}"

        records = {record["generated"]: record for record in manifest["records"] if "generated" in record}
        for path in sorted((output / "compile_fail").glob("*.rs")):
            record = records[f"compile_fail/{path.name}"]
            attributes = record["attributes"]
            expected = str(attributes["expected"])
            if attributes["harness"] == "rustc":
                command = [rustc, "--edition=2024", str(path), "-o", str(binaries / path.stem)]
            else:
                shutil.copy2(path, output / "examples" / path.name)
                command = [
                    cargo, "check", "--quiet", "--locked", "--offline", "--example", path.stem,
                    "--manifest-path", str(output / "Cargo.toml"),
                    "--target-dir", str(root / "cargo-target-compile-fail"),
                ]
            result = subprocess.run(command, cwd=output, text=True, capture_output=True, check=False)
            diagnostic = result.stderr + result.stdout
            assert result.returncode != 0, f"compile_fail unexpectedly compiled: {path.name}"
            assert expected.casefold() in diagnostic.casefold(), f"compile_fail diagnostic mismatch: {path.name}"
        return counts, fixture_skip


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--examples", action="store_true", help="compile declared golden and rulebook examples")
    parser.add_argument("--rule", help="validate one addressable coding rule")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.rule:
        _, counts = validate_rulebook(args.rule)
        fixture_skip = None
        if args.examples:
            counts, fixture_skip = validate_rulebook_examples(args.rule)
        print(
            f"OK: rule {args.rule}, {sum(counts.values())} classified Rust blocks "
            + ("compiled where declared" if args.examples else "statically checked")
        )
        if fixture_skip:
            print(fixture_skip)
        return

    config = validate_manifests_and_catalogs()
    validate_notices_and_identity()
    validate_references()
    validate_skills()
    validate_links()
    validate_agents()
    validate_hooks()
    rule_count, rule_examples = validate_rulebook()
    rule_ids = {path.stem for path in (ROOT / "skills" / "rust-coding-rules" / "references" / "rules").glob("*.md")}
    eval_count = validate_evals(rule_ids)
    validate_installer(config)
    validate_metadata_fixture()
    validate_json_fixtures()
    fixture_skip = None
    if args.examples:
        validate_examples()
        rule_examples, fixture_skip = validate_rulebook_examples()
    print(
        f"OK: {len(SKILLS)} skills, {len(AGENTS)} read-only agents, {eval_count} eval scenarios, "
        f"{rule_count} coding rules, 47 unsafe/FFI rules, {len(GOLDEN_OWNERS)} golden examples, "
        f"{sum(rule_examples.values())} classified rule examples"
        + (" compiled" if args.examples else " statically checked")
    )
    if fixture_skip:
        print(fixture_skip)


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
