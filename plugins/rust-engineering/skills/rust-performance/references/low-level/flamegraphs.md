# Low-level Flamegraphs protocol

<!-- low-level-source-family: flamegraphs; source=skills/profilers/flamegraphs/SKILL.md; sha256=8be8966fa2389ade91ff752961bd51e7b87f4250077ec06b495c79e1d5513632; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/profilers/flamegraphs/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-cargo-build`.
- Retained scope: Sampling-stack capture, folded stacks, differential views, callgrind and alternate inputs, graph interpretation, and follow-up measurement.
- Baseline correction: Box width is sample proportion, the x-axis is not time, and color is normally not semantic. Preserve raw samples and use a benchmark or counter comparison for the claimed win.
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

- `Table of Contents` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `FlameGraph scripts` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `stackcollapse scripts by profiler` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Linux perf` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Valgrind Callgrind` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `DTrace (macOS / FreeBSD / Solaris)` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Go pprof` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Java (async-profiler)` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Rust (cargo-flamegraph)` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `flamegraph.pl options` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Color palettes` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Differential flamegraphs` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Alternative flamegraph tools` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Speedscope (browser-based, interactive)` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Firefox Profiler` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `inferno (Rust implementation, fast)` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `pprof (Go, supports flamegraphs)` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Reading patterns quick reference` — inspect when relevant; source `skills/profilers/flamegraphs/references/tools.md`.
- `Install FlameGraph tools` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.
- `perf → flamegraph (most common path)` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.
- `Differential flamegraph (before/after)` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.
- `Callgrind → flamegraph` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.
- `Other profiler inputs` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.
- `Reading flamegraphs` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.
- `flamegraph.pl options` — inspect when relevant; source `skills/profilers/flamegraphs/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 19 unique source block bodies: 15 `fragment`, 4 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`cargo-flamegraph`](https://github.com/flamegraph-rs/flamegraph) — cargo-flamegraph backends and command surface; `resolved-version`, reviewed 2026-08-23.
- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; `kernel-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
