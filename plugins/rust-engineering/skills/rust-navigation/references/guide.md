# Rust Navigation Field Guide

This guide is the detailed policy for `rust-navigation`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Rust navigation crosses lexical, type, macro, and configuration graphs; no single text search represents all four.
- Definitions can be exposed through re-exports that define the public path independently of the source path.
- Trait method calls require receiver type and impl context to resolve confidently.
- Build scripts, `include!`, bindings generators, and proc macros create source that may not exist as ordinary checked-in Rust.
- Cargo features are additive within a build, while target cfg selects different source and dependencies.
- An impact cone should include callers, tests, docs, examples, impls, and serialized or FFI consumers when applicable.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Exact function name | Identifier search then inspect callers | Fast path for non-generated inherent items |
| Trait method | Find trait, impls, and receiver construction | Textual call names do not prove dispatch |
| Macro-generated item | Trace invocation and expansion contract | The apparent definition may not be checked in |
| Platform-specific behavior | Follow cfg and target dependencies | Host source path may be irrelevant on the target |
| Public API path | Trace re-exports from crate root | Source module and downstream import path can differ |

## Common Failure Modes

- Editing the first textual match without verifying it is in the active target or feature configuration.
- Missing blanket impls or default trait methods when tracing behavior.
- Treating rust-analyzer or Graphify output as proof without opening the linked source.
- Searching generated outputs but never locating the source schema or generator.
- Returning a file list without explaining the call or ownership relationship.

## Required Evidence

- Concrete definitions, construction sites, dispatch edges, and effect boundaries with paths and symbols.
- Relevant cfg, feature, target, or generated-source conditions.
- Affected tests and public or serialized consumers when the symbol changes.
- A clear distinction between confirmed edges and candidates needing type-aware confirmation.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

Choose one mode from the navigation question. Use the first available source in this order: fresh `graphify-out`, host-native LSP/rust-analyzer, locked offline Cargo commands, then `rg` plus source confirmation. A stale graph or textual match is a candidate, not proof.

## Definitions and references

- [Definitions, references, and workspace lookup](./modes/code-navigator.md)

## Symbol inventory

- [Document and workspace symbol analysis](./modes/symbol-analyzer.md)

## Trait exploration

- [Traits, implementations, methods, and dispatch](./modes/trait-explorer.md)

Confirm receiver types, blanket impls, cfg branches, proc-macro generation, and dyn construction sites.

## Call graph

- [Incoming and outgoing call hierarchy](./modes/call-graph.md)

Label edges `confirmed`, `candidate`, or `unknown`. Function pointers, trait objects, callbacks, macros, and FFI can make a static graph incomplete.

## Dependency graph

- [Cargo dependency visualization](./modes/deps-visualizer.md)

Use `cargo metadata --format-version 1 --locked --offline` for identity and resolved edges. Use `cargo tree --locked --offline` only as a presentation or focused inversion aid. If locked offline resolution fails, report the exact gap rather than falling back to manifest grep.
