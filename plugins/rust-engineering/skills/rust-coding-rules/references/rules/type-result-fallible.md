# type-result-fallible

> Use `Result<T, E>` for operations that can fail

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `Result<T, E>` for operations that can fail.

## Apply When

Apply when a type can encode a real invariant, state, identity, representation, or output contract more reliably than convention, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the extra type machinery does not eliminate a meaningful invalid state or would make a local operation harder to use. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Name the invalid states, choose the smallest nominal or algebraic representation, and review construction and conversion boundaries.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Type-driven guarantees move failures earlier but can expand public surface, conversion code, generic complexity, and diagnostics.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde_json`, `thiserror`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Use compile-pass, compile-fail, and runtime boundary cases to prove valid construction and rejection paths.

## Why It Matters

`Result<T, E>` makes failure explicit in the type system. Callers must acknowledge and handle potential errors—they can't accidentally ignore failures. The `?` operator makes error propagation ergonomic while maintaining explicit error handling.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Returning Option loses error context
fn read_config(path: &str) -> Option<Config> {
    let content = std::fs::read_to_string(path).ok()?;  // Why did it fail?
    toml::from_str(&content).ok()  // Parse error lost
}

// Panicking on errors
fn read_config(path: &str) -> Config {
    let content = std::fs::read_to_string(path).unwrap();  // Crashes
    toml::from_str(&content).unwrap()  // Crashes
}

// Sentinel values
fn divide(a: i32, b: i32) -> i32 {
    if b == 0 { return -1; }  // Magic value, easy to miss
    a / b
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Result with clear error type
fn read_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)
        .map_err(ConfigError::IoError)?;
    toml::from_str(&content)
        .map_err(ConfigError::ParseError)
}

fn divide(a: i32, b: i32) -> Result<i32, DivisionError> {
    if b == 0 {
        return Err(DivisionError::DivideByZero);
    }
    Ok(a / b)
}

// Caller must handle
match divide(10, 0) {
    Ok(result) => println!("Result: {}", result),
    Err(e) => println!("Error: {}", e),
}
```

## The ? Operator

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the The ? Operator illustration -->
```rust
fn process_file(path: &str) -> Result<ProcessedData, Error> {
    let content = std::fs::read_to_string(path)?;  // Propagates Err
    let parsed: RawData = serde_json::from_str(&content)?;
    let validated = validate(parsed)?;
    let processed = transform(validated)?;
    Ok(processed)
}

// Equivalent to:
fn process_file(path: &str) -> Result<ProcessedData, Error> {
    let content = match std::fs::read_to_string(path) {
        Ok(c) => c,
        Err(e) => return Err(e.into()),
    };
    // ... etc
}
```

## Result Combinators

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Result Combinators illustration -->
```rust
let result: Result<i32, Error> = Ok(42);

// map: transform success value
let doubled = result.map(|n| n * 2);  // Ok(84)

// map_err: transform error
let with_context = result.map_err(|e| format!("Failed: {}", e));

// and_then: chain fallible operations
let processed = result.and_then(|n| {
    if n > 0 { Ok(n * 2) } else { Err(Error::Negative) }
});

// unwrap_or: provide default on error
let value = result.unwrap_or(0);

// ok(): convert to Option, discarding error
let maybe_value: Option<i32> = result.ok();
```

## Defining Error Types

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Defining Error Types illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("failed to read file: {0}")]
    Io(#[from] std::io::Error),
    
    #[error("failed to parse config: {0}")]
    Parse(#[from] toml::de::Error),
    
    #[error("missing required field: {0}")]
    MissingField(String),
}

fn load_config(path: &str) -> Result<Config, ConfigError> {
    let content = std::fs::read_to_string(path)?;  // Io error
    let config: Config = toml::from_str(&content)?;  // Parse error
    if config.name.is_empty() {
        return Err(ConfigError::MissingField("name".into()));
    }
    Ok(config)
}
```

## Related Rules
- [err-thiserror-lib](./err-thiserror-lib.md) - Defining error types
- [err-question-mark](./err-question-mark.md) - Using ? operator
- [type-option-nullable](./type-option-nullable.md) - Option vs Result
