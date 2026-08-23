# type-newtype-ids

> Wrap IDs in newtypes: `UserId(u64)`## Decision

Consider this rule only after its prerequisites are satisfied: Wrap IDs in newtypes: `UserId(u64)`.

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

Using raw integers for IDs is error-prone. It's easy to accidentally pass a `user_id` where a `post_id` is expected. Newtypes make these mix-ups compile-time errors instead of runtime bugs.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
fn get_user_posts(user_id: u64, post_id: u64) -> Vec<Post> {
    // Which is which? Easy to swap by accident
}

// Oops! Arguments swapped - compiles fine, wrong at runtime
let posts = get_user_posts(post_id, user_id);

// Even worse with multiple IDs
fn transfer(from: u64, to: u64, amount: u64) {
    // from/to can easily be swapped
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(pub u64);

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PostId(pub u64);

fn get_user_posts(user_id: UserId, post_id: PostId) -> Vec<Post> {
    // Types are distinct
}

// This won't compile - types don't match
// let posts = get_user_posts(post_id, user_id);  // ERROR!

// Correct usage
let posts = get_user_posts(UserId(1), PostId(42));
```

## Derive Common Traits

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Derive Common Traits illustration -->
```rust
#[derive(
    Debug,      // For printing
    Clone,      // For copying
    Copy,       // For implicit copies (if small)
    PartialEq,  // For == comparison
    Eq,         // For HashMap keys
    Hash,       // For HashMap keys
    PartialOrd, // For sorting (optional)
    Ord,        // For BTreeMap keys (optional)
)]
pub struct UserId(pub u64);
```

## Add Useful Methods

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Add Useful Methods illustration -->
```rust
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct UserId(u64);

impl UserId {
    pub const fn new(id: u64) -> Self {
        Self(id)
    }
    
    pub const fn get(self) -> u64 {
        self.0
    }
    
    // For database queries
    pub fn as_i64(self) -> i64 {
        self.0 as i64
    }
}

impl From<u64> for UserId {
    fn from(id: u64) -> Self {
        Self(id)
    }
}

impl std::fmt::Display for UserId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "user:{}", self.0)
    }
}
```

## With Serde

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With Serde illustration -->
```rust
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[serde(transparent)]  // Serializes as just the inner value
pub struct UserId(pub u64);

// JSON: {"user_id": 123} not {"user_id": {"0": 123}}
```

## String IDs (UUIDs, etc.)

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the String IDs (UUIDs, etc.) illustration -->
```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct SessionId(String);

impl SessionId {
    pub fn new() -> Self {
        Self(uuid::Uuid::new_v4().to_string())
    }
    
    pub fn parse(s: &str) -> Result<Self, ParseError> {
        // Validate format
        uuid::Uuid::parse_str(s)?;
        Ok(Self(s.to_string()))
    }
    
    pub fn as_str(&self) -> &str {
        &self.0
    }
}
```

## Multiple Related IDs

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Multiple Related IDs illustration -->
```rust
// Macro for consistent ID types
macro_rules! define_id {
    ($name:ident) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
        pub struct $name(pub u64);
        
        impl $name {
            pub const fn new(id: u64) -> Self { Self(id) }
            pub const fn get(self) -> u64 { self.0 }
        }
        
        impl From<u64> for $name {
            fn from(id: u64) -> Self { Self(id) }
        }
    };
}

define_id!(UserId);
define_id!(PostId);
define_id!(CommentId);
define_id!(TeamId);
```

## Related Rules
- [api-newtype-safety](api-newtype-safety.md) - Newtypes for type safety
- [type-newtype-validated](type-newtype-validated.md) - Newtypes for validated data
- [api-parse-dont-validate](api-parse-dont-validate.md) - Parse into validated types
- [num-nonzero](num-nonzero.md) - NonZero* for never-zero ids
