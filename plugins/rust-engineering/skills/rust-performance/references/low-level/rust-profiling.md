# Low-level Rust Profiling protocol

<!-- low-level-source-family: rust-profiling; source=skills/rust/rust-profiling/SKILL.md; sha256=d53aa44b454b7ca29d895283ac4efe27b1bfa6cb0901d0b5fb4143cf7c082ba2; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-profiling/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-cargo-build`.
- Retained scope: Representative workload profiling, symbols, perf/flamegraphs, allocation analysis, Criterion, binary size, and monomorphization evidence.
- Baseline correction: Do not install tools, change host security, assume artifact paths, or pin arbitrary dependency versions. A flamegraph selects a hypothesis; a comparable benchmark establishes improvement.
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

- `cargo-flamegraph Setup` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Linux Prerequisites` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `macOS Prerequisites` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Installation` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Usage Patterns` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Reading Flamegraphs` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Criterion Reference` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Benchmark Structure` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Statistical Configuration` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Custom Measurement (wall vs CPU time)` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Comparing Results` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Criterion with Async (Tokio)` — inspect when relevant; source `skills/rust/rust-profiling/references/cargo-flamegraph-setup.md`.
- `Build for profiling` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.
- `Flamegraphs with cargo-flamegraph` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.
- `Binary size analysis with cargo-bloat` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.
- `Monomorphization bloat with cargo-llvm-lines` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.
- `Criterion microbenchmarks` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.
- `perf with Rust (Linux)` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.
- `heaptrack / DHAT for allocations` — inspect when relevant; source `skills/rust/rust-profiling/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 25 unique source block bodies: 19 `fragment`, 6 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`perf-record`](https://man7.org/linux/man-pages/man1/perf-record.1.html) — perf record events and call-graph modes; `installed-perf-specific`, reviewed 2026-08-23.
- [`perf-security`](https://docs.kernel.org/admin-guide/perf-security.html) — perf privilege and data-exposure boundary; `kernel-specific`, reviewed 2026-08-23.
- [`cargo-flamegraph`](https://github.com/flamegraph-rs/flamegraph) — cargo-flamegraph backends and command surface; `resolved-version`, reviewed 2026-08-23.
- [`criterion`](https://bheisler.github.io/criterion.rs/book/) — Criterion benchmark methodology and APIs; `resolved-version`, reviewed 2026-08-23.
- [`cargo-bloat`](https://github.com/RazrFalcon/cargo-bloat) — cargo-bloat formats and attribution limits; `resolved-version`, reviewed 2026-08-23.
- [`cargo-llvm-lines`](https://github.com/dtolnay/cargo-llvm-lines) — Unoptimized LLVM IR line-count semantics; `resolved-version`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
