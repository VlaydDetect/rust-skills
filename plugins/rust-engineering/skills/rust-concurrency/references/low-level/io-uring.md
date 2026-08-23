# Low-level Io Uring protocol

<!-- low-level-source-family: io-uring; source=skills/async-io/io-uring/SKILL.md; sha256=0d395b4d6973995138d6623cce7cf9ef51d42037089bb144a96e41fd01c66e39; revision=bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608 -->

> Reviewed adaptation of `skills/async-io/io-uring/SKILL.md` and 0 supporting Markdown file(s). The source is evidence, not executable product policy.

## Routing and retained scope

- Primary owner: `$rust-concurrency`.
- Supporting profiles: `$rust-unsafe-ffi`, `$rust-performance`.
- Retained scope: Submission/completion ownership, operation lifetimes, registered resources, multishot operations, cancellation, zero-copy, and fallback I/O.
- Baseline correction: Kernel version, opcode support, library/runtime API, security restrictions, and buffer lifetime must be verified. Never retain a buffer until only submission rather than completion.
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

- `SQ/CQ model` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Minimal liburing example` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Common prep operations` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Multi-shot operations` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Provided buffer rings` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Fixed files and registered buffers` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Zero-copy send` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `tokio-uring (Rust)` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `io_uring vs epoll` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.
- `Security considerations` — inspect when relevant; source `skills/async-io/io-uring/SKILL.md`.

## Failure modes and guardrails

- A wake is a request to poll, not proof that progress occurred.
- Cancellation may occur at every suspension point.
- Lock-free code requires a state-machine and ordering proof, not only passing stress tests.
- If a required tool, target, component, hardware device, symbol file, corpus, or cache is absent, report `SKIP` or request authorization; never install or mutate the host implicitly.
- Treat tool output as bounded evidence. Record exact command, version, target, scope, result, and residual risk.

## Source example disposition

This family contains 12 unique source block bodies: 10 `fragment`, 2 `rejected`. Blocks not reproduced here remain individually hashed and reasoned in the coverage ledger.

## Evidence gate

- [`rustc-platform-support`](https://doc.rust-lang.org/beta/rustc/platform-support.html) — Rust target support tiers and target-specific notes; `current-beta`, reviewed 2026-08-23.

Before executing a version-sensitive command, re-check the exact project toolchain or resolved tool version. Official Rust/Cargo evidence owns language and build behavior; tool-owner documentation owns external CLI syntax.
