if (-not (Get-Command cargo -ErrorAction SilentlyContinue)) {
    exit 0
}

$manifest = & cargo locate-project --workspace --message-format plain 2>$null
if ($LASTEXITCODE -ne 0) {
    exit 0
}

$rustcVersion = if (Get-Command rustc -ErrorAction SilentlyContinue) {
    & rustc --version 2>$null
} else {
    'rustc unavailable'
}
$cargoVersion = & cargo --version 2>$null

Write-Output "Rust workspace detected: $manifest"
Write-Output "Toolchain: $rustcVersion; $cargoVersion"
Write-Output 'For coding, use rust-workflow and let it select one primary plus at most two supporting profiles. Use rust-design-protocol only for cross-layer decisions and rust-research only for dated external facts. Route read-only diff review to rust-review and evidence-only commands to rust-verify. All focused profiles remain manually invocable.'
