//! # Poincaré Computing Core
//!
//! This library provides the foundational primitives for Poincaré computing:
//! backward trajectory completion in bounded phase space.
//!
//! ## Core Concepts
//!
//! - **S-Entropy Space**: Three-dimensional coordinate system [0,1]³
//! - **Ternary Addressing**: Base-3 addressing for partition hierarchies
//! - **Partition Coordinates**: Quantum numbers (n, ℓ, m, s)
//! - **Backward Navigation**: Finding penultimate states through partition structure
//! - **Trajectory Completion**: Recursive backward navigation to initial states
//!
//! ## Usage
//!
//! ```rust
//! use poincare_core::{SPoint, PoincareNavigator};
//!
//! // Create S-entropy space point
//! let final_state = SPoint::new(0.75, 0.50, 0.25);
//!
//! // Create navigator
//! let nav = PoincareNavigator::new(12, 3); // depth=12, branching=3
//!
//! // Complete trajectory backward
//! let trajectory = nav.complete_trajectory(&final_state);
//!
//! println!("Trajectory length: {}", trajectory.states().len());
//! ```
//!
//! ## Modules
//!
//! - [`space`]: S-entropy space primitives
//! - [`address`]: Ternary addressing for partition hierarchies
//! - [`partition`]: Partition quantum number coordinates
//! - [`trajectory`]: Trajectory structure and operations
//! - [`navigator`]: Backward navigation engine
//! - [`observer`]: Domain mapping traits and utilities

pub mod address;
pub mod navigator;
pub mod observer;
pub mod partition;
pub mod space;
pub mod trajectory;

// Re-export core types
pub use address::TernaryAddress;
pub use navigator::{Navigator, PoincareNavigator};
pub use observer::Observer;
pub use partition::PartitionCoord;
pub use space::SPoint;
pub use trajectory::Trajectory;

/// Result type for Poincaré operations
pub type Result<T> = std::result::Result<T, Error>;

/// Error types for Poincaré computing
#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("Invalid S-entropy coordinate: {0}")]
    InvalidCoordinate(String),

    #[error("Invalid ternary address: {0}")]
    InvalidAddress(String),

    #[error("Invalid partition coordinate: {0}")]
    InvalidPartition(String),

    #[error("Trajectory completion failed: {0}")]
    TrajectoryFailed(String),

    #[error("Navigation error: {0}")]
    NavigationError(String),

    #[error("Observer error: {0}")]
    ObserverError(String),
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_core_types_exist() {
        // Ensure all core types are accessible
        let _: SPoint;
        let _: TernaryAddress;
        let _: PartitionCoord;
        let _: Trajectory;
        let _: PoincareNavigator;
    }
}
