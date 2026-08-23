# err-source-chain

> Preserve error chains with `#[source]` or `source()` method## Decision

Consider this rule only after its prerequisites are satisfied: Preserve error chains with `#[source]` or `source()` method.

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

Errors often have underlying causes. Preserving the error chain (via `source()` method) allows logging frameworks and error reporters to show the full context: "config parse failed → JSON syntax error at line 5 → unexpected token". Without chaining, you lose valuable debugging information.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[derive(Debug)]
enum ConfigError {
    ParseFailed(String),  // Lost the original serde_json::Error
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|e| ConfigError::ParseFailed(e.to_string()))?;  // Chain lost!
    
    serde_json::from_str(&content)
        .map_err(|e| ConfigError::ParseFailed(e.to_string()))?  // No source
}

// Error output: "Parse failed: invalid type: ..."
// Missing: which file? what line? what was the parent error?
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("Failed to read config file '{path}'")]
    ReadFailed {
        path: String,
        #[source]  // Preserves the error chain
        source: std::io::Error,
    },
    
    #[error("Failed to parse config file '{path}'")]
    ParseFailed {
        path: String,
        #[source]  // Original parse error preserved
        source: serde_json::Error,
    },
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(|source| ConfigError::ReadFailed {
            path: path.to_string(),
            source,  // Chain preserved
        })?;
    
    serde_json::from_str(&content)
        .map_err(|source| ConfigError::ParseFailed {
            path: path.to_string(),
            source,
        })
}
```

## Manual source() Implementation

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Manual source() Implementation illustration -->
```rust
use std::error::Error;

#[derive(Debug)]
struct MyError {
    message: String,
    source: Option<Box<dyn Error + Send + Sync>>,
}

impl std::fmt::Display for MyError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.message)
    }
}

impl Error for MyError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        self.source.as_ref().map(|e| e.as_ref() as &(dyn Error + 'static))
    }
}
```

## Walking the Error Chain

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Walking the Error Chain illustration -->
```rust
fn print_error_chain(error: &dyn std::error::Error) {
    eprintln!("Error: {}", error);
    
    let mut source = error.source();
    while let Some(err) = source {
        eprintln!("Caused by: {}", err);
        source = err.source();
    }
}

// With anyhow, use {:?} for full chain
let result: anyhow::Result<()> = do_something();
if let Err(e) = result {
    eprintln!("{:?}", e);  // Prints full chain with backtraces
}
```

## anyhow Context

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the anyhow Context illustration -->
```rust
use anyhow::{Context, Result};

fn load_config(path: &str) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Failed to read '{}'", path))?;
    
    let config: Config = serde_json::from_str(&content)
        .with_context(|| format!("Failed to parse '{}'", path))?;
    
    Ok(config)
}

// Output:
// Error: Failed to parse 'config.json'
// Caused by: expected `:` at line 5 column 10
```

## #[from] vs #[source]

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the #[from] vs #[source] illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum MyError {
    // #[from] = implements From + sets source
    #[error("IO error")]
    Io(#[from] std::io::Error),
    
    // #[source] = only sets source (no From impl)
    #[error("Parse error in file '{path}'")]
    Parse {
        path: String,
        #[source]
        source: serde_json::Error,
    },
}
```

## Related Rules
- [err-thiserror-lib](./err-thiserror-lib.md) - thiserror for error definitions
- [err-context-chain](./err-context-chain.md) - Adding context to errors
- [err-from-impl](./err-from-impl.md) - From implementations for ?
