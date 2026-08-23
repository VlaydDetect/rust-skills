# `sync-crate-skills` adapter

Design protocol intent: create missing crate-specific skills. Product route: explicit `rust-research crate <package-id> sync`.

1. Run `cargo metadata --format-version 1 --locked --offline`.
2. Require one exact package ID; do not sync every dependency by default.
3. Compare the selected dossier's Cargo/evidence fingerprints.
4. Research exact-version primary sources.
5. Write only `.rust-engineering/crate-skills/<name>/<version>/<id-hash>/`.
6. Report changed paths and staleness evidence.

Networked resolution, lockfile changes, home-directory wrappers, and bulk sync require separate explicit authorization. No prompt-on-open behavior exists.
