#!/usr/bin/env bash
set -u

has_rust=0
for marker in Cargo.toml rust-toolchain rust-toolchain.toml src/main.rs src/lib.rs; do
  if [ -e "$marker" ]; then
    has_rust=1
    break
  fi
done
if [ "$has_rust" -eq 0 ]; then
  for file in ./*.rs ./src/*.rs; do
    if [ -f "$file" ]; then
      has_rust=1
      break
    fi
  done
fi
[ "$has_rust" -eq 1 ] || exit 0

has_nix=0
for marker in flake.nix flake.lock shell.nix; do
  if [ -e "$marker" ]; then
    has_nix=1
    break
  fi
done
command -v nix >/dev/null 2>&1 && has_nix=1
if [ "$has_nix" -eq 0 ] && [ -r /etc/os-release ]; then
  while IFS= read -r line; do
    case "$line" in
      ID=nixos|ID=\"nixos\") has_nix=1; break ;;
    esac
  done < /etc/os-release
fi

setup_offer='Rust setup is available on request; no tools or files were changed.'
nix_offer='Nix/NixOS setup is available as a separate opt-in workflow; it is not included in standard Rust setup.'
if [ ! -f Cargo.toml ] || ! command -v cargo >/dev/null 2>&1; then
  printf '%s\n' "Rust project signals detected. ${setup_offer}"
  [ "$has_nix" -eq 0 ] || printf '%s\n' "$nix_offer"
  exit 0
fi

manifest="$(cargo locate-project --workspace --message-format plain 2>/dev/null)" || {
  printf '%s\n' "Rust project signals detected. ${setup_offer}"
  [ "$has_nix" -eq 0 ] || printf '%s\n' "$nix_offer"
  exit 0
}
if command -v rustc >/dev/null 2>&1; then
  rustc_version="$(rustc --version 2>/dev/null || printf 'rustc unavailable')"
else
  rustc_version='rustc unavailable'
fi
cargo_version="$(cargo --version 2>/dev/null || printf 'cargo unavailable')"

printf '%s\n' \
  "Rust workspace detected: ${manifest}" \
  "Toolchain: ${rustc_version}; ${cargo_version}" \
  'For coding, use rust-workflow and build a ProfileStack from the current change: one owner per decision unit, coding profiles for changed constructs, and helpers only after observed triggers. Keep background and future work deferred. Use rust-design-protocol only for cross-layer discovery and rust-research only for current external facts. Route read-only diff review to rust-review and evidence-only commands to rust-verify. All focused profiles remain manually invocable.' \
  "$setup_offer"
[ "$has_nix" -eq 0 ] || printf '%s\n' "$nix_offer"
