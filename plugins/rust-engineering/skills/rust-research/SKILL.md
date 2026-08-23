---
name: rust-research
description: Research current Rust, Cargo, Clippy, standard-library, crate, dependency, documentation, and news facts with dated evidence. Use for version-sensitive questions or exact dependency dossiers; do not use for ordinary local coding facts already fixed by the repository.
---

# Rust Research

Own fresh external facts and exact Cargo package identity. Apply this skill directly for read-only research or load it as a supporting profile when implementation depends on current upstream evidence.

## Modes

- `rust`: releases, Edition, Cargo, Clippy, standard library, stabilization, and MSRV.
- `crate`: exact package identity, resolved features/targets, documentation, maintenance, and project-local dossiers.
- `news`: explicit day, week, or month Rust ecosystem reports.

## Workflow

1. Read the repository's toolchain, MSRV, edition, lockfile, manifests, CI, and local sources before browsing.
2. Select one mode and its authoritative source hierarchy.
3. Record exact subject version/package ID, canonical source, retrieval date, confidence, and gaps.
4. Distinguish fixed project state from current upstream state and discovery signals.
5. Retry one alternative authoritative source on failure, then report the gap instead of guessing.
6. Return a bounded evidence record; hand adoption, implementation, or documentation edits to their owning profiles.

## Mutation Boundary

Ordinary research is read-only. `crate sync` may create or refresh one project-local dossier only when explicitly requested. Exporting or removing a Codex/Claude wrapper writes outside the project and requires approval after validating the exact target. Never update a lockfile, install a tool, edit `.gitignore`, or fetch dependencies implicitly.

## Decision Rules

- The target project's contract outranks current stable Rust.
- Cargo package IDs and source IDs are opaque; use `cargo metadata --format-version 1 --locked --offline` rather than manifest grep.
- Match crate documentation to the resolved version and features.
- Official Rust sources support toolchain facts; community sites are discovery aids.
- Reddit is a low-trust signal and cannot establish technical, release, security, or governance facts.
- Do not persist a generic news/docs cache or trigger research for every crate name.

## Detailed References

- Read [Current Rust baseline](references/current-baseline.md) for the dated product snapshot and precedence rules.
- Read the adapted [Rust and crate research protocol](references/actionbook/rust-learner/overview.md) for release, std, Clippy, and crate modes.
- Read [Dynamic crate dossier protocol](references/actionbook/core-dynamic-skills/overview.md) only for inspect/sync/export/remove operations.
- Read [Rust news protocol](references/actionbook/rust-daily/overview.md) only for explicit news requests.
- Use the source-derived [research-agent lenses](references/actionbook-agents.md) when delegating one bounded read-only question.
- Use [Actionbook command adapters](references/actionbook-commands.md) to translate legacy slash-command intent into host-neutral modes.
- Read the retained [source docs-cache specification](references/actionbook/docs-cache-source-spec.md) only when designing dossier provenance or invalidation; its global cache paths, TTLs, and commands are not product behavior.

## Hand-offs

- `rust-crate-discovery` owns build-versus-buy and candidate selection.
- `rust-dependencies` owns adopted dependency changes and governance.
- `rust-documentation` owns edits to project docs.
- `rust-design-protocol` owns comparisons and cross-layer decisions.
- `rust-workflow` remains the sole writer for repository implementation.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
