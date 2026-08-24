# Testing

Prefix: `test-` · 15 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a concrete contract or risk needs the cheapest deterministic test that would fail for the defect.
- Defer when the technique duplicates lower-cost coverage or adds a framework, snapshot, mock, sleep, or fuzz harness without unique risk coverage.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`test-arrange-act-assert`](../rules/test-arrange-act-assert.md) | `conditional` | `rust-testing` | Structure tests with clear Arrange, Act, Assert sections |
| [`test-cfg-test-module`](../rules/test-cfg-test-module.md) | `canonical` | `rust-testing` | Put unit tests in `#[cfg(test)] mod tests { }` within each module |
| [`test-criterion-bench`](../rules/test-criterion-bench.md) | `conditional` | `rust-testing` | Use `criterion` for benchmarking |
| [`test-descriptive-names`](../rules/test-descriptive-names.md) | `canonical` | `rust-testing` | Use descriptive test names that explain what is being tested |
| [`test-doctest-examples`](../rules/test-doctest-examples.md) | `conditional` | `rust-testing` | Keep documentation examples as executable doctests |
| [`test-fixture-raii`](../rules/test-fixture-raii.md) | `conditional` | `rust-testing` | Use RAII pattern (Drop trait) for automatic test cleanup |
| [`test-integration-dir`](../rules/test-integration-dir.md) | `conditional` | `rust-testing` | Put integration tests in the `tests/` directory |
| [`test-loom-concurrency`](../rules/test-loom-concurrency.md) | `conditional` | `rust-testing` | Use `loom` to exhaustively test lock-free and concurrent code |
| [`test-mock-traits`](../rules/test-mock-traits.md) | `conditional` | `rust-testing` | Use traits for dependencies to enable mocking in tests |
| [`test-mockall-mocking`](../rules/test-mockall-mocking.md) | `conditional` | `rust-testing` | Use mockall for trait mocking |
| [`test-proptest-properties`](../rules/test-proptest-properties.md) | `conditional` | `rust-testing` | Use proptest for property-based testing |
| [`test-should-panic`](../rules/test-should-panic.md) | `canonical` | `rust-testing` | Use `#[should_panic]` to test that code panics as expected |
| [`test-snapshot-testing`](../rules/test-snapshot-testing.md) | `conditional` | `rust-testing` | Use snapshot testing (insta) for complex or serialized output |
| [`test-tokio-async`](../rules/test-tokio-async.md) | `conditional` | `rust-testing` | Use `#[tokio::test]` for async tests |
| [`test-use-super`](../rules/test-use-super.md) | `conditional` | `rust-testing` | Use `use super::*;` in test modules to access parent module items |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
