# serde-deny-unknown-fields

> Reject unexpected keys with `#[serde(deny_unknown_fields)]`## Decision

Consider this rule only after its prerequisites are satisfied: Reject unexpected keys with `#[serde(deny_unknown_fields)]`.

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

By default, serde silently discards any key in the input that doesn't match a struct field. For user-facing config files and strict API contracts this is dangerous: a typo like `"timout_secs"` passes validation without error, and the intended field is simply never set. `#[serde(deny_unknown_fields)]` turns unrecognized keys into hard errors, surfacing mistakes immediately.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};
use serde_json;

#[derive(Serialize, Deserialize, Debug)]
struct ServerConfig {
    host: String,
    port: u16,
    timeout_secs: u64,
}

fn main() {
    // "timout_secs" is a typo — serde silently ignores it, timeout stays 0
    let json = r#"{"host":"localhost","port":8080,"timout_secs":30}"#;
    let cfg: ServerConfig = serde_json::from_str(json).unwrap();
    println!("{:?}", cfg); // timeout_secs is 0, not 30
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};
use serde_json;

#[derive(Serialize, Deserialize, Debug)]
#[serde(deny_unknown_fields)]
struct ServerConfig {
    host: String,
    port: u16,
    timeout_secs: u64,
}

fn parse_config(json: &str) -> Result<ServerConfig, serde_json::Error> {
    serde_json::from_str(json)
}

fn main() {
    // Typo is now a hard error
    let bad = r#"{"host":"localhost","port":8080,"timout_secs":30}"#;
    assert!(parse_config(bad).is_err());

    // Correct input still works
    let good = r#"{"host":"localhost","port":8080,"timeout_secs":30}"#;
    let cfg = parse_config(good).unwrap();
    println!("{:?}", cfg);
}
```

## Key Points

- Apply `deny_unknown_fields` to **config-file structs**, **request/response DTOs**, and any struct that forms a public API contract where typos must be caught.
- Skip it for **flexible or extensible** structs where callers are expected to pass extra metadata. Use `#[serde(flatten)]` with a `HashMap` catch-all instead.
- The attribute works with JSON, TOML, YAML, and most self-describing formats.
- Error messages name the unexpected field, making them actionable for end users.

## Caveats

`#[serde(deny_unknown_fields)]` is **incompatible with `#[serde(flatten)]`** on the same struct. `flatten` needs to pass unmatched keys down to the flattened field; `deny_unknown_fields` intercepts them first. If you need both behaviors, split the struct or use a two-pass approach (deserialize into a `serde_json::Value`, then convert).

## Related Rules
- [serde-flatten](serde-flatten.md) - inline nested structs or collect extra keys (incompatible with deny_unknown_fields)
- [api-parse-dont-validate](api-parse-dont-validate.md) - parse into validated types at boundaries
