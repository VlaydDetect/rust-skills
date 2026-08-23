# Low-level references for `rust-performance`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`af-xdp`](../../rust-systems-networking/references/low-level/af-xdp.md) — supporting; UMEM ownership, fill/completion and RX/TX rings, XDP redirect, copy/zero-copy modes, queue binding, and packet lifecycle.
- [`branch-prediction-and-speculation`](low-level/branch-prediction-and-speculation.md) — primary; Predictability, branch layout, misprediction measurement, speculation, and side-channel constraints.
- [`build-acceleration`](low-level/build-acceleration.md) — primary; Bottleneck diagnosis, compiler caches, distributed compilation, debug information, invalidation, hit-rate analysis, and cache correctness.
- [`code-generation-and-backends`](low-level/code-generation-and-backends.md) — primary; Compiler pipeline, LLVM lowering, target triples, calling-convention lowering, backend selection, and new-target feasibility.
- [`compiler-optimizations-deep`](low-level/compiler-optimizations-deep.md) — primary; Optimization pipeline, vectorization diagnostics, register pressure, loop transforms, PGO, BOLT, and generated-code evidence.
- [`cpu-cache-opt`](low-level/cpu-cache-opt.md) — primary; Counter-led cache diagnosis, data layout, traversal, false sharing, prefetch, blocking, and cache-aware algorithm choices.
- [`cpu-pipelines-and-hazards`](low-level/cpu-pipelines-and-hazards.md) — primary; Pipeline dependencies, control and structural hazards, execution ports, instruction-level parallelism, and uop evidence.
- [`custom-allocators`](../../rust-unsafe/references/low-level/custom-allocators.md) — supporting; Pool, arena, global and system allocators, ownership, alignment, fragmentation, concurrency, teardown, and benchmarking.
- [`debug-optimized-builds`](../../debugging/references/low-level/debug-optimized-builds.md) — supporting; Inlined frames, optimized-out values, line-table drift, scheduler locking, split debug information, and profile trade-offs.
- [`dpdk`](../../rust-systems-networking/references/low-level/dpdk.md) — supporting; EAL, huge pages, PMDs, mempools/mbufs, RX/TX bursts, rings, RSS, NUMA, affinity, and pipeline topology.
- [`dwarf-debug-format`](../../debugging/references/low-level/dwarf-debug-format.md) — supporting; DWARF sections and DIEs, line and unwind data, split DWARF, debuginfod, LTO interactions, stripping, and separate symbols.
- [`elf-inspection`](../../debugging/references/low-level/elf-inspection.md) — supporting; ELF identity, sections, symbols, dynamic dependencies, disassembly, hardening properties, size, and build IDs.
- [`flamegraphs`](low-level/flamegraphs.md) — primary; Sampling-stack capture, folded stacks, differential views, callgrind and alternate inputs, graph interpretation, and follow-up measurement.
- [`hardware-counters`](low-level/hardware-counters.md) — primary; PMU event selection, perf stat/record, derived metrics, raw events, source attribution, PAPI/PCM, multiplexing, and counter limitations.
- [`heaptrack`](low-level/heaptrack.md) — primary; Allocation capture, symbol quality, retained versus peak memory, call-stack attribution, filtering, run comparison, and Rust allocator visibility.
- [`intel-vtune-amd-uprof`](low-level/intel-vtune-amd-uprof.md) — primary; Vendor profiler selection, hotspots, microarchitecture, memory access, pipeline stalls, and roofline reasoning.
- [`io-uring`](../../rust-concurrency/references/low-level/io-uring.md) — supporting; Submission/completion ownership, operation lifetimes, registered resources, multishot operations, cancellation, zero-copy, and fallback I/O.
- [`linkers-lto`](../../rust-cargo-build/references/low-level/linkers-lto.md) — supporting; Linker selection, argument ordering, LTO modes, dead-code elimination, visibility, map files, and link-failure diagnosis.
- [`linux-perf`](low-level/linux-perf.md) — primary; perf stat, sampling, reporting, annotation, live analysis, events, stack collection, and failure diagnosis.
- [`memory-hierarchy-and-caches`](low-level/memory-hierarchy-and-caches.md) — primary; Cache hierarchy, lines, associativity, coherence, false sharing, locality, prefetching, and measurement.
- [`numa-programming`](low-level/numa-programming.md) — primary; Topology discovery, memory placement, affinity, first touch, remote-access diagnosis, measurement, and fallback behavior.
- [`pgo`](low-level/pgo.md) — primary; Instrumentation or sample profile collection, workload representativeness, profile merge/use, post-link optimization, and impact verification.
- [`rust-build-times`](low-level/rust-build-times.md) — primary; Clean and incremental build measurement, Cargo timings, invalidation, monomorphization, caching, codegen backends, and linking.
- [`rust-profiling`](low-level/rust-profiling.md) — primary; Representative workload profiling, symbols, perf/flamegraphs, allocation analysis, Criterion, binary size, and monomorphization evidence.
- [`rustc-basics`](../../rust-cargo-build/references/low-level/rustc-basics.md) — supporting; Cargo profiles, rustflags precedence, target inspection, MIR/LLVM/assembly evidence, monomorphization, size, and diagnostic triage.
- [`simd-intrinsics`](low-level/simd-intrinsics.md) — primary; Auto-vectorization, runtime feature detection, x86 and ARM intrinsics, alignment, dispatch, scalar fallbacks, and generated assembly.
- [`strace-ltrace`](../../debugging/references/low-level/strace-ltrace.md) — supporting; System-call and dynamic-library tracing, filtering, errno diagnosis, timing, attachment, seccomp investigation, and bounded capture.
- [`valgrind`](low-level/valgrind.md) — primary; Memcheck, leak categories, suppressions, Cachegrind, Callgrind, Massif, overhead, and native-code coverage.
- [`virtual-memory-paging-and-tlb`](low-level/virtual-memory-paging-and-tlb.md) — primary; Page translation, faults, TLB pressure, huge pages, mapping evidence, and embedded contrasts.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
