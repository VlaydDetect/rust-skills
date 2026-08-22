---
name: nix-dev-env
description: Build reproducible Nix development shells for Rust, including toolchains, native libraries, environment variables, shell hooks, direnv, platform differences, and editor tooling. Use for developer environment setup, not production packaging.
---

# Nix Development Environments

Own developer-facing tool and environment availability for repository work. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A Rust project needs or debugs `devShells`, `mkShell`, direnv, toolchain, linker, pkg-config, bindgen, or editor setup.
- Developers and CI disagree because native tools or environment variables are implicit.
- Shell hooks are slow, mutating, networked, or platform-specific and need cleanup.

## Workflow

1. Inventory repository commands and the compile-time, runtime, native, codegen, formatting, linting, test, and editor tools they actually require.
2. Separate packages placed on PATH from libraries and headers needed by builds, then account for Linux, Darwin, and cross-target differences.
3. Choose a Rust toolchain source consistent with repository pins and avoid maintaining two conflicting version authorities.
4. Set only required environment variables and keep shell hooks fast, deterministic, idempotent, and free of network or source mutation.
5. Integrate direnv as a thin activation layer and document trust or allow steps without hiding failures.
6. Enter a clean shell and run representative repository commands, editor or language-server discovery, and native builds.

## Decision Rules

- A dev shell supplies tools; it should not compile the project, edit files, update lockfiles, download registries, or run full tests on entry.
- Do not include every possible Rust tool by default; include repository-required tools and document optional workflows.
- Keep toolchain versions aligned with `rust-toolchain*`, CI, Cargo MSRV policy, or one explicitly chosen authority.
- Native dependencies may require separate build inputs, pkg-config metadata, framework paths, or runtime library search behavior by platform.
- Environment variables are global implicit inputs; prefer narrow variables with documented owners and values.
- Shell hooks must be safe to run repeatedly and should not assume an interactive terminal.
- Do not leak credentials into shell definitions, flake output, logs, or derivation inputs.
- Validate from a clean environment so host-installed tools do not mask omissions.

## Boundaries and Hand-offs

- `nix-packaging` owns isolated build derivations; a shell may contain extra interactive tools intentionally.
- `nix-flakes` owns flake output structure and input pinning around the shell.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Nix Development Environments field guide](references/guide.md) before making a consequential design choice. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.
