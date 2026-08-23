# async-clone-before-await

> Clone Arc/Rc data before await points to avoid holding references across suspension## Decision

Consider this rule only after its prerequisites are satisfied: Clone Arc/Rc data before await points to avoid holding references across suspension.

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

References held across `.await` points extend the future's lifetime and can cause borrow checker issues or prevent `Send` bounds. Cloning `Arc`/`Rc` before the await ensures the future only holds owned data, making it `Send` and avoiding lifetime complications.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use std::sync::Arc;

async fn process(data: Arc<Data>) {
    // Borrow extends across await - future is not Send
    let slice = &data.items[..];  // Borrow of Arc contents
    
    expensive_async_operation().await;  // Await with active borrow
    
    use_slice(slice);  // Still using the borrow
}

// Error: future cannot be sent between threads safely
// because `&[Item]` cannot be sent between threads safely
tokio::spawn(process(data));
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use std::sync::Arc;

async fn process(data: Arc<Data>) {
    // Clone what you need before await
    let items = data.items.clone();  // Owned Vec
    
    expensive_async_operation().await;
    
    use_items(&items);  // Using owned data
}

// Or clone the Arc itself
async fn share_data(data: Arc<Data>) {
    let data = data.clone();  // Another Arc handle
    
    some_async_work().await;
    
    process(&data);  // Safe - we own the Arc
}
```

## The Send Problem

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the The Send Problem illustration -->
```rust
// Futures must be Send to spawn on multi-threaded runtime
async fn not_send() {
    let rc = Rc::new(42);  // Rc is !Send
    
    tokio::time::sleep(Duration::from_secs(1)).await;
    
    println!("{}", rc);  // rc held across await
}

tokio::spawn(not_send());  // ERROR: future is not Send

// Fix: use Arc or don't hold across await
async fn is_send() {
    let arc = Arc::new(42);  // Arc is Send
    
    tokio::time::sleep(Duration::from_secs(1)).await;
    
    println!("{}", arc);
}

tokio::spawn(is_send());  // OK
```

## Minimizing Clones

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Minimizing Clones illustration -->
```rust
// Bad: clone everything eagerly
async fn wasteful(data: Arc<LargeData>) {
    let data = (*data).clone();  // Clones entire LargeData
    async_work().await;
    use_one_field(&data.small_field);
}

// Good: clone only what you need
async fn efficient(data: Arc<LargeData>) {
    let small = data.small_field.clone();  // Clone only needed field
    async_work().await;
    use_one_field(&small);
}

// Good: if you need the whole thing, keep the Arc
async fn arc_efficient(data: Arc<LargeData>) {
    let data = data.clone();  // Cheap Arc clone
    async_work().await;
    use_data(&data);  // Access through Arc
}
```

## Spawn Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Spawn Pattern illustration -->
```rust
// Common pattern: clone for spawned task
let shared = Arc::new(SharedState::new());

for i in 0..10 {
    let shared = shared.clone();  // Clone before moving into spawn
    tokio::spawn(async move {
        // Task owns its Arc clone
        shared.do_something(i).await;
    });
}
```

## Scope-Based Approach

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Scope-Based Approach illustration -->
```rust
// Limit borrow scope to before await
async fn scoped(data: Arc<Data>) {
    // Scope 1: borrow, compute, drop borrow
    let computed = {
        let slice = &data.items[..];  // Borrow
        compute_something(slice)       // Use
    };  // Borrow ends here
    
    // Now safe to await
    expensive_async_operation().await;
    
    use_computed(computed);
}
```

## MutexGuard Across Await

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the MutexGuard Across Await illustration -->
```rust
use tokio::sync::Mutex;

// BAD: holding guard across await
async fn bad(mutex: Arc<Mutex<Data>>) {
    let mut guard = mutex.lock().await;
    guard.value += 1;
    
    slow_operation().await;  // Guard held during await!
    
    guard.value += 1;
}

// GOOD: release before await
async fn good(mutex: Arc<Mutex<Data>>) {
    {
        let mut guard = mutex.lock().await;
        guard.value += 1;
    }  // Guard released
    
    slow_operation().await;
    
    {
        let mut guard = mutex.lock().await;
        guard.value += 1;
    }
}
```

## Related Rules
- [async-no-lock-await](./async-no-lock-await.md) - Lock guards across await
- [own-arc-shared](./own-arc-shared.md) - Arc usage patterns
- [async-spawn-blocking](./async-spawn-blocking.md) - Blocking in async
