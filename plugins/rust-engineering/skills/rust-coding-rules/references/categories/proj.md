# Project Structure

Prefix: `proj-` · 14 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a demonstrated module, crate, visibility, target, feature, MSRV, or build-script boundary needs clearer ownership.
- Defer when the change is driven only by file size or speculative reuse and would add package, public API, build, or migration cost.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`proj-bin-dir`](../rules/proj-bin-dir.md) | `canonical` | `rust-cargo-build` | Put multiple binaries in src/bin/ |
| [`proj-build-rs-minimal`](../rules/proj-build-rs-minimal.md) | `canonical` | `rust-cargo-build` | Keep `build.rs` minimal, deterministic, and idempotent |
| [`proj-feature-additive`](../rules/proj-feature-additive.md) | `conditional` | `rust-cargo-build` | Design Cargo features to be strictly additive |
| [`proj-flat-small`](../rules/proj-flat-small.md) | `canonical` | `rust-module-layout` | Keep small projects flat |
| [`proj-lib-main-split`](../rules/proj-lib-main-split.md) | `conditional` | `rust-module-layout` | Keep `main.rs` minimal, logic in `lib.rs` |
| [`proj-mod-by-feature`](../rules/proj-mod-by-feature.md) | `canonical` | `rust-module-layout` | Organize modules by feature, not type |
| [`proj-mod-rs-dir`](../rules/proj-mod-rs-dir.md) | `conditional` | `rust-module-layout` | Use mod.rs for multi-file modules |
| [`proj-msrv-declare`](../rules/proj-msrv-declare.md) | `canonical` | `rust-stable` | Declare `rust-version` (MSRV) in Cargo.toml and test it in CI |
| [`proj-prelude-module`](../rules/proj-prelude-module.md) | `conditional` | `rust-module-layout` | Create prelude module for common imports |
| [`proj-pub-crate-internal`](../rules/proj-pub-crate-internal.md) | `canonical` | `rust-module-layout` | Use pub(crate) for internal APIs |
| [`proj-pub-super-parent`](../rules/proj-pub-super-parent.md) | `canonical` | `rust-module-layout` | Use pub(super) for parent-only visibility |
| [`proj-pub-use-reexport`](../rules/proj-pub-use-reexport.md) | `conditional` | `rust-module-layout` | Use pub use for clean public API |
| [`proj-workspace-deps`](../rules/proj-workspace-deps.md) | `conditional` | `rust-workspace` | Use workspace dependency inheritance for consistent versions across crates |
| [`proj-workspace-large`](../rules/proj-workspace-large.md) | `conditional` | `rust-workspace` | Use workspaces for large projects |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
