# serde-rename-all

> Match the external naming convention with `#[serde(rename_all = ...)]`## Decision

Consider this rule only after its prerequisites are satisfied: Match the external naming convention with `#[serde(rename_all = ...)]`.

## Apply When

Apply when an accepted Serde boundary needs an explicit wire shape, compatibility, unknown-field, default, or validation policy, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when Serde is not already accepted, the wire format is not a contract, or an attribute would silently broaden or discard input. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Write example payloads and compatibility requirements before choosing derive attributes, raw DTOs, or custom conversion.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Convenient derives tightly couple Rust representation and wire behavior unless DTOs, defaults, and validation boundaries are deliberate.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Round-trip and golden-test current, old, missing, extra, malformed, and adversarial payloads under the intended feature set.

## Why It Matters

Rust fields are `snake_case` by convention, but JSON APIs, GraphQL responses, and config formats often use `camelCase`, `kebab-case`, or `SCREAMING_SNAKE_CASE`. Renaming every field individually with `#[serde(rename = "...")]` is noisy and error-prone. A single `#[serde(rename_all = "camelCase")]` on the container keeps Rust idiomatic and the wire format correct in one declaration.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
struct UserProfile {
    #[serde(rename = "firstName")]
    first_name: String,
    #[serde(rename = "lastName")]
    last_name: String,
    #[serde(rename = "emailAddress")]
    email_address: String,
    #[serde(rename = "isActive")]
    is_active: bool,
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct UserProfile {
    first_name: String,
    last_name: String,
    email_address: String,
    is_active: bool,
    // per-field override: "type" is a keyword in Rust, so we rename it explicitly
    #[serde(rename = "type")]
    user_type: String,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "SCREAMING_SNAKE_CASE")]
enum Status {
    Active,
    Inactive,
    PendingVerification,
}
```

## Key Points

`rename_all` applies to both serialization and deserialization. Supported values:

| Value | Example field `foo_bar` becomes |
|---|---|
| `"camelCase"` | `fooBar` |
| `"PascalCase"` | `FooBar` |
| `"kebab-case"` | `foo-bar` |
| `"SCREAMING_SNAKE_CASE"` | `FOO_BAR` |
| `"snake_case"` | `foo_bar` (identity) |
| `"UPPERCASE"` | `FOOBAR` |
| `"lowercase"` | `foobar` |

A field-level `#[serde(rename = "...")]` always wins over the container-level `rename_all`, so use it for exceptions like reserved words or one-off mismatches. For enums, `rename_all` applies to variant names.

## Related Rules
- [serde-default-compat](serde-default-compat.md) - add default values for backward-compatible fields
- [api-serde-optional](api-serde-optional.md) - gate serde behind a feature flag in libraries

## Verified Rulebook Example

<!-- rust-example: fixture; dependencies: serde, serde_json -->
```rust
#[derive(Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(rename_all = "camelCase")]
struct Message {
    request_id: u64,
}

fn main() -> Result<(), serde_json::Error> {
    let value = Message { request_id: 7 };
    let json = serde_json::to_string(&value)?;
    assert_eq!(json, r#"{"requestId":7}"#);
    assert_eq!(serde_json::from_str::<Message>(&json)?, value);
    Ok(())
}
```
