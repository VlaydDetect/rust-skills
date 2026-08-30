# Rust Performance Field Guide

This guide is the detailed policy for `rust-performance`. It consolidates the benchmark, profiling, optimization, and regression contracts used by the dual-host plugin.

## Core Model

- Performance work is a controlled experiment: correctness contract, representative workload, comparable baseline, profile, one hypothesis, one change, and repeated comparison.
- Criterion is the default for maintained Rust microbenchmarks, baseline comparisons, and optimization claims. Divan is a smaller alternative for quick local exploration, not a substitute when the decision needs Criterion baselines, statistical interpretation, or its profiler hooks.
- A profiler locates resource use; it does not establish a speedup. Confirm changes with the same benchmark, profile, features, target, workload, hardware class, and environment controls.
- End-to-end workloads own service latency, I/O, queueing, contention, startup, and tail behavior that a microbenchmark cannot represent.
- Cargo profiles, codegen flags, allocators, instrumentation, and sanitizers can change the workload. Record them as experimental inputs rather than silently treating them as neutral.

## Decision Table

| Situation | Prefer | Required boundary |
|---|---|---|
| Maintained microbenchmark or regression evidence | Criterion | Preserve inputs, baseline policy, environment, and distributions |
| Small exploratory benchmark | Divan | Do not promote its result to a regression claim without an explicit comparison policy |
| Unknown CPU or latency hotspot | Sampling profiler | Use readable release-like symbols, then create a focused benchmark |
| Allocation or retained-memory question | Allocation profiler | Distinguish sampled live heap from exact per-allocation observation |
| Cache or branch hypothesis | Hardware counters | Resolve events for the actual CPU and OS; reject universal thresholds |
| Timeline, locks, frames, threads, or GPU | Tracy | Keep instrumentation conditional and account for protocol/network effects |
| Unsafe or FFI optimization | Safe baseline plus sanitizer/FFI evidence | A measured win never replaces the soundness proof |

## Benchmark Contract

Every committed benchmark records:

- the metric and correctness oracle;
- representative inputs, input sizes, cold or warm state, and throughput unit;
- toolchain, benchmark framework and resolved version, Cargo profile, target, features, relevant flags, and allocator;
- machine or runner class, OS, power/thermal/load controls, and runtime configuration;
- baseline name and retention policy when comparisons are used;
- repeated results with magnitude and variance, plus contexts that were not measured.

Criterion benchmarks should use `black_box` where compiler elision is possible, `BenchmarkGroup` and `BenchmarkId` for input matrices, `Throughput` when work units are meaningful, and `iter_batched` or `iter_batched_ref` when mutable setup must stay outside the timed section. Use the production-compatible executor for async code and prefer a synchronous benchmark when executor overhead is not the subject.

Run `cargo test --benches` as a cheap harness smoke check. Do not compare baselines produced with different profiles, flags, features, allocators, hardware classes, or workload conditions.

## Profiling Contract

Use the canonical [low-level Rust profiling protocol](./low-level/rust-profiling.md) for the `profiling` Cargo profile and the Unix/Windows tool matrix. Specialized references add one narrow interpretation:

- [flamegraphs](./low-level/flamegraphs.md) for sampled-stack meaning and cross-platform backends;
- [Linux perf](./low-level/linux-perf.md) and [hardware counters](./low-level/hardware-counters.md) for CPU-specific events;
- [VTune, AMD uProf, and Windows Performance Toolkit](./low-level/intel-vtune-amd-uprof.md) for Windows hardware and OS-level analysis;
- [sanitizers](../../rust-unsafe/references/low-level/sanitizers.md) for unsafe, FFI, C/C++, and allocator boundaries.

## Optimization Rules

- Profile before proposing a data structure, cache, pool, allocator, parallel runtime, SIMD path, unsafe block, LTO setting, or layout change.
- Change one variable at a time and keep behavior, errors, ordering, floating-point policy, cancellation, and resource limits explicit.
- Reject a noise-level result and any win whose complexity, memory, build-time, startup, or portability cost exceeds the product value.
- Do not infer performance from iterator versus loop syntax, fewer source lines, fewer `clone` calls, or a generic crate benchmark.
- Add a regression guard only when the workload and runner are stable enough for the chosen threshold policy.

## Required Evidence

- Baseline command and environment record.
- Raw benchmark, profile, counter, or trace artifacts with the tool version and scope.
- A hotspot or resource hypothesis tied to the measurement.
- Before/after distributions using the same experimental contract.
- Functional verification, new costs, residual risk, and unmeasured targets.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. External tools must already be present at a verified version or require explicit authorization; absence is `SKIP`, not permission to install or weaken host policy.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. Validate it with `cargo test --manifest-path skills/rust-performance/examples/golden/Cargo.toml`; external profiler and platform evidence remains separate.

## Design Protocol Map

- [Measurement and optimization decision model](./performance-overview.md)
- [Criterion and Divan implementation guide](./performance-optimization-guide.md)
- [Specialized performance protocol](./performance.md)

## Shared Constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Resolve framework and tool versions from the current project or installed executable; do not pin an evergreen example.
- Do not infer a dependency, runtime, framework, hardware topology, allocator, or supported target.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
