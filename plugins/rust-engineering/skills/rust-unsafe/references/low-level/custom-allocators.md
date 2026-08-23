# Low-level Custom Allocators protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-unsafe`.
- Supporting profiles: `$rust-performance`, `$rust-architecture`.
- Retained scope: Pool, arena, global and system allocators, ownership, alignment, fragmentation, concurrency, teardown, and benchmarking.
- Baseline correction: Do not adopt an allocator from generic benchmark claims. Prove layout and deallocation invariants, workload fit, OOM behavior, observability, and platform support.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- unsafe operation and safe caller contract.
- target and toolchain.
- executed input/schedule.
- FFI/native coverage.
- remaining manual invariants.

## Decision protocol

1. Write provenance, alignment, initialization, validity, aliasing, lifetime, layout, thread, panic and drop obligations.
2. Select Miri for supported MIR execution or a documented rustc sanitizer for a supported target and failure class.
3. Use the repository-pinned nightly when present; otherwise report the required evidence as unavailable instead of installing.
4. Minimize the reproducer and interpret the first causally relevant diagnostic.
5. Record what the run did not cover and keep the local safety proof authoritative.

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Allocator taxonomy` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `Simple pool allocator in C` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `Arena allocator` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `jemalloc tuning` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `mimalloc` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `tcmalloc thread-caching` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `Rust GlobalAlloc` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `Fragmentation metrics` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.
- `Benchmarking` — inspect when relevant; source `skills/allocators/custom-allocators/SKILL.md`.

## Failure modes and guardrails

- Miri explores concrete executions, not all inputs or schedules.
- Sanitizer support is mode- and target-specific and normally nightly.
- C/C++ UBSan recipes are not a Rust sanitizer mode.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 11 unique source block bodies: 11 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
