# Meta-Cognition Example: E0382 in a Trading System

> retained worked source example, not a universal prescription. Confirm the actual domain requirement before moving beyond Layer 1; Arc, clone, and the assumed fintech audit constraint are alternatives to evaluate, not defaults. Return decision evidence, not private chain-of-thought.


> Demonstrates how the three-layer cognition model traces a surface error back to domain constraints to produce a deeper solution.

## User Question

> "My trading system reports E0382 because the data was moved."

---

## Conventional Answer (Bad)

```
"Fix it with .clone()."
```

**Problem**: This fixes only the surface symptom without understanding the root cause.

---

## Meta-Cognition Trace

### Step 1: Identify the Entry Layer

| Signal | Entry layer | Trace direction |
|------|--------|----------|
| E0382 | **Layer 1** (language mechanics) | Trace upward ↑ |

**Initial skill**: m01-ownership

---

### Step 2: Layer 1 Analysis (m01-ownership)

**Core question**: Who should own this data?

| Error | Do not just say | Ask instead |
|-------|----------|--------|
| E0382 | "Clone it" | **Who should own this data?** |

**Reasoning prompts**:
1. What is this data's domain role? → "Transaction record" = Transaction Record
2. Is the ownership design intentional? → Check the domain constraints
3. Fix the symptom or redesign? → Trace upward to understand the cause

---

### Step 3: Trace Upward to Layer 3 (domain-fintech)

**Discovered domain constraints**:

| Domain rule | Design constraint | Rust implementation |
|----------|----------|-----------|
| **Audit trail** | Immutable records | Arc<T>, prohibit mutation |
| Consistency | Transaction boundaries | Explicit ownership |

**Key insight**:
```
Rule: Every transaction must be immutable and traceable
Reason: Regulatory compliance and dispute resolution
Rust: Share with Arc<T> and use an event-sourcing pattern
```

---

### Step 4: Trace Downward to the Layer 2 Design

Trace downward from domain-fintech:
```
"Immutable transaction records are required"
    ↓ m09-domain: Model them as Value Objects
    ↓ m01-ownership: Use Arc to share immutable data
```

**Design decision**: Transaction records are **Value Objects** and should be **shared immutably**, not moved or repeatedly cloned.

---

## Meta-Cognition Answer (Good)

### Trace Chain

```
┌─ Layer 1: E0382 = ownership error
│  Problem: a value is used after being moved
│      ↑
├─ Layer 3: trading-system domain constraint
│  Rule: transaction records must be immutable and traceable (audit requirement)
│  Meaning: data should be shared rather than moved or copied
│      ↓
└─ Layer 2: design-pattern selection
   Solution: use Arc<TransactionRecord> to share immutable data
```

### Recommended Fix

```rust
// Before (E0382)
fn process_transaction(record: TransactionRecord) {
    save_to_db(record);        // record moved here
    send_notification(record); // E0382: use of moved value
}

// After (Meta-Cognition Fix)
use std::sync::Arc;

fn process_transaction(record: Arc<TransactionRecord>) {
    save_to_db(Arc::clone(&record));       // Arc clone = cheap
    send_notification(Arc::clone(&record)); // Still works
    audit_log(record);                      // Last use
}
```

### Why Use Arc Instead of clone()?

| Approach | Cost | Semantics | Domain fit |
|------|------|------|------------|
| `.clone()` | Copies all data | Creates an independent copy | ❌ Violates the single source of truth |
| `Arc<T>` | Increments the reference count | Shares the same data | ✅ Satisfies audit requirements |

**Reason**:
- `clone()` copies all data → wastes memory and violates the "single source of truth"
- `Arc<T>` shares the same data → satisfies audit requirements because every reference points to the same record

### Reasoning-Chain Summary

```
E0382 → ask "Who should own the data?" → discover that it is an audit record →
domain constraints require immutability and traceability → design it for sharing with Arc<T> →
this is a design improvement, not a syntax-only fix
```

---

## Comparative Validation

| Criterion | Conventional answer | Meta-Cognition |
|----------|----------|----------------|
| Fixes the error | ✅ | ✅ |
| Explains the cause | ❌ | ✅ |
| Considers the domain | ❌ | ✅ |
| Recommends a design | ❌ | ✅ |
| Prevents future problems | ❌ | ✅ |

---

## Key Lessons

### 1. Do Not Stop at Layer 1

A surface error such as E0382 is only a symptom; the real problem may be in the design or domain layer.

### 2. Domain Constraints Determine the Design

Audit requirements in the financial domain require data to be immutable and traceable, which directly affects the ownership design.

### 3. Choosing Arc vs Clone

| Scenario | Choice |
|------|------|
| Data must evolve independently | `clone()` |
| Data represents a shared fact | `Arc<T>` |
| Financial audit records | `Arc<T>` (single source of truth) |

---

## Related Skills

| Skill | Role |
|-------|------|
| m01-ownership | Layer 1 entry point and ownership mechanics |
| m02-resource | Choosing Arc or Rc smart pointers |
| m09-domain | Modeling Value Objects vs Entities |
| domain-fintech | Financial-domain constraints |

---

## References

- `_meta/reasoning-framework.md` - Complete tracing framework
- `skills/m01-ownership/SKILL.md` - Ownership skill
- `skills/domain-fintech/SKILL.md` - Financial-domain constraints
