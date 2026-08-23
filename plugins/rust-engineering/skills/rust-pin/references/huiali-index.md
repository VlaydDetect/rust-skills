# Huiali references for `rust-pin`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-coroutine`](../../rust-concurrency/references/huiali/rust-coroutine.md) — supporting; Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.
- [`rust-pin`](huiali/rust-pin.md) — primary; Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
