# Low-level Memory Model protocol

<!-- low-level-source-family: memory-model; source=skills/low-level-programming/memory-model/SKILL.md; sha256=286469c6132de57d9ba01dc81cffc14e6df0d465b97700ea89fe68a1e733b8f0; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/low-level-programming/memory-model/SKILL.md` and 1 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-concurrency`.
- Supporting profiles: `$rust-unsafe`, `$rust-research`.
- Retained scope: Atomic ordering, happens-before, release sequences, fences, publication, lock-free state machines, and common ordering failures.
- Baseline correction: C++ examples are comparative evidence, not Rust proof. Write the Rust state machine and justify each ordering with the Rust memory model and primitive documentation.
- Project toolchain, MSRV, Edition, target, resolved dependencies, CI, hardware, operating system, and explicit user contract override this reference.

## Required context

- state owner and task/thread topology.
- wake or notification edges.
- queue and resource bounds.
- cancellation and shutdown.
- ordering and memory-model invariants.

## Decision protocol

1. Draw the state machine, ownership transfers, suspension/completion points, and failure paths.
2. For Future code, pair every Pending result with a path that can wake the latest Waker.
3. Keep buffers, permits and operations alive until the documented completion/cancellation point.
4. Bound work, queues, retries and spawned tasks; define who closes, drains and joins.
5. Use schedule/race tools only after the invariant and minimized reproducer are explicit.

## Source-derived knowledge map

The following source topics were retained as investigation branches. Their headings are not commands and do not authorize installation, privilege, network access, or configuration changes.

- `Happens-Before Relation` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `Memory Order Rules Table` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `SeqCst Total Order` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `CAS (Compare-And-Swap) Patterns` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `Lock-Free Stack` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `Platform Memory Models` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `std::atomic_flag (Simplest Atomic)` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `Rust Ordering Equivalents` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `Quick Selection Guide` — inspect when relevant; source `skills/low-level-programming/memory-model/references/cpp-memory-ordering.md`.
- `Memory ordering overview` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `Memory orderings` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `C++ std::atomic` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `Choosing the right ordering` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `Common patterns` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `Rust atomics` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `Fences` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.
- `Common mistakes` — inspect when relevant; source `skills/low-level-programming/memory-model/SKILL.md`.

## Failure modes and guardrails

- A wake is a request to poll, not proof that progress occurred.
- Cancellation may occur at every suspension point.
- Lock-free code requires a state-machine and ordering proof, not only passing stress tests.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 12 unique source block bodies: 12 `fragment`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`miri`](https://github.com/rust-lang/miri/) — Miri setup, coverage, limitations, and flags; `nightly-version-sensitive`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
