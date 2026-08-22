# perf-iter-lazy

> Keep iterators lazy, collect only when needed

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-stdlib`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Keep iterators lazy, collect only when needed.

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

Rust iterators are lazy—they compute values on demand. This enables single-pass processing, avoids intermediate allocations, and allows short-circuiting. Calling `.collect()` too early forces evaluation and allocates unnecessarily.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Collects intermediate results unnecessarily
fn process(data: Vec<i32>) -> Vec<i32> {
    let filtered: Vec<_> = data.into_iter()
        .filter(|x| *x > 0)
        .collect();  // Unnecessary allocation
    
    let mapped: Vec<_> = filtered.into_iter()
        .map(|x| x * 2)
        .collect();  // Another unnecessary allocation
    
    mapped.into_iter()
        .take(10)
        .collect()
}

// Collects before checking existence
fn has_positive(data: &[i32]) -> bool {
    let positives: Vec<_> = data.iter()
        .filter(|&&x| x > 0)
        .collect();  // Allocates entire filtered result
    
    !positives.is_empty()
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Single chain, single collect
fn process(data: Vec<i32>) -> Vec<i32> {
    data.into_iter()
        .filter(|x| *x > 0)
        .map(|x| x * 2)
        .take(10)
        .collect()
}

// Short-circuits on first match
fn has_positive(data: &[i32]) -> bool {
    data.iter().any(|&x| x > 0)
}
```

## Lazy Iterator Methods

These methods return iterators (lazy):

| Method | Description |
|--------|-------------|
| `.filter()` | Keep matching elements |
| `.map()` | Transform elements |
| `.take(n)` | Limit to n elements |
| `.skip(n)` | Skip first n elements |
| `.zip()` | Pair with another iterator |
| `.chain()` | Concatenate iterators |
| `.flat_map()` | Map and flatten |
| `.enumerate()` | Add index |

## Consuming Methods

These methods consume the iterator (evaluate immediately):

| Method | Description |
|--------|-------------|
| `.collect()` | Gather into collection |
| `.for_each()` | Execute side effect |
| `.count()` | Count elements |
| `.sum()` | Sum elements |
| `.fold()` | Accumulate value |
| `.any()` | Check if any match |
| `.all()` | Check if all match |
| `.find()` | Find first match |

## Short-Circuit Benefits

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Short-Circuit Benefits illustration -->
```rust
// Without lazy: processes ALL items
let found: Vec<_> = items.iter()
    .filter(|x| expensive_check(x))
    .collect();
let result = found.first();

// With lazy: stops at first match
let result = items.iter()
    .find(|x| expensive_check(x));
```

## Pattern: Process Without Collecting

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Process Without Collecting illustration -->
```rust
// Print all matches without allocating
data.iter()
    .filter(|x| x.is_valid())
    .for_each(|x| println!("{}", x));

// Count without collecting
let count = data.iter()
    .filter(|x| x.is_valid())
    .count();

// Sum without intermediate collection
let total: i64 = data.iter()
    .filter(|x| x.is_valid())
    .map(|x| x.value as i64)
    .sum();
```

## Related Rules
- [perf-collect-once](./perf-collect-once.md) - Single collect
- [perf-iter-over-index](./perf-iter-over-index.md) - Prefer iterators
- [anti-collect-intermediate](./anti-collect-intermediate.md) - Anti-pattern
