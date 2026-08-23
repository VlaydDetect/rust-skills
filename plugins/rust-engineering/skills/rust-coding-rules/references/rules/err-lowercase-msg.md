# err-lowercase-msg

> Start error messages lowercase, no trailing punctuation## Decision

Consider this rule only after its prerequisites are satisfied: Start error messages lowercase, no trailing punctuation.

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

Error messages are often chained, logged, or displayed with additional context. Consistent formatting—lowercase start, no trailing period—allows clean composition: "failed to load config: invalid JSON: unexpected token". Mixed case and punctuation create awkward output: "Failed to load config.: Invalid JSON.: Unexpected token.".

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("Failed to read config file.")]  // Capital F, trailing period
    ReadFailed(#[from] std::io::Error),
    
    #[error("Invalid JSON format!")]  // Capital I, exclamation
    ParseFailed(#[from] serde_json::Error),
    
    #[error("The requested key was not found")]  // Reads like a sentence
    KeyNotFound(String),
}

// Chained output: "Config load error: Failed to read config file.: No such file"
// Awkward capitalization and punctuation
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
enum ConfigError {
    #[error("failed to read config file")]  // lowercase, no period
    ReadFailed(#[from] std::io::Error),
    
    #[error("invalid JSON format")]  // lowercase, no period
    ParseFailed(#[from] serde_json::Error),
    
    #[error("key not found: {0}")]  // lowercase, data at end
    KeyNotFound(String),
}

// Chained output: "config load error: failed to read config file: no such file"
// Clean, consistent
```

## Rust Standard Library Convention

The standard library follows this convention:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Rust Standard Library Convention illustration -->
```rust
// std::io::Error messages
"entity not found"
"permission denied"
"connection refused"

// std::num::ParseIntError
"invalid digit found in string"

// std::str::Utf8Error  
"invalid utf-8 sequence"
```

## Formatting Guidelines

| Do | Don't |
|----|-------|
| `"failed to parse config"` | `"Failed to parse config."` |
| `"invalid input: expected number"` | `"Invalid input - expected a number!"` |
| `"connection timed out after {0}s"` | `"Connection Timed Out After {0} seconds."` |
| `"key '{0}' not found"` | `"Key Not Found: {0}"` |

## Context Addition Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Context Addition Pattern illustration -->
```rust
use anyhow::{Context, Result};

fn load_user(id: u64) -> Result<User> {
    let data = fetch(id)
        .with_context(|| format!("failed to fetch user {}", id))?;
    
    parse_user(data)
        .with_context(|| "failed to parse user data")?
}

// Output: "failed to fetch user 42: connection refused"
// All lowercase, clean chain
```

## Display vs Debug

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Display vs Debug illustration -->
```rust
#[derive(Error, Debug)]
#[error("invalid configuration")]  // Display: for users/logs
pub struct ConfigError {
    path: PathBuf,
    source: io::Error,
}

// Debug output (for developers) can have more detail
// Display output (for users) should be clean
```

## When to Use Capitals

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Use Capitals illustration -->
```rust
// Proper nouns / acronyms keep their case
#[error("invalid JSON syntax")]     // JSON is an acronym
#[error("OAuth token expired")]     // OAuth is a proper noun
#[error("HTTP request failed")]     // HTTP is an acronym

// Error codes can be uppercase
#[error("error code E0001: invalid input")]
```

## Related Rules
- [err-thiserror-lib](./err-thiserror-lib.md) - Error definition with thiserror
- [err-context-chain](./err-context-chain.md) - Adding context to errors
- [doc-examples-section](./doc-examples-section.md) - Documentation conventions
