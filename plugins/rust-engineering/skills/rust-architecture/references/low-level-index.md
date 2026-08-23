# Low-level references for `rust-architecture`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`binary-hardening`](../../rust-cargo-build/references/low-level/binary-hardening.md) — supporting; Hardening-property inspection, compiler/linker mitigation families, control-flow integrity, platform mechanisms, and residual attack surface.
- [`branch-prediction-and-speculation`](../../rust-performance/references/low-level/branch-prediction-and-speculation.md) — supporting; Predictability, branch layout, misprediction measurement, speculation, and side-channel constraints.
- [`cpu-cache-opt`](../../rust-performance/references/low-level/cpu-cache-opt.md) — supporting; Counter-led cache diagnosis, data layout, traversal, false sharing, prefetch, blocking, and cache-aware algorithm choices.
- [`custom-allocators`](../../rust-unsafe/references/low-level/custom-allocators.md) — supporting; Pool, arena, global and system allocators, ownership, alignment, fragmentation, concurrency, teardown, and benchmarking.
- [`embedded-rust`](low-level/embedded-rust.md) — primary; Target and memory layout, no_std entry/panic, flashing/debugging, compact telemetry, interrupts, concurrency models, and HAL ownership.
- [`linker-scripts`](../../rust-cargo-build/references/low-level/linker-scripts.md) — supporting; Memory regions, sections, VMA/LMA, startup initialization, placement, KEEP/ALIGN/PROVIDE, symbols, and map-based verification.
- [`memory-hierarchy-and-caches`](../../rust-performance/references/low-level/memory-hierarchy-and-caches.md) — supporting; Cache hierarchy, lines, associativity, coherence, false sharing, locality, prefetching, and measurement.
- [`numa-programming`](../../rust-performance/references/low-level/numa-programming.md) — supporting; Topology discovery, memory placement, affinity, first touch, remote-access diagnosis, measurement, and fallback behavior.
- [`rust-no-std`](low-level/rust-no-std.md) — primary; core/alloc/std capability boundaries, allocator and panic ownership, portable libraries, target configuration, and host-side testing.
- [`rust-security`](low-level/rust-security.md) — primary; Threat boundaries, dependency advisories and policy, FFI, fuzzing, unsafe validation, supply-chain inputs, and release hardening.
- [`virtual-memory-paging-and-tlb`](../../rust-performance/references/low-level/virtual-memory-paging-and-tlb.md) — supporting; Page translation, faults, TLB pressure, huge pages, mapping evidence, and embedded contrasts.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.
