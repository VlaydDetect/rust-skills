# Performance Measurement and Optimization Model

> A reproducible metric and comparable baseline are required before an optimization becomes policy.

## Core Question

What resource limits the representative workload, and is the measured benefit worth the added cost?

## Decision Flow

1. Define the user-visible metric, correctness contract, workload, target, and acceptable variance.
2. Reproduce the baseline with fixed toolchain, profile, features, flags, allocator, inputs, and environment controls.
3. Classify the cost before selecting a tool:
   - CPU or latency: sampling stacks;
   - allocations, retained heap, or leaks: sampled or exact heap profiling;
   - cache, branches, IPC, or bandwidth: hardware counters;
   - locks, wakeups, frames, threads, GPU, or scheduler gaps: timeline or OS tracing;
   - compile time or binary size: Cargo/compiler-specific evidence.
4. Locate one bottleneck and write one causal hypothesis.
5. Apply the smallest behavior-preserving change that tests the hypothesis.
6. Repeat the same benchmark and correctness checks; keep or reject the change from evidence.

## Benchmark Choice

| Need | Default |
|---|---|
| Maintained regression evidence, baselines, profiler hooks | Criterion |
| Minimal exploratory function benchmark | Divan |
| Service latency, startup, I/O, queueing, contention | Representative end-to-end harness |

Divan is intentionally a small alternative. Move to Criterion before the result becomes a long-lived regression or optimization contract that needs stable baseline comparison or Criterion profiler integration.

## Evidence Before Technique

| Observed evidence | Candidate investigation, not an automatic fix |
|---|---|
| Allocation-heavy hot path | Ownership, capacity, reuse, batching, data representation |
| Poor cache locality or high miss rate | Access order, layout, working-set size, false sharing |
| Lock wait or off-CPU time | Critical-section scope, ownership, queueing, scheduling |
| Hot branch or instruction sequence | Algorithm, branch behavior, generated code, target dispatch |
| High retained memory | Lifetime, cache capacity, fragmentation, allocator behavior |
| High build time or size | Monomorphization, macros, dependency graph, codegen, linking |

Do not prescribe `SmallVec`, Rayon, an allocator, `repr(packed)`, LTO, pooling, sharding, SIMD, or unsafe code without the matching measurement and project constraints.

## Comparison Gate

A comparison is invalid when any controlling input differs without being part of the experiment:

- Cargo profile, target, features, `RUSTFLAGS`, PGO/LTO, panic strategy, debug info, or allocator;
- framework/tool version or benchmark implementation;
- workload, input distribution, cold/warm state, concurrency, runtime, or I/O dependency;
- hardware class, CPU frequency/power policy, thermal state, OS/kernel, or competing load.

Report absolute values, variance, and magnitude alongside percentages. A flamegraph or trace identifies where to investigate; it does not prove the before/after result.

## Handoffs

- [Criterion and Divan implementation](./performance-optimization-guide.md)
- [Cross-platform profiling matrix](./low-level/rust-profiling.md)
- [Cargo profile mechanics](../../rust-cargo-build/references/guide.md)
- [Allocator policy](../../rust-platforms/references/guide.md)
- [Unsafe and FFI sanitizer policy](../../rust-unsafe/references/low-level/sanitizers.md)
