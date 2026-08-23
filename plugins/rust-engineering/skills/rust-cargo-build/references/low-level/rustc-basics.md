# Low-level Rustc Basics protocol

<!-- low-level-source-family: rustc-basics; source=skills/rust/rustc-basics/SKILL.md; sha256=72a63229d5542756ab05a77d3bbccf8a71688076d3a9f459a62db79d960c63d5; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rustc-basics/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-performance`, `$rust-research`.
- Retained scope: Cargo profiles, rustflags precedence, target inspection, MIR/LLVM/assembly evidence, monomorphization, size, and diagnostic triage.
- Baseline correction: Do not apply target-cpu=native, target features, LTO, panic, stripping, UPX, or direct rustc invocations universally. Preserve Cargo context and verify the deployment target.
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

- `RUSTFLAGS Complete Reference` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Codegen flags (-C)` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Emit flags (--emit)` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Cargo Profile Options (Complete)` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Profile Inheritance` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Per-Package Profile Overrides` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Common Configurations` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Maximum performance` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Minimum binary size` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Fast CI builds` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Linker Configuration` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `x86-64 Microarchitecture Levels` — inspect when relevant; source `skills/rust/rustc-basics/references/rustflags-profiles.md`.
- `Choose a build mode` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `Cargo.toml profile configuration` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `RUSTFLAGS` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `Inspect assembly output` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `Understand monomorphization` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `Binary size reduction` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `Common error triage` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.
- `Useful rustc flags` — inspect when relevant; source `skills/rust/rustc-basics/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 19 unique source block bodies: 16 `fragment`, 3 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.
- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.
- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-build-cache`](https://doc.rust-lang.org/cargo/reference/build-cache.html) — Cargo target/build directories and artifact layout; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
