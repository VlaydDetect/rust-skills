# Serde

Prefix: `serde-` · 8 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when an accepted Serde boundary needs an explicit wire shape, compatibility, unknown-field, default, or validation policy.
- Defer when Serde is not already accepted, the wire format is not a contract, or an attribute would silently broaden or discard input.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`serde-custom-with`](../rules/serde-custom-with.md) | `conditional` | `rust-api-design` | Customize a field's (de)serialization with `with` / `serialize_with` / `deserialize_with` |
| [`serde-default-compat`](../rules/serde-default-compat.md) | `conditional` | `rust-api-design` | Use `#[serde(default)]` for optional and backward-compatible fields |
| [`serde-deny-unknown-fields`](../rules/serde-deny-unknown-fields.md) | `conditional` | `rust-api-design` | Reject unexpected keys with `#[serde(deny_unknown_fields)]` |
| [`serde-enum-representation`](../rules/serde-enum-representation.md) | `conditional` | `rust-api-design` | Choose enum tagging deliberately: externally, internally, adjacently tagged, or untagged |
| [`serde-flatten`](../rules/serde-flatten.md) | `conditional` | `rust-api-design` | Inline nested structs or capture extra keys with `#[serde(flatten)]` |
| [`serde-rename-all`](../rules/serde-rename-all.md) | `conditional` | `rust-api-design` | Match the external naming convention with `#[serde(rename_all = ...)]` |
| [`serde-skip-empty`](../rules/serde-skip-empty.md) | `conditional` | `rust-api-design` | Omit empty fields with `skip_serializing_if` |
| [`serde-try-from-validate`](../rules/serde-try-from-validate.md) | `conditional` | `rust-api-design` | Validate while deserializing with `#[serde(try_from = "Raw")]` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
