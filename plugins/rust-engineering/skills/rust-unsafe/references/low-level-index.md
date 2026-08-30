# Low-level references for `rust-unsafe`

Read the shared [tooling baseline](../../rust-research/references/low-level-tooling-baseline.md) first when a command, artifact path, toolchain, target, profiler, sanitizer, privilege, or external tool is involved. Then load only the matching family.

- [`abi-and-calling-conventions`](../../rust-unsafe-ffi/references/low-level/abi-and-calling-conventions.md) — supporting; System V, AAPCS, RISC-V, stack frames, registers, variadics, unwind, and compiler-output verification.
- [`af-xdp`](../../rust-systems-networking/references/low-level/af-xdp.md) — supporting; UMEM ownership, fill/completion and RX/TX rings, XDP redirect, copy/zero-copy modes, queue binding, and packet lifecycle.
- [`concurrency-debugging`](../../debugging/references/low-level/concurrency-debugging.md) — supporting; Race, deadlock, lock-order, atomic-ordering, happens-before, and thread-state diagnosis.
- [`custom-allocators`](low-level/custom-allocators.md) — primary; Allocator invariants, composition-root policy, mimalloc-pprof/dhat evidence, sanitizer integration, FFI pairing, fragmentation, concurrency, and benchmarking.
- [`dpdk`](../../rust-systems-networking/references/low-level/dpdk.md) — supporting; EAL, huge pages, PMDs, mempools/mbufs, RX/TX bursts, rings, RSS, NUMA, affinity, and pipeline topology.
- [`ebpf-rust`](../../rust-systems-networking/references/low-level/ebpf-rust.md) — supporting; Kernel/user split, verifier constraints, program and map types, BTF/CO-RE, attachment, event transport, and load-failure diagnosis.
- [`embedded-rust`](../../rust-architecture/references/low-level/embedded-rust.md) — supporting; Target and memory layout, no_std entry/panic, flashing/debugging, compact telemetry, interrupts, concurrency models, and HAL ownership.
- [`fuzzing`](../../rust-testing/references/low-level/fuzzing.md) — supporting; Target design, corpus, dictionary, crash reproduction, minimization, sanitizer composition, structure-aware inputs, and bounded CI campaigns.
- [`memory-model`](../../rust-concurrency/references/low-level/memory-model.md) — supporting; Atomic ordering, happens-before, release sequences, fences, publication, lock-free state machines, and common ordering failures.
- [`rust-ffi`](../../rust-unsafe-ffi/references/low-level/rust-ffi.md) — supporting; Manual and generated bindings, sys-crate layering, safe wrappers, exported C APIs, linking, ownership transfer, and error translation.
- [`rust-no-std`](../../rust-architecture/references/low-level/rust-no-std.md) — supporting; core/alloc/std capability boundaries, allocator and panic ownership, portable libraries, target configuration, and host-side testing.
- [`rust-sanitizers-miri`](low-level/rust-sanitizers-miri.md) — primary; Miri and exact rustc sanitizer target selection, build-std/external-clangrt, FFI/native coverage, interpretation, and residual proof.
- [`rust-security`](../../rust-architecture/references/low-level/rust-security.md) — supporting; Threat boundaries, dependency advisories and policy, FFI, fuzzing, unsafe validation, supply-chain inputs, and release hardening.
- [`rust-unsafe`](low-level/rust-unsafe.md) — primary; Unsafe operations, raw pointers, traits, safe wrappers, transmute, UnsafeCell, provenance, aliasing, initialization, and drop.
- [`sanitizers`](low-level/sanitizers.md) — primary; ASan/LSan/TSan/MSan/CFI selection, explicit target, matching C/C++ runtime, custom allocators, suppression policy, and residual gaps.
- [`simd-intrinsics`](../../rust-performance/references/low-level/simd-intrinsics.md) — supporting; Auto-vectorization, runtime feature detection, x86 and ARM intrinsics, alignment, dispatch, scalar fallbacks, and generated assembly.
- [`valgrind`](../../rust-performance/references/low-level/valgrind.md) — supporting; Memcheck, leak categories, suppressions, Cachegrind, Callgrind, Massif, overhead, and native-code coverage.

`primary` owns the decision. `supporting` contributes one bounded constraint and then returns ownership. Topic names are references, not additional product skills.
