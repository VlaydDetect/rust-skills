# own-copy-small

> Implement `Copy` for small, simple types## Decision

Consider this rule only after its prerequisites are satisfied: Implement `Copy` for small, simple types.

## Apply When

Apply when ownership, borrowing, lifetime, pointer, mutation, or drop semantics control correctness, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when independent ownership is required, or the proposed borrowing shape would leak a guard or lifetime into unrelated callers. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Draw the owner/borrower/drop graph and choose the least complex ownership topology that enforces it.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Less cloning can increase lifetime coupling; shared ownership and interior mutability add runtime and liveness costs.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.

## Verification

Compile the affected paths and test moves, early returns, mutation, and drop or cancellation behavior that the rule changes.

## Why It Matters

Types that implement `Copy` are implicitly duplicated on assignment instead of moved. This eliminates the need for explicit `.clone()` calls and makes the code more ergonomic. For small types (generally ≤16 bytes), copying is as fast or faster than moving a pointer.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Small type without Copy - requires explicit clone
#[derive(Clone, Debug)]
struct Point {
    x: f64,
    y: f64,
}

fn distance(p1: Point, p2: Point) -> f64 {
    ((p2.x - p1.x).powi(2) + (p2.y - p1.y).powi(2)).sqrt()
}

let origin = Point { x: 0.0, y: 0.0 };
let target = Point { x: 3.0, y: 4.0 };

let d1 = distance(origin.clone(), target.clone()); // Tedious
let d2 = distance(origin.clone(), target.clone()); // Every use needs clone
// origin and target still usable but verbose
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Small type with Copy - implicit duplication
#[derive(Clone, Copy, Debug)]
struct Point {
    x: f64,
    y: f64,
}

fn distance(p1: Point, p2: Point) -> f64 {
    ((p2.x - p1.x).powi(2) + (p2.y - p1.y).powi(2)).sqrt()
}

let origin = Point { x: 0.0, y: 0.0 };
let target = Point { x: 3.0, y: 4.0 };

let d1 = distance(origin, target); // Implicitly copied
let d2 = distance(origin, target); // Still works!
// origin and target remain valid
```

## Copy Requirements

A type can implement `Copy` only if:
1. All fields implement `Copy`
2. No custom `Drop` implementation
3. No heap-allocated data (`String`, `Vec`, `Box`, etc.)

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Copy Requirements illustration -->
```rust
// ✅ Can be Copy
#[derive(Clone, Copy)]
struct Color {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}

// ❌ Cannot be Copy - contains String
#[derive(Clone)]
struct Person {
    name: String,  // String is not Copy
    age: u32,
}

// ❌ Cannot be Copy - has Drop
struct FileHandle {
    fd: i32,
}
impl Drop for FileHandle {
    fn drop(&mut self) { /* close file */ }
}
```

## Size Guidelines

| Size | Recommendation |
|------|----------------|
| ≤ 16 bytes | Implement `Copy` |
| 17-64 bytes | Consider `Copy`, benchmark if critical |
| > 64 bytes | Probably don't, prefer references |

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Size Guidelines illustration -->
```rust
use std::mem::size_of;

#[derive(Clone, Copy)]
struct SmallId(u64); // 8 bytes ✅

#[derive(Clone, Copy)]
struct Rect { x: f32, y: f32, w: f32, h: f32 } // 16 bytes ✅

#[derive(Clone)] // No Copy - 72 bytes
struct Transform {
    matrix: [[f64; 3]; 3], // 72 bytes, too large
}
```

## Common Copy Types

Standard library types that are `Copy`:
- All primitives: `i32`, `f64`, `bool`, `char`, etc.
- Shared references: `&T` (note: `&mut T` is NOT `Copy` — copying a mutable reference would alias it, so it is reborrowed instead)
- Raw pointers: `*const T`, `*mut T`
- Function pointers: `fn(T) -> U`
- Tuples of `Copy` types: `(i32, f64)`
- Arrays of `Copy` types: `[u8; 32]`
- `Option<T>` where `T: Copy`
- `PhantomData<T>`

## Related Rules
- [own-clone-explicit](./own-clone-explicit.md) - When Clone without Copy is appropriate
- [type-newtype-ids](./type-newtype-ids.md) - Newtype pattern often uses Copy
