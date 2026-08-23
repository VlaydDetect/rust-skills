# Low-level Abi And Calling Conventions protocol

<!-- low-level-source-family: abi-and-calling-conventions; source=skills/computer-architecture/abi-and-calling-conventions/SKILL.md; sha256=934013a0dfdf4f03ff599492633b8cee9a1ab45a0f107e10d0201a59fa216212; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/computer-architecture/abi-and-calling-conventions/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-unsafe-ffi`.
- Supporting profiles: `$rust-cargo-build`, `$rust-unsafe`.
- Retained scope: System V, AAPCS, RISC-V, stack frames, registers, variadics, unwind, and compiler-output verification.
- Baseline correction: Calling conventions are target ABI contracts, not architecture-only folklore. Confirm target triple, data layout, symbol ABI, variadic rules, unwind, and foreign compiler settings.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- target ABI and object format.
- type layout and calling convention.
- ownership/allocator pairing.
- pointer validity and lifetimes.
- panic/unwind, callbacks and thread rules.

## Decision protocol

1. Write the foreign contract independently of Rust syntax and identify each allocation and destruction owner.
2. Represent ABI-safe values and opaque handles; validate all lengths, alignments, encodings and nullability.
3. Keep raw declarations separate from the safe wrapper and expose unsafe obligations only where callers can satisfy them.
4. Contain panics/unwind and translate errors without borrowing temporary foreign storage.
5. Verify symbols/layout with the actual target toolchain and at least one real foreign consumer.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `System V AMD64 (Linux/macOS)` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.
- `ARM AAPCS (AArch32/AArch64)` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.
- `RISC-V psABI (RV64)` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.
- `Stack frame layout (conceptual)` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.
- `Variadic functions` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.
- `Verify in compiler output` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.
- `Agent usage` — inspect when relevant; source `skills/computer-architecture/abi-and-calling-conventions/SKILL.md`.

## Failure modes and guardrails

- repr(C) does not prove semantic compatibility.
- A non-null pointer may still be invalid, unaligned, stale or aliased.
- Foreign allocators and callbacks carry independent lifecycle/thread contracts.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 4 unique source block bodies: 4 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-codegen`](https://doc.rust-lang.org/rustc/codegen-options/index.html) — rustc code-generation options; `toolchain-specific`, reviewed 2026-08-23.
- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
