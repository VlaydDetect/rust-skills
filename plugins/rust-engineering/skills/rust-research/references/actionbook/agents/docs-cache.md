# Evidence freshness record

Actionbook's persistent Claude documentation cache is not reproduced. Keep evidence in the current research result or an explicitly requested project-local crate dossier.

For every external fact record:

```json
{
  "url": "canonical source URL",
  "retrieved_at": "RFC 3339 timestamp",
  "subject_version": "toolchain or package version",
  "content_sha256": "hash when content is persisted",
  "confidence": "high | medium | low",
  "gaps": []
}
```

Historical release notes are versioned evidence. Mutable pages such as `/latest/`, registry summaries, main-branch docs, and news feeds must be treated as stale-prone. A user request containing “refresh” authorizes new research, not silent writes outside the project.
