---
name: nix-flakes
description: Design and debug Nix flakes for Rust projects, including inputs, lockfiles, follows, systems, outputs, overlays, packages, apps, checks, and dev shells. Use when flake structure or reproducibility is the controlling concern.
---

# Nix Flakes

Own flake input, output, system, lock, and composition contracts. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A `flake.nix` or `flake.lock` is added, changed, updated, or failing to evaluate.
- Inputs, follows, outputs, systems, overlays, packages, apps, checks, or devShells need structure.
- The same Rust project must evaluate reproducibly across supported Nix systems.

## Workflow

1. Inspect repository Nix policy, existing flake, lockfile, supported systems, CI, package, dev-shell, and NixOS consumers.
2. Map every input, URL or source, follows edge, pin, and reason; remove duplicate nixpkgs graphs unless divergence is intentional.
3. Define the minimum outputs actually consumed and generate them per supported system with transparent arguments.
4. Keep package, dev-shell, check, app, overlay, and module responsibilities separate while reusing one real package definition where appropriate.
5. Update lock entries intentionally and review source revisions, hashes, transitive input changes, and supported Nix version.
6. Evaluate and build targeted outputs in pure mode first, then expand to each supported system or CI runner.

## Decision Rules

- Commit `flake.lock` when reproducible input resolution is part of the project workflow.
- Use `follows` when inputs should share the same nixpkgs or flake-parts graph; do not force it when an input requires a different revision.
- Declare only supported systems and ensure each advertised output exists on each one.
- Keep `outputs` readable; helper libraries are optional and should solve real repetition, not hide basic data flow.
- Do not put secrets, machine-local absolute paths, mutable network fetches, or impure environment assumptions into evaluation.
- A dev shell is not proof that the package builds in isolation.
- An overlay changes package-set composition and should be used only when consumers need that extension point.
- Review lockfile changes like dependency updates rather than accepting broad churn from an unrelated edit.

## Boundaries and Hand-offs

- `nix-dev-env` owns shell ergonomics and hooks; `nix-packaging` owns derivation construction.
- `nixos` owns NixOS modules and `nix-review` owns read-only review of the whole Nix change.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Nix Flakes field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
