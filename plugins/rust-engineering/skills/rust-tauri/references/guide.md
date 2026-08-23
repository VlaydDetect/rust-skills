# Rust Tauri 2 Field Guide

Research baseline: **2026-08-23**. This guide targets Tauri 2 only. At the snapshot, the official release page listed Tauri core 2.11.5, CLI 2.11.4, and JavaScript API 2.11.1; these components and every plugin have independent release trains. Run `rust-research` against the [release page](https://v2.tauri.app/release/) and [plugin catalog](https://v2.tauri.app/plugin/) immediately before changing versions or invoking any “latest” API.

## Dependency and Platform Matrix

Record exact versions of Rust, Tauri core, `tauri-build`, CLI, JavaScript API, each official or third-party plugin, frontend package manager, webview runtime, and platform build tools. Pin only where reproducibility or prerelease compatibility requires it; otherwise preserve the repository’s established update policy. Test the complete matrix on every shipped operating system and architecture because permissions, signing, updater artifacts, webviews, and plugin support differ by target.

Keep plugin Cargo and JavaScript packages compatible but do not assume equal version numbers. Enable only required Cargo features and plugin permissions. Mobile support is a separate target contract, not a consequence of compiling a desktop app.

## Capabilities Are the Effective Security Policy

Split [capability files](https://v2.tauri.app/security/capabilities/) by window or webview and responsibility. Grant the minimum permissions and scopes needed for that surface. Review the effective union: overlapping capabilities combine, and capability files can be auto-enabled depending on application configuration. A narrow-looking file is not safe if another file grants a broader permission to the same window.

Scopes must constrain values, not only operation names. Limit filesystem roots, URL origins, command arguments, executable names, and platform variants. Avoid wildcard permissions in production. Test both allowed and denied calls from each window and webview, including a newly created or renamed window.

Configure [Content Security Policy](https://v2.tauri.app/security/csp/) instead of disabling it to make development convenient. Prefer packaged local assets, restrict script, connection, image, and frame origins, avoid permissive inline execution, and keep development-only endpoints out of production policy. Loading remote content creates a separate web trust boundary: treat that origin as potentially compromised, give its webview a distinct capability set, and never assume browser same-origin policy substitutes for Tauri authorization. Rust code itself is trusted native code and can bypass capability checks, so keep privileged operations behind reviewed commands or internal modules.

## Commands and IPC

Treat each [Rust command](https://v2.tauri.app/develop/calling-rust/) as a public API callable by compromised frontend code. Deserialize into bounded DTOs, then validate authorization and domain semantics. Canonicalize and scope paths carefully, allowlist URL schemes and hosts, validate identifiers and result cardinality, cap strings, arrays, uploads, and response sizes, and return stable typed errors without secrets or raw internals.

Never expose an arbitrary shell command, unrestricted filesystem path, generic HTTP proxy, SQL string, or plugin escape hatch. Offer domain operations with fixed executables, arguments, roots, or query templates. Generated TypeScript types improve ergonomics but do not validate runtime input or confer authorization.

Synchronous commands run on the main thread. Keep them tiny. Use asynchronous commands or the runtime’s blocking facility for filesystem, CPU, database, compression, or native calls that can block, and propagate cancellation and deadlines. Do not hold application-state locks across `.await`, frontend interaction, or a blocking call.

Use events for small, lossy or independently handled notifications. Use [channels](https://v2.tauri.app/develop/calling-frontend/) for ordered or high-throughput streaming with explicit backpressure, capacity, cancellation, and terminal errors. Chunk large data instead of serializing one enormous IPC payload. Unlisten event listeners and close channels, resources, child processes, file watchers, and plugin handles on component unmount, navigation, window close, command cancellation, and application shutdown.

## State, Plugins, and Resources

Managed state should have one clear owner and shutdown path. Prefer small handles over global mutable application models. Define which thread or runtime owns native resources and whether callbacks can outlive windows. Prevent panics from crossing callback or command boundaries; translate them only where the repository’s error policy permits.

For every plugin, review native and JavaScript dependencies, permissions, scopes, platform support, release notes, and security implications. Install only the operations required. File system, shell, opener, HTTP, process, clipboard, notification, deep-link, single-instance, and updater plugins each expand the native authority available to the webview. A plugin’s presence does not enable every command, but a broad capability can.

## Updater and Release Security

The [Tauri updater](https://v2.tauri.app/plugin/updater/) requires signed artifacts; do not disable signature verification. Use HTTPS production endpoints, protect the private signing key outside the repository and ordinary CI logs, restrict who can invoke the signing workflow, and publish the correct artifact and signature for every supported platform and architecture.

Plan key rotation and recovery before a key is lost or compromised. Existing installations must be able to trust a transition or receive a recovery release under the old policy. Define rollout channels, downgrade policy, update metadata integrity, partial-publish cleanup, minimum supported version, and behavior when a signature, download, installation, or restart fails. Test a real upgrade from the oldest supported installed version on each platform; a successful fresh install is not an updater test.

## Specta and tauri-specta

Use the Tauri 2 / Specta 2 path only. This remained a prerelease line at the research snapshot. The latest published compatible set verified for this guide was exactly:

- `tauri-specta = "=2.0.0-rc.25"`;
- `specta = "=2.0.0-rc.25"`;
- `specta-typescript = "=0.0.12"`.

Do not copy the repository `main` branch dependency graph into a release build: it was already preparing a later unpublished Specta RC through pinned Git revisions. Re-run `rust-research` over [Specta releases](https://github.com/specta-rs/specta/releases), [tauri-specta releases](https://github.com/specta-rs/tauri-specta/releases), and the exact published Cargo metadata before changing any member of the trio. Prerelease upgrades can change generated output and derive behavior even when application code compiles.

Generate bindings deterministically from a test or `xtask`, never as a surprising build-time mutation. Write to a known file, normalize formatting, fail on export errors, check the generated diff in CI, and run the TypeScript compiler against the real consumer. Review removals and widenings as API changes.

Align `serde` and Specta attributes deliberately: rename rules, tagged or untagged enums, flattening, defaults, skipped fields, phase-specific input and output types, `Option` versus nullable values, byte arrays, date and URL semantics, transparent newtypes, generics, and recursive types. Test representative JSON values in both directions because a generated static type is not proof that Serde emits or accepts it.

JavaScript `number` cannot represent every Rust integer exactly. Never silently export `i64`, `u64`, `i128`, `u128`, `isize`, or `usize` as unrestricted `number`. Define a domain policy using decimal strings, semantic BigInt with a compatible IPC representation, or range-checked newtypes. Likewise decide whether bytes are arrays, base64 strings, or `Uint8Array`, and whether dates are strings, epoch values, or semantic `Date` at each phase.

## Verification Contract

Run Rust unit and command tests, capability allow/deny tests, generated-binding diff checks, TypeScript compilation, frontend integration tests, and platform packaging checks. Cover malformed IPC, oversized payloads, denied permissions, window-specific routing, cancellation, channel backpressure, listener cleanup, plugin absence, remote-content isolation, updater signature failure, and upgrade from a previous release. Keep automatic repository hooks offline and read-only; version downloads, packaging, signing, and updater tests belong in explicit workflows.

## Primary Sources

- [Tauri 2 releases](https://v2.tauri.app/release/), [plugin catalog](https://v2.tauri.app/plugin/), [capabilities](https://v2.tauri.app/security/capabilities/), and [CSP](https://v2.tauri.app/security/csp/)
- [Calling Rust](https://v2.tauri.app/develop/calling-rust/) and [calling the frontend](https://v2.tauri.app/develop/calling-frontend/)
- [Tauri updater](https://v2.tauri.app/plugin/updater/)
- [Specta releases](https://github.com/specta-rs/specta/releases) and [tauri-specta compatibility and releases](https://github.com/specta-rs/tauri-specta)
