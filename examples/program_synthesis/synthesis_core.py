"""
Poincaré Program Synthesis: Backward Navigation in Program Space

This module implements program synthesis via backward trajectory completion.
Given input/output examples, we navigate backward through program partition
space to find the function that produces those outputs.

Key insight: Programs exist in a hierarchical partition space. By observing
the final state (I/O examples), we can navigate backward to the program's
partition coordinates.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Any, Callable, Optional
from enum import Enum
import json


class OperationType(Enum):
    """Program operation categories"""
    AGGREGATION = "aggregation"      # sum, product, max, min
    TRANSFORMATION = "transformation"  # map, filter, sort
    ACCESS = "access"                 # first, last, nth
    COMPOSITION = "composition"       # nested operations


@dataclass
class SPoint:
    """S-entropy space coordinates"""
    s_k: float  # Knowledge entropy: operation type [0, 1]
    s_t: float  # Temporal entropy: composition depth [0, 1]
    s_e: float  # Evolution entropy: complexity [0, 1]

    def __post_init__(self):
        """Validate coordinates in [0, 1]"""
        for coord in [self.s_k, self.s_t, self.s_e]:
            if not 0 <= coord <= 1:
                raise ValueError(f"Coordinate must be in [0,1], got {coord}")

    def to_dict(self):
        return {'s_k': self.s_k, 's_t': self.s_t, 's_e': self.s_e}


@dataclass
class TernaryAddress:
    """Ternary address in partition space"""
    trits: List[int]  # Each trit in {0, 1, 2}

    def __post_init__(self):
        for t in self.trits:
            if t not in {0, 1, 2}:
                raise ValueError(f"Trit must be 0, 1, or 2, got {t}")

    def parent(self) -> 'TernaryAddress':
        """Navigate to parent partition (remove last trit)"""
        if len(self.trits) <= 1:
            return TernaryAddress([])
        return TernaryAddress(self.trits[:-1])

    def to_tuple(self):
        return tuple(self.trits)


@dataclass
class PartitionCoord:
    """Partition coordinate in program space"""
    operation_type: OperationType
    composition_depth: int
    complexity: int

    def to_dict(self):
        return {
            'operation_type': self.operation_type.value,
            'composition_depth': self.composition_depth,
            'complexity': self.complexity
        }


class ProgramObserver:
    """
    Observer that maps I/O examples to S-entropy space.

    This is the key bridge: we observe the behavior (I/O pairs) and
    extract the categorical features that place the program in partition space.
    """

    def observe(self, examples: List[Tuple[List, Any]]) -> SPoint:
        """
        Extract S-entropy coordinates from I/O examples.

        Args:
            examples: List of (input, output) pairs

        Returns:
            SPoint in S-entropy space
        """
        # Analyze pattern in examples
        pattern = self._analyze_pattern(examples)

        # Map to S-entropy coordinates
        s_k = self._compute_knowledge_entropy(pattern)
        s_t = self._compute_temporal_entropy(pattern)
        s_e = self._compute_evolution_entropy(pattern)

        return SPoint(s_k, s_t, s_e)

    def _analyze_pattern(self, examples: List[Tuple[List, Any]]) -> dict:
        """Analyze I/O examples to extract pattern features"""
        inputs = [ex[0] for ex in examples]
        outputs = [ex[1] for ex in examples]

        pattern = {
            'input_lengths': [len(inp) for inp in inputs],
            'output_type': type(outputs[0]).__name__,
            'is_aggregation': self._is_aggregation(inputs, outputs),
            'is_transformation': self._is_transformation(inputs, outputs),
            'is_access': self._is_access(inputs, outputs),
            'relationship': self._infer_relationship(inputs, outputs)
        }

        return pattern

    def _is_aggregation(self, inputs: List[List], outputs: List[Any]) -> bool:
        """Check if operation is aggregation (list → scalar)"""
        return all(isinstance(out, (int, float)) for out in outputs)

    def _is_transformation(self, inputs: List[List], outputs: List[Any]) -> bool:
        """Check if operation is transformation (list → list)"""
        return all(isinstance(out, list) for out in outputs)

    def _is_access(self, inputs: List[List], outputs: List[Any]) -> bool:
        """Check if operation is element access"""
        return all(
            isinstance(out, type(inp[0])) if inp else False
            for inp, out in zip(inputs, outputs)
        )

    def _infer_relationship(self, inputs: List[List], outputs: List[Any]) -> str:
        """Infer the mathematical relationship"""
        # Check for sum
        if all(sum(inp) == out for inp, out in zip(inputs, outputs)):
            return 'sum'

        # Check for product
        if all(np.prod(inp) == out for inp, out in zip(inputs, outputs)):
            return 'product'

        # Check for max
        if all(max(inp) == out if inp else False for inp, out in zip(inputs, outputs)):
            return 'max'

        # Check for min
        if all(min(inp) == out if inp else False for inp, out in zip(inputs, outputs)):
            return 'min'

        # Check for length
        if all(len(inp) == out for inp, out in zip(inputs, outputs)):
            return 'length'

        # Check for first element
        if all(inp[0] == out if inp else False for inp, out in zip(inputs, outputs)):
            return 'first'

        # Check for last element
        if all(inp[-1] == out if inp else False for inp, out in zip(inputs, outputs)):
            return 'last'

        return 'unknown'

    def _compute_knowledge_entropy(self, pattern: dict) -> float:
        """
        Map operation type to S_k coordinate.

        S_k encoding:
        0.0-0.25: Aggregation operations
        0.25-0.50: Access operations
        0.50-0.75: Transformation operations
        0.75-1.0: Composition operations
        """
        relationship = pattern['relationship']

        aggregation_ops = {'sum', 'product', 'max', 'min', 'length'}
        access_ops = {'first', 'last'}

        if relationship in aggregation_ops:
            # Map specific operation within aggregation range
            op_map = {'sum': 0.05, 'product': 0.10, 'max': 0.15, 'min': 0.20, 'length': 0.25}
            return op_map.get(relationship, 0.125)
        elif relationship in access_ops:
            op_map = {'first': 0.30, 'last': 0.40}
            return op_map.get(relationship, 0.375)
        else:
            return 0.625  # Transformation/composition

    def _compute_temporal_entropy(self, pattern: dict) -> float:
        """
        Map composition depth to S_t coordinate.

        Simple (single operation): 0.0-0.33
        Medium (2-3 operations): 0.34-0.66
        Complex (4+ operations): 0.67-1.0
        """
        # For now, assume simple operations (single level)
        return 0.15  # Simple, single operation

    def _compute_evolution_entropy(self, pattern: dict) -> float:
        """
        Map complexity to S_e coordinate.

        Low complexity: 0.0-0.33
        Medium complexity: 0.34-0.66
        High complexity: 0.67-1.0
        """
        # Simple operations have low complexity
        if pattern['relationship'] in {'sum', 'length', 'first', 'last'}:
            return 0.2
        elif pattern['relationship'] in {'product', 'max', 'min'}:
            return 0.3
        else:
            return 0.5

    def to_partition(self, s: SPoint) -> PartitionCoord:
        """Map S-coordinates to partition coordinates"""
        # Determine operation type from S_k
        if s.s_k < 0.25:
            op_type = OperationType.AGGREGATION
        elif s.s_k < 0.50:
            op_type = OperationType.ACCESS
        elif s.s_k < 0.75:
            op_type = OperationType.TRANSFORMATION
        else:
            op_type = OperationType.COMPOSITION

        # Determine composition depth from S_t
        composition_depth = int(s.s_t * 10) + 1

        # Determine complexity from S_e
        complexity = int(s.s_e * 10)

        return PartitionCoord(op_type, composition_depth, complexity)


class ProgramNavigator:
    """
    Backward navigator in program partition space.

    Given S-coordinates (from observed examples), navigate backward
    through partition space to find the program.
    """

    def __init__(self, partition_depth: int = 9, branching_factor: int = 3):
        self.partition_depth = partition_depth
        self.branching_factor = branching_factor
        self.observer = ProgramObserver()

        # Program library (partition space)
        self.program_library = self._build_program_library()

    def _build_program_library(self) -> dict:
        """Build library of available programs with their S-coordinates"""
        return {
            'sum': {
                'function': lambda lst: sum(lst),
                's_coords': SPoint(0.05, 0.15, 0.2),
                'description': 'Sum of list elements'
            },
            'product': {
                'function': lambda lst: np.prod(lst),
                's_coords': SPoint(0.10, 0.15, 0.3),
                'description': 'Product of list elements'
            },
            'max': {
                'function': lambda lst: max(lst),
                's_coords': SPoint(0.15, 0.15, 0.3),
                'description': 'Maximum element'
            },
            'min': {
                'function': lambda lst: min(lst),
                's_coords': SPoint(0.20, 0.15, 0.3),
                'description': 'Minimum element'
            },
            'length': {
                'function': lambda lst: len(lst),
                's_coords': SPoint(0.25, 0.15, 0.2),
                'description': 'Length of list'
            },
            'first': {
                'function': lambda lst: lst[0] if lst else None,
                's_coords': SPoint(0.30, 0.15, 0.2),
                'description': 'First element'
            },
            'last': {
                'function': lambda lst: lst[-1] if lst else None,
                's_coords': SPoint(0.40, 0.15, 0.2),
                'description': 'Last element'
            },
        }

    def synthesize(self, examples: List[Tuple[List, Any]]) -> Optional[Tuple[str, Callable]]:
        """
        Synthesize program from examples using backward navigation.

        Args:
            examples: List of (input, output) pairs

        Returns:
            Tuple of (program_name, function) or None if not found
        """
        # Step 1: Observe final state (I/O examples)
        s_target = self.observer.observe(examples)

        # Step 2: Navigate backward through partition space
        # Find program with closest S-coordinates
        best_program = None
        min_distance = float('inf')

        for name, prog_info in self.program_library.items():
            s_prog = prog_info['s_coords']
            distance = self._s_distance(s_target, s_prog)

            if distance < min_distance:
                # Validate program against examples
                if self._validate_program(prog_info['function'], examples):
                    min_distance = distance
                    best_program = (name, prog_info['function'])

        return best_program

    def _s_distance(self, s1: SPoint, s2: SPoint) -> float:
        """Euclidean distance in S-space"""
        return np.sqrt(
            (s1.s_k - s2.s_k)**2 +
            (s1.s_t - s2.s_t)**2 +
            (s1.s_e - s2.s_e)**2
        )

    def _validate_program(self, func: Callable, examples: List[Tuple[List, Any]]) -> bool:
        """Validate program against all examples"""
        try:
            for inp, expected_out in examples:
                actual_out = func(inp)
                if actual_out != expected_out:
                    return False
            return True
        except:
            return False


def format_examples(examples: List[Tuple[List, Any]]) -> str:
    """Format examples for display"""
    lines = []
    for inp, out in examples:
        lines.append(f"  {inp} -> {out}")
    return "\n".join(lines)
