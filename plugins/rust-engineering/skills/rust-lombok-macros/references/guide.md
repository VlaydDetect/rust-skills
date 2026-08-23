# Rust Lombok-Style Macros Field Guide

This guide is the detailed policy for `rust-lombok-macros`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Lombok-style generation trades visible repetitive code for an attribute contract, expansion cost, and discoverability burden.
- The macro's true product is the generated API, so documentation should show caller-visible methods and behavior.
- Constructors, builders, accessors, defaults, and validation interact with private invariants and cannot be generated safely from field syntax alone without policy.
- Conflict handling must cover inherent methods, multiple derives, field renames, skipped fields, and generated helper types.
- Generic input propagation and span preservation determine whether generated errors are understandable.
- Explicit opt-in generation reduces accidental API growth and makes SemVer review tractable.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One small data type | Write direct impl | Visible code is cheaper than macro infrastructure |
| Many uniform internal DTOs | Focused derive may help | Repetition and policy are genuinely shared |
| Fields have distinct invariants | Handwritten constructors and accessors | Uniform generation would expose invalid states |
| Existing adopted derive covers need | Reuse it | Avoids parallel annotation semantics |
| Generated public builder | Full API and SemVer review | Expansion becomes downstream contract |

## Common Failure Modes

- Generating setters for private invariant-bearing fields because they exist syntactically.
- Silently overwriting or colliding with user-defined methods.
- Dropping generic bounds, cfg attributes, docs, or visibility in generated items.
- Creating an infallible `build` that panics when required fields are absent.
- Adding a macro suite for a handful of lines in one type.

## Required Evidence

- A complete generated-API table with names, signatures, visibility, errors, defaults, and invariants.
- Compile-pass and compile-fail coverage for generics, attributes, conflicts, unsupported forms, and downstream use.
- Expanded-code and rustdoc inspection for public items and diagnostics.
- A measured or concrete repetition benefit relative to direct implementations and compile-time cost.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-lombok-macros/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
