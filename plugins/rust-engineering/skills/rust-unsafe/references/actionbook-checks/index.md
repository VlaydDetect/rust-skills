# Actionbook internal unsafe rule index

Load only the rules relevant to the operation under review. Each retained file
contains the full source rationale and examples plus a product adaptation note
that resolves outdated or over-broad advice.

## General and abstraction safety

| ID | Review question |
|---|---|
| [`general-01`](rules/general-01-no-abuse.md) | Is unsafe solving a real low-level contract rather than hiding a design error? |
| [`general-02`](rules/general-02-not-for-perf.md) | Does measured evidence justify the unsafe optimization? |
| [`general-03`](rules/general-03-no-alias.md) | Does naming expose review-sensitive behavior without substituting for soundness? |
| [`safety-01`](rules/safety-01-panic-safety.md) | Are all panic, unwind, and abort paths invariant-preserving? |
| [`safety-02`](rules/safety-02-verify-invariants.md) | Is every operation precondition assigned and proven? |
| [`safety-03`](rules/safety-03-no-uninit-api.md) | Can safe code observe uninitialized or invalid values? |
| [`safety-04`](rules/safety-04-double-free.md) | Do partial moves and panics preserve exactly-once destruction? |
| [`safety-05`](rules/safety-05-send-sync.md) | Are manual `Send` and `Sync` impls sound for access and destruction? |
| [`safety-06`](rules/safety-06-no-raw-ptr-api.md) | Does a raw-pointer API enforce or correctly expose caller obligations? |
| [`safety-07`](rules/safety-07-unsafe-pair.md) | Is an unchecked counterpart actually measured and required? |
| [`safety-08`](rules/safety-08-no-mut-from-immut.md) | What enforces exclusivity for mutation through shared access? |
| [`safety-09`](rules/safety-09-safety-comment.md) | Does each `SAFETY` comment prove preconditions from local facts? |
| [`safety-10`](rules/safety-10-safety-doc.md) | Are public unsafe caller obligations complete and verifiable? |
| [`safety-11`](rules/safety-11-assert-not-debug.md) | Is a release-build invariant enforced rather than debug-asserted away? |

## Pointers, unions, layout, and resources

| ID | Review question |
|---|---|
| [`ptr-01`](rules/ptr-01-no-thread-share.md) | Who synchronizes and reclaims a pointee shared across threads? |
| [`ptr-02`](rules/ptr-02-prefer-nonnull.md) | Which facts beyond non-nullness does the pointer wrapper require? |
| [`ptr-03`](rules/ptr-03-phantomdata.md) | Do ownership, drop-check, variance, and auto traits match the model? |
| [`ptr-04`](rules/ptr-04-alignment.md) | Are bounds, alignment, value validity, and byte order all proven? |
| [`ptr-05`](rules/ptr-05-no-const-to-mut.md) | Is mutation authorized by `UnsafeCell` or exclusive provenance? |
| [`ptr-06`](rules/ptr-06-prefer-cast.md) | Does the cast preserve the intended provenance and mutability contract? |
| [`union-01`](rules/union-01-avoid-except-ffi.md) | Is a union necessary, and how is active-field validity tracked? |
| [`union-02`](rules/union-02-no-cross-lifetime.md) | Can a union fabricate a lifetime or invalid representation? |
| [`mem-01`](rules/mem-01-repr-layout.md) | Which layout guarantees hold on every supported target? |
| [`mem-02`](rules/mem-02-no-other-process.md) | Is cross-boundary memory authorized and synchronized by an explicit protocol? |
| [`mem-03`](rules/mem-03-no-auto-drop-foreign.md) | Does allocation, borrowing, and destruction stay with the correct owner? |
| [`mem-04`](rules/mem-04-reentrant.md) | Does the selected platform API avoid hidden shared state for this target? |
| [`mem-05`](rules/mem-05-bitfield-crates.md) | Is std bit manipulation sufficient before adding a dependency? |
| [`mem-06`](rules/mem-06-maybeuninit.md) | Is every element initialized and dropped exactly once on every path? |
| [`io-01`](rules/io-01-raw-handle.md) | Is a raw handle owned or borrowed for the complete operation lifetime? |

## Canonical rulebook cross-links

Use these established product rules alongside the Actionbook prompt; do not
duplicate findings under both IDs:

| Concern | Canonical product rule |
|---|---|
| Minimize unsafe scope | `unsafe-minimize-scope` |
| Local operation proof | `unsafe-safety-comment` |
| Partial initialization | `unsafe-maybeuninit` |
| Manual auto traits | `unsafe-send-sync-manual` |
| Miri evidence | `unsafe-miri-ci` |

See [the complete retained inventory](source-rule-index.md),
[review protocol](overview.md), and [review checklist](checklists/review-unsafe.md).

