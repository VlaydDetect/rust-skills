# api-parse-dont-validate

> Parse into validated types at boundaries

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Parse into validated types at boundaries.

## Apply When

Apply when a public or independently evolving caller contract needs an ownership, construction, extension, or compatibility decision, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the abstraction has only one local use or would expose implementation and dependency details without caller value. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write representative caller examples, minimize public surface, and review ownership, errors, extension rights, and compatibility.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More flexibility can improve call sites while increasing inference, monomorphization, compatibility, and maintenance obligations.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Compile downstream-style examples and check docs, public paths, feature behavior, and the declared compatibility baseline.

## Why It Matters

Instead of validating data and hoping you remember to check everywhere, parse it into a type that can only be constructed from valid data. The type system then guarantees validity - you can't forget to validate because invalid states are unrepresentable.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Validation scattered throughout codebase
fn send_email(email: &str) -> Result<(), Error> {
    // Did someone validate this already? Who knows!
    if !is_valid_email(email) {
        return Err(Error::InvalidEmail);
    }
    // Send email...
}

fn add_to_mailing_list(email: &str) -> Result<(), Error> {
    // Duplicate validation, or did we forget?
    if !is_valid_email(email) {
        return Err(Error::InvalidEmail);
    }
    // Add to list...
}

// Easy to forget validation
fn process_user_email(email: &str) {
    // Oops, no validation!
    database.store_email(email);
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// A validated email address.
/// Can only be constructed via `Email::parse()`.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct Email(String);

impl Email {
    /// Parses and validates an email address.
    pub fn parse(s: impl Into<String>) -> Result<Self, EmailError> {
        let s = s.into();
        if Self::is_valid(&s) {
            Ok(Email(s))
        } else {
            Err(EmailError::Invalid)
        }
    }
    
    fn is_valid(s: &str) -> bool {
        s.contains('@') && s.len() > 3  // Simplified
    }
    
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Now functions can accept Email - guaranteed valid!
fn send_email(email: &Email) -> Result<(), Error> {
    // No validation needed - Email is always valid
    smtp_send(email.as_str())
}

fn add_to_mailing_list(email: Email) {
    // No validation needed
    list.push(email);
}
```

## More Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the More Examples illustration -->
```rust
// Port number (1-65535)
pub struct Port(u16);

impl Port {
    pub fn new(n: u16) -> Option<Self> {
        if n > 0 { Some(Port(n)) } else { None }
    }
    
    pub fn get(&self) -> u16 {
        self.0
    }
}

// Non-empty string
pub struct NonEmptyString(String);

impl NonEmptyString {
    pub fn new(s: impl Into<String>) -> Option<Self> {
        let s = s.into();
        if s.is_empty() { None } else { Some(Self(s)) }
    }
}

// Positive integer
pub struct PositiveI32(i32);

impl PositiveI32 {
    pub fn new(n: i32) -> Option<Self> {
        if n > 0 { Some(Self(n)) } else { None }
    }
}

// Bounded value
pub struct Percentage(u8);

impl Percentage {
    pub fn new(n: u8) -> Option<Self> {
        if n <= 100 { Some(Self(n)) } else { None }
    }
}
```

## Parsing at Boundaries

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Parsing at Boundaries illustration -->
```rust
// Parse at the system boundary (API, CLI, config file)
fn handle_request(raw: RawRequest) -> Result<Response, Error> {
    // Parse ALL inputs upfront
    let email = Email::parse(&raw.email)?;
    let age = Age::parse(raw.age)?;
    let username = Username::parse(&raw.username)?;
    
    // Now work with validated types
    process_user(email, age, username)
}

fn process_user(email: Email, age: Age, username: Username) {
    // All inputs guaranteed valid - no checks needed
}
```

## Evidence from sqlx

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Evidence from sqlx illustration -->
```rust
// sqlx parses SQL at compile time, ensuring query validity
// https://github.com/launchbadge/sqlx/blob/master/src/macros/mod.rs

// The query! macro parses and validates SQL
let user = sqlx::query!("SELECT * FROM users WHERE id = ?", id)
    .fetch_one(&pool)
    .await?;

// If SQL is invalid, compilation fails - invalid state unrepresentable
```

## Combining with Display

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Combining with Display illustration -->
```rust
use std::fmt;

pub struct Email(String);

impl Email {
    pub fn parse(s: &str) -> Result<Self, EmailError> { ... }
}

// Implement Display for easy printing
impl fmt::Display for Email {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.0)
    }
}

// Implement AsRef for easy borrowing
impl AsRef<str> for Email {
    fn as_ref(&self) -> &str {
        &self.0
    }
}
```

## Related Rules
- [api-newtype-safety](api-newtype-safety.md) - Use newtypes for type safety
- [type-newtype-validated](type-newtype-validated.md) - Newtypes for validated data
- [api-typestate](api-typestate.md) - Compile-time state machines
- [conv-tryfrom-fallible](conv-tryfrom-fallible.md) - Parse via TryFrom
- [serde-try-from-validate](serde-try-from-validate.md) - Validate at the serde boundary
