# doc-errors-section

> Include `# Errors` section for fallible functions

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-documentation; supporters=`rust-api-design`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Include `# Errors` section for fallible functions.

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
- External crates referenced by the source (`anyhow`) must already be accepted by the project or be approved before addition.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Run rustdoc links and doctests under intended features and inspect that examples include their actual prerequisites.

## Why It Matters

Functions returning `Result` can fail in specific, documented ways. The `# Errors` section tells users exactly when and why a function might return an error, enabling them to handle failures appropriately without reading source code.

This is especially critical for library code where users cannot easily inspect implementation details.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
/// Opens a file and reads its contents.
pub fn read_file(path: &Path) -> Result<String, Error> {
    // Users have no idea what errors to expect
}

/// Connects to the database.
pub async fn connect(url: &str) -> Result<Connection, DbError> {
    // Multiple failure modes, none documented
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// Opens a file and reads its contents as a UTF-8 string.
///
/// # Errors
///
/// Returns an error if:
/// - The file does not exist ([`Error::NotFound`])
/// - The process lacks permission to read the file ([`Error::PermissionDenied`])
/// - The file contains invalid UTF-8 ([`Error::InvalidUtf8`])
pub fn read_file(path: &Path) -> Result<String, Error> {
    // ...
}

/// Establishes a connection to the database.
///
/// # Errors
///
/// This function will return an error if:
/// - The URL is malformed ([`DbError::InvalidUrl`])
/// - The database server is unreachable ([`DbError::ConnectionFailed`])
/// - Authentication fails ([`DbError::AuthenticationFailed`])
/// - The connection pool is exhausted ([`DbError::PoolExhausted`])
pub async fn connect(url: &str) -> Result<Connection, DbError> {
    // ...
}
```

## Error Documentation Patterns

### Simple Single Error

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Simple Single Error illustration -->
```rust
/// Parses a string as an integer.
///
/// # Errors
///
/// Returns [`ParseIntError`] if the string is not a valid integer.
pub fn parse_int(s: &str) -> Result<i64, ParseIntError> {
    s.parse()
}
```

### Multiple Error Variants

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Multiple Error Variants illustration -->
```rust
/// Sends an HTTP request and returns the response.
///
/// # Errors
///
/// | Error | Condition |
/// |-------|-----------|
/// | [`HttpError::Timeout`] | Request exceeded timeout duration |
/// | [`HttpError::InvalidUrl`] | URL could not be parsed |
/// | [`HttpError::ConnectionRefused`] | Server refused connection |
/// | [`HttpError::TlsError`] | TLS handshake failed |
pub fn send(request: Request) -> Result<Response, HttpError> {
    // ...
}
```

### Propagated Errors

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Propagated Errors illustration -->
```rust
/// Loads configuration from a file.
///
/// # Errors
///
/// Returns an error if:
/// - The configuration file cannot be read (IO error)
/// - The file contains invalid TOML syntax
/// - Required fields are missing from the configuration
///
/// The underlying error is wrapped with context about which
/// configuration file failed to load.
pub fn load_config(path: &Path) -> Result<Config, anyhow::Error> {
    // ...
}
```

## Linking to Error Types

Use intra-doc links to connect error variants to their definitions:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Linking to Error Types illustration -->
```rust
/// # Errors
///
/// Returns [`ValidationError::TooShort`] if the input is less than
/// the minimum length, or [`ValidationError::InvalidChars`] if it
/// contains forbidden characters.
```

## Related Rules
- [doc-panics-section](./doc-panics-section.md) - Documenting panics
- [err-doc-errors](./err-doc-errors.md) - Error documentation patterns
- [doc-intra-links](./doc-intra-links.md) - Linking to types
