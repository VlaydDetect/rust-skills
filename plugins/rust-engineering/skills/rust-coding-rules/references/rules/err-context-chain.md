# err-context-chain

> Add context with `.context()` or `.with_context()`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-errors; supporters=`rust-api-design`, `rust-observability`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Add context with `.context()` or `.with_context()`.

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

Raw errors often lack information about what operation failed. Adding context creates an error chain that tells the full story: what you were trying to do, and why it failed.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Raw error - no context
fn load_user(id: u64) -> Result<User, Error> {
    let path = format!("users/{}.json", id);
    let content = std::fs::read_to_string(&path)?;
    Ok(serde_json::from_str(&content)?)
}

// Error message: "No such file or directory (os error 2)"
// Which file? What were we doing?
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use anyhow::{Context, Result};

fn load_user(id: u64) -> Result<User> {
    let path = format!("users/{}.json", id);
    
    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read user file: {}", path))?;
    
    let user: User = serde_json::from_str(&content)
        .with_context(|| format!("failed to parse user {} JSON", id))?;
    
    Ok(user)
}

// Error: "failed to parse user 42 JSON"
// Caused by: "expected ':' at line 5 column 12"
```

## context() vs with_context()

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the context() vs withcontext() illustration -->
```rust
// context() - static string (slight allocation)
fs::read_to_string(path)
    .context("failed to read config")?;

// with_context() - lazy evaluation (only allocates on error)
fs::read_to_string(path)
    .with_context(|| format!("failed to read {}", path))?;

// Use with_context() when:
// - Message includes runtime data (format!)
// - Computing the message is expensive
// - Error path is cold (most of the time)
```

## Building Context Chains

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Building Context Chains illustration -->
```rust
fn process_order(order_id: u64) -> Result<()> {
    let order = fetch_order(order_id)
        .with_context(|| format!("failed to fetch order {}", order_id))?;
    
    let user = load_user(order.user_id)
        .with_context(|| format!("failed to load user for order {}", order_id))?;
    
    let payment = process_payment(&order, &user)
        .context("payment processing failed")?;
    
    ship_order(&order, &payment)
        .context("shipping failed")?;
    
    Ok(())
}

// Full error chain:
// "shipping failed"
// Caused by: "carrier API returned 503"
// Caused by: "connection refused"
```

## Displaying Error Chains

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Displaying Error Chains illustration -->
```rust
fn main() {
    if let Err(e) = run() {
        // Just top-level message
        eprintln!("Error: {}", e);
        
        // Full chain with alternate format
        eprintln!("Error: {:#}", e);
        
        // Debug format (includes backtrace if enabled)
        eprintln!("Error: {:?}", e);
        
        // Iterate through chain
        for (i, cause) in e.chain().enumerate() {
            eprintln!("  {}: {}", i, cause);
        }
    }
}
```

## With thiserror

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With thiserror illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("failed to load config from {path}")]
    ConfigLoad {
        path: String,
        #[source]
        cause: std::io::Error,
    },
    
    #[error("failed to connect to database")]
    Database {
        #[source]
        cause: sqlx::Error,
    },
}

// Usage
fn load_config(path: &str) -> Result<Config, AppError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| AppError::ConfigLoad {
            path: path.to_string(),
            cause: e,
        })?;
    // ...
}
```

## Related Rules
- [err-anyhow-app](err-anyhow-app.md) - Use anyhow for applications
- [err-source-chain](err-source-chain.md) - Use #[source] to chain errors
- [err-question-mark](err-question-mark.md) - Use ? for propagation
