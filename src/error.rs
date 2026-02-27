//! Error types for program synthesis

use thiserror::Error;

/// Result type for synthesis operations
pub type Result<T> = std::result::Result<T, SynthesisError>;

/// Errors that can occur during program synthesis
#[derive(Error, Debug)]
pub enum SynthesisError {
    #[error("Invalid S-coordinate: {0}")]
    InvalidCoordinate(String),

    #[error("No program found within distance threshold {threshold}. Closest: {closest_distance:.4}")]
    NoProgramFound {
        threshold: f64,
        closest_distance: f64,
    },

    #[error("Empty example set provided")]
    EmptyExamples,

    #[error("Inconsistent example types: {0}")]
    InconsistentExamples(String),

    #[error("Unknown operation pattern: cannot infer relationship")]
    UnknownPattern,

    #[error("Invalid program: {0}")]
    InvalidProgram(String),

    #[error("Execution error: {0}")]
    ExecutionError(String),

    #[error("Library error: {0}")]
    LibraryError(String),

    #[error("I/O error: {0}")]
    IoError(#[from] std::io::Error),

    #[error("JSON error: {0}")]
    JsonError(#[from] serde_json::Error),
}
