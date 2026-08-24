# Memory Optimization

Prefix: `mem-` · 17 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when a measured allocation, footprint, locality, move, or layout cost is material on the representative workload.
- Defer when there is no profile or size evidence, or the change would complicate ownership, portability, or correctness for a noise-level gain.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`mem-arena-allocator`](../rules/mem-arena-allocator.md) | `conditional` | `rust-performance` | Use arena allocators for batch allocations |
| [`mem-arrayvec`](../rules/mem-arrayvec.md) | `conditional` | `rust-performance` | Use `ArrayVec<T, N>` for fixed-capacity collections that never heap-allocate |
| [`mem-assert-type-size`](../rules/mem-assert-type-size.md) | `conditional` | `rust-performance` | Use static assertions to guard against accidental type size growth |
| [`mem-avoid-format`](../rules/mem-avoid-format.md) | `conditional` | `rust-performance` | Avoid `format!()` when string literals work |
| [`mem-box-large-variant`](../rules/mem-box-large-variant.md) | `conditional` | `rust-performance` | Box large enum variants to reduce overall enum size |
| [`mem-boxed-slice`](../rules/mem-boxed-slice.md) | `conditional` | `rust-performance` | Use `Box<[T]>` instead of `Vec<T>` for fixed-size heap data |
| [`mem-clone-from`](../rules/mem-clone-from.md) | `conditional` | `rust-performance` | Use `clone_from()` to reuse allocations when repeatedly cloning |
| [`mem-compact-string`](../rules/mem-compact-string.md) | `conditional` | `rust-performance` | Use compact string types for memory-constrained string storage |
| [`mem-drop-order`](../rules/mem-drop-order.md) | `conditional` | `rust-performance` | Know and control drop order: struct fields drop top-to-bottom, locals in reverse |
| [`mem-reuse-collections`](../rules/mem-reuse-collections.md) | `conditional` | `rust-performance` | Clear and reuse collections instead of creating new ones in loops |
| [`mem-smaller-integers`](../rules/mem-smaller-integers.md) | `conditional` | `rust-performance` | Use appropriately-sized integers to reduce memory footprint |
| [`mem-smallvec`](../rules/mem-smallvec.md) | `conditional` | `rust-performance` | Use `SmallVec` for usually-small collections |
| [`mem-take-replace`](../rules/mem-take-replace.md) | `conditional` | `rust-performance` | Use `mem::take` / `mem::replace` to move a value out of a `&mut` without cloning |
| [`mem-thinvec`](../rules/mem-thinvec.md) | `conditional` | `rust-performance` | Use `ThinVec<T>` for nullable collections with minimal overhead |
| [`mem-with-capacity`](../rules/mem-with-capacity.md) | `conditional` | `rust-performance` | Use `with_capacity()` when size is known |
| [`mem-write-over-format`](../rules/mem-write-over-format.md) | `conditional` | `rust-performance` | Use `write!()` into existing buffers instead of `format!()` allocations |
| [`mem-zero-copy`](../rules/mem-zero-copy.md) | `conditional` | `rust-performance` | Use zero-copy patterns with slices and `Bytes` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
