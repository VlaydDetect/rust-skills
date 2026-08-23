# Rust Daily Reporter

> The read-only `rust-researcher` role Official and Foundation sources carry factual claims; Reddit is a low-trust discovery signal only.

Aggregate Rust news, filter by time range.

## Data Sources

| Category | URL |
|----------|-----|
| Low-trust signal | https://www.reddit.com/r/rust/hot/ |
| Ecosystem | https://this-week-in-rust.org/ |
| Official | https://blog.rust-lang.org/ |
| Official | https://blog.rust-lang.org/inside-rust/ |
| Foundation | https://rustfoundation.org/media/category/news/ |
| Foundation | https://rustfoundation.org/media/category/blog/ |
| Foundation | https://rustfoundation.org/events/ |

## Parameters

- `time_range`: day | week | month
- `category`: all | ecosystem | official | foundation

## Fetch Strategy

See: `_shared/fetch-strategy.md`

Use normal host web access. Follow curated/community items to their primary source before making a technical, release, security, or governance claim.

| Source | Primary Tool | Fallback |
|--------|--------------|----------|
| Reddit | Optional browser/web access | Mark as signal only |
| TWIR | Normal web access | Follow upstream links |
| Rust Blog | Normal web access | Official source |
| Foundation | Normal web access | Organization source |

No browser or MCP transport is mandatory, and no news source is fetched automatically.

## Time Filter

| Range | Filter |
|-------|--------|
| day | Last 24 hours |
| week | Last 7 days |
| month | Last 30 days |

## Output

```markdown
# Rust {Day|Week|Month} Report

**Time:** {start} - {end} | **Generated:** {now}

## Ecosystem
### Reddit r/rust
| Score | Title | Link |

### This Week in Rust
- Issue #{number} ({date}): highlights

## Official
| Date | Title | Summary |

## Foundation
| Date | Title | Summary |
```

## Validation (Required)

1. Check dates against the requested range and distinguish publication from event date.
2. Deduplicate the same event across sources.
3. Mark "No verified updates" when appropriate; do not fill quotas.
4. Retry one alternate access method, then report the source failure.
