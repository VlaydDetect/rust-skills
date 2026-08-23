# mem-thinvec

> Use `ThinVec<T>` for nullable collections with minimal overhead## Decision

Consider this rule only after its prerequisites are satisfied: Use `ThinVec<T>` for nullable collections with minimal overhead.

## Apply When

Apply when a measured allocation, footprint, locality, move, or layout cost is material on the representative workload, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when there is no profile or size evidence, or the change would complicate ownership, portability, or correctness for a noise-level gain. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Measure allocation or layout first, change one representation or reuse decision, and compare the same workload.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Inline storage, boxing, arenas, compact types, and reuse exchange simplicity, code size, stack use, locality, or dependency cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`smallvec`, `thin-vec`, `bytes`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

Standard `Vec<T>` is 24 bytes even when empty. `ThinVec` from Mozilla's `thin_vec` crate uses a single pointer (8 bytes), storing length and capacity inline with the heap allocation. For Option<Vec<T>> patterns or structs with many optional vecs, this significantly reduces memory overhead.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct TreeNode {
    value: i32,
    // Each node pays 24 bytes for children, even leaves
    children: Vec<TreeNode>,  // Most nodes are leaves with empty Vec
}

// Or using Option<Vec<T>>
struct SparseData {
    // Option<Vec> = 24 bytes (Vec is never null-pointer optimized)
    tags: Option<Vec<String>>,
    metadata: Option<Vec<Metadata>>,
    // 48 bytes for usually-None fields
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use thin_vec::ThinVec;

struct TreeNode {
    value: i32,
    // Empty ThinVec is just a null pointer - 8 bytes
    children: ThinVec<TreeNode>,
}

struct SparseData {
    // ThinVec empty = 8 bytes each
    tags: ThinVec<String>,
    metadata: ThinVec<Metadata>,
    // 16 bytes vs 48 bytes
}
```

## Memory Layout

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Memory Layout illustration -->
```rust
use std::mem::size_of;

// Standard Vec: always 24 bytes
assert_eq!(size_of::<Vec<u8>>(), 24);
assert_eq!(size_of::<Option<Vec<u8>>>(), 24);  // No NPO benefit

// ThinVec: 8 bytes (one pointer)
use thin_vec::ThinVec;
assert_eq!(size_of::<ThinVec<u8>>(), 8);
assert_eq!(size_of::<Option<ThinVec<u8>>>(), 8);  // Option is free!
```

## ThinVec vs Vec

| Feature | `Vec<T>` | `ThinVec<T>` |
|---------|----------|--------------|
| Size (empty) | 24 bytes | 8 bytes |
| Size (non-empty) | 24 bytes | 8 bytes (header on heap) |
| Option<T> optimization | No | Yes |
| Cache locality | Better (len/cap on stack) | Worse (len/cap on heap) |
| Iteration speed | Faster | Slightly slower |
| API compatibility | Full | Vec-like |

## When to Use ThinVec

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Use ThinVec illustration -->
```rust
// ✅ Good: Many instances, often empty
struct SparseGraph {
    nodes: Vec<Node>,
    // Most edges lists are empty or small
    edges: Vec<ThinVec<EdgeId>>,  // Saves 16 bytes per node
}

// ✅ Good: Nullable collection field
struct Document {
    content: String,
    attachments: ThinVec<Attachment>,  // Often empty
}

// ❌ Avoid: Hot loops, performance-critical iteration
fn process_hot_path(data: &ThinVec<Item>) {
    // Every length check goes through pointer indirection
    for item in data {  // Vec would be faster here
        process(item);
    }
}

// ❌ Avoid: Few instances
fn main() {
    let single_vec: ThinVec<i32> = ThinVec::new();
    // Saving 16 bytes once is meaningless
}
```

## API Compatibility

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the API Compatibility illustration -->
```rust
use thin_vec::{ThinVec, thin_vec};

// Constructor macro
let v: ThinVec<i32> = thin_vec![1, 2, 3];

// Familiar Vec-like API
let mut v = ThinVec::new();
v.push(1);
v.push(2);
v.extend([3, 4, 5]);
v.pop();

// Iteration
for item in &v {
    println!("{}", item);
}

// Slicing
let slice: &[i32] = &v[..];

// Conversion
let vec: Vec<i32> = v.into();
let thin: ThinVec<i32> = vec.into();
```

## Cargo.toml

```toml
[dependencies]
thin-vec = "0.2"
```

## Related Rules
- [mem-smallvec](./mem-smallvec.md) - Stack-allocated small vecs
- [mem-boxed-slice](./mem-boxed-slice.md) - Fixed-size heap slices
- [mem-with-capacity](./mem-with-capacity.md) - Pre-allocation strategies
