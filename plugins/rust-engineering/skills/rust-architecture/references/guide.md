# Rust Architecture Field Guide

This guide is the detailed policy for `rust-architecture`. It consolidates the decisions, workflows, and examples required by this profile in the dual-host plugin.

## Core Model

- Hexagonal architecture separates application or domain policy from adapters through inward-owned ports.
- A use-case boundary can often be a function or concrete service; interfaces belong only at real variation or effect boundaries.
- Values crossing boundaries should be domain-owned or explicit DTOs with translation at the edge.
- Fake ports test domain decisions without reproducing every infrastructure behavior; integration tests still cover real adapters.
- Commands change state and queries observe it, but a strict CQRS split is worthwhile only when models or scaling genuinely differ.
- Architecture quality is the ability to change one concern without unrelated changes, not the number of layers or patterns present.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| Pure domain calculation | Function or concrete type | No external variation needs a port |
| Database or network capability | Domain-owned port and adapter | Keeps foreign lifecycle and types at the edge |
| One deployment and team | Modular monolith | Avoids distributed operational cost |
| Read and write models genuinely diverge | Evaluate CQRS | Different performance or consistency needs may justify separation |
| Audit log alone | Append audit record | Event sourcing is unnecessary without state reconstruction requirements |

## Common Failure Modes

- Creating ports for every function and types with only one foreseeable implementation.
- Letting ORM, HTTP, runtime, or broker types become domain contracts.
- Spreading wiring through domain modules instead of one composition boundary.
- Adopting CQRS, event sourcing, or microservices from fashion rather than requirements.
- Designing all layers before a vertical slice proves boundaries and error translation.

## Required Evidence

- Use cases, invariants, effects, trust boundaries, consistency, deployment, and failure requirements.
- A dependency diagram showing policy inward and adapters outward.
- One end-to-end vertical slice with real and fake boundary evidence.
- Explicit rejected complexity and the future trigger that would justify it.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.

## Design protocol map

- [Entities, value objects, aggregates, repositories, and invariants](./domains/domain-overview.md)

Use the vocabulary only after identifying real identity, consistency, transaction, and ownership requirements. Prefer modules and concrete types over framework-like DDD scaffolding when they express the same contract.

For domain-specific constraint tracing, use the retained
[IoT, embedded, and cloud-native maps](./domains/domain-index.md). They feed
requirements into the existing owner skills rather than creating overlapping
framework skills.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-actor`](../../rust-concurrency/references/actor.md) — supporting; Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.
- [`rust-async-pattern`](../../rust-concurrency/references/async-pattern.md) — supporting; Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.
- [`rust-auth`](./domains/auth.md) — primary; Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- [`rust-cache`](./domains/cache.md) — primary; Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.
- [`rust-database`](./domains/database.md) — primary; Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- [`rust-distributed`](../../rust-distributed-systems/references/distributed.md) — supporting; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.
- [`rust-embedded`](./domains/embedded-runtime.md) — primary; no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.
- [`rust-error-advanced`](../../rust-errors/references/error-advanced.md) — supporting; Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.
- [`rust-middleware`](./domains/middleware.md) — primary; Request pipelines, ordering, short-circuiting, context propagation, cancellation, retries, timeouts, and cross-cutting policy.
- [`rust-web`](./domains/web.md) — primary; HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- [`rust-xacml`](./domains/xacml.md) — primary; Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return the decision to its owner after coding constraints or helper evidence have been stated.
