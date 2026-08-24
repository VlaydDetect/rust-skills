# DesignBrief contract

Return only information useful for deciding or implementing the task. This is an auditable decision record, not private chain-of-thought.

## Required fields

```text
entry_layer: Mechanics | Design | Domain
decision_units:
  - id: stable identifier
    decision: contract being decided
    owner_profile: exactly one rust-engineering profile
coding_candidates: Rust mechanics that the mutating workflow must cover
helper_evidence: triggered helper results already obtained
constraints: confirmed facts that can change the decision
evidence: repository locations, tool output, or dated external sources
alternatives: viable options and their material trade-offs
decision: selected option and why it satisfies the constraints
verification: smallest evidence that can falsify the decision
confidence: High | Medium | Low
gaps: unresolved facts or assumptions
```

Mechanics, design, and domain are discovery lenses, not ownership roles. When this protocol runs inside a mutating workflow, `rust-design-protocol` is helper evidence and each discovered unit is transferred to its listed owner in the workflow `ProfileStack`.

Omit an alternative when it is not viable. If a missing user choice would materially change the result, state the blocker and ask one focused question. Otherwise make the narrowest reasonable assumption and disclose it.

## Layer movement

- Mechanics to design: move upward only when the local ownership, type, error, or concurrency correction would preserve the wrong boundary.
- Design to domain: move upward only when product, operational, regulatory, device, model, or deployment constraints select between designs.
- Domain to mechanics: translate the accepted constraint into a concrete owner profile, types, lifecycles, failure semantics, and verification.

Do not report invented domain requirements, generic best practices as facts, or internal reasoning tokens.

## Design protocol map

Load one branch at a time.

## Layer routing and comparisons

- [Three-layer router](./routing/router.md)
- [Worked routing examples](./routing/workflow.md)
- [Comparison and ambiguity protocol](./routing/negotiation.md)
- [Optional safety-tool integration](./routing/os-checker.md)

The router does not replace `rust-workflow`, install a prompt hook, or force negotiation for keywords.

## Mental models

- [Mental-model selection](./cognition/mental-model.md)
- [Thinking in Rust patterns](./cognition/thinking-in-rust.md)

Use these for explanation and misconception repair. Confirm every analogy against the actual language invariant.

## Multi-lens analysis

- [Experimental parallel source protocol](./cognition/meta-cognition-parallel.md)
- [Layer 1 mechanics lens](./analysis/layer1-analyzer.md)
- [Layer 2 design lens](./analysis/layer2-analyzer.md)
- [Layer 3 domain lens](./analysis/layer3-analyzer.md)
- [Evidence confidence rubric](./negotiation/confidence-rubric.md)
- [Source response format](./negotiation/response-format.md)

Reuse its layer lenses and synthesis checks. Do not launch three agents by default; sequential analysis is the normal path.

## Full cognitive protocol

Load one retained document only when its trigger applies:

- [Layer definitions](./cognition/layer-definitions.md) for L1 mechanics, L2 design, and L3 domain routing.
- [Reasoning framework](./cognition/reasoning-framework.md) for upward, downward, or bidirectional constraint tracing.
- [Negotiation protocol](./negotiation/negotiation-protocol.md) and [response templates](./negotiation/negotiation-templates.md) only when work was actually delegated and evidence must be synthesized.
- [Error escalation](./cognition/error-protocol.md) after repeated evidence shows the current layer or approach is wrong; three attempts are not mandatory.
- [Externalized cognition](./cognition/externalization.md) for long tasks that need inspectable decision and evidence artifacts, never private chain-of-thought logs.
- [Hook patterns](./cognition/hooks-patterns.md) as a workflow-checkpoint catalog only. It does not authorize additional automatic host hooks.

## Worked and operational references

- [Context optimization](./analysis/context-optimization.md) preserves source
  guidance on progressive disclosure and isolated work with product limits on
  forced forks and parallelism.
- [E0382 trading-system example](./examples/e0382-trading-system.md) is
  a worked upward/downward trace. Its domain assumptions and `Arc` choice must
  be re-established before reuse.
