pub fn label(value: &str) -> String { format!("item:{}", golden_domain::normalize(value)) }

#[cfg(test)]
mod tests { #[test] fn dependency_points_to_domain() { assert_eq!(super::label(" Rust "), "item:rust"); } }
