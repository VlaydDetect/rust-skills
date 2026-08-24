#!/usr/bin/env python3
"""Install Rust Engineering through host-native plugin marketplaces."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

CONFIG_URL = "https://raw.githubusercontent.com/VlaydDetect/rust-skills/v1.0.1-rc/installers/config.json"


def load_config() -> dict:
    local = Path(__file__).with_name("config.json")
    if local.is_file():
        data = json.loads(local.read_text(encoding="utf-8"))
    else:
        with urllib.request.urlopen(CONFIG_URL, timeout=15) as response:
            data = json.load(response)
    required = {"marketplace", "plugin", "repository", "ref", "targets", "scopes"}
    scalars = ("marketplace", "plugin", "repository", "ref")
    arrays = ("targets", "scopes")
    safe_name = re.compile(r"^[a-z0-9-]+$")
    if (
        not isinstance(data, dict)
        or set(data) != required
        or not all(isinstance(data[key], str) and data[key] for key in scalars)
        or not all(
            isinstance(data[key], list)
            and data[key]
            and all(isinstance(item, str) and item for item in data[key])
            and len(data[key]) == len(set(data[key]))
            for key in arrays
        )
        or not safe_name.fullmatch(data["marketplace"])
        or not safe_name.fullmatch(data["plugin"])
        or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", data["repository"])
        or not re.fullmatch(r"v[0-9A-Za-z][0-9A-Za-z._-]*", data["ref"])
        or any(not safe_name.fullmatch(item) for key in arrays for item in data[key])
    ):
        raise RuntimeError("invalid installer config")
    return data


try:
    CONFIG = load_config()
except (OSError, ValueError, RuntimeError) as error:
    raise SystemExit(f"ERROR: cannot load installer config: {error}") from error
MARKETPLACE = CONFIG["marketplace"]
PLUGIN = CONFIG["plugin"]
REPOSITORY = CONFIG["repository"]
REF = CONFIG["ref"]
TARGETS = tuple(CONFIG["targets"])
SCOPES = tuple(CONFIG["scopes"])


def command_text(command: list[str]) -> str:
    return " ".join(command)


def planned_lines(target: str, scope: str) -> list[str]:
    selected = TARGETS if target == "all" else (target,)
    lines = [
        f"Rust Engineering {REF.removeprefix('v')}",
        f"Marketplace: {REPOSITORY}@{REF}",
    ]
    if "codex-cli" in selected:
        lines += [
            f"Codex add: codex plugin marketplace add {REPOSITORY} --ref {REF}",
            f"Codex refresh: codex plugin marketplace upgrade {MARKETPLACE}",
            f"Codex install: codex plugin add {PLUGIN}@{MARKETPLACE}",
        ]
    if "claude-code" in selected:
        lines += [
            f"Claude add: claude plugin marketplace add {REPOSITORY}@{REF} --scope {scope}",
            f"Claude refresh: claude plugin marketplace update {MARKETPLACE}",
            f"Claude install: claude plugin install {PLUGIN}@{MARKETPLACE} --scope {scope}",
            f"Claude update: claude plugin update {PLUGIN}@{MARKETPLACE} --scope {scope}",
        ]
    if "chatgpt-desktop" in selected:
        lines.append(
            "ChatGPT Desktop: open the plugin directory, select rust-engineering from rust-skills, "
            "confirm installation, then start a new task."
        )
    if "claude-desktop" in selected:
        lines.append(
            "Claude Desktop: in a local session open /plugin, add "
            f"{REPOSITORY}@{REF}, install {PLUGIN}@{MARKETPLACE}, then run /reload-plugins or restart."
        )
    return lines


def run_json(command: list[str]) -> object:
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode:
        raise RuntimeError(f"command failed: {command_text(command)}\n{completed.stderr.strip()}")
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"invalid JSON from: {command_text(command)}") from error


def run(command: list[str]) -> None:
    completed = subprocess.run(command, check=False)
    if completed.returncode:
        raise RuntimeError(f"command failed ({completed.returncode}): {command_text(command)}")


def records(value: object):
    if isinstance(value, dict):
        yield value
        for item in value.values():
            yield from records(item)
    elif isinstance(value, list):
        for item in value:
            yield from records(item)


def marketplace_record(data: object) -> dict | None:
    return next((item for item in records(data) if item.get("name") == MARKETPLACE), None)


def plugin_installed(data: object) -> bool:
    return any(
        item.get("name") == PLUGIN
        and item.get("marketplaceName") == MARKETPLACE
        and item.get("installed", True)
        for item in records(data)
    )


def assert_expected_source(record: dict) -> None:
    normalized = json.dumps(record, ensure_ascii=False).casefold().replace("\\", "/")
    if REPOSITORY.casefold() not in normalized:
        raise RuntimeError(f"marketplace name collision: {MARKETPLACE} uses another source")


def install_codex() -> None:
    executable = shutil.which("codex")
    if not executable:
        raise RuntimeError("Codex CLI not found; install it separately or use the Desktop instructions")
    existing = marketplace_record(run_json([executable, "plugin", "marketplace", "list", "--json"]))
    if existing:
        assert_expected_source(existing)
        run([executable, "plugin", "marketplace", "upgrade", MARKETPLACE])
    else:
        run([executable, "plugin", "marketplace", "add", REPOSITORY, "--ref", REF])
    if not plugin_installed(run_json([executable, "plugin", "list", "--json"])):
        run([executable, "plugin", "add", f"{PLUGIN}@{MARKETPLACE}"])


def install_claude(scope: str) -> None:
    executable = shutil.which("claude")
    if not executable:
        raise RuntimeError("Claude Code CLI not found; install it separately or use the Desktop instructions")
    existing = marketplace_record(run_json([executable, "plugin", "marketplace", "list", "--json"]))
    if existing:
        assert_expected_source(existing)
        run([executable, "plugin", "marketplace", "update", MARKETPLACE])
    else:
        run([executable, "plugin", "marketplace", "add", f"{REPOSITORY}@{REF}", "--scope", scope])
    installed = plugin_installed(run_json([executable, "plugin", "list", "--json"]))
    verb = "update" if installed else "install"
    run([executable, "plugin", verb, f"{PLUGIN}@{MARKETPLACE}", "--scope", scope])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=(*TARGETS, "all"), default="all")
    parser.add_argument("--scope", choices=SCOPES, default="user")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true", help="skip the single confirmation prompt")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print("\n".join(planned_lines(args.target, args.scope)))
    if args.dry_run:
        return 0
    selected = TARGETS if args.target == "all" else (args.target,)
    cli_targets = [item for item in selected if item in {"codex-cli", "claude-code"}]
    if cli_targets and not args.yes:
        if input("Run the host-native installation commands? [y/N] ").strip().casefold() not in {"y", "yes"}:
            print("Cancelled; no changes made.")
            return 0
    failures = []
    for target in cli_targets:
        try:
            install_codex() if target == "codex-cli" else install_claude(args.scope)
        except RuntimeError as error:
            if args.target != "all":
                print(f"ERROR: {error}", file=sys.stderr)
                return 2
            failures.append(str(error))
    for failure in failures:
        print(f"SKIP: {failure}", file=sys.stderr)
    return 0 if len(failures) < len(cli_targets) or not cli_targets else 2


if __name__ == "__main__":
    raise SystemExit(main())
