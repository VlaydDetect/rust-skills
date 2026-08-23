# Actionbook `/rust-review` adapter

The source command treated review as a Clippy run. In this product, translate
that intent into the full findings-first `rust-review` workflow:

1. Resolve the requested diff or bounded path and inspect real callers.
2. Read the repository lint configuration before selecting a command.
3. Run the narrow repository-native Clippy command only when execution is
   requested or proportionate; preserve its configured lint levels and feature
   matrix.
4. Treat compiler and Clippy diagnostics as evidence, not the whole review.
   Add behavioral, API, safety, lifecycle, concurrency, compatibility, and test
   findings only when current code proves their premises.
5. Do not prescribe `unwrap_used`, `expect_used`, pedantic, or another lint
   globally. Do not install or run Miri, advisory, geiger, or concurrency tools
   implicitly.
6. Return the canonical finding schema and `PASS`, `WARN`, `FAIL`, or
   `INCOMPLETE` verdict from `rust-review`.

Use the unsafe command adapters under `rust-unsafe` only when unsafe operations
or FFI boundaries are actually in scope.

