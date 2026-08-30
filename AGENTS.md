# Repository guidance

This repository ships one Rust Engineering product for Codex/ChatGPT Desktop and Claude Code/Desktop.

## Product boundary

- Treat `plugins/rust-engineering/` as the plugin source and the 55 skill directories as a public inventory.
- Keep skill instructions, references, examples, checks, and shared scripts host-neutral.
- Keep attribution only in the final `README.md` section named `Источники` and in `plugins/rust-engineering/THIRD_PARTY_NOTICES.md`.
- Do not add runtime dependencies when shell, Cargo, Python/Node standard libraries, or existing host behavior is sufficient.

## Dual-host model

- `plugins/rust-engineering/.codex-plugin/plugin.json` owns Codex metadata; `plugins/rust-engineering/.claude-plugin/plugin.json` owns Claude metadata.
- Host-specific SessionStart schemas live in `hooks/hooks.json` and `hooks/claude.json`. Shared behavior lives in `scripts/session-context.sh` and `scripts/session-context.ps1`.
- `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json` are thin native catalogs for the same `rust-engineering` plugin. Do not duplicate product content in them.
- Keep name, description, repository, version, marketplace identity, and installer config synchronized.

## Skill and reference structure

- Every skill has one `SKILL.md`, `agents/openai.yaml`, and at least one Markdown entrypoint directly under `references/`.
- A reference may be `references/<file>.md` or `references/<theme>/<file>.md`. Deeper nesting is forbidden.
- Shared thematic directory names are `low-level` and `cargo-tooling`. Structured skills may additionally use:
  - `rust-coding-rules`: `rules`, `categories`, `guidelines`;
  - `rust-design-protocol`: `analysis`, `cognition`, `negotiation`, `routing`, `examples`;
  - `rust-research`: `lenses`, `commands`, `dossiers`, `news`;
  - `rust-unsafe` and `rust-unsafe-ffi`: `rules`, `checklists`, `workflows`, `examples`;
  - `rust-navigation`: `modes`;
  - `rust-architecture`: `domains`.
- Use product/topic names for files and headings. When flattening creates a collision, add the shortest meaningful topic prefix.
- Update every local Markdown link when moving a reference. Merge only exact duplicates or source-specific index material into an existing product entrypoint.

## Routing and mutation

- Mutating Rust work enters `rust-workflow`. It builds a `ProfileStack` from the current change with one owner per decision unit, construct-bound coding profiles, and trigger-bound helpers.
- The `3/6/10` owner, coding, and helper limits are circuit breakers; exceeding one requires a phase split and fresh routing.
- `rust-coding-rules` is a post-routing overlay of at most nine relevant rules per active decision unit, not a profile role.
- The main agent is the only writer. Shared agents remain bounded and read-only.
- `rust-verify` closes the evidence loop; `rust-review` is optional unless requested or proportionate to risk.
- Prefer a few distinct routing owners over overlapping topic fragments.

## Hooks and setup

- Automatic SessionStart hooks must be fast, offline, deterministic, and read-only.
- A non-Rust directory is silent. Rust without Cargo receives one opt-in setup offer. Cargo projects receive local context plus one opt-in project setup offer.
- Nix/NixOS detection produces a separate offer routed through `nix-dev-env` or `nixos`.
- Before explicit user approval, never install tools, invoke package managers or generators, create project files, build Nix outputs, change lockfiles, format code, or run test suites.
- After approval, propose tools only from project evidence; do not blanket-install optional Cargo utilities.

## Release invariants

- The release gate requires exactly 55 valid skills, 265 rule IDs/aliases with all category indexes, 47 unsafe/FFI rules, 341 schema-9 eval scenarios, and four read-only agent contracts.
- `scripts/` contains only `validate.py` and the two SessionStart scripts. External corpora and provenance ledgers are not build or validation inputs.
- Version-bearing manifests, root `package.json`, `installers/config.json`, marketplaces, and installer plans must agree on `1.0.2-rc` / `v1.0.2-rc`.
- Python and Node installers stay dependency-free, print the same dry-run plan, use host-native CLI commands, reject marketplace source collisions, and never edit Desktop configuration or caches.
- Validate with `uv run --no-project plugins/rust-engineering/scripts/validate.py --examples`, both host/plugin validators when available, and `git diff --check`.
- Report a missing local CLI or cache separately from product regressions. Do not create or push a release tag without explicit release authorization.
- Preserve unrelated user files, including untracked `TODO.md` and `graphify-out/`.
