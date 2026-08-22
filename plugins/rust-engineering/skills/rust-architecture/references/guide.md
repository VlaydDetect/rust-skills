# Rust Architecture Field Guide

This guide is the detailed policy for `rust-architecture`. It synthesizes the craft Rust architecture, ports and adapters, CQRS, and events guidance; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

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
