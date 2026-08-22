# async-tokio-runtime

> Configure Tokio runtime appropriately for your workload

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-concurrency; supporters=`rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Configure Tokio runtime appropriately for your workload.

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

Tokio's default multi-threaded runtime isn't always optimal. CPU-bound work needs different configuration than IO-bound work. Incorrect configuration leads to poor performance, blocked workers, or resource exhaustion. Understanding runtime options lets you tune for your specific use case.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Default runtime for everything - not optimal
#[tokio::main]
async fn main() {
    // CPU-heavy work on async executor starves IO tasks
    for data in datasets {
        let result = heavy_computation(data).await;
    }
}

// Single-threaded when multi-threaded is needed
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // Can't utilize multiple cores for concurrent tasks
    for _ in 0..1000 {
        tokio::spawn(async { /* IO work */ });
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Multi-threaded for concurrent IO (default)
#[tokio::main]
async fn main() {
    // Good for many concurrent network connections
    let handles: Vec<_> = urls.iter()
        .map(|url| tokio::spawn(fetch(url.clone())))
        .collect();
    
    futures::future::join_all(handles).await;
}

// Current-thread for single-threaded scenarios
#[tokio::main(flavor = "current_thread")]
async fn main() {
    // Good for single-connection clients, simpler debugging
    let client = Client::new();
    client.run().await;
}

// Custom configuration
#[tokio::main(worker_threads = 4)]
async fn main() {
    // Limit to 4 worker threads
}

// Or manual setup for more control
fn main() {
    let runtime = tokio::runtime::Builder::new_multi_thread()
        .worker_threads(4)
        .enable_all()
        .thread_name("my-worker")
        .build()
        .unwrap();
    
    runtime.block_on(async_main());
}
```

## Runtime Types

| Runtime | Use Case | Configuration |
|---------|----------|---------------|
| Multi-thread | IO-bound, many connections | `#[tokio::main]` (default) |
| Current-thread | CLI tools, tests, single connection | `flavor = "current_thread"` |
| Custom | Fine-tuned performance | `Builder::new_*()` |

## Worker Thread Tuning

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Worker Thread Tuning illustration -->
```rust
use tokio::runtime::Builder;

// std::thread::available_parallelism() is stable since Rust 1.59
// and respects cgroup CPU quotas (unlike the unmaintained num_cpus crate)
let parallelism = std::thread::available_parallelism()
    .map(|n| n.get())
    .unwrap_or(1);

// IO-bound: more threads than cores can help
let io_runtime = Builder::new_multi_thread()
    .worker_threads(parallelism * 2)  // IO can benefit from oversubscription
    .max_blocking_threads(32)         // For spawn_blocking calls
    .enable_io()
    .enable_time()
    .build()?;

// CPU-bound: match core count
let cpu_runtime = Builder::new_multi_thread()
    .worker_threads(parallelism)      // No benefit from more than cores
    .build()?;
```

## Multiple Runtimes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Multiple Runtimes illustration -->
```rust
// Separate runtimes for different workloads
struct App {
    io_runtime: Runtime,
    cpu_runtime: Runtime,
}

impl App {
    fn new() -> Self {
        Self {
            io_runtime: Builder::new_multi_thread()
                .worker_threads(8)
                .thread_name("io-worker")
                .build()
                .unwrap(),
            cpu_runtime: Builder::new_multi_thread()
                .worker_threads(4)
                .thread_name("cpu-worker")
                .build()
                .unwrap(),
        }
    }
    
    fn spawn_io<F>(&self, future: F) 
    where F: Future + Send + 'static, F::Output: Send + 'static 
    {
        self.io_runtime.spawn(future);
    }
    
    fn spawn_cpu<F>(&self, task: F) 
    where F: FnOnce() + Send + 'static 
    {
        self.cpu_runtime.spawn_blocking(task);
    }
}
```

## Runtime in Tests

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Runtime in Tests illustration -->
```rust
// Single test runtime
#[tokio::test]
async fn test_single() {
    assert!(true);
}

// Multi-threaded test
#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn test_concurrent() {
    let (tx, rx) = tokio::sync::oneshot::channel();
    tokio::spawn(async move { tx.send(42).unwrap() });
    assert_eq!(rx.await.unwrap(), 42);
}

// Custom runtime in test
#[test]
fn test_with_custom_runtime() {
    let rt = Builder::new_current_thread().build().unwrap();
    rt.block_on(async {
        // test code
    });
}
```

## Related Rules
- [async-spawn-blocking](./async-spawn-blocking.md) - Handling blocking code
- [async-no-lock-await](./async-no-lock-await.md) - Avoiding lock issues
- [async-joinset-structured](./async-joinset-structured.md) - Managing spawned tasks
