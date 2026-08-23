# Low-level Rust Async Internals protocol

<!-- low-level-source-family: rust-async-internals; source=skills/rust/rust-async-internals/SKILL.md; sha256=656622037474693c396b6b336fc98f562b45fa9d81455e98900ee0edbb48d433; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/rust/rust-async-internals/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-concurrency`.
- Supporting profiles: `$rust-pin`, `$debugging`.
- Retained scope: Future polling, Waker replacement, task scheduling, pinning, cancellation, blocking boundaries, and async diagnostics.
- Baseline correction: A Future may be polled repeatedly and must arrange a wake after returning Pending. Do not spawn work on every poll, assume a runtime, or treat stack pinning as inherently unsafe.
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

- `The Future trait — poll model` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.
- `Implementing a simple Future` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.
- `Pin and Unpin` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.
- `tokio task model` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.
- `tokio-console — async task inspector` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.
- `Blocking in async — common mistake` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.
- `select! and join! pitfalls` — inspect when relevant; source `skills/rust/rust-async-internals/SKILL.md`.

## Failure modes and guardrails

- A wake is a request to poll, not proof that progress occurred.
- Cancellation may occur at every suspension point.
- Lock-free code requires a state-machine and ordering proof, not only passing stress tests.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 9 unique source block bodies: 8 `fragment`, 1 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`async-future`](https://rust-lang.github.io/async-book/02_execution/02_future.html) — Future poll and wake contract; `current`, reviewed 2026-08-23.
- [`async-pinning`](https://rust-lang.github.io/async-book/part-reference/pinning.html) — Pinning and async state-machine constraints; `current`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
