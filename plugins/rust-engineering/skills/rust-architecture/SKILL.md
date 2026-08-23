---
name: rust-architecture
description: Design Rust system boundaries, dependency direction, ports and adapters, domain ownership, composition roots, CQRS, and events proportionately. Use for new or changed architecture, not merely in-crate file organization.
---

# Rust Architecture

Own system-level boundaries, dependency direction, and composition for present product needs. Apply this profile directly for focused advice or load it from `rust-workflow` as the primary or a supporting profile.

## Use This Skill When

- A subsystem needs separation between domain logic and I/O, storage, transport, or framework adapters.
- Dependency direction, composition, test seams, commands and queries, or event flow must be designed.
- A proposed architecture risks coupling the domain to delivery or infrastructure details.

## Workflow

1. Start from use cases, invariants, trust boundaries, deployment, scale, consistency, and failure requirements rather than a named pattern.
2. Identify domain decisions and external effects; place ports where the domain needs capabilities from independently evolving adapters.
3. Make dependency direction point toward stable policy and keep transport, database, runtime, and framework types at adapters.
4. Choose modules or crates proportionately and define one composition root that wires concrete adapters.
5. Add CQRS, eventing, queues, or distributed boundaries only when read or write models, consistency, ownership, or scale requirements demand them.
6. Prove the design with one vertical slice and fake or in-memory adapters before broad scaffolding.

## Decision Rules

- Ports are owned by the policy that needs them, not by the infrastructure that implements them.
- Adapters translate errors, values, lifecycle, and concurrency instead of leaking foreign types inward.
- The composition root may know every concrete component; domain modules should not.
- Use functions and concrete types until variation, testing, or boundary ownership justifies a trait.
- Keep domain operations deterministic when possible and isolate clock, randomness, storage, network, and process effects.
- CQRS does not require event sourcing, and event sourcing is not a default persistence strategy.
- Events require ownership, ordering, idempotency, schema evolution, retry, and delivery semantics before implementation.
- Choose a modular monolith until independent deployment or ownership creates a concrete reason to distribute.

## Boundaries and Hand-offs

- `rust-workspace` and `rust-module-layout` own the physical package and file realization of accepted boundaries.
- `rust-architecture-review` owns read-only diagnosis of an existing structure; this profile designs the intended one.
- Use `rust-workflow` when the task includes implementation across the repository.
- Use `rust-review` for read-only findings and `rust-verify` for command evidence.

## Detailed Reference

Read [Rust Architecture field guide](references/guide.md) before making a consequential design choice. Use the [Design protocol domain-modelling protocol and domain constraint maps](./references/guide.md) when entity, value-object, aggregate, repository, invariant, IoT, embedded, or cloud-native constraints change the design. Keep conclusions tied to the repository's actual toolchain, targets, feature graph, and local instructions.

## Specialized Rust protocols

For additional topic detail, read the [Profile reference index](./references/guide.md) and load only the matching family reference.

## Low-level protocols

For low-level debugging, profiling, build, sanitizer, cross-target, ABI, async-internal, security, or hardware detail, read the [Low-level reference index](references/low-level-index.md) and load only the matching family. Apply its official-evidence and command-safety gate before execution.
