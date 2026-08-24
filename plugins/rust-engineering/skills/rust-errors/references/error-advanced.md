# Specialized Rust Error Advanced Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-errors`.
- Supporting profiles when needed: `$rust-api-design`, `$rust-architecture`.
- Scope retained: Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- Baseline correction: Do not leak foreign dependency errors through stable public APIs, and do not erase domain distinctions merely to standardize on one error crate.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Result vs Option vs panic

| Type | When to use | Example |
|-----|---------|-----|
| `Result<T, E>` | An operation is expected to fail | File reads, network requests |
| `Option<T>` | Absence is normal | Lookups, values that may be empty |
| `panic!` | A bug or invariant violation | Program logic errors, unrecoverable errors |
| `unreachable!()` | Code that should be impossible to reach | Exhaustive matching |


## Error-Handling Decision

```
Is failure expected?
    │
    ├─ Yes → Is this library code?
    │   ├─ Yes → thiserror (typed errors)
    │   └─ No → anyhow (ease of use)
    │
    ├─ No → Is absence normal?
    │   └─ Option<T>
    │
    └─ No → Bug or invariant violation
        └─ panic!, assert!
```


## thiserror (Library Code)<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    #[error("validation failed: {0}")]
    Validation(String),

    #[error("IO error: {source}")]
    Io {
        #[from]
        source: std::io::Error,
    },

    #[error("not found: {entity}:{id}")]
    NotFound {
        entity: String,
        id: u64,
    },
}

// Propagate with ?
fn read_config() -> Result<Config, MyError> {
    let content = std::fs::read_to_string("config.toml")?;
    Ok(toml::from_str(&content)?)
}
```


## anyhow (Application Code)<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use anyhow::{Context, Result, bail};

fn process_user(id: u64) -> Result<User> {
    let user = db.find_user(id)
        .with_context(|| format!("failed to find user {}", id))?;

    if !user.is_active {
        bail!("user {} is not active", id);
    }

    Ok(user)
}

// Combine multiple error sources
fn complex_operation() -> Result<()> {
    let a = operation_a().context("operation A failed")?;
    let b = operation_b().context("operation B failed")?;
    Ok(())
}
```


## Error-Design Principles

| Scenario | Recommendation |
|-----|------|
| Library code | thiserror and precise error types |
| Application code | anyhow for easy propagation and added context |
| Errors from library dependencies | Forward third-party errors with `#[from]` |
| Error codes are required | Enum variants |
| An error chain is required | `context()` + `with_context()` |


## Common Anti-Patterns

| Anti-pattern | Problem | Solution |
|-------|------|-----|
| `unwrap()` everywhere | Panics in a library | Use `?` |
| `Box<dyn Error>` | Loses type information | Use thiserror variants |
| Lost context | Difficult debugging | Use `.context()` |
| Too many error variants | Over-engineering | Simplify or merge them |


## When to Use panic<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 1. Invariant validation (public API)
pub fn divide(a: f64, b: f64) -> f64 {
    if b == 0.0 {
        panic!("division by zero");  // Public API: ensure callers do not pass 0
    }
    a / b
}

// 2. Unrecoverable error
fn start_engine() {
    let config = load_critical_config();
    if config.is_corrupted() {
        panic!("cannot start without valid config");
    }
}

// 3. Exhaustive matching (theoretically unreachable)
fn process_status(status: Status) {
    match status {
        Status::Running => { /* ... */ }
        Status::Stopped => { /* ... */ }
        // A new state may be added in the future
        // _ => unreachable!("unknown status: {:?}", status),
    }
}

// 4. Internal invariant
assert!(!queue.is_empty(), "queue should never be empty here");
```


## Error Chains<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Convert an error with map_err
fn high_level() -> Result<()> {
    low_level()
        .map_err(|e| MyError::from_low_level(e, "high level operation failed"))
}

// Add call-chain information with with_context
fn middle_layer() -> Result<()> {
    low_level()
        .with_context(|| format!("while processing request {}", request_id))?;
    Ok(())
}
```


## Best Practices

1. **Library code**: use precise error types with thiserror.
2. **Application code**: prioritize ease of use with anyhow.
3. **Propagating errors**: use `?` instead of `unwrap()`.
4. **Adding context**: use `.context()` or `with_context()`.
5. **Preserving error sources**: use `#[from]` to retain the underlying error.
6. **Distinguishing panic cases**: use panic for bugs and Result for expected failures.
