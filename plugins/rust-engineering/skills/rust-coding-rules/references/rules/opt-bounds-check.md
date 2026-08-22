# opt-bounds-check

> Use iterators and patterns that eliminate bounds checks in hot paths

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-cargo-build`, `rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use iterators and patterns that eliminate bounds checks in hot paths.

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

Rust's safety guarantees require bounds checking on array/slice indexing. In tight loops, these checks can cause measurable overhead (branch mispredictions, preventing vectorization). Patterns like iterators, `get_unchecked`, and index splitting can eliminate these checks while maintaining safety.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn sum_products(a: &[f64], b: &[f64]) -> f64 {
    let mut sum = 0.0;
    for i in 0..a.len() {
        sum += a[i] * b[i];  // Two bounds checks per iteration
    }
    sum
}

fn apply_filter(data: &mut [u8], kernel: &[u8; 3]) {
    for i in 1..data.len() - 1 {
        // Three bounds checks per iteration
        data[i] = (data[i - 1] + data[i] + data[i + 1]) / 3;
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn sum_products(a: &[f64], b: &[f64]) -> f64 {
    // Iterator zips - no bounds checks, vectorizes well
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

fn apply_filter(data: &mut [u8]) {
    // Windows pattern - no bounds checks
    for window in data.windows(3) {
        // window[0], window[1], window[2] are all valid
    }
    
    // Or use chunks
    for chunk in data.chunks_exact(4) {
        process_simd(chunk);
    }
}
```

## Iterator Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Iterator Patterns illustration -->
```rust
// These give the compiler much better opportunities to eliminate bounds checks
// (and often do in practice), but elimination is not guaranteed — verify hot
// code with generated assembly (e.g. cargo-show-asm):

// zip - parallel iteration
for (a, b) in xs.iter().zip(ys.iter()) { ... }

// enumerate - index + value  
for (i, x) in data.iter().enumerate() { ... }

// windows - sliding window
for window in data.windows(3) { ... }

// chunks - fixed-size groups
for chunk in data.chunks(4) { ... }
for chunk in data.chunks_exact(4) { ... }  // Guarantees exact size

// split_at - divide slice
let (left, right) = data.split_at(mid);
```

## Split for Parallel Access

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Split for Parallel Access illustration -->
```rust
fn parallel_sum(data: &[i32]) -> i32 {
    // Split into independent chunks
    let (left, right) = data.split_at(data.len() / 2);
    
    // Process chunks without bounds checks
    let sum_left: i32 = left.iter().sum();
    let sum_right: i32 = right.iter().sum();
    
    sum_left + sum_right
}
```

## get_unchecked for Proven Safety

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the getunchecked for Proven Safety illustration -->
```rust
fn matrix_multiply(a: &[f64], b: &[f64], c: &mut [f64], n: usize) {
    assert!(a.len() >= n * n);
    assert!(b.len() >= n * n);
    assert!(c.len() >= n * n);
    
    for i in 0..n {
        for j in 0..n {
            let mut sum = 0.0;
            for k in 0..n {
                // SAFETY: bounds verified by asserts above
                unsafe {
                    sum += a.get_unchecked(i * n + k) 
                         * b.get_unchecked(k * n + j);
                }
            }
            // SAFETY: bounds verified by asserts above
            unsafe {
                *c.get_unchecked_mut(i * n + j) = sum;
            }
        }
    }
}
```

## Slice Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Slice Patterns illustration -->
```rust
fn process_header(data: &[u8]) -> Option<Header> {
    // Slice pattern - single length check, no per-field checks
    let [a, b, c, d, rest @ ..] = data else {
        return None;
    };
    
    Some(Header {
        magic: *a,
        version: *b,
        flags: u16::from_le_bytes([*c, *d]),
        payload: rest,
    })
}
```

## Verify Bounds Check Elimination

```bash
# Check generated assembly
cargo asm --release my_crate::hot_function

# Look for 'cmp' and 'ja'/'jbe' instructions near array access
# If eliminated, you'll see direct memory access
```

## When to Accept Bounds Checks

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Accept Bounds Checks illustration -->
```rust
// Random access patterns - checks unavoidable
fn random_lookup(data: &[u8], indices: &[usize]) -> Vec<u8> {
    indices.iter()
        .filter_map(|&i| data.get(i).copied())  // Checked, but necessary
        .collect()
}

// Infrequent access - overhead negligible
fn get_config(&self, key: &str) -> Option<&Value> {
    self.config.get(key)  // Fine, not hot path
}
```

## Related Rules
- [opt-simd-portable](./opt-simd-portable.md) - SIMD requires unchecked access
- [opt-cache-friendly](./opt-cache-friendly.md) - Cache-efficient patterns
- [perf-profile-first](./perf-profile-first.md) - Identify actual hot paths
