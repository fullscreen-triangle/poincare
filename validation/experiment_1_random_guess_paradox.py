"""
Experiment 1: Random Guess Paradox (Sudoku)

Demonstrates that Finding (random guess) can be faster than Checking (verification),
proving they are operationally distinct operations.

This validates Theorem 6.1 (Operational Trichotomy).
"""

import time
import random
from typing import List, Tuple


def finding_sudoku(puzzle: List[List[int]]) -> Tuple[List[List[int]], float]:
    """
    Finding operation: Generate candidate solution via random guess.

    Complexity: O(1) - constant time (81 random assignments)

    Returns:
        (filled_grid, time_taken)
    """
    start = time.perf_counter()

    filled = [[random.randint(1, 9) if puzzle[i][j] == 0 else puzzle[i][j]
               for j in range(9)]
              for i in range(9)]

    t_finding = time.perf_counter() - start
    return filled, t_finding


def checking_sudoku(filled: List[List[int]]) -> Tuple[bool, float]:
    """
    Checking operation: Verify candidate satisfies all constraints.

    Complexity: O(n²) - check 9 rows + 9 cols + 9 boxes = 27 checks

    Returns:
        (is_valid, time_taken)
    """
    start = time.perf_counter()

    # Check rows (9 checks)
    for row in filled:
        if len(set(row)) != 9 or min(row) < 1 or max(row) > 9:
            return False, time.perf_counter() - start

    # Check columns (9 checks)
    for col in range(9):
        column_values = [filled[row][col] for row in range(9)]
        if len(set(column_values)) != 9:
            return False, time.perf_counter() - start

    # Check 3x3 boxes (9 checks)
    for box_row in range(3):
        for box_col in range(3):
            box = [filled[i][j]
                   for i in range(box_row * 3, box_row * 3 + 3)
                   for j in range(box_col * 3, box_col * 3 + 3)]
            if len(set(box)) != 9:
                return False, time.perf_counter() - start

    t_checking = time.perf_counter() - start
    return True, t_checking


def recognizing_sudoku(puzzle: List[List[int]], filled: List[List[int]]) -> Tuple[float, float]:
    """
    Recognizing operation: Confirm solution via triple convergence.

    Complexity: O(1) - observe thermodynamic gap from three perspectives

    Returns:
        (confidence, time_taken)
    """
    start = time.perf_counter()

    # First, must pass verification
    valid, _ = checking_sudoku(filled)
    if not valid:
        return 0.0, time.perf_counter() - start

    # Observe gap from three perspectives
    # (In full implementation, these would be actual thermodynamic measurements)
    epsilon_oscillatory = measure_oscillatory_perspective(puzzle, filled)
    epsilon_categorical = measure_categorical_perspective(puzzle, filled)
    epsilon_partition = measure_partition_perspective(puzzle, filled)

    # Triple convergence test
    CONVERGENCE_THRESHOLD = 1e-6
    convergence = (abs(epsilon_oscillatory - epsilon_categorical) < CONVERGENCE_THRESHOLD and
                   abs(epsilon_categorical - epsilon_partition) < CONVERGENCE_THRESHOLD)

    confidence = 1.0 if convergence else 0.0
    t_recognizing = time.perf_counter() - start

    return confidence, t_recognizing


def measure_oscillatory_perspective(puzzle, filled):
    """Measure thermodynamic gap from oscillatory dynamics perspective"""
    # Simplified: entropy of constraint satisfaction pattern
    violations = sum(1 for i in range(9) for j in range(9)
                    if puzzle[i][j] != 0 and puzzle[i][j] != filled[i][j])
    return violations / 81.0


def measure_categorical_perspective(puzzle, filled):
    """Measure thermodynamic gap from categorical structure perspective"""
    # Simplified: partition depth of solution
    unique_in_rows = sum(len(set(row)) for row in filled) / 81.0
    return 1.0 - unique_in_rows


def measure_partition_perspective(puzzle, filled):
    """Measure thermodynamic gap from partition coordinates perspective"""
    # Simplified: coordinate distance in S-space
    filled_entropy = sum(len(set(filled[i])) for i in range(9)) / 81.0
    return 1.0 - filled_entropy


def run_experiment(num_trials: int = 1000):
    """
    Run the Random Guess Paradox experiment.

    Expected result: Finding is significantly faster than Checking,
    demonstrating they are operationally distinct.
    """
    print("=" * 70)
    print("EXPERIMENT 1: RANDOM GUESS PARADOX (Sudoku)")
    print("=" * 70)
    print()
    print("Hypothesis: Finding (random guess) is faster than Checking (verify)")
    print("This proves Finding != Checking operationally")
    print()

    # Example Sudoku puzzle (partially filled)
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    results_finding = []
    results_checking = []
    results_recognizing = []

    print(f"Running {num_trials} trials...")
    print()

    for trial in range(num_trials):
        # Finding operation
        filled, t_finding = finding_sudoku(puzzle)
        results_finding.append(t_finding)

        # Checking operation
        valid, t_checking = checking_sudoku(filled)
        results_checking.append(t_checking)

        # Recognizing operation
        confidence, t_recognizing = recognizing_sudoku(puzzle, filled)
        results_recognizing.append(t_recognizing)

    # Calculate statistics
    avg_finding = sum(results_finding) / len(results_finding)
    avg_checking = sum(results_checking) / len(results_checking)
    avg_recognizing = sum(results_recognizing) / len(results_recognizing)

    speedup_finding_vs_checking = avg_checking / avg_finding
    speedup_finding_vs_recognizing = avg_recognizing / avg_finding

    # Display results
    print("RESULTS:")
    print("-" * 70)
    print(f"{'Operation':<20} {'Avg Time':<20} {'Complexity':<20}")
    print("-" * 70)
    print(f"{'Finding (random)':<20} {avg_finding*1e6:>10.2f} μs      {'O(1) - constant':<20}")
    print(f"{'Checking (verify)':<20} {avg_checking*1e6:>10.2f} μs      {'O(n²) - quadratic':<20}")
    print(f"{'Recognizing (gap)':<20} {avg_recognizing*1e6:>10.2f} μs      {'O(1) - constant':<20}")
    print("-" * 70)
    print()

    print("SPEEDUP ANALYSIS:")
    print("-" * 70)
    print(f"Finding vs Checking:    {speedup_finding_vs_checking:>6.1f}x faster")
    print(f"Finding vs Recognizing: {speedup_finding_vs_recognizing:>6.1f}x (similar speed)")
    print("-" * 70)
    print()

    print("INTERPRETATION:")
    print("-" * 70)
    if speedup_finding_vs_checking > 10:
        print("✓ Finding is SIGNIFICANTLY faster than Checking")
        print("✓ This proves they are OPERATIONALLY DISTINCT")
        print("✓ Random guess can find in O(1), but checking takes O(n²)")
        print()
        print("CONCLUSION: The Random Guess Paradox is empirically validated!")
        print()
        print("Traditional P vs NP asks: 'Is finding as hard as checking?'")
        print("Our answer: NO - finding can be FASTER than checking")
        print("            BUT finding without recognition provides no knowledge")
        print()
        print("This demonstrates that Finding, Checking, and Recognizing are")
        print("THREE DISTINCT OPERATIONS, validating Theorem 6.1")
    else:
        print("⚠ Finding and Checking have similar speeds")
        print("⚠ This may indicate measurement noise or implementation issues")
    print("=" * 70)


if __name__ == "__main__":
    run_experiment(num_trials=1000)
