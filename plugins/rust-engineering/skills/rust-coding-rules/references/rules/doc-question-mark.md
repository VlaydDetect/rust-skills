# doc-question-mark

> Use `?` in examples, not `.unwrap()`

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-documentation; supporters=`rust-api-design`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use `?` in examples, not `.unwrap()`.

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

Doc examples should model best practices. Using `.unwrap()` teaches users to ignore errors, while `?` demonstrates proper error propagation. Examples with `?` also fail the doctest if an error occurs, catching bugs in documentation.

Rust doctests wrap examples in a function that returns `Result<(), E>` by default when you use `?`, making this pattern easy to adopt.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
/// Reads a configuration file.
///
/// # Examples
///
/// ```
/// let config = Config::from_file("config.toml").unwrap();
/// println!("{:?}", config.database_url);
/// ```
pub fn from_file(path: &str) -> Result<Config, Error> {
    // ...
}

/// Fetches data from the API.
///
/// # Examples
///
/// ```
/// let client = Client::new();
/// let response = client.get("https://api.example.com").unwrap();
/// let data: Data = response.json().unwrap();
/// ```
pub async fn get(&self, url: &str) -> Result<Response, Error> {
    // ...
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// Reads a configuration file.
///
/// # Examples
///
/// ```
/// # use my_crate::{Config, Error};
/// # fn main() -> Result<(), Error> {
/// let config = Config::from_file("config.toml")?;
/// println!("{:?}", config.database_url);
/// # Ok(())
/// # }
/// ```
pub fn from_file(path: &str) -> Result<Config, Error> {
    // ...
}

/// Fetches data from the API.
///
/// # Examples
///
/// ```no_run
/// # use my_crate::{Client, Data, Error};
/// # async fn example() -> Result<(), Error> {
/// let client = Client::new();
/// let response = client.get("https://api.example.com").await?;
/// let data: Data = response.json().await?;
/// # Ok(())
/// # }
/// ```
pub async fn get(&self, url: &str) -> Result<Response, Error> {
    // ...
}
```

## Doctest Wrapper Pattern

Rust wraps doc examples in a function. You can make this explicit:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Doctest Wrapper Pattern illustration -->
```rust
/// # Examples
///
/// ```
/// # fn main() -> Result<(), Box<dyn std::error::Error>> {
/// let value = parse_config("key=value")?;
/// assert_eq!(value.key, "value");
/// # Ok(())
/// # }
/// ```
```

Or use the implicit wrapper (Rust 2021+):

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Doctest Wrapper Pattern illustration -->
```rust
/// # Examples
///
/// ```
/// # use my_crate::parse_config;
/// let value = parse_config("key=value")?;
/// assert_eq!(value.key, "value");
/// # Ok::<(), my_crate::Error>(())
/// ```
```

## When to Use `.unwrap()`

There are specific cases where `.unwrap()` is acceptable in examples:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Use .unwrap() illustration -->
```rust
/// # Examples
///
/// ```
/// // Static regex that is known at compile time to be valid
/// let re = Regex::new(r"^\d{4}-\d{2}-\d{2}$").unwrap();
///
/// // Parsing a literal that cannot fail
/// let n: i32 = "42".parse().unwrap();
/// ```
```

But still prefer `?` when demonstrating error handling patterns.

## Comparison

| Pattern | Behavior on Error | Teaches |
|---------|-------------------|---------|
| `.unwrap()` | Panics with generic message | Bad habits |
| `.expect()` | Panics with custom message | Slightly better |
| `?` | Propagates error, test fails | Best practices |

## Related Rules
- [doc-examples-section](./doc-examples-section.md) - Writing examples
- [doc-hidden-setup](./doc-hidden-setup.md) - Hiding setup code
- [err-question-mark](./err-question-mark.md) - Error propagation
