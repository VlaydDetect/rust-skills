# unsafe-minimize-scope

> Keep `unsafe` blocks as small as possible — mark only the operation that requires unsafety, not the surrounding safe code.

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-unsafe; supporters=none; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Keep `unsafe` blocks as small as possible — mark only the operation that requires unsafety, not the surrounding safe code.

## Apply When

Apply when an unsafe operation or safe wrapper needs an explicit validity, aliasing, initialization, layout, thread, panic, or drop proof, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a safe standard-library or already accepted crate abstraction enforces the same invariant. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. List every unsafe precondition, prove each from adjacent checks or types, and minimize the operation and caller obligations.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Unsafe may unlock an ABI or measured optimization, but creates a permanent universal soundness proof obligation.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.
- Supported targets, layout or ABI contract, panic policy, and safety invariants must be explicit.

## Verification

Audit every constructor and destruction path, compile relevant targets, and run focused tests plus Miri or sanitizers where applicable.

## Why It Matters

When an entire function is marked `unsafe fn`, every line inside appears equally suspect to an auditor. Shrinking unsafe blocks to the minimum isolates exactly which operation violates Rust's safety invariants, making reviews tractable and bugs easier to find. The Rust 2024 edition enforces this with the `unsafe_op_in_unsafe_fn` lint: unsafe operations inside an `unsafe fn` now require their own explicit `unsafe {}` block rather than inheriting the function's unsafety implicitly.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Entire function body marked unsafe — safe arithmetic, bounds checks,
// and the single unsafe dereference are all equally "dangerous" to a reader.
unsafe fn sum_at(ptr: *const i32, len: usize, index: usize) -> i32 {
    let adjusted_len = len.saturating_sub(1); // safe — but looks unsafe
    assert!(index <= adjusted_len);           // safe — but looks unsafe
    let value = *ptr.add(index);              // the only actually unsafe op
    value + 1                                 // safe — but looks unsafe
}
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// Huge unsafe block wrapping safe logic inside an unsafe fn (2024 edition
// now requires unsafe {} here anyway, but large blocks are still bad style).
pub unsafe fn process(ptr: *const u8, len: usize) -> Vec<u8> {
    unsafe {
        let mut result = Vec::with_capacity(len); // safe
        for i in 0..len {                         // safe
            result.push(*ptr.add(i));             // unsafe — buried in noise
        }
        result
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// Safe wrapper: the single unsafe operation is clearly isolated.
fn sum_at(ptr: *const i32, len: usize, index: usize) -> i32 {
    assert!(index < len, "index out of bounds");
    // SAFETY: index < len guarantees ptr.add(index) is within the allocation.
    let value = unsafe { *ptr.add(index) };
    value + 1
}
```

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
// In a genuinely unsafe fn, 2024 edition still requires unsafe {} per op.
/// # Safety
///
/// `ptr` must be valid for reads for `len` bytes and properly aligned.
pub unsafe fn process(ptr: *const u8, len: usize) -> Vec<u8> {
    let mut result = Vec::with_capacity(len); // safe — outside any unsafe block
    for i in 0..len {
        // SAFETY: caller guarantees ptr is valid for len bytes; i < len.
        let byte = unsafe { *ptr.add(i) };
        result.push(byte);
    }
    result
}
```

## Key Points

- **2024 edition `unsafe_op_in_unsafe_fn`**: even inside an `unsafe fn`, each unsafe operation now needs its own `unsafe {}`. This is a hard error in Rust 2024.
- A safe wrapper around a small `unsafe {}` is almost always preferable to exposing the entire function as `unsafe fn`.
- Each small unsafe block needs its own `// SAFETY:` comment (see `unsafe-safety-comment`).
- If multiple consecutive lines are all unsafe for the *same* invariant reason, a single block covering only those lines is acceptable.

## When a Larger Block Is Acceptable

If two unsafe operations share the *exact same precondition* and separating them would require re-stating the identical justification, a single block covering both is fine — but it should still be the minimum necessary scope.

## Related Rules
- [unsafe-safety-comment](unsafe-safety-comment.md) - write `// SAFETY:` above every unsafe block
- [unsafe-send-sync-manual](unsafe-send-sync-manual.md) - document invariants when manually implementing Send/Sync
