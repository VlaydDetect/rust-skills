---
name: rust-documentation
description: Create and review Rust crate, module, item, example, doctest, README, changelog, and migration documentation as part of the API contract. Use when users need correct discoverability, guarantees, examples, or release guidance.
---

# Rust Documentation

Own the documented user model of a Rust package and executable examples that support it. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- Public or important internal APIs need rustdoc, examples, safety, errors, panics, or usage guidance.
- README, crate docs, module docs, doctests, changelog, or migration notes need synchronization with code.
- Documentation failures, broken links, hidden setup, or misleading examples affect users.

## Workflow

1. Identify the audience and contract surface: crate purpose, common path, types, errors, safety, features, targets, MSRV, and migration needs.
2. Start with a minimal end-to-end example and navigation path, then document item-specific guarantees and edge behavior.
3. Use intra-doc links and examples that compile under intended features; mark intentionally non-running or compile-fail examples explicitly.
4. Document errors, panics, safety obligations, cancellation, blocking, ordering, and complexity only where callers need those facts.
5. Keep README, crate-level docs, examples, feature lists, and migration notes consistent without duplicating volatile details unnecessarily.
6. Run rustdoc checks and doctests in the supported configurations and inspect generated docs for discoverability when risk warrants it.

## Decision Rules

- Lead with purpose and the common successful path before exhaustive reference detail.
- Examples must include required imports, runtime setup, features, and error handling appropriate to their audience.
- Every unsafe public API needs a precise Safety section describing caller obligations.
- Document panic conditions only when they are part of supported behavior or caller avoidance.
- Do not promise thread safety, target support, complexity, allocation behavior, or stability without implementation and test evidence.
- Use hidden doctest lines sparingly for setup while keeping copied visible code coherent.
- Prefer links to one authoritative detailed section over copying the same feature matrix into several files.
- Update changelog and migration guidance when user action is required, not for every internal refactor.

## Rulebook Overlay

After identifying the reader and contract, select only relevant IDs from the [`doc-` index](../rust-coding-rules/references/categories/doc.md). Rules supplement current implementation evidence and never license claims about future behavior.

## Boundaries and Hand-offs

- `specs` owns normative product behavior; documentation presents accepted behavior to developers and users.
- `rust-api-design` owns the API contract and `rust-semver` owns compatibility classification reflected in docs.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Documentation field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
