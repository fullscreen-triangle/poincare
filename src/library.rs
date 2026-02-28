//! Program library: Collection of programs in S-entropy space

use crate::core::{SPoint, OperationType};
use crate::operations::*;
use crate::error::{Result, SynthesisError};
use std::sync::Arc;

/// A program with its S-entropy position
#[derive(Clone)]
pub struct Program {
    name: String,
    operation: Arc<dyn Operation>,
    s_coords: SPoint,
    op_type: OperationType,
    arity: usize,
    composition_depth: usize,
    description: String,
}

impl Program {
    pub fn new(
        name: impl Into<String>,
        operation: Arc<dyn Operation>,
        s_coords: SPoint,
        op_type: OperationType,
        arity: usize,
        composition_depth: usize,
        description: impl Into<String>,
    ) -> Self {
        Self {
            name: name.into(),
            operation,
            s_coords,
            op_type,
            arity,
            composition_depth,
            description: description.into(),
        }
    }

    pub fn name(&self) -> &str {
        &self.name
    }

    pub fn s_coords(&self) -> &SPoint {
        &self.s_coords
    }

    pub fn operation(&self) -> &Arc<dyn Operation> {
        &self.operation
    }

    pub fn op_type(&self) -> OperationType {
        self.op_type
    }

    pub fn arity(&self) -> usize {
        self.arity
    }

    pub fn composition_depth(&self) -> usize {
        self.composition_depth
    }

    pub fn description(&self) -> &str {
        &self.description
    }

    pub fn distance_to(&self, coords: &SPoint) -> f64 {
        self.s_coords.distance_to(coords)
    }
}

impl std::fmt::Debug for Program {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Program")
            .field("name", &self.name)
            .field("s_coords", &self.s_coords)
            .field("op_type", &self.op_type)
            .field("arity", &self.arity)
            .finish()
    }
}

/// Library of programs organized in S-entropy space
pub struct ProgramLibrary {
    programs: Vec<Program>,
}

impl ProgramLibrary {
    /// Create empty library
    pub fn new() -> Self {
        Self {
            programs: Vec::new(),
        }
    }

    /// Create standard library with validated programs
    pub fn standard() -> Self {
        let mut lib = Self::new();

        // AGGREGATION OPERATIONS (S_k: 0.01-0.10)
        lib.add(Program::new(
            "sum",
            Arc::new(SumOp),
            SPoint::new_unchecked(0.01, 0.10, 0.15),
            OperationType::Aggregation,
            1,
            1,
            "Sum of list elements",
        ));

        lib.add(Program::new(
            "product",
            Arc::new(ProductOp),
            SPoint::new_unchecked(0.02, 0.10, 0.20),
            OperationType::Aggregation,
            1,
            1,
            "Product of list elements",
        ));

        lib.add(Program::new(
            "max",
            Arc::new(MaxOp),
            SPoint::new_unchecked(0.03, 0.10, 0.18),
            OperationType::Aggregation,
            1,
            1,
            "Maximum element",
        ));

        lib.add(Program::new(
            "min",
            Arc::new(MinOp),
            SPoint::new_unchecked(0.04, 0.10, 0.18),
            OperationType::Aggregation,
            1,
            1,
            "Minimum element",
        ));

        lib.add(Program::new(
            "length",
            Arc::new(LengthOp),
            SPoint::new_unchecked(0.06, 0.10, 0.10),
            OperationType::Aggregation,
            1,
            1,
            "Length of list",
        ));

        // ACCESS OPERATIONS (S_k: 0.16-0.20)
        lib.add(Program::new(
            "first",
            Arc::new(FirstOp),
            SPoint::new_unchecked(0.16, 0.10, 0.15),
            OperationType::Access,
            1,
            1,
            "First element",
        ));

        lib.add(Program::new(
            "last",
            Arc::new(LastOp),
            SPoint::new_unchecked(0.17, 0.10, 0.15),
            OperationType::Access,
            1,
            1,
            "Last element",
        ));

        // TRANSFORMATION OPERATIONS (S_k: 0.31-0.42)
        lib.add(Program::new(
            "double_all",
            Arc::new(DoubleAllOp),
            SPoint::new_unchecked(0.31, 0.20, 0.30),
            OperationType::Transformation,
            1,
            1,
            "Double all elements",
        ));

        lib.add(Program::new(
            "square_all",
            Arc::new(SquareAllOp),
            SPoint::new_unchecked(0.32, 0.20, 0.30),
            OperationType::Transformation,
            1,
            1,
            "Square all elements",
        ));

        lib.add(Program::new(
            "reverse",
            Arc::new(ReverseOp),
            SPoint::new_unchecked(0.40, 0.15, 0.20),
            OperationType::Transformation,
            1,
            1,
            "Reverse list",
        ));

        lib.add(Program::new(
            "sort_asc",
            Arc::new(SortAscOp),
            SPoint::new_unchecked(0.41, 0.20, 0.25),
            OperationType::Transformation,
            1,
            1,
            "Sort ascending",
        ));

        lib
    }

    /// Add program to library
    pub fn add(&mut self, program: Program) {
        self.programs.push(program);
    }

    /// Find closest program to given S-coordinates
    pub fn find_closest(&self, coords: &SPoint, max_distance: f64) -> Result<&Program> {
        let mut closest: Option<(&Program, f64)> = None;

        for program in &self.programs {
            let distance = program.distance_to(coords);

            if let Some((_, min_dist)) = closest {
                if distance < min_dist {
                    closest = Some((program, distance));
                }
            } else {
                closest = Some((program, distance));
            }
        }

        match closest {
            Some((program, distance)) if distance < max_distance => Ok(program),
            Some((_, distance)) => Err(SynthesisError::NoProgramFound {
                threshold: max_distance,
                closest_distance: distance,
            }),
            None => Err(SynthesisError::LibraryError(
                "Empty library".to_string(),
            )),
        }
    }

    /// Find all programs within distance threshold
    pub fn find_neighbors(&self, coords: &SPoint, max_distance: f64) -> Vec<&Program> {
        self.programs
            .iter()
            .filter(|p| p.distance_to(coords) < max_distance)
            .collect()
    }

    /// Get program by name
    pub fn get_by_name(&self, name: &str) -> Option<&Program> {
        self.programs.iter().find(|p| p.name() == name)
    }

    /// Get all programs
    pub fn programs(&self) -> &[Program] {
        &self.programs
    }

    /// Number of programs in library
    pub fn len(&self) -> usize {
        self.programs.len()
    }

    /// Check if library is empty
    pub fn is_empty(&self) -> bool {
        self.programs.is_empty()
    }

    /// Get programs by operation type
    pub fn by_operation_type(&self, op_type: OperationType) -> Vec<&Program> {
        self.programs
            .iter()
            .filter(|p| p.op_type() == op_type)
            .collect()
    }
}

impl Default for ProgramLibrary {
    fn default() -> Self {
        Self::standard()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_library_creation() {
        let lib = ProgramLibrary::standard();
        assert!(lib.len() > 0);
        assert!(lib.get_by_name("sum").is_some());
    }

    #[test]
    fn test_find_closest() {
        let lib = ProgramLibrary::standard();

        // Sum coordinates
        let coords = SPoint::new_unchecked(0.01, 0.10, 0.15);
        let program = lib.find_closest(&coords, 0.2).unwrap();
        assert_eq!(program.name(), "sum");
    }

    #[test]
    fn test_find_by_type() {
        let lib = ProgramLibrary::standard();
        let agg_programs = lib.by_operation_type(OperationType::Aggregation);
        assert!(agg_programs.len() >= 5);
    }
}
