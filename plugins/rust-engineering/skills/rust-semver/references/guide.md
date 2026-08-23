# Rust SemVer Field Guide

This guide is the detailed policy for `rust-semver`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Rust compatibility includes name resolution, type checking, trait coherence, construction and matching, auto traits, behavior, features, MSRV, and sometimes ABI.
- Cargo SemVer expectations apply to public packages and dependency requirements, but each project may publish a stricter stability policy.
- Baseline selection must use a real release or artifact; comparing against an arbitrary branch weakens conclusions.
- Deprecation preserves source compatibility temporarily only when the old path or behavior remains usable.
- Feature removal, default-feature change, or altered feature unification can break builds even when the default public API compiles.
- A migration guide needs old and new caller examples, behavior changes, minimum versions, and feature or toolchain requirements.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Private implementation change | Patch if behavior preserved | No downstream contract changed |
| Compatible public addition | Minor | New capability without invalidating supported callers |
| Removed or incompatible public contract | Major or policy-defined break | Existing callers can fail to compile or behave correctly |
| Bug fix changes relied-on unspecified behavior | Document and assess impact | Correctness intent and ecosystem reality can conflict |
| MSRV raise | Follow explicit MSRV release policy | Compiler support is a consumer constraint |

## Common Failure Modes

- Running SemVer tooling without pinning the baseline and feature set.
- Assuming added enum variants, trait impls, bounds, or methods are always compatible.
- Ignoring behavior, errors, panics, ordering, or performance commitments because signatures match.
- Removing a deprecated item immediately after marking it deprecated in the same release.
- Treating internal workspace path builds as evidence that published dependency requirements work.

## Required Evidence

- Baseline version or artifact, comparison target, feature set, toolchain, and package list.
- Automated API comparison plus manual review of behavior, traits, macros, features, auto traits, and MSRV.
- Release classification tied to the project's declared stability policy.
- Downstream migration examples and deprecation window for intentional breaks.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Compiling Example

The [golden example](../examples/golden/) is an original, dependency-free fixture for this profile. It demonstrates one boundary or decision and is intentionally smaller than a production integration. Validate it with `cargo test --manifest-path skills/rust-semver/examples/golden/Cargo.toml`; additional external-tool or target evidence in this guide still applies.
