# serde-custom-with

> Customize a field's (de)serialization with `with` / `serialize_with` / `deserialize_with`## Decision

Consider this rule only after its prerequisites are satisfied: Customize a field's (de)serialization with `with` / `serialize_with` / `deserialize_with`.

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
- External crates referenced by the source (`serde`, `bytes`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Round-trip and golden-test current, old, missing, extra, malformed, and adversarial payloads under the intended feature set.

## Why It Matters

Some types have a natural Rust representation that differs from what the wire format expects: a `Duration` stored as whole seconds, raw bytes encoded as base64, a timestamp as an ISO-8601 string. Changing the field type just to satisfy serde pollutes the domain model. A `#[serde(with = "module")]` (or the one-sided `serialize_with`/`deserialize_with`) attributes point serde at custom conversion functions without touching the field type.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

// Forces a u64 "seconds" field instead of the natural Duration type
#[derive(Serialize, Deserialize, Debug)]
struct Task {
    name: String,
    timeout_secs: u64,   // callers must manually convert to/from Duration
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize, Serializer, Deserializer};
use std::time::Duration;

mod duration_secs {
    use super::*;

    pub fn serialize<S>(duration: &Duration, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        serializer.serialize_u64(duration.as_secs())
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Duration, D::Error>
    where
        D: Deserializer<'de>,
    {
        let secs = u64::deserialize(deserializer)?;
        Ok(Duration::from_secs(secs))
    }
}

#[derive(Serialize, Deserialize, Debug)]
struct Task {
    name: String,
    // wire format: {"name":"...", "timeout": 30}
    // Rust type: Duration — no manual conversion needed at call sites
    #[serde(with = "duration_secs", rename = "timeout")]
    timeout: Duration,
}

// One-sided variants when you only need to customize one direction:
#[derive(Serialize, Deserialize, Debug)]
struct Report {
    title: String,
    #[serde(serialize_with = "duration_secs::serialize")]
    elapsed: Duration,
    // deserialize_with leaves the deserialize direction at its default
}
```

## Key Points

- `#[serde(with = "module")]` requires the module to expose both `pub fn serialize<S>(&T, S) -> Result<S::Ok, S::Error>` and `pub fn deserialize<'de, D>(D) -> Result<T, D::Error>`.
- Use `serialize_with = "path"` or `deserialize_with = "path"` to customize only one direction, leaving the other at its derived default.
- The module approach (`with`) is more reusable: define it once, apply it anywhere. Some crates (e.g. `time`, `chrono`, `uuid`) ship ready-made `with` modules in their serde feature.
- For widespread custom representations, a newtype wrapper with its own `Serialize`/`Deserialize` impl is often cleaner than repeating `#[serde(with = "...")]` everywhere.

## Caveats

The `with` module functions must match the exact signatures serde expects. The `serialize` function receives `&T` (a reference), not `T`.

## Related Rules
- [serde-try-from-validate](serde-try-from-validate.md) - validate while deserializing with TryFrom
- [type-newtype-validated](type-newtype-validated.md) - newtypes for validated data
