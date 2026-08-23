---
name: rust-serialization
description: Design and review Rust binary serialization contracts, format selection, schema evolution, canonical bytes, framing, validation, and decode limits. Use when the byte representation itself is the primary concern, not a transport or database transaction.
---

# Rust Binary Serialization

Own the byte contract before selecting a crate. Make trust, compatibility, resource limits, framing, and canonicality explicit so an implementation cannot accidentally turn an in-memory layout into a durable protocol.

## Use This Skill When

- A Rust system writes or reads a binary file, message, archive, model asset, or cross-language payload.
- Work compares `bincode`, Protobuf, `binrw`, `rkyv`, Borsh, `postcard`, CBOR, MessagePack, FlatBuffers, or Cap’n Proto.
- Schema evolution, deterministic or canonical bytes, zero-copy access, malformed input, or decode allocation limits control correctness.

## Workflow

1. Define who produces and consumes the bytes, input trust, lifetime, language set, compatibility window, size limits, and random-access needs.
2. Decide whether the contract is schema-first, Serde-shaped, an existing binary layout, or an archived in-memory representation.
3. Specify framing, version negotiation, endian and integer encoding, canonicality, validation, and unknown-field behavior independently of the crate.
4. Set limits before allocation, recursion, decompression, or seek; use checked arithmetic for counts, offsets, and lengths.
5. Build golden bytes, current round trips, old-to-new migration fixtures, malformed-input tests, and fuzz or property scenarios.
6. Record the exact crate versions and configuration that participate in the wire contract.

## Decision Rules

- `bincode` 2.0.1 is the last functional release and upstream is unmaintained; retain it only for an accepted pinned contract, not as a default new dependency.
- Protobuf deterministic output is not canonical output; field ordering and unknown-field retention need implementation-specific verification.
- Zero-copy is conditional on validation, alignment, endian, pointer-width, backing-buffer lifetime, and access patterns.
- Serialization does not supply message framing, compression, encryption, authentication, or checksums unless the chosen envelope explicitly does so.
- Never deserialize untrusted lengths into unbounded allocation or trust offsets before bounds and overflow checks.
- Canonical hashing or signing requires a format and profile that explicitly define one byte representation.

## Boundaries and Hand-offs

- `rust-api-design` owns public Rust types; this profile owns their byte representation and compatibility.
- `rust-distributed-systems` owns delivery and transport semantics after the message contract is defined.
- `rust-database` owns transactions and migrations; `rust-unsafe-ffi` owns foreign layout and pointer safety.
- Use `rust-research` for current format and generator behavior before a consequential adoption.

## Detailed Reference

Read [Rust binary serialization field guide](references/guide.md) before choosing a format or changing an existing byte contract.
