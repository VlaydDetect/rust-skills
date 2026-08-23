# Async and Await

Prefix: `async-` · 18 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when suspension, task ownership, cancellation, backpressure, blocking work, or async runtime behavior controls correctness or liveness.
- Defer when a synchronous call path is sufficient, or adopting a runtime or channel would add an unapproved dependency or protocol.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`async-async-fn-bounds`](../rules/async-async-fn-bounds.md) | `conditional` | `rust-concurrency` | Use `AsyncFn`/`AsyncFnMut`/`AsyncFnOnce` bounds instead of `F: Fn() -> Fut, Fut: Future` |
| [`async-bounded-channel`](../rules/async-bounded-channel.md) | `conditional` | `rust-concurrency` | Use bounded channels to apply backpressure and prevent unbounded memory growth |
| [`async-broadcast-pubsub`](../rules/async-broadcast-pubsub.md) | `conditional` | `rust-concurrency` | Use `broadcast` channel for pub/sub where all subscribers receive all messages |
| [`async-cancel-safety`](../rules/async-cancel-safety.md) | `conditional` | `rust-concurrency` | Ensure futures used in `tokio::select!` branches are cancellation-safe |
| [`async-cancellation-token`](../rules/async-cancellation-token.md) | `conditional` | `rust-concurrency` | Use `CancellationToken` for graceful shutdown and task cancellation |
| [`async-clone-before-await`](../rules/async-clone-before-await.md) | `conditional` | `rust-concurrency` | Clone Arc/Rc data before await points to avoid holding references across suspension |
| [`async-fn-in-trait`](../rules/async-fn-in-trait.md) | `conditional` | `rust-concurrency` | Use native `async fn` in traits (stable 1.75) instead of the `async_trait` macro |
| [`async-join-parallel`](../rules/async-join-parallel.md) | `conditional` | `rust-concurrency` | Use `join!` or `try_join!` for concurrent independent futures |
| [`async-joinset-structured`](../rules/async-joinset-structured.md) | `conditional` | `rust-concurrency` | Use `JoinSet` for managing dynamic collections of spawned tasks |
| [`async-mpsc-queue`](../rules/async-mpsc-queue.md) | `conditional` | `rust-concurrency` | Use `mpsc` channels for async message queues between tasks |
| [`async-no-lock-await`](../rules/async-no-lock-await.md) | `conditional` | `rust-concurrency` | Never hold `Mutex`/`RwLock` across `.await` |
| [`async-oneshot-response`](../rules/async-oneshot-response.md) | `conditional` | `rust-concurrency` | Use `oneshot` channel for request-response patterns |
| [`async-select-racing`](../rules/async-select-racing.md) | `conditional` | `rust-concurrency` | Use `select!` to race futures and handle the first to complete |
| [`async-spawn-blocking`](../rules/async-spawn-blocking.md) | `conditional` | `rust-concurrency` | Use `spawn_blocking` for CPU-intensive work |
| [`async-tokio-fs`](../rules/async-tokio-fs.md) | `conditional` | `rust-concurrency` | Use `tokio::fs` instead of `std::fs` in async code |
| [`async-tokio-runtime`](../rules/async-tokio-runtime.md) | `conditional` | `rust-concurrency` | Configure Tokio runtime appropriately for your workload |
| [`async-try-join`](../rules/async-try-join.md) | `conditional` | `rust-concurrency` | Use `try_join!` for concurrent fallible operations with early return on error |
| [`async-watch-latest`](../rules/async-watch-latest.md) | `conditional` | `rust-concurrency` | Use `watch` channel for sharing the latest value with multiple observers |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
