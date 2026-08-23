# Low-level Cpu Cache Opt protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$rust-architecture`, `$rust-research`.
- Retained scope: Counter-led cache diagnosis, data layout, traversal, false sharing, prefetch, blocking, and cache-aware algorithm choices.
- Baseline correction: AoS/SoA, padding, prefetch, and blocking are workload- and hardware-dependent. Preserve semantics and compare representative measurements.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- metric and correctness contract.
- representative workload and data.
- target/profile/features/toolchain.
- hardware, kernel and load controls.
- baseline distribution and retained raw evidence.

## Decision protocol

1. Classify CPU, allocation, I/O, contention, binary-size, or build-time cost before choosing a tool.
2. Capture a comparable baseline and preserve raw samples, counters, reports, or build timings.
3. Use one profiler or counter set to locate a bottleneck; treat attribution as a hypothesis with tool limitations.
4. Change one variable and rerun the same workload and correctness checks.
5. Reject noise-level wins and report unmeasured targets, cold/warm state, tail behavior, and new complexity.

## Decision map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `perf stat Cache Events` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `Generic (portable across CPUs)` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `x86 Intel PMU Events` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `False Sharing Detection` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `ARM Cache Events` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `Interpreting Cache Rates` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `valgrind cachegrind` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `Struct Layout Analysis` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `Cache-Friendly Allocation Patterns` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `Hardware Prefetcher Behavior` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/references/cache-counters.md`.
- `Measure cache performance` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.
- `Cache line basics` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.
- `AoS vs SoA data layout` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.
- `Common cache-unfriendly patterns` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.
- `False sharing` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.
- `Prefetching` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.
- `Cache-friendly algorithm design` — inspect when relevant; source `skills/low-level-programming/cpu-cache-opt/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 17 unique source block bodies: 17 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
