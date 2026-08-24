---
name: rust-lombok-macros
description: Evaluate and implement Lombok-style Rust derives or attributes for constructors, builders, getters, setters, defaults, display, validation, and boilerplate. Use when a project specifically wants annotation-driven data-type generation.
---

# Rust Lombok-Style Macros

Own annotation-driven boilerplate generation and the explicit API it creates. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- The task references Lombok-like Rust macros or wants generated constructors, accessors, builders, defaults, display, or validation.
- A derive or attribute suite generates broad user-facing APIs from struct or enum declarations.
- Generated boilerplate needs conflict, visibility, generics, diagnostics, or compatibility policy.

## Workflow

1. Confirm that ordinary derives, direct impls, a small helper, or an existing adopted macro do not already cover the current repetition.
2. List every generated item, signature, visibility, ownership behavior, default, validation, and naming rule from a caller perspective.
3. Design opt-in attributes and conflict rules; avoid surprising generation from bare derive names.
4. Support structs, fields, generics, where clauses, lifetimes, cfg attributes, docs, and visibility only to the declared scope.
5. Emit precise diagnostics for unsupported forms, duplicate names, incompatible attributes, and invalid configuration.
6. Test expanded API, compile failures, rustdoc, downstream use, SemVer implications, and compile-time cost.

## Decision Rules

- Generated setters and getters must respect ownership and invariants; not every field should be publicly mutable.
- A generated builder must define required fields, defaults, repeated calls, validation timing, and final error type.
- Do not generate names that collide silently with user implementations; define override or skip behavior.
- Preserve generics, lifetimes, where clauses, visibility, cfg, and documentation deliberately.
- Display and Debug generation have different audience and stability expectations.
- Validation macros must not hide fallible construction behind an infallible API.
- Generated public items are ordinary SemVer surface and need documentation and tests.
- Keep feature combinations and macro dependencies small; boilerplate savings can be outweighed by compile-time and discoverability cost.

## Boundaries and Hand-offs

- `rust-macros` owns general proc-macro parsing, spans, hygiene, and testing mechanics.
- `rust-api-design` owns whether the generated public API is desirable independent of implementation convenience.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Lombok-Style Macros field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
