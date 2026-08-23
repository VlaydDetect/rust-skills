# Comparison and ambiguity protocol

> 比较查询和跨领域问题的处理协议

## When to Enable Negotiation

Use a compact comparison brief when alternatives, cross-layer constraints, or missing context can reverse the answer. Do not create an agent round-trip for a direct lookup or a local decision with adequate evidence.

| Query Pattern | Enable Negotiation | Reason |
|---------------|-------------------|--------|
| Single error code lookup | No | Direct answer |
| Single crate version | No | Direct lookup |
| "Compare X and Y" | When trade-offs matter | Multi-faceted |
| Domain + error | When domain constraints change the fix | Cross-layer context |
| "Best practices for..." | When context changes the recommendation | Requires synthesis |
| Ambiguous scope | When choices produce materially different outcomes | Needs clarification |
| Multi-crate question | When current evidence differs by crate | Multiple sources |

## Negotiation Decision Flow

```
Query Received
     │
     ▼
┌─────────────────────────────┐
│ Is query single-lookup?     │
│ (version, error code, def)  │
└─────────────────────────────┘
     │
     ├── Yes → Direct dispatch (no negotiation)
     │
     ▼ No
┌─────────────────────────────┐
│ Does query require:         │
│ - Comparison?               │
│ - Cross-domain context?     │
│ - Synthesis/aggregation?    │
│ - Multiple sources?         │
└─────────────────────────────┘
     │
     ├── Yes → Build a DesignBrief from bounded evidence
     │
     ▼ No
┌─────────────────────────────┐
│ Is scope ambiguous?         │
└─────────────────────────────┘
     │
     ├── Yes → Ask one blocking question or disclose the assumption
     │
     ▼ No
     └── Direct dispatch (no negotiation)
```

## Evidence collection

When comparison is needed:

```
1. Preserve the original task and decision criteria.
2. Inspect repository and current sources as appropriate.
3. Record:
   - Findings
   - Confidence (HIGH/MEDIUM/LOW/UNCERTAIN)
   - Gaps identified
   - Context questions (if any)
4. Evaluate evidence against the original intent.
```

## Orchestrator Evaluation

After receiving negotiation response:

| Confidence | Intent Coverage | Action |
|------------|-----------------|--------|
| HIGH | Complete | Synthesize answer |
| HIGH | Partial | May need supplementary query |
| MEDIUM | Complete | Accept with disclosed gaps |
| MEDIUM | Partial | Refine with context |
| LOW | Any | Refine or try alternative |
| UNCERTAIN | Any | Try alternative or escalate |

## Refinement Loop

If evidence is insufficient:

```
Pass 1: Initial bounded research
  │
  ▼ (LOW confidence or gaps block intent)
Pass 2: One refined query with:
  - Answers to agent's context questions
  - Narrowed scope
  │
  ▼ (still insufficient)
Stop and return the best-supported answer with disclosed gaps, or request the one missing user decision that changes the outcome.
```

## Stopping condition

Stop after one useful refinement unless the user explicitly asks for deeper research. Never loop merely to raise a confidence label.

## Negotiation Routing Examples

**Example 1: No Negotiation Needed**
```
Query: "What is tokio's latest version?"
Analysis: Single lookup
Action: Direct `rust-research crate` lookup
```

**Example 2: Negotiation Required**
```
Query: "Compare tokio and async-std for a web server"
Analysis: Comparative + domain context
Action: Compare current evidence against runtime, ecosystem, and deployment constraints
Expected: Structured responses from both runtime lookups
Evaluation: Check if web-server specific data found
```

**Example 3: Cross-Domain Negotiation**
```
Query: "E0382 in my trading system"
Analysis: Error code + domain context
Action:
  - Load rust-ownership because the error is defined
  - Inspect project trading/audit requirements only if they constrain ownership
Synthesis: Combine the compiler rule with confirmed domain requirements
```

## Output

Return the `DesignBrief` fields defined by `rust-design-protocol`: entry layer, constraints, evidence, alternatives, decision, verification, confidence, and gaps.
