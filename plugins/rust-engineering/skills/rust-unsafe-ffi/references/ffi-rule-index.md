# Design protocol FFI rule index

The 18 retained rules are adversarial review prompts. Apply the product note at
the top of each file and prove the actual ABI, header, target, ownership,
threading, panic, and lifecycle contract.

| ID | Review question |
|---|---|
| [`ffi-01`](./rules/ffi-01-no-string-direct.md) | What exact foreign string representation is required? |
| [`ffi-02`](./rules/ffi-02-read-ffi-docs.md) | Do the chosen FFI types match lifetime and ownership semantics? |
| [`ffi-03`](./rules/ffi-03-drop-for-c-ptr.md) | Does the owning wrapper call the matching destructor exactly once? |
| [`ffi-04`](./rules/ffi-04-panic-boundary.md) | What happens for panic, abort, unwind, and foreign exceptions? |
| [`ffi-05`](./rules/ffi-05-portable-types.md) | Do bindings match the target header instead of assumed C widths? |
| [`ffi-06`](./rules/ffi-06-string-abi.md) | Are encoding, termination, allocation, and destruction paired? |
| [`ffi-07`](./rules/ffi-07-no-drop-external.md) | Who owns the resource at every transfer point? |
| [`ffi-08`](./rules/ffi-08-error-handling.md) | Is the error and output representation stable and fully documented? |
| [`ffi-09`](./rules/ffi-09-ref-not-ptr.md) | Can a safe wrapper enforce non-retention, aliasing, and lifetime rules? |
| [`ffi-10`](./rules/ffi-10-thread-safety.md) | Is concurrency or thread affinity explicit and enforced? |
| [`ffi-11`](./rules/ffi-11-packed-ub.md) | Does packed-field access avoid creating misaligned references? |
| [`ffi-12`](./rules/ffi-12-invariant-doc.md) | Which foreign-input invariants are checked and which remain unsafe? |
| [`ffi-13`](./rules/ffi-13-data-layout.md) | Does layout match the header on every supported target? |
| [`ffi-14`](./rules/ffi-14-stable-layout.md) | Is the ABI representation versioned and independent of Rust internals? |
| [`ffi-15`](./rules/ffi-15-validate-external.md) | Are discriminants, strings, sizes, and pointer contracts validated? |
| [`ffi-16`](./rules/ffi-16-closure-to-c.md) | Are callback storage, races, reentrancy, panic, and deregistration sound? |
| [`ffi-17`](./rules/ffi-17-opaque-types.md) | Do distinct opaque handles preserve the foreign header's type model? |
| [`ffi-18`](./rules/ffi-18-no-trait-objects.md) | Is a manual callback or vtable ABI monomorphic and versioned? |

## Current compiler checks

For a toolchain that provides them, evaluate these compiler lints in addition
to the retained rules:

- [`invalid_runtime_symbol_definitions`](https://doc.rust-lang.org/rustc/lints/listing/deny-by-default.html#invalid-runtime-symbol-definitions)
  and [`suspicious_runtime_symbol_definitions`](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#suspicious-runtime-symbol-definitions)
  for reserved runtime symbols;
- [`c_void_returns`](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html#c-void-returns)
  for foreign declarations that return `c_void`;
- Edition 2024 unsafe extern blocks and unsafe exported attributes;
- the repository's existing `improper_ctypes` and `improper_ctypes_definitions`
  policy.

Do not set lint levels globally from this document. Confirm availability with
the selected toolchain and apply the repository lint contract.

## Canonical rulebook cross-links

Prefer the existing canonical IDs when reporting the same finding:

| Concern | Canonical product rule |
|---|---|
| Foreign declarations in Edition 2024 | `unsafe-extern-block` |
| Exported unsafe attributes | `unsafe-no-mangle-unsafe` |
| Local unsafe proof | `unsafe-safety-comment` |
| Manual Send or Sync | `unsafe-send-sync-manual` |
| Miri coverage | `unsafe-miri-ci` |

See the [retained FFI pattern corpus](./examples/ffi-patterns.md). It is a review
corpus, not compile-tested golden code.
