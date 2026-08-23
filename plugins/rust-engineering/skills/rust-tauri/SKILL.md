---
name: rust-tauri
description: Build and review Tauri 2 desktop boundaries in Rust, including IPC, capabilities, plugins, updater security, resource cleanup, and Specta TypeScript bindings. Use for Tauri application contracts, not generic database or serialization work.
---

# Rust Tauri Engineering

Own the Tauri 2 desktop trust boundary from webview permissions through Rust commands, plugins, packaging, updates, and generated TypeScript contracts.

## Use This Skill When

- A Tauri 2 application defines commands, events, channels, state, windows, webviews, capabilities, permissions, scopes, or CSP.
- Official plugins, updater artifacts, remote content, shell or filesystem access, resource handles, or shutdown cleanup need review.
- Specta and `tauri-specta` generate TypeScript bindings for Rust commands and shared types.

## Workflow

1. Verify exact Tauri core, CLI, JavaScript API, plugin, Specta, and `tauri-specta` versions independently.
2. Map each window and webview to the minimum capability, permission, scope, CSP, and remote-content trust boundary.
3. Treat every command as an externally callable API: validate path, URL, ID, size, authorization, and typed error behavior.
4. Move blocking work off the main thread; choose events for small notifications and channels for ordered high-throughput streams.
5. Close listeners, channels, resources, child processes, and plugin handles on cancellation, navigation, window close, and shutdown.
6. Generate bindings deterministically, review their diff, and compile the TypeScript consumer in CI.

## Decision Rules

- Target Tauri 2 only; do not transfer Tauri 1 APIs or security assumptions.
- Capabilities can combine, so review the effective union rather than each file in isolation.
- Never expose an arbitrary shell, path, or URL operation through a broad command or plugin scope.
- Production updates require signatures, HTTPS, protected private keys, recovery or rotation planning, and a complete platform artifact matrix.
- Keep matching `serde` and Specta representations for tags, rename, flatten, optional or null values, bytes, dates, newtypes, and recursion.
- Do not silently map Rust wide integers or pointer-sized integers to TypeScript `number`; choose a string, BigInt policy, or domain newtype.

## Boundaries and Hand-offs

- `rust-api-design` owns reusable Rust API shape; this profile owns the webview-to-Rust boundary.
- `rust-serialization` owns byte formats; Specta owns generated type contracts, not runtime validation.
- `rust-database` owns persistence and transactions even when invoked from a Tauri command.
- Use `rust-research` for every “latest” claim and exact core, plugin, or prerelease compatibility.

## Detailed Reference

Read [Rust Tauri 2 field guide](references/guide.md) before changing capabilities, commands, plugins, updater behavior, or Specta bindings.
