# Low-level references for `rust-research`

Read the shared [tooling baseline](low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`branch-prediction-and-speculation`](../../rust-performance/references/low-level/branch-prediction-and-speculation.md) — supporting; Predictability, branch layout, misprediction measurement, speculation, and side-channel constraints.
- [`build-acceleration`](../../rust-performance/references/low-level/build-acceleration.md) — supporting; Bottleneck diagnosis, compiler caches, distributed compilation, debug information, invalidation, hit-rate analysis, and cache correctness.
- [`code-generation-and-backends`](../../rust-performance/references/low-level/code-generation-and-backends.md) — supporting; Compiler pipeline, LLVM lowering, target triples, calling-convention lowering, backend selection, and new-target feasibility.
- [`compiler-optimizations-deep`](../../rust-performance/references/low-level/compiler-optimizations-deep.md) — supporting; Optimization pipeline, vectorization diagnostics, register pressure, loop transforms, PGO, BOLT, and generated-code evidence.
- [`cpu-cache-opt`](../../rust-performance/references/low-level/cpu-cache-opt.md) — supporting; Counter-led cache diagnosis, data layout, traversal, false sharing, prefetch, blocking, and cache-aware algorithm choices.
- [`cpu-pipelines-and-hazards`](../../rust-performance/references/low-level/cpu-pipelines-and-hazards.md) — supporting; Pipeline dependencies, control and structural hazards, execution ports, instruction-level parallelism, and uop evidence.
- [`hardware-counters`](../../rust-performance/references/low-level/hardware-counters.md) — supporting; PMU event selection, perf stat/record, derived metrics, raw events, source attribution, PAPI/PCM, multiplexing, and counter limitations.
- [`intel-vtune-amd-uprof`](../../rust-performance/references/low-level/intel-vtune-amd-uprof.md) — supporting; Vendor profiler selection, hotspots, microarchitecture, memory access, pipeline stalls, and roofline reasoning.
- [`memory-hierarchy-and-caches`](../../rust-performance/references/low-level/memory-hierarchy-and-caches.md) — supporting; Cache hierarchy, lines, associativity, coherence, false sharing, locality, prefetching, and measurement.
- [`memory-model`](../../rust-concurrency/references/low-level/memory-model.md) — supporting; Atomic ordering, happens-before, release sequences, fences, publication, lock-free state machines, and common ordering failures.
- [`numa-programming`](../../rust-performance/references/low-level/numa-programming.md) — supporting; Topology discovery, memory placement, affinity, first touch, remote-access diagnosis, measurement, and fallback behavior.
- [`pgo`](../../rust-performance/references/low-level/pgo.md) — supporting; Instrumentation or sample profile collection, workload representativeness, profile merge/use, post-link optimization, and impact verification.
- [`rust-build-times`](../../rust-performance/references/low-level/rust-build-times.md) — supporting; Clean and incremental build measurement, Cargo timings, invalidation, monomorphization, caching, codegen backends, and linking.
- [`rustc-basics`](../../rust-cargo-build/references/low-level/rustc-basics.md) — supporting; Cargo profiles, rustflags precedence, target inspection, MIR/LLVM/assembly evidence, monomorphization, size, and diagnostic triage.
- [`virtual-memory-paging-and-tlb`](../../rust-performance/references/low-level/virtual-memory-paging-and-tlb.md) — supporting; Page translation, faults, TLB pressure, huge pages, mapping evidence, and embedded contrasts.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
