# err-custom-type

> Define custom error types for domain-specific failures

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-errors; supporters=`rust-api-design`, `rust-observability`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Define custom error types for domain-specific failures.

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

Generic errors like `String`, `Box<dyn Error>`, or catch-all enums obscure what can actually go wrong. Custom error types document failure modes in the type system, enable pattern matching for specific handling, and provide clear API contracts. They make your code self-documenting and help callers handle errors appropriately.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Generic string errors - no structure
fn validate_user(user: &User) -> Result<(), String> {
    if user.name.is_empty() {
        return Err("Name is empty".to_string());
    }
    if user.age > 150 {
        return Err("Age is invalid".to_string());
    }
    Ok(())
}

// Caller can't match on specific errors
match validate_user(&user) {
    Ok(()) => save(user),
    Err(msg) => {
        // Can only do string comparison - fragile!
        if msg.contains("Name") {
            prompt_for_name()
        }
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ValidationError {
    #[error("name cannot be empty")]
    EmptyName,
    
    #[error("name exceeds maximum length of {max} characters")]
    NameTooLong { max: usize, actual: usize },
    
    #[error("invalid age {0}: must be between 0 and 150")]
    InvalidAge(u8),
    
    #[error("email format is invalid: {0}")]
    InvalidEmail(String),
}

fn validate_user(user: &User) -> Result<(), ValidationError> {
    if user.name.is_empty() {
        return Err(ValidationError::EmptyName);
    }
    if user.name.len() > 100 {
        return Err(ValidationError::NameTooLong { 
            max: 100, 
            actual: user.name.len() 
        });
    }
    if user.age > 150 {
        return Err(ValidationError::InvalidAge(user.age));
    }
    Ok(())
}

// Caller can match specifically
match validate_user(&user) {
    Ok(()) => save(user),
    Err(ValidationError::EmptyName) => prompt_for_name(),
    Err(ValidationError::InvalidAge(age)) => {
        show_error(&format!("Please enter a valid age (you entered {})", age))
    }
    Err(e) => show_error(&e.to_string()),
}
```

## Error Type Design Guidelines

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Error Type Design Guidelines illustration -->
```rust
// 1. Group related errors in domain-specific enums
#[derive(Error, Debug)]
pub enum AuthError {
    #[error("invalid credentials")]
    InvalidCredentials,
    #[error("account locked after {attempts} failed attempts")]
    AccountLocked { attempts: u32 },
    #[error("token expired")]
    TokenExpired,
}

#[derive(Error, Debug)]
pub enum PaymentError {
    #[error("insufficient funds: need {required}, have {available}")]
    InsufficientFunds { required: Decimal, available: Decimal },
    #[error("card declined: {reason}")]
    CardDeclined { reason: String },
}

// 2. Include relevant data for error handling/display
#[derive(Error, Debug)]
pub enum FileError {
    #[error("file not found: {path}")]
    NotFound { path: PathBuf },
    #[error("permission denied for {path}")]
    PermissionDenied { path: PathBuf },
}

// 3. Consider #[non_exhaustive] for public APIs
#[derive(Error, Debug)]
#[non_exhaustive]  // Allows adding variants without breaking changes
pub enum ApiError {
    #[error("rate limited")]
    RateLimited,
    #[error("not found")]
    NotFound,
}
```

## When to Use What

| Error Pattern | Use Case |
|---------------|----------|
| Custom enum | Library with specific failure modes |
| `thiserror` | Libraries needing `std::error::Error` |
| `anyhow::Error` | Applications, prototypes |
| Struct with source | Single error type with wrapped cause |

## Struct-Based Errors

For single error types with rich context:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Struct-Based Errors illustration -->
```rust
#[derive(Error, Debug)]
#[error("query failed for table '{table}' with filter '{filter}'")]
pub struct QueryError {
    pub table: String,
    pub filter: String,
    #[source]
    pub source: DatabaseError,
}
```

## Related Rules
- [err-thiserror-lib](./err-thiserror-lib.md) - thiserror for error definitions
- [err-anyhow-app](./err-anyhow-app.md) - When to use anyhow instead
- [api-non-exhaustive](./api-non-exhaustive.md) - Forward-compatible enums
