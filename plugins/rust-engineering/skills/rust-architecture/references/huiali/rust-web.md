# Huiali Web Protocol

> Product adaptation of `skills/rust-web/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-architecture`.
- Supporting profiles when needed: `$rust-api-design`, `$rust-errors`.
- Scope retained: HTTP boundaries, extraction, validation, state ownership, cancellation, response contracts, graceful shutdown, and framework isolation.
- Baseline correction: Do not select or prescribe a web framework without project evidence. Keep transport DTOs, domain types, and infrastructure errors separated.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Framework Selection

| Framework | Characteristics | Recommended For |
|-----------|-----------------|-----------------|
| **axum** | Modern, Tokio ecosystem, type-safe | New projects (default choice) |
| **actix-web** | High performance, Actor model | Performance-critical services |
| **rocket** | Developer-friendly, zero-config | Rapid prototyping |
| **warp** | Filter-based, functional style | Niche use cases |

**Recommendation**: Start with **axum** for most projects. It has excellent ergonomics, strong ecosystem integration, and active development.


## Solution Patterns

### Pattern 1: Axum Basic Structure

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-1; sha256=875557b9c40b24ff50701f442f2e83b46c0c05fe5d50ca925519aa9cf06d00f7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).delete(delete_user))
        .with_state(app_state());

    let listener = tokio::net::TcpListener::bind("0.0.0.0:3000")
        .await
        .unwrap();

    axum::serve(listener, app)
        .await
        .unwrap();
}
```

**Key insight**: Routes are type-safe, handlers are async functions.

### Pattern 2: Handler Patterns

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-2; sha256=435e064b79def566bb862d5986dbe20ef2f641a0b4cff7968dfb4af26f54875c -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{extract::{Path, Query, Json}, http::StatusCode};

// Path parameters
async fn get_user(Path(id): Path<u32>) -> Result<Json<User>, StatusCode> {
    User::find(id).await
        .map(Json)
        .ok_or(StatusCode::NOT_FOUND)
}

// JSON body
async fn create_user(
    Json(payload): Json<CreateUserRequest>
) -> Result<Json<User>, StatusCode> {
    User::create(payload).await
        .map(Json)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)
}

// Query parameters
async fn list_users(
    Query(params): Query<ListUsersParams>
) -> Json<Vec<User>> {
    Json(User::list(params).await)
}

// Multiple extractors
async fn update_user(
    Path(id): Path<u32>,
    State(db): State<DbPool>,
    Json(update): Json<UserUpdate>,
) -> Result<Json<User>, ApiError> {
    User::update(&db, id, update).await
        .map(Json)
}
```

**When to use**: Each extractor pattern for different input types.

### Pattern 3: State Management

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-3; sha256=c0db09d187c78a5da1a5003cc16bd0d3c42935ad11fde16b88822de156650b4e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use std::sync::Arc;
use sqlx::PgPool;

// Define shared state
#[derive(Clone)]
struct AppState {
    db: PgPool,
    config: Arc<Config>,
}

// Extract state in handlers
async fn handler(State(state): State<AppState>) -> Json<Response> {
    let user = User::fetch(&state.db, 123).await?;
    Json(Response { user })
}

// Setup
let state = AppState {
    db: PgPoolOptions::new()
        .max_connections(5)
        .connect(&db_url)
        .await?,
    config: Arc::new(load_config()),
};

let app = Router::new()
    .route("/", get(handler))
    .with_state(state);
```

**When to use**: Share database pools, configuration, clients across handlers.

**Trade-offs**: State must be `Clone + Send + Sync + 'static`.

### Pattern 4: Error Handling

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-4; sha256=f80120afbb17cc6ce21d03b9bff3670164f3267da73ab18a6a844b9ab3fa35d7 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{
    response::{IntoResponse, Response},
    http::StatusCode,
    Json,
};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("resource not found")]
    NotFound,

    #[error("invalid input: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),

    #[error("authentication required")]
    Unauthorized,
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            ApiError::NotFound => (StatusCode::NOT_FOUND, self.to_string()),
            ApiError::Validation(msg) => (StatusCode::BAD_REQUEST, msg),
            ApiError::Database(e) => {
                tracing::error!("database error: {}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error".to_string())
            }
            ApiError::Unauthorized => (StatusCode::UNAUTHORIZED, self.to_string()),
        };

        (status, Json(serde_json::json!({
            "error": message
        }))).into_response()
    }
}
```

**When to use**: Custom error types for domain-specific failures.


## Workflow

### Step 1: Choose Framework

```
Need high performance?
  → actix-web

Want modern ergonomics + Tokio ecosystem?
  → axum (recommended)

Rapid prototyping?
  → rocket
```

### Step 2: Design Handler Signatures

```
What data comes from?
  Path → Path<T>
  Query string → Query<T>
  JSON body → Json<T>
  Headers → TypedHeader<T>
  State → State<AppState>
```

### Step 3: Implement Error Handling

```
Library code?
  → Custom error enum + IntoResponse

Application code?
  → anyhow::Error with context
```

### Step 4: Add Middleware

```
Logging → tower_http::trace
CORS → tower_http::cors
Rate limiting → tower::limit
Authentication → custom middleware
```


## Middleware Patterns

### Logging Middleware

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-5; sha256=c7a670b56d5416a052a0da0bef0353f3addc94f70e8ff14984bb053876b07b8e -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{
    middleware::{self, Next},
    http::Request,
    response::Response,
};
use std::time::Instant;

async fn log_requests<B>(
    req: Request<B>,
    next: Next<B>,
) -> Response {
    let start = Instant::now();
    let method = req.method().clone();
    let uri = req.uri().clone();

    let response = next.run(req).await;

    tracing::info!(
        "{} {} {} - {:?}",
        method,
        uri,
        response.status(),
        start.elapsed()
    );

    response
}

// Apply middleware
let app = Router::new()
    .route("/", get(handler))
    .layer(middleware::from_fn(log_requests));
```

### Authentication Middleware

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-6; sha256=d5e9a86f4d15e42276053f7ccf4d3261549b4c51034965e50b7501c8bb583fd6 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{
    middleware,
    extract::Request,
    http::{StatusCode, header},
};

async fn auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get(header::AUTHORIZATION)
        .and_then(|h| h.to_str().ok())
        .ok_or(StatusCode::UNAUTHORIZED)?;

    let user = validate_token(auth_header)
        .ok_or(StatusCode::UNAUTHORIZED)?;

    req.extensions_mut().insert(user);
    Ok(next.run(req).await)
}
```


## Database Integration

### SQLx Pattern

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-7; sha256=462053f81843f7673358c7ace3dcccd5596562b42a0d89acfc72066f186574b9 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use sqlx::{PgPool, FromRow};
use chrono::{DateTime, Utc};

// Define model
#[derive(Debug, FromRow)]
struct User {
    id: i32,
    name: String,
    email: String,
    created_at: DateTime<Utc>,
}

// Query
async fn get_user(pool: &PgPool, id: i32) -> Result<User, sqlx::Error> {
    sqlx::query_as!(
        User,
        "SELECT id, name, email, created_at FROM users WHERE id = $1",
        id
    )
    .fetch_one(pool)
    .await
}

// Transaction
async fn create_user_with_profile(
    pool: &PgPool,
    user: NewUser,
) -> Result<User, sqlx::Error> {
    let mut tx = pool.begin().await?;

    let user_id = sqlx::query!(
        "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id",
        user.name,
        user.email
    )
    .fetch_one(&mut *tx)
    .await?
    .id;

    sqlx::query!(
        "INSERT INTO profiles (user_id, bio) VALUES ($1, $2)",
        user_id,
        user.bio
    )
    .execute(&mut *tx)
    .await?;

    tx.commit().await?;

    get_user(pool, user_id).await
}
```


## Best Practices

| Concern | Recommendation |
|---------|----------------|
| JSON serialization | `#[derive(Serialize, Deserialize)]` + serde |
| Configuration | `config` crate + environment variables |
| Logging | `tracing` + `tracing-subscriber` |
| Health check | `GET /health` endpoint returning 200 |
| CORS | `tower_http::cors::CorsLayer` |
| Rate limiting | `tower::limit::RateLimitLayer` |
| OpenAPI | `utoipa` for API documentation |
| Request validation | `validator` crate with #[validate] |
| Graceful shutdown | `tokio::signal` for SIGTERM handling |


## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Using `Rc` for state | Not thread-safe | Use `Arc` |
| Holding locks across `.await` | Potential deadlock | Minimize lock scope |
| Not handling errors | Handler panics | Implement `IntoResponse` for errors |
| Large request bodies | Memory pressure | Set body size limits with `DefaultBodyLimit` |
| Missing CORS headers | Browser blocks requests | Add `CorsLayer` |
| Synchronous blocking | Blocks executor | Use `spawn_blocking` for CPU work |


## Domain-Driven Project Structure

**Recommended structure for medium-to-large projects:**

```text
src/
├── main.rs                              # Entry point (load config, start HTTP)
├── bootstrap/
│   ├── mod.rs
│   └── app_builder.rs                   # Global assembly (DB/Cache/Telemetry)
├── domains/
│   ├── user/                            # Domain directory with all layers
│   │   ├── mod.rs
│   │   ├── http.rs                      # Routes + handlers + DTO mapping
│   │   ├── app.rs                       # Use cases / commands / queries
│   │   ├── entity.rs                    # Domain entities
│   │   ├── value.rs                     # Value objects
│   │   ├── policy.rs                    # Domain rules/policies
│   │   ├── port.rs                      # Port definitions (traits)
│   │   ├── repo.rs                      # Infrastructure implementation
│   │   ├── cache.rs                     # Caching adapter
│   │   ├── errors.rs                    # Domain errors
│   │   └── tests.rs                     # Domain tests
│   ├── auth/
│   │   ├── mod.rs
│   │   ├── http.rs
│   │   ├── app.rs
│   │   ├── entity.rs
│   │   ├── policy.rs
│   │   ├── port.rs
│   │   ├── repo.rs
│   │   ├── jwt.rs
│   │   ├── errors.rs
│   │   └── tests.rs
│   └── order/
│       ├── mod.rs
│       ├── http.rs
│       ├── app.rs
│       ├── entity.rs
│       ├── port.rs
│       ├── repo.rs
│       ├── events.rs
│       ├── errors.rs
│       └── tests.rs
├── shared/
│   ├── mod.rs
│   ├── error.rs                         # Common error model
│   ├── result.rs                        # Unified Result alias
│   ├── types.rs                         # Common types (ID/Time)
│   └── middleware.rs                    # Cross-domain middleware
└── tests/
    ├── integration/
    └── fixtures/
```

**Structural Principles:**
- **Domain-centric**: Each domain contains interface/application/domain/infrastructure concerns
- **File naming**: Single-word filenames clarify responsibility (`app.rs`, `port.rs`, `repo.rs`, `http.rs`)
- **Loose coupling**: Domains collaborate through application-layer interfaces, avoid direct access
- **Shared utilities**: Common capabilities in `shared/`, domain-specific logic stays local

**File Responsibilities:**
- `http.rs` - HTTP routes, handlers, request/response DTOs
- `app.rs` - Application services, use case orchestration
- `entity.rs` - Domain entities with business logic
- `port.rs` - Port trait definitions (hexagonal architecture)
- `repo.rs` - Repository implementations (database, cache)
- `errors.rs` - Domain-specific error types


## Review Checklist

When reviewing web service code:

- [ ] Handlers have appropriate extractors (Path, Query, Json)
- [ ] Shared state uses `Arc` for thread safety
- [ ] Error types implement `IntoResponse`
- [ ] Database operations use connection pooling
- [ ] Middleware is composable and reusable
- [ ] API responses follow consistent JSON format
- [ ] Authentication/authorization properly enforced
- [ ] Request body size limits configured
- [ ] CORS configured for browser clients
- [ ] Health check endpoint exists
- [ ] Logging/tracing properly instrumented
- [ ] Graceful shutdown implemented


## Verification Commands

```bash
# Check compilation
cargo check

# Run tests
cargo test

# Integration tests
cargo test --test integration

# Check for common mistakes
cargo clippy -- -D warnings

# Run development server
cargo run

# Build optimized release
cargo build --release

# Run with environment variables
DATABASE_URL=postgres://localhost cargo run
```


## Performance Optimization

### Connection Pooling

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-8; sha256=4cc949e550f7a58f7e7103b546b848be82e3bba28a7ee18717e8569a956e2914 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use sqlx::postgres::PgPoolOptions;

let pool = PgPoolOptions::new()
    .max_connections(100)
    .min_connections(10)
    .acquire_timeout(Duration::from_secs(5))
    .idle_timeout(Duration::from_secs(600))
    .connect(&database_url)
    .await?;
```

### Response Compression

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-9; sha256=aba3749755d91b9410213bbe5f8a5530885134ef1391e9782e8c32edfffb505b -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use tower_http::compression::CompressionLayer;

let app = Router::new()
    .route("/", get(handler))
    .layer(CompressionLayer::new());
```

### Caching Headers

<!-- huiali-source: skills/rust-web/SKILL.md#rust-block-10; sha256=253d355c09699c1071d815f2ebafc09aefc546b67f4412ae0d9af5f86f7d5be2 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::http::{header, HeaderMap};

async fn cached_handler() -> (HeaderMap, Json<Data>) {
    let mut headers = HeaderMap::new();
    headers.insert(
        header::CACHE_CONTROL,
        "public, max-age=3600".parse().unwrap(),
    );

    (headers, Json(get_data()))
}
```


## Related Skills

- **rust-async** - Async patterns for handlers
- **rust-concurrency** - Thread safety in web services
- **rust-database** - Database integration patterns
- **rust-error** - Error handling strategies
- **rust-auth** - Authentication and authorization
- **rust-middleware** - Middleware patterns
- **rust-observability** - Logging and metrics

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-web/SKILL_ZH.md#rust-block-1; sha256=a6247ca9dd747ed560a7b632d065ef72f8af66b5596a63d4ed3d95f382efc223 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{routing::get, Router};

#[tokio::main]
async fn main() {
    let app = Router::new()
        .route("/", get(root))
        .route("/users", get(list_users).post(create_user))
        .route("/users/:id", get(get_user).delete(delete_user))
        .with_state(pool.clone());

    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-web/SKILL_ZH.md#rust-block-2; sha256=f6e5e8f5ca043413fe94664f1024147dba5a9907e233977e312c5c4f68a2bac1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 从路径获取参数
async fn get_user(Path(id): Path<u32>) -> Json<User> {
    User::find(id).await
        .map(Json)
        .ok_or_else(|| StatusCode::NOT_FOUND)
}

// 从 JSON body 获取
async fn create_user(Json(user): Json<CreateUserRequest>) -> Result<Json<User>, StatusCode> {
    User::create(user).await
        .map(Json)
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)
}

// 查询参数
async fn list_users(Query(params): Query<ListUsersParams>) -> Json<Vec<User>> {
    User::list(params).await
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-web/SKILL_ZH.md#rust-block-3; sha256=a913b7f7f88c73261d6a7f41c76034a5853daf16b57b4b7ae112bafcb71205fe -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// AppState 类型
type AppState = Arc<Pool<Postgres>>;

// 提取状态
async fn handler(state: State<AppState>) { ... }

// 共享状态
let pool = PgPoolOptions::new()
    .max_connections(5)
    .connect(&db_url)
    .await?;

let app = Router::new()
    .route("/", get(handler))
    .with_state(Arc::new(pool));
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-web/SKILL_ZH.md#rust-block-4; sha256=0e336e4a15c5dbcae193f1905f6f61a3895d0e27ff44ee766b43a805f535ce24 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{
    response::{IntoResponse, Response},
    Json,
};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ApiError {
    #[error("user not found")]
    NotFound,

    #[error("invalid input: {0}")]
    Validation(String),

    #[error("database error")]
    Database(#[from] sqlx::Error),
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        match self {
            ApiError::NotFound => (StatusCode::NOT_FOUND, self.to_string()).into_response(),
            ApiError::Validation(msg) => (StatusCode::BAD_REQUEST, msg).into_response(),
            ApiError::Database(e) => {
                tracing::error!("database error: {}", e);
                (StatusCode::INTERNAL_SERVER_ERROR, "internal error").into_response()
            }
        }
    }
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-web/SKILL_ZH.md#rust-block-5; sha256=79764de52d2ea0127357d61f97d96f3f8bad6e3ba44e2828c41ec099948a2cf9 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 记录请求日志
async fn log_requests(req: Request, next: Next) -> Result<Response, Infallible> {
    let start = Instant::now();
    let method = req.method().clone();
    let path = req.uri().path().to_string();

    let response = next.run(req).await;

    tracing::info!(
        "{} {} {} - {:?}",
        method,
        path,
        response.status(),
        start.elapsed()
    );

    Ok(response)
}

// 使用
let app = Router::new()
    .route("/", get(handler))
    .layer(layer_fn(log_requests));
```

### `SKILL_ZH.md` example 6

<!-- huiali-source: skills/rust-web/SKILL_ZH.md#rust-block-6; sha256=8fef1cd28ed3c57149a9120a7b679e83d226234e504cc33d62b774433d9c0cdf -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// 定义模型
#[derive(Debug, FromRow)]
struct User {
    id: i32,
    name: String,
    email: String,
    created_at: chrono::DateTime<Utc>,
}

// 查询
async fn get_user(pool: &Pool<Postgres>, id: i32) -> Result<User, sqlx::Error> {
    sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(pool)
        .await
}

// 事务
let mut tx = pool.begin().await?;
sqlx::query!("INSERT INTO ...") .execute(&mut *tx).await?;
tx.commit().await?;
```
