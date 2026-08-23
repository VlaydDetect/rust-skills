# Low-level Hardware Counters protocol> Focused decision protocol; examples are evidence, not automatic product policy.
## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-research`.
- Retained scope: PMU event selection, perf stat/record, derived metrics, raw events, source attribution, PAPI/PCM, multiplexing, and counter limitations.
- Baseline correction: Event names, availability, privilege, skid, multiplexing, and useful thresholds are CPU- and kernel-specific. Prefer ratios tied to a hypothesis, not universal threshold tables.
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

- `perf stat — basic counter collection` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.
- `Specifying PMU events with -e` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.
- `Key metrics and thresholds` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.
- `Raw PMU events (CPU-specific)` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.
- `Source-level annotation with perf record/annotate` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.
- `PAPI — Portable API for hardware counters` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.
- `Intel PCM (Performance Counter Monitor)` — inspect when relevant; source `skills/profilers/hardware-counters/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 8 unique source block bodies: 7 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; `kernel-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
