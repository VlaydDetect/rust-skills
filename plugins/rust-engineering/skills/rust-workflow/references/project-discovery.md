# Project discovery

Resolve facts in this order:

1. Instructions scoped to the edited path.
2. CI, task runner, and contributing commands that are actually maintained.
3. Effective Cargo state from `cargo locate-project`, `cargo metadata --no-deps`, manifests, and config.
4. Toolchain files, `rust-version`, edition, targets, and feature declarations.
5. Existing neighboring code and tests.
6. Generic guidance only where the project is silent.

Record a `ContextBrief` with the selected package, target, feature set, platform, edition, MSRV, public compatibility surface, repository-native commands, and lockfile policy. A workspace-wide `--all-features` run is invalid when features or targets are mutually exclusive.

Prefer `cargo locate-project --workspace` and `cargo metadata --no-deps` over assumptions based on the current directory. Read `Cargo.toml`, `.cargo/config*`, `rust-toolchain*`, task runners, and CI together: the effective build contract can be split across them.

When `graphify-out/` already exists and the task concerns architecture, navigation, or blast radius, query it before broad file reading. Confirm graph claims against current source. Do not rebuild or update the graph from an automatic hook.
