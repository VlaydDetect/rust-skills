# Huiali references for `rust-ml`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-gpu`](../../rust-gpu/references/huiali/rust-gpu.md) — supporting; Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
