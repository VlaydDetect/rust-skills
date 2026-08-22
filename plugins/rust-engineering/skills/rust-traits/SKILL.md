---
name: rust-traits
description: Design Rust traits, generics, bounds, static or dynamic dispatch, associated types, object-safe APIs, newtypes, typestates, and extension points. Use when abstraction or type-system structure is the controlling decision.
---

# Rust Traits and Type-Driven Design

Own trait contracts, dispatch choice, coherence, and type-driven invariant encoding. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- An API needs polymorphism, an extension point, generic bounds, associated types, or trait objects.
- Compiler errors involve object safety, coherence, orphan rules, inference, or unsatisfied bounds.
- A state machine or validated value may benefit from newtype or typestate encoding.

## Workflow

1. Name the behavior and its current independent implementations or consumers before defining a trait.
2. Decide whether variation is compile-time, runtime, closed-set, or not actually required.
3. Design the smallest semantic method set with documented invariants, ownership, errors, and concurrency expectations.
4. Choose generic parameters, associated types, `impl Trait`, trait objects, or enums based on caller knowledge and compatibility needs.
5. Check object safety, coherence, blanket impl overlap, auto traits, and downstream extension consequences.
6. Test representative implementations and compile-time constraints; document sealing or extension policy.

## Decision Rules

- Do not introduce a trait solely to mock one implementation; use a function, closure, concrete fake, or boundary-specific trait when simpler.
- Prefer associated types when one implementation has one natural output type; use generic methods when callers choose the type.
- Static dispatch improves specialization and inlining but multiplies monomorphization; dynamic dispatch gives runtime heterogeneity and a stable erased boundary.
- Use an enum for a closed set of variants when exhaustive matching is a feature.
- The orphan rule may require a local newtype; do not fork external traits or types to bypass coherence.
- Sealed traits intentionally reserve implementations; state that compatibility decision.
- Supertraits and broad bounds are public constraints and should reflect actual semantic requirements.
- Typestate is valuable when invalid sequences are costly and states remain manageable; avoid exponential generic state for simple validation.

## Boundaries and Hand-offs

- `rust-api-design` owns the broader public contract; traits are one representation of it.
- `rust-macros` owns code generation when repetitive trait implementations justify generation.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Traits and Type-Driven Design field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
