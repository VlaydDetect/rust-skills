---
name: rust-style-clippy
description: Apply rustfmt, Clippy, workspace lint levels and priorities, typed Clippy configuration, exceptions, readability, and CI style gates. Use when lint tooling or its remediation controls the task.
---

# Rust Style and Clippy

Own mechanical style tooling and documented lint policy. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- Formatting, Clippy, lint configuration, naming policy, warnings-as-errors, or CI lint failures need work.
- A lint recommendation may change semantics, API, MSRV, allocation, or readability and needs judgment.
- Workspace-wide lint inheritance or justified allow and expect annotations need design.

## Workflow

1. Inspect repository toolchain, rustfmt config, Clippy config, workspace lints, CI commands, generated boundaries, and baseline failures.
2. Reproduce the narrow lint or format check with the exact package, target, features, and all-targets settings.
3. Classify findings as mechanical, semantic, policy conflict, generated code, false positive, or pre-existing.
4. Apply automatic formatting only when authorized; review semantic lint fixes individually and keep scope local.
5. Use allow or expect at the narrowest scope with a reason when the code intentionally violates a lint.
6. Run the repository's declared gate and separate new failures from unrelated baseline diagnostics.

## Decision Rules

- `cargo fmt -- --check` is read-only evidence; plain `cargo fmt` mutates files and belongs in an implementation workflow.
- Clippy groups change across toolchains, so pinning or policy must account for compiler updates.
- Warnings-as-errors improves cleanliness but can make dependency or toolchain updates disruptive; apply it at the intended scope.
- Do not run formatting across a dirty repository if the task does not authorize unrelated rewrites.
- A lint fix must preserve public API, MSRV, evaluation order, allocation, error context, and readability.
- Generated, vendored, example, bench, and test code may need distinct lint scope rather than blanket suppression.
- Prefer `#[expect(..., reason = ...)]` only when supported by policy and MSRV; otherwise use narrow documented allows.
- Style guidance should not duplicate rustfmt or Clippy unless a repository-specific convention adds real value.

## Rulebook Overlay

After reproducing the configured tool output, select relevant IDs from [`lint-`](../rust-coding-rules/references/categories/lint.md) or mechanical [`name-`](../rust-coding-rules/references/categories/name.md) rules. Rule IDs do not replace toolchain-specific diagnostics or baseline separation.

## Boundaries and Hand-offs

- `rust-idioms` owns semantic Rust patterns; this profile owns formatting and lint tooling.
- `rust-review` judges correctness and risk even when all lints pass.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Style and Clippy field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.

## Reviewed Cargo tooling

For lint groups, priorities, workspace inheritance, supported `clippy.toml` keys, disallowed items, CI scope, or toolchain migration, read [Advanced Clippy policy](references/cargo-tooling/clippy-advanced.md). Lint success does not replace semantic review.
