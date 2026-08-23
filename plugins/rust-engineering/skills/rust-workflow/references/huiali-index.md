# Huiali references for `rust-workflow`

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-skill`](huiali/rust-skill.md) — primary; Problem-first classification, uncertainty reduction, owner selection, supporting constraints, and verification handoff.
- [`rust-skill-index`](huiali/rust-skill-index.md) — primary; Precise symptom-to-profile lookup, negative routing, manual invocation, and escalation from mechanics to design or domain reasoning.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
