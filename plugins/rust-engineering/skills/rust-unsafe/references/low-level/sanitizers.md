# Low-level Sanitizers Protocol

> Focused decision protocol; examples are evidence, not automatic product policy.

## Routing and Scope

- Primary owner: `$rust-unsafe` for Rust validity and report interpretation.
- `$rust-unsafe-ffi` owns ABI, foreign ownership, allocator pairing, native compiler/runtime, and cross-language coverage.
- `$rust-cargo-build` supports explicit target, build-std, linker, and host/target mechanics; `$rust-verify` executes the selected evidence.
- Canonical Rust selection lives in [Rust sanitizers and Miri](./rust-sanitizers-miri.md).
- Retained scope: ASan, LSan, TSan, MSan, hardware-assisted modes, CFI, native dependency instrumentation, runtime ownership, suppressions, and residual gaps.

## Selection Rules

1. Query the current rustc sanitizer list and target matrix; never infer support from another target or from Clang alone.
2. Select one failure class and use an explicit `--target`.
3. Use the repository-pinned nightly and `build-std` only when the selected official workflow requires them.
4. Instrument every relevant C/C++ object and library with the matching Clang sanitizer flags/runtime. Use `external-clangrt` where the current Rust/native integration requires the external runtime.
5. Keep generated bindings, build scripts, proc macros, host tools, target code, and foreign libraries distinct; command-scoped flags must not accidentally spread across host builds.
6. Use suppressions only for an understood external finding with recorded ownership and expiry; never suppress an unexplained first diagnostic.

## FFI and Custom Allocator Coverage

- Rust and native code must agree on ABI, unwind policy, sanitizer runtime, and allocator pairing.
- An uninstrumented native library is a blind spot even when the Rust caller is instrumented.
- MSan generally needs all relevant code and libraries instrumented; partial instrumentation can produce unusable evidence.
- A custom allocator may require its documented sanitizer mode or replacement with the system allocator for the investigation. Record when this changes the workload.
- A C/C++ UBSan run is valid native evidence, but rustc has no `undefined` sanitizer mode and must not be configured as though it does.

## Effects and Reporting

Sanitizer builds create instrumented artifacts and execute code; some modes need matching runtimes, target components, or hardware. Missing prerequisites are `SKIP`. Never install a nightly/tool/runtime, add a target, mutate global flags, weaken host policy, or update dependencies automatically.

Record exact compiler/toolchain versions, target, flags, `build-std`/`external-clangrt` state, native objects covered, allocator/runtime, inputs/schedules, first causal report, suppressions, and residual gaps.

## Evidence Gate

Reviewed 2026-08-30.

- [rustc sanitizer reference](https://doc.rust-lang.org/beta/unstable-book/compiler-flags/sanitizer.html)
- [Clang sanitizer documentation](https://clang.llvm.org/docs/index.html)
- [Miri](https://github.com/rust-lang/miri/)

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.