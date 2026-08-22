#!/usr/bin/env python3
"""Validate the dual-host Rust engineering plugin with the standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = ROOT.parents[1]
AGENTS = {"rust-scout", "rust-reviewer", "rust-verifier"}
ENTRY_SKILLS = {"rust-workflow", "rust-review", "rust-verify"}
DISALLOWED_HOOK_COMMANDS = re.compile(
    r"\bcargo\s+(?:fmt|test|check|clippy|build|run|update|fetch|install|publish|bench|doc|fix)\b"
    r"|\bnix\s+(?:build|flake\s+(?:check|update)|develop)\b"
    r"|\b(?:curl|wget|Invoke-WebRequest)\b",
    re.IGNORECASE,
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
            target_path = (path.parent / relative).resolve()
            assert target_path.exists(), f"broken link in {path}: {target}"


def validate_manifests() -> None:
    claude = load_json(ROOT / ".claude-plugin" / "plugin.json")
    codex = load_json(ROOT / ".codex-plugin" / "plugin.json")
    assert (ROOT / "LICENSE").is_file()
    assert claude["name"] == codex["name"] == "rust-engineering"
    assert claude["version"] == codex["version"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", claude["version"])
    assert tuple(map(int, claude["version"].split("."))) >= (0, 2, 0)
    assert claude["author"]["name"] and codex["author"]["name"]
    assert all(isinstance(keyword, str) and keyword for keyword in claude["keywords"])
    assert all(isinstance(keyword, str) and keyword for keyword in codex["keywords"])
    assert set(claude) <= {
        "$schema", "name", "version", "description", "author", "license", "keywords", "hooks",
    }
    assert claude["hooks"] == "./hooks/claude.json"
    assert (ROOT / claude["hooks"]).is_file()
    assert codex["skills"] == "./skills/"
    assert "hooks" not in codex
    interface = codex["interface"]
    assert interface["displayName"] and interface["shortDescription"] and interface["longDescription"]
    assert interface["defaultPrompt"] and "$rust-workflow" in interface["defaultPrompt"][0]

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


def validate_skills(expected_skills: set[str], example_owners: set[str]) -> None:
    skill_root = ROOT / "skills"
    skill_dirs = {path.name for path in skill_root.iterdir() if path.is_dir()}
    assert skill_dirs == expected_skills, f"unexpected skills: {sorted(skill_dirs ^ expected_skills)}"
    assert len(skill_dirs) == 43
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
    assert len(actual_examples) == 21
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
        assert "rust-workflow" in content and "rust-review" in content and "rust-verify" in content


def validate_evals(skills: set[str]) -> int:
    evals = load_json(ROOT / "evals" / "evals.json")
    assert evals["schema_version"] == 2
    cases = evals["cases"]
    ids = [case["id"] for case in cases]
    assert len(cases) == 106 and len(ids) == len(set(ids)), "routing corpus must have 106 unique cases"
    modes = Counter(case["mode"] for case in cases)
    assert modes == {"manual": 43, "automatic": 43, "contrast": 8, "negative": 12}

    manual_profiles = set()
    automatic_profiles = set()
    for case in cases:
        expected = case["expected"]
        entry = expected["entry_skill"]
        primary = expected["primary_profile"]
        supporting = expected["supporting_profiles"]
        forbidden = expected["forbidden_primary_profiles"]
        assert entry in skills | {None}
        assert primary in skills | {None}
        assert len(supporting) <= 2 and set(supporting) <= skills
        assert set(forbidden) <= skills and primary not in forbidden
        assert case["prompt"] and isinstance(case["mutation"], bool) and case["tags"]
        if case["mode"] == "manual":
            assert entry == primary and primary is not None
            manual_profiles.add(primary)
        elif case["mode"] == "automatic":
            assert primary is not None
            automatic_profiles.add(primary)
            if case["mutation"]:
                assert entry == "rust-workflow"
        elif case["mode"] == "negative":
            assert entry is None and primary is None and not supporting and not forbidden
    assert manual_profiles == automatic_profiles == skills
    return len(cases)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--examples", action="store_true", help="compile and test all dependency-free golden examples")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    validate_manifests()
    coverage, owners, example_owners = validate_source_coverage()
    expected_skills = owners | {"rust-workflow", "rust-verify"}
    assert ENTRY_SKILLS <= expected_skills
    validate_skills(expected_skills, example_owners)
    validate_links()
    validate_agents()
    validate_hooks()
    eval_count = validate_evals(expected_skills)
    if args.examples:
        validate_examples(example_owners)
    print(
        f"OK: {len(expected_skills)} skills, {len(AGENTS)} read-only agents, "
        f"{eval_count} routing evals, {coverage['summary']['adapted']} adapted source skills, "
        f"{coverage['summary']['out_of_scope']} explicit exclusions, {len(example_owners)} golden examples"
        + (" compiled" if args.examples else " statically checked")
    )


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, KeyError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
