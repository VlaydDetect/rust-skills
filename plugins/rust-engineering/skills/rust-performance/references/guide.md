# Rust Performance Field Guide

This guide is the detailed policy for `rust-performance`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Performance work is an experiment: controlled baseline, profile, hypothesis, change, comparison, and decision.
- Criterion or Divan can estimate distributions and noise for microbenchmarks, while end-to-end harnesses cover realistic integration costs.
- Profilers reveal where resources are spent; allocation counters, flame graphs, sampling, tracing, and compiler timing answer different questions.
- Data layout, access locality, allocation, copies, branch behavior, hashing, dispatch, and synchronization are common runtime levers.
- Cargo profiles control optimization, debug info, LTO, codegen units, panic strategy, and stripping with build-time and artifact trade-offs.
- A benchmark committed without an execution policy can rot; document when, where, and how regression thresholds are interpreted.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Unknown hotspot | Profile first | Optimizing guesses wastes complexity |
| Small pure function | Microbenchmark | Isolates algorithm and allocation cost |
| Service latency | End-to-end representative load | Queues, I/O, runtime, and contention dominate |
| Compile-time regression | Cargo timings and clean or incremental controls | Runtime profilers answer the wrong question |
| Unsafe optimization proposal | Safe baseline and measured threshold first | Soundness debt needs material value |

## Common Failure Modes

- Benchmarking debug builds or comparing different feature, target, hardware, or load conditions.
- Reporting one timing sample without variance, warmup, or noise analysis.
- Optimizing allocation or cloning that is not visible in the profile.
- Changing hash order, floating-point behavior, errors, or cancellation while claiming semantics are preserved.
- Committing complex caching, pooling, SIMD, or unsafe code for an unmeasured future load.

## Required Evidence

- Metric, workload, baseline, environment, toolchain, profile, features, target, and correctness oracle.
- Profile or counter evidence identifying the bottleneck and its share of cost.
- Repeated before-and-after results with variance and magnitude, not only a percentage.
- Functional equivalence checks, trade-offs, regression policy, and unmeasured deployment contexts.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-performance/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.

## Design protocol map

- [Measurement and optimization decision model](./performance-overview.md)
- [Detailed optimization guide](./performance-optimization-guide.md)

Begin from a reproducible workload and release-mode baseline. Treat suggested crates, SIMD, allocation strategies, and compiler settings as candidates that require current toolchain and target evidence.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-cache`](../../rust-architecture/references/domains/cache.md) — supporting; Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.
- [`rust-concurrency`](../../rust-concurrency/references/concurrency.md) — supporting; Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.
- [`rust-const`](../../rust-stable/references/const.md) — supporting; Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.
- [`rust-database`](../../rust-architecture/references/domains/database.md) — supporting; Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- [`rust-dpdk`](../../rust-systems-networking/references/dpdk.md) — supporting; Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.
- [`rust-ebpf`](../../rust-systems-networking/references/ebpf.md) — supporting; Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.
- [`rust-gpu`](../../rust-gpu/references/gpu.md) — supporting; Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.
- [`rust-observability`](../../rust-observability/references/observability.md) — supporting; Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.
- [`rust-performance`](./performance.md) — primary; Baselines, profiling, allocation, cache behavior, batching, contention, latency distributions, throughput, and regression evidence.
- [`rust-zero-cost`](./zero-cost.md) — primary; Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
