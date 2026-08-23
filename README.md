# Rust Engineering Plugin

Dual-target плагин для Codex и Claude Code с 50 навыками: общий workflow, read-only review/verify, 46 профильных инженерных навыков и адресуемый Rust rulebook overlay. Продуктовый исходник находится в `plugins/rust-engineering/`; каталоги `references/`, `graphify-out/` и `gpt_report.md` служат сравнительной и навигационной базой, но не нужны плагину во время работы.

## Как работает маршрутизация

SessionStart hook выполняет только три дешёвых read-only действия: ищет Cargo workspace, читает версии `rustc` и `cargo`, затем добавляет рекомендацию маршрутизации в контекст хоста. Hook работает offline, не форматирует файлы, не меняет lockfile, не устанавливает инструменты и не запускает сборку или тесты.

Для задачи с изменением репозитория автоматической точкой входа служит `rust-workflow`:

```text
запрос на изменение
  -> rust-workflow
     -> discovery + TaskBrief
     -> при необходимости: L1/L2/L3 trace через rust-design-protocol
     -> при необходимости: датированные upstream facts через rust-research
     -> 1 primary profile + максимум 2 supporting profiles
     -> RuleQuery + до 8 правил из rust-coding-rules
     -> изменение выполняет только главный агент
     -> rust-verify: минимальная матрица доказательств
     -> rust-review: независимый findings-first review при необходимости
```

Если задача требует больше трёх профилей, workflow делит её на фазы и выполняет новую маршрутизацию для каждой фазы. Профили не конкурируют за решение: primary владеет решением, supporting только добавляют ограничения. Rulebook не занимает профильный слот и не переопределяет user/project contract, MSRV, target или owner-профиль. Все 50 навыков можно вызвать вручную; для focused-вопроса профиль не обязан проходить через общий workflow.

Ручной синтаксис: `$profile-name` в Codex и `/rust-engineering:profile-name` в Claude Code. Внутренние hand-off ссылки используют host-neutral имена профилей.

Read-only запросы имеют отдельные точки входа:

- `rust-review` — review ограниченного diff или PR, доказательные findings и verdict без правок;
- `rust-verify` — выполнение существующих проверок и классификация evidence без правок;
- `rust-architecture-review` — аудит структуры всего проекта;
- `nix-review` — Nix-specific review.

## Каталог навыков

### Точки входа

`rust-workflow`, `rust-review`, `rust-verify`.

### Справочный overlay

`rust-coding-rules` — 265 адресуемых ID в 26 category indexes. Обычная фаза выбирает не более восьми правил; широкий аудит идёт пакетами. Прямой вызов: `$rust-coding-rules <id|prefix|task>` в Codex и `/rust-engineering:rust-coding-rules ...` в Claude Code.

### Инженерный процесс

`addressing-findings`, `codebase-onboarding`, `debugging`, `refactoring`, `rust-navigation`, `rust-design-protocol`, `rust-research`, `specs`.

### Язык Rust и безопасность

`rust-stable`, `rust-stdlib`, `rust-by-example`, `rust-ownership`, `rust-traits`, `rust-errors`, `rust-idioms`, `rust-unsafe`, `rust-pin`.

### API, Cargo и структура проекта

`rust-api-design`, `rust-cargo-build`, `rust-workspace`, `rust-module-layout`, `rust-dependencies`, `rust-crate-discovery`, `rust-semver`, `rust-documentation`, `rust-style-clippy`, `rust-ecosystem`.

### Архитектура

`rust-architecture`, `rust-architecture-review`.

### Runtime, interop и специализированные системы

`rust-concurrency`, `rust-testing`, `rust-performance`, `rust-observability`, `rust-unsafe-ffi`, `rust-macros`, `rust-lombok-macros`, `rust-uniffi-building`, `rust-ml`, `rust-gpu`, `rust-systems-networking`, `rust-distributed-systems`.

### Nix

`nix-flakes`, `nix-dev-env`, `nix-packaging`, `nixos`, `nix-review`.

Точные границы владения и конфликтные случаи собраны в `skills/rust-workflow/references/routing-index.md`. Например:

- `rust-testing` проектирует и пишет тесты, а `rust-verify` только запускает evidence;
- `rust-unsafe` доказывает внутренние unsafe-инварианты, `rust-unsafe-ffi` владеет ABI и foreign lifecycle, `rust-uniffi-building` — UniFFI workflow;
- `rust-crate-discovery` оценивает crate до принятия, `rust-dependencies` управляет уже принятой dependency;
- `rust-workspace` владеет границами crates, `rust-module-layout` — структурой внутри crate;
- `rust-review` проверяет diff, `rust-architecture-review` — проект целиком, `nix-review` — Nix-изменения.
- `rust-pin` владеет pinning contract, `rust-unsafe` — доказательством unsafe projection, `rust-concurrency` — lifecycle `Future`;
- `rust-gpu` владеет device/memory execution, `rust-ml` — model semantics, `rust-performance` — измерением bottleneck;
- `rust-systems-networking` владеет eBPF/DPDK execution environment, а `rust-observability`, `rust-unsafe` и `rust-performance` добавляют профильные ограничения;
- `rust-distributed-systems` владеет cross-node failure/consistency, `rust-architecture` — границами системы, `rust-concurrency` — внутрипроцессным выполнением.

## Глубина содержимого

Каждый профиль содержит:

- уникальный `SKILL.md` с триггерами, процессом, правилами решений и hand-off границами;
- подробный `references/guide.md` либо специализированный reference entrypoint;
- metadata `agents/openai.yaml` для ручного вызова в Codex;
- для 25 code-oriented профилей — оригинальный dependency-free golden example, который компилируется offline.

`provenance/source-coverage.json` фиксирует все 61 исходный skill и 385 supporting files из craft/full-stack корпусов. В продукт адаптированы 46 исходных skills и сведены к 41 владельцу знаний; `rust-workflow` и `rust-verify` дополняют этот каталог. Пятнадцать вертикальных domain skills исключены явно с причиной, а не потеряны молча.

Leonardomso-корпус перенесён без сжатия: `provenance/rule-coverage.json` фиксирует все 265 исходных ID, source/target SHA-256, owners, aliases, сохранённые facets и финальный статус. Полные правила находятся в `rust-coding-rules/references/rules/`, а progressive disclosure идёт через 26 indexes. Reference-корпусы, Graphify и Cargo harness не требуются runtime-плагину.

Actionbook интегрирован как cognitive protocol, а не как второй конкурирующий plugin. `provenance/actionbook-coverage.json` учитывает все 242 файла pinned revision: полные L1/L2 mental models, design tracing, IoT/embedded/cloud-native constraint maps, ML, LSP/Graphify/`rg` navigation, symbol/trait/dependency/call graphs, Cargo-metadata dossiers, learner/docs/news и 47 unsafe/FFI rules. У каждого unsafe rule сохранён исходный ID и полный текст, а устаревшие или универсальные рекомендации снабжены локальной product correction. Автоматически остаётся только быстрый SessionStart router; тяжёлые, сетевые и мутирующие действия выбираются явно. Лицензионный и revision audit находится в `provenance/THIRD_PARTY_NOTICES.md`.

Huiali-корпус интегрирован по 39 source families без создания 35 конкурирующих skills. Четыре уникальных владельца — `rust-pin`, `rust-gpu`, `rust-systems-networking` и `rust-distributed-systems`; actor/async/coroutine, complex lifetime/affine resource, proc-macro, learning, type/const/zero-cost и доменные constraint maps раскрываются через отдельные `references/huiali/*.md` у существующих владельцев. Эти references содержат 13 836 непустых строк адаптированных workflow, алгоритмов и примеров. `provenance/huiali-coverage.json` учитывает все 348 файлов, 150 exact duplicates и все 500 Rust-блоков: 423 уникальных решения, из которых 414 retained, 1 corrected и 8 rejected с причиной. Устаревшие Aya/generator examples не выдаются за современный код; dependency- и hardware-specific snippets маркируются fragments.

## Agents и права на изменения

Плагин поставляет четыре общие read-only роли Claude Code: `rust-scout`, `rust-researcher`, `rust-reviewer`, `rust-verifier`. В Codex тот же контракт может выполняться native subagents. Делегирование необязательно и применяется только к независимым вопросам, которые реально уменьшают неопределённость.

Главный агент остаётся единственным writer, принимает cross-profile решения, интегрирует результат и отвечает за final diff. Для post-fix re-review предпочтителен свежий reviewer context.

## Структура продукта

- `.codex-plugin/plugin.json` — Codex manifest;
- `.claude-plugin/plugin.json` — Claude Code manifest;
- `hooks/hooks.json` и `hooks/claude.json` — раздельные host schema;
- `scripts/session-context.*` — быстрый общий SessionStart detector;
- `skills/` — 50 host-neutral навыков и их references/examples;
- `agents/` — четыре read-only Claude agents;
- `evals/evals.json` — schema v5: 108 базовых routing cases, 44 rulebook overlay cases и ссылки на 44 Actionbook и 48 Huiali cases;
- `evals/actionbook-cases.json` — model, cross-layer, navigation, research, unsafe, ML и negative сценарии;
- `evals/huiali-cases.json` — 16 new-profile, 16 merged-topic, 8 conflict и 8 negative сценариев; вместе с base/Actionbook это 200 routing/protocol cases;
- `provenance/source-coverage.json` — проверяемая карта исходного корпуса;
- `provenance/rule-coverage.json` — проверяемое покрытие 265 Leonardomso rules;
- `provenance/actionbook-coverage.json` — per-file учёт 242 Actionbook sources;
- `provenance/huiali-coverage.json` — per-file и per-Rust-block учёт Huiali snapshot;
- `checks/rulebook/` — dev-only locked Cargo harness и stdlib-only генератор classified examples;
- `checks/metadata-workspace/` — path-only fixture для inherited, renamed, optional и target-specific Cargo dependencies;
- `scripts/validate.py` — стандартно-библиотечный валидатор продукта.

## Проверка

Из корня репозитория:

```powershell
python plugins/rust-engineering/scripts/validate.py --examples
claude plugin validate ./plugins/rust-engineering
```

Первая команда проверяет оба manifest, 50 skills и `openai.yaml`, 265 Leonardomso rules, 47 Actionbook unsafe/FFI rules, aliases, indexes, pinned source hashes, classified Rust blocks, Markdown links, SessionStart-only hooks, четыре agent-контракта, 242-file Actionbook ledger, Huiali `348/348` ledger с `500/423/77` block accounting, 200 base/Actionbook/Huiali routing cases и 44 rulebook overlay cases, а также locked/offline Cargo metadata fixture. С `--examples` она дополнительно компилирует 25 dependency-free golden examples, три standalone rulebook examples и один ожидаемый compile-fail; шесть fixture examples сначала проверяются `cargo --locked --offline`. Если crate отсутствует в Cargo cache, validator сообщает environment skip и требует отдельного разрешения перед `cargo fetch --locked`.

Дополнительно skill и Codex manifest можно прогнать штатными валидаторами `skill-creator` и `plugin-creator`. Существующий Graphify-граф помогает искать связи в исходных корпусах, но не является runtime-зависимостью или обязательным build gate; вывод графа всегда подтверждается по текущим файлам.
