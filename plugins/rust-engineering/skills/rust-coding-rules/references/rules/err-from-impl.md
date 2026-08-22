# err-from-impl

> Implement `From<E>` for error conversions to enable `?` operator

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-errors; supporters=`rust-api-design`, `rust-observability`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Implement `From<E>` for error conversions to enable `?` operator.

## Apply When

Apply when the caller-visible failure taxonomy, propagation, recovery, context, or panic policy is being decided, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the failure is an internal invariant violation, or erasure would remove a caller action that the boundary promises. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map each failure to a caller action, then preserve sources and add context only at the boundary that owns the operation.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Typed errors preserve decisions but expand compatibility surface; erased reports compose easily but reduce programmatic matching.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde_json`, `anyhow`, `thiserror`) must already be accepted by the project or be approved before addition.

## Verification

Test important variants, source chains, display or redaction, negative recovery, and documented panic behavior.

## Why It Matters

The `?` operator automatically converts errors using `From` trait. By implementing `From<SourceError> for YourError`, you enable seamless error propagation without explicit `.map_err()` calls. This makes error handling code cleaner and ensures consistent error wrapping throughout your codebase.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(serde_json::Error),
    Database(diesel::result::Error),
}

fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| AppError::Io(e))?;  // Manual conversion everywhere
    
    let config: Config = serde_json::from_str(&content)
        .map_err(|e| AppError::Parse(e))?;  // Repeated boilerplate
    
    save_to_db(&config)
        .map_err(|e| AppError::Database(e))?;  // Gets tedious
    
    Ok(config)
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[derive(Debug)]
enum AppError {
    Io(std::io::Error),
    Parse(serde_json::Error),
    Database(diesel::result::Error),
}

// Implement From for each source error type
impl From<std::io::Error> for AppError {
    fn from(err: std::io::Error) -> Self {
        AppError::Io(err)
    }
}

impl From<serde_json::Error> for AppError {
    fn from(err: serde_json::Error) -> Self {
        AppError::Parse(err)
    }
}

impl From<diesel::result::Error> for AppError {
    fn from(err: diesel::result::Error) -> Self {
        AppError::Database(err)
    }
}

fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)?;  // Auto-converts
    let config: Config = serde_json::from_str(&content)?;  // Clean!
    save_to_db(&config)?;
    Ok(config)
}
```

## Use thiserror for Automatic From

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Use thiserror for Automatic From illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),  // Auto-generates From impl
    
    #[error("Parse error: {0}")]
    Parse(#[from] serde_json::Error),  // #[from] does the work
    
    #[error("Database error: {0}")]
    Database(#[from] diesel::result::Error),
}

// Now ? just works
fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)?;
    let config: Config = serde_json::from_str(&content)?;
    save_to_db(&config)?;
    Ok(config)
}
```

## From with Context

Sometimes you need to add context during conversion:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the From with Context illustration -->
```rust
#[derive(Error, Debug)]
enum ConfigError {
    #[error("Failed to read config from '{path}': {source}")]
    ReadFailed {
        path: String,
        #[source]
        source: std::io::Error,
    },
}

// Can't use #[from] when you need extra context
fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|source| ConfigError::ReadFailed {
            path: path.to_string(),
            source,
        })?;
    // ...
}

// Or use anyhow for ad-hoc context
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read config from '{}'", path))?;
    // ...
}
```

## Blanket From Implementations

Be careful with blanket implementations:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Blanket From Implementations illustration -->
```rust
// ❌ Too broad - conflicts with other From impls
impl<E: std::error::Error> From<E> for AppError {
    fn from(err: E) -> Self {
        AppError::Other(err.to_string())
    }
}

// ✅ Specific implementations
impl From<std::io::Error> for AppError { ... }
impl From<ParseIntError> for AppError { ... }
```

## Related Rules
- [err-thiserror-lib](./err-thiserror-lib.md) - Using thiserror for libraries
- [err-source-chain](./err-source-chain.md) - Preserving error chains
- [err-question-mark](./err-question-mark.md) - The ? operator
- [conv-tryfrom-fallible](./conv-tryfrom-fallible.md) - TryFrom for fallible conversions
