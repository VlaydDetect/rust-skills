#!/usr/bin/env python3
"""Stage Huiali skill families and maintain their pinned provenance ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from collections import Counter
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
REPOSITORY = PLUGIN.parents[1]
SOURCE = REPOSITORY / "references" / "rust-skills_huiali"
LEDGER = PLUGIN / "provenance" / "huiali-coverage.json"
STATUSES = {"pending", "in_progress", "adapted", "merged", "duplicate", "excluded"}
BLOCK_STATUSES = {"pending", "retained", "corrected", "rejected"}
RUST_BLOCK = re.compile(r"^```rust[^\n]*\n(.*?)^```[ \t]*$", re.MULTILINE | re.DOTALL)


FAMILY_CONFIG = {
    "rust-pin": {
        "owner": "rust-pin",
        "supporting": ["rust-unsafe", "rust-concurrency", "rust-ownership"],
        "focus": "Address sensitivity, Pin/Unpin, structural projection, self-reference, Future polling, and the drop guarantee.",
        "correction": "Treat pinning as a library contract, not a synonym for heap allocation. Pin::new_unchecked and unsafe projection require a local proof covering movement, projection, replacement, and destruction.",
    },
    "rust-gpu": {
        "owner": "rust-gpu",
        "supporting": ["rust-ml", "rust-performance"],
        "focus": "Device capabilities, memory hierarchy, transfer cost, alignment, coalescing, batching, synchronization, and measurement.",
        "correction": "Do not choose wgpu, CUDA, or another backend universally. Resolve the target, device capabilities, dependency version, data layout, and measurement plan first.",
    },
    "rust-ebpf": {
        "owner": "rust-systems-networking",
        "supporting": ["rust-observability", "rust-unsafe", "rust-performance"],
        "focus": "Verifier constraints, bounded control flow, maps, XDP and probe attachment, no_std code, kernel/user ABI, and observability boundaries.",
        "correction": "Retain verifier and ABI reasoning, but verify every Aya API against the exact resolved release. Version-sensitive Aya examples from the source are rejected rather than presented as current code.",
    },
    "rust-dpdk": {
        "owner": "rust-systems-networking",
        "supporting": ["rust-unsafe", "rust-performance"],
        "focus": "Mempools, mbuf ownership, queues, burst processing, RSS, NUMA placement, affinity, and bounded packet-resource lifecycles.",
        "correction": "Keep the execution and ownership model binding-neutral. Never infer a Rust binding, NIC topology, queue count, huge-page layout, or core placement without project and hardware evidence.",
    },
    "rust-distributed": {
        "owner": "rust-distributed-systems",
        "supporting": ["rust-architecture", "rust-errors", "rust-concurrency"],
        "focus": "Consistency, idempotency, retry budgets, leases, versioned contracts, saga/outbox coordination, consensus, and two-phase commit models.",
        "correction": "Model partial failure before selecting a protocol. Do not implement Raft, consensus, or two-phase commit from scratch for production; use mature, verified components and state their failure assumptions.",
    },
    "rust-actor": {
        "owner": "rust-concurrency",
        "supporting": ["rust-architecture", "rust-errors"],
        "focus": "Actor ownership, bounded mailboxes, request-response, supervision, restart policy, lifecycle, and backpressure.",
        "correction": "The actor model is conditional, and Actix is not a default. Select actors only when isolated mutable state and message-driven failure boundaries fit the problem.",
    },
    "rust-async": {
        "owner": "rust-concurrency",
        "supporting": ["rust-ownership", "rust-errors"],
        "focus": "Future lifecycle, cancellation safety, structured tasks, backpressure, bounded streams, joins, selection, and blocking boundaries.",
        "correction": "Use the repository's resolved runtime and cancellation contract. Do not hold blocking or inappropriate synchronization guards across await, but do not ban standard mutexes or channels universally.",
    },
    "rust-async-pattern": {
        "owner": "rust-concurrency",
        "supporting": ["rust-architecture", "rust-ownership"],
        "focus": "Async architecture choices, arenas, actors, owned snapshots, task topology, cancellation, and lifetime containment.",
        "correction": "Prefer the smallest ownership shape that makes task lifetime explicit; do not introduce actors, arenas, boxed futures, or detached tasks merely to silence a borrow error.",
    },
    "rust-coroutine": {
        "owner": "rust-concurrency",
        "supporting": ["rust-pin", "rust-stable"],
        "focus": "Stackless and stackful models, explicit state machines, suspension, scheduling, pinning, cancellation, and resource cleanup.",
        "correction": "Old generators/generator_trait material is not current baseline. Nightly uses coroutines/coroutine_trait; prefer stable Future, streams, iterators, or an explicit state machine unless nightly is an explicit project constraint.",
    },
    "rust-concurrency": {
        "owner": "rust-concurrency",
        "supporting": ["rust-ownership", "rust-performance"],
        "focus": "Send/Sync, shared-state and message-passing choices, atomics, lock scope, thread/task ownership, cancellation, and shutdown.",
        "correction": "Choose synchronization from invariants and measurements. std::sync::Mutex, standard channels, parking_lot, and crossbeam are all conditional rather than universal defaults or bans.",
    },
    "rust-lifetime-complex": {
        "owner": "rust-ownership",
        "supporting": ["rust-traits", "rust-api-design"],
        "focus": "Lifetime diagnosis, variance, HRTBs, GATs, reborrowing, returned borrows, trait objects, and async lifetime boundaries.",
        "correction": "Start from who owns the data and how long the API must expose it. Add explicit lifetimes, HRTBs, or GATs only after the concrete relationship is identified.",
    },
    "rust-linear-type": {
        "owner": "rust-ownership",
        "supporting": ["rust-traits", "rust-errors"],
        "focus": "Affine resource semantics, exactly-once transitions, typestate, non-cloneable capabilities, RAII, and leak versus double-use analysis.",
        "correction": "Rust ownership is affine: values may be consumed at most once but may also be dropped unused. Do not claim the language provides general linear types or compile-time exactly-once use.",
    },
    "rust-resource": {
        "owner": "rust-ownership",
        "supporting": ["rust-errors", "rust-concurrency"],
        "focus": "RAII, smart-pointer selection, pools, guards, acquisition ordering, partial construction, cleanup, and cancellation-safe release.",
        "correction": "Make ownership and cleanup paths explicit, including partial failure and cancellation. Pools and shared ownership are optimizations or coordination tools, not defaults.",
    },
    "rust-mutability": {
        "owner": "rust-ownership",
        "supporting": ["rust-concurrency", "rust-api-design"],
        "focus": "Exclusive mutation, reborrowing, interior mutability, aliasing, lock/borrow scope, and observable API effects.",
        "correction": "Select Cell, RefCell, locks, or atomics from the sharing and failure contract. Interior mutability moves checks or synchronization; it does not remove aliasing obligations.",
    },
    "rust-ownership": {
        "owner": "rust-ownership",
        "supporting": ["rust-api-design", "rust-concurrency"],
        "focus": "Moves, borrows, reborrows, smart pointers, lifetime boundaries, clone decisions, and ownership-error diagnosis.",
        "correction": "Describe Rust ownership as affine and diagnose the intended owner before cloning, adding indirection, or widening a lifetime.",
    },
    "rust-macro": {
        "owner": "rust-macros",
        "supporting": ["rust-testing", "rust-api-design"],
        "focus": "macro_rules!, derive, attribute and function-like procedural macros, token handling, hygiene, diagnostics, expansion, and compile-time tests.",
        "correction": "Procedural macros have three official forms: function-like, derive, and attribute. Use absolute generated paths where appropriate, preserve spans for diagnostics, and test expansion and failure behavior on the supported toolchain.",
    },
    "rust-learner": {
        "owner": "rust-research",
        "supporting": ["rust-by-example", "rust-stable"],
        "focus": "Current-feature adoption, MSRV and Edition evidence, release-note research, feedback, and dependency-ordered practice.",
        "correction": "Date current claims and prefer official Rust and exact-version crate sources. Learning guidance does not authorize an MSRV, Edition, dependency, or lockfile upgrade.",
    },
    "rust-skill": {
        "owner": "rust-workflow",
        "supporting": [],
        "focus": "Problem-first classification, uncertainty reduction, owner selection, supporting constraints, and verification handoff.",
        "correction": "Route one primary profile and at most two supporting profiles per phase. Do not load the whole catalog or let overlapping profiles compete for the same decision.",
    },
    "rust-skill-index": {
        "owner": "rust-workflow",
        "supporting": [],
        "focus": "Precise symptom-to-profile lookup, negative routing, manual invocation, and escalation from mechanics to design or domain reasoning.",
        "correction": "The product routing index is authoritative. Huiali source names that were merged are reference families, not additional standalone skills.",
    },
    "rust-type-driven": {
        "owner": "rust-traits",
        "supporting": ["rust-api-design", "rust-stable"],
        "focus": "Newtypes, typestate, sealed states, capability types, trait bounds, associated types, and invalid-state elimination.",
        "correction": "Use type-level states when they materially remove invalid runtime states; avoid type-state explosion and preserve diagnostics, semver, and compile-time cost.",
    },
    "rust-const": {
        "owner": "rust-stable",
        "supporting": ["rust-traits", "rust-performance"],
        "focus": "Const evaluation, const fn, const generics, compile-time constraints, static data, and supported-toolchain limits.",
        "correction": "The real project toolchain and MSRV determine available const features. Do not turn a current-stable or nightly capability into an unconditional product baseline.",
    },
    "rust-zero-cost": {
        "owner": "rust-performance",
        "supporting": ["rust-traits", "rust-stable"],
        "focus": "Static versus dynamic dispatch, monomorphization, iterators, abstraction boundaries, code size, allocation, and measured runtime cost.",
        "correction": "Zero-cost means an abstraction should not impose avoidable runtime overhead relative to a suitable manual implementation; it does not promise zero compile time, code size, allocation, or all-purpose performance.",
    },
    "rust-error": {
        "owner": "rust-errors",
        "supporting": ["rust-api-design"],
        "focus": "Result propagation, error boundaries, context, recoverability, domain errors, panic policy, and source chains.",
        "correction": "Evaluate unwrap and expect at the boundary and against the invariant. Neither is universally preferred or forbidden; public and recoverable paths need deliberate error contracts.",
    },
    "rust-error-advanced": {
        "owner": "rust-errors",
        "supporting": ["rust-api-design", "rust-architecture"],
        "focus": "Layered error composition, stable public variants, context, aggregation, retry classification, and async/concurrent failures.",
        "correction": "Do not leak foreign dependency errors through stable public APIs, and do not erase domain distinctions merely to standardize on one error crate.",
    },
    "rust-ffi": {
        "owner": "rust-unsafe-ffi",
        "supporting": ["rust-unsafe", "rust-ownership"],
        "focus": "ABI layout, ownership transfer, allocator pairing, strings, callbacks, panic containment, handles, and foreign-thread behavior.",
        "correction": "Validate the actual foreign ABI and target. repr(C), raw pointers, and a safety comment are inputs to a proof, not a complete proof.",
    },
    "rust-unsafe": {
        "owner": "rust-unsafe",
        "supporting": ["rust-review", "rust-testing"],
        "focus": "Unsafe preconditions, aliasing, initialization, layout, provenance, Send/Sync, panic safety, and safe-abstraction review.",
        "correction": "Minimize unsafe surface and write a local proof for every operation. Unsafe is not a default performance technique, and comments must name the invariant evidence rather than restate the operation.",
    },
    "rust-testing": {
        "owner": "rust-testing",
        "supporting": ["rust-verify"],
        "focus": "Unit, integration, property, compile-fail, concurrency, fuzz and regression strategy with observable failure criteria.",
        "correction": "Choose test layers from risk and contract. Dependency-specific harnesses and exhaustive matrices are conditional; verification must distinguish compiled fixtures from illustrative fragments.",
    },
    "rust-observability": {
        "owner": "rust-observability",
        "supporting": ["rust-errors", "rust-performance"],
        "focus": "Structured events, spans, metrics, correlation, cardinality, redaction, sampling, and operational failure evidence.",
        "correction": "Follow the project's telemetry stack and privacy boundary. Do not add a logging or tracing dependency, high-cardinality label, or global subscriber without a demonstrated contract.",
    },
    "rust-performance": {
        "owner": "rust-performance",
        "supporting": ["debugging", "rust-observability"],
        "focus": "Baselines, profiling, allocation, cache behavior, batching, contention, latency distributions, throughput, and regression evidence.",
        "correction": "Profile the actual target and workload before optimizing. Dependency swaps and unsafe code require measured benefit and explicit new costs.",
    },
    "rust-ecosystem": {
        "owner": "rust-ecosystem",
        "supporting": ["rust-crate-discovery", "rust-research"],
        "focus": "Solution classes, ecosystem maturity, maintenance, portability, interoperability, and evidence-led crate selection.",
        "correction": "Treat crate names and popularity as time-sensitive leads. Resolve project constraints and verify current upstream status before recommending or adding a dependency.",
    },
    "rust-coding": {
        "owner": "rust-style-clippy",
        "supporting": ["rust-idioms", "rust-coding-rules"],
        "focus": "Readable Rust, naming, formatting, Clippy scope, documentation, control flow, API conventions, and reviewable diffs.",
        "correction": "Project policy and selected toolchain own formatting and lint levels. Avoid universal deny lists, mechanical rewrites, and preferences that conflict with the local contract.",
    },
    "rust-anti-pattern": {
        "owner": "rust-idioms",
        "supporting": ["rust-coding-rules", "rust-review"],
        "focus": "Symptom-to-cause diagnosis for cloning, allocation, stringly APIs, panic, locking, abstraction, collection, and async mistakes.",
        "correction": "Anti-patterns are contextual warning signs, not bans. Identify the violated invariant or measured cost before rewriting code.",
    },
    "rust-auth": {
        "owner": "rust-architecture",
        "supporting": ["rust-errors", "rust-api-design"],
        "focus": "Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.",
        "correction": "Model the application's threat and trust boundaries before selecting protocols or crates. Never invent credential, token, storage, or audit requirements.",
    },
    "rust-cache": {
        "owner": "rust-architecture",
        "supporting": ["rust-performance", "rust-concurrency"],
        "focus": "Cache ownership, key identity, freshness, invalidation, stampede control, capacity, failure behavior, and observability.",
        "correction": "Caching is a measured architectural trade-off. Define source of truth, staleness budget, invalidation, and failure mode before choosing a crate or distributed cache.",
    },
    "rust-database": {
        "owner": "rust-architecture",
        "supporting": ["rust-errors", "rust-performance"],
        "focus": "Persistence boundaries, transactions, consistency, schema evolution, query ownership, pooling, and error translation.",
        "correction": "Use the project's actual database and durability contract. Do not infer an ORM, pool, isolation level, retry policy, or migration mechanism.",
    },
    "rust-middleware": {
        "owner": "rust-architecture",
        "supporting": ["rust-concurrency", "rust-observability"],
        "focus": "Request pipelines, ordering, short-circuiting, context propagation, cancellation, retries, timeouts, and cross-cutting policy.",
        "correction": "Make middleware order and ownership explicit; do not hide domain behavior, duplicate retries, or hold request resources beyond their lifecycle.",
    },
    "rust-web": {
        "owner": "rust-architecture",
        "supporting": ["rust-api-design", "rust-errors"],
        "focus": "HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.",
        "correction": "Do not select or prescribe a web framework without project evidence. Keep transport DTOs, domain types, and infrastructure errors separated.",
    },
    "rust-embedded": {
        "owner": "rust-architecture",
        "supporting": ["rust-unsafe", "rust-concurrency"],
        "focus": "no_std constraints, HAL ownership, interrupts, bounded memory, timing, peripherals, power, and deterministic cleanup.",
        "correction": "Target MCU, HAL, allocator, interrupt model, and timing budget are required evidence. Do not infer heapless data structures, executors, or hardware topology.",
    },
    "rust-xacml": {
        "owner": "rust-architecture",
        "supporting": ["rust-api-design", "rust-errors"],
        "focus": "Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.",
        "correction": "Treat XACML as a domain constraint map, not a framework default. Confirm policy semantics, trust boundaries, and interoperability requirements before designing types.",
    },
}


FAMILY_ORDER = list(FAMILY_CONFIG)


SUPPORT_TARGETS = {
    "references/best-practices/api-design.md": "skills/rust-api-design/references/guide.md",
    "references/best-practices/best-practices.md": "skills/rust-idioms/references/guide.md",
    "references/best-practices/coding-standards.md": "skills/rust-style-clippy/references/huiali/rust-coding.md",
    "references/best-practices/error-handling.md": "skills/rust-errors/references/huiali/rust-error.md",
    "references/best-practices/performance.md": "skills/rust-performance/references/huiali/rust-performance.md",
    "references/best-practices/unsafe-rules.md": "skills/rust-unsafe/references/huiali/rust-unsafe.md",
    "references/commands/audit.md": "skills/rust-review/references/review-lenses.md",
    "references/commands/crate-info.md": "skills/rust-research/references/actionbook-commands.md",
    "references/commands/docs.md": "skills/rust-research/references/actionbook-commands.md",
    "references/commands/guideline.md": "skills/rust-coding-rules/references/routing.md",
    "references/commands/rust-features.md": "skills/rust-research/references/current-baseline.md",
    "references/commands/rust-review.md": "skills/rust-review/references/review-lenses.md",
    "references/commands/skill-index.md": "skills/rust-workflow/references/routing-index.md",
    "references/commands/unsafe-check.md": "skills/rust-unsafe/references/actionbook-checks/index.md",
    "references/core-concepts/concurrency.md": "skills/rust-concurrency/references/huiali/rust-concurrency.md",
    "references/core-concepts/lifetimes.md": "skills/rust-ownership/references/huiali/rust-lifetime-complex.md",
    "references/core-concepts/ownership.md": "skills/rust-ownership/references/huiali/rust-ownership.md",
    "references/core-concepts/traits.md": "skills/rust-traits/references/huiali/rust-type-driven.md",
    "references/ecosystem/async-runtimes.md": "skills/rust-concurrency/references/huiali/rust-async.md",
    "references/ecosystem/crates.md": "skills/rust-ecosystem/references/huiali/rust-ecosystem.md",
    "references/ecosystem/modern-crates.md": "skills/rust-ecosystem/references/huiali/rust-ecosystem.md",
    "references/ecosystem/testing.md": "skills/rust-testing/references/huiali/rust-testing.md",
    "references/GLOSSARY.md": "skills/rust-workflow/references/routing-index.md",
    "references/versions/rust-editions.md": "skills/rust-research/references/current-baseline.md",
}


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file()
        and ".git" not in path.relative_to(SOURCE).parts
        and "graphify-out" not in path.relative_to(SOURCE).parts
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_count(path: Path) -> int | None:
    try:
        return len(path.read_text(encoding="utf-8").splitlines())
    except UnicodeDecodeError:
        return None


def normalized_block(body: str) -> str:
    return body.replace("\r\n", "\n").rstrip()


def block_digest(body: str) -> str:
    return hashlib.sha256(normalized_block(body).encode()).hexdigest()


def family_from_source(source_path: str) -> str | None:
    parts = source_path.split("/")
    if len(parts) >= 3 and parts[0] == "skills":
        return parts[1]
    if len(parts) >= 4 and parts[:2] == [".codex", "skills"]:
        return parts[2]
    return None


def refresh_summary(data: dict) -> None:
    counts = Counter(entry["status"] for entry in data["entries"])
    block_counts = Counter(entry["status"] for entry in data["rust_blocks"])
    data["summary"] = {
        "source_files": len(data["entries"]),
        **{status: counts[status] for status in sorted(STATUSES)},
        "exact_duplicate_files": counts["duplicate"],
        "canonical_markdown_files": data["source_metrics"]["canonical_markdown_files"],
        "canonical_markdown_lines": data["source_metrics"]["canonical_markdown_lines"],
        "source_rust_blocks": data["source_metrics"]["source_rust_blocks"],
        "unique_rust_blocks": len(data["rust_blocks"]),
        "rust_block_aliases": data["source_metrics"]["rust_block_aliases"],
        "example_decisions": {status: block_counts[status] for status in sorted(BLOCK_STATUSES)},
    }


def save(data: dict) -> None:
    refresh_summary(data)
    LEDGER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def initialize(force: bool) -> None:
    if LEDGER.exists() and not force:
        raise SystemExit(f"ledger already exists: {LEDGER}")
    entries = []
    for path in source_files():
        relative = path.relative_to(SOURCE).as_posix()
        entry = {
            "source_path": relative,
            "source_sha256": digest(path),
            "source_lines": line_count(path),
            "source_bytes": path.stat().st_size,
            "status": "pending",
            "target_paths": [],
            "reason": "Awaiting sequential Huiali review.",
        }
        if relative.startswith(".codex/skills/"):
            canonical = SOURCE / relative.removeprefix(".codex/")
            if canonical.is_file() and digest(canonical) == entry["source_sha256"]:
                entry.update(
                    status="duplicate",
                    duplicate_of=canonical.relative_to(SOURCE).as_posix(),
                    reason="Exact SHA-256 duplicate of the canonical skills/** file; not copied twice.",
                )
        entries.append(entry)

    markdown = sorted((SOURCE / "skills").rglob("*.md"))
    blocks: dict[str, dict] = {}
    occurrences = 0
    for path in markdown:
        relative = path.relative_to(SOURCE).as_posix()
        for index, match in enumerate(RUST_BLOCK.finditer(path.read_text(encoding="utf-8")), start=1):
            occurrences += 1
            sha = block_digest(match.group(1))
            record = blocks.setdefault(
                sha,
                {
                    "source_sha256": sha,
                    "status": "pending",
                    "target_paths": [],
                    "classification": None,
                    "reason": "Awaiting sequential source-family classification.",
                    "occurrences": [],
                },
            )
            record["occurrences"].append(
                {"source_path": relative, "block_index": index, "family": family_from_source(relative)}
            )

    data = {
        "schema_version": 1,
        "source": {
            "name": "huiali/rust-skills",
            "relative_path": "references/rust-skills_huiali",
            "revision": "947bf77509d9b421035037e983da6662d08cbb8e",
            "commit_date": "2026-02-09T15:36:33+08:00",
            "license": "MIT",
            "copyright": "Copyright (c) 2026 Li Pianpian <huiali@hotmail.com>",
        },
        "statuses": sorted(STATUSES),
        "rust_block_statuses": sorted(BLOCK_STATUSES),
        "family_order": FAMILY_ORDER,
        "source_metrics": {
            "canonical_markdown_files": len(markdown),
            "canonical_markdown_lines": sum(line_count(path) or 0 for path in markdown),
            "source_rust_blocks": occurrences,
            "unique_rust_blocks": len(blocks),
            "rust_block_aliases": occurrences - len(blocks),
        },
        "summary": {},
        "entries": entries,
        "rust_blocks": [blocks[key] for key in sorted(blocks)],
    }
    save(data)


def load() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def by_source(data: dict) -> dict[str, dict]:
    return {entry["source_path"]: entry for entry in data["entries"]}


def by_block(data: dict) -> dict[str, dict]:
    return {entry["source_sha256"]: entry for entry in data["rust_blocks"]}


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end < 0:
        # A few Huiali files append the closing marker to the description line.
        # Preserve their Markdown body while treating the malformed header as source metadata.
        heading = text.find("\n# ", 4)
        if heading < 0:
            raise ValueError("unclosed source frontmatter")
        return text[heading + 1 :]
    return text[end + 4 :].lstrip("\r\n")


def strip_localized_reference(text: str) -> str:
    return re.sub(r"\n## Localized Reference\s*\n.*\Z", "\n", text, flags=re.DOTALL)


def apply_prose_corrections(family: str, text: str) -> str:
    replacements = {
        "rust-coding": {
            "| `std::sync::mpsc` | `crossbeam::channel` | - |": "| `std::sync::mpsc` | Keep or replace only when required semantics and measurements justify it | project-specific |",
            "| `std::sync::Mutex` | `parking_lot::Mutex` | - |": "| `std::sync::Mutex` | Keep or replace only when lock semantics and measurements justify it | project-specific |",
            "rust-version = \"1.85\"": "# rust-version = \"<project MSRV>\"",
            "pedantic = \"warn\"": "# Enable selected pedantic lints individually when the project benefits.",
            "| `clippy::expect_used` | Prefer expect |": "| `clippy::expect_used` | Review `expect` at invariant boundaries; it is not preferred universally |",
        },
        "rust-concurrency": {
            "| Lock-free structures | High contention | Complex, use crates (crossbeam) |": "| Lock-free structures | Proven contention bottleneck and suitable model | Complex; verify a project-approved crate and measure |",
        },
        "rust-ecosystem": {
            "| Scenario | Recommendation |": "| Scenario | Candidates to verify against the current project |",
            "| Work stealing | **crossbeam**, tokio |": "| Work stealing | Existing runtime or a currently maintained work-stealing implementation |",
            "| Channels | **tokio::sync**, crossbeam, flume |": "| Channels | Standard or resolved runtime/crate channel matching required semantics |",
        },
        "rust-pin": {
            "## Unpin Marker Trait": "## Unpin Marker Trait\n\n> Product correction: compiler-generated Futures are not uniformly `!Unpin`; determine the concrete type. Source references to Generators are historical—current nightly terminology is coroutines, while stable `Future`, streams, iterators, or explicit state machines remain preferred when nightly is unnecessary.",
            "  → async/await (Future trait)\n  → Self-referential struct\n  → Implementing custom Future\n  → Working with generators": "  → polling or implementing an address-sensitive Future\n  → self-referential or intrusive state\n  → an API explicitly requires Pin<P>\n  → current nightly coroutines only when the project intentionally uses them",
            "  → Stack-allocated temporaries": "  → ordinary values with no address-sensitive invariant",
        },
    }
    for old, new in replacements.get(family, {}).items():
        text = text.replace(old, new)
    return text


def target_for_family(family: str) -> str:
    owner = FAMILY_CONFIG[family]["owner"]
    return f"skills/{owner}/references/huiali/{family}.md"


def block_decision(family: str, body: str) -> tuple[str, str, str]:
    normalized = normalized_block(body)
    lowered = normalized.lower()
    if family == "rust-ebpf" and re.search(r"\baya(?:_bpf|_ebpf)?\b|aya::|aya_bpf::", lowered):
        return (
            "rejected",
            normalized,
            "Version-sensitive Aya API was rejected; keep verifier/no_std/map/ABI reasoning and research the exact resolved Aya release.",
        )
    if family == "rust-coroutine" and re.search(
        r"generator_trait|#!\[feature\(generators\)\]|std::ops::generator|generatorstate", lowered
    ):
        return (
            "rejected",
            normalized,
            "Obsolete generator feature/API example was rejected; use current nightly coroutines only when required, otherwise stable Future/stream/state-machine code.",
        )
    if family == "rust-pin" and "use futures::Future;" in normalized:
        return (
            "corrected",
            normalized.replace("use futures::Future;", "use std::future::Future;"),
            "Removed an unnecessary futures-crate import; the fragment uses std::future::Future and still requires the surrounding async operation.",
        )
    return (
        "retained",
        normalized,
        "Retained as a source fragment; project MSRV, target, dependencies, omitted context, and behavior still require verification.",
    )


def record_block(
    record: dict,
    status: str,
    target: str | None,
    reason: str,
) -> None:
    if target and target not in record["target_paths"]:
        record["target_paths"].append(target)
    if target:
        if record["status"] == "pending" or (record["status"] == "rejected" and status != "rejected"):
            record["status"] = status
            record["classification"] = "fragment"
            record["reason"] = reason
        elif record["status"] == "corrected" and status == "retained":
            record["status"] = "retained"
            record["reason"] = "Retained in at least one context; another occurrence received a local source correction."
    elif record["status"] == "pending":
        record["status"] = "rejected"
        record["classification"] = None
        record["reason"] = reason


def render_block(
    family: str,
    source_path: str,
    block_index: int,
    body: str,
    target: str,
    block_records: dict[str, dict],
) -> str:
    sha = block_digest(body)
    status, rendered, reason = block_decision(family, body)
    record = block_records[sha]
    if status == "rejected":
        record_block(record, status, None, reason)
        return f"> Rejected Huiali Rust block `{sha[:12]}`: {reason}"
    record_block(record, status, target, reason)
    source = f"{source_path}#rust-block-{block_index}"
    return (
        f"<!-- huiali-source: {source}; sha256={sha} -->\n"
        "<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->\n"
        f"```rust\n{rendered}\n```"
    )


def annotate_document(
    text: str,
    family: str,
    source_path: str,
    target: str,
    block_records: dict[str, dict],
) -> tuple[str, set[str]]:
    pieces: list[str] = []
    cursor = 0
    hashes: set[str] = set()
    for index, match in enumerate(RUST_BLOCK.finditer(text), start=1):
        pieces.append(text[cursor : match.start()])
        body = match.group(1)
        hashes.add(block_digest(body))
        pieces.append(render_block(family, source_path, index, body, target, block_records))
        cursor = match.end()
    pieces.append(text[cursor:])
    return "".join(pieces), hashes


def mark_family_sources(data: dict, family: str, status: str, target: str) -> None:
    entries = by_source(data)
    root = SOURCE / "skills" / family
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        relative = path.relative_to(SOURCE).as_posix()
        entry = entries[relative]
        if path.name == "SKILL.md":
            entry.update(status=status, target_paths=[target], reason="Canonical English workflow adapted with product routing, baseline corrections, and classified examples.")
        elif path.name in {"SKILL_EN.md", "SKILL_ZH.md"}:
            entry.update(status="merged", target_paths=[target], reason="Unique checklist, localized detail, and Rust examples merged into one English product reference; localized duplicate not shipped separately.")
    agent = root / "agents" / "openai.yaml"
    if agent.is_file():
        entry = entries[agent.relative_to(SOURCE).as_posix()]
        entry.update(status="excluded", target_paths=[], reason="Source UI metadata replaced by product-owned dual-host agents/openai.yaml metadata.")


def stage_family(family: str) -> None:
    if family not in FAMILY_CONFIG:
        raise SystemExit(f"unknown family: {family}")
    data = load()
    entries = by_source(data)
    target = target_for_family(family)
    canonical_path = SOURCE / "skills" / family / "SKILL.md"
    canonical_relative = canonical_path.relative_to(SOURCE).as_posix()
    canonical_entry = entries[canonical_relative]
    if canonical_entry["status"] in {"adapted", "merged"}:
        raise SystemExit(f"family already staged: {family}")
    for path in (SOURCE / "skills" / family).glob("SKILL*.md"):
        entries[path.relative_to(SOURCE).as_posix()].update(
            status="in_progress", target_paths=[target], reason=f"Sequential adaptation of {family} is in progress."
        )
    save(data)

    config = FAMILY_CONFIG[family]
    block_records = by_block(data)
    canonical = apply_prose_corrections(
        family,
        strip_localized_reference(strip_frontmatter(canonical_path.read_text(encoding="utf-8"))),
    )
    annotated, canonical_hashes = annotate_document(
        canonical, family, canonical_relative, target, block_records
    )
    additions: list[str] = []
    seen = set(canonical_hashes)
    for name in ("SKILL_EN.md", "SKILL_ZH.md"):
        path = canonical_path.parent / name
        if not path.is_file():
            continue
        relative = path.relative_to(SOURCE).as_posix()
        for index, match in enumerate(RUST_BLOCK.finditer(path.read_text(encoding="utf-8")), start=1):
            body = match.group(1)
            sha = block_digest(body)
            if sha in seen:
                continue
            seen.add(sha)
            additions.append(
                f"### `{name}` example {index}\n\n"
                + render_block(family, relative, index, body, target, block_records)
            )

    title = family.removeprefix("rust-").replace("-", " ").title()
    header = (
        f"# Huiali {title} Protocol\n\n"
        f"> Product adaptation of `{canonical_relative}` at revision "
        "`947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; "
        "product routing and current-project constraints override source-wide preferences.\n\n"
        "## Product routing and baseline\n\n"
        f"- Primary owner: `${config['owner']}`.\n"
        f"- Supporting profiles when needed: {', '.join(f'`${item}`' for item in config['supporting']) or 'none'}.\n"
        f"- Scope retained: {config['focus']}\n"
        f"- Baseline correction: {config['correction']}\n"
        "- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. "
        "Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.\n\n"
        "## Adapted source workflow\n\n"
    )
    appendix = ""
    if additions:
        appendix = (
            "\n\n## Additional unique source examples\n\n"
            "These code-only deltas appeared in the condensed English or localized source. They remain fragments, "
            "not dependency or hardware claims.\n\n"
            + "\n\n".join(additions)
        )
    output = (header + annotated.strip() + appendix).replace("\r\n", "\n")
    output = "\n".join(line.rstrip() for line in output.splitlines()) + "\n"
    target_path = PLUGIN / target
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(output, encoding="utf-8")

    mark_family_sources(data, family, "adapted", target)
    save(data)
    print(f"staged {family} -> {target} ({len(output.splitlines())} lines, {len(seen)} unique family blocks)")


def finalize_non_family_entries() -> None:
    data = load()
    entries = by_source(data)
    notices = ["THIRD_PARTY_NOTICES.md", "provenance/THIRD_PARTY_NOTICES.md", "provenance/huiali-coverage.json"]

    for relative, entry in entries.items():
        if entry["status"] != "pending":
            continue
        if relative in SUPPORT_TARGETS:
            entry.update(
                status="merged",
                target_paths=[SUPPORT_TARGETS[relative]],
                reason="Supporting source guidance was merged into the corresponding family reference or existing product owner; the Chinese/source duplicate is not shipped separately.",
            )
        elif relative == "LICENSE":
            entry.update(status="merged", target_paths=notices, reason="Pinned MIT license and copyright reproduced in product notices and coverage metadata.")
        elif relative in {"SKILL.md", "SKILL_zh.md", "SKILL_AUDIT_REPORT.md"}:
            entry.update(
                status="merged",
                target_paths=["skills/rust-workflow/references/routing-index.md", "provenance/huiali-coverage.json"],
                reason="Source-wide routing and audit inventory were normalized into the product routing index and exhaustive ledger.",
            )
        elif relative.startswith("skills/") and relative.endswith("/agents/openai.yaml"):
            entry.update(status="excluded", target_paths=[], reason="Source UI metadata replaced by product-owned dual-host agents/openai.yaml metadata.")
        elif relative.startswith("scripts/"):
            entry.update(status="excluded", target_paths=[], reason="Source wrapper script is replaced by existing Cargo commands and the product validator; no runtime dependency added.")
        elif relative.startswith((".claude/", ".cursor/")) or relative in {".codex/AGENTS.md", ".mcp.json"}:
            entry.update(status="excluded", target_paths=[], reason="Source host settings, MCP configuration, or editor policy is not part of the dual-host runtime product.")
        elif relative in {
            "README.md", "README_zh.md", "CLAUDE_CODE_GUIDE.md", "CLAUDE_CODE_GUIDE_zh.md",
            "USAGE_GLOBAL.md", "USAGE_GUIDE.md", "USAGE_SUBMODULE.md", "USER_GUIDE.md", "USER_GUIDE_zh.md",
        }:
            entry.update(status="excluded", target_paths=[], reason="Source installation and usage guide describes the upstream package rather than this product's stable dual-host interface.")
        else:
            raise SystemExit(f"no explicit finalization policy for {relative}")

    save(data)
    print("finalized non-family Huiali entries")


def write_indexes() -> None:
    owners: dict[str, list[tuple[str, str]]] = {}
    for family, config in FAMILY_CONFIG.items():
        owners.setdefault(config["owner"], []).append((family, "primary"))
        for supporting in config["supporting"]:
            owners.setdefault(supporting, []).append((family, "supporting"))

    for owner, families in sorted(owners.items()):
        owner_root = PLUGIN / "skills" / owner
        if not owner_root.is_dir():
            raise SystemExit(f"missing owner skill: {owner}")
        index_path = owner_root / "references" / "huiali-index.md"
        lines = [
            f"# Huiali references for `{owner}`",
            "",
            "Read only the family reference that matches the current decision. `primary` means this profile owns the decision; `supporting` means it contributes constraints without taking ownership.",
            "",
        ]
        seen: set[str] = set()
        for family, role in sorted(families):
            key = f"{family}:{role}"
            if key in seen:
                continue
            seen.add(key)
            target = PLUGIN / target_for_family(family)
            relative = os.path.relpath(target, index_path.parent).replace("\\", "/")
            lines.append(f"- [`{family}`]({relative}) — {role}; {FAMILY_CONFIG[family]['focus']}")
        lines += [
            "",
            "## Shared constraints",
            "",
            "- Project MSRV, Edition, target, Cargo metadata, and explicit user requirements override reference defaults.",
            "- Do not infer a dependency, runtime, framework, hardware topology, retry policy, or persistence contract.",
            "- Classify imported Rust snippets as fragments unless a product golden fixture actually compiles them.",
            "- Return ownership to the primary profile when supporting constraints have been stated.",
            "",
        ]
        index_path.write_text("\n".join(lines), encoding="utf-8")

        skill_path = owner_root / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        marker = "[Huiali integration index](references/huiali-index.md)"
        old_route = (
            "For Pin, GPU, systems networking, distributed systems, actor/async/coroutine, complex lifetime/resource, macro, learning, or domain-specific detail, "
            "read the [Huiali integration index](references/huiali-index.md) and load only the matching family reference."
        )
        new_route = (
            "For source-derived detail relevant to this profile, read the "
            "[Huiali integration index](references/huiali-index.md) and load only the matching family reference."
        )
        content = content.replace(old_route, new_route)
        if marker not in content:
            content = content.rstrip() + (
                "\n\n## Huiali protocols\n\n"
                f"{new_route}\n"
            )
        skill_path.write_text(content, encoding="utf-8")
    print(f"wrote Huiali indexes for {len(owners)} product owners")


def verify() -> None:
    data = load()
    assert data["schema_version"] == 1
    assert set(data["statuses"]) == STATUSES
    assert set(data["rust_block_statuses"]) == BLOCK_STATUSES
    assert data["source"] == {
        "name": "huiali/rust-skills",
        "relative_path": "references/rust-skills_huiali",
        "revision": "947bf77509d9b421035037e983da6662d08cbb8e",
        "commit_date": "2026-02-09T15:36:33+08:00",
        "license": "MIT",
        "copyright": "Copyright (c) 2026 Li Pianpian <huiali@hotmail.com>",
    }
    entries = data["entries"]
    assert len(entries) == 348
    assert len({entry["source_path"] for entry in entries}) == 348
    assert sum(entry["status"] == "duplicate" for entry in entries) == 150
    assert not [entry for entry in entries if entry["status"] in {"pending", "in_progress"}]
    for entry in entries:
        assert entry["status"] in STATUSES and entry["reason"]
        if entry["status"] in {"adapted", "merged"}:
            assert entry["target_paths"]
        if entry["status"] in {"duplicate", "excluded"}:
            assert not entry["target_paths"]
        for target in entry["target_paths"]:
            assert (PLUGIN / target).is_file(), f"missing target: {target}"

    actual = source_files()
    assert len(actual) == 348
    indexed = {entry["source_path"]: entry for entry in entries}
    assert {path.relative_to(SOURCE).as_posix() for path in actual} == set(indexed)
    for path in actual:
        entry = indexed[path.relative_to(SOURCE).as_posix()]
        assert digest(path) == entry["source_sha256"], f"source changed: {path}"
        assert path.stat().st_size == entry["source_bytes"]
        assert line_count(path) == entry["source_lines"]
        if entry["status"] == "duplicate":
            duplicate = SOURCE / entry["duplicate_of"]
            assert duplicate.is_file() and digest(duplicate) == entry["source_sha256"]

    metrics = data["source_metrics"]
    assert metrics == {
        "canonical_markdown_files": 111,
        "canonical_markdown_lines": 25175,
        "source_rust_blocks": 500,
        "unique_rust_blocks": 423,
        "rust_block_aliases": 77,
    }
    blocks = data["rust_blocks"]
    assert len(blocks) == 423
    assert sum(len(block["occurrences"]) for block in blocks) == 500
    assert not [block for block in blocks if block["status"] == "pending"]
    for block in blocks:
        assert block["status"] in BLOCK_STATUSES
        assert block["reason"]
        if block["status"] in {"retained", "corrected"}:
            assert block["classification"] == "fragment" and block["target_paths"]
        else:
            assert block["classification"] is None and not block["target_paths"]

    known_hashes = {block["source_sha256"] for block in blocks}
    for path in (PLUGIN / "skills").glob("*/references/huiali/*.md"):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if line.strip() != "```rust":
                continue
            assert index >= 2 and lines[index - 1].startswith("<!-- rust-example: "), f"unclassified block: {path}:{index + 1}"
            marker = lines[index - 2]
            match = re.fullmatch(r"<!-- huiali-source: .*; sha256=([0-9a-f]{64}) -->", marker)
            assert match and match.group(1) in known_hashes, f"missing Huiali source marker: {path}:{index + 1}"
    print("OK: 348 files, 150 duplicates, 500 Rust blocks, 423 unique block decisions")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    init = subparsers.add_parser("init")
    init.add_argument("--force", action="store_true")
    stage = subparsers.add_parser("stage-family")
    stage.add_argument("family", choices=FAMILY_ORDER)
    subparsers.add_parser("finalize")
    subparsers.add_parser("write-indexes")
    subparsers.add_parser("verify")
    args = parser.parse_args()
    if args.command == "init":
        initialize(args.force)
    elif args.command == "stage-family":
        stage_family(args.family)
    elif args.command == "finalize":
        finalize_non_family_entries()
    elif args.command == "write-indexes":
        write_indexes()
    else:
        verify()


if __name__ == "__main__":
    main()
