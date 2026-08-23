---
name: rust-macros
description: Design and debug declarative and procedural Rust macros with stable syntax, hygienic expansion, useful diagnostics, bounded compile-time cost, and testable generated contracts. Use when code generation is necessary and ordinary Rust abstractions do not suffice.
---

# Rust Macros

Own macro syntax, expansion contracts, hygiene, diagnostics, and compile-time behavior. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A `macro_rules!`, derive, attribute, or function-like proc macro is being created, changed, or debugged.
- Generated item names, hygiene, spans, token parsing, recursion, or diagnostics affect users.
- Repetition may justify compile-time generation after functions, traits, generics, and build-time data generation are considered.

## Workflow

1. State the repetition or syntax problem and show why functions, traits, generics, derives already present, or build scripts do not solve it more simply.
2. Design the smallest invocation grammar with representative valid and invalid examples and a clear expansion contract.
3. For declarative macros, control fragment specifiers, repetition, hygiene, `crate` paths, recursion, and evaluation count.
4. For proc macros, parse structured syntax, preserve useful spans, aggregate actionable diagnostics, and separate parsing from expansion.
5. Inspect expanded code and test runtime behavior, compile-pass, compile-fail, crate renaming, feature combinations, and cross-crate use.
6. Measure compile-time impact for widely used or complex macros and document generated public API and compatibility.

## Decision Rules

- Do not create a macro merely to save a few repeated lines when a function or ordinary type remains clearer.
- Evaluate each macro argument once unless repetition is explicitly documented and safe.
- Use `crate` for internal declarative-macro paths so downstream crate renaming does not break expansion.
- Proc macros should emit diagnostics at the most relevant input span and avoid panicking on user syntax.
- Generated identifiers and public items are compatibility surface even when users do not see source expansion directly.
- Keep proc-macro dependencies and parsing work proportionate because they affect clean builds and tool responsiveness.
- Test failure messages as categories and spans where possible, not brittle full compiler output.
- Document hygiene, supported item forms, attribute interactions, and expansion side effects.

## Rulebook Overlay

After ordinary Rust alternatives are rejected and the expansion contract is written, select only relevant IDs from the [`macro-` index](../rust-coding-rules/references/categories/macro.md). Proc-macro dependency examples do not authorize crate adoption.

## Boundaries and Hand-offs

- `rust-lombok-macros` owns Java-Lombok-style derive and boilerplate-generator decisions.
- `rust-cargo-build` owns build scripts and generated files when token-level Rust integration is unnecessary.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Macros field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
