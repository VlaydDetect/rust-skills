# async-join-parallel

> Use `join!` or `try_join!` for concurrent independent futures## Decision

Consider this rule only after its prerequisites are satisfied: Use `join!` or `try_join!` for concurrent independent futures.

## Apply When

Apply when suspension, task ownership, cancellation, backpressure, blocking work, or async runtime behavior controls correctness or liveness, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a synchronous call path is sufficient, or adopting a runtime or channel would add an unapproved dependency or protocol. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Define task ownership, suspension and cancellation points, bounds, shutdown, and observation before choosing the async primitive.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Async scales suspended I/O but introduces executor, cancellation, Send, lifetime, and observability constraints.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`tokio`, `futures`) must already be accepted by the project or be approved before addition.
- Runtime, task ownership, cancellation, capacity, blocking, and shutdown behavior must be known.

## Verification

Test success, cancellation, close, timeout, overload, and clean shutdown with bounded deterministic waits.

## Why It Matters

Awaiting futures sequentially takes the sum of their durations. `join!` runs futures concurrently, taking only as long as the slowest one. For independent operations like multiple API calls or parallel file reads, this can dramatically reduce latency.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
async fn fetch_data() -> (User, Posts, Comments) {
    // Sequential: 300ms total (100 + 100 + 100)
    let user = fetch_user().await;        // 100ms
    let posts = fetch_posts().await;      // 100ms  
    let comments = fetch_comments().await; // 100ms
    
    (user, posts, comments)
}

async fn read_configs() -> Result<(Config, Settings)> {
    // Sequential: 20ms + 20ms = 40ms
    let config = fs::read_to_string("config.toml").await?;
    let settings = fs::read_to_string("settings.json").await?;
    
    Ok((parse_config(&config)?, parse_settings(&settings)?))
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tokio::join;

async fn fetch_data() -> (User, Posts, Comments) {
    // Concurrent: ~100ms total (max of all three)
    let (user, posts, comments) = join!(
        fetch_user(),
        fetch_posts(),
        fetch_comments(),
    );
    
    (user, posts, comments)
}

use tokio::try_join;

async fn read_configs() -> Result<(Config, Settings)> {
    // Concurrent: ~20ms total
    let (config_str, settings_str) = try_join!(
        fs::read_to_string("config.toml"),
        fs::read_to_string("settings.json"),
    )?;
    
    Ok((parse_config(&config_str)?, parse_settings(&settings_str)?))
}
```

## join! vs try_join!

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the join! vs tryjoin! illustration -->
```rust
// join! - all futures run to completion, returns tuple
let (a, b, c) = join!(future_a, future_b, future_c);

// try_join! - short-circuits on first error
let (a, b, c) = try_join!(fallible_a, fallible_b, fallible_c)?;
// If fallible_b fails, returns Err immediately
// Other futures may still be running (cancellation is async)
```

## futures::join_all for Dynamic Collections

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the futures::joinall for Dynamic Collections illustration -->
```rust
use futures::future::join_all;

async fn fetch_all_users(ids: &[u64]) -> Vec<User> {
    let futures: Vec<_> = ids.iter()
        .map(|id| fetch_user(*id))
        .collect();
    
    join_all(futures).await
}

// With fallible futures
use futures::future::try_join_all;

async fn fetch_all_users(ids: &[u64]) -> Result<Vec<User>> {
    let futures: Vec<_> = ids.iter()
        .map(|id| fetch_user(*id))
        .collect();
    
    try_join_all(futures).await
}
```

## Limiting Concurrency

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Limiting Concurrency illustration -->
```rust
use futures::stream::{self, StreamExt};

async fn fetch_with_limit(ids: &[u64]) -> Vec<Result<User>> {
    stream::iter(ids)
        .map(|id| fetch_user(*id))
        .buffer_unordered(10)  // Max 10 concurrent requests
        .collect()
        .await
}

// Or with tokio::sync::Semaphore
use tokio::sync::Semaphore;

async fn fetch_with_semaphore(ids: &[u64]) -> Vec<User> {
    let semaphore = Arc::new(Semaphore::new(10));
    
    let futures: Vec<_> = ids.iter().map(|id| {
        let semaphore = semaphore.clone();
        async move {
            let _permit = semaphore.acquire().await.unwrap();
            fetch_user(*id).await
        }
    }).collect();
    
    join_all(futures).await
}
```

## When NOT to Use join!

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When NOT to Use join! illustration -->
```rust
// ❌ Dependent futures - must be sequential
async fn create_and_populate() -> Result<()> {
    let db = create_database().await?;   // Must complete first
    populate_tables(&db).await?;          // Depends on db
    Ok(())
}

// ❌ Short-circuiting logic
async fn find_first() -> Option<Data> {
    // Want to stop when one succeeds
    // Use select! instead
}

// ❌ Shared mutable state
async fn bad_shared_state() {
    let counter = Arc::new(Mutex::new(0));
    // This might work but can cause contention
    join!(
        increment(counter.clone()),
        increment(counter.clone()),
    );
}
```

## Related Rules
- [async-try-join](./async-try-join.md) - Error handling in concurrent futures
- [async-select-racing](./async-select-racing.md) - Racing futures
- [async-joinset-structured](./async-joinset-structured.md) - Dynamic task sets

## Verified Rulebook Example

<!-- rust-example: fixture; dependencies: tokio -->
```rust
#[tokio::main(flavor = "current_thread")]
async fn main() {
    let (left, right) = tokio::join!(async { 2_u8 }, async { 3_u8 });
    assert_eq!(left + right, 5);
}
```
