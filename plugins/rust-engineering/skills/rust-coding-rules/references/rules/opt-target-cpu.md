# opt-target-cpu

> Evaluate `target-cpu` only for a measured workload and an exactly known deployment CPU contract

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-cargo-build`, `rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: compare an explicit deployment baseline with a target-specific build, preserving a portable fallback when the fleet is heterogeneous.

## Apply When

Apply when a reproducible profile or benchmark identifies a compiler, codegen, branch, cache, or target-specific bottleneck, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the workload, deployment target, or portability contract is unknown, or the expected benefit is speculative. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Hold toolchain, target, profile, features, inputs, and hardware constant; test one optimization hypothesis at a time.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

LTO, codegen, inlining, PGO, SIMD, and target tuning can trade build time, size, portability, debuggability, and determinism.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Compare repeated release-like measurements and artifact or codegen evidence while preserving functional behavior and fallback targets.

## Why It Matters

The effective CPU baseline comes from the target specification and selected toolchain. `target-cpu=native` asks that toolchain to tune for the build host and may enable host features, but it does not guarantee a speedup or compatibility with another machine. Inspect generated code and compare the real deployment workload.

## Bad

```toml
# Cargo.toml - compiles for generic x86-64
[profile.release]
# No target-cpu specified
# Binary works everywhere but uses only SSE2
```

## Good

For a homogeneous, documented deployment fleet, keep the setting target-scoped in `.cargo/config.toml` and use only a CPU name accepted by the pinned rustc for that target. Record the portable baseline and rollback condition beside the measurement; do not copy a placeholder or build-host value.

## Via Environment

```bash
# Local experiment on this build host; do not commit as a portable default
RUSTFLAGS="-C target-cpu=native" cargo build --release

# Check what features are enabled
rustc --print cfg -C target-cpu=native | grep target_feature
```

## Target CPU Availability

Do not preserve a static CPU-name table: accepted names and tuning behavior belong to the exact rustc/LLVM toolchain and target. Query that toolchain, then record the selected CPU, required features, oldest supported deployment host, and portable fallback in the measurement evidence.

## Feature Detection at Runtime

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Feature Detection at Runtime illustration -->
```rust
// For portable binaries that use native features when available
#[cfg(target_arch = "x86_64")]
fn process_fast(data: &[u8]) -> u64 {
    if is_x86_feature_detected!("avx2") {
        // SAFETY: only reached after avx2 is detected at runtime
        unsafe { process_avx2(data) }
    } else {
        process_generic(data)
    }
}

#[cfg(target_arch = "x86_64")]
#[target_feature(enable = "avx2")]
unsafe fn process_avx2(data: &[u8]) -> u64 {
    // an AVX2-optimized path would go here; delegate to the scalar version
    process_generic(data)
}

fn process_generic(data: &[u8]) -> u64 {
    data.iter().map(|&b| u64::from(b)).sum()
}
```

## Multi-Architecture Builds

Build and test each explicit target/CPU variant under a distinct, derived Cargo target directory and preserve its build metadata. Do not move files from an assumed `target/release` layout. Prefer one portable binary with runtime feature detection when its complexity and measured cost are justified.

## Cargo Configuration

Cargo configuration must use a valid `[target.<triple>]` table for the exact deployment triple. Cargo has no arbitrary `[target.<triple>.deployment]` profile namespace. Check rustflags precedence and host/build-script effects in the shared tooling baseline before committing a target policy.

## What Changes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the What Changes illustration -->
```rust
// With AVX2 enabled:
// - 256-bit SIMD operations
// - Better autovectorization
// - FMA (fused multiply-add)
// - BMI (bit manipulation)

// Example: sum of squares
fn sum_squares(data: &[f64]) -> f64 {
    data.iter().map(|x| x * x).sum()
}
// Generic: scalar loop
// AVX2: processes 4 f64s per iteration
```

## Checking Enabled Features

```bash
# What's enabled for native?
rustc --print cfg -C target-cpu=native | grep feature

# Compare generic vs native
rustc --print cfg -C target-cpu=x86-64 | grep feature
rustc --print cfg -C target-cpu=native | grep feature

# View generated assembly only if cargo-asm is already present and version-checked
cargo asm --rust --release my_crate::hot_function
```

## Related Rules
- [opt-lto-release](./opt-lto-release.md) - Combine with LTO
- [opt-simd-portable](./opt-simd-portable.md) - Portable SIMD
- [opt-codegen-units](./opt-codegen-units.md) - Single codegen unit
