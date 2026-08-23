# Rust Question Router

> Adapted from Actionbook `rust-router`. `rust-workflow` remains the automatic entrypoint. This reference supplies a cognitive routing model, not an all-Rust keyword hook or a requirement to expose private reasoning.

> **Version:** 2.0.0 | **Last Updated:** 2025-01-22
>
> **v2.0:** Context optimized - detailed examples moved to sub-files

## Meta-Cognition Framework

### Core Principle

Start at the layer that controls correctness. Answer a local question directly; trace across layers only when the local decision depends on design or domain constraints.

```
Layer 3: Domain Constraints (WHY)
├── Product, operational, regulatory, and deployment constraints
├── rust-ml when ML semantics control the task
└── "Why must the system behave this way?"

Layer 2: Design Choices (WHAT)
├── Architecture patterns, DDD concepts
├── rust-architecture, performance, ecosystem, lifecycle, errors, idioms
└── "What pattern should I use?"

Layer 1: Language Mechanics (HOW)
├── Ownership, borrowing, lifetimes, traits
├── rust-ownership, traits, errors, concurrency, unsafe
└── "How do I implement this in Rust?"
```

### Routing by Entry Point

| User Signal | Entry Layer | Direction | First Skill |
|-------------|-------------|-----------|-------------|
| E0xxx error | Layer 1 | Trace UP ↑ | m01-m07 |
| Compile error | Layer 1 | Trace UP ↑ | Error table below |
| "How to design..." | Layer 2 | Check L3, then DOWN ↓ | rust-design-protocol or rust-architecture |
| "Building an ML system" | Layer 3 | Trace DOWN ↓ | rust-ml |
| "Best practice..." | Layer 2 | Both directions when context matters | owning profile |
| Performance issue | Layer 1 → 2 | Measure, then trace as needed | rust-performance |

### Conditional domain loading

Load a domain profile only when its constraints change the language or design decision:

| Domain Keywords | L1 Skill | L3 Skill |
|-----------------|----------|----------|
| ML model, tensor, device, batching, inference | relevant L1 owner | **rust-ml** |
| Other domain terminology | relevant L1 owner | Use repository specifications; do not invent a domain skill |

---

## Host-neutral workflow adaptation

### Comparison and ambiguity protocol

Use a comparison brief only when alternatives or missing context materially affect the answer:

| Query Contains | Action |
|----------------|--------|
| Explicit alternatives with different trade-offs | Compare against the stated constraints |
| "Best practice" without context | State which missing facts could reverse the recommendation |
| Domain plus compiler error | Start from the error; load domain constraints only if they change the fix |
| Ambiguous scope | Ask only when the unresolved choice would materially change the result |

**When negotiation is required, include:**

```markdown
## Design Brief

**Query Type:** [Comparative | Cross-domain | Synthesis | Ambiguous]
**Entry Layer:** [Mechanics | Design | Domain]

### Evidence: [Source or repository location]
**Confidence:** HIGH | MEDIUM | LOW | UNCERTAIN
**Gaps:** [What's missing]

## Decision
[Selected option and relevant trade-offs]

**Overall Confidence:** [Level]
**Disclosed Gaps:** [Gaps user should know]
```

> **详细协议见:** `patterns/negotiation.md`

---

### Project baseline precedence

Preserve the target project's toolchain, MSRV, edition, resolver, CI, and lint policy. For a greenfield project, use the Cargo default stable edition. Declare an MSRV only when compatibility is a real contract and verify it with that toolchain. Select individual Clippy lints from project evidence; do not enable `pedantic` or deny all warnings universally.

---

## Layer 1 Skills (Language Mechanics)

| Pattern | Route To |
|---------|----------|
| move, borrow, lifetime, E0382, E0597 | rust-ownership (`m01`) |
| Box, Rc, Arc, RefCell, Cell | rust-ownership (`m02`) |
| mut, interior mutability, E0499, E0502, E0596 | rust-ownership (`m03`) |
| generic, trait, inline, monomorphization | rust-traits (`m04`) |
| type state, phantom, newtype | rust-traits or rust-api-design (`m05`) |
| Result, Error, panic, ?, anyhow, thiserror | rust-errors (`m06`) |
| Send, Sync, thread, async, channel | rust-concurrency (`m07`) |
| unsafe, raw pointer, transmute | **rust-unsafe** |
| FFI, extern, ABI | **rust-unsafe-ffi** |

## Layer 2 Skills (Design Choices)

| Pattern | Route To |
|---------|----------|
| domain model, business logic | rust-architecture (`m09`) |
| performance, optimization, benchmark | rust-performance (`m10`) |
| integration, interop, bindings | rust-ecosystem (`m11`) |
| resource lifecycle, RAII, Drop | rust-ownership (`m12`) |
| domain error, recovery strategy | rust-errors (`m13`) |
| mental model, how to think | rust-design-protocol (`m14`) |
| anti-pattern, common mistake, pitfall | rust-idioms (`m15`) |

## Layer 3 Skills (Domain Constraints)

| Domain Keywords | Route To |
|-----------------|----------|
| ml, tensor, model, inference | rust-ml |
| any other domain | repository specifications and the owning general profile; no synthetic domain skill |

---

## Error Code Routing

| Error Code | Route To | Common Cause |
|------------|----------|--------------|
| E0382 | rust-ownership | Use of moved value |
| E0597 | rust-ownership | Lifetime too short |
| E0506 | rust-ownership | Cannot assign to borrowed |
| E0507 | rust-ownership | Cannot move out of borrowed |
| E0515 | rust-ownership | Return local reference |
| E0716 | rust-ownership | Temporary value dropped |
| E0106 | rust-ownership | Missing lifetime specifier |
| E0596 | rust-ownership | Cannot borrow as mutable |
| E0499 | rust-ownership | Multiple mutable borrows |
| E0502 | rust-ownership | Borrow conflict |
| E0277 | rust-traits or rust-concurrency | Trait bound not satisfied; inspect the bound |
| E0308 | rust-traits | Type mismatch |
| E0599 | rust-traits | No method found |
| E0038 | rust-traits | Trait not dyn-compatible |
| E0433 | rust-ecosystem | Cannot find crate/module |

---

## Functional Routing Table

| Pattern | Route To | Action |
|---------|----------|--------|
| latest version, what's new | **rust-research** | Use current primary sources |
| API, docs, documentation | **rust-research** or **rust-documentation** | Separate research from editing |
| code style, naming, clippy | **rust-style-clippy** plus `rust-coding-rules` | Select contextual rules |
| unsafe code, FFI | **rust-unsafe** or **rust-unsafe-ffi** | Select relevant safety checks |
| code review | **rust-review** | Findings-first, read-only review |

---

## Priority Order

1. **Identify cognitive layer** (L1/L2/L3)
2. **Load the product owner profile**
3. **Trace through layers** (UP or DOWN)
4. **Cross-reference skills** as indicated in "Trace" sections
5. **Return a concise decision, evidence, verification, confidence, and gaps**

### Keyword Conflict Resolution

| Keyword | Resolution |
|---------|------------|
| `unsafe` | **rust-unsafe**; use **rust-unsafe-ffi** when an ABI is crossed |
| `error` | **rust-errors**, with domain semantics when confirmed |
| `RAII` | **rust-ownership**, supported by rust-architecture for system lifecycle |
| `crate` | **rust-research** for current facts, **rust-dependencies** for an adopted crate |
| `tokio` | **rust-research** for current API facts, **rust-concurrency** for concepts and protocols |

**Priority Hierarchy:**

```
1. Error codes (E0xxx) → Direct lookup, highest priority
2. Explicit comparison → Build a bounded DesignBrief
3. Domain keywords + error → Load domain constraints only when they change the fix
4. Specific crate keywords → Route current facts to rust-research
5. General concept keywords → Route to the one profile that owns correctness
```

---

## Sub-Files Reference

| File | Content |
|------|---------|
| `patterns/negotiation.md` | Negotiation protocol details |
| `examples/workflow.md` | Workflow examples |
| `integrations/os-checker.md` | OS-Checker integration |
