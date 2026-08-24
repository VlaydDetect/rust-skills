# Rust Engineering

Rust Engineering — единый плагин для Codex, ChatGPT Desktop, Claude Code и Claude Desktop. Он поставляет 55 сфокусированных скиллов, адресуемый rulebook из 265 Rust-правил, быстрый SessionStart-контекст и воспроизводимый цикл реализации, review и проверки.

Продуктовый исходник находится в `plugins/rust-engineering/`. Плагин не требует сетевого доступа или дополнительных runtime-зависимостей.

## Как работает плагин

SessionStart сначала проверяет только локальные признаки проекта. В нерелевантном каталоге hook ничего не выводит. Для Rust-файлов без Cargo он один раз предлагает opt-in настройку toolchain; для Cargo workspace добавляет путь к manifest, версии `rustc`/`cargo` и предложение проектной настройки. Если обнаружены `flake.nix`, `shell.nix`, Nix в `PATH` или NixOS, предложение Nix/NixOS выводится отдельно.

Hook остаётся быстрым, offline и read-only: он не устанавливает инструменты, не создаёт файлы, не меняет lockfile и не запускает сборку, форматирование или тесты.

```text
запрос на изменение
  -> rust-workflow
     -> локальный discovery и TaskBrief
     -> decision units: по 1 owner на каждое решение
     -> coding-профили для изменяемых Rust-конструктов
     -> helper-профили только после наблюдаемого триггера
     -> RuleQuery и до 9 правил на decision unit
     -> основной агент вносит единое изменение
     -> rust-verify собирает минимально достаточные доказательства
     -> rust-review при запросе или повышенном риске
```

`rust-workflow` владеет изменяющими задачами и остаётся единственной точкой записи. `ProfileStack` строится из текущего среза изменения: общий план и будущие платформенные реализации остаются фоном и не активируют профиль. Каждый decision unit имеет одного owner; coding-профили привязаны к конкретным Rust-механикам, а helpers подключаются по фактическому триггеру. Потолки `3/6/10` для owners, coding и helpers являются аварийными ограничителями: превышение разбивает фазу, а не обрезает список.

`rust-coding-rules` остаётся отдельным overlay, а `rust-workflow`, review и verify образуют управляющий контур и не занимают профильные роли. Перед редактированием `coverage.gaps` должен быть пуст: решения, существенные конструкты и критерии приёмки обязаны иметь владельца и проверяемое покрытие.

Read-only задачи могут входить напрямую:

- `rust-review` проверяет ограниченный diff и возвращает findings-first verdict;
- `rust-verify` запускает существующие проверки и классифицирует evidence;
- `rust-architecture-review` проверяет структуру проекта целиком;
- `nix-review` проверяет Nix-изменения.

Все 55 скиллов доступны вручную: `$skill-name` в Codex и `/rust-engineering:skill-name` в Claude Code.

## Области работы

- Процесс: `rust-workflow`, `addressing-findings`, `codebase-onboarding`, `debugging`, `refactoring`, `rust-navigation`, `rust-design-protocol`, `rust-research`, `specs`.
- Язык и безопасность: `rust-stable`, `rust-stdlib`, `rust-by-example`, `rust-ownership`, `rust-traits`, `rust-errors`, `rust-idioms`, `rust-unsafe`, `rust-unsafe-ffi`, `rust-pin`.
- API и Cargo: `rust-api-design`, `rust-cargo-build`, `rust-workspace`, `rust-module-layout`, `rust-dependencies`, `rust-crate-discovery`, `rust-semver`, `rust-documentation`, `rust-style-clippy`, `rust-ecosystem`.
- Архитектура и runtime: `rust-architecture`, `rust-concurrency`, `rust-testing`, `rust-performance`, `rust-observability`, `rust-platforms`, `rust-serialization`, `rust-data`, `rust-database`, `rust-tauri`.
- Специализированный Rust: `rust-macros`, `rust-lombok-macros`, `rust-uniffi-building`, `rust-ml`, `rust-gpu`, `rust-systems-networking`, `rust-distributed-systems`.
- Nix: `nix-flakes`, `nix-dev-env`, `nix-packaging`, `nixos`, `nix-review`.

`rust-coding-rules` выбирает конкретные ID по коду и границе изменения. Для каждого активного decision unit отдельный набор содержит не более девяти правил; широкий аудит разбивается на последовательные пакеты. `rust-design-protocol` в изменяющем workflow только обнаруживает межслойные decision units и передаёт их настоящим owners, а `rust-research` подключается лишь для текущих внешних фактов.

## Настройка Rust-проекта

Настройка входит в `rust-workflow` и всегда начинается с read-only инвентаризации manifest, toolchain, CI, targets и уже доступных команд. До явного согласия пользователя плагин не запускает `rustup`, `cargo install`, package managers или генераторы и не создаёт файлы.

После согласия предлагаются только подтверждённые проектом действия. Опциональные инструменты вроде `cargo-nextest`, `cargo-llvm-cov` и `cargo-machete` не устанавливаются «на всякий случай». Nix development shell направляется в `nix-dev-env`, а NixOS-настройка — в `nixos` отдельным предложением и не входит в обычный Rust setup.

## Установка

Релиз-кандидат устанавливается из фиксированного Git-тега `v1.0.0-rc`. Установщики не устанавливают Codex, Claude, Node.js, uv или Rust.

### Через uv

```powershell
uv run --no-project https://raw.githubusercontent.com/VlaydDetect/rust-skills/v1.0.0-rc/installers/install.py --target all
```

### Через npx, npm или pnpm

```powershell
npx --yes github:VlaydDetect/rust-skills#v1.0.0-rc --target all
npm exec --yes --package=github:VlaydDetect/rust-skills#v1.0.0-rc -- rust-engineering-install --target all
pnpm dlx github:VlaydDetect/rust-skills#v1.0.0-rc --target all
```

Оба установщика поддерживают:

- `--target codex-cli|chatgpt-desktop|claude-code|claude-desktop|all`, по умолчанию `all`;
- `--scope user|project|local` для Claude, по умолчанию `user`;
- `--dry-run` для печати плана без действий;
- `--yes` для пропуска одного CLI-подтверждения.

Скрипты проверяют наличие host CLI, обновляют уже известный marketplace и останавливаются, если имя `rust-skills` занято другим source.

### Нативные CLI-команды

Codex:

```powershell
codex plugin marketplace add VlaydDetect/rust-skills --ref v1.0.0-rc
codex plugin add rust-engineering@rust-skills
```

Для обновления уже установленного плагина достаточно обновить marketplace; установщик проверяет поле `installed` и не вызывает повторный `plugin add`:

```powershell
codex plugin marketplace upgrade rust-skills
```

Если marketplace известен, но сам плагин ещё не установлен, выполните `codex plugin add rust-engineering@rust-skills`.

Claude Code:

```powershell
claude plugin marketplace add VlaydDetect/rust-skills@v1.0.0-rc --scope user
claude plugin install rust-engineering@rust-skills --scope user
```

Для другого уровня замените `user` на `project` или `local`. Повторная установка использует `claude plugin marketplace update rust-skills` и `claude plugin update rust-engineering@rust-skills --scope <scope>`.

### Desktop

Desktop-конфигурации и кэши намеренно не редактируются скриптами. Для ChatGPT Desktop откройте каталог плагинов, выберите `rust-engineering` из `rust-skills`, подтвердите установку и начните новую задачу. Для Claude Desktop откройте `/plugin` в локальной сессии, добавьте marketplace с тегом, установите плагин и выполните `/reload-plugins` либо перезапустите приложение. UI-подтверждение обязательно.

## Разработка и проверка

Из корня репозитория:

```powershell
uv run --no-project plugins/rust-engineering/scripts/validate.py --examples
node installers/install.mjs --target all --dry-run
claude plugin validate ./plugins/rust-engineering
git diff --check
```

Внутренний validator проверяет 55 скиллов и ссылки, предельную глубину `references`, 265 rule ID/alias, 47 unsafe/FFI rules, 341 eval-сценарий схемы 9, структуру и лимиты `ProfileStack`, manifests и marketplaces, общий installer config, parity Python/Node dry-run, поведение повторной установки и конфликта source, read-only hooks и fixtures. `claude plugin validate` выполняется только при наличии Claude CLI.

## Лицензия

Проект распространяется по [MIT License](plugins/rust-engineering/LICENSE). Канонические атрибуции и тексты сторонних лицензий находятся в [THIRD_PARTY_NOTICES.md](plugins/rust-engineering/THIRD_PARTY_NOTICES.md).

## Источники

- [gurinderu/craft](https://github.com/gurinderu/craft), revision `d9caf7faf36b565a59534c581fdc27516e87600a`.
- [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills), revision `25e44452df00055ca246ec806425d99028eaae19`.
- [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills), revision `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9`.
- [actionbook/rust-skills](https://github.com/actionbook/rust-skills), revision `fa60f7931223646fb71c4586b4a6c8545016076a`.
- [huiali/rust-skills](https://github.com/huiali/rust-skills), revision `947bf77509d9b421035037e983da6662d08cbb8e`.
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills), revision `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`.
- [laurigates/claude-plugins](https://github.com/laurigates/claude-plugins), revision `a1e72ed186b97555256d8c058ff291c182332df7`.
