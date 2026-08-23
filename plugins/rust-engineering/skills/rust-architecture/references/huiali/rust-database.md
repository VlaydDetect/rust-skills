# Huiali Database Protocol

> Product adaptation of `skills/rust-database/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-architecture`.
- Supporting profiles when needed: `$rust-errors`, `$rust-performance`.
- Scope retained: Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.
- Baseline correction: Use the project's actual database and durability contract. Do not infer an ORM, pool, isolation level, retry policy, or migration mechanism.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

# Rust Database Skill

## Core Question

**How do we guarantee data correctness while keeping queries and migrations operationally safe?**

## Persistence Architecture

- Keep repository/data-access layer separate from business logic.
- Define explicit transaction boundaries around business invariants.
- Choose stack by need:
  - `sqlx`: explicit SQL and compile-time query checks.
  - `diesel`: typed query builder with strong schema coupling.
  - `sea-orm`: async ORM convenience with rapid CRUD iteration.

## Transaction and Consistency Rules

- Keep transactions short.
- Do not perform network calls inside transactions.
- Handle deadlock/serialization retries with bounded policy.

## Query Performance

- Use indexes based on real access patterns.
- Detect and remove N+1 query behavior.
- Inspect query plans for slow paths.

## Migration Safety

- Prefer additive migrations for rolling deployments.
- Separate destructive changes into phased rollouts.
- Verify backward/forward compatibility windows.

## Common Pitfalls

- Long-lived transactions causing lock contention.
- Schema changes incompatible with old app versions.
- Inconsistent timezone/nullability handling across layers.
- Pool exhaustion under burst traffic.

## Review Checklist

- [ ] Transaction boundaries align with domain invariants.
- [ ] Retry/timeout policy is explicit for DB operations.
- [ ] Migrations are safe for rolling deploy.
- [ ] Query plans and indexes are validated.
- [ ] Metrics cover pool usage, latency, and error rates.

## Verification Commands

```bash
cargo check
cargo test
cargo clippy
cargo sqlx prepare
cargo sqlx migrate run
```

## Related Skills

- `rust-web`
- `rust-cache`
- `rust-observability`
