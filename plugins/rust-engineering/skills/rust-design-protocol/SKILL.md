---
name: rust-design-protocol
description: Trace consequential Rust questions across language mechanics, design choices, and confirmed domain constraints, then return an evidence-backed decision brief. Use for architecture, comparisons, ambiguous best practices, and cross-layer failures; skip obvious local fixes.
---

# Rust Design Protocol

Own cross-layer reasoning when no single local rule is sufficient. Apply this skill directly for design or comparative questions, or load it from `rust-workflow` as one of the normal profile slots. Do not activate merely because the prompt contains a Rust keyword.

## Use This Skill When

- A compiler or runtime symptom keeps recurring because ownership, lifecycle, API, or domain boundaries may be wrong.
- The task compares libraries, runtimes, patterns, or architectures whose trade-offs depend on context.
- A design request must be translated into concrete Rust mechanisms.
- An explanation needs a correct mental model rather than a one-off compiler workaround.

## Workflow

1. Identify the entry layer: mechanics, design, or domain constraints.
2. Select the one product profile that owns correctness and at most two supporting profiles.
3. Trace to an adjacent layer only when evidence there can change the decision.
4. Separate repository facts, current external facts, assumptions, and unknowns.
5. Compare only viable alternatives against explicit criteria; reject speculative flexibility.
6. Return a concise `DesignBrief`, then hand implementation back to `rust-workflow`.

## Decision Rules

- Local compiler questions receive local answers unless repeated failure exposes a boundary problem.
- Domain claims require repository specifications or user-provided constraints. ML has a dedicated domain profile; IoT, embedded, and cloud-native constraint maps route through `rust-architecture` and the existing implementation owners.
- A named pattern is not evidence. State the invariant, cost, and failure mode it addresses.
- Do not require parallel agents, forced clarification, or a displayed chain-of-thought. Delegate only independent read-only research that materially reduces uncertainty.
- Preserve the target project's toolchain, MSRV, edition, dependency, and lint contracts.

## Output Contract

Read [DesignBrief contract and topic map](references/design-brief.md) for the public decision artifact. For the complete layer router, comparison protocol, mental-model techniques, and worked examples, load only the needed branch from that topic map.

## Boundaries and Hand-offs

- `rust-architecture` owns accepted system boundaries; `rust-design-protocol` connects evidence across layers.
- `rust-research` owns current Rust and crate facts.
- `rust-workflow` remains the sole writer for repository changes.
- `rust-review` owns read-only findings and `rust-verify` owns command evidence.
