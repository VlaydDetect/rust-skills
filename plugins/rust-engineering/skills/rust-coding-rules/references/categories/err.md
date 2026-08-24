# Error Handling

Prefix: `err-` · 12 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when the caller-visible failure taxonomy, propagation, recovery, context, or panic policy is being decided.
- Defer when the failure is an internal invariant violation, or erasure would remove a caller action that the boundary promises.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`err-anyhow-app`](../rules/err-anyhow-app.md) | `conditional` | `rust-errors` | Use `anyhow` for application error handling |
| [`err-context-chain`](../rules/err-context-chain.md) | `conditional` | `rust-errors` | Add context with `.context()` or `.with_context()` |
| [`err-custom-type`](../rules/err-custom-type.md) | `conditional` | `rust-errors` | Define custom error types for domain-specific failures |
| [`err-doc-errors`](../rules/err-doc-errors.md) | `alias` | `rust-documentation` | Document error conditions with `# Errors` section in doc comments |
| [`err-expect-bugs-only`](../rules/err-expect-bugs-only.md) | `conditional` | `rust-errors` | Use `expect()` only for invariants that indicate bugs, not user errors |
| [`err-from-impl`](../rules/err-from-impl.md) | `conditional` | `rust-errors` | Implement `From<E>` for error conversions to enable `?` operator |
| [`err-lowercase-msg`](../rules/err-lowercase-msg.md) | `conditional` | `rust-errors` | Start error messages lowercase, no trailing punctuation |
| [`err-no-unwrap-prod`](../rules/err-no-unwrap-prod.md) | `conditional` | `rust-errors` | Avoid `unwrap()` in production code; use `?`, `expect()`, or handle errors |
| [`err-question-mark`](../rules/err-question-mark.md) | `conditional` | `rust-errors` | Use `?` operator for clean propagation |
| [`err-result-over-panic`](../rules/err-result-over-panic.md) | `conditional` | `rust-errors` | Return `Result<T, E>` instead of panicking for recoverable errors |
| [`err-source-chain`](../rules/err-source-chain.md) | `conditional` | `rust-errors` | Preserve error chains with `#[source]` or `source()` method |
| [`err-thiserror-lib`](../rules/err-thiserror-lib.md) | `conditional` | `rust-errors` | Use `thiserror` for library error types |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
