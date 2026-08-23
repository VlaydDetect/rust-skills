# Actionbook navigation modes

Choose one mode from the navigation question. Use the first available source in this order: fresh `graphify-out`, host-native LSP/rust-analyzer, locked offline Cargo commands, then `rg` plus source confirmation. A stale graph or textual match is a candidate, not proof.

## Definitions and references

- [Definitions, references, and workspace lookup](actionbook/rust-code-navigator/overview.md)

## Symbol inventory

- [Document and workspace symbol analysis](actionbook/rust-symbol-analyzer/overview.md)

## Trait exploration

- [Traits, implementations, methods, and dispatch](actionbook/rust-trait-explorer/overview.md)

Confirm receiver types, blanket impls, cfg branches, proc-macro generation, and dyn construction sites.

## Call graph

- [Incoming and outgoing call hierarchy](actionbook/rust-call-graph/overview.md)

Label edges `confirmed`, `candidate`, or `unknown`. Function pointers, trait objects, callbacks, macros, and FFI can make a static graph incomplete.

## Dependency graph

- [Cargo dependency visualization](actionbook/rust-deps-visualizer/overview.md)

Use `cargo metadata --format-version 1 --locked --offline` for identity and resolved edges. Use `cargo tree --locked --offline` only as a presentation or focused inversion aid. If locked offline resolution fails, report the exact gap rather than falling back to manifest grep.
