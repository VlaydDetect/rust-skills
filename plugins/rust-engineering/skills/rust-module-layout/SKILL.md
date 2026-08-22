---
name: rust-module-layout
description: Organize Rust modules, files, visibility, re-exports, tests, and generated boundaries within a crate. Use for in-crate structure, public paths, privacy, and migration between file layouts without introducing unnecessary crates.
---

# Rust Module Layout

Own in-crate namespaces, privacy, source layout, re-exports, and cohesive module responsibility. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A crate's files, `mod` declarations, visibility, re-exports, tests, or generated modules need restructuring.
- Public paths and implementation layout must be decoupled.
- A module has unclear responsibility, excessive visibility, or difficult navigation.

## Workflow

1. Trace crate roots, module declarations, inline or file modules, cfg variants, re-exports, tests, macros, and generated includes.
2. Name cohesive responsibilities and identify which items are public API, crate-internal, parent-only, or private implementation.
3. Choose the shallowest layout that communicates ownership; use submodules when a concept has internal structure, not just many lines.
4. Preserve or deliberately migrate public paths through crate-root or facade re-exports.
5. Move declarations and tests in compiling steps, then tighten visibility and remove obsolete compatibility modules.
6. Validate all cfg and feature-selected module variants plus rustdoc links and examples.

## Decision Rules

- Prefer private-by-default and widen visibility to the narrowest necessary scope such as `pub(crate)` or `pub(super)`.
- Filesystem layout is not the public API; re-exports should define intentional downstream paths.
- Avoid `mod.rs` versus same-name-file debates unless repository convention or tooling gives a real reason.
- Keep tests near private behavior when they need private access; use integration tests for public caller behavior.
- Do not place unrelated helpers in a generic module merely to shorten owner modules.
- Generated modules must expose their generator and source of truth and remain clearly separated from handwritten code.
- Macro visibility and expansion paths may not follow ordinary item intuition; verify exported macro use explicitly.
- A module split should reduce conceptual load or enforce privacy, not just satisfy a line-count threshold.

## Boundaries and Hand-offs

- `rust-workspace` owns whether a concept becomes a separate crate; this profile defaults to the cheaper module boundary.
- `rust-api-design` owns downstream contract decisions represented through module visibility and re-exports.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Module Layout field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
