# err-thiserror-lib

> Use `thiserror` for library error types## Decision

Consider this rule only after its prerequisites are satisfied: Use `thiserror` for library error types.

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
- External crates referenced by the source (`anyhow`, `thiserror`) must already be accepted by the project or be approved before addition.

## Verification

Test important variants, source chains, display or redaction, negative recovery, and documented panic behavior.

## Why It Matters

Libraries should expose typed, matchable errors so users can handle specific error conditions. `thiserror` generates `Error` trait implementations with minimal boilerplate, creating ergonomic error types that are easy to match against.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// String errors - not matchable
fn parse(input: &str) -> Result<Data, String> {
    Err("parse error".to_string())
}

// Box<dyn Error> - not matchable
fn load(path: &Path) -> Result<Data, Box<dyn std::error::Error>> {
    Err(Box::new(std::io::Error::new(std::io::ErrorKind::NotFound, "file not found")))
}

// Manual implementation - verbose
#[derive(Debug)]
enum MyError {
    Io(std::io::Error),
    Parse(String),
}

impl std::fmt::Display for MyError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            MyError::Io(e) => write!(f, "io error: {}", e),
            MyError::Parse(s) => write!(f, "parse error: {}", s),
        }
    }
}

impl std::error::Error for MyError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            MyError::Io(e) => Some(e),
            MyError::Parse(_) => None,
        }
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ParseError {
    #[error("invalid syntax at line {line}: {message}")]
    Syntax { line: usize, message: String },
    
    #[error("unexpected end of file")]
    UnexpectedEof,
    
    #[error("invalid utf-8 encoding")]
    Utf8(#[from] std::str::Utf8Error),
    
    #[error("io error reading input")]
    Io(#[from] std::io::Error),
}

// Usage
fn parse(input: &str) -> Result<Ast, ParseError> {
    if input.is_empty() {
        return Err(ParseError::UnexpectedEof);
    }
    // ...
}

// Users can match specific errors
match parse(input) {
    Ok(ast) => process(ast),
    Err(ParseError::Syntax { line, message }) => {
        eprintln!("Syntax error on line {}: {}", line, message);
    }
    Err(ParseError::UnexpectedEof) => {
        eprintln!("File ended unexpectedly");
    }
    Err(e) => eprintln!("Error: {}", e),
}
```

## Key Attributes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Key Attributes illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum MyError {
    // Simple message
    #[error("operation failed")]
    Failed,
    
    // Interpolated fields
    #[error("invalid value: {0}")]
    InvalidValue(String),
    
    // Named fields
    #[error("connection to {host}:{port} failed")]
    Connection { host: String, port: u16 },
    
    // Automatic From impl with #[from]
    #[error("database error")]
    Database(#[from] sqlx::Error),
    
    // Source without From (manual conversion needed)
    #[error("validation failed")]
    Validation {
        #[source]
        cause: ValidationError,
        field: String,
    },
    
    // Transparent - delegates Display and source to inner
    #[error(transparent)]
    Other(#[from] anyhow::Error),
}
```

## Error Chaining

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Error Chaining illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("failed to read config file")]
    Read(#[source] std::io::Error),
    
    #[error("failed to parse config")]
    Parse(#[source] toml::de::Error),
    
    #[error("invalid config value for '{key}'")]
    InvalidValue {
        key: String,
        #[source]
        cause: ValueError,
    },
}

// Error chain is preserved
fn load_config(path: &Path) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(ConfigError::Read)?;
    
    let config: Config = toml::from_str(&content)
        .map_err(ConfigError::Parse)?;
    
    Ok(config)
}
```

## Library vs Application

| Context | Crate | Why |
|---------|-------|-----|
| Library | `thiserror` | Typed errors users can match |
| Application | `anyhow` | Easy error handling with context |
| Both | `thiserror` for public API, `anyhow` internally | Best of both |

## Related Rules
- [err-anyhow-app](err-anyhow-app.md) - Use anyhow for applications
- [err-from-impl](err-from-impl.md) - Use #[from] for automatic conversion
- [err-source-chain](err-source-chain.md) - Use #[source] to chain errors

## Verified Rulebook Example

<!-- rust-example: fixture; dependencies: thiserror -->
```rust
#[derive(Debug, thiserror::Error)]
enum LoadError {
    #[error("missing configuration")]
    Missing,
}

fn main() {
    assert_eq!(LoadError::Missing.to_string(), "missing configuration");
}
```
