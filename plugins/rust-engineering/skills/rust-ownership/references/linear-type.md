# Specialized Rust Linear Type Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-ownership`.
- Supporting profiles when needed: `$rust-traits`, `$rust-errors`.
- Scope retained: Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.
- Baseline correction: Rust ownership is affine: values may be consumed at most once but may also be dropped unused. Do not claim the language provides general linear types or compile-time exactly-once use.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Linear Types vs Rust Ownership

| Property | Rust ownership | Linear types |
|-----|------------|---------|
| Move semantics | ✓ | ✓ |
| Copy semantics | Optional | ✗ |
| Destruction guarantee | Drop | Destructible |
| Borrowing | ✓ | ✗ or restricted |
| Multiple ownership | Rc/Arc | ✗ |

Rust types are not linear by default, but patterns can provide linear semantics.


## Destructible Trait<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Core of a linear type: Destructible guarantees destruction
use std::mem::ManuallyDrop;

struct LinearBuffer {
    ptr: *mut u8,
    size: usize,
}

impl Drop for LinearBuffer {
    fn drop(&mut self) {
        unsafe {
            std::alloc::dealloc(self.ptr, Layout::array::<u8>(self.size).unwrap());
        }
    }
}

// Prevent a double free
struct SafeLinearBuffer {
    inner: ManuallyDrop<LinearBuffer>,
}

impl Drop for SafeLinearBuffer {
    fn drop(&mut self) {
        // Ensure the resource is freed exactly once
        unsafe {
            ManuallyDrop::drop(&mut self.inner);
        }
    }
}
```


## Exclusive-Object Pattern<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Ensure the object can be moved but not copied
#[derive(Copy, Clone)]
struct FileHandle(u32);

impl FileHandle {
    // Private constructor prevents direct external construction
    fn from_raw(fd: u32) -> Self {
        Self(fd)
    }
}

// Wrap it as a linear type
struct LinearFile {
    fd: FileHandle,
}

impl LinearFile {
    pub fn open(path: &str) -> Result<Self, std::io::Error> {
        // Open the file and return a linear file handle
        Ok(LinearFile {
            fd: FileHandle::from_raw(0), // Example
        })
    }

    // consume() consumes self, enforcing linear use
    pub fn consume(self) -> FileHandle {
        self.fd
    }
}
```


## Resource-Token Pattern<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Linear resource token
struct ResourceToken<T> {
    resource: T,
    consumed: bool,
}

impl<T> ResourceToken<T> {
    pub fn new(resource: T) -> Self {
        Self {
            resource,
            consumed: false,
        }
    }

    // Consume the token and return the resource
    pub fn consume(mut self) -> T {
        self.consumed = true;
        self.resource
    }

    // Check whether the token has been consumed
    pub fn is_consumed(&self) -> bool {
        self.consumed
    }
}

// Usage example
fn process_resource(token: ResourceToken<Vec<u8>>) -> Vec<u8> {
    // Process the resource here
    let data = token.consume(); // The token is invalid after consumption
    data
}
```


## Transactional Resource Management<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Two-phase commit pattern
struct Transaction<T> {
    data: T,
    committed: bool,
}

impl<T> Transaction<T> {
    pub fn new(data: T) -> Self {
        Self {
            data,
            committed: false,
        }
    }

    pub fn commit(mut self) -> T {
        self.committed = true;
        self.data
    }

    // Roll back by discarding the resource
    pub fn rollback(self) {
        // Drop is invoked automatically
    }
}

// Usage
fn example() -> Result<i32, ()> {
    let tx = Transaction::new(100);

    if condition {
        tx.commit(); // Commit and return the data
    } else {
        tx.rollback(); // Roll back and discard it
    }
}
```


## Unique-Pointer Pattern<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// Linear pointer similar to C++ unique_ptr
struct UniquePtr<T: Sized> {
    ptr: *mut T,
    _marker: std::marker::PhantomData<T>,
}

impl<T> UniquePtr<T> {
    pub fn new(data: T) -> Self {
        let ptr = Box::into_raw(Box::new(data));
        Self {
            ptr,
            _marker: std::marker::PhantomData,
        }
    }

    pub fn as_ref(&self) -> Option<&T> {
        if self.ptr.is_null() {
            None
        } else {
            Some(unsafe { &*self.ptr })
        }
    }

    // Consume self and return the Box
    pub fn into_box(self) -> Box<T> {
        unsafe {
            let ptr = self.ptr;
            std::mem::forget(self);
            Box::from_raw(ptr)
        }
    }
}

impl<T> Drop for UniquePtr<T> {
    fn drop(&mut self) {
        if !self.ptr.is_null() {
            unsafe {
                Box::from_raw(self.ptr);
            }
        }
    }
}
```


## Linear-Semantics Scenarios in Rust

| Scenario | Linear guarantee | Pattern |
|-----|---------|------|
| File handle | Close exactly once | RAII + Drop |
| Network connection | Close exactly once | RAII + Drop |
| Memory allocation | Free exactly once | RAII + Drop |
| Lock | Unlock exactly once | RAII + Drop |
| Transaction | Commit or roll back | Transactional resource management |
| FFI resource | Release exactly once | Resource token |


## Patterns to Avoid

| Anti-pattern | Problem | Correct approach |
|-------|------|---------|
| Clone permits copying | Breaks linear semantics | Use move semantics |
| Rc/Arc sharing | Multiple ownership | Use a linear token |
| Manual lifetime management | Error-prone | Use RAII + Drop |
| Skipping Drop | Resource leak | Use a scoped API |


## Related Skills

```
rust-linear-type
    │
    ├─► rust-resource → RAII and Drop implementations
    ├─► rust-ownership → ownership patterns
    └─► rust-unsafe → low-level resource operations
```
