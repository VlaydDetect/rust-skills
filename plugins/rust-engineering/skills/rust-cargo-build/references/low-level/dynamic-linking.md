# Low-level Dynamic Linking protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-unsafe-ffi`, `$debugging`.
- Retained scope: Shared-library identity, SONAME, RPATH/RUNPATH, loader search, plugins, interposition, visibility, and loader errors.
- Baseline correction: Loader order and path semantics are OS-specific and security-sensitive. Do not set global loader variables or assume a GNU layout for macOS or Windows.
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

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `ld.so Search Path Configuration` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `System-wide (/etc/ld.so.conf)` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Per-user (LD_LIBRARY_PATH)` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `RPATH / RUNPATH Deep Dive` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `$ORIGIN Patterns` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Modifying Existing RPATH` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `CMake RPATH Configuration` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Soname Versioning Lifecycle` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Creating a versioned library` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Upgrading (minor ABI-compatible)` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Breaking ABI (major bump)` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Version Scripts (GNU ld)` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Debugging Dynamic Linking` — inspect when relevant; source `skills/binaries/dynamic-linking/references/ld-rpath-soname.md`.
- `Creating a shared library` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `Soname versioning convention` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `RPATH vs RUNPATH` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `Library search order` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `dlopen / dlsym plugin pattern` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `LD_PRELOAD interposition` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `Symbol visibility control` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.
- `Common errors` — inspect when relevant; source `skills/binaries/dynamic-linking/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 27 unique source block bodies: 23 `fragment`, 4 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
