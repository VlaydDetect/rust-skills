# async-select-racing

> Use `select!` to race futures and handle the first to complete

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-concurrency; supporters=`rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `select!` to race futures and handle the first to complete.

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

Sometimes you need the first result from multiple futures—timeout vs operation, cancellation vs work, or competing alternatives. `tokio::select!` lets you race futures and handle whichever completes first, while properly cancelling the others.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Can't express "whichever finishes first"
async fn fetch_with_fallback() -> Data {
    match fetch_primary().await {
        Ok(data) => data,
        Err(_) => fetch_fallback().await.unwrap(),  // Sequential, not racing
    }
}

// Manual timeout is error-prone
async fn fetch_with_timeout() -> Option<Data> {
    let start = Instant::now();
    loop {
        if start.elapsed() > Duration::from_secs(5) {
            return None;
        }
        // How do we check timeout while awaiting?
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tokio::select;

async fn fetch_with_timeout() -> Result<Data, Error> {
    select! {
        result = fetch_data() => result,
        _ = tokio::time::sleep(Duration::from_secs(5)) => {
            Err(Error::Timeout)
        }
    }
}

async fn fetch_with_fallback() -> Data {
    select! {
        result = fetch_primary() => {
            match result {
                Ok(data) => data,
                Err(_) => fetch_fallback().await.unwrap()
            }
        }
        _ = tokio::time::sleep(Duration::from_secs(1)) => {
            // Primary too slow, use fallback
            fetch_fallback().await.unwrap()
        }
    }
}
```

## select! Syntax

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the select! Syntax illustration -->
```rust
select! {
    // Pattern = future => handler
    result = async_operation() => {
        // Handle result
        println!("Got: {:?}", result);
    }
    
    // Can bind with pattern matching
    Ok(data) = fallible_operation() => {
        process(data);
    }
    
    // Conditional branches with if guards
    msg = channel.recv(), if should_receive => {
        handle_message(msg);
    }
    
    // else branch for when all futures are disabled
    else => {
        println!("All branches disabled");
    }
}
```

## Cancellation Behavior

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Cancellation Behavior illustration -->
```rust
async fn select_example() {
    select! {
        _ = operation_a() => {
            println!("A completed first");
            // operation_b() is dropped/cancelled
        }
        _ = operation_b() => {
            println!("B completed first");
            // operation_a() is dropped/cancelled
        }
    }
}

// Futures are cancelled at their next .await point
// For immediate cancellation, futures must be cancel-safe
```

## Biased Selection

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Biased Selection illustration -->
```rust
// By default, select! randomly picks when multiple are ready
// Use biased mode for deterministic priority
select! {
    biased;  // Check branches in order
    
    msg = high_priority.recv() => handle_high(msg),
    msg = low_priority.recv() => handle_low(msg),
}

// Without biased, both channels have equal chance
// when both have messages ready
```

## Loop with select!

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Loop with select! illustration -->
```rust
async fn event_loop(
    mut commands: mpsc::Receiver<Command>,
    shutdown: CancellationToken,
) {
    loop {
        select! {
            _ = shutdown.cancelled() => {
                println!("Shutting down");
                break;
            }
            Some(cmd) = commands.recv() => {
                process_command(cmd).await;
            }
            else => {
                // commands channel closed
                break;
            }
        }
    }
}
```

## Racing Multiple of Same Type

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Racing Multiple of Same Type illustration -->
```rust
// Race multiple servers for fastest response
async fn fastest_response(servers: &[String]) -> Result<Response> {
    let futures = servers.iter()
        .map(|s| fetch_from(s))
        .collect::<Vec<_>>();
    
    // select! requires static branches, use select_all for dynamic
    let (result, _index, _remaining) = 
        futures::future::select_all(futures).await;
    
    result
}
```

## Common Patterns

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Common Patterns illustration -->
```rust
// Timeout
select! {
    result = operation() => result,
    _ = sleep(Duration::from_secs(5)) => Err(Timeout),
}

// Cancellation
select! {
    result = operation() => result,
    _ = cancel_token.cancelled() => Err(Cancelled),
}

// Interval with cancellation
let mut interval = tokio::time::interval(Duration::from_secs(1));
loop {
    select! {
        _ = shutdown.cancelled() => break,
        _ = interval.tick() => {
            do_periodic_work().await;
        }
    }
}
```

## Related Rules
- [async-cancellation-token](./async-cancellation-token.md) - Cancellation patterns
- [async-join-parallel](./async-join-parallel.md) - All futures, not racing
- [async-bounded-channel](./async-bounded-channel.md) - Channel operations in select
