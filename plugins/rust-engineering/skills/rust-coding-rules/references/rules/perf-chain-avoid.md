# perf-chain-avoid

> Avoid chain in hot loops## Decision

Consider this rule only after its prerequisites are satisfied: Avoid chain in hot loops.

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
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Record exact workload, toolchain, target, features, profile, environment, before/after distributions, and functional equivalence.

## Why It Matters

`Iterator::chain()` adds overhead for checking which iterator is active on every `.next()` call. In hot loops, this branch prediction overhead can impact performance. For performance-critical code, prefer single iterators or pre-combined collections.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Chain in hot inner loop
fn process_hot_path(a: &[i32], b: &[i32]) -> i64 {
    let mut sum = 0i64;
    
    // Called millions of times
    for _ in 0..1_000_000 {
        for x in a.iter().chain(b.iter()) {  // Branch every iteration
            sum += *x as i64;
        }
    }
    sum
}

// Chaining multiple small slices in tight loop
fn combine_results(parts: &[&[u8]]) -> Vec<u8> {
    let mut result = Vec::new();
    for part in parts {
        for byte in std::iter::once(&0u8).chain(part.iter()) {
            result.push(*byte);
        }
    }
    result
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Separate loops - branch-free inner loops
fn process_hot_path(a: &[i32], b: &[i32]) -> i64 {
    let mut sum = 0i64;
    
    for _ in 0..1_000_000 {
        for x in a {
            sum += *x as i64;
        }
        for x in b {
            sum += *x as i64;
        }
    }
    sum
}

// Pre-combine outside hot loop
fn combine_results(parts: &[&[u8]]) -> Vec<u8> {
    let mut result = Vec::new();
    for part in parts {
        result.push(0u8);
        result.extend_from_slice(part);
    }
    result
}
```

## When Chain Is Fine

Chain is perfectly acceptable when:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When Chain Is Fine illustration -->
```rust
// One-time iteration, not in hot path
fn collect_all(a: Vec<i32>, b: Vec<i32>) -> Vec<i32> {
    a.into_iter().chain(b).collect()
}

// Lazy evaluation with short-circuit
fn find_in_either(a: &[Item], b: &[Item], target: i32) -> Option<&Item> {
    a.iter().chain(b.iter()).find(|x| x.id == target)
}

// Small number of elements
fn get_prefixes() -> impl Iterator<Item = &'static str> {
    ["Mr.", "Mrs.", "Dr."].iter().copied()
        .chain(["Prof."].iter().copied())
}
```

## Alternative Patterns

### Pre-allocate and Extend

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pre-allocate and Extend illustration -->
```rust
fn merge_slices(slices: &[&[i32]]) -> Vec<i32> {
    let total: usize = slices.iter().map(|s| s.len()).sum();
    let mut result = Vec::with_capacity(total);
    for slice in slices {
        result.extend_from_slice(slice);
    }
    result
}
```

### Use append for Vecs

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Use append for Vecs illustration -->
```rust
fn combine_vecs(mut a: Vec<i32>, mut b: Vec<i32>) -> Vec<i32> {
    a.append(&mut b);  // Moves elements, no reallocation if a has capacity
    a
}
```

### Flatten Instead of Chain

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Flatten Instead of Chain illustration -->
```rust
// Instead of: a.iter().chain(b.iter()).chain(c.iter())
let all = [a, b, c];
for item in all.iter().flat_map(|slice| slice.iter()) {
    process(item);
}
```

## Performance Impact

| Pattern | Per-Item Overhead |
|---------|-------------------|
| Single iterator | None |
| `chain(a, b)` | 1 branch per item |
| `chain(a, b, c)` | 2 branches per item |
| Nested chains | Compounds |
| Separate loops | None (but code duplication) |

## Related Rules
- [perf-iter-over-index](./perf-iter-over-index.md) - Prefer iterators
- [perf-extend-batch](./perf-extend-batch.md) - Batch insertions
- [opt-cache-friendly](./opt-cache-friendly.md) - Cache-friendly patterns
