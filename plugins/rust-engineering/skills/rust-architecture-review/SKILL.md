---
name: rust-architecture-review
description: Perform a read-only whole-project assessment of Rust package and module boundaries, dependency direction, coupling, cycles, god modules, layer leaks, and unjustified complexity. Use for structural audits rather than diff review.
---

# Rust Architecture Review

Own evidence-backed diagnosis of current project structure and its highest-impact architectural risks. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- The user asks for a whole-codebase architecture audit, health assessment, or structural debt review.
- Crate and module boundaries, dependency direction, or layering may be impeding change.
- Potential cycles, god components, framework leaks, duplicate models, or over-engineering need evidence.

## Workflow

1. Define review scope, product context, supported targets, and the changes the architecture is expected to make easy.
2. Map packages, key modules, public surfaces, dependency edges, runtime components, data ownership, adapters, and composition roots.
3. Trace representative vertical paths and recent change hotspots to test whether boundaries match actual behavior.
4. Evaluate cohesion, coupling, dependency direction, cycles, layer leaks, shared mutable state, god modules, duplication, and speculative abstractions.
5. Ground each finding in concrete files, edges, and change impact; separate confirmed defects from suspected design pressure.
6. Rank a small remediation sequence by risk and leverage, assign an architecture health verdict, and state residual unknowns.

## Decision Rules

- Do not grade architecture by conformity to a named pattern; judge it against product change and operational needs.
- A large module is not automatically a god module; confirm mixed responsibilities and wide change impact.
- Cargo forbids package cycles, but conceptual cycles can still appear through shared types, callbacks, or duplicated coordination.
- Treat Graphify, metadata, and search output as navigation aids and confirm relationships in source.
- Distinguish intentional facade re-exports from layer leaks.
- Flag both under-structured coupling and over-structured indirection when they have concrete maintenance cost.
- Recommend the smallest sequence that improves direction or ownership; do not redesign the entire project by default.
- Keep the review read-only and route accepted remediation through `addressing-findings` and `rust-workflow`.

## Boundaries and Hand-offs

- `rust-review` owns diff or pull-request correctness; this profile evaluates current whole-project structure.
- `rust-architecture` owns designing an accepted target architecture after findings are triaged.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Architecture Review field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
