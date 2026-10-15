# Rust Profiling Guide

## Select the Measurement Layer

| Question | Evidence to start with | What it cannot establish alone |
|---|---|---|
| Cost of a stable isolated operation | Criterion with representative input groups | Service queueing, I/O or p99 latency |
| Which functions consume CPU | Sampling stacks with usable symbols | Waiting time or an optimization's speedup |
| Why request completion stalls | Correlated timeline, scheduler and I/O trace | Causality from an unrelated coincident event |
| Why memory grows or allocation is expensive | Allocation/lifetime profile plus process memory | RSS from summing requested bytes |
| Why a loop stalls | CPU-specific counters and final generated code | A universal cache-miss/IPC threshold |
| Why a build or binary is large | Cargo timings, sections, symbols, compiler/linker evidence | Runtime speed from fewer bytes |

Do not collect every tool by default. Obtain one observation that changes the next decision, validate it, then escalate only if uncertainty remains.

## Experiment Identity

Record the source state including dirty changes, exact command, tool versions, rustc/LLVM, target, package/target selection, feature set, effective profile and flags, allocator, runtime/executor and worker count. Record hardware, OS/kernel, runner class, power/thermal/load state, workload seed/corpus, useful work units and cold/warm policy.

Use the project-owned `profiling` profile if present. Otherwise propose a release-derived custom profile with sufficient debug information and unstripped symbols; do not assume that every repository already defines it. Creating or changing configuration is an implementation action. Frame-pointer or unwind changes can perturb code generation and must be recorded. Do not compare an instrumented capture's time to an uninstrumented benchmark as a speedup.

Resolve the executable from Cargo output or its artifact messages rather than guessing the latest file. On Windows MSVC, preserve the matching EXE/PDB and verify the recorded PDB identity (GUID/age) where tooling exposes it; matching stems are a useful selection check, not proof of identity. On ELF/Mach-O, retain the corresponding build ID/UUID and debug files. Keep the binary and source revision used by the capture even after rebuilding.

## Tool Selection

Use the canonical [cross-platform matrix](../../rust-performance/references/low-level/rust-profiling.md). It covers Criterion/Divan, perf, samply, cargo-flamegraph, pprof-rs, heap profilers, Tracy, vendor profilers and WPR/WPA. Check the exact installed version and OS backend: a common frontend does not imply identical capabilities.

For compiler inspection, prefer available LLVM tools from the selected Rust toolchain, with cargo-binutils as an optional artifact-selection/demangling wrapper. Resolve the installed `llvm-tools-preview`/`llvm-tools` component and actual executable location; adding it does not put every tool on PATH. Never assume BOLT or llvm-mca is bundled. `cargo-show-asm` can inspect assembly/IR/MIR when supported, but check its final target and Windows limitations. Inspect the final linked artifact when LTO or inlining changes the code of interest.

Use cargo-bloat or LLVM size/objdump for code-size attribution. Specify section/file size versus deployed size, symbols and debug data; a smaller binary can still execute more slowly. For build time, compare clean and incremental scenarios separately and keep cache state, changed inputs, jobs and linking equivalent; `rust-cargo-build` owns configuration changes.

Callgrind/Cachegrind and an existing Gungraun harness can provide instruction/model counters for focused CI regression checks. Their modeled cycles/cache behavior are not measurements of the deployment CPU's elapsed time. `llvm-mca` similarly tests a scheduling-model hypothesis, with assumptions about memory and aliasing; confirm on hardware.

## Output Contract

Return the metric and scope, validity verdict, absolute observations, uncertainty, artifact identities, attribution hypothesis, a disconfirming test, and unavailable evidence. Label synthetic fixtures, model simulations and article-reported numbers clearly. Do not interpret an unmeasured proposed optimization as established performance evidence.

Use [benchmark analysis](benchmark-analysis.md) for statistical decisions, [profile interpretation](profile-interpretation.md) for resource attribution, and the [PGO/BOLT protocol](../../rust-performance/references/low-level/pgo.md) only when training or evaluating feedback-directed builds. Miri and sanitizer runs remain correctness evidence under [rust-unsafe](../../rust-unsafe/references/low-level/rust-sanitizers-miri.md).

If an installed Miri fails while preparing a sysroot or unpacking cached crates inside a sandbox, use that protocol's permission diagnosis and authorized normal-account retry. Do not infer a missing component from the outer Cargo error or compare runs across changed test contracts.
