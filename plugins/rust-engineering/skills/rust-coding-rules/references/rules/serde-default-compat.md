# serde-default-compat

> Use `#[serde(default)]` for optional and backward-compatible fields

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-api-design; supporters=`rust-errors`, `rust-cargo-build`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `#[serde(default)]` for optional and backward-compatible fields.

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

Without `#[serde(default)]`, any field missing from an incoming payload causes deserialization to fail with a "missing field" error. When you add new fields to a struct over time, older payloads that predate those fields will suddenly break. Marking fields (or the whole container) with `#[serde(default)]` fills missing keys from the type's `Default` implementation, enabling graceful forward compatibility.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
struct Config {
    host: String,
    port: u16,
    timeout_secs: u64,  // newly added — old configs don't have this, so they fail
    retries: u32,       // newly added — same problem
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};

fn default_timeout() -> u64 { 30 }
fn default_retries() -> u32 { 3 }

#[derive(Serialize, Deserialize, Debug)]
struct Config {
    host: String,
    port: u16,
    // fills from Default::default() (0u64) if missing
    #[serde(default)]
    timeout_secs: u64,
    // fills from the named function if missing
    #[serde(default = "default_retries")]
    retries: u32,
    // fills from Default (None) if missing
    #[serde(default)]
    tls_cert_path: Option<String>,
}

// Alternatively, annotate the whole container so every field uses its Default:
#[derive(Serialize, Deserialize, Debug, Default)]
#[serde(default)]
struct FeatureFlags {
    enable_caching: bool,    // false
    enable_metrics: bool,    // false
    max_connections: u32,    // 0
}
```

## Key Points

- **Field-level** `#[serde(default)]` — fills only that field; other required fields still fail if absent.
- **Field-level** `#[serde(default = "path")]` — calls a user-supplied function `fn() -> T`; use this when `Default` would produce the wrong value (e.g. `timeout = 30` rather than `0`).
- **Container-level** `#[serde(default)]` — applies to every field; the struct must implement `Default` (or `#[derive(Default)]`). Convenient for all-optional structs like feature-flag configs.
- The default function signature must be `fn() -> T` with no arguments and no generics.
- `#[serde(default)]` only affects **deserialization**. It has no effect on serialization; pair with `#[serde(skip_serializing_if = "...")]` if you also want to omit defaults on the way out.

## Caveats

Using container-level `#[serde(default)]` makes every field optional to deserializers, which can hide typos in field names. Prefer field-level annotation when only some fields are backward-compatible additions.

## Related Rules
- [serde-skip-empty](serde-skip-empty.md) - omit None/empty values during serialization
- [api-default-impl](api-default-impl.md) - implement `Default` for sensible defaults
