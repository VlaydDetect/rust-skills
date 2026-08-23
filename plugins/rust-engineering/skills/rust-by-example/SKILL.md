---
name: rust-by-example
description: Explain Rust concepts with minimal compiling examples that expose the important type, ownership, error, or runtime behavior. Use when a concrete example is the requested output or the fastest way to test understanding; do not substitute examples for repository-specific analysis.
---

# Rust by Example

Own small, accurate, runnable examples as an explanatory and diagnostic modality. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- The user asks for an example, comparison, translation, or minimal reproduction of a Rust concept.
- A language or library rule is easier to verify with compiling code than prose alone.
- A repository issue needs an isolated example before the production design is chosen.

## Workflow

1. Identify the single concept and the assumptions the example must make about edition, MSRV, dependencies, and runtime.
2. Choose the smallest complete crate or snippet that compiles and demonstrates one observable outcome.
3. Use names that reveal ownership and state transitions; omit frameworks and abstractions unrelated to the concept.
4. Include the success case and one contrast or failure case when the distinction is the lesson.
5. Compile or otherwise validate the example under its declared toolchain and dependency set when local execution is available.
6. Explain what the example proves, what it intentionally omits, and how repository constraints could change the choice.

## Decision Rules

- A pedagogical snippet may use `unwrap` only when error handling is explicitly outside the lesson and that limitation is stated.
- Do not hide required imports, trait bounds, runtime setup, or Cargo dependencies.
- Prefer std-only examples unless the requested concept is specifically about an external crate.
- Make compile-fail examples clearly labeled and include the relevant diagnostic reason rather than presenting broken code as runnable.
- Avoid lifetimes, generics, traits, or async machinery that do not contribute to the target concept.
- Do not use unsound unsafe code for brevity.
- Keep output deterministic unless nondeterminism is itself the concept.
- Route production decisions to the responsible domain skill after the example clarifies the mechanism.

## Boundaries and Hand-offs

- Domain profiles own production policy; this profile supplies a minimal concrete demonstration.
- `rust-testing` owns repository test design; an example is not automatically an adequate regression test.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust by Example field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Huiali protocols

For source-derived detail relevant to this profile, read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference.
