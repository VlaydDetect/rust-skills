# Low-level Linker Scripts protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-architecture`, `$rust-unsafe-ffi`.
- Retained scope: Memory regions, sections, VMA/LMA, startup initialization, placement, KEEP/ALIGN/PROVIDE, symbols, and map-based verification.
- Baseline correction: A linker script is target firmware policy. Verify the selected linker grammar, memory map, startup code, retained sections, alignment, stack/heap boundaries, and final map file.
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

- `Table of Contents` — inspect when relevant; source `skills/embedded/linker-scripts/references/linker-script-anatomy.md`.
- `Complete STM32 Example` — inspect when relevant; source `skills/embedded/linker-scripts/references/linker-script-anatomy.md`.
- `Location Counter Operations` — inspect when relevant; source `skills/embedded/linker-scripts/references/linker-script-anatomy.md`.
- `Output Section Attributes` — inspect when relevant; source `skills/embedded/linker-scripts/references/linker-script-anatomy.md`.
- `Built-in Functions` — inspect when relevant; source `skills/embedded/linker-scripts/references/linker-script-anatomy.md`.
- `Linker script anatomy` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.
- `VMA vs LMA` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.
- `Startup .bss / .data initialization` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.
- `Placing code in specific regions` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.
- `KEEP, ALIGN, PROVIDE` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.
- `Weak symbols` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.
- `Common linker errors` — inspect when relevant; source `skills/embedded/linker-scripts/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 14 unique source block bodies: 14 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
