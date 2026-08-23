# Nix Flakes Field Guide

This guide is the detailed policy for `nix-flakes`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- A flake has declared inputs, a locked resolution, and an output function producing a typed attribute tree for consumers.
- Common outputs include `packages`, `apps`, `checks`, `devShells`, `formatter`, `overlays`, `nixosModules`, and templates, but unused outputs add maintenance.
- System-specific outputs must be instantiated for each supported platform; package availability can differ across nixpkgs systems.
- `follows` reduces duplicate input graphs and aligns package sets, while independent pins can preserve an input's tested environment.
- Pure evaluation rejects undeclared local and environment dependencies, revealing reproducibility gaps.
- Lockfile updates can change source revisions, nar hashes, nested inputs, and transitive nixpkgs graphs even when `flake.nix` is unchanged.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One Rust package and shell | Minimal direct flake outputs | Avoids a framework for a small attribute tree |
| Many repeated systems and outputs | Small established helper if already adopted | Real repetition may justify composition tooling |
| Input should use project nixpkgs | follows | Aligns packages and reduces graph duplication |
| Input requires tested independent nixpkgs | Separate pin | Forced alignment may break upstream assumptions |
| Only local shell succeeds | Build package output in pure mode | Shell availability can mask undeclared inputs |

## Common Failure Modes

- Adding every conventional flake output before a consumer exists.
- Updating the entire lock graph to change one unrelated source without reviewing transitive revisions.
- Advertising systems whose package or dependency set does not evaluate.
- Using impure environment reads or local paths for required build inputs.
- Duplicating package logic independently in package, check, app, and shell outputs until they drift.

## Required Evidence

- An input and follows graph with source, pin, purpose, and intentional independent revisions.
- A consumer-to-output map and exact supported system list.
- Pure evaluation plus targeted builds and checks for each supported output class.
- A reviewed lockfile delta separated from source and derivation changes.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
