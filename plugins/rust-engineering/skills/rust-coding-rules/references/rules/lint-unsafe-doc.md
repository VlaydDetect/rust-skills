# lint-unsafe-doc

> Require documentation for unsafe blocks## Decision

Consider this rule only after its prerequisites are satisfied: Require documentation for unsafe blocks.

## Apply When

Apply when the repository needs a scoped formatting, lint, warning-level, cfg, or CI policy under its actual toolchain, and current code establishes the premise described below.

## Avoid When

Do not apply mechanically when a broad lint group or automatic fix would change API, MSRV, semantics, generated code, or unrelated dirty files. A conflicting project contract or owner-profile decision wins.

## Algorithm

1. Inspect the actual callers, invariants, repository instructions, toolchain, target, features, and accepted dependencies.
2. Confirm the concrete trigger for this rule; a keyword or hypothetical future need is insufficient.
3. Reproduce the exact lint, classify it, fix semantic causes individually, and use the narrowest documented allow for intentional exceptions.
4. Implement the smallest coherent option, compare material alternatives, and run evidence that can falsify the decision.

## Trade-offs

Stricter lint policy catches defects earlier but increases toolchain churn, exception maintenance, and migration work.

## Prerequisites

- The user and project contract, actual callers, edition, MSRV, toolchain, target, and feature matrix take precedence over this rule.
- External crates referenced by the source (`bytes`) must already be accepted by the project or be approved before addition.

## Verification

Run the configured format and Clippy gate with exact packages, targets, features, and toolchain; separate baseline failures.

## Why It Matters

The `undocumented_unsafe_blocks` lint ensures every unsafe block has a `// SAFETY:` comment explaining why the operation is sound. Unsafe code is the source of most memory safety bugs—documenting invariants catches mistakes and helps reviewers.

## Configuration

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Configuration illustration -->
```rust
#![warn(clippy::undocumented_unsafe_blocks)]
```

Or in `Cargo.toml`:

```toml
[lints.clippy]
undocumented_unsafe_blocks = "warn"
```

For strict enforcement:

```toml
[lints.clippy]
undocumented_unsafe_blocks = "deny"
```

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
pub fn read_data(ptr: *const u8, len: usize) -> &[u8] {
    unsafe {
        std::slice::from_raw_parts(ptr, len)  // WARN: undocumented
    }
}

impl Buffer {
    pub fn get_unchecked(&self, index: usize) -> &u8 {
        unsafe { self.data.get_unchecked(index) }  // WARN
    }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
pub fn read_data(ptr: *const u8, len: usize) -> &[u8] {
    // SAFETY: Caller guarantees:
    // - ptr is valid for reads of len bytes
    // - ptr is properly aligned for u8
    // - the memory is initialized
    // - no mutable references exist to this memory
    unsafe {
        std::slice::from_raw_parts(ptr, len)
    }
}

impl Buffer {
    pub fn get_unchecked(&self, index: usize) -> &u8 {
        debug_assert!(index < self.len(), "index out of bounds");
        // SAFETY: We verified index < len in debug builds.
        // Callers must ensure index is within bounds.
        unsafe { self.data.get_unchecked(index) }
    }
}
```

## SAFETY Comment Format

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the SAFETY Comment Format illustration -->
```rust
// SAFETY: <explanation of why this is sound>
unsafe {
    // ...
}
```

The comment should explain:
1. **What invariants are upheld** - preconditions that make this safe
2. **Why the invariants hold** - how you know they're satisfied
3. **What could go wrong** - if invariants are violated

## Examples by Category

### Pointer Operations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Pointer Operations illustration -->
```rust
// SAFETY: ptr was obtained from Box::into_raw, so it's valid
// and properly aligned. We're taking back ownership.
let boxed = unsafe { Box::from_raw(ptr) };
```

### Unchecked Operations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Unchecked Operations illustration -->
```rust
// SAFETY: We just checked that i < self.len() above.
// The bounds check cannot be elided by the optimizer
// because len() is not inlined.
unsafe { self.data.get_unchecked(i) }
```

### FFI Calls

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the FFI Calls illustration -->
```rust
// SAFETY: libc::getenv is safe to call with a null-terminated
// string. We ensure null termination with CString::new.
// The returned pointer is valid for the lifetime of the environment.
let value = unsafe { libc::getenv(key.as_ptr()) };
```

### Trait Implementations

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Trait Implementations illustration -->
```rust
// SAFETY: MyType contains no pointers or interior mutability,
// and all bit patterns are valid MyType values.
unsafe impl Send for MyType {}
unsafe impl Sync for MyType {}
```

## Related Lints

```toml
[lints.clippy]
undocumented_unsafe_blocks = "warn"
# Also consider:
multiple_unsafe_ops_per_block = "warn"  # One operation per block
```

## Related Rules
- [doc-safety-section](./doc-safety-section.md) - `# Safety` in docs
- [lint-deny-correctness](./lint-deny-correctness.md) - Correctness lints
- [type-repr-transparent](./type-repr-transparent.md) - FFI safety
