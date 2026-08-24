# Naming Conventions

Prefix: `name-` · 16 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when an identifier is part of a Rust caller contract or repository convention and its name communicates cost, ownership, state, or behavior.
- Defer when a rename would create compatibility churn without improving meaning or merely enforces taste already handled by tooling.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`name-acronym-word`](../rules/name-acronym-word.md) | `canonical` | `rust-style-clippy` | Treat acronyms as words in identifiers: `HttpServer`, not `HTTPServer` |
| [`name-as-free`](../rules/name-as-free.md) | `conditional` | `rust-api-design` | `as_` prefix: free reference conversion |
| [`name-consts-screaming`](../rules/name-consts-screaming.md) | `canonical` | `rust-style-clippy` | Use `SCREAMING_SNAKE_CASE` for constants and statics |
| [`name-crate-no-rs`](../rules/name-crate-no-rs.md) | `conditional` | `rust-style-clippy` | Don't suffix crate names with `-rs` or `-rust` |
| [`name-funcs-snake`](../rules/name-funcs-snake.md) | `canonical` | `rust-style-clippy` | Use `snake_case` for functions, methods, variables, and modules |
| [`name-into-ownership`](../rules/name-into-ownership.md) | `conditional` | `rust-api-design` | Use `into_` prefix for ownership-consuming conversions |
| [`name-is-has-bool`](../rules/name-is-has-bool.md) | `canonical` | `rust-api-design` | Use `is_`, `has_`, `can_`, `should_` prefixes for boolean-returning methods |
| [`name-iter-convention`](../rules/name-iter-convention.md) | `canonical` | `rust-api-design` | Use iter/iter_mut/into_iter for iterator methods |
| [`name-iter-method`](../rules/name-iter-method.md) | `alias` | `rust-api-design` | Name iterator methods `iter()`, `iter_mut()`, and `into_iter()` consistently |
| [`name-iter-type-match`](../rules/name-iter-type-match.md) | `canonical` | `rust-api-design` | Name iterator types after their source method |
| [`name-lifetime-short`](../rules/name-lifetime-short.md) | `conditional` | `rust-style-clippy` | Use short, conventional lifetime names: `'a`, `'b`, `'de`, `'src` |
| [`name-no-get-prefix`](../rules/name-no-get-prefix.md) | `canonical` | `rust-api-design` | Omit get_ prefix for simple getters |
| [`name-to-expensive`](../rules/name-to-expensive.md) | `canonical` | `rust-api-design` | Use `to_` prefix for expensive conversions that allocate or compute |
| [`name-type-param-single`](../rules/name-type-param-single.md) | `canonical` | `rust-style-clippy` | Use single uppercase letters for type parameters: `T`, `E`, `K`, `V` |
| [`name-types-camel`](../rules/name-types-camel.md) | `canonical` | `rust-style-clippy` | Use `UpperCamelCase` for types, traits, and enum names |
| [`name-variants-camel`](../rules/name-variants-camel.md) | `canonical` | `rust-style-clippy` | Use `UpperCamelCase` for enum variants |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
