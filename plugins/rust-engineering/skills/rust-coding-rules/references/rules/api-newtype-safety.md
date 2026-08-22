# api-newtype-safety

> Use newtypes to prevent mixing semantically different values

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-traits`, `rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use newtypes to prevent mixing semantically different values.

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

Raw primitives like `u64` or `String` carry no semantic meaning. A function taking `(u64, u64)` can easily be called with arguments swapped. Newtypes wrap primitives in distinct types, making the compiler catch mistakes at compile time rather than runtime.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct User {
    id: u64,
    group_id: u64,
    created_at: u64,  // Unix timestamp
}

fn add_user_to_group(user_id: u64, group_id: u64) { ... }

// Bug: arguments swapped - compiles fine, fails at runtime
let user = User { id: 100, group_id: 5, created_at: 1234567890 };
add_user_to_group(user.group_id, user.id);  // Silent bug!

// Bug: wrong field used - timestamp passed as ID
add_user_to_group(user.created_at, user.group_id);  // Compiles fine!
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct UserId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct GroupId(u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
struct Timestamp(u64);

struct User {
    id: UserId,
    group_id: GroupId,
    created_at: Timestamp,
}

fn add_user_to_group(user_id: UserId, group_id: GroupId) { ... }

// Compile error: expected UserId, found GroupId
let user = User { ... };
add_user_to_group(user.group_id, user.id);  // Error!

// Compile error: expected UserId, found Timestamp
add_user_to_group(user.created_at, user.group_id);  // Error!
```

## Derive Common Traits

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Derive Common Traits illustration -->
```rust
// Minimal: just enough for your use case
#[derive(Debug, Clone, Copy)]
struct MeterId(u32);

// Full ID type: hashable, comparable, displayable
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct OrderId(u64);

impl std::fmt::Display for OrderId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "ORD-{:08}", self.0)
    }
}

// With serde for serialization
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(transparent)]  // Serializes as raw u64
struct ProductId(u64);
```

## Constructor Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Constructor Patterns illustration -->
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Email(String);

impl Email {
    /// Creates a new Email, validating the format.
    pub fn new(s: &str) -> Result<Self, EmailError> {
        if is_valid_email(s) {
            Ok(Email(s.to_string()))
        } else {
            Err(EmailError::InvalidFormat)
        }
    }
    
    /// Returns the email as a string slice.
    pub fn as_str(&self) -> &str {
        &self.0
    }
}

// Usage enforces validation
let email = Email::new("user@example.com")?;  // Must go through validation
```

## Zero-Cost Abstraction

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Zero-Cost Abstraction illustration -->
```rust
use std::mem::size_of;

#[derive(Clone, Copy)]
struct Miles(f64);

#[derive(Clone, Copy)]
struct Kilometers(f64);

// Same size as raw f64
assert_eq!(size_of::<Miles>(), size_of::<f64>());
assert_eq!(size_of::<Kilometers>(), size_of::<f64>());

// But can't accidentally mix them
fn drive(distance: Miles) { ... }

let km = Kilometers(100.0);
drive(km);  // Error: expected Miles, found Kilometers

// Explicit conversion
impl From<Kilometers> for Miles {
    fn from(km: Kilometers) -> Self {
        Miles(km.0 * 0.621371)
    }
}

drive(km.into());  // Explicit, visible conversion
```

## When Newtypes Help Most

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When Newtypes Help Most illustration -->
```rust
// ✅ IDs that could be confused
fn transfer(from: AccountId, to: AccountId, amount: Money) { ... }

// ✅ Units that shouldn't mix
struct Celsius(f64);
struct Fahrenheit(f64);

// ✅ Validated strings
struct Username(String);  // Validated alphanumeric
struct Password(String);  // Never logged

// ✅ Different meanings of same type
struct Milliseconds(u64);
struct Seconds(u64);

// ❌ Overkill: single use, no confusion possible
struct X(i32);  // Just use i32
```

## Related Rules
- [type-newtype-ids](./type-newtype-ids.md) - Newtype pattern for IDs
- [api-parse-dont-validate](./api-parse-dont-validate.md) - Type-driven validation
- [own-copy-small](./own-copy-small.md) - Making newtypes Copy
