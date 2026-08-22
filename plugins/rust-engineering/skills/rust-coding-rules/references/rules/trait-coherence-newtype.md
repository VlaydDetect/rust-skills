# trait-coherence-newtype

> Respect the orphan rule; wrap a foreign type in a newtype to implement a foreign trait on it

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Respect the orphan rule; wrap a foreign type in a newtype to implement a foreign trait on it.

## Apply When

Apply when real implementations or callers need a behavioral abstraction, extension point, dispatch choice, or coherence solution, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when one concrete implementation or a closed enum expresses the current contract more directly. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Identify the variation axis, choose static, dynamic, associated-type, generic, enum, or newtype representation, then check coherence.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Static dispatch enables optimization but grows code; dynamic dispatch erases types but adds allocation, lifetime, and object-safety constraints.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile representative implementations and rejection cases; inspect object safety, blanket impls, auto traits, and downstream rights.

## Why It Matters

Rust's coherence rules — enforced by the orphan rule — require that for any `impl Trait for Type`, either `Trait` or `Type` must be defined in the current crate. This prevents two crates from providing conflicting implementations for the same (trait, type) pair, which would make the compiler unable to pick one. When you need to implement a trait you didn't define (e.g., `std::fmt::Display`) on a type you didn't define (e.g., `Vec<i32>`), the compiler rejects the impl outright. The solution is to wrap the foreign type in a local newtype struct, then implement the foreign trait on the wrapper. Marking the wrapper `#[repr(transparent)]` keeps it zero-cost and allows safe pointer casts where needed.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::fmt;

// error[E0117]: only traits defined in the current crate can be implemented for
// types defined outside of the crate
// impl fmt::Display for Vec<i32> { ... }  // both `Display` and `Vec` are foreign
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::fmt;

// A local newtype wrapping the foreign type.
// `#[repr(transparent)]` guarantees the same memory layout as Vec<i32>.
#[repr(transparent)]
struct CommaSeparated(Vec<i32>);

impl CommaSeparated {
    pub fn new(v: Vec<i32>) -> Self { Self(v) }

    // Provide access to the inner value.
    pub fn into_inner(self) -> Vec<i32> { self.0 }
    pub fn inner(&self) -> &Vec<i32> { &self.0 }
}

// Now both the trait (Display) is foreign and the type (CommaSeparated) is local —
// the orphan rule is satisfied because CommaSeparated is defined here.
impl fmt::Display for CommaSeparated {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut iter = self.0.iter().peekable();
        while let Some(n) = iter.next() {
            write!(f, "{n}")?;
            if iter.peek().is_some() {
                write!(f, ", ")?;
            }
        }
        Ok(())
    }
}

// Implement From/Into so conversion is ergonomic.
impl From<Vec<i32>> for CommaSeparated {
    fn from(v: Vec<i32>) -> Self { Self(v) }
}

impl From<CommaSeparated> for Vec<i32> {
    fn from(w: CommaSeparated) -> Self { w.0 }
}

fn demo() {
    let nums = CommaSeparated::new(vec![1, 2, 3, 4, 5]);
    println!("{nums}");   // "1, 2, 3, 4, 5"

    // Round-trip through the inner type.
    let v: Vec<i32> = nums.into();
    let again = CommaSeparated::from(v);
    println!("{again}");
}
```

## Key Points

- The orphan rule: `impl<T> ForeignTrait for ForeignType<T>` is always rejected, even with a type parameter.
- `#[repr(transparent)]` is mandatory for newtypes that need the same ABI as the inner type (e.g., FFI, pointer casts via `transmute`). For purely logical wrapping, it is optional but good practice.
- Provide `From`/`Into` conversions and an `inner()` / `into_inner()` accessor so callers can move in and out of the wrapper easily.
- The newtype pattern is described in the Rust API Guidelines under "Newtypes provide static distinctions" (rust-lang.github.io/api-guidelines/).
- Newtype wrappers are also the correct way to add trait impls to types from transitive dependencies that you do not control.

## Related Rules
- [api-newtype-safety](api-newtype-safety.md) - use newtypes for type-safe distinctions
- [type-repr-transparent](type-repr-transparent.md) - use `#[repr(transparent)]` for FFI newtypes
- [trait-blanket-impl](trait-blanket-impl.md) - give behaviour to every type meeting a bound
- [api-from-not-into](api-from-not-into.md) - implement `From`, not `Into` (auto-derived)
