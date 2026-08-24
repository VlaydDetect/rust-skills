# Context Optimization Guide

> retain progressive disclosure and isolation heuristics, but do not force context forks, three-agent parallelism, fixed token estimates, or host-specific commands. Load one needed branch and delegate only bounded independent read-only work.


> Rust Skills context-optimization strategies and results

## Overview

Rust Skills uses three methods to optimize context consumption, reducing token usage by approximately **68%** in combination.

| Optimization method | Type | Applicable scenario | Savings |
|---------|------|---------|---------|
| **Split Skill content** | Static | Large reference skills | 50-60% |
| **context: fork** | Dynamic | Task-execution skills | 75-85% |
| **Three-layer parallel Fork** | Dynamic | Collaborative analysis across multiple skills | 65-75% |

---

## Method One: Split Skill Content (Static Optimization)

### Principle

Move non-core content from a large Skill into supporting files. Keep only the core routing logic in the main SKILL.md and load other content on demand.

### Implementation Example: rust-router

| Metric | Before | After | Savings |
|------|--------|--------|------|
| File size | 18.7 KB | 8.1 KB | **56%** |
| Approximate tokens | ~4,700 | ~2,000 | **~2,700 tokens** |

### File Structure

```
skills/rust-router/
├── SKILL.md (8.1 KB - core routing, always loaded)
├── patterns/
│   └── negotiation.md (negotiation protocol, loaded on demand)
├── examples/
│   └── workflow.md (workflow example, loaded on demand)
└── integrations/
    └── os-checker.md (integration notes, loaded on demand)
```

### Moved Content

| Content | Moved to | Size |
|------|--------|------|
| Negotiation Protocol | `patterns/negotiation.md` | 4.5 KB |
| Workflow Example | `examples/workflow.md` | 2.3 KB |
| OS-Checker Integration | `integrations/os-checker.md` | 1.3 KB |
| Skill File Paths | Deleted (redundant) | 1.5 KB |

### Key Point: Automatic Triggering Is Unaffected

Claude Code's automatic triggering mechanism depends only on the `description` field in the frontmatter:

```yaml
---
name: rust-router
description: "CRITICAL: Use for ALL Rust questions...
Triggers on: Rust, cargo, rustc, E0382, E0597..."
---
```

The SKILL.md body contains guidance used **after** triggering, so moving content into supporting files does not affect triggering.

### Applicable Scenarios

- Skills containing substantial reference material
- Skills with multiple usage scenarios
- Skills containing detailed examples or templates

---

## Method Two: Isolated Execution with context: fork (Dynamic Optimization)

### Principle

Use `context: fork` to run the Skill in an isolated subagent context. Intermediate work does not consume the main context; only a summarized result is returned.

### Configuration

```yaml
---
name: my-task-skill
description: "Task description"
context: fork
agent: general-purpose  # Or Explore
---
```

### Implementation Examples

| Skill | Typical execution tokens | Main context after Fork | Savings |
|-------|---------------|----------------|------|
| `rust-skill-creator` | ~3,000 | ~500 (summary) | **~83%** |
| `core-dynamic-skills` | ~2,000 | ~400 | **~80%** |
| `core-fix-skill-docs` | ~1,500 | ~300 | **~80%** |
| `rust-daily` | ~2,500 | ~500 | **~80%** |

### Fork Characteristics

| Characteristic | Description |
|------|------|
| Isolated execution | The Skill runs in a new, independent context |
| No conversation history | The subagent **cannot access** the main conversation history |
| Result summary | Output is summarized before returning to the main conversation |
| Environment inheritance | The working directory, CLAUDE.md, and environment variables are inherited |

### Inheritance

```
Main Context
├── Conversation history ─────► ❌ Not inherited
├── Current working directory ─► ✅ Inherited
├── CLAUDE.md ─────────────────► ✅ Inherited (as a reference)
├── Preloaded skills ──────────► ✅ Accessible
└── Environment variables ─────► ✅ Inherited
```

### Applicable Scenarios

- Independently executed tasks such as creating files or synchronizing data
- Operations that do not need conversation history
- Exploration or research tasks

### Inapplicable Scenarios

- Tasks that require interactive follow-up questions
- Tasks where the complete reasoning process must remain visible
- Tasks whose result details are too important to summarize

---

## Method Three: Three-Layer Parallel Fork (Experimental)

### Principle

Using the meta-cognition framework's three-layer model, distribute analysis in parallel to three isolated layer analyzers. Each analyzes independently and returns a summary, and the main context performs cross-layer synthesis.

### Architecture

```
User Question
     │
     ▼
meta-cognition-parallel (coordinator)
     │
     ├─── Fork → layer1-analyzer ──► L1 summary
     │           (language-mechanics analysis)
     │
     ├─── Fork → layer2-analyzer ──► L2 summary    [parallel]
     │           (design-choice analysis)
     │
     └─── Fork → layer3-analyzer ──► L3 summary
                 (domain-constraint analysis)
     │
     ▼
Cross-Layer Synthesis (main context)
     │
     └─► Domain-correct architectural solution
```

### Context-Consumption Comparison

**Conventional approach (main context):**
```
├── Read m01-ownership        +1,200 tokens
├── Read m02-resource         +1,000 tokens
├── Read domain-fintech       +1,500 tokens
├── Intermediate reasoning    +2,500 tokens
└── Final answer              +1,800 tokens
                          ────────────
                          ~8,000 tokens
```

**Three-layer parallel Fork:**
```
├── L1 summary returned             +600 tokens
├── L2 summary returned             +600 tokens
├── L3 summary returned             +600 tokens
└── Cross-layer synthesis + answer  +700 tokens
                          ────────────
                          ~2,500 tokens
```

**Savings: ~69%**

### Related Files

- `skills/meta-cognition-parallel/SKILL.md` - Coordination Skill
- `agents/layer1-analyzer.md` - Language-mechanics analysis (m01-m07)
- `agents/layer2-analyzer.md` - Design-choice analysis (m09-m15)
- `agents/layer3-analyzer.md` - Domain-constraint analysis (domain-*)

### Command

```bash
/meta-parallel <your Rust question>
```

### Test Scenarios

```bash
# Test 1: trading system
/meta-parallel The trading system reports E0382 because the trade record was moved

# Test 2: Web API
/meta-parallel Multiple handlers in a Web API need to share a database connection pool

# Test 3: CLI tool
/meta-parallel How should a CLI tool prioritize configuration files and command-line arguments?
```

---

## Estimated Combined Effect

Assume a typical Rust question-and-answer session:

| Stage | Before | After |
|------|--------|--------|
| rust-router loading | 4,700 | 2,000 |
| Multi-skill analysis | 8,000 | 2,500 |
| Task execution | 3,000 | 500 |
| **Total** | **15,700** | **5,000** |
| **Savings** | - | **~68%** |

---

## Selection Decision Tree

```
Question type
    │
    ├── Large reference Skill?
    │   └── YES → Method one: split content
    │             Move non-core content to supporting files
    │
    ├── Independently executed task?
    │   └── YES → Method two: context: fork
    │             Add context: fork to the frontmatter
    │
    └── Multi-layer collaborative analysis?
        └── YES → Method three: three-layer parallel Fork
                  Use meta-cognition-parallel
```

---

## Best Practices

### 1. Content-Splitting Principles

- Keep core routing logic in SKILL.md
- Move examples and templates to `examples/`
- Move integration notes to `integrations/`
- Move detailed references to `references/`

### 2. Fork Usage Principles

- Use fork only for task-oriented Skills
- Do not use fork for reference or guidance Skills
- Do not use fork when user interaction is required

### 3. Parallel-Analysis Principles

- Each analysis task should be independent and have no dependencies
- Complete synthesis and reasoning in the main context
- Explicitly pass all necessary information to each fork

---

## Validation Checklist

### Method-One Validation

- [ ] Test automatic rust-router triggering
  ```bash
  claude -p "How do I fix E0382?"
  claude -p "Compare tokio and async-std"
  ```

### Method-Two Validation

- [ ] Test Fork skill execution
  ```bash
  /sync-crate-skills
  /rust-daily
  ```

### Method-Three Validation

- [ ] Test three-layer parallel analysis
  ```bash
  /meta-parallel The trading system reports E0382
  ```

---

## Version History

| Version | Date | Optimization |
|------|------|---------|
| 2.0.0 | 2025-01-22 | Split rust-router content (56% savings) |
| 2.0.4 | 2025-01-22 | Added context: fork to four skills (thanks @pinghe) |
| 2.0.5 | 2025-01-22 | Experimental support for three-layer parallel Fork |

---

**Created:** 2025-01-21
**Updated:** 2025-01-22
**Status:** ✅ Implemented (Methods 1-3)
