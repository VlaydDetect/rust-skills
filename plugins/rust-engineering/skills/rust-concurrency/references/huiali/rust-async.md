# Huiali Async Protocol

> Product adaptation of `skills/rust-async/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-concurrency`.
- Supporting profiles when needed: `$rust-ownership`, `$rust-errors`.
- Scope retained: Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.
- Baseline correction: Use the repository's resolved runtime and cancellation contract. Do not hold blocking or inappropriate synchronization guards across await, but do not ban standard mutexes or channels universally.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Solution Patterns

### Pattern 1: Stream Processing

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-1; sha256=ba91dd1884d1fa99130ddd69396eda4982d8f4174ccb87098d6af4a00f734f72 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio_stream::{self as stream, StreamExt};

async fn process_stream(stream: impl Stream<Item = Data>) {
    stream
        .chunks(100)           // Batch processing
        .for_each(|batch| async {
            process_batch(batch).await;
        })
        .await;
}
```

**When to use**: Processing continuous data flows (websockets, file streams, API pagination).

**Key insight**: Streams are async iterators - pull-based, lazy evaluation.

### Pattern 2: Backpressure Control

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-2; sha256=b97339f0653b00135d4d7684b5e393772434809ead4634d0ea07b7d7bd4af22e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

let semaphore = Arc::new(Semaphore::new(10));  // Max 10 concurrent

let stream = tokio_stream::iter(0..1000)
    .map(|i| {
        let permit = semaphore.clone().acquire_owned();
        async move {
            let _permit = permit.await?;
            process(i).await
        }
    })
    .buffer_unordered(100);  // Max 100 buffered futures
```

**When to use**: Prevent overwhelming downstream systems or resource exhaustion.

**Trade-offs**: Adds latency but prevents overload.

### Pattern 3: Select Multiplexing

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-3; sha256=0f3c05a3df3e2ca98cf7a36df50fcf988b24b9e2399077e772793c271c661a46 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::select;
use tokio::time::{sleep, Duration};

async fn multiplex() {
    loop {
        select! {
            msg = receiver.recv() => {
                if let Some(msg) = msg {
                    handle(msg).await;
                } else {
                    break;  // Channel closed
                }
            }
            _ = sleep(Duration::from_secs(5)) => {
                // Timeout handling
                check_health().await;
            }
            else => break,  // All branches complete
        }
    }
}
```

**When to use**: Waiting on multiple async operations, first-to-complete wins.

**Gotcha**: All branches must be cancellation-safe.

### Pattern 4: Task Cancellation

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-4; sha256=f93fe01dd114ba216f7f066ca550a8166a54b0e31017060afa0bafd25eaab2d4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::time::timeout;
use std::time::Duration;

async fn with_timeout() -> Result<Value, TimeoutError> {
    timeout(Duration::from_secs(5), long_operation()).await
        .map_err(|_| TimeoutError)?
}

// Cooperative cancellation
let mut task = tokio::spawn(async move {
    loop {
        // Check cancellation
        tokio::task::yield_now().await;  // Yield point

        // Do work
        if let Err(_) = work().await {
            return;
        }
    }
});

// Cancel task
task.abort();
let _ = task.await;  // Will return JoinError::Cancelled
```

**When to use**: Operations with time limits or user-requested cancellation.

**Key insight**: Cancellation is cooperative - requires yield points.


## Workflow

### Step 1: Choose Stream vs Iterator

```
Sync data source?
  → Use Iterator (more efficient)

Async data source (network, DB)?
  → Use Stream

Need backpressure?
  → Definitely Stream
```

### Step 2: Design Concurrency Strategy

```
Sequential processing?
  → for_each / fold

Limited concurrency?
  → buffer_unordered(N) + Semaphore

Unlimited (dangerous)?
  → Use with extreme caution
```

### Step 3: Handle Cancellation

```
Long-running task?
  → Add timeout wrapper

User-initiated?
  → Implement abort signal

Resource cleanup?
  → Use Drop or explicit cleanup
```


## Join vs Try_Join

### Join - Wait for All

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-5; sha256=75533abb55f6c9711a7f4faf72fd49aa2bcbdddd78e8e60491cb3c00ce590dab -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::join;

// All operations run concurrently, wait for all to complete
let (a, b, c) = join!(
    fetch_user(),
    fetch_posts(),
    fetch_comments()
);
// All values available, even if some operations failed
```

**Use when**: All results needed regardless of individual failures.

### Try_Join - Fail Fast

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-6; sha256=dd6535c78631d3859b75765504c756b5c98f434956b76e390dfa2b605ed4fbe7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::try_join;

// Stop on first error
let (a, b) = try_join!(
    async_op_a(),
    async_op_b()
)?;
// Both succeeded, or error from first failure
```

**Use when**: All operations must succeed, fail fast on errors.

### Combined Pattern

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-7; sha256=c19422efb9d7409eb971951ef86e49217784fdbabea91891e3f2beb4cc75a731 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
async fn fetch_dashboard() -> Result<Dashboard, Error> {
    let (user, posts, comments) = try_join!(
        fetch_user(),
        fetch_posts(),
        fetch_comments()
    )?;

    Ok(Dashboard { user, posts, comments })
}
```


## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `.await` forgotten | Future not polled | Check all async fn calls have `.await` |
| Cancellation unhandled | Task aborted mid-operation | Implement cooperative cancellation |
| Missing backpressure | Unbounded concurrency | Use Semaphore or buffer_unordered |
| Deadlock | Lock held across `.await` | Minimize lock scope, drop before await |
| Async drop unsupported | Drop in async context | Use spawn for cleanup or blocking drop |


## Backpressure Strategies

### Strategy 1: Semaphore-Based

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-8; sha256=06150e0070ec188a168b9cebda5e9f5421f4c55817a48ebe70d16e757164195c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
let sem = Arc::new(Semaphore::new(10));

stream
    .map(|item| {
        let sem = sem.clone();
        async move {
            let _permit = sem.acquire().await?;
            process(item).await
        }
    })
    .buffer_unordered(10)
```

**Pros**: Precise control, easy to reason about
**Cons**: Semaphore overhead

### Strategy 2: Buffered Stream

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-9; sha256=6cb22d67b1b809039a431e2483008e99594b537256940b2277f2723ca484553f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
stream
    .chunks(100)
    .for_each_concurrent(5, |batch| async move {
        process_batch(batch).await
    })
    .await
```

**Pros**: Simple, built-in to StreamExt
**Cons**: Less fine-grained control

### Strategy 3: Channel-Based

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-10; sha256=8d4703046f87d9abc990fad91146a49f9adc4909aeffc172664b82a10c0b6db7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
let (tx, mut rx) = mpsc::channel(100);  // Buffer size = backpressure

// Producer respects backpressure
tx.send(item).await?;

// Consumer pulls at own pace
while let Some(item) = rx.recv().await {
    process(item).await;
}
```

**Pros**: Natural backpressure from bounded channel
**Cons**: Extra copy/move overhead


## Performance Tips

| Pattern | Performance Insight |
|---------|---------------------|
| `select!` | More lightweight than multiple `tokio::spawn` |
| `buffer_unordered` | More flexible than `for_each_concurrent` |
| `.chunks()` | Reduces per-item overhead for bulk operations |
| Lock-free at await | Never hold locks across `.await` points |
| `spawn_blocking` | Use for CPU-bound work in async context |


## Advanced: Future Trait

### Implementing Future

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-11; sha256=306eb72364fab6f8b7e2899b3814ce72f2587fad599c0c018a70475841a19ed4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

struct Delay {
    when: Instant,
}

impl Future for Delay {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        if Instant::now() >= self.when {
            Poll::Ready(())
        } else {
            // Wake me later
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}
```

**When to implement**: Custom async primitives, advanced control flow.

**Gotcha**: Must properly handle wakeup notifications.


## Review Checklist

When reviewing async code:

- [ ] All async functions are properly `.await`ed
- [ ] Backpressure mechanisms in place for streams
- [ ] Cancellation handled cooperatively (yield points)
- [ ] No locks held across `.await` points
- [ ] Stream processing uses appropriate concurrency limits
- [ ] Error propagation uses `?` or proper handling
- [ ] `select!` branches are cancellation-safe
- [ ] Long-running tasks have timeout protection
- [ ] Resource cleanup happens even on cancellation
- [ ] CPU-bound work uses `spawn_blocking`


## Verification Commands

```bash
# Check async code compilation
cargo check

# Run async tests
cargo test

# Check for common async mistakes
cargo clippy -- -W clippy::await_holding_lock

# Test with tokio-console for debugging
RUSTFLAGS="--cfg tokio_unstable" cargo run

# Profile async runtime
cargo flamegraph --bin your-app
```


## Common Pitfalls

### 1. Forgotten Await

**Symptom**: Future never executes, unexpected behavior

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-12; sha256=3420ef3dba3d0840137ca3fe4c6670af22909fb3dacb42d5695f4ca4c4da461c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: future not awaited
async fn bad() {
    fetch_data();  // Returns Future, never runs!
}

// ✅ Good
async fn good() {
    fetch_data().await;  // Actually runs
}
```

### 2. Unbounded Concurrency

**Symptom**: Resource exhaustion, system overload

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-13; sha256=645cf9514e691a4872fe00986236c19df4203b3af60989ad34a0fe4e21c8f93d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: all operations run concurrently
let futures: Vec<_> = urls.iter()
    .map(|url| fetch(url))
    .collect();
let results = join_all(futures).await;

// ✅ Good: limited concurrency
use futures::stream::{self, StreamExt};

let results = stream::iter(urls)
    .map(|url| fetch(url))
    .buffer_unordered(10)  // Max 10 concurrent
    .collect::<Vec<_>>()
    .await;
```

### 3. Lock Across Await

**Symptom**: Deadlock, "future cannot be sent between threads safely"

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-14; sha256=502cb52202e23d2184601ac00fe5c3c945d64e46b3c398287e2128e988d3cc52 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: lock held during await
let guard = mutex.lock().await;
some_async_op().await;  // DANGER
drop(guard);

// ✅ Good: drop lock before await
let value = {
    let guard = mutex.lock().await;
    guard.clone()
};  // lock dropped
some_async_op().await;
```

### 4. Async Drop

**Symptom**: Cannot await in Drop impl

<!-- huiali-source: skills/rust-async/SKILL.md#rust-block-15; sha256=b6be7e532030a44eb950b492e73c04b25587fb709f2d45f732affb1e0dd20b6c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: async operation in Drop
impl Drop for Resource {
    fn drop(&mut self) {
        // Cannot await here!
        self.cleanup().await;  // Won't compile
    }
}

// ✅ Good: explicit async cleanup
impl Resource {
    async fn cleanup(self) {
        // Async cleanup logic
    }
}

// Or spawn cleanup task
impl Drop for Resource {
    fn drop(&mut self) {
        let handle = self.handle.take();
        tokio::spawn(async move {
            if let Some(h) = handle {
                h.cleanup().await;
            }
        });
    }
}
```


## Related Skills

- **rust-concurrency** - Thread safety, Send/Sync basics
- **rust-async-pattern** - Async architecture patterns
- **rust-ownership** - Lifetime issues in async contexts
- **rust-pin** - Pin and self-referential types
- **rust-performance** - Async performance optimization
- **rust-web** - Async web frameworks (axum, actix)

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_EN.md` example 1

<!-- huiali-source: skills/rust-async/SKILL_EN.md#rust-block-1; sha256=34e0a501f3932aa3cbab626700e0f6082bf15a89a552b2c6115aaedc028f4435 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use futures::{stream, StreamExt, TryStreamExt};

async fn fetch_all(urls: Vec<String>) -> Result<Vec<String>, reqwest::Error> {
    stream::iter(urls)
        .map(|u| async move { reqwest::get(u).await?.text().await })
        .buffer_unordered(32)
        .try_collect()
        .await
}
```

### `SKILL_EN.md` example 2

<!-- huiali-source: skills/rust-async/SKILL_EN.md#rust-block-2; sha256=67a2de850ab34d5e2cfc446153b880e783ed7755b29ea3ebc255373a88b1ad4f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::time::{timeout, Duration};

async fn call_with_timeout<F, T, E>(f: F) -> Result<T, String>
where
    F: std::future::Future<Output = Result<T, E>>,
    E: std::fmt::Display,
{
    match timeout(Duration::from_secs(2), f).await {
        Ok(Ok(v)) => Ok(v),
        Ok(Err(e)) => Err(format!("request failed: {e}")),
        Err(_) => Err("request timed out".to_string()),
    }
}
```

### `SKILL_EN.md` example 3

<!-- huiali-source: skills/rust-async/SKILL_EN.md#rust-block-3; sha256=786f3f4f5f8611d1cffe17e9d8f5333ee2cde41b04d79e81e3ac9ab106b640e1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::select;
use tokio::sync::watch;

async fn run_loop(mut shutdown: watch::Receiver<bool>) {
    loop {
        select! {
            _ = shutdown.changed() => {
                if *shutdown.borrow() { break; }
            }
            _ = do_one_tick() => {}
        }
    }
}

async fn do_one_tick() {
    // periodic work
}
```

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-async/SKILL_ZH.md#rust-block-1; sha256=06f5d7ea4624c3f66ebf98b82c1aca912d9532e8890264ad88fdf43b9bcc3595 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio_stream::{self as Stream, StreamExt};

async fn process_stream(stream: impl Stream<Item = Data>) {
    stream
        .chunks(100)           // 批量处理
        .for_each(|batch| async {
            process_batch(batch).await;
        })
        .await;
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-async/SKILL_ZH.md#rust-block-2; sha256=62d9d08f1a44b72d0f577fa6f67469bfb2d3525ac685d27df5c9cd13f70a9ace -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::sync::Semaphore;

let semaphore = Semaphore::new(10);  // 最多 10 个并发

let stream = tokio_stream::iter(0..1000)
    .map(|i| {
        let permit = semaphore.clone().acquire_owned();
        async move {
            let _permit = permit.await;
            process(i).await
        }
    })
    .buffer_unordered(100);  // 最多 100 并发
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-async/SKILL_ZH.md#rust-block-3; sha256=ad4b4144c9311d01aaeb9490af2452af8c15709647f2b97aded65ced27228b8b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::select;
use tokio::time::{sleep, timeout};

async fn multiplex() {
    loop {
        select! {
            msg = receiver.recv() => {
                if let Ok(msg) = msg {
                    handle(msg).await;
                }
            }
            _ = sleep(Duration::from_secs(5)) => {
                // 超时处理
            }
            else => break,  // 所有分支都完成
        }
    }
}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-async/SKILL_ZH.md#rust-block-4; sha256=0c4fb9a31fa8f98ca8510199bd874133f236a368bb562faec56181521a886b28 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tokio::time::timeout;

async fn with_timeout() -> Result<Value, TimeoutError> {
    timeout(Duration::from_secs(5), long_operation()).await
}

// 协作式取消
let mut task = tokio::spawn(async move {
    loop {
        // 检查取消
        if task.is_cancelled() {
            return;
        }
        // 继续工作
    }
});

// 取消任务
task.abort();
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-async/SKILL_ZH.md#rust-block-5; sha256=975aaffca6d45bf1498448b466e3d752e31ef85c41b138b60ffeaf42146eb0d0 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 并行执行，不等待完成
let (a, b) = tokio::join!(async_a(), async_b());

// 全部成功才成功
let (a, b) = tokio::try_join!(async_a(), async_b())?;

// 错误传播
fn combined() -> impl Future<Output = Result<(A, B), E>> {
    async {
        let (a, b) = try_join!(op_a(), op_b())?;
        Ok((a, b))
    }
}
```
