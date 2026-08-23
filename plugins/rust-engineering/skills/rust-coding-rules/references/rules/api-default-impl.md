# api-default-impl

> Implement `Default` for types with sensible default values## Decision

Use this context-sensitive Rust decision when its premise is established: Implement `Default` for types with sensible default values.

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

`Default` is a standard trait that provides a canonical way to create a default instance. It integrates with many ecosystem patterns: `Option::unwrap_or_default()`, `#[derive(Default)]`, struct update syntax `..Default::default()`, and generic code that requires `T: Default`. Implementing it makes your types more ergonomic.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct Config {
    timeout: Duration,
    retries: u32,
    verbose: bool,
}

impl Config {
    // Custom constructor - works but non-standard
    fn new() -> Self {
        Config {
            timeout: Duration::from_secs(30),
            retries: 3,
            verbose: false,
        }
    }
}

// Can't use with standard patterns
let config: Config = Default::default();  // Error: Default not implemented
let timeout = settings.get("timeout").unwrap_or_default();  // Won't work
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::time::Duration;

// Simple case: derive uses each field type's Default (Duration::ZERO, 0, false)
#[derive(Default)]
struct Config {
    timeout: Duration,
    retries: u32,
    verbose: bool,
}
```

For a non-zero default, implement `Default` by hand instead of deriving. (Per-field defaults like `timeout: Duration = Duration::from_secs(30)` require the nightly `default_field_values` feature.)

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::time::Duration;

struct Config {
    timeout: Duration,
    retries: u32,
    verbose: bool,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            timeout: Duration::from_secs(30),
            retries: 3,
            verbose: false,
        }
    }
}

// Now works with all standard patterns
let config = Config::default();
let config = Config { retries: 5, ..Default::default() };
let value = map.get("key").cloned().unwrap_or_default();
```

## Derive vs Manual

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Derive vs Manual illustration -->
```rust
// Derive: all fields use their own Default
#[derive(Default)]
struct Simple {
    count: u32,      // 0
    name: String,    // ""
    items: Vec<i32>, // []
}

// Manual: when you need custom defaults
struct Connection {
    host: String,
    port: u16,
    timeout: Duration,
}

impl Default for Connection {
    fn default() -> Self {
        Connection {
            host: "localhost".to_string(),
            port: 8080,
            timeout: Duration::from_secs(30),
        }
    }
}
```

## Builder with Default

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Builder with Default illustration -->
```rust
#[derive(Default)]
struct ServerBuilder {
    host: String,
    port: u16,
    workers: usize,
}

impl ServerBuilder {
    fn host(mut self, host: impl Into<String>) -> Self {
        self.host = host.into();
        self
    }
    
    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }
}

// Clean initialization
let server = ServerBuilder::default()
    .host("0.0.0.0")
    .port(3000)
    .build();
```

## Default with Required Fields

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Default with Required Fields illustration -->
```rust
// When some fields have no sensible default, don't implement Default
struct User {
    id: UserId,       // No sensible default
    name: String,     // Could default to ""
}

// Instead, provide a constructor
impl User {
    fn new(id: UserId, name: impl Into<String>) -> Self {
        User { id, name: name.into() }
    }
}

// Or use builder with required fields
struct UserBuilder {
    id: Option<UserId>,
    name: String,
}

impl Default for UserBuilder {
    fn default() -> Self {
        UserBuilder {
            id: None,
            name: String::new(),
        }
    }
}
```

## Generic Default

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Generic Default illustration -->
```rust
// Require Default in generic bounds when needed
fn create_or_default<T: Default>(opt: Option<T>) -> T {
    opt.unwrap_or_default()
}

// PhantomData is Default regardless of T
use std::marker::PhantomData;
struct Wrapper<T> {
    _marker: PhantomData<T>,
}

impl<T> Default for Wrapper<T> {
    fn default() -> Self {
        Wrapper { _marker: PhantomData }
    }
}
```

## Related Rules
- [api-builder-pattern](./api-builder-pattern.md) - Building complex types
- [api-common-traits](./api-common-traits.md) - Other common traits to implement
- [api-from-not-into](./api-from-not-into.md) - Conversion traits
