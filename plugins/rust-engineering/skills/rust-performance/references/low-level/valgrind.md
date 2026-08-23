# Low-level Valgrind protocol

<!-- low-level-source-family: valgrind; source=skills/profilers/valgrind/SKILL.md; sha256=9da280ba707bc94e6b7239bcd5ad0ce0cdf0a39415a257cdbdd2ed335e62ccf6; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/profilers/valgrind/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-performance`.
- Supporting profiles: `$debugging`, `$rust-unsafe`.
- Retained scope: Memcheck, leak categories, suppressions, Cachegrind, Callgrind, Massif, overhead, and native-code coverage.
- Baseline correction: Valgrind support and semantics are target-specific and do not replace Miri or Rust sanitizers. Validate allocator, JIT, FFI, and optimized-code visibility.
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

- `Comparison` — inspect when relevant; source `skills/profilers/valgrind/references/valgrind-vs-asan.md`.
- `When to use which` — inspect when relevant; source `skills/profilers/valgrind/references/valgrind-vs-asan.md`.
- `Both together` — inspect when relevant; source `skills/profilers/valgrind/references/valgrind-vs-asan.md`.
- `Combining sanitizers for maximum coverage` — inspect when relevant; source `skills/profilers/valgrind/references/valgrind-vs-asan.md`.
- `Memcheck — memory error detection` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Understanding Memcheck output` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Leak kinds` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Suppressions` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Cachegrind — cache simulation` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Callgrind — call graph profiling` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Massif — heap profiling` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.
- `Performance considerations` — inspect when relevant; source `skills/profilers/valgrind/SKILL.md`.

## Failure modes and guardrails

- Flamegraph width is sample proportion, not an optimization measurement.
- Hardware events and thresholds are CPU/kernel-specific.
- Compile-time, binary-size and runtime improvements can trade against one another.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 7 unique source block bodies: 6 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.
- [`rust-sanitizers`](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — Supported rustc sanitizer modes and target matrix; `nightly-target-specific`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
