# Ownership and Borrowing

Prefix: `own-` · 12 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than eight rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when ownership, borrowing, lifetime, pointer, mutation, or drop semantics control correctness.
- Defer when independent ownership is required, or the proposed borrowing shape would leak a guard or lifetime into unrelated callers.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`own-arc-shared`](../rules/own-arc-shared.md) | `conditional` | `rust-ownership` | Use `Arc<T>` for thread-safe shared ownership |
| [`own-borrow-over-clone`](../rules/own-borrow-over-clone.md) | `canonical` | `rust-ownership` | Prefer `&T` borrowing over `.clone()` |
| [`own-clone-explicit`](../rules/own-clone-explicit.md) | `canonical` | `rust-ownership` | Use explicit `Clone` for types where copying has meaningful cost |
| [`own-copy-small`](../rules/own-copy-small.md) | `conditional` | `rust-ownership` | Implement `Copy` for small, simple types |
| [`own-cow-conditional`](../rules/own-cow-conditional.md) | `conditional` | `rust-ownership` | Use `Cow<'a, T>` for conditional ownership |
| [`own-lifetime-elision`](../rules/own-lifetime-elision.md) | `canonical` | `rust-ownership` | Rely on lifetime elision rules; add explicit lifetimes only when required |
| [`own-move-large`](../rules/own-move-large.md) | `conditional` | `rust-ownership` | Move large types instead of copying; use `Box` if moves are expensive |
| [`own-mutex-interior`](../rules/own-mutex-interior.md) | `conditional` | `rust-ownership` | Use `Mutex<T>` for interior mutability across threads |
| [`own-rc-single-thread`](../rules/own-rc-single-thread.md) | `conditional` | `rust-ownership` | Use `Rc<T>` for shared ownership in single-threaded contexts |
| [`own-refcell-interior`](../rules/own-refcell-interior.md) | `conditional` | `rust-ownership` | Use `RefCell<T>` for interior mutability in single-threaded code |
| [`own-rwlock-readers`](../rules/own-rwlock-readers.md) | `conditional` | `rust-ownership` | Use `RwLock<T>` when reads significantly outnumber writes |
| [`own-slice-over-vec`](../rules/own-slice-over-vec.md) | `canonical` | `rust-ownership` | Accept `&[T]` not `&Vec<T>`, `&str` not `&String` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most eight rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
