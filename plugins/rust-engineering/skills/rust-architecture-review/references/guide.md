# Rust Architecture Review Field Guide

This guide is the detailed policy for `rust-architecture-review`. It synthesizes the craft architecture-review workflow, Rust architecture profiles, and graph-assisted repository navigation practices; it is adapted for a dual-host workflow rather than copied as an upstream transcript.

## Core Model

- Architecture review relates current dependency and ownership structure to expected change, test, deployment, and failure boundaries.
- Cohesion asks whether a component's elements change for the same reasons; coupling asks how many external reasons force it to change.
- Layer leaks appear when domain policy depends on storage, transport, framework, runtime, or generated types.
- God components combine unrelated policy, coordination, state, and I/O such that small changes touch broad surfaces.
- Over-engineering appears as indirection, generic extension, duplicate DTOs, or distributed boundaries without current variants or requirements.
- A useful health rating is accompanied by concrete strengths, high-leverage risks, evidence limits, and a staged remediation path.

## Decision Table

| Situation | Prefer | Reason or evidence |
|---|---|---|
| One broad component with cohesive purpose | Observe, not automatically split | Size alone is weak evidence |
| Stable domain imports adapter types | Confirmed direction leak | Policy cannot evolve independently of infrastructure |
| Many one-implementation interfaces | Assess for speculative abstraction | Indirection may not buy test or variation value |
| Shared crate imported everywhere | Inspect responsibility and change fan-out | A dependency magnet can hide ownership |
| Graph suggests an edge | Open source and confirm | Indexes can be stale or syntactic |

## Common Failure Modes

- Producing a directory tour with no judgment about change impact or dependency direction.
- Declaring every cross-layer import a defect without understanding composition and adapter roles.
- Recommending microservices, CQRS, or many crates as a universal cleanup.
- Using metrics or graph communities as conclusions without code-path verification.
- Listing dozens of equal-priority observations instead of a small leverage-ranked remediation sequence.

## Required Evidence

- A confirmed package and key-module dependency map with representative vertical traces.
- Findings containing concrete edges, impact, confidence, and smallest remediation direction.
- Strengths and intentional boundaries as well as defects, so proposals preserve what works.
- A health verdict and staged priorities tied to product change and operational requirements.

## Completion Contract

State the selected option, rejected alternatives that materially affect correctness, assumptions that remain unproved, and the smallest verification needed. Do not turn preferences into repository policy without evidence in code, manifests, CI, documentation, or an explicit user decision.
