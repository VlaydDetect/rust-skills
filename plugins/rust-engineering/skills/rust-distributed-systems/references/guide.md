# Rust Distributed Systems Field Guide

## Operation Contract

For each distributed operation record caller-visible identity, idempotency scope, authoritative state, invariant, command/result contract, deadline, retry policy, deduplication record, ordering key, version, and recovery owner. Distinguish a command accepted, durably recorded, applied, published, observed, and acknowledged.

## Failure Matrix

Evaluate failure before send, after send but before receive, before/after local persistence, before/after side effect, before/after publish, lost acknowledgement, duplicate delivery, reordering, consumer crash, coordinator crash, partition, stale lease holder, and recovery replay. Name which states are distinguishable and which remain uncertain.

## Retry and Idempotency

- Retry only classified transient or unknown outcomes and preserve cancellation/deadlines.
- Use a stable key at the effect boundary, not a newly generated key on every attempt.
- Bind deduplication records to operation semantics, result replay, retention, and version.
- Bound attempts and elapsed time; cap backoff and add jitter where synchronized retry storms are plausible.
- Do not stack hidden client, middleware, queue, and service retries without one aggregate budget.

## Coordination Models

Sagas compensate business effects but do not erase externally observed history. Transactional outbox connects a local state transition to eventual publication but still needs a relay and consumer idempotency. Consensus coordinates replicated state under stated fault assumptions. Two-phase commit can block and needs a real coordinator/recovery implementation. Select mature components and document their operational assumptions.

## Required Evidence

- Failure matrix and invariant.
- Versioned message/API schema and compatibility policy.
- Idempotency and retry-budget tests with a deterministic clock or model.
- Recovery, replay, duplicate, stale-leader, and cancellation scenarios.
- Operational ownership for retention, poison messages, dead letters, repair, and rollbacks.

## Compiling Example

The dependency-free fixture in `../examples/golden/` models a bounded retry and idempotency decision without network, clock, or storage dependencies.

## Specialized topic map

Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.

- [`rust-distributed`](./distributed.md) — primary; Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.

## Shared constraints

- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.
- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.
- Classify uncompiled Rust snippets as fragments unless a product golden fixture actually compiles them.
- Return ownership to the primary profile when supporting constraints have been stated.
