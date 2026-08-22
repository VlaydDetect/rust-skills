# async-spawn-blocking

> Use `spawn_blocking` for CPU-intensive work

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-concurrency; supporters=`rust-ownership`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use `spawn_blocking` for CPU-intensive work.

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
- External crates referenced by the source (`tokio`, `serde_json`, `rayon`) must already be accepted by the project or be approved before addition.
- Runtime, task ownership, cancellation, capacity, blocking, and shutdown behavior must be known.

## Verification

Test success, cancellation, close, timeout, overload, and clean shutdown with bounded deterministic waits.

## Why It Matters

Async runtimes like Tokio use a small number of threads to handle many tasks. CPU-intensive or blocking operations on these threads starve other tasks. `spawn_blocking` moves such work to a dedicated thread pool.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// BAD: Blocks the async runtime thread
async fn process_image(data: &[u8]) -> ProcessedImage {
    // CPU-intensive work on async thread!
    let resized = resize_image(data);      // Blocks!
    let compressed = compress(resized);     // Blocks!
    compressed
}

// BAD: Synchronous file I/O in async context
async fn read_large_file(path: &Path) -> Vec<u8> {
    std::fs::read(path).unwrap()  // Blocks the runtime!
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
use tokio::task;

// GOOD: Offload CPU work to blocking pool
async fn process_image(data: Vec<u8>) -> ProcessedImage {
    task::spawn_blocking(move || {
        let resized = resize_image(&data);
        compress(resized)
    })
    .await
    .expect("spawn_blocking failed")
}

// GOOD: Use async file I/O
async fn read_large_file(path: &Path) -> tokio::io::Result<Vec<u8>> {
    tokio::fs::read(path).await
}

// GOOD: Or spawn_blocking for unavoidable sync I/O
async fn read_with_sync_lib(path: PathBuf) -> Vec<u8> {
    task::spawn_blocking(move || {
        sync_library::read_file(&path)
    })
    .await
    .unwrap()
}
```

## What Counts as Blocking

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the What Counts as Blocking illustration -->
```rust
// CPU-intensive operations
- Cryptographic operations (hashing, encryption)
- Image/video processing
- Compression/decompression
- Complex parsing
- Mathematical computations

// Blocking I/O
- std::fs operations
- Synchronous database drivers
- Synchronous HTTP clients
- Thread::sleep

// Example thresholds (rough guidelines):
// < 10µs: OK on async thread
// 10µs - 1ms: Consider spawn_blocking
// > 1ms: Definitely spawn_blocking
```

## Practical Examples

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Practical Examples illustration -->
```rust
// Password hashing (CPU-intensive)
async fn hash_password(password: String) -> String {
    task::spawn_blocking(move || {
        bcrypt::hash(password, bcrypt::DEFAULT_COST).unwrap()
    })
    .await
    .unwrap()
}

// JSON parsing of large documents
async fn parse_large_json(data: String) -> serde_json::Value {
    task::spawn_blocking(move || {
        serde_json::from_str(&data).unwrap()
    })
    .await
    .unwrap()
}

// Compression
async fn compress_data(data: Vec<u8>) -> Vec<u8> {
    task::spawn_blocking(move || {
        let mut encoder = flate2::write::GzEncoder::new(
            Vec::new(),
            flate2::Compression::default(),
        );
        encoder.write_all(&data).unwrap();
        encoder.finish().unwrap()
    })
    .await
    .unwrap()
}
```

## spawn_blocking vs spawn

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the spawnblocking vs spawn illustration -->
```rust
// spawn: Runs async code on runtime threads
tokio::spawn(async {
    // Async code here
    some_async_operation().await;
});

// spawn_blocking: Runs sync code on blocking thread pool
tokio::task::spawn_blocking(|| {
    // Synchronous, possibly CPU-intensive code
    heavy_computation();
});

// spawn_blocking returns JoinHandle that can be awaited
let result = tokio::task::spawn_blocking(|| {
    expensive_sync_operation()
}).await?;
```

## Rayon for Parallel CPU Work

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Rayon for Parallel CPU Work illustration -->
```rust
// For parallel CPU work, consider Rayon inside spawn_blocking
async fn parallel_process(items: Vec<Item>) -> Vec<Output> {
    task::spawn_blocking(move || {
        use rayon::prelude::*;
        items.par_iter()
            .map(|item| cpu_intensive_transform(item))
            .collect()
    })
    .await
    .unwrap()
}
```

## Related Rules
- [async-tokio-fs](async-tokio-fs.md) - Use tokio::fs for async file I/O
- [async-no-lock-await](async-no-lock-await.md) - Don't hold locks across await
