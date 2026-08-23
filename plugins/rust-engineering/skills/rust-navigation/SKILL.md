---
name: rust-navigation
description: Navigate Rust symbols, call paths, macro expansion, trait dispatch, module visibility, and Cargo topology efficiently. Use to locate the real definition, caller, implementation, feature gate, or generated boundary before analysis or editing.
---

# Rust Navigation

Own targeted repository navigation once the question to trace is known. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A symbol's definition, callers, trait implementation, re-export, macro origin, or feature gate is unclear.
- Text search returns aliases or generated code and the real execution path must be traced.
- The task needs a fast impact cone rather than a full onboarding map.

## Workflow

1. Turn the task into a concrete navigation question such as who constructs this type, which impl handles this call, or which feature enables this module.
2. Search exact identifiers and paths first, then aliases, trait methods, re-exports, macro invocations, and configuration names.
3. Open the definition in module context, including visibility, cfg attributes, generic bounds, and generated or included sources.
4. Trace outward to callers and inward to effects until the contract owner and affected tests are identified.
5. Cross-check Cargo targets, features, build scripts, and proc macros when source presence does not imply compiled presence.
6. Return a compact path map with file and symbol evidence, uncertainty, and the next smallest file set to inspect.

## Decision Rules

- Use `rg` or repository indexes for candidates, but confirm semantic relationships in source.
- A same-named method may resolve through inherent impl, trait impl, deref coercion, or macro expansion; do not infer from text alone.
- Follow `pub use`, module aliases, and crate renames before declaring a definition unused.
- Account for `cfg`, target-specific modules, feature gates, and test-only implementations.
- Treat generated files as navigation nodes, not edit targets; locate their generator and input.
- For dynamic dispatch, identify the trait-object construction sites and every relevant implementer.
- For macros, inspect invocation, exported name, expansion contract, and generated item names.
- Stop when the task's behavior path and ownership boundary are proven; do not catalogue unrelated matches.

## Boundaries and Hand-offs

- `codebase-onboarding` owns the first broad repository map; navigation answers a bounded path question.
- `rust-module-layout` owns designing module structure; navigation observes the current structure.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Navigation field guide](references/guide.md) before making a consequential design choice. Load exactly one mode from the [Design protocol navigation index](./references/guide.md) for definitions, symbols, traits, calls, or dependencies. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
