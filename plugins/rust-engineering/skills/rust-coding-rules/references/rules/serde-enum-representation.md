# serde-enum-representation

> Choose enum tagging deliberately: externally, internally, adjacently tagged, or untagged## Decision

Consider this rule only after its prerequisites are satisfied: Choose enum tagging deliberately: externally, internally, adjacently tagged, or untagged.

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

Serde's default enum representation (externally tagged) wraps every variant in an object keyed by variant name. That format can clash with external APIs, event systems, or config schemas that use a discriminator field. Picking the wrong tagging strategy produces a mismatch between your wire format and the expected schema, leading to silent parse failures or round-trip data loss.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use serde::{Serialize, Deserialize};

// Default: externally tagged. Serializes as {"Circle":{"radius":5.0}}
// Most REST APIs expect {"type":"circle","radius":5.0} instead.
#[derive(Serialize, Deserialize, Debug)]
enum Shape {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use serde::{Serialize, Deserialize};

// Externally tagged (default) — {"Circle":{"radius":5.0}}
// Good for: Rust-to-Rust, when the variant name IS the key
#[derive(Serialize, Deserialize, Debug)]
enum ShapeExternal {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}

// Internally tagged — {"type":"Circle","radius":5.0}
// Good for: REST APIs with a discriminator field; all variants must be structs/maps
#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type")]
enum ShapeInternal {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
}

// Adjacently tagged — {"t":"Circle","c":{"radius":5.0}}
// Good for: when variants may contain primitives or vecs (internally tagged can't handle those)
#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "t", content = "c")]
enum ShapeAdjacent {
    Circle { radius: f64 },
    Rectangle { width: f64, height: f64 },
    Count(u32),  // tuple variant — works here, but NOT with internally tagged
}

// Untagged — {"radius":5.0}
// Good for: wrapping a small number of clearly distinct types; avoid otherwise
#[derive(Serialize, Deserialize, Debug)]
#[serde(untagged)]
enum Value {
    Integer(i64),
    Float(f64),
    Text(String),
}
```

## Comparison Table

| Strategy | Attribute | Wire form (Circle) | Tuple variant |
|---|---|---|---|
| Externally tagged | (default) | `{"Circle":{"radius":5}}` | yes |
| Internally tagged | `#[serde(tag = "type")]` | `{"type":"Circle","radius":5}` | no |
| Adjacently tagged | `#[serde(tag="t", content="c")]` | `{"t":"Circle","c":{"radius":5}}` | yes |
| Untagged | `#[serde(untagged)]` | `{"radius":5}` | yes |

## Caveats

- **Untagged** deserializes by trying each variant in declaration order; it is slower, can silently pick the wrong variant, and produces generic error messages. Reserve it for small, structurally distinct sets (numbers vs strings).
- **Internally tagged** cannot represent tuple variants or newtype variants wrapping primitives/vecs — use adjacently tagged instead.
- All variants in an internally tagged enum must serialize as maps (structs or `HashMap`).

## Related Rules
- [type-enum-states](type-enum-states.md) - use enums for mutually exclusive states
- [api-non-exhaustive](api-non-exhaustive.md) - use `#[non_exhaustive]` for future-proof enums
- [serde-flatten](serde-flatten.md) - inline nested struct fields into parent
