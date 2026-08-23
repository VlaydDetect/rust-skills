# serde-flatten

> Inline nested structs or capture extra keys with `#[serde(flatten)]`## Decision

Consider this rule only after its prerequisites are satisfied: Inline nested structs or capture extra keys with `#[serde(flatten)]`.

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

APIs frequently share a common set of fields across multiple message types (pagination metadata, audit timestamps, error envelopes). Duplicating those fields in every struct is fragile. `#[serde(flatten)]` merges a nested struct's fields directly into the parent's wire representation, so the JSON looks flat while the Rust code stays modular. The same attribute can also collect all unknown keys into a `HashMap`, giving you a "catch-all" bucket.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

// Duplicated pagination fields in every list response
#[derive(Serialize, Deserialize, Debug)]
struct UserListResponse {
    users: Vec<String>,
    page: u32,
    per_page: u32,
    total: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct PostListResponse {
    posts: Vec<String>,
    page: u32,       // copy-paste
    per_page: u32,   // copy-paste
    total: u64,      // copy-paste
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug)]
struct Pagination {
    page: u32,
    per_page: u32,
    total: u64,
}

#[derive(Serialize, Deserialize, Debug)]
struct UserListResponse {
    users: Vec<String>,
    #[serde(flatten)]
    pagination: Pagination,
}

#[derive(Serialize, Deserialize, Debug)]
struct PostListResponse {
    posts: Vec<String>,
    #[serde(flatten)]
    pagination: Pagination,
}

// Capture unknown/dynamic keys into a map
#[derive(Serialize, Deserialize, Debug)]
struct FlexibleConfig {
    name: String,
    version: u32,
    #[serde(flatten)]
    extra: HashMap<String, serde_json::Value>,
}
```

`UserListResponse` serializes to `{"users":[...],"page":1,"per_page":20,"total":100}` — the `Pagination` fields appear at the top level, not nested under a `"pagination"` key.

## Key Points

- Works with both structs and maps. The flattened type must implement `Serialize`/`Deserialize`.
- Multiple `#[serde(flatten)]` fields are allowed on the same struct, as long as the key sets don't overlap at runtime.
- `HashMap<String, serde_json::Value>` (or any map type) as a flattened field acts as a catch-all for keys not matched by other fields — useful for extensible configs and pass-through proxies.

## Caveats

- `#[serde(flatten)]` is **incompatible with `#[serde(deny_unknown_fields)]`** on the same struct. The two attributes conflict because `flatten` needs to forward unrecognized keys.
- Flattening uses a less efficient internal deserialization path (content buffering) compared to normal struct deserialization. Avoid it on extremely hot deserialization paths.
- `flatten` does not work with non-self-describing formats like `bincode` that don't support maps with arbitrary keys.

## Related Rules
- [serde-deny-unknown-fields](serde-deny-unknown-fields.md) - reject unexpected keys (incompatible with flatten)
- [serde-enum-representation](serde-enum-representation.md) - choose enum tagging strategy
