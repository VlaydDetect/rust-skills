# Documentation

Prefix: `doc-` · 12 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a user-facing or safety-relevant Rust contract needs discoverable guarantees, examples, errors, panics, features, or migration guidance.
- Defer when the prose would duplicate volatile implementation detail or claim behavior not established by current code and tests.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`doc-all-public`](../rules/doc-all-public.md) | `canonical` | `rust-documentation` | Document all public items with `///` doc comments |
| [`doc-cargo-metadata`](../rules/doc-cargo-metadata.md) | `conditional` | `rust-documentation` | Fill `Cargo.toml` metadata for published crates |
| [`doc-crate-readme`](../rules/doc-crate-readme.md) | `canonical` | `rust-documentation` | Unify the README and crate root docs with `#![doc = include_str!("../README.md")]` |
| [`doc-errors-section`](../rules/doc-errors-section.md) | `conditional` | `rust-documentation` | Include `# Errors` section for fallible functions |
| [`doc-examples-section`](../rules/doc-examples-section.md) | `canonical` | `rust-documentation` | Include `# Examples` with runnable code |
| [`doc-hidden-setup`](../rules/doc-hidden-setup.md) | `canonical` | `rust-documentation` | Use `# ` prefix to hide example setup code |
| [`doc-intra-links`](../rules/doc-intra-links.md) | `conditional` | `rust-documentation` | Use intra-doc links to reference types and items |
| [`doc-link-types`](../rules/doc-link-types.md) | `alias` | `rust-documentation` | Use intra-doc links to connect related types and functions |
| [`doc-module-inner`](../rules/doc-module-inner.md) | `conditional` | `rust-documentation` | Use `//!` for module-level documentation |
| [`doc-panics-section`](../rules/doc-panics-section.md) | `canonical` | `rust-documentation` | Include `# Panics` section for functions that can panic |
| [`doc-question-mark`](../rules/doc-question-mark.md) | `canonical` | `rust-documentation` | Use `?` in examples, not `.unwrap()` |
| [`doc-safety-section`](../rules/doc-safety-section.md) | `conditional` | `rust-documentation` | Include `# Safety` section for unsafe functions |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
