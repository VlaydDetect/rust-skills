# opt-likely-hint

> Use code structure to hint at likely branches; use intrinsics on nightly

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-performance; supporters=`rust-cargo-build`, `rust-stable`; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Use code structure to hint at likely branches; use intrinsics on nightly.

## Apply When

Apply when a reproducible profile or benchmark identifies a compiler, codegen, branch, cache, or target-specific bottleneck, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the workload, deployment target, or portability contract is unknown, or the expected benefit is speculative. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Hold toolchain, target, profile, features, inputs, and hardware constant; test one optimization hypothesis at a time.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Bad

Applying the headline as a universal rewrite without proving its premise, prerequisites, and caller-visible effects.

## Good

Apply the rule only to the demonstrated boundary, preserve the controlling contract, and retain evidence for the changed property.

## Trade-offs

LTO, codegen, inlining, PGO, SIMD, and target tuning can trade build time, size, portability, debuggability, and determinism.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Compare repeated release-like measurements and artifact or codegen evidence while preserving functional behavior and fallback targets.

## Why It Matters

Modern CPUs predict branches to speculatively execute code. Mispredictions cause pipeline stalls (10-20 cycles). Helping the compiler understand which branches are likely allows it to generate optimal code layout and branch hints, improving performance in hot paths.

## Stable Rust: Code Structure Hints

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Stable Rust: Code Structure Hints illustration -->
```rust
// Pattern 1: Early returns for unlikely cases
fn process(data: Option<&Data>) -> i32 {
    // Compiler assumes early return is "unlikely"
    let data = match data {
        None => return 0,  // Unlikely
        Some(d) => d,
    };
    
    // Hot path continues here
    complex_processing(data)
}

// Pattern 2: if-else ordering
fn calculate(x: i32) -> i32 {
    if x >= 0 {
        // Put likely case in "if" branch
        x * 2
    } else {
        // Unlikely case in "else"
        handle_negative(x)
    }
}

// Pattern 3: Cold function extraction
fn hot_path(data: &[u8]) -> Result<(), Error> {
    if data.is_empty() {
        return cold_empty_error();  // Extracted = unlikely
    }
    
    process_fast(data)
}

#[cold]
fn cold_empty_error() -> Result<(), Error> {
    Err(Error::EmptyInput)
}
```

## Nightly: std::hint

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Nightly: std::hint illustration -->
```rust
// Requires nightly; still unstable as of Rust 1.96
#![feature(likely_unlikely)]
use std::hint::{likely, unlikely};

fn process(data: &Data) -> i32 {
    if unlikely(data.is_corrupted()) {
        return handle_corruption(data);
    }
    
    if likely(data.is_cached()) {
        return fast_cached_path(data);
    }
    
    slow_uncached_path(data)
}
```

## Boolean Likely Wrapper (Nightly)

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Boolean Likely Wrapper (Nightly) illustration -->
```rust
// Requires nightly; still unstable as of Rust 1.96
#![feature(likely_unlikely)]

#[inline(always)]
fn likely(b: bool) -> bool {
    std::hint::likely(b)
}

#[inline(always)]
fn unlikely(b: bool) -> bool {
    std::hint::unlikely(b)
}

// Usage
if likely(x > 0) {
    hot_path(x)
} else {
    cold_path(x)
}
```

## Stable: std::hint::cold_path

`std::hint::cold_path()` (stable since Rust 1.95) marks the enclosing code path as unlikely so the optimizer can deprioritize it — a stable substitute for nightly `unlikely`. Call it inside the rarely-taken branch:

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Stable: std::hint::coldpath illustration -->
```rust
fn process(data: &Data) -> i32 {
    if data.is_corrupted() {
        std::hint::cold_path(); // tell the optimizer this branch is rare
        return handle_corruption(data);
    }
    fast_path(data)
}
```

## Stable: likely-stable Crate

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Stable: likely-stable Crate illustration -->
```rust
use likely_stable::{likely, unlikely};

fn check(value: i32) -> bool {
    if unlikely(value < 0) {
        handle_negative()
    } else if likely(value < 1000) {
        handle_common()
    } else {
        handle_large()
    }
}
```

## Loop Optimization

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Loop Optimization illustration -->
```rust
fn search(data: &[i32], target: i32) -> Option<usize> {
    for (i, &item) in data.iter().enumerate() {
        // Assume most iterations DON'T find the target
        if unlikely(item == target) {
            return Some(i);
        }
    }
    None
}

// Alternative: structure for likely case
fn search_common(data: &[i32], target: i32) -> Option<usize> {
    // If target is usually found
    for (i, &item) in data.iter().enumerate() {
        if likely(item == target) {
            return Some(i);
        }
    }
    None
}
```

## Match Arm Ordering

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Match Arm Ordering illustration -->
```rust
// Put most common variants first
fn process_message(msg: Message) {
    match msg {
        // Most common - listed first
        Message::Data(d) => handle_data(d),
        Message::Heartbeat => (), // Second most common
        
        // Rare cases last
        Message::Error(e) => handle_error(e),
        Message::Shutdown => shutdown(),
    }
}
```

## Benchmark-Driven Hints

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Benchmark-Driven Hints illustration -->
```rust
// Profile first to know which branches are actually likely!
fn speculative(x: i32) -> i32 {
    // DON'T GUESS - measure with profiling
    // perf record / perf report
    // cargo flamegraph
    
    if x > threshold {  // Is this actually common?
        path_a(x)
    } else {
        path_b(x)
    }
}
```

## Related Rules
- [opt-cold-unlikely](./opt-cold-unlikely.md) - #[cold] for unlikely functions
- [opt-inline-never-cold](./opt-inline-never-cold.md) - Keeping cold code separate
- [perf-profile-first](./perf-profile-first.md) - Profile to know what's likely
