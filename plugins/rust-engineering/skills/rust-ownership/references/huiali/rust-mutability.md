# Huiali Mutability Protocol

> Product adaptation of `skills/rust-mutability/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-ownership`.
- Supporting profiles when needed: `$rust-concurrency`, `$rust-api-design`.
- Scope retained: Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.
- Baseline correction: Select Cell, RefCell, locks, or atomics from the sharing and failure contract. Interior mutability moves checks or synchronization; it does not remove aliasing obligations.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Mutability Types

| Type | Controller | Thread-Safe | Use Case |
|------|------------|-------------|----------|
| `&mut T` | External caller | Yes | Standard mutable borrow |
| `Cell<T>` | Interior | No | Copy types with interior mutability |
| `RefCell<T>` | Interior | No | Non-Copy types with interior mutability |
| `Mutex<T>` | Interior | Yes | Multi-threaded interior mutability |
| `RwLock<T>` | Interior | Yes | Multi-threaded read-write lock |


## Solution Patterns

### Pattern 1: External Mutability

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-1; sha256=0342a271a410c6dd4c1fe2bca46d02895308b85061e8a317eba47b95f2ea576b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Standard mutable borrow
fn increment(counter: &mut u32) {
    *counter += 1;
}

// Mutable method
impl Counter {
    fn increment(&mut self) {
        self.value += 1;
    }
}
```

**When to use**: Default choice, mutability controlled by caller.

### Pattern 2: Cell for Copy Types

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-2; sha256=dd5964c1be1d325d25261ded9d46f226200edca9a7a09a3e3f8c5b522eecc412 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::cell::Cell;

struct State {
    count: Cell<u32>,
}

impl State {
    // Get immutable &self, mutate interior
    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }
}
```

**When to use**: Simple values (Copy types) need interior mutability.

**Trade-offs**: Only works with Copy types, no references.

### Pattern 3: RefCell for Non-Copy Types

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-3; sha256=79afab4fec216feffdd63254d5b98ecd269ee1544543c4cded36795018324073 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::cell::RefCell;

struct Cache {
    data: RefCell<HashMap<String, Value>>,
}

impl Cache {
    fn insert(&self, key: String, value: Value) {
        self.data.borrow_mut().insert(key, value);
    }

    fn get(&self, key: &str) -> Option<Value> {
        self.data.borrow().get(key).cloned()
    }
}
```

**When to use**: Need `&mut T` from `&self`, single-threaded.

**Trade-offs**: Runtime borrow checking, can panic.

### Pattern 4: Mutex for Thread Safety

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-4; sha256=bd94e1f5c2ac70bcd65fb7c1699bb6a99ecab911ee48568baf824ad94a615825 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::Mutex;

struct SharedState {
    data: Mutex<HashMap<String, Value>>,
}

impl SharedState {
    fn insert(&self, key: String, value: Value) {
        self.data.lock().unwrap().insert(key, value);
    }
}
```

**When to use**: Multi-threaded interior mutability.

**Trade-offs**: Lock contention, can deadlock.

### Pattern 5: RwLock for Read-Heavy Workloads

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-5; sha256=afe60cb049b26ed8e79f7036407e90d4b470715dc0d1a034236e3c091514e933 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::RwLock;

struct Config {
    settings: RwLock<HashMap<String, String>>,
}

impl Config {
    fn get(&self, key: &str) -> Option<String> {
        self.settings.read().unwrap().get(key).cloned()
    }

    fn update(&self, key: String, value: String) {
        self.settings.write().unwrap().insert(key, value);
    }
}
```

**When to use**: Many readers, few writers.

**Trade-offs**: Write locks more expensive than Mutex.


## Borrow Rules

```
At any time, you can have either:
├─ Multiple &T (immutable borrows)
└─ OR one &mut T (mutable borrow)

Never both simultaneously
```


## Error Code Quick Reference

| Code | Meaning | Don't Say | Ask Instead |
|------|---------|-----------|-------------|
| E0596 | Cannot get mutable reference | "add mut" | Does this really need mutability? |
| E0499 | Multiple mutable borrows conflict | "split borrows" | Is data structure design correct? |
| E0502 | Borrow conflict | "separate scopes" | Why both borrows needed simultaneously? |
| RefCell panic | Runtime borrow error | "use try_borrow" | Is runtime checking appropriate? |


## Workflow

### Step 1: Choose Mutability Strategy

```
Single-threaded?
  Need &mut from &self?
    → RefCell<T>
  Copy type?
    → Cell<T>
  Otherwise?
    → &mut T

Multi-threaded?
  Simple atomic?
    → AtomicU64/AtomicBool
  Complex data?
    Read-heavy → RwLock<T>
    Write-heavy → Mutex<T>
```

### Step 2: Handle Borrow Conflicts

```
E0499 (multiple mut borrows)?
  → Split struct into smaller pieces
  → Use Cell/RefCell for interior mutability
  → Redesign to avoid simultaneous access

E0502 (borrow conflict)?
  → Minimize borrow scopes
  → Clone data if needed
  → Restructure code flow
```

### Step 3: Consider Trade-offs

```
RefCell?
  ✅ Flexible
  ❌ Runtime panics possible
  → Use in prototypes, single-threaded

Mutex?
  ✅ Thread-safe
  ❌ Lock contention
  → Profile before optimizing

RwLock?
  ✅ Many readers efficient
  ❌ Writer starvation possible
  → Use when reads >> writes
```


## Thread-Safe Selection

### Atomic Types

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-6; sha256=45cf8f545e2cabc95adde05798e4e6a90f2ef10fc64996d2b16d343c1e337f3a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::atomic::{AtomicU64, Ordering};

let counter = AtomicU64::new(0);
counter.fetch_add(1, Ordering::Relaxed);
```

**Use when**: Simple counters, flags.

### Mutex

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-7; sha256=b040955dad1a60a8f91978c1c446d86b1c06ff0c1b6526a82e37800197a17641 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::Mutex;

let data = Mutex::new(HashMap::new());
data.lock().unwrap().insert(key, value);
```

**Use when**: Thread-safe mutation, balanced read/write.

### RwLock

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-8; sha256=0e69f4ded2cddf71739faf6f65d7dd36dc5cb88fb894bca98d88848e28d204d5 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::RwLock;

let data = RwLock::new(HashMap::new());
data.read().unwrap().get(&key);  // Many readers
data.write().unwrap().insert(key, value);  // Few writers
```

**Use when**: Read-heavy workloads (10+ reads per write).


## Common Pitfalls

### 1. Borrow Conflict

**Symptom**: E0499, E0502 errors

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-9; sha256=fd37e948f5a746c1f7f981fe494c9ba373662fcd9e65dd5f1a1b9944f3f3d8bd -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: multiple mutable borrows
let r1 = &mut data.field1;
let r2 = &mut data.field2;  // Error!

// ✅ Good: split borrows
let (field1, field2) = (&mut data.field1, &mut data.field2);

// ✅ Better: restructure
struct Data {
    part1: Part1,
    part2: Part2,
}
```

### 2. RefCell Panic

**Symptom**: "already borrowed" panic at runtime

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-10; sha256=e65a16c6e3f041273ea9fff687ac4121153a8c1bbfb658996ed76bae20bd19b9 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: nested borrows
let cell = RefCell::new(vec![1, 2, 3]);
let borrow1 = cell.borrow();
let borrow2 = cell.borrow_mut();  // Panics!

// ✅ Good: drop first borrow
{
    let borrow1 = cell.borrow();
    // use borrow1...
}  // dropped
let borrow2 = cell.borrow_mut();  // OK

// ✅ Better: use try_borrow
if let Ok(mut b) = cell.try_borrow_mut() {
    // safe mutation
}
```

### 3. Lock Held Across Await

**Symptom**: Deadlock in async code

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-11; sha256=a76b0c8f9a90f7c1bacb345eeef57c62d98aaf57177ca12f381a5bc654ea20d7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: MutexGuard across await
let guard = mutex.lock().unwrap();
async_op().await;  // DANGER

// ✅ Good: drop lock before await
let value = {
    let guard = mutex.lock().unwrap();
    guard.clone()
};  // lock dropped
async_op().await;
```


## Review Checklist

When reviewing mutability code:

- [ ] Mutability truly necessary (not premature)
- [ ] Appropriate mutability type chosen (Cell/RefCell/Mutex)
- [ ] RefCell used only in single-threaded contexts
- [ ] Mutex/RwLock used for multi-threaded access
- [ ] Lock scopes minimized to avoid contention
- [ ] No locks held across `.await` points
- [ ] Borrow conflicts resolved at design level
- [ ] Runtime panics handled (try_borrow)
- [ ] Atomic types used for simple counters/flags
- [ ] Read-write patterns match RwLock choice


## Verification Commands

```bash
# Check compilation
cargo check

# Look for borrow conflict errors
cargo check 2>&1 | grep -E "E0499|E0502|E0596"

# Run tests
cargo test

# Check for deadlocks (with loom)
cargo test --features loom

# Clippy warnings
cargo clippy -- -W clippy::mutex_atomic
```


## Advanced Patterns

### Splitting Borrows

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-12; sha256=688e35673ec85d6b669b0fabb3fac46624b4a3b2e551ed89706ef56f379aa205 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ✅ Split struct to enable simultaneous borrows
struct Data {
    readers: Vec<Reader>,
    writers: Vec<Writer>,
}

fn process(data: &mut Data) {
    let readers = &data.readers;
    let writers = &mut data.writers;  // OK, different fields
    // use both...
}
```

### Interior Mutability with Shared Ownership

<!-- huiali-source: skills/rust-mutability/SKILL.md#rust-block-13; sha256=d0560f08bb67040771199f7b06076d4acd556119a06acd0072eaabd85ff8cbaa -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::{Arc, Mutex};

#[derive(Clone)]
struct Shared {
    inner: Arc<Mutex<Inner>>,
}

impl Shared {
    fn update(&self) {
        self.inner.lock().unwrap().modify();
    }
}
```


## Related Skills

- **rust-ownership** - Ownership and borrowing fundamentals
- **rust-concurrency** - Thread-safe patterns
- **rust-unsafe** - UnsafeCell and low-level mutability
- **rust-anti-pattern** - Mutability anti-patterns
- **rust-performance** - Lock contention optimization

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-mutability/SKILL_ZH.md#rust-block-1; sha256=63799b12e7ec3c6f7c60be3fd8f6388322bc4c5c8c9448a4480c544d74601de3 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 情况1：从 &self 获取 &mut T
struct Config {
    counters: RefCell<HashMap<String, u32>>,
}

impl Config {
    fn increment(&self, key: &str) {
        // 从不可变引用获取可变引用
        let mut counters = self.counters.borrow_mut();
        *counters.entry(key.to_string()).or_insert(0) += 1;
    }
}

// 情况2：Copy 类型
struct State {
    count: Cell<u32>,
}

impl State {
    fn increment(&self) {
        self.count.set(self.count.get() + 1);
    }
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-mutability/SKILL_ZH.md#rust-block-2; sha256=2e2bb7ef5daa1abf3812594c146ed3fab078eeeb8607d31080653b75f5823dbc -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 简单计数器 → 原子类型
let counter = AtomicU64::new(0);

// 复杂数据 → Mutex 或 RwLock
let data = Mutex::new(HashMap::new());

// 读多写少 → RwLock
let data = RwLock::new(HashMap::new());
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-mutability/SKILL_ZH.md#rust-block-3; sha256=25270fba17693457e660acb035ff038ecbdd4a089efc9bd1be59ca7183365efe -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 借用冲突
let mut s = String::new();
let r1 = &s;
let r2 = &s;
let r3 = &mut s; // 冲突！

// ✅ 分开作用域
let mut s = String::new();
{
    let r1 = &s;
    // 使用 r1
}
let r3 = &mut s;
// 使用 r3
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-mutability/SKILL_ZH.md#rust-block-4; sha256=9831471aad58aec6b9a67796f77a1dc85b471c4b5aa42350f72f60f049a283f6 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ 双重可变借用
let cell = RefCell::new(vec![]);
let mut_borrow = cell.borrow_mut();
let another = cell.borrow(); // panic!

// ✅ 用 try_borrow 避免 panic
if let Ok(mut_borrow) = cell.try_borrow_mut() {
    // 安全使用
}
```
