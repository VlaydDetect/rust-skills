# Clippy and Linting

Prefix: `lint-` · 13 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when the repository needs a scoped formatting, lint, warning-level, cfg, or CI policy under its actual toolchain.
- Defer when a broad lint group or automatic fix would change API, MSRV, semantics, generated code, or unrelated dirty files.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Source decision |
|---|---|---|---|
| [`lint-cargo-metadata`](../rules/lint-cargo-metadata.md) | `conditional` | `rust-style-clippy` | Enable clippy::cargo for published crates |
| [`lint-cfg-check`](../rules/lint-cfg-check.md) | `conditional` | `rust-style-clippy` | Enable `unexpected_cfgs` and declare known cfgs to catch feature-gate typos |
| [`lint-clippy-nursery-selected`](../rules/lint-clippy-nursery-selected.md) | `adapted` | `rust-style-clippy` | Enable high-value `clippy::nursery` lints selectively, not the whole group |
| [`lint-deny-correctness`](../rules/lint-deny-correctness.md) | `adapted` | `rust-style-clippy` | `#![deny(clippy::correctness)]` |
| [`lint-missing-docs`](../rules/lint-missing-docs.md) | `adapted` | `rust-style-clippy` | Warn on missing documentation for public items |
| [`lint-pedantic-selective`](../rules/lint-pedantic-selective.md) | `adapted` | `rust-style-clippy` | Enable clippy::pedantic selectively |
| [`lint-rustfmt-check`](../rules/lint-rustfmt-check.md) | `adapted` | `rust-style-clippy` | Run cargo fmt --check in CI |
| [`lint-unsafe-doc`](../rules/lint-unsafe-doc.md) | `conditional` | `rust-style-clippy` | Require documentation for unsafe blocks |
| [`lint-warn-complexity`](../rules/lint-warn-complexity.md) | `adapted` | `rust-style-clippy` | Enable clippy::complexity for simpler code |
| [`lint-warn-perf`](../rules/lint-warn-perf.md) | `adapted` | `rust-style-clippy` | Enable clippy::perf for performance improvements |
| [`lint-warn-style`](../rules/lint-warn-style.md) | `adapted` | `rust-style-clippy` | Enable clippy::style for idiomatic code |
| [`lint-warn-suspicious`](../rules/lint-warn-suspicious.md) | `adapted` | `rust-style-clippy` | Enable clippy::suspicious for likely bugs |
| [`lint-workspace-lints`](../rules/lint-workspace-lints.md) | `adapted` | `rust-style-clippy` | Configure lints at workspace level for consistent enforcement |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
