$rustMarkers = @('Cargo.toml', 'rust-toolchain', 'rust-toolchain.toml', 'src/main.rs', 'src/lib.rs')
$hasRust = ($rustMarkers | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1) -ne $null
if (-not $hasRust) {
    $hasRust = @(Get-ChildItem -LiteralPath . -Filter '*.rs' -File -ErrorAction SilentlyContinue).Count -gt 0
}
if (-not $hasRust -and (Test-Path -LiteralPath 'src')) {
    $hasRust = @(Get-ChildItem -LiteralPath 'src' -Filter '*.rs' -File -ErrorAction SilentlyContinue).Count -gt 0
}
if (-not $hasRust) {
    exit 0
}

$nixMarkers = @('flake.nix', 'flake.lock', 'shell.nix')
$hasNix = ($nixMarkers | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1) -ne $null
$hasNix = $hasNix -or [bool](Get-Command nix -ErrorAction SilentlyContinue)
if (-not $hasNix -and (Test-Path -LiteralPath '/etc/os-release')) {
    $hasNix = (Get-Content -LiteralPath '/etc/os-release' -ErrorAction SilentlyContinue) -match '^ID="?nixos"?$'
}

$setupOffer = 'Rust setup is available on request; no tools or files were changed.'
$nixOffer = 'Nix/NixOS setup is available as a separate opt-in workflow; it is not included in standard Rust setup.'
$cargo = Get-Command cargo -ErrorAction SilentlyContinue
if (-not $cargo -or -not (Test-Path -LiteralPath 'Cargo.toml')) {
    Write-Output "Rust project signals detected. $setupOffer"
    if ($hasNix) { Write-Output $nixOffer }
    exit 0
}

$manifest = & $cargo.Source locate-project --workspace --message-format plain 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Output "Rust project signals detected. $setupOffer"
    if ($hasNix) { Write-Output $nixOffer }
    exit 0
}

$rustcVersion = if (Get-Command rustc -ErrorAction SilentlyContinue) {
    & rustc --version 2>$null
} else {
    'rustc unavailable'
}
$cargoVersion = & $cargo.Source --version 2>$null

Write-Output "Rust workspace detected: $manifest"
Write-Output "Toolchain: $rustcVersion; $cargoVersion"
Write-Output 'For coding, use rust-workflow and build a ProfileStack from the current change: one owner per decision unit, coding profiles for changed constructs, and helpers only after observed triggers. Keep background and future work deferred. Use rust-design-protocol only for cross-layer discovery and rust-research only for current external facts. Route read-only diff review to rust-review and evidence-only commands to rust-verify. All focused profiles remain manually invocable.'
Write-Output $setupOffer
if ($hasNix) { Write-Output $nixOffer }
