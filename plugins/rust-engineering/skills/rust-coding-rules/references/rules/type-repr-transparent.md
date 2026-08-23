# type-repr-transparent

> Use `#[repr(transparent)]` for newtypes in FFI contexts## Decision

Use this context-sensitive Rust decision when its premise is established: Use `#[repr(transparent)]` for newtypes in FFI contexts.

## Apply When

Apply when a type can encode a real invariant, state, identity, representation, or output contract more reliably than convention, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the extra type machinery does not eliminate a meaningful invalid state or would make a local operation harder to use. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Name the invalid states, choose the smallest nominal or algebraic representation, and review construction and conversion boundaries.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Type-driven guarantees move failures earlier but can expand public surface, conversion code, generic complexity, and diagnostics.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- Supported targets, layout or ABI contract, panic policy, and safety invariants must be explicit.
- Public compatibility and downstream caller impact must be known before changing an exported contract.

## Verification

Use compile-pass, compile-fail, and runtime boundary cases to prove valid construction and rejection paths.

## Why It Matters

`#[repr(transparent)]` guarantees a newtype has the same memory layout as its inner type. This is essential for FFI where you need type safety in Rust but must match C ABI layouts. Without it, the compiler may add padding or change layout.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// No layout guarantee - might not match inner type in FFI
struct Handle(u64);

// Passing to C code might fail
extern "C" {
    fn process_handle(h: Handle);  // May not work correctly
}

// Wrapping C type without layout guarantee
struct SafePointer(*mut c_void);
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Guaranteed same layout as inner type
#[repr(transparent)]
struct Handle(u64);

// Safe for FFI
extern "C" {
    fn process_handle(h: Handle);  // Works - same layout as u64
}

// FFI pointer wrapper
#[repr(transparent)]
struct SafePointer(*mut c_void);

impl SafePointer {
    // Safe Rust API around raw pointer
    pub fn new(ptr: *mut c_void) -> Option<Self> {
        if ptr.is_null() {
            None
        } else {
            Some(SafePointer(ptr))
        }
    }
}
```

## What repr(transparent) Guarantees

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the What repr(transparent) Guarantees illustration -->
```rust
use std::mem::{size_of, align_of};

#[repr(transparent)]
struct Meters(f64);

// Same size
assert_eq!(size_of::<Meters>(), size_of::<f64>());

// Same alignment
assert_eq!(align_of::<Meters>(), align_of::<f64>());

// Same ABI - can pass where f64 expected
extern "C" fn measure(distance: Meters) { ... }
```

## With PhantomData

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the With PhantomData illustration -->
```rust
use std::marker::PhantomData;

// PhantomData is zero-sized, doesn't affect layout
#[repr(transparent)]
struct TypedHandle<T> {
    raw: u64,
    _marker: PhantomData<T>,  // Zero-sized, ignored for layout
}

// Still same layout as u64
assert_eq!(size_of::<TypedHandle<String>>(), size_of::<u64>());
```

## NonZero Wrappers

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the NonZero Wrappers illustration -->
```rust
use std::num::NonZeroU64;

#[repr(transparent)]
struct NonZeroHandle(NonZeroU64);

// Inherits null-pointer optimization
assert_eq!(size_of::<Option<NonZeroHandle>>(), size_of::<u64>());
```

## FFI Pattern

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the FFI Pattern illustration -->
```rust
mod ffi {
    use std::os::raw::c_int;
    
    #[repr(transparent)]
    pub struct FileDescriptor(c_int);
    
    extern "C" {
        pub fn open(path: *const i8, flags: c_int) -> FileDescriptor;
        pub fn close(fd: FileDescriptor) -> c_int;
        pub fn read(fd: FileDescriptor, buf: *mut u8, len: usize) -> isize;
    }
}

// Safe wrapper
pub struct File {
    fd: ffi::FileDescriptor,
}

impl File {
    pub fn open(path: &str) -> std::io::Result<Self> {
        let c_path = std::ffi::CString::new(path)?;
        let fd = unsafe { ffi::open(c_path.as_ptr(), 0) };
        // ... error handling
        Ok(File { fd })
    }
}
```

## When to Use

| Scenario | Use `#[repr(transparent)]`? |
|----------|----------------------------|
| FFI newtype wrappers | Yes |
| Type-safe handles | Yes |
| NonZero optimization | Yes |
| Pure Rust newtypes | Optional (doesn't hurt) |
| Multi-field structs | N/A (only for single-field) |

## Related Rules
- [type-newtype-ids](./type-newtype-ids.md) - Newtype pattern
- [type-phantom-marker](./type-phantom-marker.md) - PhantomData usage
- [api-newtype-safety](./api-newtype-safety.md) - Type-safe newtypes
