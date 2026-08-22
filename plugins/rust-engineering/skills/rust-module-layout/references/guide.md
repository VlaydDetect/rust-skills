# Rust Module Layout Field Guide

This guide is the detailed policy for `rust-module-layout`. It synthesizes the full-stack module-layout skill and its detailed module, visibility, testing, facade, and generated-code references; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Crate roots establish the module tree; source files are one representation of that tree.
- Visibility is relative to the module hierarchy and can be restricted to crate, parent, or an ancestor path.
- Re-exports create facade APIs and can preserve stable downstream imports while implementation moves.
- Conditional modules can provide platform implementations behind one stable facade.
- Unit tests compile within the crate and can access private items by placement; integration tests are separate crates using public API.
- Cohesion and ownership are stronger layout criteria than alphabetical grouping or fixed file size.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One cohesive concept, several private helpers | Module with private submodules | Preserves one public owner |
| Stable public facade, changing internals | Crate-root re-exports | Decouples downstream paths from files |
| Target-specific implementation | Cfg-selected private modules plus facade | Callers see one contract |
| Helper used by sibling modules | Narrow common owner or `pub(super)` | Avoids crate-wide visibility |
| Independent release or target needed | Evaluate workspace crate | Module boundaries cannot isolate compilation or publication |

## Common Failure Modes

- Making every item `pub(crate)` to bypass ownership decisions.
- Exposing a deep implementation path and later treating source movement as internal.
- Creating a `utils` module with unrelated functions and no semantic owner.
- Moving tests away from private code and compensating by widening production visibility.
- Editing generated Rust instead of its schema, template, or build step.

## Required Evidence

- A module and visibility map for the affected crate, including cfg and generated variants.
- Public import paths before and after the change.
- Reason for each widened visibility and each new submodule boundary.
- Compilation, tests, rustdoc links, and examples for affected configurations.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-module-layout/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
