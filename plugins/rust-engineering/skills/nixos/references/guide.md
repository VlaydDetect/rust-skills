# NixOS and Home Manager Field Guide

This guide is the detailed policy for `nixos`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Nix modules merge option definitions from imports into a final configuration according to types and priorities.
- `mkIf`, `mkDefault`, `mkForce`, `mkBefore`, and `mkAfter` influence conditional and priority behavior and should be used deliberately.
- A service module typically owns package selection, config generation, user or group, state and runtime directories, unit dependencies, restart policy, and network access.
- Secrets must be materialized outside immutable world-readable store paths with runtime permissions and service access.
- Systemd hardening is a threat and capability model, not a checklist; each restriction should preserve required operations.
- NixOS VM tests can verify evaluation, boot, service readiness, files, networking, upgrades, and failure conditions in one declarative scenario.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| System daemon | NixOS module and system service | Boot, users, privileges, and networking are system-owned |
| Per-user tool or service | Home Manager module | User session and home files own lifecycle |
| Secret value | Runtime credential or secret-manager path | Avoids putting contents in the store |
| Small known configuration | Typed options | Evaluation catches invalid values |
| Large upstream config | Generated file with validated escape hatch | Avoid re-modeling the entire external schema prematurely |

## Common Failure Modes

- Writing secrets into generated Nix store files or command-line arguments.
- Using `mkForce` to win merges instead of resolving module ownership.
- Running a service as root when only one filesystem or network capability is needed.
- Creating state in immutable package paths or leaving runtime directory ownership implicit.
- Testing evaluation only and missing unit startup, permissions, readiness, restart, or network behavior.

## Required Evidence

- An option-to-system-effect map including package, files, users, directories, unit, network, and credentials.
- Evaluation tests for defaults, overrides, assertions, invalid combinations, and merge behavior.
- Generated systemd or Home Manager artifacts reviewed for permissions, dependencies, lifecycle, and hardening.
- A VM or integration test for important startup, readiness, secret access, state, networking, and upgrade behavior.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
