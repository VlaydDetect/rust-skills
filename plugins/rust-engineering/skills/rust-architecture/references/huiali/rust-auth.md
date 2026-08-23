# Huiali Auth Protocol

> Product adaptation of `skills/rust-auth/SKILL.md` at revision `947bf77509d9b421035037e983da6662d08cbb8e`. The source workflow is retained below; product routing and current-project constraints override source-wide preferences.

## Product routing and baseline

- Primary owner: `$rust-architecture`.
- Supporting profiles when needed: `$rust-errors`, `$rust-api-design`.
- Scope retained: Authentication and authorization boundaries, credential lifecycle, expiry, revocation, audit, secret handling, and failure taxonomy.
- Baseline correction: Model the application's threat and trust boundaries before selecting protocols or crates. Never invent credential, token, storage, or audit requirements.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Adapted source workflow

## Authentication Strategies

| Method | Use Case | Security | Complexity |
|--------|----------|----------|------------|
| **JWT Token** | API access, SPA | High | Medium |
| **API Key** | Service-to-service, automation | Medium | Low |
| **OAuth 2.0** | Third-party login | High | High |
| **Session Cookie** | Traditional web apps | Medium | Medium |
| **mTLS** | Service mesh, microservices | Very High | High |


## Solution Patterns

### Pattern 1: JWT Authentication

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-1; sha256=a804552650ace8bc5006c5b72c98296aeff4a48e769acc47a69ab2a0ee583b36 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,           // Subject (user ID)
    exp: u64,              // Expiration
    iat: u64,              // Issued at
    roles: Vec<String>,    // User roles
}

struct JwtService {
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    algorithm: Algorithm,
    expiry_seconds: u64,
}

impl JwtService {
    // Recommended: EdDSA (Ed25519)
    pub fn new_ed25519(private_pem: &[u8], public_pem: &[u8]) -> Result<Self, Error> {
        Ok(Self {
            encoding_key: EncodingKey::from_ed_pem(private_pem)?,
            decoding_key: DecodingKey::from_ed_pem(public_pem)?,
            algorithm: Algorithm::EdDSA,
            expiry_seconds: 3600, // 1 hour
        })
    }

    // Alternative: RS256 (RSA)
    pub fn new_rs256(private_pem: &[u8], public_pem: &[u8]) -> Result<Self, Error> {
        Ok(Self {
            encoding_key: EncodingKey::from_rsa_pem(private_pem)?,
            decoding_key: DecodingKey::from_rsa_pem(public_pem)?,
            algorithm: Algorithm::RS256,
            expiry_seconds: 3600,
        })
    }

    pub fn generate_token(&self, user_id: &str, roles: Vec<String>) -> Result<String, Error> {
        let now = SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs();

        let claims = Claims {
            sub: user_id.to_string(),
            exp: now + self.expiry_seconds,
            iat: now,
            roles,
        };

        encode(&Header::new(self.algorithm), &claims, &self.encoding_key)
            .map_err(Into::into)
    }

    pub fn verify_token(&self, token: &str) -> Result<Claims, Error> {
        let mut validation = Validation::new(self.algorithm);
        validation.validate_exp = true;

        decode::<Claims>(token, &self.decoding_key, &validation)
            .map(|data| data.claims)
            .map_err(Into::into)
    }
}
```

**Algorithm Selection:**
- **EdDSA (Ed25519)**: Recommended default (fast, secure, small keys)
- **RS256**: Use when ecosystem already standardized on RSA
- **HS256**: Only for single-service, tightly controlled scenarios

### Pattern 2: API Key Authentication

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-2; sha256=e0aef66e6011d654a2789f70c29074d77bcc6c99f3b49de50178ca188df3c0a2 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use sha2::{Digest, Sha256};
use rand::{thread_rng, Rng};

struct ApiKey {
    key_id: String,
    secret_hash: String,
    owner_id: String,
    scopes: Vec<String>,
    expires_at: i64,
    disabled: bool,
}

struct ApiKeyService {
    secret: String,
    prefix: String,
}

impl ApiKeyService {
    pub fn generate(&self, owner_id: &str, scopes: Vec<String>) -> (String, String) {
        let key_id = self.generate_id();
        let secret = self.generate_secret();
        let signature = self.compute_signature(&key_id, &secret);

        let api_key = format!("{}_{}_{}", self.prefix, key_id, signature);
        let secret_hash = self.hash_secret(&secret);

        (api_key, secret_hash)
    }

    pub fn verify(&self, api_key: &str, stored: &ApiKey) -> Result<(), AuthError> {
        if stored.disabled {
            return Err(AuthError::KeyRevoked);
        }

        let now = chrono::Utc::now().timestamp();
        if stored.expires_at < now {
            return Err(AuthError::KeyExpired);
        }

        let parts: Vec<&str> = api_key.split('_').collect();
        if parts.len() != 3 {
            return Err(AuthError::InvalidFormat);
        }

        let expected_sig = self.compute_signature(parts[1], "");
        if parts[2] != expected_sig {
            return Err(AuthError::InvalidSignature);
        }

        Ok(())
    }

    fn generate_id(&self) -> String {
        const CHARSET: &[u8] = b"abcdefghijklmnopqrstuvwxyz0123456789";
        let mut rng = thread_rng();
        (0..16).map(|_| CHARSET[rng.gen_range(0..CHARSET.len())] as char).collect()
    }

    fn generate_secret(&self) -> String {
        const CHARSET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        let mut rng = thread_rng();
        (0..32).map(|_| CHARSET[rng.gen_range(0..CHARSET.len())] as char).collect()
    }

    fn compute_signature(&self, key_id: &str, secret: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(format!("{}{}{}", key_id, secret, self.secret));
        format!("{:x}", hasher.finalize())[..16].to_string()
    }

    fn hash_secret(&self, secret: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(format!("{}{}", secret, self.secret));
        format!("{:x}", hasher.finalize())
    }
}
```

### Pattern 3: Password Hashing (Argon2)

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-3; sha256=f8460af8fe90efc64504889aa4d1746d94f78f303bd9fefb2deac789dd786f49 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use argon2::{Argon2, PasswordHash, PasswordHasher, PasswordVerifier};
use argon2::password_hash::{rand_core::OsRng, SaltString};

struct PasswordService;

impl PasswordService {
    pub fn hash_password(password: &str) -> Result<String, argon2::password_hash::Error> {
        let salt = SaltString::generate(&mut OsRng);
        let argon2 = Argon2::default();

        let hash = argon2.hash_password(password.as_bytes(), &salt)?;
        Ok(hash.to_string())
    }

    pub fn verify_password(password: &str, hash: &str) -> Result<bool, argon2::password_hash::Error> {
        let parsed_hash = PasswordHash::new(hash)?;
        let argon2 = Argon2::default();

        Ok(argon2.verify_password(password.as_bytes(), &parsed_hash).is_ok())
    }
}
```

### Pattern 4: Distributed Token Storage (Redis)

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-4; sha256=61a66989d9d6ed027d57d4606b70b3205b95cd0d253059a73271222c0c28fe3a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use redis::AsyncCommands;
use serde_json;

struct TokenStore {
    redis: redis::aio::ConnectionManager,
    prefix: String,
}

impl TokenStore {
    pub async fn store_token(
        &mut self,
        user_id: &str,
        token_id: &str,
        claims: &Claims,
        max_concurrent: usize,
    ) -> Result<(), Error> {
        let user_tokens_key = format!("{}:user:{}:tokens", self.prefix, user_id);

        // Check concurrent session limit
        let count: usize = self.redis.scard(&user_tokens_key).await?;
        if count >= max_concurrent {
            // Remove oldest token
            if let Some(old_token) = self.redis.spop::<_, Option<String>>(&user_tokens_key).await? {
                self.redis.del(format!("{}:token:{}", self.prefix, old_token)).await?;
            }
        }

        // Store new token
        let token_key = format!("{}:token:{}", self.prefix, token_id);
        let data = serde_json::to_string(claims)?;
        let ttl = claims.exp - chrono::Utc::now().timestamp() as u64;

        self.redis.set_ex(&token_key, data, ttl as usize).await?;
        self.redis.sadd(&user_tokens_key, token_id).await?;

        Ok(())
    }

    pub async fn revoke_token(&mut self, user_id: &str, token_id: &str) -> Result<(), Error> {
        self.redis.del(format!("{}:token:{}", self.prefix, token_id)).await?;
        self.redis.srem(format!("{}:user:{}:tokens", self.prefix, user_id), token_id).await?;
        Ok(())
    }

    pub async fn revoke_all_tokens(&mut self, user_id: &str) -> Result<(), Error> {
        let user_tokens_key = format!("{}:user:{}:tokens", self.prefix, user_id);
        let tokens: Vec<String> = self.redis.smembers(&user_tokens_key).await?;

        for token_id in tokens {
            self.redis.del(format!("{}:token:{}", self.prefix, token_id)).await?;
        }
        self.redis.del(&user_tokens_key).await?;

        Ok(())
    }
}
```

### Pattern 5: Auth Middleware (Axum)

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-5; sha256=376a194e49a2b17253fbeb69c23d73e54f829f628587b0f1d41b33201b02a3f9 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
use axum::{
    extract::Request,
    middleware::Next,
    response::Response,
    http::StatusCode,
};

pub async fn jwt_auth_middleware(
    mut req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let auth_header = req.headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .ok_or(StatusCode::UNAUTHORIZED)?;

    let token = auth_header
        .strip_prefix("Bearer ")
        .ok_or(StatusCode::UNAUTHORIZED)?;

    let jwt_service = req.extensions()
        .get::<JwtService>()
        .ok_or(StatusCode::INTERNAL_SERVER_ERROR)?;

    let claims = jwt_service
        .verify_token(token)
        .map_err(|_| StatusCode::UNAUTHORIZED)?;

    req.extensions_mut().insert(claims);
    Ok(next.run(req).await)
}
```


## RBAC (Role-Based Access Control)

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-6; sha256=cfe166af57331150cb58fdf685eaa103cb075fd572366240c9e05d62751b9efe -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[derive(Debug, Clone)]
pub enum Permission {
    Read,
    Write,
    Delete,
    Admin,
}

#[derive(Debug, Clone)]
pub struct Role {
    name: String,
    permissions: Vec<Permission>,
}

pub struct RbacService {
    roles: HashMap<String, Role>,
}

impl RbacService {
    pub fn check_permission(&self, user_roles: &[String], required: Permission) -> bool {
        user_roles.iter().any(|role_name| {
            self.roles
                .get(role_name)
                .map(|role| role.permissions.contains(&required))
                .unwrap_or(false)
        })
    }
}
```


## Workflow

### Step 1: Choose Auth Strategy

```
Use case:
  → API/SPA? JWT
  → Service-to-service? API Key or mTLS
  → Traditional web? Session Cookie
  → Third-party login? OAuth 2.0
  → Microservices? mTLS + JWT
```

### Step 2: Implement Securely

```
Security checklist:
  → Strong password hashing (Argon2)
  → Secure token generation (crypto random)
  → HTTPS only in production
  → Validate all inputs
  → Rate limiting on auth endpoints
  → Audit logging
```

### Step 3: Handle Token Lifecycle

```
Token management:
  → Issue: Generate with expiry
  → Refresh: Before expiry
  → Revoke: Blacklist or store state
  → Rotate: Periodic key rotation
```


## Review Checklist

When implementing auth:

- [ ] Passwords hashed with Argon2 (not bcrypt/MD5)
- [ ] JWT tokens have expiration
- [ ] API keys have scope limitations
- [ ] HTTPS enforced in production
- [ ] Rate limiting on login endpoints
- [ ] Audit logging for auth events
- [ ] Token refresh mechanism
- [ ] Secure session storage (Redis with encryption)
- [ ] IP whitelisting for API keys
- [ ] Concurrent session limits


## Verification Commands

```bash
# Test JWT generation
cargo test jwt_generation

# Verify password hashing
cargo test password_hashing

# Check token expiration
cargo test token_expiry

# Load test auth endpoints
wrk -t4 -c100 -d30s http://localhost:3000/auth/login
```


## Common Pitfalls

### 1. Weak Password Hashing

**Symptom**: Fast brute-force attacks

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-7; sha256=a8787b766f652b92b88116675bf8a688bd3e676279b6ede98960da91285a406a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: MD5/SHA256 (too fast)
let hash = format!("{:x}", md5::compute(password));

// ✅ Good: Argon2 (designed for passwords)
let hash = Argon2::default().hash_password(password.as_bytes(), &salt)?;
```

### 2. No Token Expiration

**Symptom**: Stolen tokens valid forever

<!-- huiali-source: skills/rust-auth/SKILL.md#rust-block-8; sha256=bb8df0633d1cff3dfeafdde2a5b21436d9e124ce38bd5376db689c94c4668905 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
// ❌ Bad: no expiration
let claims = Claims { sub: user_id, exp: None };

// ✅ Good: reasonable expiry
let claims = Claims {
    sub: user_id,
    exp: now + 3600, // 1 hour
};
```

### 3. Storing Tokens in LocalStorage

**Symptom**: XSS vulnerability

```javascript
// ❌ Bad: accessible to XSS
localStorage.setItem('token', jwt);

// ✅ Good: HTTP-only cookie
// Set-Cookie: token=...; HttpOnly; Secure; SameSite=Strict
```


## Related Skills

- **rust-web** - Web framework integration
- **rust-middleware** - Middleware patterns
- **rust-cache** - Token storage with Redis
- **rust-error** - Error handling
- **rust-database** - User storage

## Additional unique source examples

These code-only deltas appeared in the condensed English or localized source. They remain fragments, not dependency or hardware claims.

### `SKILL_EN.md` example 1

<!-- huiali-source: skills/rust-auth/SKILL_EN.md#rust-block-1; sha256=3f538fc1053cb3727cff9e43ab46d10cf56e355853043b3a07d8b827050d70ef -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
#[derive(serde::Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
    aud: String,
    iss: String,
}
```

### `SKILL_ZH.md` example 1

<!-- huiali-source: skills/rust-auth/SKILL_ZH.md#rust-block-1; sha256=291ac87d2d915a5bc715f611f2abba023bc709208251c4b74e33fa07a9e0f0c1 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! JWT 认证模块

use jsonwebtoken::{decode, encode, Algorithm, DecodingKey, EncodingKey, Header, Validation};
use serde::{Deserialize, Serialize};
use std::time::{Duration, SystemTime};
use thiserror::Error;

/// JWT 错误类型
#[derive(Error, Debug)]
pub enum JwtError {
    #[error("Token 解析失败: {0}")]
    ParseError(String),
    #[error("Token 验证失败: {0}")]
    ValidationError(String),
    #[error("Token 已过期")]
    Expired,
    #[error("Token 签名无效")]
    InvalidSignature,
}

/// Token 声明（通用结构）
#[derive(Debug, Serialize, Deserialize)]
pub struct Claims {
    pub sub: String,          // 主体标识
    pub name: Option<String>, // 名称
    pub roles: Vec<String>,   // 角色列表
    pub exp: u64,             // 过期时间
    pub iat: u64,             // 签发时间
    // 业务字段可通过扩展字段添加
}

/// JWT 服务
pub struct JwtService {
    encoding_key: EncodingKey,
    decoding_key: DecodingKey,
    secret: String,
    expiry: Duration,
    algorithm: Algorithm,
}

impl JwtService {
    pub fn new(secret: String, expiry_seconds: u64) -> Self {
        Self {
            encoding_key: EncodingKey::from_secret(secret.as_bytes()),
            decoding_key: DecodingKey::from_secret(secret.as_bytes()),
            secret,
            expiry: Duration::from_secs(expiry_seconds),
            algorithm: Algorithm::HS256,
        }
    }

    /// 生成 Token
    pub fn generate_token(&self, subject: &str, roles: &[String]) -> Result<String, JwtError> {
        let now = SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let claims = Claims {
            sub: subject.to_string(),
            name: None,
            roles: roles.to_vec(),
            exp: now + self.expiry.as_secs(),
            iat: now,
        };

        encode(&Header::new(self.algorithm), &claims, &self.encoding_key)
            .map_err(|e| JwtError::ParseError(e.to_string()))
    }

    /// 验证并解析 Token
    pub fn verify_token(&self, token: &str) -> Result<Claims, JwtError> {
        let validation = Validation::new(self.algorithm);

        decode::<Claims>(token, &self.decoding_key, &validation)
            .map(|data| data.claims)
            .map_err(|e| match e.kind() {
                jsonwebtoken::errors::ErrorKind::ExpiredSignature => JwtError::Expired,
                jsonwebtoken::errors::ErrorKind::InvalidSignature => JwtError::InvalidSignature,
                _ => JwtError::ValidationError(e.to_string()),
            })
    }

    /// 检查 Token 是否即将过期（剩余 < 10 分钟返回 true）
    pub fn is_expiring_soon(&self, claims: &Claims) -> bool {
        let now = SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .unwrap()
            .as_secs();
        claims.exp - now < 600
    }
}
```

### `SKILL_ZH.md` example 2

<!-- huiali-source: skills/rust-auth/SKILL_ZH.md#rust-block-2; sha256=8a9f84cd45ad778f90f9331bde01f676d23b83d7ac450ce19efdaf01fc0001c2 -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! API Key 认证模块

use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// API Key 配置
#[derive(Debug, Clone)]
pub struct ApiKeyConfig {
    pub prefix: String,           // Key 前缀
    pub secret: String,           // 签名密钥
    pub expiry_days: i64,         // 有效期
    pub allowed_ips: Vec<String>, // IP 白名单
}

/// API Key 信息
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApiKeyInfo {
    pub key_id: String,
    pub owner_id: String,
    pub secret_hash: String,
    pub created_at: DateTime<Utc>,
    pub expires_at: DateTime<Utc>,
    pub last_used_at: Option<DateTime<Utc>>,
    pub disabled: bool,
    pub scopes: Vec<String>,
}

/// API Key 错误
#[derive(Debug)]
pub enum ApiKeyError {
    InvalidKey,
    KeyExpired,
    KeyRevoked,
    SignatureMismatch,
}

/// API Key 生成器
pub struct ApiKeyGenerator;

impl ApiKeyGenerator {
    /// 生成 API Key
    /// 格式: {prefix}_{key_id}_{signature}
    pub fn generate(config: &ApiKeyConfig, owner_id: &str) -> (String, String) {
        let key_id = Self::generate_key_id();
        let secret = Self::generate_secret();
        let signature = Self::compute_signature(config, &key_id, &secret);

        let api_key = format!("{}_{}_{}", config.prefix, key_id, signature);
        let secret_hash = Self::hash_secret(config, &secret);

        (api_key, secret_hash)
    }

    /// 验证 API Key
    pub async fn verify(
        config: &ApiKeyConfig,
        api_key: &str,
        ip: Option<&str>,
        key_info: &ApiKeyInfo,
    ) -> Result<(), ApiKeyError> {
        let parts: Vec<&str> = api_key.split('_').collect();
        if parts.len() != 3 {
            return Err(ApiKeyError::InvalidKey);
        }

        if key_info.disabled {
            return Err(ApiKeyError::KeyRevoked);
        }

        if key_info.expires_at < Utc::now() {
            return Err(ApiKeyError::KeyExpired);
        }

        if let Some(client_ip) = ip {
            if !config.allowed_ips.is_empty()
                && !config.allowed_ips.contains(&client_ip.to_string()) {
                return Err(ApiKeyError::InvalidKey);
            }
        }

        let expected_signature = Self::compute_signature(config, parts[1], "stored");
        if parts[2] != expected_signature {
            return Err(ApiKeyError::SignatureMismatch);
        }

        Ok(())
    }

    fn generate_key_id() -> String {
        use rand::Rng;
        const CHARSET: &[u8] = b"abcdefghijklmnopqrstuvwxyz0123456789";
        let mut rng = rand::thread_rng();
        (0..16).map(|_| CHARSET[rng.gen_range(0..CHARSET.len())] as char).collect()
    }

    fn generate_secret() -> String {
        use rand::Rng;
        const CHARSET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*";
        let mut rng = rand::thread_rng();
        (0..32).map(|_| CHARSET[rng.gen_range(0..CHARSET.len())] as char).collect()
    }

    fn compute_signature(config: &ApiKeyConfig, key_id: &str, secret: &str) -> String {
        let data = format!("{}{}", key_id, secret);
        let mut hasher = Sha256::new();
        hasher.update(data.as_bytes());
        hasher.update(config.secret.as_bytes());
        format!("{:x}", hasher.finalize())[..8].to_string()
    }

    fn hash_secret(config: &ApiKeyConfig, secret: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(secret.as_bytes());
        hasher.update(config.secret.as_bytes());
        format!("{:x}", hasher.finalize())
    }
}
```

### `SKILL_ZH.md` example 3

<!-- huiali-source: skills/rust-auth/SKILL_ZH.md#rust-block-3; sha256=97b5e6b87bec71397c2689430d3d81e8abee717dafab32d815d286944ff31d1a -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! 分布式 Token 存储

use redis::AsyncCommands;

/// Token 存储配置
#[derive(Debug, Clone)]
pub struct TokenStoreConfig {
    pub redis_url: String,
    pub prefix: String,
}

pub struct TokenStore {
    redis: Option<redis::aio::ConnectionManager>,
    config: TokenStoreConfig,
}

impl TokenStore {
    pub async fn new(config: TokenStoreConfig) -> Result<Self, Box<dyn std::error::Error>> {
        let redis = if config.redis_url.starts_with("redis://") {
            let client = redis::Client::open(config.redis_url.as_str())?;
            let conn = redis::aio::ConnectionManager::new(client).await?;
            Some(conn)
        } else {
            None
        };
        Ok(Self { redis, config })
    }

    /// 存储 Token（带并发控制）
    pub async fn store_token(
        &self,
        user_id: &str,
        token_id: &str,
        claims: &Claims,
        max_concurrent: usize,
    ) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(ref mut redis) = self.redis {
            let prefix = &self.config.prefix;
            let key = format!("{}:tokens:{}", prefix, user_id);

            // 检查并发数量
            let current_count: usize = redis.scard(&key).await?;

            if current_count >= max_concurrent {
                if let Some(old_token) = redis.spop::<String>(&key).await? {
                    redis.del(&format!("{}:token:{}", prefix, old_token)).await?;
                }
            }

            let token_key = format!("{}:token:{}", prefix, token_id);
            let token_data = serde_json::to_string(claims)?;
            let ttl = claims.exp.saturating_sub(86400);
            redis.set_ex(&token_key, token_data, ttl).await?;
            redis.sadd(&key, token_id).await?;
        }
        Ok(())
    }

    /// 撤销 Token
    pub async fn revoke_token(&self, user_id: &str, token_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(ref mut redis) = self.redis {
            let prefix = &self.config.prefix;
            redis.del(&format!("{}:token:{}", prefix, token_id)).await?;
            redis.srem(&format!("{}:tokens:{}", prefix, user_id), token_id).await?;
        }
        Ok(())
    }

    /// 撤销用户所有 Token
    pub async fn revoke_all_tokens(&self, user_id: &str) -> Result<(), Box<dyn std::error::Error>> {
        if let Some(ref mut redis) = self.redis {
            let prefix = &self.config.prefix;
            let set_key = format!("{}:tokens:{}", prefix, user_id);
            let token_ids: Vec<String> = redis.smembers(&set_key).await?;

            for token_id in token_ids {
                redis.del(&format!("{}:token:{}", prefix, token_id)).await?;
            }
            redis.del(&set_key).await?;
        }
        Ok(())
    }
}
```

### `SKILL_ZH.md` example 4

<!-- huiali-source: skills/rust-auth/SKILL_ZH.md#rust-block-4; sha256=5d082aa1e4e17d6cf764ff918f7eec309fa20caaf4ba349a359f04eadfb35f0d -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! 认证中间件

use actix_web::{
    dev::{forward_ready, Service, ServiceRequest, ServiceResponse, Transform},
    Error, HttpMessage,
};
use futures::future::{ready, LocalBoxFuture, Ready};
use std::rc::Rc;

pub struct JwtAuthentication;

impl<S, B> Transform<S, ServiceRequest> for JwtAuthentication
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type InitError = ();
    type Transform = JwtAuthMiddleware<S>;
    type Future = Ready<Result<Self::Transform, Self::InitError>>;

    fn new_transform(&self, service: S) -> Self::Future {
        ready(Ok(JwtAuthMiddleware { service: Rc::new(service) }))
    }
}

pub struct JwtAuthMiddleware<S> {
    service: Rc<S>,
}

impl<S, B> Service<ServiceRequest> for JwtAuthMiddleware<S>
where
    S: Service<ServiceRequest, Response = ServiceResponse<B>, Error = Error> + 'static,
    S::Future: 'static,
    B: 'static,
{
    type Response = ServiceResponse<B>;
    type Error = Error;
    type Future = LocalBoxFuture<'static, Result<Self::Response, Self::Error>>;

    forward_ready!(service);

    fn call(&self, req: ServiceRequest) -> Self::Future {
        let service = Rc::clone(&self.service);

        Box::pin(async move {
            let auth_header = req.headers()
                .get("Authorization")
                .and_then(|v| v.to_str().ok());

            let token = match auth_header {
                Some(header) if header.starts_with("Bearer ") => &header[7..],
                _ => return Err(actix_web::error::ErrorUnauthorized("Invalid Authorization")),
            };

            let jwt_service = req.app_data::<JwtService>()
                .ok_or(actix_web::error::ErrorInternalServerError("JWT not configured"))?;

            let claims = jwt_service.verify_token(token)
                .map_err(|_| actix_web::error::ErrorUnauthorized("Invalid token"))?;

            req.extensions_mut().insert(claims);
            service.call(req).await
        })
    }
}
```

### `SKILL_ZH.md` example 5

<!-- huiali-source: skills/rust-auth/SKILL_ZH.md#rust-block-5; sha256=7883adecb6c41089a5d73c4499942485355411ec6381fc1f7c6feb69b582cbdd -->
<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! 密码安全存储

use argon2::{self, Config};
use rand::Rng;

/// 密码哈希服务
pub struct PasswordHasher;

impl PasswordHasher {
    /// 哈希密码
    pub fn hash_password(password: &str) -> Result<String, argon2::Error> {
        let salt = rand::thread_rng().gen::<[u8; 32]>();
        let config = Config::default();

        argon2::hash_raw(password.as_bytes(), &salt, &config)
            .map(|bytes| {
                let salt_b64 = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, &salt);
                let hash_b64 = base64::Engine::encode(&base64::engine::general_purpose::STANDARD, &bytes);
                format!("$argon2id$v=19,m=4096,t=3,p=1${}${}$", salt_b64, hash_b64)
            })
    }

    /// 验证密码
    pub fn verify_password(password: &str, stored_hash: &str) -> Result<bool, argon2::Error> {
        use subtle::ConstantTimeEq;

        let parts: Vec<&str> = stored_hash.split('$').collect();
        if parts.len() != 5 { return Ok(false); }

        let salt = base64::Engine::decode(&base64::engine::general_purpose::STANDARD, parts[2]).unwrap_or_default();
        let stored = base64::Engine::decode(&base64::engine::general_purpose::STANDARD, parts[3]).unwrap_or_default();

        let config = Config::default();
        let computed = argon2::hash_raw(password.as_bytes(), &salt, &config)?;

        Ok(computed.as_slice().ct_eq(&stored))
    }
}
```
