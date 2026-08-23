# Low-level Rust Cross protocol

<!-- low-level-source-family: rust-cross; source=skills/rust/rust-cross/SKILL.md; sha256=3834230005747c063552150d2d4c1a935a3cd0e10133fb4bc444d85fffb42f90; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-cross/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-stable`, `$rust-unsafe-ffi`.
- Retained scope: Host/target separation, target support tiers, linker and runner configuration, native libraries, containers, emulators, and deployment validation.
- Baseline correction: Installing a Rust target does not install a linker, sysroot, native libraries, emulator, or hardware. Resolve current target names and support guarantees instead of retaining a static catalog.
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

- `Full Target Triple Format` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `Tier 1 Targets (guaranteed to work)` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `Popular Tier 2 Targets` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `Bare Metal (Embedded) Targets` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `Glibc Version Targeting (cargo-zigbuild)` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `cross Docker Images` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `OpenSSL Cross-Compilation` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `Embedded Project Structure` — inspect when relevant; source `skills/rust/rust-cross/references/cross-targets.md`.
- `Add a rustup target` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.
- `Common target triples` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.
- `cross tool (Docker-based, easiest)` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.
- `cargo-zigbuild (zero-setup, uses zig cc)` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.
- `.cargo/config.toml for cross targets` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.
- `Static binaries with musl` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.
- `Embedded bare-metal (#[no_std])` — inspect when relevant; source `skills/rust/rust-cross/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 17 unique source block bodies: 10 `fragment`, 7 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustup-cross`](https://rust-lang.github.io/rustup/cross-compilation.html) — rustup cross-compilation responsibilities; `current-rustup`, reviewed 2026-08-23.
- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.
- [`cargo-build-cache`](https://doc.rust-lang.org/cargo/reference/build-cache.html) — Cargo target/build directories and artifact layout; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
