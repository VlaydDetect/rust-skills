---
name: rust-idioms
description: Apply established Rust patterns and reject common anti-patterns while respecting the repository's edition, MSRV, API, and performance needs. Use when code is correct but its Rust expression, maintainability, or conventional structure is under review.
---

# Rust Idioms

Own idiomatic expression and pattern selection below the architecture and public-contract level. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- Code needs a Rust-native simplification or an anti-pattern assessment.
- A design uses excessive cloning, indexing, boolean flags, broad mutability, panics, or Java-style abstraction.
- Several valid implementations differ mainly in readability and alignment with Rust conventions.

## Workflow

1. Confirm behavior, public contract, MSRV, and performance sensitivity before changing expression style.
2. Identify the local smell and the invariant it obscures rather than applying a global stylistic rule.
3. Choose a standard Rust pattern that makes ownership, state, errors, or iteration more explicit with less machinery.
4. Check whether the proposed idiom changes allocation, ordering, short-circuiting, panic, drop timing, or borrow scope.
5. Apply the smallest coherent rewrite and keep repository conventions where they remain sound.
6. Use compiler, Clippy, tests, and benchmarks only for the properties they can actually demonstrate.

## Decision Rules

- Prefer iterators when they clarify transformation, but use an ordinary loop when control flow is clearer.
- Model meaningful states with enums or types instead of interacting boolean flags.
- Use `?` for propagation when no boundary-specific context or recovery is required.
- Prefer borrowing over cloning, but clone explicitly when independent ownership is the intended behavior.
- Avoid indexing collections when iteration or checked access better represents bounds behavior.
- Use newtypes for domain invariants and units when primitive confusion is a real risk.
- Keep constructors and builders proportionate; builders help many optional or validated fields, not trivial structs.
- Do not turn a Clippy suggestion into policy without checking readability, MSRV, public compatibility, and local exceptions.

## Rulebook Overlay

After confirming behavior and local convention, select only relevant IDs from [`num-`](../rust-coding-rules/references/categories/num.md), [`pat-`](../rust-coding-rules/references/categories/pat.md), or [`anti-`](../rust-coding-rules/references/categories/anti.md). Alias anti-rules resolve to their canonical owner and must not duplicate findings.

## Boundaries and Hand-offs

- `rust-style-clippy` owns formatting and lint configuration; idioms own semantic code patterns.
- `rust-api-design` and `rust-architecture` own public and system-level structure even when idioms inform them.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Idioms field guide](references/guide.md) before making a consequential design choice. Use the [Actionbook anti-pattern protocol](references/actionbook-index.md) for detailed diagnostic examples without treating pattern names as findings. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
