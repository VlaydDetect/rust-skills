//! The caller-visible API a boilerplate macro would have to generate.

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct User { name: String, active: bool }

impl User {
    pub fn new(name: impl Into<String>) -> Result<Self, &'static str> {
        let name = name.into();
        if name.trim().is_empty() { return Err("name is empty"); }
        Ok(Self { name, active: true })
    }
    pub fn name(&self) -> &str { &self.name }
    pub fn is_active(&self) -> bool { self.active }
    pub fn deactivate(&mut self) { self.active = false; }
}

#[cfg(test)]
mod tests {
    #[test]
    fn generated_surface_must_preserve_invariants() {
        assert!(super::User::new(" ").is_err());
        let mut user = super::User::new("Ada").unwrap();
        user.deactivate();
        assert_eq!((user.name(), user.is_active()), ("Ada", false));
    }
}
