# Low-level Linux Perf protocol

<!-- low-level-source-family: linux-perf; source=skills/profilers/linux-perf/SKILL.md; sha256=37a36c26bf493d7c193df5d8f1e076013f0148ad84235daa15308f160ab5735c; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/profilers/linux-perf/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-cargo-build`.
- Retained scope: perf stat, sampling, reporting, annotation, live analysis, events, stack collection, and failure diagnosis.
- Baseline correction: Select frame-pointer, DWARF, or LBR call graphs from the binary and CPU. perf_event_paranoid is a security boundary and must never be weakened automatically.
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

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Table of Contents` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Hardware events` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Raw PMU events (Intel Skylake example)` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Software events` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Tracepoints` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Interpreting metrics` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Diagnosing bottlenecks` — inspect when relevant; source `skills/profilers/linux-perf/references/events.md`.
- `Prerequisites` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `perf stat — quick counters` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `perf record — sampling` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `perf report — interactive analysis` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `perf annotate — hot instructions` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `perf top — live profiling` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `Feed into flamegraphs` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `Common issues` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.
- `Useful events` — inspect when relevant; source `skills/profilers/linux-perf/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 11 unique source block bodies: 8 `fragment`, 3 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; `kernel-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
