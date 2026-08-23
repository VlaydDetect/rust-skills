---
name: rust-database
description: Engineer Rust database transactions, client and pool lifecycles, schema migrations, retries, testing, backup, and SurrealDB integration. Use when persistence semantics are primary; do not route generic database work to a UI framework skill.
---

# Rust Database Engineering

Own persistence lifecycle and transactional correctness. Treat client libraries as protocol implementations, not substitutes for an explicit consistency, migration, retry, and recovery contract.

## Use This Skill When

- Rust code opens a database client or pool, runs transactions, migrates schema, retries operations, or restores persisted state.
- SurrealDB server, WebSocket, HTTP, or embedded modes require feature, lifecycle, query, transaction, or live-query decisions.
- A change needs schema evolution, idempotency, integration tests, backup, restore, retention, or deployment sequencing.

## Workflow

1. Record deployment mode, server and SDK compatibility, consistency needs, transaction boundaries, capacity, durability, and recovery objectives.
2. Select only required transport and storage features; define one bounded client or pool lifecycle with backpressure.
3. Bind all user values, inspect per-statement errors, and keep transactions short with explicit commit or cancellation paths.
4. Store schema, indexes, and permissions as versioned migrations; use expand, application cutover, then contract for shared production changes.
5. Define retryable failures, idempotency keys, reconnect behavior, live-query gap recovery, and shutdown ordering.
6. Test migrations, rollback or forward recovery, concurrency, disconnection, backup, and restore against the deployed mode.

## Decision Rules

- Never interpolate user input into query text when a binding API is available.
- A successful request future does not prove every statement succeeded; inspect the response before using results or committing dependent work.
- Do not hold a transaction while waiting for UI or human input.
- Live-query reconnection requires cancellation, resubscription, deduplication, and a gap-recovery policy; do not assume global writer order.
- Embedded mode needs explicit path permissions, locking, sync, snapshots, retention, and restore behavior.
- Stable releases are the default; exact prerelease pins require a demonstrated capability need and an upgrade plan.

## Boundaries and Hand-offs

- `rust-distributed-systems` owns cluster-wide delivery, consensus, and retry semantics beyond the database boundary.
- `rust-serialization` owns stored or transported byte formats; `rust-architecture` owns application layering.
- `rust-tauri` owns desktop IPC and capabilities even when a Tauri command calls the database.
- Use `rust-research` to verify the current SDK, server, storage engine, and method semantics.

## Detailed Reference

Read [Rust database field guide](references/guide.md) before changing transaction, migration, SurrealDB, live-query, or embedded persistence behavior.
