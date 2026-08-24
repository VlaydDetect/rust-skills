---
name: rust-workflow
description: Orchestrate project-aware Rust implementation and opt-in setup by discovering the current change slice, assigning one owner per decision unit, loading only required coding profiles and triggered helpers, making one coherent root-cause change, and producing risk-based evidence. Use for features, fixes, refactors, project bootstrap, toolchain setup, and other mutating coding work. Do not use for read-only review or verification-only requests.
---

# Rust Workflow

Treat the repository's effective state and explicit user contract as controlling evidence. This skill is the automatic coding entrypoint; detailed engineering policy lives in the profiles selected for the current change slice. Keep the main agent as the only writer.

## Workflow

1. Read the task and path-scoped instructions. Inspect dirty state before touching files.
2. Trace the real call path, tests, manifests, toolchain, CI, and repository-native commands. Preserve unrelated work.
3. Build the `TaskBrief` and `ProfileStack` from [ProfileStack contract](references/profile-stack.md), using [Profile routing index](references/routing-index.md) only to find candidate owners and specialists. Current instructions and changed symbols outrank background plans.
4. Split the phase and re-route when the stack crosses a circuit breaker. Do not edit until `coverage.gaps` is empty.
5. Read each active profile's `SKILL.md` and relevant reference before applying its decisions. Load helpers only after their documented trigger and unload them after recording the result.
6. Build one `RuleQuery` per active decision unit from the actual constructs, boundary, toolchain, configuration, and measurements. Load at most nine rules per unit; `rust-coding-rules` remains an overlay.
7. Implement the smallest coherent root-cause change. Update tests, documentation, manifests, or generated sources only when the changed contract requires them. Re-route and re-query rules against the actual diff.
8. Invoke `rust-verify` for the smallest sufficient evidence matrix. Use `rust-review` when requested or proportionate to risk, inspect the final diff, and report the stack, rule IDs, checks, failures by cause, and residual risk.

## Profile Loading Contract

- Every decision unit has exactly one owner. Coding profiles bind to named constructs; helpers bind to observed triggers.
- Do not summarize a profile from memory when its detailed reference is locally available.
- Do not load profiles merely because a keyword appears. Route by the decision that controls correctness.
- `rust-coding-rules` supplies concrete rule IDs after profile selection. It never enters `ProfileStack` roles and cannot override project state or a decision owner.
- Re-route after a phase when the owner changes, such as discovery -> API design -> verification.
- A direct profile invocation may answer a focused question without this workflow. Any repository mutation still returns here for discovery, integration, and evidence.

## Adaptive Delegation

Use host-native subagents when available; otherwise perform the same roles sequentially.

- Low risk: no delegation. Examples: local typo, obvious test adjustment, one-file mechanical fix.
- Medium risk: at most two read-only roles when they reduce uncertainty.
- High risk: use a scout plus the relevant reviewer or verifier. Examples: public API, unsafe or FFI, concurrency, feature graphs, cross-target behavior, broad refactors, or security boundaries.

Available role contracts are `rust-scout`, `rust-researcher`, `rust-reviewer`, and `rust-verifier`. Give each a bounded `RoleBrief` for one decision-unit slice from [Agent contracts](references/agent-contracts.md). They return evidence; they never edit. Use the researcher only for one version-sensitive external question. The main agent decides, writes, integrates, and owns the final result. Avoid delegation for tiny tasks and avoid multiple agents reading the same scope. When re-reviewing fixes, prefer a fresh reviewer context.

## Project Setup

Setup is an opt-in phase of this workflow, not a separate skill.

1. Inspect existing Rust files, Cargo manifests, toolchain files, CI, target configuration, and available commands before proposing anything.
2. Offer only tools and files justified by those facts. State the exact commands and changes before running them.
3. Wait for explicit user approval before invoking `rustup`, `cargo install`, package managers, generators, or before creating or modifying project files.
4. Keep ordinary Rust setup separate from Nix. Route a requested Nix development shell through `nix-dev-env` and NixOS-specific work through `nixos`.
5. Do not install optional tools such as `cargo-nextest`, `cargo-llvm-cov`, or `cargo-machete` unless the project evidence and requested workflow call for them.

If there are Rust files without Cargo metadata, offer toolchain or project setup once. If a Cargo project is already configured, report its current context and offer one project-specific setup action. Treat `flake.nix`, `shell.nix`, a detected `nix` command, or NixOS as a separate Nix/NixOS offer.

## Routing Rules

Keep automatic work cheap. Session hooks may discover context, but must not format files, modify lockfiles, download tools, run a full workspace test suite, publish, or perform security or network actions.

Require explicit authorization before publishing, changing registry credentials, yanking releases, deleting user data, or broadening the task beyond the repository.

Read [Project discovery](references/project-discovery.md) when the workspace, feature matrix, or repository-native commands are unclear. Use `addressing-findings` when a supplied review set must be closed. Unknown constraints remain unknown; do not invent them.
