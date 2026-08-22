# test-doctest-examples

> Keep documentation examples as executable doctests

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Keep documentation examples as executable doctests.

## Apply When

Apply when a concrete contract or risk needs the cheapest deterministic test that would fail for the defect, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the technique duplicates lower-cost coverage or adds a framework, snapshot, mock, sleep, or fuzz harness without unique risk coverage. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Map the contract to one test level and technique, isolate uncontrolled resources, and prove the assertion fails for the intended regression when practical.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Specialized test tools broaden state-space coverage but add dependencies, execution cost, maintenance, and false-stability risk.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tempfile`) must already be accepted by the project or be approved before addition.

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

Doctests are examples in documentation that are automatically tested. They serve dual purposes: demonstrating usage to readers and verifying the examples compile and work. When your API changes, failing doctests catch outdated documentation.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
/// Parses a number from a string.
/// 
/// Example:
/// let n = parse("42");  // Not tested!
/// assert_eq!(n, 42);
pub fn parse(s: &str) -> i32 {
    s.parse().unwrap()
}

// Documentation can become outdated:
/// Adds two numbers.
/// 
/// ```
/// let sum = add(1, 2, 3);  // Wrong number of args - not caught!
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// Parses a number from a string.
/// 
/// # Examples
/// 
/// ```
/// use my_crate::parse;
/// 
/// let n = parse("42");
/// assert_eq!(n, 42);
/// ```
pub fn parse(s: &str) -> i32 {
    s.parse().unwrap()
}

/// Adds two numbers.
/// 
/// # Examples
/// 
/// ```
/// use my_crate::add;
/// 
/// let sum = add(1, 2);
/// assert_eq!(sum, 3);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## Hiding Setup Code

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Hiding Setup Code illustration -->
```rust
/// Processes data from a file.
/// 
/// # Examples
/// 
/// ```
/// # use std::io::Write;
/// # let mut file = tempfile::NamedTempFile::new().unwrap();
/// # writeln!(file, "test data").unwrap();
/// # let path = file.path();
/// use my_crate::process_file;
/// 
/// let result = process_file(path)?;
/// assert!(!result.is_empty());
/// # Ok::<(), Box<dyn std::error::Error>>(())
/// ```
pub fn process_file(path: &Path) -> Result<String, Error> {
    std::fs::read_to_string(path).map_err(Error::from)
}
```

## Showing Error Handling

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Showing Error Handling illustration -->
```rust
/// Parses and validates an email address.
/// 
/// # Examples
/// 
/// ```
/// use my_crate::Email;
/// 
/// let email = Email::parse("user@example.com")?;
/// assert_eq!(email.domain(), "example.com");
/// # Ok::<(), my_crate::EmailError>(())
/// ```
/// 
/// # Errors
/// 
/// Returns error for invalid format:
/// 
/// ```
/// use my_crate::Email;
/// 
/// assert!(Email::parse("not-an-email").is_err());
/// ```
pub fn parse(s: &str) -> Result<Email, EmailError> {
    // ...
}
```

## no_run and ignore

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the norun and ignore illustration -->
```rust
/// Starts the server.
/// 
/// ```no_run
/// use my_crate::Server;
/// 
/// // This compiles but doesn't run (would block forever)
/// Server::new().run();
/// ```
pub fn run(&self) { ... }

/// Platform-specific example.
/// 
/// ```ignore
/// // This might not compile on all platforms
/// use windows_specific::Feature;
/// ```
```

## compile_fail

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the compilefail illustration -->
```rust
/// This type is not Clone.
/// 
/// ```compile_fail
/// use my_crate::UniqueHandle;
/// 
/// let a = UniqueHandle::new();
/// let b = a.clone();  // Error: Clone not implemented
/// ```
pub struct UniqueHandle { ... }
```

## Running Doctests

```bash
# Run all tests including doctests
cargo test

# Run only doctests
cargo test --doc

# Run doctests for specific item
cargo test --doc my_function
```

## Related Rules
- [doc-examples-section](./doc-examples-section.md) - Documentation structure
- [doc-hidden-setup](./doc-hidden-setup.md) - Hiding setup code
- [doc-question-mark](./doc-question-mark.md) - Error handling in examples
