"""
Poincaré Computing: Backward Trajectory Completion in Bounded Phase Space

This package provides Python bindings for the Poincaré computing framework.

Core Types:
    - SPoint: S-entropy space coordinates
    - TernaryAddress: Base-3 addressing
    - PartitionCoord: Quantum number coordinates (n, ℓ, m, s)
    - Trajectory: Sequence of states
    - PoincareNavigator: Backward navigation engine

Example:
    >>> from poincare import SPoint, PoincareNavigator
    >>>
    >>> # Create navigator
    >>> nav = PoincareNavigator(partition_depth=12, branching_factor=3)
    >>>
    >>> # Observe final state
    >>> final_state = SPoint(s_k=0.75, s_t=0.50, s_e=0.25)
    >>>
    >>> # Complete trajectory backward
    >>> trajectory = nav.complete_trajectory(final_state)
    >>>
    >>> print(f"Trajectory has {len(trajectory)} states")
"""

__version__ = "0.1.0"

# Import core types from Rust extension
try:
    from ._native import (
        SPoint,
        TernaryAddress,
        PartitionCoord,
        Trajectory,
        PoincareNavigator,
    )
except ImportError:
    # Stubs for development without compiled extension
    class SPoint:
        """S-entropy space point (stub)"""
        def __init__(self, s_k: float, s_t: float, s_e: float):
            raise NotImplementedError("Rust extension not compiled")

    class TernaryAddress:
        """Ternary address (stub)"""
        def __init__(self, trits: list[int]):
            raise NotImplementedError("Rust extension not compiled")

    class PartitionCoord:
        """Partition coordinate (stub)"""
        def __init__(self, n: int, l: int, m: int, s: float):
            raise NotImplementedError("Rust extension not compiled")

    class Trajectory:
        """Trajectory (stub)"""
        pass

    class PoincareNavigator:
        """Navigator (stub)"""
        def __init__(self, partition_depth: int, branching_factor: int):
            raise NotImplementedError("Rust extension not compiled")

__all__ = [
    "SPoint",
    "TernaryAddress",
    "PartitionCoord",
    "Trajectory",
    "PoincareNavigator",
]
