# Rust Refactoring Field Guide

This guide is the detailed policy for `refactoring`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Refactoring changes structure while holding a named set of observables constant.
- Characterization tests capture current behavior; they are especially useful when intent is underdocumented.
- Move-then-edit separates relocation mistakes from semantic rewrites.
- The migration graph includes callers, re-exports, macros, docs, examples, feature configurations, and generated consumers.
- Temporary duplication can support a staged migration, but permanent dual paths multiply maintenance and test cost.
- A smaller dependency cone usually makes a refactor easier to validate and review.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Private helper used once | Keep local or inline | Extraction without reuse or boundary value adds navigation cost |
| Shared logic with stable invariant | Extract one owner | One root implementation prevents divergent fixes |
| Public path must move | Re-export or deprecate for a defined window | Callers need a migration path |
| Behavior and structure both change | Stage structure first | Separate evidence makes regressions diagnosable |
| Crate split proposed | Require an ownership or build-boundary benefit | A package boundary has versioning and dependency cost |

## Common Failure Modes

- Claiming behavior preservation without naming serialization, error, ordering, or feature observables.
- Adding a trait, factory, or generic layer with only one implementation and no boundary need.
- Keeping both old and new internal paths indefinitely after all callers have migrated.
- Renaming public items without checking rustdoc links, examples, macros, and downstream paths.
- Using a full workspace pass as the only evidence for a narrow but semantically risky migration.

## Required Evidence

- A before-and-after contract list and complete affected-caller inventory.
- Characterization or existing tests for behavior that could change during movement.
- Targeted compilation and behavior checks for each supported feature or target affected.
- Diff evidence that obsolete paths and temporary scaffolding are removed or explicitly time-bounded.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

- [Rename, extract, move, and impact-analysis workflows](./refactoring-workflow.md)

Use the navigation operations to enumerate definitions, references, callers, imports, trait impls, cfg branches, tests, docs, and generated consumers. The preserved behavior/API/serialization/performance contract remains authoritative; an LSP rename or successful compilation alone is insufficient evidence.
