# perf-iter-over-index

> Prefer iterators over manual indexing

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-stdlib`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Prefer iterators over manual indexing.

## Apply When

Apply when a controlled benchmark or profile identifies the operation and the proposed pattern preserves the correctness contract, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the change is based on source aesthetics, a synthetic non-representative workload, or an unapproved faster-but-weaker primitive. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Define metric and baseline, locate the bottleneck, test one pattern, compare repeated samples, and reject noise-level wins.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Lower runtime cost may increase code, dependency, memory, security, build-time, determinism, or maintenance cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`rayon`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Record exact workload, toolchain, target, features, profile, environment, before/after distributions, and functional equivalence.

## Why It Matters

Iterators are the idiomatic way to traverse collections in Rust. They enable bounds check elimination, SIMD auto-vectorization, and cleaner code. Manual indexing (`for i in 0..len`) often prevents these optimizations and introduces off-by-one error risks.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Manual indexing - bounds checked every iteration
fn sum_squares(data: &[i32]) -> i64 {
    let mut sum = 0i64;
    for i in 0..data.len() {
        sum += (data[i] as i64) * (data[i] as i64);
    }
    sum
}

// Index-based iteration with multiple collections
fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    let mut sum = 0.0;
    for i in 0..a.len().min(b.len()) {
        sum += a[i] * b[i];
    }
    sum
}

// Mutating with indices
fn double_values(data: &mut [i32]) {
    for i in 0..data.len() {
        data[i] *= 2;
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Iterator - bounds checks eliminated, SIMD-friendly
fn sum_squares(data: &[i32]) -> i64 {
    data.iter()
        .map(|&x| (x as i64) * (x as i64))
        .sum()
}

// Zip iterators - no manual length handling
fn dot_product(a: &[f64], b: &[f64]) -> f64 {
    a.iter()
        .zip(b.iter())
        .map(|(&x, &y)| x * y)
        .sum()
}

// Mutable iteration
fn double_values(data: &mut [i32]) {
    for x in data.iter_mut() {
        *x *= 2;
    }
}
```

## When Indexing Is Needed

Sometimes you genuinely need indices:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When Indexing Is Needed illustration -->
```rust
// Need the index for output or processing
for (i, value) in data.iter().enumerate() {
    println!("Index {}: {}", i, value);
}

// Non-sequential access patterns
fn interleave(data: &mut [i32]) {
    let mid = data.len() / 2;
    for i in 0..mid {
        data.swap(i * 2, mid + i);
    }
}
```

## Performance Comparison

| Pattern | Bounds Checks | SIMD Potential | Clarity |
|---------|---------------|----------------|---------|
| `for i in 0..len` | Every access | Limited | Medium |
| `for &x in slice` | None | High | High |
| `.iter().enumerate()` | None | Medium | High |
| `get_unchecked` | None (unsafe) | High | Low |

## Iterator Advantages

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Iterator Advantages illustration -->
```rust
// Chaining operations - single pass
let result: Vec<_> = data.iter()
    .filter(|x| **x > 0)
    .map(|x| x * 2)
    .collect();

// Early termination optimized
let found = data.iter().any(|&x| x == target);

// Parallel iteration (with rayon)
use rayon::prelude::*;
let sum: i64 = data.par_iter().map(|&x| x as i64).sum();
```

## Related Rules
- [perf-iter-lazy](./perf-iter-lazy.md) - Keep iterators lazy
- [opt-bounds-check](./opt-bounds-check.md) - Bounds check elimination
- [anti-index-over-iter](./anti-index-over-iter.md) - Anti-pattern
- [conc-rayon-par-iter](./conc-rayon-par-iter.md) - Parallelize data-parallel loops
