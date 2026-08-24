---
name: nix-review
description: Perform a read-only findings-first review of Nix flakes, derivations, dev shells, NixOS or Home Manager modules, locks, hashes, purity, platforms, security, and Rust integration. Use for Nix-specific review rather than implementation.
---

# Nix Review

Own read-only correctness and risk assessment for Nix expressions and their Rust build or deployment effects. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- A Nix diff, flake update, package, dev shell, NixOS module, Home Manager module, or lockfile needs review.
- Purity, reproducibility, hashes, platforms, native dependencies, secrets, service hardening, or output shape may regress.
- The user requests a Nix audit or CI-aware Nix gate without code changes.

## Workflow

1. Establish diff or audit scope, supported Nix versions and systems, consumers, CI jobs, lock baseline, and Rust package relationship.
2. Inspect inputs, locks, output shape, derivations, source filters, hashes, platform-separated inputs, shells, modules, secrets, and service artifacts.
3. Evaluate changed outputs read-only and run targeted checks or builds only when authorized and locally supported.
4. Apply Nix-specific rules for purity, reproducibility, laziness, merge semantics, platform support, closure, security, and activation behavior.
5. Ground findings in exact expressions and resulting evaluation or artifact behavior; mark unavailable platform or network evidence as incomplete.
6. Report findings by severity, verdict, strengths, residual risk, and the smallest correction; route accepted items through `addressing-findings`.

## Decision Rules

- Review the lockfile delta independently from expression changes and identify every unexpected input revision.
- A shell that works is not evidence that a derivation builds purely or that a package runs from its closure.
- Automatic entry hooks must remain fast, read-only, offline, and deterministic.
- Check Linux and Darwin or other advertised systems separately when platform-specific packages, frameworks, or linkers appear.
- Flag network access, local paths, mutable environment, host tools, or undeclared files in evaluation and build inputs.
- Treat store-embedded secrets and broad service privileges as high-risk confirmed findings when the path is real.
- Do not require a Nix framework or abstraction merely because one style is fashionable.
- Separate evaluation, build, test, activation, and runtime evidence; success at one phase does not prove the next.

## Boundaries and Hand-offs

- `rust-review` owns non-Nix Rust diff findings and overall mixed-diff coordination.
- `nix-flakes`, `nix-dev-env`, `nix-packaging`, and `nixos` own implementation guidance for accepted findings.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Nix Review field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
