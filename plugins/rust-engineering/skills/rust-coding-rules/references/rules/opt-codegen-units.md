# opt-codegen-units

> Set `codegen-units = 1` for maximum optimization in release builds

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-cargo-build`, `rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Set `codegen-units = 1` for maximum optimization in release builds.

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

By default, Cargo splits code into multiple codegen units for parallel compilation. This speeds up builds but prevents some cross-unit optimizations. Setting `codegen-units = 1` allows LLVM to optimize across the entire crate, potentially improving runtime performance by 5-20% at the cost of slower builds.

## Bad

```toml
# Cargo.toml - default settings
[profile.release]
# codegen-units defaults to 16
# Fast to compile, but misses optimization opportunities
```

## Good

```toml
# Cargo.toml - optimized for runtime performance
[profile.release]
codegen-units = 1  # Single unit = better optimization
lto = true         # Link-time optimization
opt-level = 3      # Maximum optimization
```

## What codegen-units Affects

| Codegen Units | Compile Time | Runtime Performance | Memory Use |
|---------------|--------------|---------------------|------------|
| 16 (default)  | Faster       | Baseline            | Lower      |
| 4-8           | Moderate     | Slightly better     | Moderate   |
| 1             | Slower       | Best                | Higher     |

## How It Works

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the How It Works illustration -->
```rust
// With codegen-units = 16:
// - Crate split into 16 independent compilation units
// - Compiled in parallel
// - Limited visibility between units for optimization

// With codegen-units = 1:
// - Entire crate in single unit
// - LLVM sees all code at once
// - Can inline across module boundaries
// - Better dead code elimination
// - Better constant propagation
```

## Full Release Profile

```toml
[profile.release]
# Maximum runtime performance
opt-level = 3
lto = "fat"
codegen-units = 1
panic = "abort"      # Smaller binary, slight perf gain
strip = true         # Smaller binary

[profile.release-with-debug]
# Performance with debugging ability
inherits = "release"
debug = true         # Keep debug symbols
strip = false

[profile.bench]
# For benchmarking
inherits = "release"
```

## Build Time Trade-offs

```bash
# Default release build (fast compile)
cargo build --release
# Time: ~30s

# Optimized release build (slow compile, fast runtime)
# With codegen-units = 1, lto = "fat"
cargo build --release
# Time: ~2-5min, but potentially 10-20% faster binary
```

## Per-Profile Configuration

```toml
# Fast debug builds
[profile.dev]
codegen-units = 256  # Maximum parallelism

# Fast CI builds
[profile.ci]
inherits = "release"
codegen-units = 16   # Balance compile time vs runtime
lto = "thin"         # Faster than "fat"

# Production release
[profile.production]
inherits = "release"
codegen-units = 1
lto = "fat"
```

## When to Use What

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Use What illustration -->
```rust
// codegen-units = 16 (default)
// - Development builds
// - CI where compile time matters
// - When runtime performance isn't critical

// codegen-units = 1
// - Production deployments
// - Performance-critical applications
// - Final releases
// - Benchmarking
```

## Measuring Impact

```bash
# Build with different settings
cargo build --release

# Benchmark
cargo bench

# Compare binary sizes
ls -lh target/release/my_binary

# Profile runtime
perf stat ./target/release/my_binary
```

## Related Rules
- [opt-lto-release](./opt-lto-release.md) - Link-time optimization
- [opt-pgo-profile](./opt-pgo-profile.md) - Profile-guided optimization
- [opt-target-cpu](./opt-target-cpu.md) - CPU-specific optimization
