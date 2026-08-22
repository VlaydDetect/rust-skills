# async-bounded-channel

> Use bounded channels to apply backpressure and prevent unbounded memory growth

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-concurrency; supporters=`rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use bounded channels to apply backpressure and prevent unbounded memory growth.

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

Unbounded channels grow without limit when producers outpace consumers. In production, this leads to memory exhaustion. Bounded channels apply backpressure—producers wait when the channel is full, naturally throttling the system. This prevents OOM and makes resource usage predictable.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use tokio::sync::mpsc;

// Unbounded channel - can grow forever
let (tx, mut rx) = mpsc::unbounded_channel::<Message>();

// Fast producer, slow consumer = unbounded memory growth
tokio::spawn(async move {
    loop {
        let msg = generate_message();
        tx.send(msg).unwrap();  // Never blocks, never fails (until OOM)
    }
});

tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        slow_process(msg).await;  // Can't keep up
    }
});
// Memory grows unboundedly until crash
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tokio::sync::mpsc;

// Bounded channel - backpressure when full
let (tx, mut rx) = mpsc::channel::<Message>(100);  // Max 100 items

// Producer waits when channel full
tokio::spawn(async move {
    loop {
        let msg = generate_message();
        // Blocks if channel is full - natural backpressure
        tx.send(msg).await.unwrap();
    }
});

tokio::spawn(async move {
    while let Some(msg) = rx.recv().await {
        slow_process(msg).await;
    }
});
// Memory usage capped at ~100 messages
```

## Choosing Buffer Size

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Choosing Buffer Size illustration -->
```rust
// Too small: frequent blocking, reduced throughput
let (tx, rx) = mpsc::channel::<Item>(1);

// Too large: delayed backpressure, memory waste
let (tx, rx) = mpsc::channel::<Item>(1_000_000);

// Guidelines:
// - Start with expected burst size
// - Measure actual usage in production
// - Err on the smaller side initially

// Small items, high throughput
let (tx, rx) = mpsc::channel::<u64>(1000);

// Large items, moderate throughput  
let (tx, rx) = mpsc::channel::<LargeStruct>(100);

// Low latency requirement
let (tx, rx) = mpsc::channel::<Command>(10);
```

## Handling Full Channel

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Handling Full Channel illustration -->
```rust
use tokio::sync::mpsc;
use tokio::time::{timeout, Duration};

let (tx, mut rx) = mpsc::channel::<Message>(100);

// Option 1: Wait indefinitely (default)
tx.send(msg).await?;

// Option 2: Try send, fail if full
match tx.try_send(msg) {
    Ok(()) => println!("Sent"),
    Err(TrySendError::Full(msg)) => {
        println!("Channel full, dropping message");
    }
    Err(TrySendError::Closed(msg)) => {
        println!("Receiver dropped");
    }
}

// Option 3: Timeout
match timeout(Duration::from_secs(1), tx.send(msg)).await {
    Ok(Ok(())) => println!("Sent"),
    Ok(Err(_)) => println!("Channel closed"),
    Err(_) => println!("Timeout - channel full for too long"),
}

// Option 4: send with permit reservation
let permit = tx.reserve().await?;
permit.send(msg);  // Guaranteed to succeed
```

## Channel Types

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Channel Types illustration -->
```rust
// mpsc: many producers, single consumer
let (tx, rx) = mpsc::channel::<Message>(100);
let tx2 = tx.clone();  // Can clone sender

// oneshot: single value, one producer, one consumer
let (tx, rx) = oneshot::channel::<Response>();
tx.send(response);  // Can only send once

// broadcast: multiple consumers, each gets all messages
let (tx, _) = broadcast::channel::<Event>(100);
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

// watch: single latest value, multiple consumers
let (tx, rx) = watch::channel::<State>(initial);
// Receivers see latest value, not all values
```

## Worker Pool Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Worker Pool Pattern illustration -->
```rust
async fn process_with_workers(items: Vec<Item>) -> Vec<Result> {
    let (tx, rx) = mpsc::channel(100);
    let rx = Arc::new(Mutex::new(rx));
    
    // Spawn worker pool
    let workers: Vec<_> = (0..4).map(|_| {
        let rx = rx.clone();
        tokio::spawn(async move {
            loop {
                let item = {
                    let mut rx = rx.lock().await;
                    rx.recv().await
                };
                match item {
                    Some(item) => process(item).await,
                    None => break,
                }
            }
        })
    }).collect();
    
    // Send items
    for item in items {
        tx.send(item).await.unwrap();
    }
    drop(tx);  // Signal workers to stop
    
    futures::future::join_all(workers).await;
}
```

## Related Rules
- [async-mpsc-queue](./async-mpsc-queue.md) - Multi-producer patterns
- [async-oneshot-response](./async-oneshot-response.md) - Request-response pattern
- [async-watch-latest](./async-watch-latest.md) - Latest-value broadcasting
