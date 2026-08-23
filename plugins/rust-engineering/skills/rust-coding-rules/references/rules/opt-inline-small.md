# opt-inline-small

> Use `#[inline]` for small hot functions## Decision

Consider this rule only after its prerequisites are satisfied: Use `#[inline]` for small hot functions.

## Apply When

Apply when a reproducible profile or benchmark identifies a compiler, codegen, branch, cache, or target-specific bottleneck, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when the workload, deployment target, or portability contract is unknown, or the expected benefit is speculative. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Hold toolchain, target, profile, features, inputs, and hardware constant; test one optimization hypothesis at a time.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

LTO, codegen, inlining, PGO, SIMD, and target tuning can trade build time, size, portability, debuggability, and determinism.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- A representative measurement must identify the relevant hot path, allocation, footprint, contention, or artifact constraint.

## Verification

Compare repeated release-like measurements and artifact or codegen evidence while preserving functional behavior and fallback targets.

## Why It Matters

Function call overhead (stack frame setup, register saves, jumps) can dominate small functions. Inlining eliminates this overhead and enables further optimizations by the compiler. The compiler often inlines automatically, but hints help for cross-crate calls.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Small hot function without inline hint
// May not be inlined across crate boundaries
fn is_ascii_digit(b: u8) -> bool {
    b >= b'0' && b <= b'9'
}

// Called millions of times
for byte in data {
    if is_ascii_digit(*byte) {  // Function call overhead
        count += 1;
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
#[inline]
fn is_ascii_digit(b: u8) -> bool {
    b >= b'0' && b <= b'9'
}

// Now the compiler will inline this
for byte in data {
    if is_ascii_digit(*byte) {  // Inlined, no call overhead
        count += 1;
    }
}
```

## Inline Attributes

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Inline Attributes illustration -->
```rust
// No attribute - compiler decides (usually good for same-crate)
fn auto_decide() { }

// Suggest inlining - helps cross-crate
#[inline]
fn suggest_inline() { }

// Strongly suggest inlining - almost always inlined
#[inline(always)]
fn force_inline() { }

// Strongly suggest NOT inlining - for large/cold code
#[inline(never)]
fn prevent_inline() { }
```

## When to Use Each

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the When to Use Each illustration -->
```rust
// #[inline] - Small functions, especially in libraries
#[inline]
pub fn len(&self) -> usize {
    self.inner.len()
}

// #[inline(always)] - Critical hot path, verified by profiling
#[inline(always)]
fn hot_inner_loop_helper(x: u32) -> u32 {
    x.wrapping_mul(0x9E3779B9)
}

// #[inline(never)] - Error handlers, cold paths
#[inline(never)]
fn handle_error(err: Error) -> ! {
    eprintln!("Fatal: {}", err);
    std::process::exit(1);
}

// No attribute - large functions, infrequent calls
fn complex_processing(data: &mut Data) {
    // Many lines of code...
}
```

## Evidence from ripgrep

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Evidence from ripgrep illustration -->
```rust
// https://github.com/BurntSushi/ripgrep/blob/master/crates/printer/src/standard.rs

#[inline(always)]
fn write_prelude(
    &self,
    absolute_byte_offset: u64,
    line_number: Option<u64>,
    column: Option<u64>,
) -> io::Result<()> {
    // Hot path in printing matches
}

#[inline(always)]
fn write_line(&self, line: &[u8]) -> io::Result<()> {
    // Called for every line
}
```

## Generic Functions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Generic Functions illustration -->
```rust
// Generic functions are already candidates for per-monomorphization inlining
// But #[inline] helps ensure it across crates

#[inline]
pub fn min<T: Ord>(a: T, b: T) -> T {
    if a < b { a } else { b }
}
```

## Cautions

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Cautions illustration -->
```rust
// DON'T inline large functions - hurts instruction cache
#[inline(always)]  // BAD for large function
fn large_complex_function(data: &mut [u8]) {
    // 100+ lines of code
    // Inlining bloats every call site
}

// DON'T assume inlining always helps - measure!
// Sometimes the compiler makes better decisions

// Cross-crate inlining requires #[inline] on each function
// Without LTO, a function body is not available to other crates unless
// it carries #[inline]. Within a single crate (or with LTO enabled),
// the compiler may still inline `inner` transitively after inlining
// `outer`, but this is not guaranteed — verify hot code with assembly.
#[inline]
fn outer() {
    inner();
}

fn inner() { }  // May not be inlined at outer's call sites across crate boundaries without #[inline]
```

## Verifying Inlining

```bash
# Check if function was inlined using Cachegrind
# Non-inlined functions show entry/exit counts

# Or examine assembly
cargo rustc --release -- --emit=asm
# Look for call instructions vs inlined code
```

## Related Rules
- [opt-inline-always-rare](opt-inline-always-rare.md) - Use #[inline(always)] sparingly
- [opt-inline-never-cold](opt-inline-never-cold.md) - Use #[inline(never)] for cold paths
- [opt-cold-unlikely](opt-cold-unlikely.md) - Use #[cold] for unlikely paths
- [opt-lto-release](opt-lto-release.md) - LTO enables cross-crate inlining
