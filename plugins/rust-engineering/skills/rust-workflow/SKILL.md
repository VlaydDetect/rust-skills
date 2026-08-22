---
name: rust-workflow
description: Orchestrate project-aware Rust and Nix implementation by discovering effective state, selecting one primary and at most two supporting engineering profiles, making one coherent root-cause change, and producing risk-based evidence. Use for features, fixes, refactors, and other mutating coding work. Do not use for read-only review or verification-only requests.
---

# Rust Workflow

Treat the repository's effective state and explicit user contract as controlling evidence. This skill is the automatic coding entrypoint; detailed engineering policy lives in the profile it selects. Keep the main agent as the only writer.

## Workflow

1. Read the task and path-scoped instructions. Inspect dirty state before touching files.
2. Trace the real call path, tests, manifests, toolchain, CI, and repository-native commands. Preserve unrelated work.
3. Write a compact `TaskBrief`: goal, non-goals, affected packages, constraints, compatibility surface, acceptance evidence, and unknowns.
4. Select exactly one primary profile and zero to two supporting profiles from [Profile routing index](references/routing-index.md). If more are needed, split the work into phases and route each phase separately.
5. Read each selected profile's `SKILL.md` and detailed reference before making its design decisions. Resolve semantics, safety, and compatibility before optimization.
6. Classify risk and delegate only independent read-only investigation when it materially reduces uncertainty.
7. Implement the smallest coherent root-cause change. Update tests, documentation, manifests, or generated sources only when the changed contract requires them.
8. Invoke `rust-verify` for the smallest sufficient evidence matrix. Use `rust-review` for an independent findings-first pass when requested or proportionate to risk.
9. Inspect the final diff and report selected profiles, changed files, exact checks, failures by cause, and unverified risk.

## Profile Loading Contract

- The primary profile owns the decision and vocabulary. Supporting profiles constrain it; they do not create parallel solutions.
- Do not summarize a profile from memory when its detailed reference is locally available.
- Do not load profiles merely because a keyword appears. Route by the decision that controls correctness.
- Re-route after a phase when the owner changes, such as discovery -> API design -> verification.
- A direct profile invocation may answer a focused question without this workflow. Any repository mutation still returns here for discovery, integration, and evidence.

## Adaptive Delegation

Use host-native subagents when available; otherwise perform the same roles sequentially.

- Low risk: no delegation. Examples: local typo, obvious test adjustment, one-file mechanical fix.
- Medium risk: at most two read-only roles when they reduce uncertainty.
- High risk: use a scout plus the relevant reviewer or verifier. Examples: public API, unsafe or FFI, concurrency, feature graphs, cross-target behavior, broad refactors, or security boundaries.

Available role contracts are `rust-scout`, `rust-reviewer`, and `rust-verifier`. Give each a bounded `RoleBrief` from [Agent contracts](references/agent-contracts.md) plus the selected profile names. They return evidence; they never edit. The main agent decides, writes, integrates, and owns the final result. Avoid delegation for tiny tasks and avoid multiple agents reading the same scope. When re-reviewing fixes, prefer a fresh reviewer context.

## Routing Rules

Keep automatic work cheap. Session hooks may discover context, but must not format files, modify lockfiles, download tools, run a full workspace test suite, publish, or perform security or network actions.

Require explicit authorization before publishing, changing registry credentials, yanking releases, deleting user data, or broadening the task beyond the repository.

Read [Project discovery](references/project-discovery.md) when the workspace, feature matrix, or repository-native commands are unclear. Use `addressing-findings` when a supplied review set must be closed. Unknown constraints remain unknown; do not invent them.
