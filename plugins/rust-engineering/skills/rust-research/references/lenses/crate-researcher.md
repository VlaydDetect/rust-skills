# Crate research lens

> The read-only `rust-researcher` role Resolve project dependencies by exact Cargo package ID before using registry or documentation pages.

Fetch exact-version crate metadata, documentation, and maintenance evidence.

## Fetch

Use available sources in this order:
- `cargo metadata --format-version 1 --locked --offline` for project identity and features;
- exact-version docs.rs and the package's declared repository/source;
- crates.io metadata;
- lib.rs only as a discovery summary, never as sole API or suitability evidence.

## Output (Standard Mode)

```markdown
## <Crate Name>

**Version:** <latest>
**Description:** <short>

**Features:**
- `feature1`: desc

**Links:**
- docs.rs | crates.io | repo
```

## Validation

1. Content contains version number
2. Not a "crate not found" page
3. Has description
4. On failure: "Crate does not exist or fetch failed"

---

## Negotiation Mode

For a comparison, return the `DesignBrief` evidence/confidence/gaps fields.

### Confidence Assessment

| Data Found | Confidence |
|------------|------------|
| Version + description + features + docs | HIGH |
| Version + description + features | HIGH |
| Version + description | MEDIUM |
| Version only | LOW |
| Not found or error | UNCERTAIN |

**Degrading factors:**
- Last update > 2 years: -1 level
- No README: -1 level
- Yanked versions: mention in gaps

### Gap Categories

Standard gaps to check:

- [ ] Feature documentation incomplete
- [ ] Version history not available
- [ ] Dependency tree not fetched
- [ ] Breaking changes unknown
- [ ] Comparison data not available (for comparative queries)
- [ ] MSRV not specified
- [ ] License unclear

### Context Questions

When crate usage is unclear, ask:

| Situation | Question |
|-----------|----------|
| Multiple use cases | "Is this for async or sync usage?" |
| Feature selection | "Which features do you plan to enable?" |
| Version targeting | "What's your minimum supported Rust version?" |
| Comparison query | "What specific aspect do you want compared?" |

### Negotiation Response Template

```markdown
## Negotiation Response

### Findings
**Crate:** <name>
**Version:** <version>
**Description:** <description>

**Features:**
- `feature1`: description

**Dependencies:** [if relevant]
**Last Updated:** <date>

### Confidence
- **Level**: [HIGH|MEDIUM|LOW|UNCERTAIN]
- **Reason**: [e.g., "Exact package ID and version-specific docs agree"]

### Gaps Identified
- [ ] [Specific gap 1]
- [ ] [Specific gap 2]

### Context Needed
- Q1: [If ambiguous]

### Metadata
- **Source**: cargo metadata | exact docs.rs | repository | crates.io | discovery summary
- **Coverage**: [e.g., "90% - missing changelog"]
```

Use `rust-design-protocol` for the response structure when a real decision is being compared.
