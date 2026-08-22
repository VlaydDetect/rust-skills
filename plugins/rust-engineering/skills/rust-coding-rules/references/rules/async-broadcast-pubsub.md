# async-broadcast-pubsub

> Use `broadcast` channel for pub/sub where all subscribers receive all messages

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-concurrency; supporters=`rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `broadcast` channel for pub/sub where all subscribers receive all messages.

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
- External crates referenced by the source (`tokio`, `log`) must already be accepted by the project or be approved before addition.
- Runtime, task ownership, cancellation, capacity, blocking, and shutdown behavior must be known.

## Verification

Test success, cancellation, close, timeout, overload, and clean shutdown with bounded deterministic waits.

## Why It Matters

Unlike `mpsc` where one consumer receives each message, `broadcast` delivers each message to all subscribers. This is ideal for event broadcasting, real-time notifications, or when multiple components need to react to the same events independently.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
use tokio::sync::mpsc;

// mpsc only delivers to ONE consumer
let (tx, mut rx) = mpsc::channel::<Event>(100);

// Only one of these receives each message!
let mut rx2 = ???;  // Can't clone receiver
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tokio::sync::broadcast;

// broadcast delivers to ALL subscribers
let (tx, _) = broadcast::channel::<Event>(100);

// Each subscriber gets ALL messages
let mut rx1 = tx.subscribe();
let mut rx2 = tx.subscribe();

tokio::spawn(async move {
    while let Ok(event) = rx1.recv().await {
        handle_in_logger(event);
    }
});

tokio::spawn(async move {
    while let Ok(event) = rx2.recv().await {
        handle_in_metrics(event);
    }
});

// Both subscribers receive this
tx.send(Event::UserLogin { user_id: 42 })?;
```

## Broadcast Semantics

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Broadcast Semantics illustration -->
```rust
use tokio::sync::broadcast;

let (tx, mut rx1) = broadcast::channel::<i32>(16);
let mut rx2 = tx.subscribe();

tx.send(1)?;
tx.send(2)?;

// Both receive all messages
assert_eq!(rx1.recv().await?, 1);
assert_eq!(rx1.recv().await?, 2);
assert_eq!(rx2.recv().await?, 1);
assert_eq!(rx2.recv().await?, 2);
```

## Handling Lagging Receivers

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Handling Lagging Receivers illustration -->
```rust
use tokio::sync::broadcast::{self, error::RecvError};

let (tx, mut rx) = broadcast::channel::<Event>(16);

loop {
    match rx.recv().await {
        Ok(event) => {
            process(event);
        }
        Err(RecvError::Lagged(count)) => {
            // Receiver couldn't keep up, missed `count` messages
            log::warn!("Missed {} events", count);
            // Continue receiving new messages
        }
        Err(RecvError::Closed) => {
            break;  // All senders dropped
        }
    }
}
```

## Event Bus Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Event Bus Pattern illustration -->
```rust
use tokio::sync::broadcast;

#[derive(Clone, Debug)]
enum AppEvent {
    UserLoggedIn { user_id: u64 },
    OrderCreated { order_id: u64 },
    SystemShutdown,
}

struct EventBus {
    tx: broadcast::Sender<AppEvent>,
}

impl EventBus {
    fn new() -> Self {
        let (tx, _) = broadcast::channel(1000);
        EventBus { tx }
    }
    
    fn publish(&self, event: AppEvent) {
        // Ignore error if no subscribers
        let _ = self.tx.send(event);
    }
    
    fn subscribe(&self) -> broadcast::Receiver<AppEvent> {
        self.tx.subscribe()
    }
}

// Usage
let bus = EventBus::new();

// Logger subscribes
let mut log_rx = bus.subscribe();
tokio::spawn(async move {
    while let Ok(event) = log_rx.recv().await {
        log::info!("Event: {:?}", event);
    }
});

// Metrics subscribes
let mut metrics_rx = bus.subscribe();
tokio::spawn(async move {
    while let Ok(event) = metrics_rx.recv().await {
        record_metric(&event);
    }
});

// Publish events
bus.publish(AppEvent::UserLoggedIn { user_id: 42 });
```

## Broadcast vs Watch

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Broadcast vs Watch illustration -->
```rust
// broadcast: subscribers get ALL messages
// Good for: events, logs, notifications
let (tx, _) = broadcast::channel::<Event>(100);

// watch: subscribers get LATEST value only
// Good for: config changes, state updates
let (tx, _) = watch::channel(initial_state);

// If subscriber is slow:
// - broadcast: they receive old messages (or lag)
// - watch: they skip to latest (no history)
```

## Clone Requirement

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Clone Requirement illustration -->
```rust
// broadcast requires Clone because message is cloned to each receiver
use tokio::sync::broadcast;

#[derive(Clone)]  // Required for broadcast
struct Event {
    data: String,
}

let (tx, _) = broadcast::channel::<Event>(100);

// For non-Clone types, wrap in Arc
use std::sync::Arc;

let (tx, _) = broadcast::channel::<Arc<LargeNonClone>>(100);
```

## Related Rules
- [async-mpsc-queue](./async-mpsc-queue.md) - Single-consumer channels
- [async-watch-latest](./async-watch-latest.md) - Latest-value only
- [async-bounded-channel](./async-bounded-channel.md) - Buffer sizing
