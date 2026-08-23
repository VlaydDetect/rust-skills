# Huiali references for `rust-unsafe-ffi`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-ffi`](huiali/rust-ffi.md) — primary; ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
