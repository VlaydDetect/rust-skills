# perf-collect-once

> Don't collect intermediate iterators

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-stdlib`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Don't collect intermediate iterators.

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

Each `.collect()` allocates a new collection. Chaining multiple operations with intermediate collections wastes memory and CPU cycles. Keep iterator chains lazy and collect only once at the end.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Three allocations, three passes
fn process_users(users: Vec<User>) -> Vec<String> {
    let active: Vec<_> = users.into_iter()
        .filter(|u| u.is_active)
        .collect();
    
    let verified: Vec<_> = active.into_iter()
        .filter(|u| u.is_verified)
        .collect();
    
    verified.into_iter()
        .map(|u| u.name)
        .collect()
}

// Collecting to count
fn count_valid(items: &[Item]) -> usize {
    items.iter()
        .filter(|i| i.is_valid())
        .collect::<Vec<_>>()  // Unnecessary!
        .len()
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// One allocation, one pass
fn process_users(users: Vec<User>) -> Vec<String> {
    users.into_iter()
        .filter(|u| u.is_active)
        .filter(|u| u.is_verified)
        .map(|u| u.name)
        .collect()
}

// No allocation needed
fn count_valid(items: &[Item]) -> usize {
    items.iter()
        .filter(|i| i.is_valid())
        .count()
}
```

## Pattern: Deferred Collection

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Deferred Collection illustration -->
```rust
// Create the iterator chain
fn prepare_data(raw: Vec<RawData>) -> impl Iterator<Item = ProcessedData> {
    raw.into_iter()
        .filter(|d| d.is_valid())
        .map(ProcessedData::from)
}

// Collect only when needed
let data: Vec<_> = prepare_data(input).collect();

// Or consume without collecting
prepare_data(input).for_each(|d| process(d));
```

## When Intermediate Collection Is Needed

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When Intermediate Collection Is Needed illustration -->
```rust
// Need to iterate multiple times
let items: Vec<_> = data.iter()
    .filter(|x| x.is_valid())
    .collect();

let count = items.len();
let first = items.first();
for item in &items {
    process(item);
}

// Need to sort (requires concrete collection)
let mut sorted: Vec<_> = data.iter()
    .filter(|x| x.is_active)
    .collect();
sorted.sort_by_key(|x| x.priority);
```

## Comparison

| Approach | Allocations | Passes | Memory |
|----------|-------------|--------|--------|
| Multiple `.collect()` | N | N | O(N × data) |
| Single chain + `.collect()` | 1 | 1 | O(data) |
| No `.collect()` (streaming) | 0 | 1 | O(1) |

## Pattern: Collect with Capacity

When you must collect, pre-allocate:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Collect with Capacity illustration -->
```rust
// With estimated capacity
let mut result = Vec::with_capacity(items.len());
result.extend(
    items.iter()
        .filter(|x| x.is_valid())
        .map(|x| x.clone())
);
```

## Related Rules
- [perf-iter-lazy](./perf-iter-lazy.md) - Keep iterators lazy
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocate collections
- [anti-collect-intermediate](./anti-collect-intermediate.md) - Anti-pattern
