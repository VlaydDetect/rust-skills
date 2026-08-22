# anti-over-abstraction

> Don't over-abstract with excessive generics

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-idioms; supporters=none; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Don't over-abstract with excessive generics.

## Apply When

Apply when the named anti-pattern exists in a real path and obscures ownership, errors, iteration, abstraction, or measured performance, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the alleged smell is required by the contract or the replacement would add more complexity or alter behavior. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Locate the concrete impact, route to the canonical positive rule when one exists, and make the smallest semantics-preserving correction.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Removing a smell can simplify code, but mechanical rewrites can change ownership, allocation, ordering, errors, or readability.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.

## Verification

Compile and test the affected behavior; add performance evidence only when the finding is performance-specific.

## Why It Matters

Generics and traits are powerful but come at a cost: compile times, binary size, and cognitive load. Over-abstraction—making everything generic "for flexibility"—often adds complexity without benefit. Start concrete; generalize when you have real use cases.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Overly generic for a simple function
fn add<T, U, R>(a: T, b: U) -> R
where
    T: Into<R>,
    U: Into<R>,
    R: std::ops::Add<Output = R>,
{
    a.into() + b.into()
}

// Just call add(1, 2) - why make it this complex?

// Trait explosion
trait Readable {}
trait Writable {}
trait ReadWritable: Readable + Writable {}
trait AsyncReadable {}
trait AsyncWritable {}
trait AsyncReadWritable: AsyncReadable + AsyncWritable {}

// Abstract factory pattern (Java flashback)
trait Factory<T> {
    fn create(&self) -> T;
}
trait FactoryFactory<F: Factory<T>, T> {
    fn create_factory(&self) -> F;
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Concrete implementation - clear and simple
fn add_i32(a: i32, b: i32) -> i32 {
    a + b
}

// Generic when actually needed (e.g., library code)
fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}

// Simple traits for actual polymorphism needs
trait Storage {
    fn save(&self, key: &str, value: &[u8]) -> Result<(), Error>;
    fn load(&self, key: &str) -> Result<Vec<u8>, Error>;
}

// Concrete types first
struct FileStorage { path: PathBuf }
struct MemoryStorage { data: HashMap<String, Vec<u8>> }
```

## Signs of Over-Abstraction

| Sign | Symptom |
|------|---------|
| Single implementation | Generic trait with only one impl |
| Type parameter soup | `T, U, V, W` everywhere |
| Marker traits | Traits with no methods |
| Deep trait bounds | `where T: A + B + C + D + E` |
| Phantom generics | Type parameters not used meaningfully |

## When to Generalize

Generalize when:
- You have 2+ concrete types that share behavior
- You're writing library code for public consumption
- Performance requires static dispatch
- The abstraction simplifies the API

Don't generalize when:
- You "might need it later" (YAGNI)
- Only one type will ever implement it
- It makes code harder to understand

## Rule of Three

Wait until you have three similar concrete implementations before abstracting:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Rule of Three illustration -->
```rust
// Version 1: Just FileStorage
struct FileStorage { /* ... */ }

// Version 2: Added MemoryStorage, similar interface
struct MemoryStorage { /* ... */ }

// Version 3: Now Redis too - time to abstract
trait Storage {
    fn save(&self, key: &str, value: &[u8]) -> Result<()>;
    fn load(&self, key: &str) -> Result<Vec<u8>>;
}
```

## Prefer Concrete Types in Private Code

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Prefer Concrete Types in Private Code illustration -->
```rust
// Internal function - concrete type is fine
fn process_orders(db: &PostgresDb, orders: Vec<Order>) { }

// Public API - might benefit from abstraction
pub fn process_orders<S: Storage>(storage: &S, orders: Vec<Order>) { }
```

## Related Rules
- [type-generic-bounds](./type-generic-bounds.md) - Minimal bounds
- [api-sealed-trait](./api-sealed-trait.md) - Controlled extension
- [anti-type-erasure](./anti-type-erasure.md) - When Box<dyn> is wrong
