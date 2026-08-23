# Rust Database Field Guide

Research baseline: **2026-08-23**. Re-run `rust-research` before relying on SDK, server, transport, storage-engine, or method details. At this snapshot the official SurrealDB Rust reference required Rust 1.89 or newer and documented server compatibility through 3.2.4; treat that as dated evidence, not a timeless range.

## Persistence Contract

Start with deployment topology, authority for schema, consistency and isolation needs, transaction size, concurrent writers, expected failure modes, latency and throughput, data lifetime, recovery point and time objectives, and whether the application can operate during migration or partial outage.

Keep four lifecycles distinct:

1. process-level runtime or driver initialization;
2. client or pool startup, health, capacity, and shutdown;
3. request or unit-of-work transaction scope;
4. durable schema, backup, restore, and retention across releases.

A client should normally be constructed once for the application scope, cloned or borrowed as designed by the SDK, and bounded by connection, in-flight request, queue, and timeout limits. Do not create a new client per query or hide an unbounded queue behind a cheap clone.

## Transactions, Retries, and Queries

Define the business invariant and make the transaction cover exactly the reads and writes needed to protect it. Keep it short; never hold it while waiting for a user, UI event, remote service without a deadline, or arbitrary retry sleep. Every path must commit once or cancel or roll back. Account for APIs where commit, cancel, or result extraction consumes the transaction or response value.

Classify failures before retrying. Connection loss, serialization conflicts, timeouts, constraint violations, authentication failure, malformed queries, and application rejection do not share one policy. Retry only documented transient failures with bounded attempts, jitter, cancellation, and an overall deadline. Make the complete operation idempotent using a natural key, request key, version check, or transactional outbox pattern; retrying an individual statement can duplicate side effects.

Bind user data through the driver's parameter API. Never build query text with interpolated values, including identifiers unless the API provides a safe identifier mechanism and an allowlist. Parameter binding prevents syntax injection but does not validate authorization, path scope, cardinality, or result size.

## Versioned Schema and Recovery

Keep schema, indexes, permissions, and data transformations in reviewable versioned migrations. Record applied migration identity and checksum. Test from the oldest supported production state, a fresh database, and the immediately previous release. A migration is incomplete until its operational rollout and recovery path are known.

For shared production systems prefer:

1. **expand**: add compatible fields, tables, indexes, or permissions;
2. **application cutover**: deploy code that can tolerate both states, backfill under bounded load, and verify;
3. **contract**: remove old structures only after all readers and rollback windows have moved.

Do not rely on a down migration for destructive recovery: restoring data often requires a tested backup or forward repair. Exercise backup and restore, measure duration, verify integrity and permissions, and document key management, snapshot consistency, retention, and point-in-time limitations.

## SurrealDB Deployment Matrix

Pin a tested tuple of Rust toolchain, `surrealdb` SDK version, server version, transport, authentication mode, and embedded engine. Enable only required Cargo features because transports and embedded engines can bring different native dependencies, binary size, platform support, and operational behavior.

Treat the main modes as distinct products:

- **WebSocket** is stateful and suitable for sessions and live behavior, but needs reconnect, in-flight request, authentication refresh, and resubscription policy.
- **HTTP** is request-oriented and stateless at the transport layer; confirm which SDK features and transaction semantics are available for the exact release.
- **Embedded** runs storage in the process and needs explicit filesystem ownership, single- or multi-process locking rules, durability, sync, snapshots, compaction, retention, backup, restore, and shutdown sequencing.

One globally managed client lifecycle is the default. Bound simultaneous queries and response sizes, propagate cancellation, and make shutdown stop new work before closing streams and storage.

## SurrealDB Query and Transaction Rules

Use `.bind(...)` for every user value. After `query().await`, inspect per-statement failures with the version-appropriate [`Response`](https://docs.rs/surrealdb/latest/surrealdb/struct.Response.html) API such as `.check()` or `.take_errors()` before treating a multi-statement request as successful or consuming dependent results. A successful transport future can contain statement-level errors. Be mindful that `take`, `check`, and related methods may mutate or consume response state; order result extraction deliberately.

Use typed result DTOs at the persistence boundary rather than exposing SDK-native values through the application. Validate record identity, cardinality, optional rows, and permission-filtered empty results. Put maximum result and traversal sizes in the query or application boundary instead of collecting an unbounded response.

For explicit transactions, use the exact SDK or SurrealQL transaction API supported by the pinned matrix. Keep all statements under one cancellation scope, cancel on any intermediate application or statement error, and commit only after required preconditions are known. Do not mix a consuming transaction API with later calls to a moved client or response; shape ownership around the real signatures.

## Live Queries

A live query is a long-lived replicated view, not a durable global event log. Define:

- the owner and explicit cancellation path;
- reconnect delay, authentication refresh, and resubscription;
- stable event identity or version for deduplication;
- bounded buffering and slow-consumer behavior;
- what snapshot or query repairs events lost during a disconnect;
- how initial snapshot and live tail avoid or tolerate a race;
- ordering scope and conflict handling across multiple writers.

Make reconnect idempotent and observable. On a gap, rebuild from an authoritative query or version cursor if supported; do not assume global total order merely because one stream appeared ordered in a local test.

## SurrealQL Migrations and Permissions

Store schemafull definitions, indexes, events, access methods, and permissions in versioned `.surql` files. Review permissions as data access policy, not only as migration syntax. Test least-privilege identities and permission-filtered reads, writes, live queries, and schema operations. A schemafull declaration does not replace application validation for domain invariants or resource limits.

For indexes, measure build and write amplification, verify query-plan use, and plan online rollout. Backfills should be resumable, rate-limited, observable, and safe to rerun. Never combine a destructive schema change and irreversible data rewrite into an untested single deployment step.

## Test Matrix

Use an isolated real server or the exact embedded engine for integration semantics; mocks are suitable only for application branching. Cover statement-level partial failures, concurrent conflicts, timeout and cancellation, reconnect, permission denial, client shutdown, migration from historical state, large and malformed results, live-query gaps, backup, and restore. Keep server and SDK versions in test output.

## Primary Sources

- [SurrealDB Rust SDK reference](https://surrealdb.com/docs/reference/rust) and [Rust SDK methods](https://surrealdb.com/docs/reference/rust/methods)
- [SurrealDB Rust language and connection modes](https://surrealdb.com/docs/languages/rust)
- [`surrealdb::Response` documentation](https://docs.rs/surrealdb/latest/surrealdb/struct.Response.html)
- [SurrealDB releases](https://surrealdb.com/releases)
