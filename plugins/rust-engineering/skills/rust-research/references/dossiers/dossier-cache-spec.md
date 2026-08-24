# Documentation Cache Specification

> Use this specification only for cache-key, evidence, and invalidation decisions. Do not create a global cache, use fixed TTLs, or expose internal commands. The product default is read-only research; explicitly requested crate sync writes a project-local exact-version Cargo-metadata dossier.


> Local caching mechanism for documentation retrieved by an agent

## Cache Goals

- Reduce repeated network requests
- Improve response speed
- Support offline use while the cache entry remains valid

## Cache Locations

### Priority

1. **Skill references directory** (when the skill exists)
   ```
   ~/.claude/skills/{crate}/references/{item}.md
   ```

2. **Global cache directory** (fallback)
   ```
   ~/.claude/cache/rust-docs/{source}/{path}.json
   ```

### Path Mapping

| Documentation type | Cache path |
|----------|----------|
| docs.rs crate | `~/.claude/cache/rust-docs/docs.rs/{crate}/{item}.json` |
| std library | `~/.claude/cache/rust-docs/std/{module}/{item}.json` |
| releases.rs | `~/.claude/cache/rust-docs/releases.rs/{version}.json` |
| lib.rs | `~/.claude/cache/rust-docs/lib.rs/{crate}.json` |
| clippy | `~/.claude/cache/rust-docs/clippy/{lint}.json` |

## Cache Format

### JSON Structure

```json
{
  "meta": {
    "url": "https://doc.rust-lang.org/std/marker/trait.Send.html",
    "fetched_at": "2025-01-16T23:30:00Z",
    "expires_at": "2025-01-23T23:30:00Z",
    "source": "agent-browser",
    "version": "1"
  },
  "content": {
    "title": "std::marker::Send",
    "signature": "pub unsafe auto trait Send { }",
    "description": "Types that can be transferred across thread boundaries...",
    "sections": {
      "implementors": "...",
      "examples": "..."
    }
  }
}
```

### Markdown Format (for references/)

```markdown
---
url: https://doc.rust-lang.org/std/marker/trait.Send.html
fetched_at: 2025-01-16T23:30:00Z
expires_at: 2025-01-23T23:30:00Z
source: agent-browser
---

# std::marker::Send

**Signature:**
```rust
pub unsafe auto trait Send { }
```

**Description:**
Types that can be transferred across thread boundaries...
```

## Expiration Times

| Documentation type | Default expiration | Description |
|----------|--------------|------|
| std library | 30 days | Stable and changes infrequently |
| crate docs (stable) | 7 days | The version may be updated |
| releases.rs | Never expires | Historical versions do not change |
| lib.rs (crate info) | 1 day | Version information changes quickly |
| clippy lints | 14 days | Updated with each Rust release |

## Agent Workflow

### 1. Check the Cache

```
1. Build the cache path
2. Check whether the file exists
3. Check whether it has expired (expires_at < now)
4. Return the cached content when it is valid
```

### 2. Retrieve and Cache

```
1. Retrieve with design-protocol + agent-browser
2. Parse the content
3. Generate a cache file in JSON or Markdown format
4. Save it to the corresponding path
5. Return the content
```

### 3. Force a Refresh

The user can request a forced refresh:
```
"Refresh the Send trait documentation"
"refresh tokio::spawn docs"
```

## Cache-Management Commands

### /rust-skills:cache-status

Show cache status:
```
Rust Docs Cache Status:
- std library: 45 items, 12MB
- docs.rs: 128 items, 34MB
- releases.rs: 15 items, 2MB
- Total: 188 items, 48MB

Expired: 23 items
```

### /rust-skills:cache-clean

Remove expired entries or clear the entire cache:
```
/rust-skills:cache-clean          # Remove expired entries
/rust-skills:cache-clean --all    # Clear all entries
/rust-skills:cache-clean tokio    # Clear a specific crate
```

## Implementation Locations

| File | Responsibility |
|------|------|
| `agents/docs-cache.md` | Shared instructions for checking and saving cache entries |
| `agents/docs-researcher.md` | Update: add caching logic |
| `agents/std-docs-researcher.md` | Update: add caching logic |
| `commands/cache-status.md` | Cache-status command |
| `commands/cache-clean.md` | Cache-clean command |
