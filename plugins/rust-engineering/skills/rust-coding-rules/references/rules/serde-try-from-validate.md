# serde-try-from-validate

> Validate while deserializing with `#[serde(try_from = "Raw")]`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-errors`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Validate while deserializing with `#[serde(try_from = "Raw")]`.

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
- External crates referenced by the source (`serde_json`, `serde`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Round-trip and golden-test current, old, missing, extra, malformed, and adversarial payloads under the intended feature set.

## Why It Matters

Running validation after deserialization means you can construct an invalid value in memory, even briefly. Parse-don't-validate says to make invalid states unrepresentable. `#[serde(try_from = "Raw")]` wires the deserializer directly through a `TryFrom` conversion: serde reads the raw type, then your conversion either produces the validated value or returns an error — so an invalid instance is never constructed.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Email(String);

impl Email {
    fn new(s: String) -> Result<Self, String> {
        if s.contains('@') {
            Ok(Email(s))
        } else {
            Err(format!("invalid email: {s}"))
        }
    }
}

// Caller must validate after deserialization — easy to forget:
fn process(json: &str) -> Result<(), Box<dyn std::error::Error>> {
    let email: Email = serde_json::from_str(json)?;
    // nothing stops "notanemail" from being deserialized and used
    println!("{:?}", email);
    Ok(())
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};
use serde_json;

#[derive(Debug, Clone)]
struct Email(String);

impl TryFrom<String> for Email {
    type Error = String;

    fn try_from(s: String) -> Result<Self, Self::Error> {
        if s.contains('@') && !s.starts_with('@') && !s.ends_with('@') {
            Ok(Email(s))
        } else {
            Err(format!("invalid email address: {s}"))
        }
    }
}

// For the serialize direction: implement From<Email> for String, then add into = "String"
impl From<Email> for String {
    fn from(e: Email) -> String {
        e.0
    }
}

// Deserialize: serde reads a String, then calls Email::try_from — error if invalid.
// Serialize:   serde calls String::from(email) — converts back to the raw type.
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(try_from = "String", into = "String")]
struct ValidatedEmail(String);

impl TryFrom<String> for ValidatedEmail {
    type Error = String;

    fn try_from(s: String) -> Result<Self, Self::Error> {
        if s.contains('@') && !s.starts_with('@') && !s.ends_with('@') {
            Ok(ValidatedEmail(s))
        } else {
            Err(format!("invalid email address: {s}"))
        }
    }
}

impl From<ValidatedEmail> for String {
    fn from(e: ValidatedEmail) -> String {
        e.0
    }
}

fn main() {
    // Valid email round-trips fine
    let good = serde_json::from_str::<ValidatedEmail>("\"user@example.com\"").unwrap();
    println!("{}", serde_json::to_string(&good).unwrap());

    // Invalid email is rejected at parse time — never enters the program
    let bad = serde_json::from_str::<ValidatedEmail>("\"notanemail\"");
    assert!(bad.is_err());
}
```

## Key Points

- `#[serde(try_from = "Raw")]` — serde deserializes `Raw`, then calls `T::try_from(raw)?`. Any error from `TryFrom` becomes a serde deserialization error.
- `#[serde(into = "Raw")]` — serde calls `Raw::from(value)` for serialization. The type must also implement `Clone` because serde may clone before converting.
- The `Raw` type must itself implement `Deserialize` (for `try_from`) and the target must implement `Into<Raw>` / `From<T> for Raw` (for `into`).
- This pattern is composable with other rules: define the `TryFrom` logic once and reuse it in both serde and non-serde code paths (e.g. CLI argument parsing, form validation).

## Caveats

`#[serde(try_from)]` and `#[serde(into)]` are mutually exclusive with deriving `Serialize`/`Deserialize` via field-by-field derivation on the same struct — the attribute replaces the derived impl entirely.

## Related Rules
- [api-parse-dont-validate](api-parse-dont-validate.md) - parse into validated types at boundaries
- [type-newtype-validated](type-newtype-validated.md) - newtypes for validated data
- [serde-custom-with](serde-custom-with.md) - customize field (de)serialization with with modules
