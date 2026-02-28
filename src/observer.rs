//! Observer: Extract S-coordinates from I/O examples

use crate::core::{SPoint, OperationType};
use crate::error::{Result, SynthesisError};
use serde::{Deserialize, Serialize};

/// Value types that can appear in examples
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum ExampleValue {
    Scalar(i64),
    Float(f64),
    List(Vec<i64>),
    Tuple(Vec<i64>),
}

impl ExampleValue {
    pub fn is_scalar(&self) -> bool {
        matches!(self, ExampleValue::Scalar(_) | ExampleValue::Float(_))
    }

    pub fn is_list(&self) -> bool {
        matches!(self, ExampleValue::List(_))
    }

    pub fn as_scalar(&self) -> Option<i64> {
        match self {
            ExampleValue::Scalar(v) => Some(*v),
            _ => None,
        }
    }

    pub fn as_list(&self) -> Option<&[i64]> {
        match self {
            ExampleValue::List(v) => Some(v),
            _ => None,
        }
    }
}

/// A single input-output example
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Example {
    pub input: ExampleValue,
    pub output: ExampleValue,
}

impl Example {
    pub fn new(input: ExampleValue, output: ExampleValue) -> Self {
        Self { input, output }
    }

    pub fn new_scalar_list(input: Vec<i64>, output: i64) -> Self {
        Self {
            input: ExampleValue::List(input),
            output: ExampleValue::Scalar(output),
        }
    }

    pub fn new_list_list(input: Vec<i64>, output: Vec<i64>) -> Self {
        Self {
            input: ExampleValue::List(input),
            output: ExampleValue::List(output),
        }
    }
}

/// Observer extracts S-entropy coordinates from example sets
pub struct Observer {
    // Configuration could go here
}

impl Observer {
    pub fn new() -> Self {
        Self {}
    }

    /// Extract S-coordinates from examples
    pub fn observe(&self, examples: &[Example]) -> Result<SPoint> {
        if examples.is_empty() {
            return Err(SynthesisError::EmptyExamples);
        }

        // Analyze pattern
        let pattern = self.analyze_pattern(examples)?;

        // Compute coordinates
        let s_k = self.compute_s_k(&pattern);
        let s_t = self.compute_s_t(&pattern);
        let s_e = self.compute_s_e(&pattern);

        SPoint::new(s_k, s_t, s_e)
            .map_err(|e| SynthesisError::InvalidCoordinate(e.to_string()))
    }

    /// Analyze examples to determine pattern
    fn analyze_pattern(&self, examples: &[Example]) -> Result<Pattern> {
        // Determine arity
        let arity = self.infer_arity(examples)?;

        // Determine operation type
        let op_type = self.infer_operation_type(examples)?;

        // Infer specific relationship
        let relationship = self.infer_relationship(examples)?;

        // Estimate complexity
        let composition_depth = self.estimate_composition_depth(&relationship);
        let complexity_score = self.estimate_complexity(&relationship);

        Ok(Pattern {
            arity,
            op_type,
            relationship,
            composition_depth,
            complexity_score,
        })
    }

    fn infer_arity(&self, examples: &[Example]) -> Result<usize> {
        let first = &examples[0];

        Ok(match &first.input {
            ExampleValue::List(_) => 1,
            ExampleValue::Tuple(t) => t.len(),
            ExampleValue::Scalar(_) | ExampleValue::Float(_) => 1,
        })
    }

    fn infer_operation_type(&self, examples: &[Example]) -> Result<OperationType> {
        let first = &examples[0];

        let input_is_list = first.input.is_list();
        let output_is_scalar = first.output.is_scalar();
        let output_is_list = first.output.is_list();

        Ok(if input_is_list && output_is_scalar {
            // Could be aggregation or access
            if self.is_aggregation_pattern(examples) {
                OperationType::Aggregation
            } else {
                OperationType::Access
            }
        } else if input_is_list && output_is_list {
            OperationType::Transformation
        } else if !input_is_list && output_is_scalar {
            OperationType::Arithmetic
        } else {
            OperationType::Aggregation // Default
        })
    }

    fn is_aggregation_pattern(&self, examples: &[Example]) -> bool {
        // Aggregations typically transform the entire list
        // Access operations just extract elements
        for ex in examples {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                // If output equals first/last element, likely access not aggregation
                if !inp.is_empty() && (out == inp[0] || out == inp[inp.len() - 1]) {
                    return false;
                }
            }
        }
        true
    }

    fn infer_relationship(&self, examples: &[Example]) -> Result<String> {
        // Try to match known patterns
        if self.matches_sum(examples) {
            return Ok("sum".to_string());
        }
        if self.matches_product(examples) {
            return Ok("product".to_string());
        }
        if self.matches_max(examples) {
            return Ok("max".to_string());
        }
        if self.matches_min(examples) {
            return Ok("min".to_string());
        }
        if self.matches_length(examples) {
            return Ok("length".to_string());
        }
        if self.matches_first(examples) {
            return Ok("first".to_string());
        }
        if self.matches_last(examples) {
            return Ok("last".to_string());
        }
        if self.matches_double_all(examples) {
            return Ok("double_all".to_string());
        }
        if self.matches_square_all(examples) {
            return Ok("square_all".to_string());
        }

        Ok("unknown".to_string())
    }

    // Pattern matching functions
    fn matches_sum(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.iter().sum::<i64>() == out
            } else {
                false
            }
        })
    }

    fn matches_product(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.iter().product::<i64>() == out
            } else {
                false
            }
        })
    }

    fn matches_max(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.iter().max().copied() == Some(out)
            } else {
                false
            }
        })
    }

    fn matches_min(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.iter().min().copied() == Some(out)
            } else {
                false
            }
        })
    }

    fn matches_length(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.len() as i64 == out
            } else {
                false
            }
        })
    }

    fn matches_first(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.first().copied() == Some(out)
            } else {
                false
            }
        })
    }

    fn matches_last(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let (Some(inp), Some(out)) = (ex.input.as_list(), ex.output.as_scalar()) {
                inp.last().copied() == Some(out)
            } else {
                false
            }
        })
    }

    fn matches_double_all(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let ExampleValue::List(inp) = &ex.input {
                if let ExampleValue::List(out) = &ex.output {
                    return inp.iter().map(|&x| x * 2).collect::<Vec<_>>() == *out;
                }
            }
            false
        })
    }

    fn matches_square_all(&self, examples: &[Example]) -> bool {
        examples.iter().all(|ex| {
            if let ExampleValue::List(inp) = &ex.input {
                if let ExampleValue::List(out) = &ex.output {
                    return inp.iter().map(|&x| x * x).collect::<Vec<_>>() == *out;
                }
            }
            false
        })
    }

    fn estimate_composition_depth(&self, relationship: &str) -> usize {
        match relationship {
            "sum_of_squares" | "sum_of_doubled" => 2,
            "factorial" | "fibonacci" => 3,
            _ => 1,
        }
    }

    fn estimate_complexity(&self, relationship: &str) -> f64 {
        match relationship {
            "first" | "last" | "length" => 0.2,
            "sum" | "product" | "max" | "min" => 0.3,
            "factorial" | "fibonacci" => 0.7,
            _ => 0.5,
        }
    }

    /// Compute S_k from pattern
    fn compute_s_k(&self, pattern: &Pattern) -> f64 {
        RELATIONSHIP_SK_MAP
            .iter()
            .find(|(name, _)| *name == pattern.relationship.as_str())
            .map(|(_, sk)| *sk)
            .unwrap_or(0.5)
    }

    /// Compute S_t from pattern
    fn compute_s_t(&self, pattern: &Pattern) -> f64 {
        RELATIONSHIP_ST_MAP
            .iter()
            .find(|(name, _)| *name == pattern.relationship.as_str())
            .map(|(_, st)| *st)
            .unwrap_or(0.2)
    }

    /// Compute S_e from pattern
    fn compute_s_e(&self, pattern: &Pattern) -> f64 {
        RELATIONSHIP_SE_MAP
            .iter()
            .find(|(name, _)| *name == pattern.relationship.as_str())
            .map(|(_, se)| *se)
            .unwrap_or(0.3)
    }
}

impl Default for Observer {
    fn default() -> Self {
        Self::new()
    }
}

/// Pattern extracted from examples
#[derive(Debug)]
struct Pattern {
    arity: usize,
    op_type: OperationType,
    relationship: String,
    composition_depth: usize,
    complexity_score: f64,
}

// S_k mappings (from validated Python implementation)
const RELATIONSHIP_SK_MAP: &[(&str, f64)] = &[
    // Aggregation
    ("sum", 0.01),
    ("product", 0.02),
    ("max", 0.03),
    ("min", 0.04),
    ("mean", 0.05),
    ("length", 0.06),
    // Access
    ("first", 0.16),
    ("last", 0.17),
    ("second", 0.18),
    // Transformation
    ("double_all", 0.31),
    ("square_all", 0.32),
    ("negate_all", 0.33),
    ("filter_positive", 0.36),
    ("filter_even", 0.38),
    ("reverse", 0.40),
    ("sort_asc", 0.41),
    ("sort_desc", 0.42),
    // Arithmetic
    ("add", 0.51),
    ("subtract", 0.52),
    ("multiply", 0.53),
    ("divide", 0.54),
    // Conditional
    ("max_of_two", 0.61),
    ("min_of_two", 0.62),
    // Composition
    ("sum_of_squares", 0.71),
    ("sum_of_doubled", 0.72),
    // Recursive
    ("factorial", 0.86),
    ("fibonacci", 0.87),
];

// S_t mappings
const RELATIONSHIP_ST_MAP: &[(&str, f64)] = &[
    ("sum", 0.10),
    ("product", 0.10),
    ("max", 0.10),
    ("min", 0.10),
    ("length", 0.10),
    ("first", 0.10),
    ("last", 0.10),
    ("mean", 0.15),
    ("double_all", 0.20),
    ("square_all", 0.20),
    ("sum_of_squares", 0.35),
    ("sum_of_doubled", 0.35),
    ("factorial", 0.60),
    ("fibonacci", 0.65),
];

// S_e mappings
const RELATIONSHIP_SE_MAP: &[(&str, f64)] = &[
    ("length", 0.10),
    ("first", 0.15),
    ("last", 0.15),
    ("sum", 0.15),
    ("add", 0.15),
    ("max", 0.18),
    ("min", 0.18),
    ("product", 0.20),
    ("mean", 0.25),
    ("double_all", 0.30),
    ("square_all", 0.30),
    ("sum_of_doubled", 0.40),
    ("sum_of_squares", 0.45),
    ("factorial", 0.70),
    ("fibonacci", 0.75),
];

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_observe_sum() {
        let observer = Observer::new();
        let examples = vec![
            Example::new_scalar_list(vec![1, 2, 3], 6),
            Example::new_scalar_list(vec![4, 5, 6], 15),
        ];

        let coords = observer.observe(&examples).unwrap();
        assert_eq!(coords.s_k, 0.01); // sum
        assert_eq!(coords.s_t, 0.10);
        assert_eq!(coords.s_e, 0.15);
    }

    #[test]
    fn test_observe_first() {
        let observer = Observer::new();
        let examples = vec![
            Example::new_scalar_list(vec![5, 2, 8], 5),
            Example::new_scalar_list(vec![20, 10, 30], 20),
        ];

        let coords = observer.observe(&examples).unwrap();
        assert_eq!(coords.s_k, 0.16); // first
    }
}
