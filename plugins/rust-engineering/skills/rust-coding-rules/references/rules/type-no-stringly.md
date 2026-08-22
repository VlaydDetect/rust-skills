# type-no-stringly

> Avoid stringly-typed APIs; use enums, newtypes, or validated types

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-traits; supporters=`rust-api-design`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Avoid stringly-typed APIs; use enums, newtypes, or validated types.

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
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Use compile-pass, compile-fail, and runtime boundary cases to prove valid construction and rejection paths.

## Why It Matters

Strings accept any value—typos, wrong formats, invalid data all compile fine. Enums, newtypes, and validated types catch errors at compile time or construction time, not runtime. They also provide better IDE support, documentation, and make invalid states unrepresentable.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Status as string - easy to get wrong
fn set_status(status: &str) {
    match status {
        "pending" => { ... }
        "active" => { ... }
        "completed" => { ... }
        _ => panic!("Unknown status"),  // Runtime error
    }
}

// Easy to misuse
set_status("pending");   // OK
set_status("Pending");   // Runtime error - wrong case
set_status("aktive");    // Runtime error - typo
set_status("done");      // Runtime error - wrong word

// Configuration as strings
fn configure(key: &str, value: &str) {
    // No type safety, no validation
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Status as enum - compile-time safety
enum Status {
    Pending,
    Active,
    Completed,
}

fn set_status(status: Status) {
    match status {
        Status::Pending => { ... }
        Status::Active => { ... }
        Status::Completed => { ... }
    }  // Exhaustive - compiler checks all cases
}

// Can only pass valid values
set_status(Status::Pending);  // OK
set_status(Status::Aktivev);  // Compile error - typo caught!

// Configuration with typed builder
struct Config {
    timeout: Duration,
    retries: u32,
    mode: Mode,
}

enum Mode { Fast, Safe, Balanced }
```

## Parsing at Boundaries

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Parsing at Boundaries illustration -->
```rust
use std::str::FromStr;

#[derive(Debug, Clone, Copy)]
enum Priority {
    Low,
    Medium,
    High,
}

impl FromStr for Priority {
    type Err = ParseError;
    
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "low" => Ok(Priority::Low),
            "medium" | "med" => Ok(Priority::Medium),
            "high" => Ok(Priority::High),
            _ => Err(ParseError::UnknownPriority(s.to_string())),
        }
    }
}

// Parse once at boundary
fn handle_request(priority_str: &str) -> Result<(), Error> {
    let priority: Priority = priority_str.parse()?;
    // From here, priority is type-safe
    process(priority);
    Ok(())
}
```

## Validated Newtypes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Validated Newtypes illustration -->
```rust
// Instead of string for email
struct Email(String);

impl Email {
    fn new(s: &str) -> Result<Self, ValidationError> {
        if is_valid_email(s) {
            Ok(Email(s.to_string()))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
}

// Instead of string for UUID
struct UserId(uuid::Uuid);

// Instead of string for paths
struct ConfigPath(PathBuf);
```

## With Serde

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With Serde illustration -->
```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
enum EventType {
    UserCreated,
    UserDeleted,
    UserUpdated,
}

// JSON: {"type": "user_created", ...}
// Automatically validated during deserialization
```

## Related Rules
- [anti-stringly-typed](./anti-stringly-typed.md) - Anti-pattern details
- [type-newtype-validated](./type-newtype-validated.md) - Validated newtypes
- [type-enum-states](./type-enum-states.md) - Enums for states
