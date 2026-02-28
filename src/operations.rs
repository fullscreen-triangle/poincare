//! Program operations and execution

use crate::observer::ExampleValue;
use crate::error::{Result, SynthesisError};

/// A program operation that can be executed
pub trait Operation: Send + Sync {
    /// Execute the operation on input
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue>;

    /// Name of the operation
    fn name(&self) -> &str;

    /// Arity (number of arguments)
    fn arity(&self) -> usize;
}

// ============================================================================
// AGGREGATION OPERATIONS
// ============================================================================

#[derive(Debug)]
pub struct SumOp;

impl Operation for SumOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => Ok(ExampleValue::Scalar(v.iter().sum())),
            _ => Err(SynthesisError::ExecutionError(
                "sum requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "sum"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct ProductOp;

impl Operation for ProductOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => Ok(ExampleValue::Scalar(v.iter().product())),
            _ => Err(SynthesisError::ExecutionError(
                "product requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "product"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct MaxOp;

impl Operation for MaxOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => v
                .iter()
                .max()
                .map(|&x| ExampleValue::Scalar(x))
                .ok_or_else(|| {
                    SynthesisError::ExecutionError("max on empty list".to_string())
                }),
            _ => Err(SynthesisError::ExecutionError(
                "max requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "max"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct MinOp;

impl Operation for MinOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => v
                .iter()
                .min()
                .map(|&x| ExampleValue::Scalar(x))
                .ok_or_else(|| {
                    SynthesisError::ExecutionError("min on empty list".to_string())
                }),
            _ => Err(SynthesisError::ExecutionError(
                "min requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "min"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct LengthOp;

impl Operation for LengthOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => Ok(ExampleValue::Scalar(v.len() as i64)),
            _ => Err(SynthesisError::ExecutionError(
                "length requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "length"
    }

    fn arity(&self) -> usize {
        1
    }
}

// ============================================================================
// ACCESS OPERATIONS
// ============================================================================

#[derive(Debug)]
pub struct FirstOp;

impl Operation for FirstOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => v
                .first()
                .map(|&x| ExampleValue::Scalar(x))
                .ok_or_else(|| {
                    SynthesisError::ExecutionError("first on empty list".to_string())
                }),
            _ => Err(SynthesisError::ExecutionError(
                "first requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "first"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct LastOp;

impl Operation for LastOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => v
                .last()
                .map(|&x| ExampleValue::Scalar(x))
                .ok_or_else(|| {
                    SynthesisError::ExecutionError("last on empty list".to_string())
                }),
            _ => Err(SynthesisError::ExecutionError(
                "last requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "last"
    }

    fn arity(&self) -> usize {
        1
    }
}

// ============================================================================
// TRANSFORMATION OPERATIONS
// ============================================================================

#[derive(Debug)]
pub struct DoubleAllOp;

impl Operation for DoubleAllOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => {
                Ok(ExampleValue::List(v.iter().map(|&x| x * 2).collect()))
            }
            _ => Err(SynthesisError::ExecutionError(
                "double_all requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "double_all"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct SquareAllOp;

impl Operation for SquareAllOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => {
                Ok(ExampleValue::List(v.iter().map(|&x| x * x).collect()))
            }
            _ => Err(SynthesisError::ExecutionError(
                "square_all requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "square_all"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct ReverseOp;

impl Operation for ReverseOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => {
                let mut reversed = v.clone();
                reversed.reverse();
                Ok(ExampleValue::List(reversed))
            }
            _ => Err(SynthesisError::ExecutionError(
                "reverse requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "reverse"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[derive(Debug)]
pub struct SortAscOp;

impl Operation for SortAscOp {
    fn execute(&self, input: &ExampleValue) -> Result<ExampleValue> {
        match input {
            ExampleValue::List(v) => {
                let mut sorted = v.clone();
                sorted.sort_unstable();
                Ok(ExampleValue::List(sorted))
            }
            _ => Err(SynthesisError::ExecutionError(
                "sort_asc requires list input".to_string(),
            )),
        }
    }

    fn name(&self) -> &str {
        "sort_asc"
    }

    fn arity(&self) -> usize {
        1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sum() {
        let op = SumOp;
        let input = ExampleValue::List(vec![1, 2, 3]);
        let result = op.execute(&input).unwrap();
        assert_eq!(result, ExampleValue::Scalar(6));
    }

    #[test]
    fn test_double_all() {
        let op = DoubleAllOp;
        let input = ExampleValue::List(vec![1, 2, 3]);
        let result = op.execute(&input).unwrap();
        assert_eq!(result, ExampleValue::List(vec![2, 4, 6]));
    }

    #[test]
    fn test_first() {
        let op = FirstOp;
        let input = ExampleValue::List(vec![5, 2, 8]);
        let result = op.execute(&input).unwrap();
        assert_eq!(result, ExampleValue::Scalar(5));
    }
}
