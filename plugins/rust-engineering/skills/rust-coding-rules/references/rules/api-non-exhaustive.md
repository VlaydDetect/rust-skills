# api-non-exhaustive

> Use `#[non_exhaustive]` on public enums and structs for forward compatibility

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `#[non_exhaustive]` on public enums and structs for forward compatibility.

## Apply When

Apply when a public or independently evolving caller contract needs an ownership, construction, extension, or compatibility decision, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the abstraction has only one local use or would expose implementation and dependency details without caller value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write representative caller examples, minimize public surface, and review ownership, errors, extension rights, and compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More flexibility can improve call sites while increasing inference, monomorphization, compatibility, and maintenance obligations.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

Adding a variant to a public enum or a field to a public struct is normally a breaking change—downstream code may match exhaustively or use struct literal syntax. `#[non_exhaustive]` forces external code to use wildcards in matches and constructors, allowing you to add variants/fields in minor versions without breaking callers.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Public enum - adding variant breaks downstream matches
pub enum ErrorKind {
    NotFound,
    PermissionDenied,
    TimedOut,
}

// Downstream code
match error.kind() {
    ErrorKind::NotFound => ...,
    ErrorKind::PermissionDenied => ...,
    ErrorKind::TimedOut => ...,
    // No wildcard - will break when you add ErrorKind::Interrupted
}

// Public struct - adding field breaks downstream construction
pub struct Config {
    pub name: String,
    pub value: i32,
}

// Downstream code
let config = Config { name: "test".into(), value: 42 };
// Will break when you add `pub enabled: bool`
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Can add variants in minor versions
#[non_exhaustive]
pub enum ErrorKind {
    NotFound,
    PermissionDenied,
    TimedOut,
    // Future: can add Interrupted here without breaking changes
}

// Downstream code MUST have wildcard
match error.kind() {
    ErrorKind::NotFound => ...,
    ErrorKind::PermissionDenied => ...,
    ErrorKind::TimedOut => ...,
    _ => ...,  // Required by non_exhaustive
}

// Can add fields in minor versions
#[non_exhaustive]
pub struct Config {
    pub name: String,
    pub value: i32,
}

// Downstream CANNOT use struct literal syntax
// let config = Config { name: "test".into(), value: 42 };  // Error!

// Must use constructor
impl Config {
    pub fn new(name: impl Into<String>, value: i32) -> Self {
        Config { name: name.into(), value }
    }
}
```

## How It Works

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the How It Works illustration -->
```rust
#[non_exhaustive]
pub enum Status {
    Active,
    Inactive,
}

// Inside your crate: exhaustive match is allowed
fn internal(s: Status) {
    match s {
        Status::Active => {},
        Status::Inactive => {},
        // No wildcard needed inside defining crate
    }
}

// Outside your crate: wildcard required
fn external(s: my_crate::Status) {
    match s {
        my_crate::Status::Active => {},
        my_crate::Status::Inactive => {},
        _ => {},  // REQUIRED
    }
}
```

## Struct Usage

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Struct Usage illustration -->
```rust
#[non_exhaustive]
pub struct Point {
    pub x: f64,
    pub y: f64,
}

impl Point {
    // Provide constructor
    pub fn new(x: f64, y: f64) -> Self {
        Point { x, y }
    }
}

// External code can read fields but not construct with literals
fn external(p: Point) {
    println!("x: {}, y: {}", p.x, p.y);  // Reading is fine
    
    // let p2 = Point { x: 1.0, y: 2.0 };  // Error!
    let p2 = Point::new(1.0, 2.0);  // Must use constructor
}
```

## Non-Exhaustive Variants

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Non-Exhaustive Variants illustration -->
```rust
pub enum Message {
    // Specific variant is non-exhaustive
    #[non_exhaustive]
    Error { code: u32, message: String },
    
    Ok(Data),
}

// Can destructure Ok normally
// But Error requires `..` to handle future fields
match msg {
    Message::Ok(data) => {},
    Message::Error { code, message, .. } => {},  // `..` required
}
```

## When to Use

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Use illustration -->
```rust
// ✅ Use for public API types that may evolve
#[non_exhaustive]
pub enum ApiError { ... }

#[non_exhaustive]
pub struct Options { ... }

// ✅ Use for error types
#[non_exhaustive]
pub enum MyError { ... }

// ❌ Don't use for internal types
enum InternalState { ... }  // Not public, no concern

// ❌ Don't use for stable, complete types
pub enum Ordering {  // Less, Equal, Greater is complete
    Less,
    Equal,
    Greater,
}
```

## Related Rules
- [api-sealed-trait](./api-sealed-trait.md) - Controlling trait implementations
- [err-custom-type](./err-custom-type.md) - Error type design
- [api-builder-pattern](./api-builder-pattern.md) - Alternative to struct literals
