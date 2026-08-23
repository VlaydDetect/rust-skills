# `crate-info` adapter

Actionbook intent: return current crate metadata and documentation.

Product route: `rust-research crate <name-or-package-id> inspect`.

1. If inside a Rust project, resolve through locked offline Cargo metadata.
2. If multiple package IDs match, show version/source choices and stop.
3. Return aliases, resolved features, target/dependency kinds, edition, MSRV, exact-version docs/repository links, retrieval date, confidence, and gaps.
4. If the crate is not adopted, hand candidate evaluation to `rust-crate-discovery`.

This adapter is read-only and never runs `cargo add`, `cargo update`, or dossier sync.
