# Rust news protocol

> Adapted from Actionbook `rust-daily`. News research runs only on an explicit daily, weekly, or monthly request. It has no automatic fetch, persistent news cache, or scheduled background process.

## Time range

- `day`: rolling 24 hours ending at the research time.
- `week`: rolling seven days.
- `month`: rolling 30 days.

State start/end timestamps and timezone. Compare publication date with the date the reported event or release actually occurred.

## Source tiers

| Tier | Sources | Use |
|---|---|---|
| Primary | Rust Blog, Inside Rust, official release notes | Rust releases, compiler/library/Cargo facts, project announcements |
| Organization | Rust Foundation news, blog, and events | Foundation governance, programs, events, security and ecosystem initiatives |
| Curated community | This Week in Rust | Discovery and ecosystem aggregation; follow links for important claims |
| Low-trust signal | Reddit r/rust | Topic discovery and community reaction only |

Reddit score, title, or comment is never sufficient evidence for an API, toolchain, security, governance, or release claim.

## Collection

1. Fetch only sources relevant to the requested range/category.
2. Record title, canonical URL, publication date, event date when different, and source tier.
3. Deduplicate syndicated stories by canonical event; retain the primary source and optionally one community perspective.
4. For technical claims, open the linked primary release, RFC, repository, advisory, or documentation.
5. Exclude undated items that cannot be placed in the requested range, or list them separately as uncertain.
6. Retry one alternative access method on failure, then record the source as unavailable.

## Output

```text
Rust {Daily|Weekly|Monthly} Report
time_range; generated_at; timezone

Official
- date; title; event summary; why it matters; primary link

Foundation
- date; title; summary; primary link

Ecosystem
- date; title; verified summary; source and upstream links

Signals
- low-confidence topic; why it may deserve follow-up; signal link

Unavailable sources; confidence; gaps
```

Prefer a short report of material changes over filling every section. “No verified updates” is valid. Never fabricate a result to satisfy a per-source quota.
