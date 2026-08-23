# Low-level references for `rust-cargo-build`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`abi-and-calling-conventions`](../../rust-unsafe-ffi/references/low-level/abi-and-calling-conventions.md) — supporting; System V, AAPCS, RISC-V, stack frames, registers, variadics, unwind, and compiler-output verification.
- [`binary-hardening`](low-level/binary-hardening.md) — primary; Hardening-property inspection, compiler/linker mitigation families, control-flow integrity, platform mechanisms, and residual attack surface.
- [`binutils`](../../debugging/references/low-level/binutils.md) — supporting; Archive, strip, objcopy, address translation, demangling, strings, headers, disassembly, and cross-tool selection.
- [`build-acceleration`](../../rust-performance/references/low-level/build-acceleration.md) — supporting; Bottleneck diagnosis, compiler caches, distributed compilation, debug information, invalidation, hit-rate analysis, and cache correctness.
- [`cargo-workflows`](low-level/cargo-workflows.md) — primary; Workspace, feature, build-script, lockfile, cache, CI, and Cargo tool workflows.
- [`code-generation-and-backends`](../../rust-performance/references/low-level/code-generation-and-backends.md) — supporting; Compiler pipeline, LLVM lowering, target triples, calling-convention lowering, backend selection, and new-target feasibility.
- [`compiler-optimizations-deep`](../../rust-performance/references/low-level/compiler-optimizations-deep.md) — supporting; Optimization pipeline, vectorization diagnostics, register pressure, loop transforms, PGO, BOLT, and generated-code evidence.
- [`core-dumps`](../../debugging/references/low-level/core-dumps.md) — supporting; Core/minidump acquisition, build identity, symbols, debugger loading, thread triage, and missing-symbol recovery.
- [`debug-optimized-builds`](../../debugging/references/low-level/debug-optimized-builds.md) — supporting; Inlined frames, optimized-out values, line-table drift, scheduler locking, split debug information, and profile trade-offs.
- [`dwarf-debug-format`](../../debugging/references/low-level/dwarf-debug-format.md) — supporting; DWARF sections and DIEs, line and unwind data, split DWARF, debuginfod, LTO interactions, stripping, and separate symbols.
- [`dynamic-linking`](low-level/dynamic-linking.md) — primary; Shared-library identity, SONAME, RPATH/RUNPATH, loader search, plugins, interposition, visibility, and loader errors.
- [`embedded-rust`](../../rust-architecture/references/low-level/embedded-rust.md) — supporting; Target and memory layout, no_std entry/panic, flashing/debugging, compact telemetry, interrupts, concurrency models, and HAL ownership.
- [`flamegraphs`](../../rust-performance/references/low-level/flamegraphs.md) — supporting; Sampling-stack capture, folded stacks, differential views, callgrind and alternate inputs, graph interpretation, and follow-up measurement.
- [`gdb`](../../debugging/references/low-level/gdb.md) — supporting; GDB startup, breakpoints, watchpoints, state and thread inspection, reverse and remote debugging, scripting, and common symbol failures.
- [`heaptrack`](../../rust-performance/references/low-level/heaptrack.md) — supporting; Allocation capture, symbol quality, retained versus peak memory, call-stack attribution, filtering, run comparison, and Rust allocator visibility.
- [`linker-scripts`](low-level/linker-scripts.md) — primary; Memory regions, sections, VMA/LMA, startup initialization, placement, KEEP/ALIGN/PROVIDE, symbols, and map-based verification.
- [`linkers-lto`](low-level/linkers-lto.md) — primary; Linker selection, argument ordering, LTO modes, dead-code elimination, visibility, map files, and link-failure diagnosis.
- [`linux-perf`](../../rust-performance/references/low-level/linux-perf.md) — supporting; perf stat, sampling, reporting, annotation, live analysis, events, stack collection, and failure diagnosis.
- [`lldb`](../../debugging/references/low-level/lldb.md) — supporting; LLDB startup, breakpoints, expressions, watchpoints, threads, Apple behavior, IDE integration, and scripting.
- [`pgo`](../../rust-performance/references/low-level/pgo.md) — supporting; Instrumentation or sample profile collection, workload representativeness, profile merge/use, post-link optimization, and impact verification.
- [`rust-build-times`](../../rust-performance/references/low-level/rust-build-times.md) — supporting; Clean and incremental build measurement, Cargo timings, invalidation, monomorphization, caching, codegen backends, and linking.
- [`rust-cross`](low-level/rust-cross.md) — primary; Host/target separation, target support tiers, linker and runner configuration, native libraries, containers, emulators, and deployment validation.
- [`rust-debugging`](../../debugging/references/low-level/rust-debugging.md) — supporting; Debug-profile selection, Rust-aware GDB/LLDB, backtraces, panics, structured instrumentation, and async task inspection.
- [`rust-ffi`](../../rust-unsafe-ffi/references/low-level/rust-ffi.md) — supporting; Manual and generated bindings, sys-crate layering, safe wrappers, exported C APIs, linking, ownership transfer, and error translation.
- [`rust-no-std`](../../rust-architecture/references/low-level/rust-no-std.md) — supporting; core/alloc/std capability boundaries, allocator and panic ownership, portable libraries, target configuration, and host-side testing.
- [`rust-profiling`](../../rust-performance/references/low-level/rust-profiling.md) — supporting; Representative workload profiling, symbols, perf/flamegraphs, allocation analysis, Criterion, binary size, and monomorphization evidence.
- [`rustc-basics`](low-level/rustc-basics.md) — primary; Cargo profiles, rustflags precedence, target inspection, MIR/LLVM/assembly evidence, monomorphization, size, and diagnostic triage.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
