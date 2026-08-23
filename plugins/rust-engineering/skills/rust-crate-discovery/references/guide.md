# Rust Crate Discovery Field Guide

This guide is the detailed policy for `rust-crate-discovery`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- A useful rubric combines functional fit, integration fit, compatibility, operations, maintenance, trust, and total lifecycle cost.
- Primary evidence includes official documentation, source repository, releases, manifests, issues, advisories, and license texts.
- MSRV, target support, async runtime, no-std, feature flags, and native dependencies can disqualify an otherwise capable crate.
- Maintenance health is multi-signal: recent releases, response to defects, contributor concentration, roadmap, and ecosystem adoption all need context.
- Dependency depth and unsafe code are review inputs, not automatic rejection; reachability and boundary containment matter.
- A local spike converts documentation claims into project-specific evidence and exposes ergonomics, type coupling, build cost, and target failures.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Std already covers contract | Use std | No new supply-chain or upgrade surface |
| Existing dependency exposes capability | Reuse it | Avoids duplicate concepts and versions |
| Narrow stable algorithm | Small local implementation | Lifecycle may be cheaper than a broad crate |
| Complex maintained domain | Evaluate leading focused crates | Upstream expertise and testing may dominate local cost |
| Critical constraint lacks evidence | Defer or spike | Unknown compatibility is not a safe adoption decision |

## Common Failure Modes

- Selecting the most popular crate without testing the actual feature, target, and MSRV combination.
- Comparing candidates with different criteria or incomplete evidence dates.
- Ignoring public type leakage and discovering replacement cost after API release.
- Treating no reported advisories as proof of security.
- Writing a networked runtime helper into the plugin instead of using authorized host research and local Cargo evidence.

## Required Evidence

- A requirements rubric with hard gates, weights, evidence sources, dates, and unknowns.
- A comparable candidate table including exact versions, features, MSRV, targets, dependencies, licenses, and maintenance signals.
- A minimal integration spike for the highest-risk path under repository constraints.
- A decision and conditions for adoption, review, updates, and possible replacement.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-crate-discovery/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-ecosystem`](../../rust-ecosystem/references/ecosystem.md) — supporting; Solution classes, ecosystem maturity, maintenance, portability, interoperability, and evidence-led crate selection.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
