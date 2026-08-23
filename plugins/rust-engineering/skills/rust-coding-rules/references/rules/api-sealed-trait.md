# api-sealed-trait

> Use sealed traits to prevent external implementations while allowing use## Decision

Consider this rule only after its prerequisites are satisfied: Use sealed traits to prevent external implementations while allowing use.

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

Public traits can be implemented by anyone, which may be undesirable when you need to guarantee behavior or add methods in future versions. A sealed trait can be used by external code but not implemented by it, giving you control over implementations while maintaining a usable API.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Anyone can implement this trait
pub trait DatabaseDriver {
    fn connect(&self, url: &str) -> Connection;
    fn execute(&self, query: &str) -> Result<Rows, Error>;
}

// External crate implements it incorrectly
impl DatabaseDriver for MyBadDriver {
    fn connect(&self, url: &str) -> Connection {
        // Buggy implementation that doesn't handle errors
        unsafe { force_connect(url) }
    }
}

// Later, you want to add a required method - BREAKING CHANGE
pub trait DatabaseDriver {
    fn connect(&self, url: &str) -> Connection;
    fn execute(&self, query: &str) -> Result<Rows, Error>;
    fn transaction(&self) -> Transaction;  // External impls now broken!
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Create a private module with a private trait
mod private {
    pub trait Sealed {}
}

// Public trait requires the private trait
pub trait DatabaseDriver: private::Sealed {
    fn connect(&self, url: &str) -> Connection;
    fn execute(&self, query: &str) -> Result<Rows, Error>;
}

// Only your crate can implement Sealed, thus DatabaseDriver
pub struct PostgresDriver;
impl private::Sealed for PostgresDriver {}
impl DatabaseDriver for PostgresDriver {
    fn connect(&self, url: &str) -> Connection { ... }
    fn execute(&self, query: &str) -> Result<Rows, Error> { ... }
}

pub struct MySqlDriver;
impl private::Sealed for MySqlDriver {}
impl DatabaseDriver for MySqlDriver {
    fn connect(&self, url: &str) -> Connection { ... }
    fn execute(&self, query: &str) -> Result<Rows, Error> { ... }
}

// External crate cannot implement - private::Sealed is not accessible
// impl DatabaseDriver for ExternalDriver { }  // Error!

// But external code CAN use the trait
fn use_driver(driver: &impl DatabaseDriver) {
    let conn = driver.connect("postgres://localhost");
}
```

## Full Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Full Pattern illustration -->
```rust
pub mod db {
    mod private {
        pub trait Sealed {}
    }
    
    /// Database driver trait.
    /// 
    /// This trait is sealed and cannot be implemented outside this crate.
    pub trait Driver: private::Sealed {
        /// Connects to the database.
        fn connect(&self, url: &str) -> Result<Connection, Error>;
        
        /// Executes a query.
        fn execute(&self, sql: &str) -> Result<Rows, Error>;
    }
    
    pub struct Postgres;
    impl private::Sealed for Postgres {}
    impl Driver for Postgres { ... }
    
    pub struct Sqlite;
    impl private::Sealed for Sqlite {}
    impl Driver for Sqlite { ... }
}

// Usage works fine
use db::{Driver, Postgres};

fn query(driver: &impl Driver) {
    driver.execute("SELECT 1")?;
}

query(&Postgres);
```

## Benefits of Sealing

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Benefits of Sealing illustration -->
```rust
// 1. Add methods without breaking changes
pub trait Format: private::Sealed {
    fn format(&self) -> String;
    
    // Added later - not breaking because no external impls exist
    fn format_pretty(&self) -> String {
        self.format()  // Default implementation
    }
}

// 2. Guarantee invariants
pub trait SafeBuffer: private::Sealed {
    // You control all implementations, so you know they're all correct
    fn get(&self, index: usize) -> Option<&u8>;
}

// 3. Use as marker traits
pub trait ValidConfig: private::Sealed {}
// Only validated configs implement this
```

## Partially Sealed

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Partially Sealed illustration -->
```rust
// Allow implementing some methods but not all
mod private {
    pub trait SealedCore {}
}

pub trait Plugin: private::SealedCore {
    // Sealed - only we implement
    fn initialize(&self);
    fn shutdown(&self);
    
    // Open - users can override
    fn name(&self) -> &str { "unnamed" }
}

// Only we can add new required sealed methods
// Users can customize open methods
```

## When to Seal

| Seal When | Don't Seal When |
|-----------|-----------------|
| API stability is critical | You want extension points |
| Implementation correctness is hard | Users need custom implementations |
| You'll add methods later | Trait is simple and stable |
| Safety invariants required | Standard patterns (Iterator, etc.) |

## Related Rules
- [api-non-exhaustive](./api-non-exhaustive.md) - Related pattern for enums/structs
- [api-extension-trait](./api-extension-trait.md) - Adding methods to external types
- [api-typestate](./api-typestate.md) - Compile-time state guarantees
