# Low-level references for `debugging`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`binutils`](low-level/binutils.md) — primary; Archive, strip, objcopy, address translation, demangling, strings, headers, disassembly, and cross-tool selection.
- [`concurrency-debugging`](low-level/concurrency-debugging.md) — primary; Race, deadlock, lock-order, atomic-ordering, happens-before, and thread-state diagnosis.
- [`core-dumps`](low-level/core-dumps.md) — primary; Core/minidump acquisition, build identity, symbols, debugger loading, thread triage, and missing-symbol recovery.
- [`cpu-pipelines-and-hazards`](../../rust-performance/references/low-level/cpu-pipelines-and-hazards.md) — supporting; Pipeline dependencies, control and structural hazards, execution ports, instruction-level parallelism, and uop evidence.
- [`debug-optimized-builds`](low-level/debug-optimized-builds.md) — primary; Inlined frames, optimized-out values, line-table drift, scheduler locking, split debug information, and profile trade-offs.
- [`dwarf-debug-format`](low-level/dwarf-debug-format.md) — primary; DWARF sections and DIEs, line and unwind data, split DWARF, debuginfod, LTO interactions, stripping, and separate symbols.
- [`dynamic-linking`](../../rust-cargo-build/references/low-level/dynamic-linking.md) — supporting; Shared-library identity, SONAME, RPATH/RUNPATH, loader search, plugins, interposition, visibility, and loader errors.
- [`elf-inspection`](low-level/elf-inspection.md) — primary; ELF identity, sections, symbols, dynamic dependencies, disassembly, hardening properties, size, and build IDs.
- [`flamegraphs`](../../rust-performance/references/low-level/flamegraphs.md) — supporting; Sampling-stack capture, folded stacks, differential views, callgrind and alternate inputs, graph interpretation, and follow-up measurement.
- [`gdb`](low-level/gdb.md) — primary; GDB startup, breakpoints, watchpoints, state and thread inspection, reverse and remote debugging, scripting, and common symbol failures.
- [`hardware-counters`](../../rust-performance/references/low-level/hardware-counters.md) — supporting; PMU event selection, perf stat/record, derived metrics, raw events, source attribution, PAPI/PCM, multiplexing, and counter limitations.
- [`heaptrack`](../../rust-performance/references/low-level/heaptrack.md) — supporting; Allocation capture, symbol quality, retained versus peak memory, call-stack attribution, filtering, run comparison, and Rust allocator visibility.
- [`intel-vtune-amd-uprof`](../../rust-performance/references/low-level/intel-vtune-amd-uprof.md) — supporting; Vendor profiler selection, hotspots, microarchitecture, memory access, pipeline stalls, and roofline reasoning.
- [`linux-perf`](../../rust-performance/references/low-level/linux-perf.md) — supporting; perf stat, sampling, reporting, annotation, live analysis, events, stack collection, and failure diagnosis.
- [`lldb`](low-level/lldb.md) — primary; LLDB startup, breakpoints, expressions, watchpoints, threads, Apple behavior, IDE integration, and scripting.
- [`rust-async-internals`](../../rust-concurrency/references/low-level/rust-async-internals.md) — supporting; Future polling, Waker replacement, task scheduling, pinning, cancellation, blocking boundaries, and async diagnostics.
- [`rust-debugging`](low-level/rust-debugging.md) — primary; Debug-profile selection, Rust-aware GDB/LLDB, backtraces, panics, structured instrumentation, and async task inspection.
- [`rust-profiling`](../../rust-performance/references/low-level/rust-profiling.md) — supporting; Representative workload profiling, symbols, perf/flamegraphs, allocation analysis, Criterion, binary size, and monomorphization evidence.
- [`rust-sanitizers-miri`](../../rust-unsafe/references/low-level/rust-sanitizers-miri.md) — supporting; Miri and Rust sanitizer selection, execution scope, report interpretation, unsafe-code validation, and residual proof obligations.
- [`strace-ltrace`](low-level/strace-ltrace.md) — primary; System-call and dynamic-library tracing, filtering, errno diagnosis, timing, attachment, seccomp investigation, and bounded capture.
- [`valgrind`](../../rust-performance/references/low-level/valgrind.md) — supporting; Memcheck, leak categories, suppressions, Cachegrind, Callgrind, Massif, overhead, and native-code coverage.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Source family names are references, not additional product skills.
