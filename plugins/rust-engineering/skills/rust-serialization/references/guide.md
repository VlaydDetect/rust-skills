# Rust Binary Serialization Field Guide

Research baseline: **2026-08-23**. Use `rust-research` to recheck current crate versions, maintenance state, generator behavior, validation APIs, and format guarantees before adoption or a compatibility change. The check for this guide found that bincode 3.0.0 is an intentional compile-error deprecation release and upstream development has ceased; 2.0.1 is the last functional release.

## Define the Contract Before the Crate

Record the producer and every consumer, whether bytes are trusted, compatibility lifetime, language set, `no_std` requirement, maximum encoded and decoded sizes, streaming and random-access needs, acceptable copies, and whether bytes must be canonical. Decide separately how records are framed, versioned, compressed, encrypted, authenticated, and checksummed. A serializer alone rarely supplies all of those layers.

Use explicit envelope metadata when the payload can outlive one deployment: magic, format or schema version, declared length, and integrity policy. Validate envelope limits before allocating or invoking decompression. Keep semantic validation after structural decoding; a well-formed message can still contain an invalid path, identifier, range, or state transition.

## Selection Matrix

| Requirement | Candidate | Main caveat |
|---|---|---|
| Existing compact Rust-to-Rust contract | [`bincode` 2.0.1](https://docs.rs/bincode/2.0.1/bincode/) | Unmaintained; pin exactly and plan migration rather than adopting by default |
| New compact or embedded/`no_std` message | [`postcard`](https://docs.rs/postcard/latest/postcard/) or current crate discovery | Still needs framing and an evolution policy |
| Schema-first, multiple languages | Protobuf with [`prost`](https://docs.rs/prost/latest/prost/) | Deterministic output is not canonical output |
| Parse or write an existing binary layout | [`binrw`](https://docs.rs/binrw/latest/binrw/) | Counts, offsets, seeks, and alignment are attacker-controlled inputs |
| Archived or mmap-backed access | [`rkyv`](https://rkyv.org/) | Validation, alignment, endian, pointer width, and backing lifetime matter |
| Canonical bytes for hashing or signing | [Borsh](https://docs.rs/borsh/latest/borsh/) | Canonicality does not replace domain separation or signature policy |
| Self-describing interchange | CBOR via `ciborium`, or MessagePack via `rmp-serde` | Profiles differ; canonical CBOR requires explicit rules |
| Schema-first random access | FlatBuffers or Cap’n Proto | Generated schema and access model affect evolution and validation |

Treat this as a shortlist, not a scorecard. Compare resolved versions, maintenance, target support, security history, generated-code workflow, and the repository’s existing ecosystem.

## Format-Specific Rules

### bincode 2.0.1

Do not resolve `bincode = "*"` or `latest`: 3.0.0 intentionally does not provide a working codec. For an already accepted v2 contract, pin 2.0.1 and the exact configuration: standard or legacy profile, endian, integer encoding, size limit, and whether trailing bytes are accepted. Prefer its native `Encode` and `Decode` model unless Serde interoperability is required and its documented limitations are accepted. Never infer schema evolution from successful round trips; enum variants, field order, collection shape, and configuration changes can alter the bytes. Put a versioned DTO between durable bytes and mutable domain types, keep golden bytes, and document a migration candidate. New projects must run `rust-crate-discovery` rather than treating an unmaintained codec as the default.

### Protobuf with prost

Keep `.proto` files as the schema authority. Never reuse a removed field number or name; reserve both. Choose scalar and message presence deliberately, preserve compatibility across old and new readers, and frame messages when carried over a byte stream. The official encoding guide permits multiple valid byte encodings for the same message, so [deterministic serialization is not canonical serialization](https://protobuf.dev/programming-guides/serialization-not-canonical/). Do not hash or sign raw Protobuf output as though it were unique. Verify unknown-field preservation in the exact Rust generator and conversion path instead of assuming every runtime retains it.

### binrw

Use `binrw` when the layout already exists or offsets and conditional fields are the actual format. Validate magic, version, count, size, and offset before allocation or seek. Use checked add and multiply, prove a region stays inside the containing file, cap recursion and collection counts, and treat relative bases explicitly. Test truncated input at every boundary, malformed alignment, overlapping sections, integer overflow, and both seekable and unseekable sources. If a parser requires `Read + Seek`, copy into a bounded cursor or use an appropriate wrapper rather than silently assuming a network stream can seek.

### rkyv

An archive is not ordinary portable serialization by default. Endian, alignment, pointer-width profile, archived type shape, and feature configuration participate in the durable contract. For potentially malicious bytes, use the safe checked-access path and the matching validation support before constructing an archived reference. Never create an aligned reference into arbitrary network or file bytes. If an archive is mmap-backed, the archived view cannot outlive the mapping, and slices can retain the mapping even when the logical record is small. Keep mutation or deserialization separate unless in-place archived mutation is explicitly designed and validated.

### Other formats

Use `postcard` for constrained targets only after checking its supported data model and evolution envelope. Use Borsh when its deterministic, canonical specification matches the domain, while still adding domain separation and versioning for signed material. For CBOR, select a canonical profile if byte uniqueness matters. MessagePack is self-describing but does not make application semantics self-validating. FlatBuffers and Cap’n Proto reduce some access copies, but generated schemas, alignment, verification, and buffer lifetime remain real costs.

## Limits, Framing, and Trust

Apply limits before `Vec::with_capacity`, seek, recursion, string conversion, decompression, or nested decoding. Bound total input, decoded allocation, element count, nesting depth, individual blob length, and processing time where adversaries can supply input. Use checked arithmetic and reject lengths not representable by the target index type. A length prefix must be authenticated or bounded before use.

Define trailing-byte policy. For framed messages, require the decoder to consume exactly the frame. For concatenated records, return consumed length and advance under a total budget. Separate EOF from truncation, unsupported version, integrity failure, structural decode failure, and semantic validation so recovery and telemetry remain correct.

## Evolution and Evidence

Keep compatibility fixtures in source control:

- golden bytes for each supported version and configuration;
- same-version round trips plus semantic equality checks;
- old writer to new reader, and new writer to old reader where promised;
- removed, optional, unknown, defaulted, and reordered fields;
- malformed lengths, offsets, tags, nesting, truncation, and trailing bytes;
- fuzz or property tests with strict allocation and time budgets.

Golden bytes catch unplanned wire changes that round trips miss because encoder and decoder can change together. Migration tests should start from real historical artifacts, not regenerated structures. When signing or hashing, include protocol name, version, and context in the signed domain, and verify canonicalization before signature verification.

## Primary Sources

- [bincode 2.0.1 documentation](https://docs.rs/bincode/2.0.1/bincode/), [bincode 3.0.0 deprecation release](https://docs.rs/crate/bincode/3.0.0), and [postcard documentation](https://docs.rs/postcard/latest/postcard/)
- [Protobuf encoding guide](https://protobuf.dev/programming-guides/encoding/) and [non-canonical serialization note](https://protobuf.dev/programming-guides/serialization-not-canonical/)
- [binrw documentation](https://docs.rs/binrw/latest/binrw/) and [rkyv validation](https://rkyv.org/validation.html)
- [Borsh crate documentation and source](https://docs.rs/borsh/latest/borsh/) and [`prost` documentation](https://docs.rs/prost/latest/prost/)
