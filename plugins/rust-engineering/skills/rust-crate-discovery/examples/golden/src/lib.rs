//! A comparable rubric: hard gates first, then weighted evidence.

#[derive(Clone, Copy)]
pub struct Candidate {
    pub supports_msrv: bool,
    pub license_allowed: bool,
    pub api_fit: u8,
    pub maintenance: u8,
    pub dependency_cost: u8,
}

pub fn score(candidate: Candidate) -> Option<u16> {
    if !candidate.supports_msrv || !candidate.license_allowed { return None; }
    Some(u16::from(candidate.api_fit) * 5
        + u16::from(candidate.maintenance) * 3
        + u16::from(10 - candidate.dependency_cost.min(10)) * 2)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn a_hard_gate_cannot_be_outvoted() {
        let candidate = Candidate { supports_msrv: false, license_allowed: true, api_fit: 10, maintenance: 10, dependency_cost: 0 };
        assert_eq!(score(candidate), None);
    }
}
