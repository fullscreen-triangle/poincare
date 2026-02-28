//! Navigator: Backward trajectory completion for program synthesis

use crate::core::SPoint;
use crate::error::Result;
use crate::library::{Program, ProgramLibrary};
use crate::observer::{Example, Observer};

/// Navigator performs backward trajectory completion
pub struct Navigator {
    observer: Observer,
    library: ProgramLibrary,
    max_distance: f64,
}

impl Navigator {
    /// Create new navigator with standard library
    pub fn new() -> Self {
        Self {
            observer: Observer::new(),
            library: ProgramLibrary::standard(),
            max_distance: 0.2, // Default threshold from validation
        }
    }

    /// Create navigator with custom library
    pub fn with_library(library: ProgramLibrary) -> Self {
        Self {
            observer: Observer::new(),
            library,
            max_distance: 0.2,
        }
    }

    /// Set maximum distance threshold
    pub fn with_max_distance(mut self, max_distance: f64) -> Self {
        self.max_distance = max_distance;
        self
    }

    /// Synthesize program from examples
    ///
    /// This implements backward trajectory completion:
    /// 1. Observer extracts S-coordinates from examples
    /// 2. Navigator finds closest program in library
    /// 3. Returns synthesized program if within distance threshold
    pub fn synthesize(&self, examples: &[Example]) -> Result<&Program> {
        // Observe: Extract S-coordinates
        let s_coords = self.observer.observe(examples)?;

        // Navigate: Find closest program
        self.library.find_closest(&s_coords, self.max_distance)
    }

    /// Get S-coordinates for examples without synthesizing
    pub fn observe(&self, examples: &[Example]) -> Result<SPoint> {
        self.observer.observe(examples)
    }

    /// Get library reference
    pub fn library(&self) -> &ProgramLibrary {
        &self.library
    }

    /// Find neighbors of given coordinates
    pub fn find_neighbors(&self, coords: &SPoint) -> Vec<&Program> {
        self.library.find_neighbors(coords, self.max_distance)
    }
}

impl Default for Navigator {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::observer::Example;

    #[test]
    fn test_synthesis_sum() {
        let navigator = Navigator::new();

        let examples = vec![
            Example::new_scalar_list(vec![1, 2, 3], 6),
            Example::new_scalar_list(vec![4, 5, 6], 15),
            Example::new_scalar_list(vec![10], 10),
        ];

        let program = navigator.synthesize(&examples).unwrap();
        assert_eq!(program.name(), "sum");
    }

    #[test]
    fn test_synthesis_max() {
        let navigator = Navigator::new();

        let examples = vec![
            Example::new_scalar_list(vec![1, 5, 3], 5),
            Example::new_scalar_list(vec![2, 9, 4], 9),
        ];

        let program = navigator.synthesize(&examples).unwrap();
        assert_eq!(program.name(), "max");
    }

    #[test]
    fn test_synthesis_first() {
        let navigator = Navigator::new();

        let examples = vec![
            Example::new_scalar_list(vec![5, 2, 8], 5),
            Example::new_scalar_list(vec![20, 10, 30], 20),
        ];

        let program = navigator.synthesize(&examples).unwrap();
        assert_eq!(program.name(), "first");
    }

    #[test]
    fn test_synthesis_double_all() {
        let navigator = Navigator::new();

        let examples = vec![
            Example::new_list_list(vec![1, 2, 3], vec![2, 4, 6]),
            Example::new_list_list(vec![5], vec![10]),
        ];

        let program = navigator.synthesize(&examples).unwrap();
        assert_eq!(program.name(), "double_all");
    }
}
