# Quality gates

Prefer repository-native equivalents. Adapt placeholders to the effective project state.

| Evidence needed | Typical command |
|---|---|
| Formatting | `cargo fmt --all -- --check` |
| Type/build validity | `cargo check -p <package> --all-targets <features>` |
| Behavior | `cargo test -p <package> <test-filter> <features>` |
| Lints | `cargo clippy -p <package> --all-targets <features> -- -D warnings` |
| Documentation | `RUSTDOCFLAGS="-D warnings" cargo doc -p <package> --no-deps <features>` |
| Unsafe model | `cargo +nightly miri test -p <package> <features>` |
| API compatibility | repository-configured `cargo semver-checks` invocation |
| Dependency policy | repository-configured `cargo audit` or `cargo deny check` |
| Cross target | `cargo check -p <package> --target <triple> <features>` plus target link or runtime evidence |
| Nix evaluation | repository-configured `nix flake check --no-update-lock-file` |
| Performance | repository benchmark with the same profile, input, warm-up, machine, and statistic as baseline |

`<features>` means the supported feature selection, not automatically `--all-features`. Add `--locked` when the repository requires a committed lockfile to remain unchanged.

`cargo fmt -- --check` is acceptable because it checks without accepting rewrites. Do not run a formatter without its check flag in verification mode. Tool availability is a precondition, not permission to install it. A target `cargo check` proves type checking only; it does not prove linking, packaging, ABI compatibility, or runtime behavior.

Miri's presence does not guarantee that a sandbox can prepare its sysroot or unpack cached crates. Read the [Miri restricted-environment procedure](../../rust-unsafe/references/low-level/rust-sanitizers-miri.md) before classifying cache permission failures as missing tools. An authorized retry under the normal user account must use the host permission mechanism and retain the same focused test/build contract; no Administrator/root or ACL changes are implied.

For Python-based validators, verify the actual interpreter and its imports before declaring a dependency absent. A bundled runtime and the user's installed Python can have different packages. Prefer an existing suitable environment rather than installing a duplicate dependency.
