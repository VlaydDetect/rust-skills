# perf-extend-batch

> Use extend for batch insertions## Decision

Consider this rule only after its prerequisites are satisfied: Use extend for batch insertions.

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

`extend()` can pre-allocate capacity for the incoming elements and insert them in a single operation. Individual `push()` calls may trigger multiple reallocations as the collection grows. For adding multiple elements, `extend()` is both faster and clearer.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Multiple potential reallocations
fn collect_results(sources: Vec<Source>) -> Vec<Result> {
    let mut results = Vec::new();
    
    for source in sources {
        for result in source.get_results() {
            results.push(result);  // May reallocate
        }
    }
    results
}

// Loop with push for known data
fn build_list() -> Vec<i32> {
    let mut list = Vec::new();
    for i in 0..1000 {
        list.push(i);  // Many reallocations
    }
    list
}

// Appending another collection
fn combine(mut a: Vec<i32>, b: Vec<i32>) -> Vec<i32> {
    for item in b {
        a.push(item);
    }
    a
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Single extend with size hint
fn collect_results(sources: Vec<Source>) -> Vec<Result> {
    let mut results = Vec::new();
    
    for source in sources {
        results.extend(source.get_results());
    }
    results
}

// Direct collection from iterator
fn build_list() -> Vec<i32> {
    (0..1000).collect()
}

// Extend for combining
fn combine(mut a: Vec<i32>, b: Vec<i32>) -> Vec<i32> {
    a.extend(b);
    a
}
```

## Extend with Capacity

For best performance, combine with `reserve()`:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Extend with Capacity illustration -->
```rust
fn merge_all(chunks: Vec<Vec<Item>>) -> Vec<Item> {
    // Calculate total size
    let total: usize = chunks.iter().map(|c| c.len()).sum();
    
    let mut result = Vec::with_capacity(total);
    for chunk in chunks {
        result.extend(chunk);
    }
    result
}
```

## Extend Methods

| Method | Description |
|--------|-------------|
| `.extend(iter)` | Add all elements from iterator |
| `.extend_from_slice(&[T])` | Add from slice (for `Copy` types) |
| `.append(&mut Vec)` | Move all from another Vec |

## Pattern: Building Strings

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Building Strings illustration -->
```rust
// Bad: multiple allocations
fn build_message(parts: &[&str]) -> String {
    let mut result = String::new();
    for part in parts {
        result.push_str(part);  // May reallocate
    }
    result
}

// Good: extend with known parts
fn build_message(parts: &[&str]) -> String {
    let total_len: usize = parts.iter().map(|s| s.len()).sum();
    let mut result = String::with_capacity(total_len);
    for part in parts {
        result.push_str(part);
    }
    result
}

// Better: collect/join
fn build_message(parts: &[&str]) -> String {
    parts.concat()  // or parts.join("")
}
```

## HashMap/HashSet Extend

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the HashMap/HashSet Extend illustration -->
```rust
use std::collections::HashMap;

// Extend from iterator of tuples
fn merge_maps(mut base: HashMap<String, i32>, other: HashMap<String, i32>) -> HashMap<String, i32> {
    base.extend(other);  // Moves entries from other
    base
}

// Extend from iterator
let mut set = HashSet::new();
set.extend(items.iter().map(|i| i.id));
```

## Performance

| Operation | Allocations | Complexity |
|-----------|-------------|------------|
| N × `push()` | O(log N) | O(N) amortized |
| `extend(iter)` | O(1)* | O(N) |
| `with_capacity` + `extend` | 1 | O(N) |

*When iterator provides accurate `size_hint()`

## Related Rules
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocation
- [perf-drain-reuse](./perf-drain-reuse.md) - Reusing allocations
- [mem-reuse-collections](./mem-reuse-collections.md) - Collection reuse
