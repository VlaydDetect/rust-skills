# opt-target-cpu

> Use `target-cpu=native` for maximum performance on known deployment targets

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-cargo-build`, `rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `target-cpu=native` for maximum performance on known deployment targets.

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

By default, Rust compiles for a generic x86-64 baseline (roughly Sandy Bridge era). Modern CPUs have SIMD extensions (AVX2, AVX-512), improved instructions, and micro-architectural optimizations that go unused. `target-cpu=native` enables all features of your current CPU, potentially unlocking significant speedups.

## Bad

```toml
# Cargo.toml - compiles for generic x86-64
[profile.release]
# No target-cpu specified
# Binary works everywhere but uses only SSE2
```

## Good

```toml
# .cargo/config.toml - for known deployment target
[build]
rustflags = ["-C", "target-cpu=native"]

# Or specific CPU for cross-compilation
# rustflags = ["-C", "target-cpu=skylake"]
```

## Via Environment

```bash
# Build with native optimizations
RUSTFLAGS="-C target-cpu=native" cargo build --release

# Check what features are enabled
rustc --print cfg -C target-cpu=native | grep target_feature
```

## Common Target CPUs

```bash
# x86-64 targets
target-cpu=native          # Current machine
target-cpu=x86-64          # Baseline (SSE2)
target-cpu=x86-64-v2       # SSE4.2, POPCNT
target-cpu=x86-64-v3       # AVX2, BMI2
target-cpu=x86-64-v4       # AVX-512

# Intel specific
target-cpu=skylake         # 6th gen Core
target-cpu=alderlake       # 12th gen Core

# AMD specific
target-cpu=znver3          # Zen 3
target-cpu=znver4          # Zen 4

# ARM
target-cpu=apple-m1        # Apple Silicon
target-cpu=neoverse-n1     # AWS Graviton2
```

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

```bash
# Build multiple binaries
RUSTFLAGS="-C target-cpu=x86-64" cargo build --release
mv target/release/app target/release/app-generic

RUSTFLAGS="-C target-cpu=x86-64-v3" cargo build --release
mv target/release/app target/release/app-avx2

# Select at runtime
if supports_avx2; then
    ./app-avx2
else
    ./app-generic
fi
```

## Cargo Configuration

```toml
# .cargo/config.toml

# Native builds for development
[target.x86_64-unknown-linux-gnu]
rustflags = ["-C", "target-cpu=native"]

# AWS deployment (Graviton2)
[target.aarch64-unknown-linux-gnu]
rustflags = ["-C", "target-cpu=neoverse-n1"]

# Intel server deployment
[target.x86_64-unknown-linux-gnu.deployment]
rustflags = ["-C", "target-cpu=skylake-avx512"]
```

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

# View generated assembly
cargo asm --rust --release my_crate::hot_function
```

## Related Rules
- [opt-lto-release](./opt-lto-release.md) - Combine with LTO
- [opt-simd-portable](./opt-simd-portable.md) - Portable SIMD
- [opt-codegen-units](./opt-codegen-units.md) - Single codegen unit
