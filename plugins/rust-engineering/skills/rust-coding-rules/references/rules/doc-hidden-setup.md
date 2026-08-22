# doc-hidden-setup

> Use `# ` prefix to hide example setup code

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-documentation; supporters=`rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use `# ` prefix to hide example setup code.

## Apply When

Apply when a user-facing or safety-relevant Rust contract needs discoverable guarantees, examples, errors, panics, features, or migration guidance, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the prose would duplicate volatile implementation detail or claim behavior not established by current code and tests. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Identify the reader path and contract, write the smallest complete example, and link to one authoritative detailed explanation.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

More documentation improves discoverability but duplicated volatile detail drifts; executable examples cost maintenance but catch contract regressions.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Run rustdoc links and doctests under intended features and inspect that examples include their actual prerequisites.

## Why It Matters

Doc examples often require setup code (imports, struct initialization, mock data) that distracts from the main point. The `# ` prefix hides lines from rendered documentation while keeping them in the compiled test, showing users only the relevant code.

This keeps examples focused and readable while ensuring they still compile and run.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
/// Processes a batch of items.
///
/// # Examples
///
/// ```
/// use my_crate::{Processor, Config, Item};
/// use std::sync::Arc;
/// 
/// let config = Config {
///     batch_size: 100,
///     timeout_ms: 5000,
///     retry_count: 3,
/// };
/// let processor = Processor::new(Arc::new(config));
/// let items = vec![
///     Item::new("a"),
///     Item::new("b"),
///     Item::new("c"),
/// ];
/// 
/// // This is the actual example - buried after 15 lines of setup
/// let results = processor.process_batch(&items)?;
/// assert!(results.all_succeeded());
/// # Ok::<(), my_crate::Error>(())
/// ```
pub fn process_batch(&self, items: &[Item]) -> Result<Results, Error> {
    // ...
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// Processes a batch of items.
///
/// # Examples
///
/// ```
/// # use my_crate::{Processor, Config, Item, Error};
/// # use std::sync::Arc;
/// # let config = Config { batch_size: 100, timeout_ms: 5000, retry_count: 3 };
/// # let processor = Processor::new(Arc::new(config));
/// # let items = vec![Item::new("a"), Item::new("b"), Item::new("c")];
/// let results = processor.process_batch(&items)?;
/// assert!(results.all_succeeded());
/// # Ok::<(), Error>(())
/// ```
pub fn process_batch(&self, items: &[Item]) -> Result<Results, Error> {
    // ...
}
```

Users see only:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
let results = processor.process_batch(&items)?;
assert!(results.all_succeeded());
```

## What to Hide

| Hide | Show |
|------|------|
| `use` statements | Core API usage |
| Type definitions | Method calls |
| Mock/test data setup | Key parameters |
| Error handling boilerplate | Return value handling |
| `Ok(())` return | Assertions (sometimes) |

## Pattern: Hiding Multi-Line Setup

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Hiding Multi-Line Setup illustration -->
```rust
/// # Examples
///
/// ```
/// # use my_crate::{Client, Request};
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// # let client = Client::builder()
/// #     .timeout(30)
/// #     .retry(3)
/// #     .build()?;
/// let response = client.send(Request::get("/users"))?;
/// println!("Status: {}", response.status());
/// # Ok(())
/// # }
/// ```
```

## Pattern: Showing Setup When Relevant

Sometimes setup IS the point—don't hide it:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: Showing Setup When Relevant illustration -->
```rust
/// Creates a new client with custom configuration.
///
/// # Examples
///
/// ```
/// use my_crate::Client;
///
/// // Configuration IS the example - show it
/// let client = Client::builder()
///     .base_url("https://api.example.com")
///     .timeout_secs(30)
///     .max_retries(3)
///     .build()?;
/// # Ok::<(), my_crate::Error>(())
/// ```
```

## Pattern: `ignore` and `no_run`

For examples that shouldn't run in tests:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pattern: ignore and norun illustration -->
```rust
/// # Examples
///
/// ```no_run
/// # use my_crate::Server;
/// // This would actually start a server - don't run in tests
/// let server = Server::bind("0.0.0.0:8080").await?;
/// server.run().await?;
/// # Ok::<(), my_crate::Error>(())
/// ```

/// ```ignore
/// // Pseudocode or incomplete example
/// let magic = do_something_undefined();
/// ```
```

## Related Rules
- [doc-examples-section](./doc-examples-section.md) - Writing examples
- [doc-question-mark](./doc-question-mark.md) - Using `?` in examples
- [test-doctest-examples](./test-doctest-examples.md) - Doctests as tests
