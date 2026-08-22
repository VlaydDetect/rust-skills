# Unsafe Code

Prefix: `unsafe-` · 7 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when an unsafe operation or safe wrapper needs an explicit validity, aliasing, initialization, layout, thread, panic, or drop proof.
- Defer when a safe standard-library or already accepted crate abstraction enforces the same invariant.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Source decision |
|---|---|---|---|
| [`unsafe-extern-block`](../rules/unsafe-extern-block.md) | `conditional` | `rust-unsafe` | In Rust 2024, wrap `extern` blocks in `unsafe extern { }` and annotate each item as `safe` or `unsafe`. |
| [`unsafe-maybeuninit`](../rules/unsafe-maybeuninit.md) | `adapted` | `rust-unsafe` | Use `MaybeUninit<T>` for uninitialized memory; never use `mem::uninitialized()` or `mem::zeroed()` for types with validity invariants. |
| [`unsafe-minimize-scope`](../rules/unsafe-minimize-scope.md) | `conditional` | `rust-unsafe` | Keep `unsafe` blocks as small as possible — mark only the operation that requires unsafety, not the surrounding safe code. |
| [`unsafe-miri-ci`](../rules/unsafe-miri-ci.md) | `conditional` | `rust-unsafe` | Run `cargo miri test` in CI for every crate that contains `unsafe` code. |
| [`unsafe-no-mangle-unsafe`](../rules/unsafe-no-mangle-unsafe.md) | `adapted` | `rust-unsafe` | In Rust 2024, write `#[unsafe(no_mangle)]`, `#[unsafe(export_name = "...")]`, and `#[unsafe(link_section = "...")]` — not the bare attribute forms. |
| [`unsafe-safety-comment`](../rules/unsafe-safety-comment.md) | `conditional` | `rust-unsafe` | Write a `// SAFETY:` comment above every `unsafe` block and a `# Safety` section in every `unsafe fn`. |
| [`unsafe-send-sync-manual`](../rules/unsafe-send-sync-manual.md) | `adapted` | `rust-unsafe` | Document the invariants when manually implementing `Send` or `Sync`; prefer letting the compiler derive them automatically. |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
