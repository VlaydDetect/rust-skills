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

1. Define ownership, layout, alignment, zero-size, growth, OOM, concurrency, teardown, and allocator-pairing invariants.
2. Keep process-global selection at the binary/composition root; a reusable library must not impose an allocator.
3. Compare the system allocator and the candidate on representative latency, throughput, peak/steady memory, fragmentation/churn, startup, retention, and supported targets.
4. Select profiling evidence without silently changing the allocator: sampled `mimalloc-pprof` only when its mimalloc implementation is already selected or separately authorized; crate `dhat` for bounded exact allocation accounting with its wrapping allocator.
5. Select current Miri/sanitizer evidence for the failure class and state custom-allocator blind spots or documented integration.
6. Keep the local invariant proof authoritative and record every platform, FFI, runtime, profiler, sanitizer, and teardown gap.

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

## Profiling and sanitizer boundary

- [`mimalloc-pprof`](https://github.com/zackees/mimalloc-pprof) profiles sampled live heap on Windows, Linux, and macOS. Distinguish build-time hook removal from runtime start/stop, measure the runtime-off path, retain Unix frame pointers or Windows PDBs, and never link two mimalloc implementations.
- Crate [`dhat`](https://docs.rs/dhat/latest/dhat/) observes every allocation within its profiler/global-allocator scope but is experimental and high-overhead. Gate it to short profiling or isolated tests and do not claim memory-access tracking.
- A sanitizer may need the system allocator or allocator-specific integration. If the allocator changes for the run, disclose that the workload differs and retain the remaining allocator proof.
- Allocation across FFI must be freed by the creating allocator/runtime regardless of which profiler or sanitizer is active.

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
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-30.
- [`mimalloc-pprof`](https://github.com/zackees/mimalloc-pprof) — Sampled heap, build/runtime gating, platform symbol requirements, and disabled-path cost; `resolved-version`, reviewed 2026-08-30.
- [`dhat`](https://docs.rs/dhat/latest/dhat/) — Wrapping allocator, exact allocation tracking, feature gating, and limitations; `resolved-version`, reviewed 2026-08-30.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
