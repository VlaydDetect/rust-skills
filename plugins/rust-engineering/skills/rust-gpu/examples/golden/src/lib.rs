//! Backend-neutral GPU batch planning from explicit budgets.

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct BatchPlan {
    pub items: usize,
    pub transfer_bytes: usize,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PlanError {
    ZeroItemSize,
    NoCapacity,
    Overflow,
}

pub fn plan_batch(
    requested: usize,
    bytes_per_item: usize,
    resident_budget: usize,
    transfer_budget: usize,
) -> Result<BatchPlan, PlanError> {
    if bytes_per_item == 0 {
        return Err(PlanError::ZeroItemSize);
    }
    let capacity = (resident_budget / bytes_per_item).min(transfer_budget / bytes_per_item);
    let items = requested.min(capacity);
    if items == 0 {
        return Err(PlanError::NoCapacity);
    }
    let transfer_bytes = items.checked_mul(bytes_per_item).ok_or(PlanError::Overflow)?;
    Ok(BatchPlan { items, transfer_bytes })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn the_tightest_explicit_budget_limits_the_batch() {
        let plan = plan_batch(64, 256, 64 * 256, 12 * 256).unwrap();
        assert_eq!(plan, BatchPlan { items: 12, transfer_bytes: 3072 });
    }

    #[test]
    fn absent_capacity_is_not_reported_as_gpu_execution() {
        assert_eq!(plan_batch(8, 256, 128, 4096), Err(PlanError::NoCapacity));
    }
}

