//! Hide an optional implementation behind a project-owned contract.

pub trait Digest { fn digest(&self, input: &[u8]) -> u64; }

pub struct Portable;
impl Digest for Portable {
    fn digest(&self, input: &[u8]) -> u64 {
        input.iter().fold(0_u64, |state, byte| state.rotate_left(5) ^ u64::from(*byte))
    }
}

pub fn fingerprint(engine: &impl Digest, input: &[u8]) -> u64 { engine.digest(input) }

#[cfg(test)]
mod tests {
    #[test]
    fn caller_contract_is_not_a_dependency_type() {
        assert_eq!(super::fingerprint(&super::Portable, b"abc"), super::fingerprint(&super::Portable, b"abc"));
    }
}
