# err-question-mark

> Use `?` operator for clean propagation

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-errors; supporters=`rust-api-design`, `rust-observability`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `?` operator for clean propagation.

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

The `?` operator is Rust's idiomatic way to propagate errors. It's concise, readable, and automatically converts between compatible error types using `From`. It replaces verbose `match` or `unwrap()` calls.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Verbose match-based error handling
fn load_config() -> Result<Config, Error> {
    let content = match std::fs::read_to_string("config.toml") {
        Ok(c) => c,
        Err(e) => return Err(Error::Io(e)),
    };
    
    let config = match toml::from_str(&content) {
        Ok(c) => c,
        Err(e) => return Err(Error::Parse(e)),
    };
    
    Ok(config)
}

// Or worse - using unwrap
fn load_config_bad() -> Config {
    let content = std::fs::read_to_string("config.toml").unwrap();
    toml::from_str(&content).unwrap()
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
fn load_config() -> Result<Config, Error> {
    let content = std::fs::read_to_string("config.toml")?;
    let config = toml::from_str(&content)?;
    Ok(config)
}

// Even more concise
fn load_config() -> Result<Config, Error> {
    Ok(toml::from_str(&std::fs::read_to_string("config.toml")?)?)
}
```

## How ? Works

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the How ? Works illustration -->
```rust
// This:
let x = expr?;

// Expands roughly to:
let x = match expr {
    Ok(val) => val,
    Err(err) => return Err(From::from(err)),
};
```

## Combining with Context

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Combining with Context illustration -->
```rust
use anyhow::{Context, Result};

fn load_user(id: u64) -> Result<User> {
    let path = format!("users/{}.json", id);
    
    let content = std::fs::read_to_string(&path)
        .with_context(|| format!("failed to read user file: {}", path))?;
    
    let user: User = serde_json::from_str(&content)
        .context("failed to parse user JSON")?;
    
    Ok(user)
}
```

## ? with Option

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the ? with Option illustration -->
```rust
fn get_first_word(text: &str) -> Option<&str> {
    let first_line = text.lines().next()?;
    let first_word = first_line.split_whitespace().next()?;
    Some(first_word)
}

// Convert Option to Result
fn get_required_config(key: &str) -> Result<String, Error> {
    config.get(key)
        .cloned()
        .ok_or_else(|| Error::MissingConfig(key.to_string()))
}
```

## Error Type Conversion

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Error Type Conversion illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum MyError {
    #[error("io error")]
    Io(#[from] std::io::Error),  // Auto From impl
    
    #[error("parse error")]
    Parse(#[from] serde_json::Error),  // Auto From impl
}

fn process() -> Result<(), MyError> {
    // ? automatically converts io::Error to MyError via From
    let content = std::fs::read_to_string("file.txt")?;
    
    // ? automatically converts serde_json::Error to MyError
    let data: Data = serde_json::from_str(&content)?;
    
    Ok(())
}
```

## In main()

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the In main() illustration -->
```rust
// Option 1: Return Result from main
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = load_config()?;
    run_app(config)?;
    Ok(())
}

// Option 2: Handle in main, exit on error
fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {:#}", e);
        std::process::exit(1);
    }
}

fn run() -> anyhow::Result<()> {
    let config = load_config()?;
    run_app(config)?;
    Ok(())
}
```

## Related Rules
- [err-context-chain](err-context-chain.md) - Add context with .context()
- [err-from-impl](err-from-impl.md) - Use #[from] for automatic conversion
- [err-anyhow-app](err-anyhow-app.md) - Use anyhow for applications
