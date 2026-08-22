# test-integration-dir

> Put integration tests in the `tests/` directory

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Put integration tests in the `tests/` directory.

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
- External crates referenced by the source (`tokio`) must already be accepted by the project or be approved before addition.

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

Integration tests live in `tests/` at the crate root, separate from `src/`. Each file in `tests/` is compiled as a separate crate, testing your library's public API as external users would. This separation ensures you're testing the real public interface, not implementation details.

## Structure

```
my_project/
├── Cargo.toml
├── src/
│   ├── lib.rs
│   └── internal.rs
└── tests/
    ├── integration_test.rs    # Each file is a separate test binary
    ├── api_tests.rs
    └── common/                 # Shared test utilities
        └── mod.rs
```

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// src/lib.rs
// Mixing integration test logic in library code
#[test]
fn integration_test_full_workflow() {
    // This is a unit test location, not integration
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// tests/integration_test.rs
use my_crate::{Client, Config};  // Uses public API only

#[test]
fn test_full_workflow() {
    let config = Config::default();
    let client = Client::new(config);
    
    let result = client.process("input");
    assert!(result.is_ok());
}

#[test]
fn test_error_handling() {
    let client = Client::new(Config::strict());
    
    let result = client.process("invalid");
    assert!(matches!(result, Err(Error::InvalidInput { .. })));
}
```

## Shared Test Utilities

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Shared Test Utilities illustration -->
```rust
// tests/common/mod.rs
use my_crate::Config;

pub fn test_config() -> Config {
    Config {
        timeout: Duration::from_secs(5),
        retries: 3,
        debug: true,
    }
}

pub fn setup_test_environment() {
    // Set up test fixtures
}

// tests/api_tests.rs
mod common;

use my_crate::Client;

#[test]
fn test_with_shared_config() {
    common::setup_test_environment();
    let client = Client::new(common::test_config());
    // ...
}
```

## Organizing Many Tests

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Organizing Many Tests illustration -->
```rust
// tests/api/mod.rs
mod auth;
mod users;
mod orders;

// tests/api/auth.rs
use my_crate::auth::{login, logout};

#[test]
fn test_login_success() { ... }

#[test]
fn test_login_invalid_credentials() { ... }

// tests/api/users.rs
use my_crate::users::{create_user, get_user};

#[test]
fn test_create_user() { ... }
```

## Integration vs Unit Tests

| Unit Tests | Integration Tests |
|------------|-------------------|
| In `src/` with `#[cfg(test)]` | In `tests/` directory |
| Access private items | Public API only |
| Test individual functions | Test module interactions |
| Fast, isolated | May be slower |
| `cargo test --lib` | `cargo test --test '*'` |

## Running Specific Tests

```bash
# Run all tests
cargo test

# Run only integration tests
cargo test --test '*'

# Run specific integration test file
cargo test --test integration_test

# Run tests matching pattern
cargo test --test api_tests test_login
```

## Related Rules
- [test-cfg-test-module](./test-cfg-test-module.md) - Unit test modules
- [test-descriptive-names](./test-descriptive-names.md) - Test naming
- [test-tokio-async](./test-tokio-async.md) - Async integration tests
