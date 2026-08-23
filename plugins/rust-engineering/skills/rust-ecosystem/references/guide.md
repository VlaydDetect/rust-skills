# Rust Ecosystem Field Guide

This guide is the detailed policy for `rust-ecosystem`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Ecosystem orientation begins with product and target constraints, then selects solution classes, then evaluates concrete dependencies.
- Rust packages can provide multiple targets, but deployment, release, feature, and compilation boundaries may justify a workspace later.
- Async runtime, serialization, web framework, database client, GUI, embedded HAL, and native bindings are sticky choices with integration consequences.
- Std-first and existing-dependency-first checks reduce supply-chain, compile-time, and conceptual cost.
- A vertical slice validates toolchain, target, packaging, observability, and test assumptions earlier than a broad scaffold.
- Ecosystem facts drift; current recommendations need current primary-source verification when they affect substantial time or dependency commitments.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Small command-line tool | Single binary package and std first | Keeps packaging and errors simple |
| Reusable library | Library package with narrow public API | Downstream compatibility becomes primary |
| Async network service | Evaluate runtime and framework as coupled choices | Runtime types and cancellation spread through APIs |
| Embedded or no-std | Target-first design | Allocator, OS, panic, and hardware support constrain all libraries |
| Several real deployment components | Workspace evaluation | Independent targets and ownership may justify crates |

## Common Failure Modes

- Generating a large workspace and framework stack before the first behavior is specified.
- Choosing a runtime or framework from popularity instead of deployment and dependency constraints.
- Ignoring toolchain, native libraries, linker, target installation, and packaging until CI.
- Creating a common crate before any stable shared concept exists.
- Giving stale crate recommendations without date or source verification.

## Required Evidence

- Product, target, deployment, MSRV, async, no-std, native, and compatibility constraints.
- A minimal project shape and first vertical slice with reasons for each non-std choice.
- Explicit routing of sticky dependency choices to current candidate research.
- Build and delivery evidence for the real target rather than only host compilation.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

- [Crate integration, features, workspaces, and interop](./ecosystem-overview.md)

Use this for solution-class orientation. Current crate identity and resolved features come from `rust-research` and Cargo metadata; adoption policy remains with `rust-crate-discovery` or `rust-dependencies`.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-ecosystem`](./ecosystem.md) — primary; Solution classes, ecosystem maturity, maintenance, portability, interoperability, and evidence-led crate selection.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
