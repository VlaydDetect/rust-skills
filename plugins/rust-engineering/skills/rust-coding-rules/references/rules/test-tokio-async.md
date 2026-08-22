# test-tokio-async

> Use `#[tokio::test]` for async tests

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-testing; supporters=`rust-verify`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `#[tokio::test]` for async tests.

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
- External crates referenced by the source (`tokio`, `mockall`) must already be accepted by the project or be approved before addition.

## Verification

Run the exact new test and its owning package or target, then record required features, runtime, seed, environment, and residual matrix.

## Why It Matters

Async functions can't be called directly—they need a runtime to drive them. `#[tokio::test]` provides a Tokio runtime for your test, handling setup automatically. This is simpler than manually creating a runtime and essential for testing async code.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Won't compile - async fn can't be called without runtime
#[test]
async fn test_async_function() {  // Error!
    let result = fetch_data().await;
    assert!(result.is_ok());
}

// Manual runtime - verbose and error-prone
#[test]
fn test_async_function() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        let result = fetch_data().await;
        assert!(result.is_ok());
    });
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[tokio::test]
async fn test_async_function() {
    let result = fetch_data().await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_concurrent_operations() {
    let (a, b) = tokio::join!(
        fetch_user(1),
        fetch_user(2),
    );
    assert!(a.is_ok());
    assert!(b.is_ok());
}
```

## Runtime Configuration

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Runtime Configuration illustration -->
```rust
// Multi-threaded runtime (default)
#[tokio::test]
async fn test_default_runtime() {
    // Uses multi-thread runtime
}

// Single-threaded (current_thread)
#[tokio::test(flavor = "current_thread")]
async fn test_single_threaded() {
    // Simpler, deterministic
}

// With specific thread count
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_with_workers() {
    // Exactly 2 worker threads
}

// With time control
#[tokio::test(start_paused = true)]
async fn test_with_time_control() {
    // Time starts paused for deterministic testing
    tokio::time::advance(Duration::from_secs(60)).await;
}
```

## Testing Timeouts

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Testing Timeouts illustration -->
```rust
use tokio::time::{timeout, Duration};

#[tokio::test]
async fn test_operation_completes_in_time() {
    let result = timeout(
        Duration::from_secs(5),
        slow_operation()
    ).await;
    
    assert!(result.is_ok(), "Operation timed out");
}

#[tokio::test]
async fn test_timeout_triggers() {
    let result = timeout(
        Duration::from_millis(100),
        never_completes()
    ).await;
    
    assert!(result.is_err(), "Expected timeout");
}
```

## Testing Channels

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Testing Channels illustration -->
```rust
use tokio::sync::mpsc;

#[tokio::test]
async fn test_channel_communication() {
    let (tx, mut rx) = mpsc::channel(10);
    
    tokio::spawn(async move {
        tx.send("hello").await.unwrap();
        tx.send("world").await.unwrap();
    });
    
    assert_eq!(rx.recv().await, Some("hello"));
    assert_eq!(rx.recv().await, Some("world"));
    assert_eq!(rx.recv().await, None);
}
```

## Testing with Mocks

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Testing with Mocks illustration -->
```rust
use mockall::*;

#[automock]
#[async_trait::async_trait]
trait Database {
    async fn get_user(&self, id: u64) -> Option<User>;
}

#[tokio::test]
async fn test_with_mock_database() {
    let mut mock = MockDatabase::new();
    mock.expect_get_user()
        .with(eq(42))
        .returning(|_| Some(User { id: 42, name: "Alice".into() }));
    
    let service = UserService::new(mock);
    let user = service.find_user(42).await;
    
    assert_eq!(user.unwrap().name, "Alice");
}
```

## Related Rules
- [async-tokio-runtime](./async-tokio-runtime.md) - Runtime configuration
- [test-mock-traits](./test-mock-traits.md) - Mocking async traits
- [test-fixture-raii](./test-fixture-raii.md) - Async test cleanup
