# mem-smaller-integers

> Use appropriately-sized integers to reduce memory footprint## Decision

Consider this rule only after its prerequisites are satisfied: Use appropriately-sized integers to reduce memory footprint.

## Apply When

Apply when a measured allocation, footprint, locality, move, or layout cost is material on the representative workload, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when there is no profile or size evidence, or the change would complicate ownership, portability, or correctness for a noise-level gain. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Measure allocation or layout first, change one representation or reuse decision, and compare the same workload.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Inline storage, boxing, arenas, compact types, and reuse exchange simplicity, code size, stack use, locality, or dependency cost.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Keep correctness tests green and record before/after allocations, type size, memory footprint, or representative benchmark evidence.

## Why It Matters

Using `i64` when `i16` suffices wastes 6 bytes per value. In arrays, vectors, and structs with millions of instances, this waste compounds dramatically. Choosing the smallest integer type that fits your domain reduces memory usage and improves cache utilization.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
struct Pixel {
    r: u64,  // Color channels 0-255 = 8 bits needed
    g: u64,  // Using 64 bits = 8x waste
    b: u64,
    a: u64,
}
// Size: 32 bytes per pixel

struct HttpStatus {
    code: i32,      // HTTP codes 100-599 = 10 bits needed
    version: i32,   // HTTP 1.0, 1.1, 2, 3 = 2 bits needed
}
// Size: 8 bytes per status

struct GeoPoint {
    lat: f64,   // -90 to 90
    lon: f64,   // -180 to 180
}
// Often f32 precision is sufficient for display
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
struct Pixel {
    r: u8,
    g: u8,
    b: u8,
    a: u8,
}
// Size: 4 bytes per pixel (8x smaller!)

struct HttpStatus {
    code: u16,      // 100-599 fits in u16
    version: u8,    // 1, 2, 3 fits in u8
}
// Size: 3 bytes (+ 1 padding = 4 bytes)

struct GeoPoint {
    lat: f32,   // ~7 decimal digits precision
    lon: f32,   // Sufficient for most geo applications
}
// Size: 8 bytes vs 16 bytes
```

## Integer Size Reference

| Type | Range | Use For |
|------|-------|---------|
| `u8` | 0 to 255 | Bytes, small counts, flags |
| `i8` | -128 to 127 | Small signed values |
| `u16` | 0 to 65,535 | Port numbers, small indices |
| `i16` | -32,768 to 32,767 | Audio samples |
| `u32` | 0 to 4 billion | Array indices, timestamps (seconds) |
| `i32` | ±2 billion | General integers, file offsets |
| `u64` | 0 to 18 quintillion | Large counts, nanosecond timestamps |
| `usize` | Platform-dependent | Array indexing (required by Rust) |

## Struct Packing

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Struct Packing illustration -->
```rust
use std::mem::size_of;

// Poor ordering - 24 bytes due to padding
struct Wasteful {
    a: u8,    // 1 byte + 7 padding
    b: u64,   // 8 bytes
    c: u8,    // 1 byte + 7 padding
}
assert_eq!(size_of::<Wasteful>(), 24);

// Better ordering - 16 bytes
struct Efficient {
    b: u64,   // 8 bytes (aligned)
    a: u8,    // 1 byte
    c: u8,    // 1 byte + 6 padding
}
assert_eq!(size_of::<Efficient>(), 16);

// Even better with smaller types - 10 bytes
struct Compact {
    b: u32,   // 4 bytes (if u32 suffices)
    a: u8,    // 1 byte
    c: u8,    // 1 byte
}
assert_eq!(size_of::<Compact>(), 8);  // With padding
```

## Conversion Safety

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Conversion Safety illustration -->
```rust
// Safe: always succeeds (widening)
let small: u8 = 42;
let big: u32 = small.into();

// Fallible: may overflow (narrowing)
let big: u32 = 1000;
let small: u8 = big.try_into().expect("value out of range");

// Or use checked conversion
if let Ok(small) = u8::try_from(big) {
    use_small(small);
} else {
    handle_overflow();
}
```

## Bitflags for Boolean Sets

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bitflags for Boolean Sets illustration -->
```rust
use bitflags::bitflags;

// Instead of 8 separate bool fields (8 bytes minimum)
bitflags! {
    struct Permissions: u8 {
        const READ    = 0b0000_0001;
        const WRITE   = 0b0000_0010;
        const EXECUTE = 0b0000_0100;
        const DELETE  = 0b0000_1000;
    }
}
// All 8 flags in 1 byte!

let perms = Permissions::READ | Permissions::WRITE;
if perms.contains(Permissions::READ) {
    // ...
}
```

## NonZero Types for Option Optimization

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the NonZero Types for Option Optimization illustration -->
```rust
use std::num::NonZeroU64;

// Option<u64> = 16 bytes (no null pointer optimization)
assert_eq!(size_of::<Option<u64>>(), 16);

// Option<NonZeroU64> = 8 bytes (0 represents None)
assert_eq!(size_of::<Option<NonZeroU64>>(), 8);

let id: Option<NonZeroU64> = NonZeroU64::new(42);
```

## Related Rules
- [mem-box-large-variant](./mem-box-large-variant.md) - Optimizing enum sizes
- [mem-assert-type-size](./mem-assert-type-size.md) - Compile-time size checks
- [type-newtype-ids](./type-newtype-ids.md) - Type safety for integer IDs
- [num-nonzero](num-nonzero.md) - NonZero* niche optimization
- [num-cast-try-from](num-cast-try-from.md) - Avoid lossy `as` casts
