# DesignBrief contract

Return only information useful for deciding or implementing the task. This is an auditable decision record, not private chain-of-thought.

## Required fields

```text
entry_layer: Mechanics | Design | Domain
owner_profile: exactly one rust-engineering profile
supporting_profiles: zero to two profiles
constraints: confirmed facts that can change the decision
evidence: repository locations, tool output, or dated external sources
alternatives: viable options and their material trade-offs
decision: selected option and why it satisfies the constraints
verification: smallest evidence that can falsify the decision
confidence: High | Medium | Low
gaps: unresolved facts or assumptions
```

Omit an alternative when it is not viable. If a missing user choice would materially change the result, state the blocker and ask one focused question. Otherwise make the narrowest reasonable assumption and disclose it.

## Layer movement

- Mechanics to design: move upward only when the local ownership, type, error, or concurrency correction would preserve the wrong boundary.
- Design to domain: move upward only when product, operational, regulatory, device, model, or deployment constraints select between designs.
- Domain to mechanics: translate the accepted constraint into a concrete owner profile, types, lifecycles, failure semantics, and verification.

Do not report invented domain requirements, generic best practices as facts, or internal reasoning tokens.
