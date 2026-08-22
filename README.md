# Rust Engineering Plugin

Dual-target плагин для Codex и Claude Code, который автоматически маршрутизирует задачи по Rust через один workflow и 40 профильных инженерных навыков. Продуктовый исходник находится в `plugins/rust-engineering/`; каталоги `references/`, `graphify-out/` и `gpt_report.md` служат сравнительной и навигационной базой, но не нужны плагину во время работы.

## Как работает маршрутизация

SessionStart hook выполняет только три дешёвых read-only действия: ищет Cargo workspace, читает версии `rustc` и `cargo`, затем добавляет рекомендацию маршрутизации в контекст хоста. Hook работает offline, не форматирует файлы, не меняет lockfile, не устанавливает инструменты и не запускает сборку или тесты.

Для задачи с изменением репозитория автоматической точкой входа служит `rust-workflow`:

```text
запрос на изменение
  -> rust-workflow
     -> discovery + TaskBrief
     -> 1 primary profile + максимум 2 supporting profiles
     -> изменение выполняет только главный агент
     -> rust-verify: минимальная матрица доказательств
     -> rust-review: независимый findings-first review при необходимости
```

Если задача требует больше трёх профилей, workflow делит её на фазы и выполняет новую маршрутизацию для каждой фазы. Профили не конкурируют за решение: primary владеет решением, supporting только добавляют ограничения. Все 43 навыка можно вызвать вручную; для focused-вопроса профиль не обязан проходить через общий workflow.

Ручной синтаксис: `$profile-name` в Codex и `/rust-engineering:profile-name` в Claude Code. Внутренние hand-off ссылки используют host-neutral имена профилей.

Read-only запросы имеют отдельные точки входа:

- `rust-review` — review ограниченного diff или PR, доказательные findings и verdict без правок;
- `rust-verify` — выполнение существующих проверок и классификация evidence без правок;
- `rust-architecture-review` — аудит структуры всего проекта;
- `nix-review` — Nix-specific review.

## Каталог навыков

### Точки входа

`rust-workflow`, `rust-review`, `rust-verify`.

### Инженерный процесс

`addressing-findings`, `codebase-onboarding`, `debugging`, `refactoring`, `rust-navigation`, `specs`.

### Язык Rust и безопасность

`rust-stable`, `rust-stdlib`, `rust-by-example`, `rust-ownership`, `rust-traits`, `rust-errors`, `rust-idioms`, `rust-unsafe`.

### API, Cargo и структура проекта

`rust-api-design`, `rust-cargo-build`, `rust-workspace`, `rust-module-layout`, `rust-dependencies`, `rust-crate-discovery`, `rust-semver`, `rust-documentation`, `rust-style-clippy`, `rust-ecosystem`.

### Архитектура

`rust-architecture`, `rust-architecture-review`.

### Runtime, interop и специализированные системы

`rust-concurrency`, `rust-testing`, `rust-performance`, `rust-observability`, `rust-unsafe-ffi`, `rust-macros`, `rust-lombok-macros`, `rust-uniffi-building`, `rust-ml`.

### Nix

`nix-flakes`, `nix-dev-env`, `nix-packaging`, `nixos`, `nix-review`.

Точные границы владения и конфликтные случаи собраны в `skills/rust-workflow/references/routing-index.md`. Например:

- `rust-testing` проектирует и пишет тесты, а `rust-verify` только запускает evidence;
- `rust-unsafe` доказывает внутренние unsafe-инварианты, `rust-unsafe-ffi` владеет ABI и foreign lifecycle, `rust-uniffi-building` — UniFFI workflow;
- `rust-crate-discovery` оценивает crate до принятия, `rust-dependencies` управляет уже принятой dependency;
- `rust-workspace` владеет границами crates, `rust-module-layout` — структурой внутри crate;
- `rust-review` проверяет diff, `rust-architecture-review` — проект целиком, `nix-review` — Nix-изменения.

## Глубина содержимого

Каждый профиль содержит:

- уникальный `SKILL.md` с триггерами, процессом, правилами решений и hand-off границами;
- подробный `references/guide.md` либо специализированный reference entrypoint;
- metadata `agents/openai.yaml` для ручного вызова в Codex;
- для 21 code-oriented профиля — оригинальный dependency-free golden example, который компилируется offline.

`provenance/source-coverage.json` фиксирует все 61 исходный skill и 385 supporting files из двух сравнительных корпусов. В продукт адаптированы 46 исходных skills и сведены к 41 владельцу знаний; ещё два навыка — `rust-workflow` и `rust-verify`. Пятнадцать вертикальных domain skills исключены явно с причиной, а не потеряны молча.

Материал реорганизован по владельцам решений и progressive disclosure. Исходные файлы не копируются wholesale и не требуются runtime-плагину.

## Agents и права на изменения

Плагин поставляет три общие read-only роли Claude Code: `rust-scout`, `rust-reviewer`, `rust-verifier`. В Codex тот же контракт может выполняться native subagents. Делегирование необязательно и применяется только к независимым вопросам, которые реально уменьшают неопределённость.

Главный агент остаётся единственным writer, принимает cross-profile решения, интегрирует результат и отвечает за final diff. Для post-fix re-review предпочтителен свежий reviewer context.

## Структура продукта

- `.codex-plugin/plugin.json` — Codex manifest;
- `.claude-plugin/plugin.json` — Claude Code manifest;
- `hooks/hooks.json` и `hooks/claude.json` — раздельные host schema;
- `scripts/session-context.*` — быстрый общий SessionStart detector;
- `skills/` — 43 host-neutral навыка и их references/examples;
- `agents/` — три read-only Claude agents;
- `evals/evals.json` — 106 routing cases schema v2: 43 manual, 43 automatic, 8 contrast, 12 negative;
- `provenance/source-coverage.json` — проверяемая карта исходного корпуса;
- `scripts/validate.py` — стандартно-библиотечный валидатор продукта.

## Проверка

Из корня репозитория:

```powershell
python plugins/rust-engineering/scripts/validate.py --examples
claude plugin validate ./plugins/rust-engineering
```

Первая команда проверяет оба manifest, все 43 skills и `openai.yaml`, Markdown links, hooks, три agent-контракта, provenance, 106 routing cases и компилирует 21 golden example offline. Без `--examples` выполняется только быстрая статическая проверка.

Дополнительно skill и Codex manifest можно прогнать штатными валидаторами `skill-creator` и `plugin-creator`. Существующий Graphify-граф помогает искать связи в исходных корпусах, но не является runtime-зависимостью или обязательным build gate; вывод графа всегда подтверждается по текущим файлам.
