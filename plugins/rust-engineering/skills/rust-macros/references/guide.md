# Rust Macros Field Guide

This guide is the detailed policy for `rust-macros`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Declarative macros match token trees with fragment specifiers and repetition; proc macros transform token streams using compiler invocation boundaries.
- Hygiene governs how identifiers resolve between definition and invocation contexts; paths and generated names need deliberate ownership.
- Spans determine where compiler diagnostics point and materially affect user experience.
- Expansion is part of downstream compile behavior, public API, lint behavior, and compile time.
- Trybuild-style compile cases can validate accepted and rejected syntax and diagnostics without exposing implementation internals.
- Macro grammar should remain narrow and Rust-like; inventing a language creates parser, tooling, documentation, and compatibility obligations.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Reusable runtime behavior | Function, trait, or generic | Ordinary Rust is type-checked and easier to navigate |
| Simple syntactic repetition | macro_rules | No proc-macro crate or parser needed |
| Derive from item structure | Proc-macro derive | Structured input drives generated impls |
| Validate or transform annotated item | Attribute macro | The item itself is the input boundary |
| Generate from external schema | Build-time generator | Token macros may be the wrong source-of-truth boundary |

## Common Failure Modes

- Creating a custom DSL when ordinary Rust syntax and a helper API suffice.
- Using absolute crate-name paths that fail when downstream dependencies are renamed.
- Panicking or emitting errors at call-site root rather than the offending token.
- Generating public names or impls that collide without a documented policy.
- Testing only one happy expansion and missing invalid syntax or cross-crate behavior.

## Required Evidence

- Valid and invalid invocation examples plus the intended expansion or generated contract.
- Compile-pass and compile-fail tests, cross-crate invocation, crate rename, and relevant feature cases.
- Expanded-code inspection for hygiene, evaluation count, visibility, unsafe, and public API.
- Compile-time measurements when the macro is broad, recursive, dependency-heavy, or widely invoked.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-macros/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-macro`](./macro.md) — primary; macro_rules!, derive, attribute and function-like procedural macros, token handling, hygiene, diagnostics, expansion, and compile-time tests.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
