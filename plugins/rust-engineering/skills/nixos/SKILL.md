---
name: nixos
description: Design NixOS and Home Manager modules for Rust services and tools, including options, merge semantics, systemd, users, files, secrets, networking, assertions, and tests. Use for declarative system or user configuration.
---

# NixOS and Home Manager

Own declarative deployment modules and the system or user lifecycle of Rust applications. Apply this profile directly for focused advice or load it from `rust-workflow` in the role justified by the current decision unit.

## Use This Skill When

- A Rust service or tool needs a NixOS module, systemd unit, Home Manager module, package option, user, file, network, or secret integration.
- Nix module options, imports, merge priority, assertions, defaults, or generated configuration behave unexpectedly.
- Service hardening, state directories, credentials, upgrades, or NixOS tests need design.

## Workflow

1. Define service owner, package, executable, configuration, state, network, credentials, privileges, lifecycle, upgrade, and observability requirements.
2. Design a small option schema with `enable`, package override, typed settings, safe defaults, examples, descriptions, and assertions for invalid combinations.
3. Translate options into files, users, directories, firewall rules, and systemd or user services while respecting Nix module merge semantics.
4. Keep secrets out of the store and pass runtime credential paths or secret-manager integrations with correct permissions.
5. Apply least privilege and explicit ordering, restart or reload triggers, environment, working directory, and state ownership.
6. Evaluate the module, inspect generated unit or files, and use a NixOS or Home Manager test for consequential lifecycle and networking behavior.

## Decision Rules

- Options describe user policy; implementation details should remain internal unless consumers need to control them safely.
- Use typed options, defaults, examples, assertions, and warnings to make invalid combinations fail during evaluation.
- Do not embed plaintext secrets or secret contents in Nix expressions because evaluated values can enter the store.
- Use systemd credentials, runtime secret paths, or an adopted secret manager according to repository policy.
- Create dedicated users and state directories and harden services proportionately without breaking required filesystem, network, or device access.
- Distinguish reload from restart and tie changes to the lifecycle the service actually supports.
- Home Manager user services and files have different ownership and boot semantics from NixOS system services.
- Avoid exposing free-form extra configuration when a small typed option schema can express current needs.

## Boundaries and Hand-offs

- `nix-packaging` owns producing the package installed by the module.
- `rust-observability` owns application telemetry semantics while this profile owns system logging and unit wiring.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [NixOS and Home Manager field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
