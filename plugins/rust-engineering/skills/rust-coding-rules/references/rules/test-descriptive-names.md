# test-descriptive-names

> Use descriptive test names that explain what is being tested

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=adapted -->

## Decision

Use this context-sensitive Rust decision when its premise is established: Use descriptive test names that explain what is being tested.

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

Test names appear in test output and serve as documentation. A good test name tells you what behavior is being verified without reading the test body. When a test fails, a descriptive name immediately tells you what broke.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
#[test]
fn test1() { ... }

#[test]
fn test_parse() { ... }  // Parse what? What behavior?

#[test]
fn it_works() { ... }

#[test]
fn test_function() { ... }

// Failure output: "test test_parse ... FAILED"
// What failed? No idea.
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[test]
fn parse_returns_error_for_empty_input() { ... }

#[test]
fn parse_handles_unicode_characters() { ... }

#[test]
fn user_creation_requires_valid_email() { ... }

#[test]
fn expired_token_is_rejected() { ... }

// Failure output: "test parse_returns_error_for_empty_input ... FAILED"
// Immediately know what broke!
```

## Naming Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Naming Patterns illustration -->
```rust
// Pattern: function_condition_expected_result
#[test]
fn parse_valid_json_returns_document() { ... }

#[test]
fn parse_invalid_json_returns_syntax_error() { ... }

// Pattern: scenario_expectation
#[test]
fn empty_cart_has_zero_total() { ... }

#[test]
fn adding_item_increases_cart_total() { ... }

// Pattern: when_given_then (BDD-style)
#[test]
fn when_user_not_found_then_returns_404() { ... }
```

## Edge Cases

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Edge Cases illustration -->
```rust
#[test]
fn handles_empty_string() { ... }

#[test]
fn handles_max_length_input() { ... }

#[test]
fn handles_unicode_emoji() { ... }

#[test]
fn handles_null_bytes() { ... }

#[test]
fn handles_concurrent_access() { ... }
```

## Error Cases

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Error Cases illustration -->
```rust
#[test]
fn rejects_negative_quantity() { ... }

#[test]
fn returns_error_for_invalid_email_format() { ... }

#[test]
fn panics_on_double_initialization() { ... }

#[test]
fn timeout_returns_timeout_error() { ... }
```

## Module Organization

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Module Organization illustration -->
```rust
#[cfg(test)]
mod tests {
    use super::*;
    
    mod parsing {
        use super::*;
        
        #[test]
        fn accepts_valid_json() { ... }
        
        #[test]
        fn rejects_trailing_comma() { ... }
    }
    
    mod validation {
        use super::*;
        
        #[test]
        fn requires_name_field() { ... }
        
        #[test]
        fn email_must_contain_at_symbol() { ... }
    }
}

// Test output:
// tests::parsing::accepts_valid_json
// tests::parsing::rejects_trailing_comma
// tests::validation::requires_name_field
```

## Related Rules
- [test-arrange-act-assert](./test-arrange-act-assert.md) - Test structure
- [test-cfg-test-module](./test-cfg-test-module.md) - Test module organization
- [doc-examples-section](./doc-examples-section.md) - Documentation tests
