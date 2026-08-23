# Low-level Cargo Workflows protocol

<!-- low-level-source-family: cargo-workflows; source=skills/rust/cargo-workflows/SKILL.md; sha256=a2e0d836f2f5e929cb380fd4ed7b872e657424bfbf0340f66dab96f1a66010ea; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/cargo-workflows/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-dependencies`, `$rust-verify`.
- Retained scope: Workspace, feature, build-script, lockfile, cache, CI, and Cargo tool workflows.
- Baseline correction: Resolver, build-script directive, external-tool, audit-policy, and lockfile behavior comes from the effective project and current Cargo/tool documentation; source defaults are not policy.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- workspace root and selected package.
- rust-toolchain/MSRV/Edition.
- effective Cargo configuration.
- host and target triples.
- profile, features, lockfile policy, and native inputs.

## Decision protocol

1. Resolve effective state with repository files and cargo metadata before proposing flags.
2. Separate host tools/build scripts/proc macros from target artifacts and runtime dependencies.
3. State the exact artifact or behavior being changed and derive paths from Cargo output, not folklore.
4. Change the owning manifest/config once; keep environment-only experiments local and reversible.
5. Validate the affected package/target/profile matrix and review lockfile or artifact changes separately.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Workspace Dependency Management` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Centralizing versions` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Feature Resolution (resolver = "2")` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Virtual Manifest Pattern` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Path vs Registry Dependencies` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Selective Build Commands` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Cargo.lock Management` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `CI Configuration Patterns` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `GitHub Actions matrix` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `MSRV (minimum supported Rust version)` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Published Crate Checklist` — inspect when relevant; source `skills/rust/cargo-workflows/references/workspace-patterns.md`.
- `Workspace setup` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.
- `Feature flags` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.
- `Build scripts (build.rs)` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.
- `Incremental builds and CI caching` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.
- `cargo nextest (faster test runner)` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.
- `Dependency management and auditing` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.
- `Useful cargo commands` — inspect when relevant; source `skills/rust/cargo-workflows/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 25 unique source block bodies: 20 `fragment`, 5 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-metadata`](https://doc.rust-lang.org/nightly/cargo/commands/cargo-metadata.html) — Machine-readable workspace, target directory, and resolved packages; `stable-format-v1`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.
- [`cargo-build-scripts`](https://doc.rust-lang.org/cargo/reference/build-scripts.html) — Build-script inputs, outputs, directives, and host/target behavior; `stable`, reviewed 2026-08-23.
- [`cargo-resolver`](https://doc.rust-lang.org/cargo/reference/resolver.html) — Dependency and feature resolution; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
