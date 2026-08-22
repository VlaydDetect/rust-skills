# unsafe-safety-comment

> Write a `// SAFETY:` comment above every `unsafe` block and a `# Safety` section in every `unsafe fn`.

<!-- rulebook-meta: source=leonardomso/rust-skills@1.5.1; owner=rust-unsafe; supporters=none; status=conditional -->

## Decision

Consider this rule only after its prerequisites are satisfied: Write a `// SAFETY:` comment above every `unsafe` block and a `# Safety` section in every `unsafe fn`.

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
- External crates referenced by the source (`tokio`, `bytes`) must already be accepted by the project or be approved before addition.
- Supported targets, layout or ABI contract, panic policy, and safety invariants must be explicit.

## Verification

Audit every constructor and destruction path, compile relevant targets, and run focused tests plus Miri or sanitizers where applicable.

## Why It Matters

Unsafe blocks are unauditable without justification. A reviewer cannot verify invariants they cannot read. The `clippy::undocumented_unsafe_blocks` lint enforces this mechanically. The standard library, tokio, and bevy all require both forms before merging unsafe code.

There are two distinct levels of documentation:

1. **`# Safety` in a doc comment on an `unsafe fn`** — describes the *caller's* obligations (preconditions that must hold for the call to be sound).
2. **`// SAFETY:` inline comment above each `unsafe {}` block** — explains why *this specific operation* upholds the required invariants at the call site.

Both are required. Omitting either leaves an auditor unable to verify soundness.

## Bad

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Bad illustration -->
```rust
// unsafe fn with no # Safety section — caller has no idea what's required
pub unsafe fn read_at(ptr: *const u8, offset: usize) -> u8 {
    // no SAFETY comment — why is this dereference sound?
    unsafe { *ptr.add(offset) }
}

// standalone block with no justification
fn process(slice: &[u8]) -> u8 {
    unsafe { *slice.as_ptr().add(10) }
}
```

## Good

<!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Good illustration -->
```rust
/// Returns the byte at `ptr + offset`.
///
/// # Safety
///
/// - `ptr` must be valid for reads for at least `offset + 1` bytes.
/// - `ptr` must not be null and must be properly aligned for `u8`.
/// - The memory must not be mutated for the duration of this call.
pub unsafe fn read_at(ptr: *const u8, offset: usize) -> u8 {
    // SAFETY: caller guarantees ptr is valid for at least offset + 1 bytes,
    // so ptr.add(offset) is in bounds and dereferenceable.
    unsafe { *ptr.add(offset) }
}

fn process(slice: &[u8]) -> Option<u8> {
    if slice.len() > 10 {
        // SAFETY: we just checked that slice has at least 11 elements,
        // so index 10 is within bounds.
        Some(unsafe { *slice.as_ptr().add(10) })
    } else {
        None
    }
}
```

## Key Points

- A `# Safety` doc section and a `// SAFETY:` inline comment serve different audiences: the doc section targets *callers*, the inline comment targets *auditors* of the implementation.
- Enable the lint explicitly to catch omissions:
  <!-- rust-example: fragment; missing: surrounding domain types, functions, imports, and crate context referenced by the Key Points illustration -->
  ```rust
  #![warn(clippy::undocumented_unsafe_blocks)]
  ```
- When an unsafe block spans multiple operations, write one `// SAFETY:` comment that addresses each distinct invariant, or split into multiple smaller blocks (see `unsafe-minimize-scope`).
- In an `unsafe fn`, the body still requires `// SAFETY:` comments for each inner `unsafe {}` block under the 2024 edition's `unsafe_op_in_unsafe_fn` lint.

## Related Rules
- [unsafe-minimize-scope](unsafe-minimize-scope.md) - keep unsafe blocks as small as possible
- [lint-unsafe-doc](lint-unsafe-doc.md) - enable `clippy::undocumented_unsafe_blocks`
- [doc-safety-section](doc-safety-section.md) - include `# Safety` sections in public unsafe fns
