# Low-level Rust Sanitizers and Miri Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Scope

- Primary owner: `$rust-unsafe`.
- Supporting profiles: `$rust-unsafe-ffi` for foreign code/runtime coverage, `$rust-cargo-build` for target/build mechanics, `$rust-verify` for execution, and `$debugging` for a concrete failure.
- Retained scope: Miri and rustc sanitizer selection, explicit target/runtime coverage, report interpretation, unsafe validation, and residual proof obligations.
- Baseline correction: Rust does not expose an `undefined` sanitizer mode. Miri and sanitizers execute bounded inputs/configurations; neither proves soundness across all calls, targets, optimizations, foreign code, or schedules.

## Required Context

- unsafe operation and safe caller contract;
- target triple, toolchain/channel, host versus target build roles, and whether `build-std` is required;
- selected sanitizer failure class and current rustc target support;
- executed inputs, concurrency schedules, features, allocator, and optimization profile;
- C/C++/other-language compiler flags, sanitizer runtime ownership, and every uninstrumented native dependency;
- remaining provenance, alignment, initialization, validity, aliasing, lifetime, layout, thread, panic, and drop obligations.

## Decision Protocol

1. Write the local unsafe/FFI invariants before selecting a dynamic tool.
2. Select Miri for supported MIR execution or one sanitizer mode documented by the current rustc for the exact target and failure class.
3. Use the repository-pinned nightly when required. If it or the target component is absent, report `SKIP`; do not install or switch toolchains implicitly.
4. Pass an explicit `--target` for sanitizer builds so command-scoped `RUSTFLAGS` do not unintentionally instrument host build scripts or proc macros.
5. Use `-Z build-std` when the selected mode/target requires the standard library to be rebuilt and instrumented.
6. For C/C++ or another instrumented language, compile the native side with the matching Clang sanitizer/runtime and use rustc `external-clangrt` when the current official contract requires a shared external runtime.
7. Minimize the reproducer, interpret the first causally relevant diagnostic, and record every uninstrumented library, allocator, runtime, input, target, and schedule.
8. Keep the manual safety proof authoritative after the dynamic run.

## Tool Boundaries

| Question | Evidence |
|---|---|
| Rust aliasing, validity, provenance, selected UB patterns | Miri on supported code/inputs |
| Heap/stack out-of-bounds, use-after-free, selected leaks | current rustc Address/Leak sanitizer on a supported target |
| Data race in an executed schedule | current rustc Thread sanitizer on a supported target |
| Uninitialized reads through fully instrumented code | current rustc Memory sanitizer with matching native/runtime coverage |
| C/C++ undefined-behavior checks | Clang UBSan on the native side; do not describe it as Rust `-Zsanitizer=undefined` |
| FFI control-flow compatibility | current CFI contract with compatible LTO/native instrumentation where supported |

Do not combine sanitizer flags by analogy. Check the current official list, target matrix, incompatibilities, runtime requirements, and known limitations for every run.

## Allocator and FFI Caveats

- A custom/global allocator can change or hide sanitizer behavior. Use the system allocator or the allocator's documented sanitizer integration when the investigation requires it, and state the resulting blind spots.
- Memory created on one side of FFI must still be destroyed by its paired allocator/runtime.
- Instrumenting only Rust does not observe bugs wholly inside an uninstrumented C/C++ library; instrumenting only native code does not prove Rust unsafe invariants.
- Static and dynamic sanitizer runtimes, multiple heaps, preloaded allocators, and crash/profiler hooks can conflict. Resolve one runtime/allocator path for the run.

## Guardrails

- No implicit nightly/component installation, target addition, privilege change, global `RUSTFLAGS`, host configuration, or lockfile mutation.
- No claim that passing Miri/ASan/TSan/MSan proves all inputs, schedules, targets, optimizations, FFI, or soundness.
- Record exact command, toolchain, target, profile/features, native compiler/runtime, allocator, executed scope, diagnostic, and residual proof.

## Evidence Gate

Reviewed 2026-08-30.

- [rustc sanitizer reference](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html) — current modes, targets, `--target`, `build-std`, and `external-clangrt`.
- [Miri](https://github.com/rust-lang/miri/) — current setup, coverage, flags, and limitations.
