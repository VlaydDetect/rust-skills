---
name: specs
description: Turn product intent into precise Rust-facing specifications, examples, and acceptance scenarios with explicit boundaries and observables. Use when behavior is ambiguous, a feature needs a contract, or implementation and tests need a shared source of truth.
---

# Executable Specifications

Own behavioral specification and acceptance scenarios before implementation details dominate. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- A requested feature has ambiguous terms, edge cases, errors, ordering, persistence, compatibility, or authorization rules.
- The team needs Given-When-Then scenarios, acceptance criteria, or a normative contract for Rust implementation.
- Tests and documentation disagree because no explicit behavioral source of truth exists.

## Workflow

1. Identify actors, boundary, inputs, preconditions, observable outputs, state transitions, errors, and non-goals.
2. Define domain terms independently of current type or function names unless those names are themselves public contract.
3. Write a rule model, representative examples, and declarative Given-When-Then scenarios covering success, boundary, and failure cases.
4. Separate normative behavior from implementation plan, internal representation, performance tactics, and test harness mechanics.
5. Resolve contradictions and missing product decisions explicitly; do not encode them as accidental test assumptions.
6. Map each normative rule to acceptance evidence and record which requirements remain non-executable or environment-dependent.

## Decision Rules

- Use RFC 2119-style force only when the document is normative and the obligation has an owner.
- Scenarios must describe observable behavior, not private method calls or a chosen data structure.
- Keep each scenario independent and deterministic; name necessary shared state as a precondition.
- Specify error category and externally visible payload constraints without freezing incidental formatting unless required.
- State ordering, equality, time, numeric, concurrency, and retry semantics when they affect callers.
- Distinguish unsupported, invalid, unavailable, and temporarily failed outcomes.
- Include explicit non-goals to prevent implementation scope from expanding through inference.
- When the existing implementation is evidence rather than authority, label observed behavior separately from desired behavior.

## Boundaries and Hand-offs

- `rust-api-design` owns turning an accepted contract into a public Rust API shape.
- `rust-testing` owns test structure and techniques; this profile owns what behavior those tests must demonstrate.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Executable Specifications field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
