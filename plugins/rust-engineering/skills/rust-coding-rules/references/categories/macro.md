# Macros

Prefix: `macro-` · 8 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when ordinary functions, traits, generics, derives, or build-time generation cannot express required Rust syntax or repetition cleanly.
- Defer when a normal language abstraction is sufficient or the proposed DSL adds more grammar and diagnostics than value.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`macro-export-crate-path`](../rules/macro-export-crate-path.md) | `canonical` | `rust-macros` | Export declarative macros with `#[macro_export]` and a clean import path |
| [`macro-fragment-specifiers`](../rules/macro-fragment-specifiers.md) | `canonical` | `rust-macros` | Capture with precise fragment specifiers, not raw `:tt`, where you can |
| [`macro-prefer-functions`](../rules/macro-prefer-functions.md) | `canonical` | `rust-macros` | Reach for a macro only when a function or generic cannot express it |
| [`macro-private-helpers`](../rules/macro-private-helpers.md) | `conditional` | `rust-macros` | Hide macro-generated helper items behind a `#[doc(hidden)] pub mod __private` |
| [`macro-proc-error-spans`](../rules/macro-proc-error-spans.md) | `conditional` | `rust-macros` | Report proc-macro errors as spanned compile errors, never by panicking |
| [`macro-proc-syn-quote`](../rules/macro-proc-syn-quote.md) | `conditional` | `rust-macros` | Build procedural macros with `syn`, `quote`, and `proc-macro2` |
| [`macro-proc-two-crate`](../rules/macro-proc-two-crate.md) | `conditional` | `rust-macros` | Put procedural macros in a dedicated `proc-macro = true` crate and re-export from the facade |
| [`macro-rules-hygiene`](../rules/macro-rules-hygiene.md) | `canonical` | `rust-macros` | Rely on `macro_rules!` hygiene and use `$crate` for paths to your crate's items |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
