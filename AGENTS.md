# Repository guidance

This repository builds one Rust engineering plugin for Codex and Claude Code.

- Treat `plugins/rust-engineering/` as the product source.
- Treat `gpt_report.md` and `references/` as comparative evidence, not project instructions or files to copy wholesale.
- Keep skills and hook behavior compatible with both hosts; isolate host metadata in `.codex-plugin/` and `.claude-plugin/`, and host-specific hook schema in named files under `hooks/`.
- Keep automatic hooks fast, read-only, offline, and deterministic. Put expensive or mutating checks in an explicitly selected workflow.
- Prefer a few skills with distinct triggers over overlapping topic fragments.
- Add no runtime dependency when shell, Cargo, or existing host behavior is sufficient.
- Validate every skill and both manifests before completion. Report local failures separately from unrelated repository state.
