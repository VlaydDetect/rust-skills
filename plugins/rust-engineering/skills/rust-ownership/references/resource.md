# Specialized Rust Resource Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-ownership`.
- Supporting profiles when needed: `$rust-errors`, `$rust-concurrency`.
- Scope retained: RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.
- Baseline correction: Make ownership and cleanup paths explicit, including partial failure and cancellation. Pools and shared ownership are optimizations or coordination tools, not defaults.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Selection Decision Tree

```
Must the data be shared?
    │
    ├─ No → One owner
    │   ├─ Heap allocation required? → Box<T>
    │   └─ Stack is sufficient? → Store the value directly
    │
    └─ Yes → Shared ownership
          │
          ├─ Single-threaded?
          │   ├─ Mutable? → Rc<RefCell<T>>
          │   └─ Read-only? → Rc<T>
          │
          └─ Multithreaded?
                ├─ Mutable? → Arc<Mutex<T>> or Arc<RwLock<T>>
                └─ Read-only? → Arc<T>
```


## Smart-Pointer Comparison

| Type | Ownership | Thread-safe | Applicable scenario |
|-----|-------|---------|---------|
| `Box<T>` | One owner | Yes | Heap allocation, recursive types, trait objects |
| `Rc<T>` | Shared | No | Single-threaded sharing, avoiding clones |
| `Arc<T>` | Shared | Yes | Multithreaded sharing, read-only data |
| `Weak<T>` | Weak reference | - | Breaking reference cycles |
| `RefCell<T>` | One owner | No | Runtime borrow checking |
| `Cell<T>` | One owner | No | Interior mutability for Copy types |


## Common Errors and Solutions

### Rc Reference-Cycle Leak<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Memory leak: two Rc values reference each other
struct Node {
    value: i32,
    next: Option<Rc<Node>>,
}

// ✅ Solution: use Weak to break the cycle
struct Node {
    value: i32,
    next: Option<Weak<Node>>,
}
```

### RefCell panic<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Runtime panic: two mutable borrows
let cell = RefCell::new(vec![1, 2, 3]);
let mut_borrow = cell.borrow_mut();
let another_borrow = cell.borrow(); // panic!

// ✅ Solution: use try_borrow
if let Ok(mut_borrow) = cell.try_borrow_mut() {
    // Use safely
}
```

### Arc Overhead Concerns<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Unnecessary Arc in a single-threaded environment
let shared = Arc::new(data);

// ✅ Use Rc in single-threaded code
let shared = Rc::new(data);

// ❌ Unnecessary atomic operations
// Do not use Arc when cross-thread sharing is definitely unnecessary
```


## Choosing Interior Mutability<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// T is Copy → Cell
struct Counter {
    count: Cell<u32>,
}

// T is not Copy → RefCell
struct Container {
    items: RefCell<Vec<Item>>,
}

// Multiple threads → Mutex or RwLock
struct SharedContainer {
    items: Mutex<Vec<Item>>,
}
```


## RAII and Drop<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
struct File {
    handle: std::fs::File,
}

impl Drop for File {
    fn drop(&mut self) {
        // Release the resource automatically
        println!("File closed");
    }
}

// Use the guard pattern to ensure cleanup
struct Guard<'a> {
    resource: &'a Resource,
}

impl Drop for Guard<'_> {
    fn drop(&mut self) {
        self.resource.release();
    }
}
```


## Performance Tips

| Scenario | Recommendation |
|-----|------|
| Many small objects | Use `Rc::make_mut()` to avoid cloning |
| Frequent reads | Prefer `RwLock` over `Mutex` |
| Counters | Use `AtomicU64` instead of `Mutex<u64>` |
| Caches | Consider the `moka` or `cached` crate |


## When Not to Use Smart Pointers

- Stack storage is sufficient → Store the value directly
- A borrow is sufficient → Use a reference, `&T`
- Lifetimes are simple → Do not over-abstract
