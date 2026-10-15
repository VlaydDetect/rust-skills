# Rust Engineering

**Сфокусированные инструкции по Rust: от первого вопроса до проверенного изменения.**

[English](README.md) · [Русский](README_ru.md) · [Релизы](https://github.com/VlaydDetect/rust-skills/releases) · [Лицензия MIT](plugins/rust-engineering/LICENSE)

Единый плагин для **Codex / ChatGPT Desktop** и **Claude Code / Desktop**. Rust Engineering помогает агенту разобраться в репозитории, подобрать профиль, сохранить контракты и подтвердить результат проверками.

| Скиллы | Правила Rust | Правила unsafe / FFI | Eval-сценарии |
| :---: | :---: | :---: | :---: |
| **57** | **265** | **47** | **369** |

[Установка](#установка) · [С чего начать](#с-чего-начать) · [Каталог скиллов](#каталог-скиллов) · [Как это работает](#как-это-работает) · [Проверка](#проверка)

## С чего начать

Опишите результат и ограничения обычным языком либо вызовите скилл напрямую: `$skill-name` в Codex и `/rust-engineering:skill-name` в Claude Code.

| Задача | Точка входа | Что происходит дальше |
| --- | --- | --- |
| Реализовать возможность или исправление | `rust-workflow` | Анализ проекта, владельцы решений, изменение и проверка. |
| Разобраться с необъяснимым сбоем | `debugging` | Воспроизведение ошибки и локализация причины до исправления. |
| Изучить незнакомый репозиторий | `codebase-onboarding` | Карта пакетов, точек входа, границ, команд и рисков. |
| Проверить изменение | `rust-review` | Анализ diff и связанного кода, подтверждённые замечания. |
| Запустить проверки существующего состояния | `rust-verify` | Достаточный набор проверок с разделением ошибок и ограничений среды. |
| Улучшить производительность | `rust-performance` | Измерения в `rust-profiling`, изменения в `rust-optimization`, доказательства безопасности в `rust-unsafe`. |
| Подготовить development shell | `nix-dev-env` | Анализ toolchain и нативных зависимостей перед проектированием среды. |

## Установка

Текущий релиз-кандидат — **1.0.2-rc**, фиксированный Git-тег `v1.0.2-rc`. Выберите один из установщиков: оба используют нативные команды хоста и не имеют собственных пакетных зависимостей.

**Через uv**

~~~powershell
uv run --no-project https://raw.githubusercontent.com/VlaydDetect/rust-skills/v1.0.2-rc/installers/install.py --target all
~~~

**Через npx**

~~~powershell
npx --yes github:VlaydDetect/rust-skills#v1.0.2-rc --target all
~~~

<details>
<summary>Другие package runners и параметры установщиков</summary>

~~~powershell
npm exec --yes --package=github:VlaydDetect/rust-skills#v1.0.2-rc -- rust-engineering-install --target all
pnpm dlx github:VlaydDetect/rust-skills#v1.0.2-rc --target all
~~~

- `--target codex-cli|chatgpt-desktop|claude-code|claude-desktop|all` (по умолчанию `all`).
- `--scope user|project|local` для Claude (по умолчанию `user`).
- `--dry-run` печатает план без изменений.
- `--yes` пропускает подтверждение установщика.

Для CLI-целей нужен CLI соответствующего хоста. Установщики не устанавливают Codex, Claude, Node.js, uv или Rust. Если имя marketplace занято другим источником, установка останавливается.

</details>

<details>
<summary>Нативная установка и обновление через CLI</summary>

Codex:

~~~powershell
codex plugin marketplace add VlaydDetect/rust-skills --ref v1.0.2-rc
codex plugin add rust-engineering@rust-skills
~~~

Claude Code:

~~~powershell
claude plugin marketplace add VlaydDetect/rust-skills@v1.0.2-rc --scope user
claude plugin install rust-engineering@rust-skills --scope user
~~~

Для обновления настроенного источника используйте `codex plugin marketplace upgrade rust-skills` либо `claude plugin marketplace update rust-skills`. Для Claude затем выполните `claude plugin update rust-engineering@rust-skills --scope user`.

Обновление сохраняет настроенный Git ref. Если выбран старый релизный тег, сначала переключите ref на нужный релиз через команды marketplace или UI хоста: обновление старого тега не выбирает новый релиз. Проверяйте установленную версию через `codex plugin list --json` либо `claude plugin list --json`.

</details>

**Desktop:** подтвердите установку через каталог плагинов хоста или `/plugin` в локальной сессии. В Codex / ChatGPT Desktop начните новую задачу; в Claude при необходимости выполните `/reload-plugins` или перезапустите приложение. Установщики выводят инструкции для Desktop и не редактируют его конфигурацию или кэши напрямую.

## Каталог скиллов

Каждая ссылка открывает инструкции скилла. Подробные references загружаются только для текущего решения.

### Процесс и навигация

| Скилл | Когда использовать |
| --- | --- |
| [rust-workflow](plugins/rust-engineering/skills/rust-workflow/SKILL.md) | Координировать изменение, назначить владельцев решений и собрать доказательства. |
| [specs](plugins/rust-engineering/skills/specs/SKILL.md) | Превратить запрос в наблюдаемые контракты и сценарии приёмки. |
| [codebase-onboarding](plugins/rust-engineering/skills/codebase-onboarding/SKILL.md) | Разобраться в незнакомом репозитории перед существенными изменениями. |
| [rust-navigation](plugins/rust-engineering/skills/rust-navigation/SKILL.md) | Найти определения, вызовы, реализации трейтов, макросы и feature gates. |
| [rust-design-protocol](plugins/rust-engineering/skills/rust-design-protocol/SKILL.md) | Согласовать существенные решения между языком, дизайном и предметной областью. |
| [debugging](plugins/rust-engineering/skills/debugging/SKILL.md) | Воспроизвести и локализовать ошибки компиляции, исполнения, конкурентности и производительности. |
| [refactoring](plugins/rust-engineering/skills/refactoring/SKILL.md) | Изменить структуру кода с сохранением поведения и совместимости. |
| [addressing-findings](plugins/rust-engineering/skills/addressing-findings/SKILL.md) | Разобрать замечания, исправить подтверждённые проблемы и проверить результат. |

### Ревью и доказательства

| Скилл | Когда использовать |
| --- | --- |
| [rust-review](plugins/rust-engineering/skills/rust-review/SKILL.md) | Проверить ограниченный diff и вернуть подтверждённые замечания с вердиктом. |
| [rust-architecture-review](plugins/rust-engineering/skills/rust-architecture-review/SKILL.md) | Оценить границы пакетов, направление зависимостей, связность и сложность. |
| [rust-verify](plugins/rust-engineering/skills/rust-verify/SKILL.md) | Запустить достаточные проверки и классифицировать причины сбоев. |
| [rust-research](plugins/rust-engineering/skills/rust-research/SKILL.md) | Проверить актуальные сведения о Rust и экосистеме по первоисточникам. |

### Язык и API

| Скилл | Когда использовать |
| --- | --- |
| [rust-api-design](plugins/rust-engineering/skills/rust-api-design/SKILL.md) | Спроектировать публичные контракты, видимость и удобство использования API. |
| [rust-ownership](plugins/rust-engineering/skills/rust-ownership/SKILL.md) | Разобраться с заимствованиями, временами жизни, перемещениями и владением ресурсами. |
| [rust-traits](plugins/rust-engineering/skills/rust-traits/SKILL.md) | Выбрать обобщения, trait objects, bounds, ассоциированные типы и typestate. |
| [rust-errors](plugins/rust-engineering/skills/rust-errors/SKILL.md) | Определить границы ошибок, восстановление, контекст и политику panic. |
| [rust-idioms](plugins/rust-engineering/skills/rust-idioms/SKILL.md) | Применить идиомы Rust с учётом ограничений проекта. |
| [rust-stable](plugins/rust-engineering/skills/rust-stable/SKILL.md) | Выбрать edition, MSRV, стабильные возможности и подход к совместимости. |
| [rust-stdlib](plugins/rust-engineering/skills/rust-stdlib/SKILL.md) | Подобрать стандартные коллекции, итераторы, I/O и средства синхронизации. |
| [rust-by-example](plugins/rust-engineering/skills/rust-by-example/SKILL.md) | Объяснить механизм Rust минимальным компилируемым примером. |
| [rust-pin](plugins/rust-engineering/skills/rust-pin/SKILL.md) | Установить гарантии стабильности адреса, проекций, polling и pinned destruction. |

### Cargo, структура и качество

| Скилл | Когда использовать |
| --- | --- |
| [rust-cargo-build](plugins/rust-engineering/skills/rust-cargo-build/SKILL.md) | Разобраться с manifests, features, профилями, build scripts и состоянием Cargo. |
| [rust-workspace](plugins/rust-engineering/skills/rust-workspace/SKILL.md) | Спроектировать границы crates, общие метаданные, resolver и группы релизов. |
| [rust-module-layout](plugins/rust-engineering/skills/rust-module-layout/SKILL.md) | Организовать модули, файлы, видимость, реэкспорты и размещение тестов. |
| [rust-dependencies](plugins/rust-engineering/skills/rust-dependencies/SKILL.md) | Управлять версиями, features, источниками и безопасностью принятых зависимостей. |
| [rust-crate-discovery](plugins/rust-engineering/skills/rust-crate-discovery/SKILL.md) | Проверить кандидатов на роль зависимости до их принятия в проект. |
| [rust-semver](plugins/rust-engineering/skills/rust-semver/SKILL.md) | Оценить совместимость изменений API, поведения, features и MSRV. |
| [rust-style-clippy](plugins/rust-engineering/skills/rust-style-clippy/SKILL.md) | Применить правила форматирования и lint с обоснованными исключениями. |
| [rust-testing](plugins/rust-engineering/skills/rust-testing/SKILL.md) | Спроектировать unit, integration, property, async, fuzz и end-to-end тесты. |
| [rust-documentation](plugins/rust-engineering/skills/rust-documentation/SKILL.md) | Поддерживать rustdoc, примеры, doctests, README и инструкции миграции. |
| [rust-ecosystem](plugins/rust-engineering/skills/rust-ecosystem/SKILL.md) | Выбрать форму проекта и соглашения toolchain до выбора конкретных crates. |
| [rust-coding-rules](plugins/rust-engineering/skills/rust-coding-rules/SKILL.md) | Подобрать конкретные правила из каталога 265 правил после маршрутизации. |

### Архитектура и исполнение

| Скилл | Когда использовать |
| --- | --- |
| [rust-architecture](plugins/rust-engineering/skills/rust-architecture/SKILL.md) | Определить границы системы, направление зависимостей, порты, адаптеры и композицию. |
| [rust-concurrency](plugins/rust-engineering/skills/rust-concurrency/SKILL.md) | Спроектировать задачи, потоки, блокировки, каналы, отмену и backpressure. |
| [rust-data](plugins/rust-engineering/skills/rust-data/SKILL.md) | Выбрать представление и обход данных по измеренным паттернам доступа. |
| [rust-database](plugins/rust-engineering/skills/rust-database/SKILL.md) | Организовать транзакции, пулы, миграции, повторы, резервирование и интеграционные тесты. |
| [rust-distributed-systems](plugins/rust-engineering/skills/rust-distributed-systems/SKILL.md) | Учесть частичные отказы, идемпотентность, согласованность и координацию. |
| [rust-serialization](plugins/rust-engineering/skills/rust-serialization/SKILL.md) | Определить форматы, эволюцию схемы, канонические байты и ограничения декодирования. |
| [rust-platforms](plugins/rust-engineering/skills/rust-platforms/SKILL.md) | Спроектировать поведение на Unix и Windows и жизненный цикл ресурсов. |
| [rust-observability](plugins/rust-engineering/skills/rust-observability/SKILL.md) | Спроектировать tracing, логи, метрики, корреляцию, редактирование данных и cardinality. |

### Производительность и безопасность

| Скилл | Когда использовать |
| --- | --- |
| [rust-performance](plugins/rust-engineering/skills/rust-performance/SKILL.md) | Уточнить задачу производительности и выбрать профиль через совместимую точку входа. |
| [rust-profiling](plugins/rust-engineering/skills/rust-profiling/SKILL.md) | Спроектировать корректный эксперимент и интерпретировать бенчмарки, профили, счётчики и трассы. |
| [rust-optimization](plugins/rust-engineering/skills/rust-optimization/SKILL.md) | Выбрать изменения по подтверждённому узкому месту и проверить системный эффект. |
| [rust-unsafe](plugins/rust-engineering/skills/rust-unsafe/SKILL.md) | Доказать предусловия unsafe и корректность безопасных абстракций; использовать Miri как дополнительную проверку. |
| [rust-unsafe-ffi](plugins/rust-engineering/skills/rust-unsafe-ffi/SKILL.md) | Определить ABI, передачу владения, callbacks, unwinding и времена жизни на FFI-границе. |

### Специализированный Rust

| Скилл | Когда использовать |
| --- | --- |
| [rust-macros](plugins/rust-engineering/skills/rust-macros/SKILL.md) | Спроектировать декларативные и процедурные макросы с контролируемым раскрытием и диагностикой. |
| [rust-lombok-macros](plugins/rust-engineering/skills/rust-lombok-macros/SKILL.md) | Оценить derives и атрибуты для конструкторов, builders и шаблонного кода. |
| [rust-tauri](plugins/rust-engineering/skills/rust-tauri/SKILL.md) | Спроектировать границы Tauri 2: IPC, capabilities, plugins, updater и frontend. |
| [rust-uniffi-building](plugins/rust-engineering/skills/rust-uniffi-building/SKILL.md) | Поддерживать интерфейсы UniFFI, bindings, scaffolding и межъязыковые тесты. |
| [rust-ml](plugins/rust-engineering/skills/rust-ml/SKILL.md) | Спроектировать работу с моделями, тензорами, preprocessing, устройствами и serving. |
| [rust-gpu](plugins/rust-engineering/skills/rust-gpu/SKILL.md) | Проанализировать обмен с GPU, layouts, dispatch, синхронизацию и узкие места. |
| [rust-systems-networking](plugins/rust-engineering/skills/rust-systems-networking/SKILL.md) | Спроектировать eBPF и DPDK: буферы, очереди, владение, affinity и NUMA. |

### Nix и NixOS

| Скилл | Когда использовать |
| --- | --- |
| [nix-flakes](plugins/rust-engineering/skills/nix-flakes/SKILL.md) | Спроектировать flake inputs, locks, systems, overlays, packages и checks. |
| [nix-dev-env](plugins/rust-engineering/skills/nix-dev-env/SKILL.md) | Подготовить воспроизводимые Rust development shells и окружения редакторов. |
| [nix-packaging](plugins/rust-engineering/skills/nix-packaging/SKILL.md) | Упаковать Rust с фиксированными Cargo sources и воспроизводимой сборкой. |
| [nixos](plugins/rust-engineering/skills/nixos/SKILL.md) | Настроить модули NixOS и Home Manager, сервисы, options и secrets. |
| [nix-review](plugins/rust-engineering/skills/nix-review/SKILL.md) | Проверить Nix-изменения: purity, платформы, hashes и безопасность. |

## Как это работает

~~~text
Запрос → rust-workflow → анализ проекта → владельцы решений
       → нужные coding-профили и правила → реализация
       → rust-verify → rust-review по запросу или соразмерно риску
~~~

Workflow выбирает профили по текущему изменению. У каждого решения один владелец; helpers подключаются после наблюдаемого триггера. Лимиты `ProfileStack` — **3 owners / 6 coding-профилей / 10 helpers** — требуют разделить фазу при превышении. Rulebook добавляет не более **девяти релевантных правил на решение** после маршрутизации. Изменения вносит основной агент; вспомогательные агенты работают read-only.

Оптимизация начинается с нагрузки и измеримой цели. Сначала проверяется эксперимент, затем определяется ограничивающий ресурс, выбирается изменение по данным и инвариантам, после чего повторно измеряется вся система. Criterion, VTune, WPR/WPA, perf, анализ аллокаций, машинного кода, PGO и BOLT выбираются по задаче и платформе. Miri проверяет корректность исполненных путей; его timings не являются измерением нативной производительности.

SessionStart hooks анализируют локальные признаки проекта. Они остаются быстрыми, offline, детерминированными и read-only: нерелевантный каталог не вызывает вывода; Rust-проект получает контекст и предложение opt-in настройки. Nix/NixOS предлагается отдельно. Инструменты выбираются по данным проекта и устанавливаются только с разрешения.

Исходник продукта — `plugins/rust-engineering/`. Инструкции скиллов и общие скрипты не зависят от хоста; manifests и SessionStart schemas у Codex и Claude отдельные. Самому плагину не нужны дополнительные runtime-зависимости или сеть; отдельным исследовательским задачам и измерениям могут понадобиться внешние инструменты или онлайн-источники.

## Проверка

Из корня репозитория:

~~~powershell
uv run --no-project plugins/rust-engineering/scripts/validate.py --examples
node installers/install.mjs --target all --dry-run
git diff --check
~~~

Release gate проверяет оба README-каталога и ссылки, все 57 скиллов, структуру references, 265 rule ID/alias, 47 unsafe/FFI rules, 369 eval-сценариев схемы 9, четыре read-only agent contracts, manifests, parity установщиков, конфликты source, offline hooks и fixtures. Он запускает **25 golden example projects** и проверяет классификацию **1 141 примера правил**; компилируемые примеры тестируются в заявленном контексте.

Валидация eval JSON проверяет структуру и контракты маршрутизации. Поведенческие прогоны модели и аппаратные измерения являются отдельными доказательствами. При наличии Claude CLI выполните `claude plugin validate ./plugins/rust-engineering`; используйте validator хоста, если он доступен в установленной версии.

Если Miri не дошёл до тестов из-за запрета sandbox на запись в пользовательский кэш, проверьте причину и повторите ту же локальную команду под обычной учётной записью через разрешённый механизм запуска хоста. Сохраните toolchain, target, features и offline policy. Такой отказ не означает провал теста и не требует автоматической переустановки Miri.

## Лицензия

Проект распространяется по [MIT License](plugins/rust-engineering/LICENSE). Сторонние лицензии и атрибуции находятся в [THIRD_PARTY_NOTICES.md](plugins/rust-engineering/THIRD_PARTY_NOTICES.md).

## Источники

- [gurinderu/craft](https://github.com/gurinderu/craft), revision `d9caf7faf36b565a59534c581fdc27516e87600a`.
- [full-stack-skills/rust-skills](https://github.com/full-stack-skills/rust-skills), revision `25e44452df00055ca246ec806425d99028eaae19`.
- [leonardomso/rust-skills](https://github.com/leonardomso/rust-skills), revision `fd2a861ab0406a4ac536a55274d14ea6fd1ca9c9`.
- [actionbook/rust-skills](https://github.com/actionbook/rust-skills), revision `fa60f7931223646fb71c4586b4a6c8545016076a`.
- [huiali/rust-skills](https://github.com/huiali/rust-skills), revision `947bf77509d9b421035037e983da6662d08cbb8e`.
- [mohitmishra786/low-level-dev-skills](https://github.com/mohitmishra786/low-level-dev-skills), revision `bdc58472fa9f309ed1b3f7d985a0d8e9bd8f4608`.
- [laurigates/claude-plugins](https://github.com/laurigates/claude-plugins), revision `a1e72ed186b97555256d8c058ff291c182332df7`.

Материалы по оптимизации и измерениям (проверены 2026-10-15; результаты авторов не воспроизводились):

- [Figma: memory optimizations in Rust](https://www.figma.com/blog/supporting-faster-file-load-times-with-memory-optimizations-in-rust/).
- [Cloudflare: trie-hard](https://blog.cloudflare.com/pingora-saving-compute-1-percent-at-a-time/).
- [Cloudflare: WAF ML pipeline](https://blog.cloudflare.com/making-waf-ai-models-go-brr/).
- [Sentry: A locking war story](https://blog.sentry.io/locking-war-story/).
- [ScyllaDB: Rust Alternator driver](https://www.scylladb.com/2026/08/27/new-rust-driver-for-scylladbs-dynamodb-api/).
- [Cloudflare: DNS cache memory](https://blog.cloudflare.com/dns-cache-memory-optimization-1111/).
- [Cloudflare: consistent hashing memory](https://blog.cloudflare.com/saving-100-tb-of-ram-with-math/).
- [ClickHouse: hash tables and zero-cost abstractions](https://clickhouse.com/blog/hash-tables-in-clickhouse-and-zero-cost-abstractions).
- [ScyllaDB: asymmetric io_uring backend](https://www.scylladb.com/2026/07/22/asymmetric-io_uring-backend-seastar/).
- [Cloudflare: WAN throughput and latency](https://blog.cloudflare.com/optimizing-tcp-for-high-throughput-and-low-latency/).
- [Abseil #75: How to microbenchmark](https://abseil.io/fast/75).
- [Abseil #53: Hardware Performance Counters](https://abseil.io/fast/53).
- [Abseil #83: Reducing memory indirections](https://abseil.io/fast/83).
- [Abseil #39: Microbenchmark limitations](https://abseil.io/fast/39).
- [Abseil #88: Measurement methodology](https://abseil.io/fast/88).

Для ScyllaDB asymmetric io_uring доступен индексируемый фрагмент первоисточника; неподтверждённые численные детали не перенесены. Технические контракты инструментов проверяются по официальной документации, связанной с соответствующими протоколами.
