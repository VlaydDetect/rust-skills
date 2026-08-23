# Nix Review Field Guide

This guide is the detailed policy for `nix-review`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Nix review follows the artifact chain: declared input, locked source, evaluated output, derivation, store artifact, activation, and runtime.
- Purity means all required inputs are declared; reproducibility additionally depends on deterministic tools and external platform assumptions.
- Lazy evaluation can hide invalid outputs until a consumer forces them, so review must target advertised output paths.
- Cross compilation and native dependencies require correct build, host, and target platform placement.
- NixOS review includes option types and merges, secrets, users, filesystem state, unit lifecycle, network, and hardening—not only syntax.
- A strong review confirms premises, recognizes intentional local conventions, and avoids speculative findings unsupported by evaluation or source.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Flake input change | Inspect lock graph and consumers | A URL edit can alter many transitive pins |
| Package derivation change | Build and inspect artifact or closure | Evaluation alone misses phases and runtime dependencies |
| Dev-shell change | Clean activation and representative commands | Host environment can mask omissions |
| NixOS module change | Evaluation plus generated unit and integration path | Merge and runtime behavior are both relevant |
| Advertised remote platform unavailable | Mark evidence incomplete | Host success cannot prove the platform |

## Common Failure Modes

- Reviewing only formatting and attribute names without forcing changed outputs.
- Ignoring a broad lockfile update because the visible `flake.nix` diff is small.
- Assuming an impure local success will reproduce in a sandbox or CI.
- Applying generic security hardening that prevents the service's documented function.
- Inventing defects from Nix style preferences without concrete correctness or maintenance impact.

## Required Evidence

- Exact changed inputs, outputs, systems, derivations, modules, and Rust consumers.
- Read-only evaluation, targeted build or check, artifact or unit inspection, and runtime evidence by phase.
- Confirmed findings with premise, impact, location, confidence, and smallest fix.
- A clear list of unavailable systems, network-dependent freshness, secret integrations, or runtime checks.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
