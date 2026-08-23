# Rust Dependency Governance Field Guide

This guide is the detailed policy for `rust-dependencies`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Dependency cost includes binary size, compile time, native tools, MSRV, feature surface, maintenance, advisories, licenses, and public coupling.
- The manifest states requested requirements and features; the lockfile records one resolution for a graph and source set.
- Runtime, build, proc-macro, and dev dependencies have different trust and deployment consequences.
- Feature unification can enable code that no single direct dependency declaration appears to request in isolation.
- Transitive packages are governed through direct requirements, feature choices, updates, patches, or upstream collaboration—not by editing the lockfile manually.
- Removal is the best dependency simplification when current code and supported configurations no longer need the capability.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Unused direct dependency | Remove | Eliminates all downstream cost |
| Defaults enable unwanted subsystems | Disable defaults and opt in | Makes required capability explicit |
| Two compatible versions with low cost | Leave unless policy requires alignment | Churn can exceed benefit |
| Known vulnerable reachable version | Update, mitigate, or document decision | Reachability and deployment determine urgency |
| Public dependency type | Treat as API contract | Version changes can affect downstream type identity |

## Common Failure Modes

- Running a broad update while making an unrelated source fix and obscuring the graph delta.
- Disabling default features without testing all code paths that relied on them indirectly.
- Calling every duplicate version bloat without measuring artifact or build impact.
- Ignoring licenses, native code, proc macros, or build scripts because the Rust API is small.
- Claiming security from an old or unavailable audit without date, database state, and reachability context.

## Required Evidence

- Direct purpose, reverse dependency path, resolved version, source, features, target scope, and public exposure.
- Manifest intent and lockfile transitive changes reviewed separately.
- Current dated advisory and license evidence when requested or required, including unavailable checks.
- Build and behavior checks for affected packages, features, targets, and native integration.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-dependencies/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
