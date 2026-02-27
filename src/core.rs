//! Core types for S-entropy space representation

use serde::{Deserialize, Serialize};
use std::fmt;

/// S-entropy point in [0,1]³ space
///
/// Represents a program's position in the partition hierarchy:
/// - S_k: Knowledge entropy (operation type)
/// - S_t: Temporal entropy (composition depth)
/// - S_e: Evolution entropy (implementation complexity)
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct SPoint {
    pub s_k: f64,
    pub s_t: f64,
    pub s_e: f64,
}

impl SPoint {
    /// Create new S-point with validation
    pub fn new(s_k: f64, s_t: f64, s_e: f64) -> Result<Self, &'static str> {
        if !Self::is_valid_coordinate(s_k) {
            return Err("s_k must be in [0, 1]");
        }
        if !Self::is_valid_coordinate(s_t) {
            return Err("s_t must be in [0, 1]");
        }
        if !Self::is_valid_coordinate(s_e) {
            return Err("s_e must be in [0, 1]");
        }

        Ok(Self { s_k, s_t, s_e })
    }

    /// Create new S-point without validation (for known-safe values)
    pub const fn new_unchecked(s_k: f64, s_t: f64, s_e: f64) -> Self {
        Self { s_k, s_t, s_e }
    }

    /// Check if coordinate is valid (in [0, 1])
    #[inline]
    fn is_valid_coordinate(val: f64) -> bool {
        val >= 0.0 && val <= 1.0 && val.is_finite()
    }

    /// Compute Euclidean distance to another point
    pub fn distance_to(&self, other: &SPoint) -> f64 {
        let dk = self.s_k - other.s_k;
        let dt = self.s_t - other.s_t;
        let de = self.s_e - other.s_e;
        (dk * dk + dt * dt + de * de).sqrt()
    }

    /// Manhattan distance (L1 norm)
    pub fn manhattan_distance(&self, other: &SPoint) -> f64 {
        (self.s_k - other.s_k).abs() +
        (self.s_t - other.s_t).abs() +
        (self.s_e - other.s_e).abs()
    }

    /// Total entropy (sum of coordinates)
    pub fn total_entropy(&self) -> f64 {
        self.s_k + self.s_t + self.s_e
    }

    /// Check if point is within distance threshold of another
    pub fn is_similar(&self, other: &SPoint, threshold: f64) -> bool {
        self.distance_to(other) < threshold
    }
}

impl fmt::Display for SPoint {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "({:.4}, {:.4}, {:.4})", self.s_k, self.s_t, self.s_e)
    }
}

/// Program operation type categories
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum OperationType {
    /// List → Scalar: sum, product, max, min, mean, length, range
    Aggregation,
    /// List → Scalar: first, last, second, nth
    Access,
    /// List → List: map, filter, sort, reverse
    Transformation,
    /// Scalars → Scalar: add, subtract, multiply, divide
    Arithmetic,
    /// Comparison/branching: max_of_two, abs, sign
    Conditional,
    /// Nested operations: sum_of_squares, filter_then_sum
    Composition,
    /// Self-referential: factorial, fibonacci
    Recursive,
}

impl OperationType {
    /// Get the S_k range for this operation type
    pub fn s_k_range(&self) -> (f64, f64) {
        match self {
            Self::Aggregation => (0.01, 0.10),
            Self::Access => (0.16, 0.20),
            Self::Transformation => (0.31, 0.42),
            Self::Arithmetic => (0.51, 0.56),
            Self::Conditional => (0.61, 0.66),
            Self::Composition => (0.71, 0.76),
            Self::Recursive => (0.86, 0.88),
        }
    }

    /// Get base S_k coordinate for this type
    pub fn base_s_k(&self) -> f64 {
        self.s_k_range().0
    }

    /// Check if S_k coordinate matches this operation type
    pub fn matches_s_k(&self, s_k: f64) -> bool {
        let (min, max) = self.s_k_range();
        s_k >= min && s_k <= max
    }
}

impl fmt::Display for OperationType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Self::Aggregation => write!(f, "aggregation"),
            Self::Access => write!(f, "access"),
            Self::Transformation => write!(f, "transformation"),
            Self::Arithmetic => write!(f, "arithmetic"),
            Self::Conditional => write!(f, "conditional"),
            Self::Composition => write!(f, "composition"),
            Self::Recursive => write!(f, "recursive"),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spoint_creation() {
        let p = SPoint::new(0.5, 0.5, 0.5).unwrap();
        assert_eq!(p.s_k, 0.5);
        assert_eq!(p.s_t, 0.5);
        assert_eq!(p.s_e, 0.5);
    }

    #[test]
    fn test_spoint_validation() {
        assert!(SPoint::new(-0.1, 0.5, 0.5).is_err());
        assert!(SPoint::new(0.5, 1.1, 0.5).is_err());
        assert!(SPoint::new(0.5, 0.5, f64::NAN).is_err());
    }

    #[test]
    fn test_distance() {
        let p1 = SPoint::new_unchecked(0.0, 0.0, 0.0);
        let p2 = SPoint::new_unchecked(1.0, 0.0, 0.0);
        assert_eq!(p1.distance_to(&p2), 1.0);

        let p3 = SPoint::new_unchecked(0.0, 1.0, 1.0);
        let dist = p1.distance_to(&p3);
        assert!((dist - 2.0_f64.sqrt()).abs() < 1e-10);
    }

    #[test]
    fn test_operation_type_ranges() {
        assert!(OperationType::Aggregation.matches_s_k(0.05));
        assert!(!OperationType::Aggregation.matches_s_k(0.15));
        assert!(OperationType::Recursive.matches_s_k(0.87));
    }
}
