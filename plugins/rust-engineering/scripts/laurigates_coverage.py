#!/usr/bin/env python3
"""Stage Laurigates Rust-tool families and maintain their pinned coverage ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from collections import Counter
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
REPOSITORY = PLUGIN.parents[1]
SOURCE = REPOSITORY / "references" / "claude-plugins_laurigates"
LEDGER = PLUGIN / "provenance" / "laurigates-coverage.json"
INDEX = PLUGIN / "provenance" / "laurigates-index.md"
STAGING = PLUGIN / "provenance" / ".laurigates-staging"

REVISION = "a1e72ed186b97555256d8c058ff291c182332df7"
STATUSES = {"pending", "in_progress", "adapted", "merged", "duplicate", "excluded"}
BLOCK_STATUSES = {"pending", "retained", "corrected", "fragment", "rejected"}
FENCE = re.compile(r"^```([^\n`]*)\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)


def family(owner: str, supporting: list[str], target: str, evidence: list[str], tool: str) -> dict:
    return {
        "owner": owner,
        "supporting": supporting,
        "target": target,
        "evidence": evidence,
        "tool": tool,
    }


FAMILY_CONFIG = {
    "cargo-generate": family(
        "rust-cargo-build",
        ["rust-workspace", "rust-research"],
        "skills/rust-cargo-build/references/cargo-tooling/cargo-generate.md",
        ["cargo-generate-guide", "cargo-generate-api", "cargo-metadata"],
        "cargo-generate",
    ),
    "cargo-nextest": family(
        "rust-testing",
        ["rust-verify", "debugging"],
        "skills/rust-testing/references/cargo-tooling/cargo-nextest.md",
        ["nextest-running", "nextest-config", "nextest-coverage"],
        "cargo-nextest",
    ),
    "cargo-llvm-cov": family(
        "rust-testing",
        ["rust-verify", "rust-research"],
        "skills/rust-testing/references/cargo-tooling/cargo-llvm-cov.md",
        ["cargo-llvm-cov", "nextest-coverage"],
        "cargo-llvm-cov",
    ),
    "cargo-machete": family(
        "rust-dependencies",
        ["rust-cargo-build", "rust-verify"],
        "skills/rust-dependencies/references/cargo-tooling/cargo-machete.md",
        ["cargo-machete", "cargo-metadata"],
        "cargo-machete",
    ),
    "cargo-worktree-builds": family(
        "rust-cargo-build",
        ["rust-performance", "rust-verify"],
        "skills/rust-cargo-build/references/cargo-tooling/cargo-worktree-builds.md",
        ["cargo-build-cache", "cargo-config", "git-worktree", "sccache-rust"],
        "cargo",
    ),
    "clippy-advanced": family(
        "rust-style-clippy",
        ["rust-stable", "rust-verify"],
        "skills/rust-style-clippy/references/cargo-tooling/clippy-advanced.md",
        ["clippy-config", "cargo-lints", "clippy-catalog"],
        "clippy",
    ),
}
FAMILY_ORDER = list(FAMILY_CONFIG)

EVIDENCE = {
    "cargo-generate-guide": ("https://cargo-generate.github.io/cargo-generate/", "cargo-generate templates, variables, hooks, and CLI"),
    "cargo-generate-api": ("https://docs.rs/cargo-generate/latest/cargo_generate/struct.GenerateArgs.html", "resolved cargo-generate argument semantics"),
    "cargo-metadata": ("https://doc.rust-lang.org/cargo/commands/cargo-metadata.html", "Cargo workspace and target-directory metadata"),
    "nextest-running": ("https://nexte.st/docs/running/", "nextest execution, filtering, and doctest boundary"),
    "nextest-config": ("https://nexte.st/docs/configuration/reference/", "nextest profiles, groups, retries, threads, timeouts, and JUnit"),
    "nextest-coverage": ("https://nexte.st/docs/integrations/test-coverage/", "nextest coverage integration"),
    "cargo-llvm-cov": ("https://github.com/taiki-e/cargo-llvm-cov/blob/main/README.md", "cargo-llvm-cov instrumentation, reporting, and unstable modes"),
    "cargo-machete": ("https://github.com/bnjbvr/cargo-machete", "cargo-machete scanning, metadata, and exit semantics"),
    "cargo-build-cache": ("https://doc.rust-lang.org/cargo/reference/build-cache.html", "Cargo target and build directory behavior"),
    "cargo-config": ("https://doc.rust-lang.org/cargo/reference/config.html", "Cargo configuration precedence and build directory templates"),
    "git-worktree": ("https://git-scm.com/docs/git-worktree.html", "Git linked worktree administration"),
    "sccache-rust": ("https://github.com/mozilla/sccache/blob/main/docs/Rust.md", "sccache Rust compiler-wrapper behavior"),
    "clippy-config": ("https://doc.rust-lang.org/clippy/lint_configuration.html", "Clippy typed configuration keys"),
    "cargo-lints": ("https://doc.rust-lang.org/cargo/reference/manifest.html#the-lints-section", "Cargo lint levels, priorities, and workspace inheritance"),
    "clippy-catalog": ("https://rust-lang.github.io/rust-clippy/", "toolchain-specific Clippy lint catalog"),
}

WRONG = re.compile(
    r"cargo\s+machete\s+--fix|\.cargo-machete\.toml|machete:ignore|"
    r"test-threads\s*=\s*0|--fail-under-branches|"
    r"touch\s+src[/\\]|--message-format\s+(?:json|json-pretty)",
    re.IGNORECASE,
)
UNSAFE_EFFECT = re.compile(
    r"cargo\s+install|rustup\s+(?:update|component\s+add|target\s+add)|"
    r"\bsudo\b|\bsysctl\b|--allow-commands|--open\b|codecov|coveralls|"
    r"cargo\s+clean|cargo\s+machete\s+--with-metadata",
    re.IGNORECASE,
)
TOOL_PATTERNS = {
    "cargo": r"\bcargo\b",
    "cargo-generate": r"\bcargo(?:-generate|\s+generate)\b",
    "cargo-nextest": r"\bcargo(?:-nextest|\s+nextest)\b",
    "cargo-llvm-cov": r"\bcargo(?:-llvm-cov|\s+llvm-cov)\b",
    "cargo-machete": r"\bcargo(?:-machete|\s+machete)\b",
    "clippy": r"\bclippy(?:\.toml|::|\b)|\bcargo\s+clippy\b",
    "git": r"\bgit\s+(?:worktree|rev-parse|status|diff)\b",
    "sccache": r"\bsccache\b",
    "llvm-profdata": r"\bllvm-profdata\b",
    "grcov": r"\bgrcov\b",
    "tarpaulin": r"\btarpaulin\b",
}
COMMAND_LANGUAGES = {"bash", "sh", "shell", "powershell", "console", "cmd"}


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(SOURCE).parts
        and "graphify-out" not in path.relative_to(SOURCE).parts
    )


def relative(path: Path) -> str:
    return path.relative_to(SOURCE).as_posix()


def family_root(name: str) -> Path:
    return SOURCE / "rust-plugin" / "skills" / name


def family_markdown(name: str) -> list[Path]:
    return sorted(family_root(name).glob("*.md"))


def rust_development_markdown() -> list[Path]:
    return sorted((SOURCE / "rust-plugin" / "skills" / "rust-development").glob("*.md"))


def selected_markdown() -> list[Path]:
    return sorted({path for name in FAMILY_ORDER for path in family_markdown(name)} | set(rust_development_markdown()))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int | None:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return None


def nonempty_line_count(path: Path) -> int:
    return sum(bool(line.strip()) for line in path.read_text(encoding="utf-8").splitlines())


def normalized_block(body: str) -> str:
    return body.replace("\r\n", "\n").rstrip()


def block_digest(body: str) -> str:
    return hashlib.sha256(normalized_block(body).encode()).hexdigest()


def family_for_path(path: Path) -> str:
    name = path.parent.name
    return name if name in FAMILY_CONFIG else "rust-development"


def tools_for(body: str, family_name: str) -> list[str]:
    tools = {name for name, pattern in TOOL_PATTERNS.items() if re.search(pattern, body, re.IGNORECASE | re.MULTILINE)}
    if not tools:
        tools.add(FAMILY_CONFIG[family_name]["tool"] if family_name in FAMILY_CONFIG else "shell")
    return sorted(tools)


def effects_for(body: str, family_name: str) -> list[str]:
    effects: set[str] = set()
    if re.search(r"cargo\s+install|rustup\s+(?:update|component\s+add|target\s+add)", body, re.IGNORECASE):
        effects.update({"install", "network"})
    if re.search(r"https?://|git\s+clone|cargo\s+generate\s+--git", body, re.IGNORECASE):
        effects.add("network")
    if re.search(r"cargo\s+(?:generate|new)|--init\b|--overwrite\b|--force\b|cargo\s+clippy.*--fix", body, re.IGNORECASE):
        effects.add("source-writes")
    if re.search(r"--with-metadata|Cargo\.lock", body, re.IGNORECASE) and family_name == "cargo-machete":
        effects.add("lockfile")
    if re.search(r"cargo\s+(?:build|check|test|nextest|clippy|llvm-cov)|CARGO_TARGET_DIR", body, re.IGNORECASE):
        effects.add("build-artifacts")
    if re.search(r"llvm-cov|junit|lcov|cobertura|html|json", body, re.IGNORECASE):
        effects.add("report-artifacts")
    if re.search(r"cargo\s+(?:test|nextest|run)|system::command", body, re.IGNORECASE):
        effects.add("process-execution")
    if re.search(r"--open\b", body, re.IGNORECASE):
        effects.add("gui")
    if re.search(r"codecov|coveralls|upload", body, re.IGNORECASE):
        effects.add("upload")
    if re.search(r"sudo|sysctl", body, re.IGNORECASE):
        effects.add("global-config")
    return sorted(effects or {"read-only-host"})


def command_contract(body: str, language: str, family_name: str, decision: str, evidence_ids: list[str]) -> dict | None:
    tools = tools_for(body, family_name)
    if language not in COMMAND_LANGUAGES and not any(re.search(pattern, body, re.IGNORECASE) for pattern in TOOL_PATTERNS.values()):
        return None
    nightly = bool(re.search(r"\+nightly|-Z\b|branch coverage|doctest coverage", body, re.IGNORECASE))
    external = any(tool.startswith("cargo-") or tool in {"git", "sccache", "llvm-profdata", "grcov", "tarpaulin"} for tool in tools)
    channel = "nightly" if nightly else ("external" if external else "project")
    version = {
        "nightly": "project-pinned nightly and resolved external-tool version",
        "external": "already-installed, resolved tool version",
        "project": "project-selected Rust/Cargo/Clippy toolchain",
    }[channel]
    components = [f"preinstalled `{tool}` with version/help checked" for tool in tools if tool not in {"cargo", "clippy"}]
    return {
        "tools": tools,
        "applicable_version": version,
        "status": channel,
        "os_constraints": ["resolve shell, filesystem, and process semantics from the project host"],
        "target_constraints": ["resolve host and selected Cargo target from project state"],
        "required_components_and_dependencies": components,
        "side_effects": effects_for(body, family_name),
        "evidence_ids": evidence_ids,
        "decision": decision,
        "reason": "Source command was classified individually; product execution still requires resolved --version/--help, project policy, and authorization for every effect.",
    }


def target_for_family(name: str) -> str:
    return FAMILY_CONFIG[name]["target"]


def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    counts = Counter(entry["status"] for entry in data["entries"])
    block_counts = Counter(block["status"] for block in data["blocks"])
    data["summary"] = {
        "source_files": len(data["entries"]),
        **{status: counts[status] for status in sorted(STATUSES)},
        "block_decisions": {status: block_counts[status] for status in sorted(BLOCK_STATUSES)},
        "command_blocks": sum("command_contract" in block for block in data["blocks"]),
        "rust_blocks": sum(block["language"] == "rust" for block in data["blocks"]),
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def initialize(force: bool) -> None:
    if LEDGER.exists() and not force:
        raise SystemExit(f"ledger already exists: {LEDGER}")
    selected = selected_markdown()
    selected_set = set(selected)
    entries = [
        {
            "source_path": relative(path),
            "source_sha256": digest(path),
            "source_bytes": path.stat().st_size,
            "source_lines": line_count(path),
            "status": "pending",
            "target_paths": [],
            "reason": "Awaiting sequential Laurigates review.",
            "selected": path in selected_set or relative(path) == "LICENSE",
        }
        for path in source_files()
    ]
    blocks: dict[str, dict] = {}
    occurrences = 0
    for path in selected:
        family_name = family_for_path(path)
        for index, match in enumerate(FENCE.finditer(path.read_text(encoding="utf-8")), start=1):
            occurrences += 1
            body = normalized_block(match.group(2))
            sha = block_digest(body)
            item = blocks.setdefault(
                sha,
                {
                    "source_sha256": sha,
                    "language": match.group(1).strip().lower() or "plain",
                    "status": "pending",
                    "target_paths": [],
                    "reason": "Awaiting family review.",
                    "evidence_ids": [],
                    "occurrences": [],
                },
            )
            item["occurrences"].append({"source_path": relative(path), "block_index": index, "family": family_name})
    evidence = {
        key: {"url": url, "subject": subject, "authority": "official-rust" if "doc.rust-lang.org" in url else "tool-owner", "channel": "current-or-resolved", "reviewed_on": "2026-08-23"}
        for key, (url, subject) in EVIDENCE.items()
    }
    data = {
        "schema_version": 1,
        "source": {
            "name": "laurigates/claude-plugins",
            "relative_path": "references/claude-plugins_laurigates",
            "revision": REVISION,
            "commit_date": "2026-08-23T09:39:01Z",
            "plugin_version": "1.7.0",
            "license": "MIT",
            "copyright": "Copyright (c) 2026 Lauri Gates",
        },
        "statuses": sorted(STATUSES),
        "block_statuses": sorted(BLOCK_STATUSES),
        "family_order": FAMILY_ORDER,
        "source_metrics": {
            "selected_markdown_files": len(selected),
            "selected_markdown_lines": sum(nonempty_line_count(path) for path in selected),
            "selected_markdown_line_basis": "nonempty",
            "source_blocks": occurrences,
            "unique_source_blocks": len(blocks),
            "source_block_aliases": occurrences - len(blocks),
        },
        "evidence": evidence,
        "entries": entries,
        "blocks": sorted(blocks.values(), key=lambda item: item["source_sha256"]),
    }
    save(data)
    print(f"initialized {len(entries)} files and {occurrences}/{len(blocks)} source blocks")


def entries_by_path(data: dict) -> dict[str, dict]:
    return {entry["source_path"]: entry for entry in data["entries"]}


def blocks_by_hash(data: dict) -> dict[str, dict]:
    return {block["source_sha256"]: block for block in data["blocks"]}


def stage_family(name: str) -> None:
    data = load()
    if any(entry["status"] == "in_progress" for entry in data["entries"]):
        raise SystemExit("finish the active family first")
    entries = entries_by_path(data)
    paths = family_markdown(name)
    if entries[relative(family_root(name) / "SKILL.md")]["status"] != "pending":
        raise SystemExit(f"family already staged or finalized: {name}")
    destination = STAGING / name
    destination.mkdir(parents=True, exist_ok=False)
    for path in paths:
        entries[relative(path)].update(status="in_progress", target_paths=[target_for_family(name)], reason=f"Sequential review of {name} is in progress.")
        shutil.copy2(path, destination / path.name)
    save(data)
    print(f"staged {name}: {', '.join(relative(path) for path in paths)}")


def classify_family_blocks(data: dict, family_name: str, paths: list[Path], evidence_ids: list[str], target: str | None) -> None:
    blocks = blocks_by_hash(data)
    seen: set[str] = set()
    for path in paths:
        for match in FENCE.finditer(path.read_text(encoding="utf-8")):
            body = normalized_block(match.group(2))
            sha = block_digest(body)
            if sha in seen:
                continue
            seen.add(sha)
            status = "rejected" if WRONG.search(body) or UNSAFE_EFFECT.search(body) else ("corrected" if command_contract(body, match.group(1).strip().lower(), family_name, "corrected", evidence_ids) else "fragment")
            reason = {
                "rejected": "Rejected: obsolete syntax, unsafe automatic side effect, or source-wide preference is not product guidance.",
                "corrected": "Command-bearing source example retained only as a reviewed algorithm; exact syntax and effects were corrected by the product reference.",
                "fragment": "Configuration or code fragment is useful evidence but is not shipped as a universal, compile-tested recipe.",
            }[status]
            item = blocks[sha]
            item.update(status=status, target_paths=[target] if target and status == "corrected" else [], reason=reason, evidence_ids=evidence_ids)
            contract = command_contract(body, item["language"], family_name, status, evidence_ids)
            if contract:
                item["command_contract"] = contract
            if item["language"] == "rust":
                item["rust_example"] = "fragment" if status != "rejected" else None


def finalize_family(name: str) -> None:
    data = load()
    entries = entries_by_path(data)
    staging = STAGING / name
    if not staging.is_dir():
        raise SystemExit(f"family is not staged: {name}")
    source = family_root(name) / "SKILL.md"
    target = target_for_family(name)
    target_path = PLUGIN / target
    if not target_path.is_file():
        raise SystemExit(f"write the adapted target before finalizing: {target}")
    marker = f"<!-- laurigates-source-family: {name}; source={relative(source)}; sha256={digest(source)}; revision={REVISION} -->"
    if marker not in target_path.read_text(encoding="utf-8"):
        raise SystemExit(f"missing or stale provenance marker in {target}")
    paths = family_markdown(name)
    classify_family_blocks(data, name, paths, FAMILY_CONFIG[name]["evidence"], target)
    for path in paths:
        status = "adapted" if path.name == "SKILL.md" else "merged"
        entries[relative(path)].update(
            status=status,
            target_paths=[target],
            reason="Canonical workflow rewritten behind current tool-owner evidence and effect gates." if status == "adapted" else "Supporting reference merged into the reviewed family protocol.",
        )
    shutil.rmtree(staging)
    if STAGING.exists() and not any(STAGING.iterdir()):
        STAGING.rmdir()
    save(data)
    print(f"finalized {name} -> {target}")


def exclusion_reason(path: str) -> str:
    if path == "rust-plugin/skills/mockito-http-mocking/SKILL.md":
        return f"Excluded `{path}`: HTTP mocking was explicitly out of scope and receives no product reference, trigger, or positive eval."
    if path.startswith(".claude/rules/"):
        return f"Excluded `{path}`: Claude-repository authoring policy is not Rust tooling knowledge or dual-host runtime policy."
    if path.startswith(".claude/skills/"):
        return f"Excluded `{path}`: upstream plugin-authoring skill is outside the retained Rust plugin scope."
    if path.startswith(".claude/scripts/"):
        return f"Excluded `{path}`: upstream helper script would add unrelated source/runtime behavior."
    if path.startswith((".claude/", ".claude-plugin/")) or path in {".mcp.json", ".claude-code-version-check.json", ".obsidian-cli-version-check.json"}:
        return f"Excluded `{path}`: source-host settings, MCP, or marketplace metadata are replaced by this product's existing dual-host interface."
    if path.startswith("rust-plugin/"):
        return f"Excluded `{path}`: upstream plugin packaging, catalog, or release history is provenance evidence rather than runtime guidance."
    if Path(path).name in {"README.md", "MIGRATION.md", "CLAUDE.md"}:
        return f"Excluded `{path}`: source repository documentation describes upstream development and installation, not product runtime behavior."
    return f"Excluded `{path}`: source CI, release, lint, editor, security, or repository metadata is not required by the reviewed Rust tooling integration."


def finalize_remaining() -> None:
    data = load()
    if any(entry["status"] == "in_progress" for entry in data["entries"]):
        raise SystemExit("finish the active family first")
    entries = entries_by_path(data)
    for name in FAMILY_ORDER:
        if entries[relative(family_root(name) / "SKILL.md")]["status"] != "adapted":
            raise SystemExit(f"family not finalized: {name}")
    merged_targets = [target_for_family(name) for name in FAMILY_ORDER] + ["skills/rust-research/references/low-level-tooling-baseline.md"]
    development = rust_development_markdown()
    classify_family_blocks(data, "rust-development", development, list(EVIDENCE), None)
    for path in development:
        entries[relative(path)].update(
            status="merged",
            target_paths=merged_targets,
            reason="Umbrella Rust material audited; only missing external-tool boundary details were merged into existing owners and baseline.",
        )
    notices = ["THIRD_PARTY_NOTICES.md", "provenance/THIRD_PARTY_NOTICES.md", "provenance/laurigates-coverage.json"]
    for entry in data["entries"]:
        if entry["status"] != "pending":
            continue
        if entry["source_path"] == "LICENSE":
            entry.update(status="merged", target_paths=notices, reason="Pinned MIT license and copyright reproduced in product notices and coverage metadata.")
        else:
            entry.update(status="excluded", target_paths=[], reason=exclusion_reason(entry["source_path"]))
    save(data)
    print("finalized rust-development audit and non-selected entries")


def write_index() -> None:
    data = load()
    counts = Counter(entry["status"] for entry in data["entries"])
    lines = [
        "# Laurigates coverage index",
        "",
        f"Snapshot `{REVISION}` of `laurigates/claude-plugins`; source plugin `1.7.0`.",
        "",
        f"Files: {len(data['entries'])}; " + ", ".join(f"`{key}` {counts[key]}" for key in sorted(counts)),
        "",
        "| Family | Owner | Supporting | Product reference |",
        "|---|---|---|---|",
    ]
    for name in FAMILY_ORDER:
        config = FAMILY_CONFIG[name]
        lines.append(f"| `{name}` | `{config['owner']}` | {', '.join(f'`{item}`' for item in config['supporting'])} | [`{Path(config['target']).name}`](../{config['target']}) |")
    lines += ["", "`mockito-http-mocking` is recorded as excluded and has no runtime route.", ""]
    INDEX.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {INDEX.relative_to(PLUGIN).as_posix()}")


def verify() -> None:
    data = load()
    assert data["schema_version"] == 1
    assert set(data["statuses"]) == STATUSES
    assert set(data["block_statuses"]) == BLOCK_STATUSES
    assert data["family_order"] == FAMILY_ORDER
    assert data["source"] == {
        "name": "laurigates/claude-plugins",
        "relative_path": "references/claude-plugins_laurigates",
        "revision": REVISION,
        "commit_date": "2026-08-23T09:39:01Z",
        "plugin_version": "1.7.0",
        "license": "MIT",
        "copyright": "Copyright (c) 2026 Lauri Gates",
    }
    assert data["source_metrics"] == {
        "selected_markdown_files": 10,
        "selected_markdown_lines": 2364,
        "selected_markdown_line_basis": "nonempty",
        "source_blocks": 130,
        "unique_source_blocks": 130,
        "source_block_aliases": 0,
    }
    entries = data["entries"]
    assert len(entries) == 83 and len({entry["source_path"] for entry in entries}) == 83
    assert Counter(entry["status"] for entry in entries) == {"adapted": 6, "merged": 5, "excluded": 72}
    assert not [entry for entry in entries if entry["status"] in {"pending", "in_progress", "duplicate"}]
    indexed = entries_by_path(data)
    actual = source_files()
    assert len(actual) == 83 and {relative(path) for path in actual} == set(indexed)
    for path in actual:
        entry = indexed[relative(path)]
        assert digest(path) == entry["source_sha256"]
        assert path.stat().st_size == entry["source_bytes"]
        assert line_count(path) == entry["source_lines"]
        assert entry["reason"]
        for target in entry["target_paths"]:
            assert (PLUGIN / target).is_file(), f"missing target: {target}"
    blocks = data["blocks"]
    assert len(blocks) == 130 and sum(len(item["occurrences"]) for item in blocks) == 130
    assert not [block for block in blocks if block["status"] == "pending"]
    for block in blocks:
        assert block["status"] in BLOCK_STATUSES - {"pending"}
        assert block["reason"] and block["evidence_ids"]
        assert set(block["evidence_ids"]) <= set(EVIDENCE)
        if "command_contract" in block:
            contract = block["command_contract"]
            assert contract["tools"] and contract["applicable_version"]
            assert contract["status"] in {"stable", "nightly", "external", "project"}
            assert contract["os_constraints"] and contract["target_constraints"] and contract["side_effects"]
            assert contract["decision"] == block["status"]
        if block["language"] == "rust":
            assert block["rust_example"] == ("fragment" if block["status"] != "rejected" else None)
    for name in FAMILY_ORDER:
        target = PLUGIN / target_for_family(name)
        assert target.is_file()
        source = family_root(name) / "SKILL.md"
        marker = f"<!-- laurigates-source-family: {name}; source={relative(source)}; sha256={digest(source)}; revision={REVISION} -->"
        assert marker in target.read_text(encoding="utf-8")
    refs = [PLUGIN / target_for_family(name) for name in FAMILY_ORDER]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in refs)
    forbidden = [
        r"cargo\s+machete\s+--fix", r"\.cargo-machete\.toml", r"test-threads\s*=\s*0",
        r"--fail-under-branches", r"touch\s+src[/\\]", r"restriction\s*=\s*['\"]deny",
    ]
    assert not any(re.search(pattern, combined, re.IGNORECASE) for pattern in forbidden)
    assert not (PLUGIN / "skills" / "mockito-http-mocking").exists()
    assert not list((PLUGIN / "skills").glob("*/references/**/mockito-http-mocking.md"))
    assert not STAGING.exists()
    assert INDEX.is_file()
    print("OK: 83 files, 6 adapted families, 10 selected Markdown files, 130/130/0 block accounting")


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init")
    init.add_argument("--force", action="store_true")
    stage = commands.add_parser("stage-family")
    stage.add_argument("family", choices=FAMILY_ORDER)
    finalize = commands.add_parser("finalize")
    finalize.add_argument("family", nargs="?", choices=FAMILY_ORDER)
    commands.add_parser("write-index")
    commands.add_parser("verify")
    args = parser.parse_args()
    if args.command == "init":
        initialize(args.force)
    elif args.command == "stage-family":
        stage_family(args.family)
    elif args.command == "finalize":
        finalize_family(args.family) if args.family else finalize_remaining()
    elif args.command == "write-index":
        write_index()
    else:
        verify()


if __name__ == "__main__":
    main()
