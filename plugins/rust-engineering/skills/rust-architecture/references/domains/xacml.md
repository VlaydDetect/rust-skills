# Specialized Rust Xacml Protocol

> Apply this topic through the owning profile. Product routing and current-project constraints override generic preferences.

## Product routing and baseline

- Primary owner: `$rust-architecture`.
- Supporting profiles when needed: `$rust-api-design`, `$rust-errors`.
- Scope retained: Policy decision and enforcement boundaries, attribute modelling, combining algorithms, obligations, versioning, and auditability.
- Baseline correction: Treat XACML as a domain constraint map, not a framework default. Confirm policy semantics, trust boundaries, and interoperability requirements before designing types.
- The repository's actual MSRV, Edition, target, Cargo resolution, dependency versions, and user contract take precedence. Rust 1.98, Edition 2024, and resolver 3 are product reference defaults, not forced project upgrades.

## Workflow

## Core Patterns

### 1. Policy Evaluator<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! Policy evaluator

use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Request context
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RequestContext {
    pub subject: Subject,      // Subject
    pub resource: Resource,    // Resource
    pub action: String,        // Action
    pub environment: HashMap<String, String>,  // Environment
}

/// Subject
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Subject {
    pub id: String,
    pub roles: Vec<String>,
    pub attributes: HashMap<String, String>,
}

/// Resource
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Resource {
    pub id: String,
    pub r#type: String,
    pub attributes: HashMap<String, String>,
}

/// Decision result
#[derive(Debug, Clone, PartialEq)]
pub enum Decision {
    Permit,
    Deny,
    NotApplicable,
    Indeterminate(String),
}

/// Policy definition
#[derive(Debug, Clone)]
pub struct Policy {
    pub id: String,
    pub target: PolicyTarget,
    pub rules: Vec<Rule>,
    pub combining_algorithm: CombiningAlgorithm,
}

/// Policy target (matching conditions)
#[)]
pub struct PolicyTarget {
    pubderive(Debug, Clone subjects: Vec<Vec<String>>,  // Role combinations
    pub resources: Vec<String>,
    pub actions: Vec<String>,
}

/// Access rule
#[derive(Debug, Clone)]
pub struct Rule {
    pub id: String,
    pub effect: RuleEffect,
    pub condition: Option<Box<dyn Fn(&RequestContext) -> bool + Send>>,
}

#[derive(Debug, Clone, Copy)]
pub enum RuleEffect {
    Permit,
    Deny,
}

/// Policy-combining algorithm
#[derive(Debug, Clone, Copy)]
pub enum CombiningAlgorithm {
    DenyOverrides,      // Deny takes precedence
    PermitOverrides,    // Permit takes precedence
    FirstApplicable,    // First applicable policy
    OnlyOneApplicable,  // Exactly one applicable policy
}

/// Policy evaluator
pub struct PolicyEvaluator {
    policies: Vec<Policy>,
}

impl PolicyEvaluator {
    pub fn new(policies: Vec<Policy>) -> Self {
        Self { policies }
    }

    /// Evaluate a request
    pub fn evaluate(&self, context: &RequestContext) -> Decision {
        let mut applicable_policies: Vec<&Policy> = self.policies
            .iter()
            .filter(|p| self.is_target_matched(p, context))
            .collect();

        if applicable_policies.is_empty() {
            return Decision::NotApplicable;
        }

        // Compute the final decision using the combining algorithm
        match applicable_policies.first().map(|p| p.combining_algorithm).unwrap_or(CombiningAlgorithm::FirstApplicable) {
            CombiningAlgorithm::DenyOverrides => self.deny_overrides(&applicable_policies, context),
            CombiningAlgorithm::PermitOverrides => self.permit_overrides(&applicable_policies, context),
            CombiningAlgorithm::FirstApplicable => self.first_applicable(&applicable_policies, context),
            CombiningAlgorithm::OnlyOneApplicable => {
                if applicable_policies.len() == 1 {
                    self.evaluate_policy(applicable_policies[0], context)
                } else {
                    Decision::Indeterminate("Multiple applicable policies".to_string())
                }
            }
        }
    }

    fn is_target_matched(&self, policy: &Policy, context: &RequestContext) -> bool {
        // Check subjects
        let subject_matches = policy.target.subjects.is_empty() ||
            policy.target.subjects.iter().any(|roles| {
                roles.iter().all(|r| context.subject.roles.contains(r))
            });

        // Check resources
        let resource_matches = policy.target.resources.is_empty() ||
            policy.target.resources.contains(&context.resource.r#type);

        // Check actions
        let action_matches = policy.target.actions.is_empty() ||
            policy.target.actions.contains(&context.action);

        subject_matches && resource_matches && action_matches
    }

    fn deny_overrides(&self, policies: &[&Policy], context: &RequestContext) -> Decision {
        let mut has_error = false;
        let mut error_msg = String::new();

        for policy in policies {
            match self.evaluate_policy(policy, context) {
                Decision::Deny => return Decision::Deny,
                Decision::Indeterminate(msg) => {
                    has_error = true;
                    error_msg = msg;
                }
                _ => {}
            }
        }

        if has_error {
            Decision::Indeterminate(error_msg)
        } else {
            Decision::Permit
        }
    }

    fn permit_overrides(&self, policies: &[&Policy], context: &RequestContext) -> Decision {
        let mut has_error = false;
        let mut error_msg = String::new();

        for policy in policies {
            match self.evaluate_policy(policy, context) {
                Decision::Permit => return Decision::Permit,
                Decision::Indeterminate(msg) => {
                    has_error = true;
                    error_msg = msg;
                }
                _ => {}
            }
        }

        if has_error {
            Decision::Indeterminate(error_msg)
        } else {
            Decision::Deny
        }
    }

    fn first_applicable(&self, policies: &[&Policy], context: &RequestContext) -> Decision {
        for policy in policies {
            let decision = self.evaluate_policy(policy, context);
            if decision != Decision::NotApplicable {
                return decision;
            }
        }
        Decision::Deny
    }

    fn evaluate_policy(&self, policy: &Policy, context: &RequestContext) -> Decision {
        for rule in &policy.rules {
            if let Some(ref condition) = rule.condition {
                if !condition(context) {
                    continue;
                }
            }
            return match rule.effect {
                RuleEffect::Permit => Decision::Permit,
                RuleEffect::Deny => Decision::Deny,
            };
        }
        Decision::NotApplicable
    }
}
```

### 2. RBAC Permission Checking<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! RBAC permission checking

use std::collections::HashMap;

/// RBAC configuration
#[derive(Debug, Clone)]
pub struct RbacConfig {
    /// Role hierarchy
    pub role_hierarchy: HashMap<String, Vec<String>>,
    /// Role-to-permission mapping
    pub role_permissions: HashMap<String, Vec<String>>,
    /// Permission definitions
    pub permissions: HashMap<String, PermissionDef>,
}

/// Permission definition
#[derive(Debug, Clone)]
pub struct PermissionDef {
    pub resource: String,
    pub actions: Vec<String>,
}

/// RBAC checker
pub struct RbacChecker {
    config: RbacConfig,
}

impl RbacChecker {
    pub fn new(config: RbacConfig) -> Self {
        Self { config }
    }

    /// Check whether a user has permission
    pub fn check_permission(
        &self,
        user_roles: &[String],
        resource: &str,
        action: &str,
    ) -> bool {
        // Get all inherited roles
        let all_roles = self.expand_roles(user_roles);

        // Check for permission
        for role in &all_roles {
            if let Some(perms) = self.config.role_permissions.get(role) {
                for perm_id in perms {
                    if let Some(perm) = self.config.permissions.get(perm_id) {
                        if perm.resource == resource && perm.actions.contains(&action) {
                            return true;
                        }
                    }
                }
            }
        }

        false
    }

    /// Expand the role hierarchy
    fn expand_roles(&self, roles: &[String]) -> Vec<String> {
        let mut expanded = Vec::new();
        let mut visited = std::collections::HashSet::new();
        let mut queue = Vec::new();

        for role in roles {
            if !visited.contains(role) {
                queue.push(role.clone());
                visited.insert(role.clone());
            }
        }

        while let Some(role) = queue.pop() {
            expanded.push(role.clone());

            if let Some(parents) = self.config.role_hierarchy.get(&role) {
                for parent in parents {
                    if !visited.contains(parent) {
                        visited.insert(parent.clone());
                        queue.push(parent.clone());
                    }
                }
            }
        }

        expanded
    }

    /// Get all permissions for a user
    pub fn get_user_permissions(&self, user_roles: &[String]) -> Vec<String> {
        let all_roles = self.expand_roles(user_roles);
        let mut permissions = std::collections::HashSet::new();

        for role in &all_roles {
            if let Some(role_perms) = self.config.role_permissions.get(role) {
                for perm in role_perms {
                    permissions.insert(perm.clone());
                }
            }
        }

        permissions.into_iter().collect()
    }
}
```

### 3. Policy Cache<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! Policy cache

use crate::{Policy, PolicyEvaluator};
use std::sync::Arc;
use tokio::sync::RwLock;
use std::time::{Duration, Instant};

/// Cache configuration
#[derive(Debug, Clone)]
pub struct PolicyCacheConfig {
    pub ttl: Duration,
    pub max_size: usize,
}

/// Cache entry
struct CacheEntry {
    policy: Policy,
    inserted_at: Instant,
}

/// Policy cache
pub struct PolicyCache {
    config: PolicyCacheConfig,
    cache: Arc<RwLock<HashMap<String, CacheEntry>>>,
}

impl PolicyCache {
    pub fn new(config: PolicyCacheConfig) -> Self {
        Self {
            config,
            cache: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Get a policy
    pub async fn get(&self, policy_id: &str) -> Option<Policy> {
        let cache = self.cache.read().await;
        cache.get(policy_id).map(|entry| entry.policy.clone())
    }

    /// Store a policy
    pub async fn set(&self, policy: Policy) {
        let mut cache = self.cache.write().await;

        // Remove expired entries
        let now = Instant::now();
        cache.retain(|_, v| now.duration_since(v.inserted_at) < self.config.ttl);

        // Remove entries beyond the size limit
        if cache.len() >= self.config.max_size {
            let to_remove = cache.len() - self.config.max_size + 1;
            let keys: Vec<String> = cache.keys().take(to_remove).cloned().collect();
            for key in keys {
                cache.remove(&key);
            }
        }

        cache.insert(policy.id.clone(), CacheEntry {
            policy,
            inserted_at: Instant::now(),
        });
    }

    /// Invalidate a policy
    pub async fn invalidate(&self, policy_id: &str) {
        let mut cache = self.cache.write().await;
        cache.remove(policy_id);
    }

    /// Clear all policies
    pub async fn clear(&self) {
        let mut cache = self.cache.write().await;
        cache.clear();
    }
}
```


## Best Practices

### 1. Policy-Definition DSL<!-- rust-example: fragment; missing: surrounding project types, dependencies, target, and verification harness -->
```rust
//! Policy builder

use crate::{Policy, PolicyTarget, Rule, RuleEffect, CombiningAlgorithm};

/// Policy builder
pub struct PolicyBuilder {
    policy: Policy,
}

impl PolicyBuilder {
    pub fn new(id: &str) -> Self {
        Self {
            policy: Policy {
                id: id.to_string(),
                target: PolicyTarget {
                    subjects: Vec::new(),
                    resources: Vec::new(),
                    actions: Vec::new(),
                },
                rules: Vec::new(),
                combining_algorithm: CombiningAlgorithm::DenyOverrides,
            },
        }
    }

    pub fn with_subject_roles(mut self, roles: &[&str]) -> Self {
        self.policy.target.subjects = vec![roles.iter().map(|s| s.to_string()).collect()];
        self
    }

    pub fn with_resource(mut self, resource: &str) -> Self {
        self.policy.target.resources = vec![resource.to_string()];
        self
    }

    pub fn with_action(mut self, action: &str) -> Self {
        self.policy.target.actions = vec![action.to_string()];
        self
    }

    pub fn add_rule(
        mut self,
        id: &str,
        effect: RuleEffect,
        condition: impl Fn(&crate::RequestContext) -> bool + Send + 'static,
    ) -> Self {
        self.policy.rules.push(Rule {
            id: id.to_string(),
            effect,
            condition: Some(Box::new(condition)),
        });
        self
    }

    pub fn with_combining_algorithm(mut self, algo: CombiningAlgorithm) -> Self {
        self.policy.combining_algorithm = algo;
        self
    }

    pub fn build(self) -> Policy {
        self.policy
    }
}

/// Usage example
fn example_policy() -> Policy {
    PolicyBuilder::new("read-policy")
        .with_subject_roles(&["user", "admin"])
        .with_resource("document")
        .with_action("read")
        .add_rule("own-document", RuleEffect::Permit, |ctx| {
            // A subject may read a document it created
            ctx.resource.attributes.get("owner") == Some(&ctx.subject.id)
        })
        .add_rule("public-document", RuleEffect::Permit, |ctx| {
            // Public documents may be read
            ctx.resource.attributes.get("visibility") == Some(&"public".to_string())
        })
        .with_combining_algorithm(CombiningAlgorithm::DenyOverrides)
        .build()
}
```


## Common Problems

| Problem | Cause | Solution |
|-----|------|---------|
| Inconsistent decisions | Incorrect combining algorithm | Choose an algorithm appropriate to the domain |
| Poor performance | Too many policies | Use caching and indexing |
| Authorization bypass | Incorrect rule order | Give DenyOverrides precedence |


## Related Skills

- `rust-auth` - Authentication and authorization
- `rust-web` - Web integration
- `rust-cache` - Policy caching
- `rust-performance` - Performance optimization
