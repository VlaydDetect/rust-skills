# Huiali Pin Protocol

> Product adaptation of `skills/rust-pin/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-pin`.
- Supporting profiles when needed: `$rust-unsafe`, `$rust-concurrency`, `$rust-ownership`.
- Scope retained: Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.
- Baseline correction: Treat pinning as a library contract, not a synonym for heap allocation. Pin::new_unchecked and unsafe projection require a local proof covering movement, projection, replacement, and destruction.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## When Pin is Needed

### 1. async/await Futures

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-1; sha256=63e503306011ece97948bdf70078f02cfcd301009ce49a70e8b0ba57c9ebfd9e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;
use std::task::{Context, Poll};
use std::future::Future;

struct MyFuture {
    state: State,
}

impl Future for MyFuture {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        // self is pinned, guaranteed not to move
        let this = self.get_mut();
        Poll::Ready(())
    }
}
```

### 2. Self-Referential Structures

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-2; sha256=ce5bf82f5aa53d83d8b5d61ecc6c49653bf3b83bc54cad889dad6506482d8164 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;

struct Node {
    value: i32,
    // Self-reference: pointer to field within same struct
    next: Option<Pin<Box<Node>>>,
}
```


## Solution Patterns

### Pattern 1: Pinning on Heap

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-3; sha256=8360d8faef3d61aac246113829cae480584de90ea264d5de9eada3988ab91ddf -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;

let future = async {
    // async block creates a Future
};

// Pin future on heap
let pinned: Pin<Box<dyn Future<Output = ()>>> = Box::pin(future);

// Now safe to poll
```

### Pattern 2: Pinning with Pin::new_unchecked

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-4; sha256=41f33bb97a9605322dc17d94165af8d010030fc75a82cfd7cf06e8189bc4da0f -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;

struct SelfReferential {
    data: String,
    ptr: *const String,  // Points to data field
}

impl SelfReferential {
    fn new(data: String) -> Pin<Box<Self>> {
        let mut boxed = Box::new(SelfReferential {
            data,
            ptr: std::ptr::null(),
        });

        let ptr = &boxed.data as *const String;
        boxed.ptr = ptr;

        // SAFETY: boxed is on heap and won't move
        unsafe { Pin::new_unchecked(boxed) }
    }

    fn data(&self) -> &str {
        // SAFETY: ptr still valid because we're pinned
        unsafe { &*self.ptr }
    }
}
```

### Pattern 3: Pin Projection

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-5; sha256=0e661243f0d219ad8e1e3c912323db971f0150f512ece525048b534af9e193a3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;

struct Wrapper<T> {
    inner: T,
    extra: String,
}

impl<T: Unpin> Wrapper<T> {
    // Safe projection: T is Unpin
    fn project(self: Pin<&mut Self>) -> Pin<&mut T> {
        Pin::new(&mut self.get_mut().inner)
    }
}

impl<T> Wrapper<T> {
    // Unsafe projection: must maintain invariants
    fn project_unchecked(self: Pin<&mut Self>) -> Pin<&mut T> {
        // SAFETY: if Self is pinned, inner field is also pinned
        unsafe {
            Pin::new_unchecked(&mut self.get_unchecked_mut().inner)
        }
    }
}
```

### Pattern 4: Pinning in Async Context

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-6; sha256=cbb139690d828711f99555c971211118b390d12d25eb09e34cf82f2c923ac7d5 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;
use std::future::Future;

async fn process_data() {
    let mut state = String::new();

    // This reference is held across await
    let state_ref = &mut state;

    some_async_operation().await;

    // state_ref must remain valid
    state_ref.push_str("data");
}

// Compiler ensures state doesn't move by pinning the Future
```


## Pin Types

| Type | Use Case | Example |
|------|----------|---------|
| `Pin<&T>` | Borrowed, immutable | `Pin<&Foo>` |
| `Pin<&mut T>` | Borrowed, mutable | `Pin<&mut Foo>` |
| `Pin<Box<T>>` | Owned on heap | `Pin<Box<Foo>>` |
| `Pin<Arc<T>>` | Shared ownership | `Pin<Arc<Foo>>` |


## Unpin Marker Trait

> Product correction: compiler-generated Futures are not uniformly `!Unpin`; determine the concrete type. Source references to Generators are historical—current nightly terminology is coroutines, while stable `Future`, streams, iterators, or explicit state machines remain preferred when nightly is unnecessary.

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-7; sha256=6cd0e40fd61773826b1fd42cf5704b634b5c7491dc1168a187cbb990533a1e20 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Most types implement Unpin (safe to move)
struct MyType {
    data: Vec<u8>,
}
// Unpin auto-implemented

// Which types DON'T implement Unpin?
// - Futures (from async/await)
// - Generators
// - Manually marked with PhantomPinned

use std::marker::PhantomPinned;

struct NotUnpin {
    data: String,
    _pin: PhantomPinned,  // Opts out of Unpin
}
```


## Workflow

### Step 1: Determine if Pin Needed

```
Need Pin when:
  → polling or implementing an address-sensitive Future
  → self-referential or intrusive state
  → an API explicitly requires Pin<P>
  → current nightly coroutines only when the project intentionally uses them

Don't need Pin when:
  → Synchronous code
  → No self-references
  → ordinary values with no address-sensitive invariant
  → Type is Unpin
```

### Step 2: Choose Pinning Strategy

```
Heap pinning:
  → Box::pin(value)
  → Safe, most common

Stack pinning:
  → pin!(value)  // macro in std
  → More complex, zero allocation

Unsafe pinning:
  → Pin::new_unchecked()
  → Require SAFETY comments
```

### Step 3: Handle Projections

```
Projecting to field:
  → If T: Unpin → Safe with Pin::new
  → If !Unpin → Unsafe, need Pin::new_unchecked
  → Use pin-project crate for safety
```


## Common Use Cases

| Scenario | Need Pin? |
|----------|-----------|
| `async {}` block | ✅ Yes (Future) |
| `Box<dyn Future>` | ✅ Yes |
| Self-referential struct | ✅ Yes |
| Regular Vec/HashMap | ❌ No |
| Stack variables | ❌ No |
| No self-references | ❌ No |


## Review Checklist

When working with Pin:

- [ ] Pin actually necessary (async or self-ref)
- [ ] Correct pinning strategy chosen (heap vs stack)
- [ ] Unsafe projections have SAFETY comments
- [ ] Type correctly implements/opts-out of Unpin
- [ ] No accidental moves after pinning
- [ ] Projection maintains structural pinning
- [ ] Drop implementation respects pinning
- [ ] Documentation explains why pinned


## Verification Commands

```bash
# Check if type is Unpin
cargo expand

# Verify async state machine
cargo expand --lib my_async_fn

# Test with miri
cargo +nightly miri test
```


## Common Pitfalls

### 1. Forgetting to Pin Future

**Symptom**: Compilation error about poll signature

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-8; sha256=23393e1fdbb3ea7cc929d97087984a0fc3ee660b069b670173803560345158d3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: Future not pinned
fn poll_future(mut future: impl Future) {
    future.poll();  // Error: no poll method
}

// ✅ Good: Pin the Future
fn poll_future(mut future: Pin<&mut impl Future>) {
    future.as_mut().poll(cx);  // OK
}
```

### 2. Moving Pinned Value

**Symptom**: Undefined behavior

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-9; sha256=dff57d3d1b47db943cabe4dae68e35080ca505b2b48d7762a97024698a1b63a1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: moving after pinning
let pinned = Box::pin(value);
let moved = *pinned;  // Error: cannot move out of pinned

// ✅ Good: work with pinned reference
let pinned = Box::pin(value);
let pinned_ref: Pin<&mut Value> = pinned.as_mut();
```

### 3. Incorrect Projection

**Symptom**: Unsoundness in self-referential types

<!-- huiali-source: skills/rust-pin/SKILL.md#rust-block-10; sha256=58e0bed721b268d9b24699ffa3bde066e077ce55788c64a97bfeab02da4f50f4 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: unsafe projection without guarantee
impl<T> Wrapper<T> {
    fn bad_project(self: Pin<&mut Self>) -> &mut T {
        &mut self.get_mut().inner  // Unsound if T: !Unpin
    }
}

// ✅ Good: safe projection with Unpin bound
impl<T: Unpin> Wrapper<T> {
    fn safe_project(self: Pin<&mut Self>) -> Pin<&mut T> {
        Pin::new(&mut self.get_mut().inner)
    }
}
```


## Related Skills

- **rust-async** - Async/await and Future trait
- **rust-unsafe** - Unsafe code for Pin::new_unchecked
- **rust-ownership** - Lifetime and borrowing
- **rust-type-driven** - PhantomPinned and marker types
- **rust-performance** - Zero-cost abstractions with Pin

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-pin/SKILL_ZH.md#rust-block-1; sha256=007b0d4c8e6f220863e4d4a197ad712b4a51da3ab33afd45c191e0d155e1f139 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;
use std::task::{Context, Poll};

struct MyFuture {
    state: State,
}

impl Future for MyFuture {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        // 安全使用 this.state
        Poll::Ready(())
    }
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-pin/SKILL_ZH.md#rust-block-2; sha256=581125892be687b43ecce8a1a2e65309e3c189c0eef66114e29d429a81866c2e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::pin::Pin;

struct Node {
    value: i32,
    parent: Option<Pin<Box<Node>>>,  // 自引用
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-pin/SKILL_ZH.md#rust-block-3; sha256=4664df12f3fc6c91def0a4ff1132cd41cc3ea3ed3b01fd95903d1bd3ec662666 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 类型可以实现 Unpin 表示它不介意被移动
struct MyType {
    data: Vec<u8>,
}

// Unpin 自动实现，大多数类型不需要手动实现
// 哪些类型没有实现 Unpin？
// - Future (async/await 生成的)
// - Generator
// - 手动用 !Unpin 标记的类型

struct NotUnpinType {
    // 包含自引用指针
    ptr: *const Self,
}

impl !Unpin for NotUnpinType {}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-pin/SKILL_ZH.md#rust-block-4; sha256=c8693031a31ed5ae3380bfe7907374acd6f46322d21a5128e8de33871f330715 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct Wrapper<T> {
    inner: T,
    extra: String,
}

impl<T> Pin for Wrapper<T> where T: Unpin {
    // projection 到 inner
    fn project(self: Pin<&mut Self>) -> Pin<&mut T> {
        // SAFETY: Wrapper is pinned, inner is inside it
        unsafe {
            &mut self.get_unchecked_mut().inner
        }
    }
}
```
