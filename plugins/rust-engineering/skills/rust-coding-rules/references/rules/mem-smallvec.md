# mem-smallvec

> Use `SmallVec` for usually-small collections

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-ownership`, `rust-stdlib`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `SmallVec` for usually-small collections.

## Apply When

Apply when a measured allocation, footprint, locality, move, or layout cost is material on the representative workload, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when there is no profile or size evidence, or the change would complicate ownership, portability, or correctness for a noise-level gain. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Measure allocation or layout first, change one representation or reuse decision, and compare the same workload.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`smallvec`, `arrayvec`, `thin-vec`, `bytes`, `tinyvec`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

`SmallVec<[T; N]>` stores up to N elements inline (on the stack), only allocating on the heap when the size exceeds N. This eliminates heap allocations for the common case while still allowing growth when needed.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Always heap-allocates, even for 1-2 elements
fn get_path_components(path: &str) -> Vec<&str> {
    path.split('/').collect()  // Usually 2-4 components
}

// Always heap-allocates for error list
fn validate(input: &Input) -> Vec<ValidationError> {
    let mut errors = Vec::new();  // Usually 0-3 errors
    // validation logic...
    errors
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use smallvec::{smallvec, SmallVec};

// Stack-allocated for typical paths (1-8 components)
fn get_path_components(path: &str) -> SmallVec<[&str; 8]> {
    path.split('/').collect()
}

// Stack-allocated for typical error counts
fn validate(input: &Input) -> SmallVec<[ValidationError; 4]> {
    let mut errors = SmallVec::new();
    // validation logic...
    errors
}

// Using smallvec! macro
let v: SmallVec<[i32; 4]> = smallvec![1, 2, 3];
```

## Choosing Capacity N

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Choosing Capacity N illustration -->
```rust
// Measure your actual data distribution!
// Guidelines:

// Path components: 4-8 (most paths are shallow)
type PathParts<'a> = SmallVec<[&'a str; 8]>;

// Function arguments: 4-8 (most functions have few args)  
type Args = SmallVec<[Arg; 8]>;

// AST children: 2-4 (binary ops, if/else, etc.)
type Children = SmallVec<[Node; 4]>;

// Error accumulation: 2-4 (most inputs have few errors)
type Errors = SmallVec<[Error; 4]>;

// Attribute lists: 4-8 (most items have few attributes)
type Attrs = SmallVec<[Attribute; 8]>;
```

## Evidence from rust-analyzer

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Evidence from rust-analyzer illustration -->
```rust
// https://github.com/rust-lang/rust/blob/main/compiler/rustc_expand/src/base.rs
macro_rules! make_stmts_default {
    ($me:expr) => {
        $me.make_expr().map(|e| {
            smallvec![ast::Stmt {
                id: ast::DUMMY_NODE_ID,
                span: e.span,
                kind: ast::StmtKind::Expr(e),
            }]
        })
    }
}
```

## Trade-offs

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Trade-offs illustration -->
```rust
// SmallVec is slightly larger than Vec
use std::mem::size_of;
// Vec<i32>: 24 bytes (ptr + len + cap)
// SmallVec<[i32; 4]>: 32 bytes (inline storage + len + discriminant)

// SmallVec has branching overhead on every operation
// (must check if inline or heap)

// Profile to verify benefit!
```

## When to Use SmallVec vs Alternatives

| Situation | Use |
|-----------|-----|
| Usually small, sometimes large | `SmallVec<[T; N]>` |
| Always small, fixed max | `ArrayVec<T, N>` |
| Rarely grows past initial | `Vec::with_capacity` |
| No `unsafe` allowed | `TinyVec` |
| Often empty | `ThinVec` |

## ArrayVec Alternative

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the ArrayVec Alternative illustration -->
```rust
use arrayvec::ArrayVec;

// Fixed maximum capacity, never heap allocates
// Panics if you exceed capacity
fn parse_rgb(s: &str) -> ArrayVec<u8, 3> {
    let mut components = ArrayVec::new();
    for part in s.split(',').take(3) {
        components.push(part.parse().unwrap());
    }
    components
}
```

## TinyVec (No Unsafe)

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the TinyVec (No Unsafe) illustration -->
```rust
use tinyvec::{tiny_vec, TinyVec};

// Same concept as SmallVec but 100% safe code
let v: TinyVec<[i32; 4]> = tiny_vec![1, 2, 3];
```

## Related Rules
- [mem-arrayvec](mem-arrayvec.md) - Use ArrayVec for fixed-max collections
- [mem-with-capacity](mem-with-capacity.md) - Pre-allocate when size is known
- [mem-thinvec](mem-thinvec.md) - Use ThinVec for often-empty vectors

## Verified Rulebook Example

<!-- rust-example: fixture; dependencies: smallvec -->
```rust
use smallvec::SmallVec;

fn main() {
    let values: SmallVec<[u8; 4]> = [1, 2, 3].into_iter().collect();
    assert!(!values.spilled());
}
```
