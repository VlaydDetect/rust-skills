# Rust changelog research lens

> The read-only `rust-researcher` role Official Rust release sources are authoritative.

Fetch Rust version changes from the Rust Blog release announcement and official release notes.

## URL

`https://doc.rust-lang.org/releases.html` and the matching Rust Blog release URL.

## Fetch

Use normal host web access when current external evidence is requested. A community release index may aid discovery but must not replace official notes.

## Output (Standard Mode)

```markdown
## Rust <Version> Release Notes

**Release Date:** <date>

### Language Features
- feature: desc

### Standard Library
- new/stabilized API: desc

### Cargo
- change: desc

### Breaking Changes
- note: desc
```

## Validation

1. Content contains version number
2. Has "Language" or "Features" sections
3. Not "version not found"
4. On failure: "Version {v} does not exist or fetch failed"

---

## Negotiation Mode

For migration or comparison, return the `DesignBrief` evidence/confidence/gaps fields.

### Confidence Assessment

| Data Found | Confidence |
|------------|------------|
| Full release notes | HIGH |
| Partial notes (some sections) | MEDIUM |
| Minimal info | LOW |
| Version not found | UNCERTAIN |

### Gap Categories

Standard gaps to check:

- [ ] Migration guide not available
- [ ] Edition changes not detailed
- [ ] Cargo changes incomplete
- [ ] MSRV impact unclear
- [ ] Deprecation notices missing
- [ ] Security fixes not listed

### Context Questions

When changelog request needs clarification:

| Situation | Question |
|-----------|----------|
| Migration | "Are you migrating from a specific version?" |
| Edition | "Do you need edition-specific changes?" |
| Feature focus | "Are you looking for a specific feature?" |
| Stability | "Stable, beta, or nightly?" |

### Negotiation Response Template

```markdown
## Negotiation Response

### Findings
**Version:** Rust <version>
**Release Date:** <date>

**Language Features:**
- Feature 1: description

**Stabilized APIs:**
- API 1: description

**Breaking Changes:**
- Change 1: description

### Confidence
- **Level**: [HIGH|MEDIUM|LOW|UNCERTAIN]
- **Reason**: [e.g., "Official Rust release announcement and release notes agree"]

### Gaps Identified
- [ ] [Specific gap 1]
- [ ] [Specific gap 2]

### Context Needed
- Q1: [If ambiguous]

### Metadata
- **Source**: blog.rust-lang.org and doc.rust-lang.org/releases.html
- **Coverage**: [e.g., "85% - missing detailed migration"]
```

Use `rust-design-protocol` when the release facts feed a design or migration decision.
