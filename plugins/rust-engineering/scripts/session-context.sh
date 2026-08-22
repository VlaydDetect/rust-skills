#!/usr/bin/env bash
set -u

command -v cargo >/dev/null 2>&1 || exit 0
manifest="$(cargo locate-project --workspace --message-format plain 2>/dev/null)" || exit 0
if command -v rustc >/dev/null 2>&1; then
  rustc_version="$(rustc --version 2>/dev/null || printf 'rustc unavailable')"
else
  rustc_version='rustc unavailable'
fi
cargo_version="$(cargo --version 2>/dev/null || printf 'cargo unavailable')"

printf '%s\n' \
  "Rust workspace detected: ${manifest}" \
  "Toolchain: ${rustc_version}; ${cargo_version}" \
  'For coding, use the rust-workflow profile and let it select one primary plus at most two supporting profiles from its routing index. Route read-only diff review to rust-review and evidence-only commands to rust-verify. All focused profiles remain manually invocable.'
