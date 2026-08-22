# Codebase Onboarding Field Guide

This guide is the detailed policy for `codebase-onboarding`. It synthesizes the craft onboarding workflow and full-stack workspace, Cargo, module-layout, and documentation guidance; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- A useful map has four layers: repository governance, Cargo topology, runtime flow, and validation or delivery flow.
- Workspace membership does not necessarily equal product boundaries; binaries, libraries, build scripts, proc macros, and xtask crates serve different roles.
- Feature unification, target-specific dependencies, and workspace inheritance can make a manifest appear simpler than effective state.
- CI and task runners reveal supported commands and platform matrices that README examples may omit.
- One end-to-end trace exposes naming conventions and abstraction boundaries faster than cataloguing every file.
- Unknowns are onboarding output when they influence correctness, compatibility, or scope.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Virtual workspace | Start at root Cargo.toml and metadata | There may be no root package or source target |
| Single package with many binaries | Map targets before modules | Executables may have different feature and deployment contracts |
| Large monorepo | Follow the affected package dependency cone | Full-tree reading creates noise without better task evidence |
| Docs and manifests disagree | Report both and validate effective state | Silent reconciliation hides a maintenance defect |
| Generated bindings or schemas | Find their generator and source of truth | Editing generated output causes drift |

## Common Failure Modes

- Assuming `src/main.rs` is the only entry point in a multi-target package.
- Treating `Cargo.toml` declarations as the effective feature graph without metadata or cfg context.
- Ignoring AGENTS.md, CLAUDE.md, CI, or task-runner instructions scoped to the affected path.
- Describing directories without tracing how data or control moves between them.
- Running expensive workspace checks during what should be read-only discovery.

## Required Evidence

- Workspace root, package and target inventory, toolchain, resolver, and lockfile policy.
- At least one traced entry-to-effect path with concrete symbols and files.
- Repository-native build, test, lint, docs, and formatting commands or an explicit statement that they are absent.
- Known generated boundaries, platform or feature gates, and unresolved task-relevant questions.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
