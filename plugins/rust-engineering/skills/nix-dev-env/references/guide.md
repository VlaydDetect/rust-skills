# Nix Development Environments Field Guide

This guide is the detailed policy for `nix-dev-env`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- `mkShell` or a dev-shell derivation assembles PATH, build inputs, environment, and hooks for interactive work.
- Rust toolchain, linker, C compiler, pkg-config, bindgen or libclang, native libraries, Nix tooling, and repository task runners form distinct requirements.
- Linux and Darwin expose native frameworks and linker behavior differently; one package list may not be portable unchanged.
- Direnv can activate the flake shell on directory entry, but activation should remain visible and user-approved.
- A clean shell test reveals accidental reliance on global Cargo tools, system headers, environment variables, and mutable caches.
- Fast activation supports frequent use; expensive checks belong to explicit commands or flake checks.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Tool invoked by developers | PATH package | The command must be directly available |
| Native header or library | Build input with platform handling | Compilation and linking need metadata |
| Optional rare analyzer | Document optional shell or command | Avoids slowing every developer environment |
| Repository toolchain already pinned | Reuse the same pin | Prevents shell and CI drift |
| Expensive startup check | Move to explicit check | Entry hooks should remain fast and read-only |

## Common Failure Modes

- Running cargo fetch, builds, formatters, migrations, or tests automatically in `shellHook`.
- Depending on globally installed rustup, compiler, linker, or pkg-config while claiming reproducibility.
- Adding broad environment variables that change unrelated tools or leak host paths.
- Testing only inside an already polluted interactive shell.
- Copying Linux native-library setup to Darwin without framework and linker validation.

## Required Evidence

- A command-to-tool and native-input inventory tied to actual repository workflows.
- Toolchain and platform matrix with one authoritative version policy.
- Clean-shell execution of representative check, build, test, codegen, and editor commands.
- Measured activation behavior and confirmation that hooks are offline, read-only, deterministic, and idempotent.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
