# Actionbook domain constraint maps

These are detailed Layer-3 inputs, not standalone framework selectors:

- [IoT](iot.md): classify gateway, edge, or device; then derive network,
  buffering, power, security, OTA, and telemetry constraints.
- [Embedded](embedded.md): derive `no_std`, allocation, interrupt, timing,
  peripheral ownership, and memory constraints from the actual target.
- [Cloud native](cloud-native.md): derive deployment, health, shutdown,
  configuration, state, scaling, and observability contracts from the runtime.

Route implementation details to `rust-concurrency`, `rust-performance`,
`rust-errors`, `rust-observability`, `rust-dependencies`, `rust-unsafe`, or
`rust-unsafe-ffi` as needed. Use `rust-research` before choosing crates or
copying version-sensitive examples.

