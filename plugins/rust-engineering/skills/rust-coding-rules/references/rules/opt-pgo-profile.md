# opt-pgo-profile

> Evaluate Profile-Guided Optimization against representative workloads

## Decision

Use PGO only when a measured CPU/codegen hypothesis justifies the cost of training, rebuilding and maintaining profiles. No percentage improvement is guaranteed.

## Apply When

A comparable native baseline and a representative workload identify branch, inlining or code-layout costs that compiler feedback could improve. The deployment target and release process can preserve profile/build identity.

## Avoid When

The primary limit is unexplained, correctness is wrong, I/O/queueing dominates, or only an unrelated microbenchmark is available. Do not assume a test corpus represents production.

## Algorithm

1. Read the [canonical PGO/BOLT protocol](../../../rust-performance/references/low-level/pgo.md) and resolve rustc/LLVM, target, features and effective flags with rust-cargo-build.
2. Retain an uninstrumented baseline, generate instrumentation in a fresh task-owned directory, and exercise a representative training mix.
3. Merge compatible profiles, inspect coverage/mismatch diagnostics, and rebuild with otherwise equivalent settings.
4. Compare the exact optimized artifact on held-out and training scenarios; record useful-work metrics, uncertainty and costs.

## Bad

Assume PGO gives a fixed speedup, train only a hot microbenchmark, copy a stale profile into another build, or feed raw perf.data directly to BOLT as merged BOLT profile data.

## Good

Use absolute profile paths, an explicit Cargo target, compatible llvm-profdata, independent evaluation and the same native comparison contract. Preserve unrelated flags and data. Use cargo-pgo only as an optional installed adapter; verify its current CLI and artifact paths.

## Trade-offs

Training/release complexity, build time, code size and workload sensitivity may outweigh a runtime gain. BOLT is a separate post-link experiment for supported ELF architectures, with exact-binary profile identity and symbol/relocation requirements; it is not a Windows PE optimization path.

## Prerequisites

- Current project MSRV, target, features, build settings and user requirements control the experiment.
- Tool and component installation, host-policy changes and publication require their own authorization.
- Preserve source/toolchain/build identity and select a collision-safe profile output policy for concurrent runs.

## Verification

Use rust-profiling for comparable estimates and held-out workload coverage. Check correctness, tails, startup, binary size and training/build cost. Report missing coverage, inconclusive results and unsupported targets rather than suppressing diagnostics.

## Representative Workloads

<!-- rust-example: fragment; missing: representative corpus, process implementation, project target and training/evaluation split -->
```rust
fn profile_workload() {
    for input in representative_training_inputs() {
        process(&input);
    }
}
```

This fragment selects training work; it is not a performance result. Keep independent evaluation inputs and do not derive a deployment claim from coverage alone.

## Related Rules

- [perf-profile-first](./perf-profile-first.md)
- [perf-release-profile](./perf-release-profile.md)
- [opt-lto-release](./opt-lto-release.md)
