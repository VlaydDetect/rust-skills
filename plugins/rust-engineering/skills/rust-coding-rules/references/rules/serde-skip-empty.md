# serde-skip-empty

> Omit empty fields with `skip_serializing_if`## Decision

Consider this rule only after its prerequisites are satisfied: Omit empty fields with `skip_serializing_if`.

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

Serializing `None` values as `null` and empty collections as `[]` bloats payloads, clutters logs, and can confuse clients that distinguish between a missing key and an explicit null. `#[serde(skip_serializing_if = "predicate")]` conditionally drops a field from output when the predicate returns true, keeping the wire format lean. `#[serde(skip)]` goes further and excludes a field from both serialization and deserialization entirely.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct ApiResponse {
    id: u64,
    name: String,
    description: Option<String>,  // serializes as null when None
    tags: Vec<String>,            // serializes as [] when empty
    error: Option<String>,        // serializes as null when None
}
```

Produces: `{"id":1,"name":"Alice","description":null,"tags":[],"error":null}`

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct ApiResponse {
    id: u64,
    name: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    description: Option<String>,
    #[serde(skip_serializing_if = "Vec::is_empty")]
    tags: Vec<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
    // internal field excluded entirely from the wire format
    #[serde(skip)]
    _cache_key: Option<String>,
}

impl Default for ApiResponse {
    fn default() -> Self {
        ApiResponse {
            id: 0,
            name: String::new(),
            description: None,
            tags: Vec::new(),
            error: None,
            _cache_key: None,
        }
    }
}
```

Produces: `{"id":1,"name":"Alice"}` — absent fields are simply omitted.

## Key Points

- `skip_serializing_if` takes any path resolving to `fn(&T) -> bool`. Common choices:
  - `Option::is_none` for `Option<T>`
  - `Vec::is_empty` / `<[T]>::is_empty` for collections
  - `String::is_empty` for strings
  - A custom function for more complex conditions
- `#[serde(skip)]` removes the field from **both** directions. The type must implement `Default` so deserialization can still construct the struct (serde fills it with `Default::default()`).
- `#[serde(skip_serializing)]` skips only on the way out; `#[serde(skip_deserializing)]` skips only on the way in — useful when reading legacy fields you no longer write.
- Pair `skip_serializing_if` with `#[serde(default)]` so that a missing key on deserialization also produces the empty/`None` value rather than a hard error.

## Related Rules
- [serde-default-compat](serde-default-compat.md) - fill missing fields from Default on deserialization
- [serde-rename-all](serde-rename-all.md) - match external naming conventions with rename_all
