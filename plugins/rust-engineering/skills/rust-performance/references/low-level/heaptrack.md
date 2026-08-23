# Low-level Heaptrack protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-cargo-build`.
- Retained scope: Allocation capture, symbol quality, retained versus peak memory, call-stack attribution, filtering, run comparison, and Rust allocator visibility.
- Baseline correction: Verify that the selected allocator and workload are observable by the tool. Tool output paths and GUI availability are environment-specific.
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

- `heaptrack_print Complete Options` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Output Sections Explained` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Hotspot Output Format` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Flamegraph from heaptrack` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Common Allocation Hotspot Patterns` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Pattern: Excessive small allocations` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Pattern: Container growth` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Pattern: Leaked connection/handle` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Pattern: Temporary string allocations` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Comparing Allocators` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `heaptrack GUI (heaptrack_gui)` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Masif vs heaptrack Quick Command Comparison` — inspect when relevant; source `skills/profilers/heaptrack/references/heaptrack-analysis.md`.
- `Installation` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `Basic usage` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `Build for better profiling` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `Interpreting heaptrack_print output` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `Filtering and analysis options` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `Comparing two runs` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `heaptrack vs Valgrind massif` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.
- `Integration with Rust` — inspect when relevant; source `skills/profilers/heaptrack/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 19 unique source block bodies: 18 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-profiles`](https://doc.rust-lang.org/cargo/reference/profiles.html) — Cargo profile keys and inheritance; `stable`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
