# Specialized Rust Performance Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product Routing and Baseline

- Primary owner: `$rust-performance`.
- Supporting profiles when triggered: `$rust-cargo-build` for profiles and codegen inputs, `$rust-platforms` for process-global allocators and OS constraints, `$rust-observability` for tracing span semantics, and `$rust-unsafe`/`$rust-unsafe-ffi` for sanitizer and soundness boundaries.
- Retained scope: benchmarks, CPU and latency profiles, allocations, cache behavior, batching, contention, timelines, latency distributions, throughput, and regression evidence.
- Baseline correction: profile the actual target and workload before optimizing. A dependency swap, allocator, unsafe path, instrumentation layer, or compiler setting requires a measured benefit and explicit cost.

## Workflow

1. Name the metric, correctness oracle, workload, target, baseline, acceptable variance, and environment controls.
2. Choose Criterion for maintained microbenchmarks or Divan for a deliberately minimal exploratory benchmark.
3. Build release-like code with readable symbols; use the project-owned `profiling` profile for profiler captures.
4. Select the smallest tool that answers the question:
   - sampled stacks for CPU attribution;
   - sampled or exact allocation tracking for heap behavior;
   - PMU counters for cache, branches, IPC, or bandwidth;
   - Tracy for application timelines and Windows Performance Toolkit for scheduler/I/O causality.
5. Form one hypothesis, change one variable, and rerun the identical benchmark and correctness checks.
6. Keep the change only when the magnitude exceeds noise and the new complexity, memory, build, startup, and portability costs are acceptable.

## Invariants

- Flamegraph width is sample proportion, not elapsed timeline or proof of speedup.
- Sampling misses events; exact allocation tracking changes runtime cost substantially.
- Counter names, availability, skid, multiplexing, and useful ratios are CPU/OS/tool-specific.
- A microbenchmark does not prove service tail latency, queueing, startup, I/O, or scheduler behavior.
- A benchmark produced with different profiles, flags, features, allocators, or workload conditions is not a baseline comparison.
- Passing Miri or one sanitizer execution supports but does not replace the unsafe/FFI invariant proof.

## Optimization Candidate Gate

Consider allocation reuse, data layout, batching, collection changes, parallelism, SIMD, caching, pooling, custom allocators, LTO, or unsafe code only after evidence connects that candidate to the measured bottleneck. Preserve ordering, errors, cancellation, floating-point policy, resource limits, and supported targets.

Do not turn generic advice such as “iterators are faster,” “use Rayon,” “use SmallVec,” “box large values,” “switch allocator,” or “enable LTO” into repository policy. Each may improve or regress a real workload.

## Required Record

- exact benchmark and profiler commands;
- resolved framework/tool versions;
- Cargo profile, target, features, relevant flags, allocator, and symbol policy;
- workload and environment controls;
- raw output location and whether it contains sensitive source, symbols, or runtime data;
- before/after distributions, correctness evidence, trade-offs, and unmeasured targets.

## References

- [Rust Performance field guide](./guide.md)
- [Criterion and Divan implementation guide](./performance-optimization-guide.md)
- [Cross-platform profiling protocol](./low-level/rust-profiling.md)
- [Hardware counter protocol](./low-level/hardware-counters.md)
- [Windows vendor and OS profiler protocol](./low-level/intel-vtune-amd-uprof.md)
