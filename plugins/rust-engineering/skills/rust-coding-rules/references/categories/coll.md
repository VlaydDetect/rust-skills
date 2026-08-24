# Collections

Prefix: `coll-` · 4 addressable rules.

Load this index only when the current Rust decision matches the category. Select the smallest RuleSet (normally no more than nine rules) and then read the linked rule files; do not treat the table as a blanket checklist.

## Category Boundary

- Select when ordering, uniqueness, lookup, range, queue, priority, locality, or mutation operations determine the collection.
- Defer when an alternative collection changes required ordering or security semantics merely for assumed speed.
- The listed owner profile controls the decision; this rulebook supplies concrete checks and examples without consuming a primary or supporting profile slot.

## Rules

| Rule | Status | Owner | Decision |
|---|---|---|---|
| [`coll-binaryheap`](../rules/coll-binaryheap.md) | `canonical` | `rust-stdlib` | Use `BinaryHeap` for a priority queue or repeated max-extraction |
| [`coll-map-choice`](../rules/coll-map-choice.md) | `conditional` | `rust-stdlib` | Pick the map by access pattern: `HashMap` (fast, unordered), `BTreeMap` (sorted / range queries), `IndexMap` (insertion order) |
| [`coll-seq-choice`](../rules/coll-seq-choice.md) | `canonical` | `rust-stdlib` | Default to `Vec`; use `VecDeque` for queue/deque behaviour; avoid `LinkedList` |
| [`coll-set-membership`](../rules/coll-set-membership.md) | `conditional` | `rust-stdlib` | Use `HashSet`/`BTreeSet` for membership tests and dedup, not linear `Vec::contains` |

## Batch Audit

For a broad audit, evaluate this category in batches of at most nine rules. Carry forward only evidence-backed findings; do not load another category until the current batch is closed or explicitly deferred.
