# Huiali references for `rust-distributed-systems`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-distributed`](huiali/rust-distributed.md) — primary; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
