# Low-level Linkers Lto protocol

<!-- low-level-source-family: linkers-lto; source=skills/binaries/linkers-lto/SKILL.md; sha256=4b9cc771b17333d51fd5e2a67f68eab502b7631a00eca13e0980766030850651; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/binaries/linkers-lto/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-performance`, `$rust-unsafe-ffi`.
- Retained scope: Linker selection, argument ordering, LTO modes, dead-code elimination, visibility, map files, and link-failure diagnosis.
- Baseline correction: Compiler driver, linker flavor, arguments, target ABI, native libraries, and current platform defaults must be observed. Change one measured variable and preserve symbol/debug requirements.
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

- `Table of Contents` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Linker selection` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `GNU ld / gold flags` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Basics` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Symbol control` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Dead-code removal` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Hardening` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Diagnostics` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Group / circular deps` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `lld flags` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `GCC LTO flags` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Clang LTO flags` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Full LTO` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `ThinLTO (preferred for large projects)` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `LTO in CMake` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `MSVC LTCG` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Linker scripts basics` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Common linker errors` — inspect when relevant; source `skills/binaries/linkers-lto/references/flags.md`.
- `Linker selection` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `Essential linker flags` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `Link order matters (GNU ld)` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `LTO with GCC` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `LTO with Clang / lld` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `Dead-code stripping` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `Symbol visibility` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `Common linker errors` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.
- `Linker map file` — inspect when relevant; source `skills/binaries/linkers-lto/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 23 unique source block bodies: 23 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
