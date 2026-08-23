# Low-level Binary Hardening protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-cargo-build`.
- Supporting profiles: `$rust-architecture`, `$rust-unsafe-ffi`.
- Retained scope: Hardening-property inspection, compiler/linker mitigation families, control-flow integrity, platform mechanisms, and residual attack surface.
- Baseline correction: Hardening flags depend on object format, linker, target, runtime, deployment, and threat model. Verify the final artifact; never copy C flags into rustflags without rustc/linker evidence.
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

- `Complete Hardened Build Commands` — inspect when relevant; source `skills/runtimes/binary-hardening/references/hardening-flags.md`.
- `GCC (Linux)` — inspect when relevant; source `skills/runtimes/binary-hardening/references/hardening-flags.md`.
- `Clang (Linux)` — inspect when relevant; source `skills/runtimes/binary-hardening/references/hardening-flags.md`.
- `Shared Libraries` — inspect when relevant; source `skills/runtimes/binary-hardening/references/hardening-flags.md`.
- `Flag Reference Table` — inspect when relevant; source `skills/runtimes/binary-hardening/references/hardening-flags.md`.
- `Distribution Defaults` — inspect when relevant; source `skills/runtimes/binary-hardening/references/hardening-flags.md`.
- `Analyze existing binary with checksec` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `Hardening compiler and linker flags` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `Control Flow Integrity (CFI)` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `Stack canaries in depth` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `FORTIFY_SOURCE` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `seccomp-bpf syscall filtering` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `Intel CET (Shadow Stack + IBT)` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `ARM BTI and PAC (AArch64)` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `ARM Memory Tagging (MTE)` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.
- `glibc shadow stack (2.39+)` — inspect when relevant; source `skills/runtimes/binary-hardening/SKILL.md`.

## Failure modes and guardrails

- Static target, linker, runner, and artifact-path catalogs drift.
- RUSTFLAGS can affect host invocations unless an explicit --target separates them.
- A faster link or smaller binary is not automatically a valid deployment artifact.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 16 unique source block bodies: 15 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`cargo-config`](https://doc.rust-lang.org/cargo/reference/config.html) — Cargo configuration hierarchy, target linker/runner, wrappers, and rustflags; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
