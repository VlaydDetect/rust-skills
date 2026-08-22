# test-should-panic

> Use `#[should_panic]` to test that code panics as expected

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use `#[should_panic]` to test that code panics as expected.

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

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

Some code should panic on invalid inputs or invariant violations. `#[should_panic]` verifies the panic occurs, optionally checking the panic message. This ensures defensive panics work correctly and documents expected panic conditions.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[test]
fn test_panic() {
    // Just calling panicking code makes test fail
    divide(1, 0);  // Test fails with panic
}

// Using catch_unwind is verbose
#[test]
fn test_panic_manual() {
    let result = std::panic::catch_unwind(|| divide(1, 0));
    assert!(result.is_err());
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[test]
#[should_panic]
fn divide_by_zero_panics() {
    divide(1, 0);  // Test passes when this panics
}

// With expected message
#[test]
#[should_panic(expected = "division by zero")]
fn divide_by_zero_panics_with_message() {
    divide(1, 0);  // Panics with "division by zero"
}

// Partial message match
#[test]
#[should_panic(expected = "index out of bounds")]
fn index_panic_contains_message() {
    let v = vec![1, 2, 3];
    let _ = v[100];  // Message contains "index out of bounds"
}
```

## Testing Invariants

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Testing Invariants illustration -->
```rust
struct NonEmpty<T>(Vec<T>);

impl<T> NonEmpty<T> {
    fn new(items: Vec<T>) -> Self {
        assert!(!items.is_empty(), "NonEmpty cannot be empty");
        NonEmpty(items)
    }
}

#[test]
#[should_panic(expected = "NonEmpty cannot be empty")]
fn non_empty_rejects_empty_vec() {
    NonEmpty::new(Vec::<i32>::new());
}

#[test]
fn non_empty_accepts_non_empty_vec() {
    let ne = NonEmpty::new(vec![1, 2, 3]);
    assert_eq!(ne.0.len(), 3);
}
```

## With expect() Messages

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With expect() Messages illustration -->
```rust
fn get_config_value(key: &str) -> String {
    CONFIG.get(key)
        .expect(&format!("missing required config: {}", key))
        .to_string()
}

#[test]
#[should_panic(expected = "missing required config: DATABASE_URL")]
fn missing_config_panics_with_key() {
    get_config_value("DATABASE_URL");
}
```

## When NOT to Use should_panic

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When NOT to Use shouldpanic illustration -->
```rust
// ❌ For recoverable errors - use Result
#[test]
#[should_panic]  // Wrong: this should return Err, not panic
fn invalid_input_panics() {
    parse_config("invalid");  // Should return Err, not panic
}

// ✅ Return Result and test the error
#[test]
fn invalid_input_returns_error() {
    let result = parse_config("invalid");
    assert!(result.is_err());
}
```

## Combining with Result

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Combining with Result illustration -->
```rust
#[test]
#[should_panic]
fn test_panics() -> Result<(), Error> {
    // Can combine with Result for setup
    let data = setup_test_data()?;
    
    // This should panic
    process_invalid(&data);
    
    Ok(())  // Never reached
}
```

## Related Rules
- [err-result-over-panic](./err-result-over-panic.md) - Panic vs Result
- [err-expect-bugs-only](./err-expect-bugs-only.md) - When to use expect
- [test-descriptive-names](./test-descriptive-names.md) - Test naming
