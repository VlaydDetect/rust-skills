# Rust PGO and LLVM BOLT

## Ownership and Applicability

`rust-optimization` owns whether feedback-directed optimization is worth its training, release and portability costs. `rust-profiling` owns representative workload design and independent comparison; `rust-cargo-build` owns effective flags and linking. Keep this public reference path stable.

Consider PGO for a measured CPU/code-layout/branch/inlining problem, not an unexplained slowdown, I/O wait or correctness issue. A profile trains the compiler on the exercised workload; more training of an unrepresentative benchmark can make deployment performance worse.

## Establish the Build Contract

Record source state, rustc/LLVM, target CPU/features, profile, Cargo features, native libraries, linker, LTO and other flags. Use one controlled baseline without PGO and retain its exact artifact. Keep equivalent settings between generation/use builds except the required instrumentation/profile-use differences.

Resolve `llvm-profdata` compatible with the selected compiler, preferably from that toolchain's installed LLVM tools. Check the actual `llvm-tools-preview`/`llvm-tools` component and executable location; it is not automatically on PATH. Do not assume an arbitrary system LLVM can read the profile format.

## Instrumentation PGO Workflow

1. Create a fresh task-owned profile directory, leaving unrelated evidence untouched. Use absolute paths and a collision-safe profile naming pattern when concurrent processes generate data.
2. Build an optimized instrumented artifact with `-Cprofile-generate=<absolute-directory>`. Pass an explicit Cargo `--target` so host build scripts/proc macros are not accidentally instrumented; preserve existing flags rather than replacing them silently.
3. Run that exact artifact on training inputs that exercise the important workload mix, including infrequent but valuable paths. Unit tests can add coverage but are not automatically representative training.
4. Merge the resulting `.profraw` files with compatible `llvm-profdata merge -o <absolute-file> <profile-inputs>`. Inspect merge diagnostics and `llvm-profdata show` coverage/counts. Do not mix unrelated builds, stale profiles or duplicates that accidentally overweight one workload.
5. Rebuild using `-Cprofile-use=<absolute-file>` with the same controlling configuration. Inspect missing-function/hash/coverage warnings; where supported, the LLVM missing-function warning can expose profile gaps. Do not suppress a mismatch and claim effective coverage.
6. Evaluate the optimized final artifact on held-out representative inputs plus training scenarios. Compare baseline, PGO and any additional stage separately, with native uninstrumented performance measurements and functional checks.

Rust's documented workflow is instrumentation-based PGO. Sample-based LLVM workflows are separate toolchain-specific branches; a VTune or perf capture is not automatically consumable by `-Cprofile-use`.

## Optional cargo-pgo Adapter

When already available, inspect the installed `cargo pgo --help` and `cargo pgo info`. Common upstream commands are `cargo pgo instrument build -- <cargo-args>` (or `cargo pgo build`) and `cargo pgo optimize build -- <cargo-args>`. Resolve their current output paths and flag behavior instead of copying a fixed path. The adapter normally chooses release builds; it does not remove the requirement to preserve features, target and training identity. Installation is a separate action.

## BOLT Post-link Branch

BOLT is a post-link optimizer, not a Rust compiler mode or a generic Windows PE tool. Confirm the installed BOLT supports the exact architecture/format; upstream's documented path targets x86-64 and AArch64 ELF. Retain unstripped symbols, and emit relocations with the actual ELF linker's supported option when needed for useful layout transformations. Inspect the final binary for relocation sections rather than passing GNU flags to an MSVC linker.

Collect a BOLT profile against the exact input binary using the supported sampling or instrumentation path. For perf data, check event/branch-stack support and convert using the matching `perf2bolt` workflow; instrumentation produces BOLT data through a different path. A profile from a pre-PGO binary must not be reused as though it belonged to a rebuilt PGO artifact.

With a compatible cargo-pgo version, the optional `cargo pgo bolt build`/`cargo pgo bolt optimize` adapter creates separate instrumented/optimized binaries. Read the tool's reported paths and execute those artifacts, not the ordinary release binary by mistake. Tool support is experimental; retain the pre-BOLT artifact and review warnings, unwind/debug behavior, correctness, startup, size and representative performance before adoption.

If combining PGO and BOLT, evaluate baseline -> PGO -> BOLT applied to that PGO artifact. Train the BOLT stage again against its actual input. Never overwrite the only known-good binary or infer that independent percentage gains multiply under a different workload.

## Acceptance and Maintenance

Use the same benchmark contract as source optimizations. Include held-out distributions, critical tails, cold start, binary size, build/training time and supported deployment CPUs. Tie profiles to source/toolchain/build identities, define retraining triggers, and reject stale coverage after code or workload drift. If the tool, format, profile, permissions or hardware are absent, report `SKIP` and its gap; do not install tools or weaken policy implicitly.

## Official Command Contracts

Check the exact toolchain/tool version before execution: [Rust PGO](https://doc.rust-lang.org/rustc/profile-guided-optimization.html), [cargo-pgo commands](https://github.com/Kobzol/cargo-pgo), and [BOLT input/collection requirements](https://github.com/llvm/llvm-project/tree/main/bolt). These links establish technical command contracts; article attribution is kept in the product notices.
