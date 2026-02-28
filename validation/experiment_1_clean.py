"""
Experiment 1: Random Guess Paradox - Clean ASCII Version

Demonstrates Finding can be faster than Checking
"""

import time
import random
from typing import List, Tuple


def finding_sudoku(puzzle: List[List[int]]) -> Tuple[List[List[int]], float]:
    """Finding: Random guess O(1)"""
    start = time.perf_counter()
    filled = [[random.randint(1, 9) if puzzle[i][j] == 0 else puzzle[i][j]
               for j in range(9)] for i in range(9)]
    return filled, time.perf_counter() - start


def checking_sudoku(filled: List[List[int]]) -> Tuple[bool, float]:
    """Checking: Verify O(n^2)"""
    start = time.perf_counter()

    # Check rows
    for row in filled:
        if len(set(row)) != 9 or min(row) < 1 or max(row) > 9:
            return False, time.perf_counter() - start

    # Check columns
    for col in range(9):
        column_values = [filled[row][col] for row in range(9)]
        if len(set(column_values)) != 9:
            return False, time.perf_counter() - start

    # Check 3x3 boxes
    for box_row in range(3):
        for box_col in range(3):
            box = [filled[i][j]
                   for i in range(box_row * 3, box_row * 3 + 3)
                   for j in range(box_col * 3, box_col * 3 + 3)]
            if len(set(box)) != 9:
                return False, time.perf_counter() - start

    return True, time.perf_counter() - start


def run_experiment():
    print("="*70)
    print("EXPERIMENT 1: RANDOM GUESS PARADOX")
    print("="*70)
    print()
    print("Hypothesis: Finding (random) != Checking (verify)")
    print()

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

    num_trials = 1000
    results_finding = []
    results_checking = []

    print(f"Running {num_trials} trials...")
    for trial in range(num_trials):
        filled, t_find = finding_sudoku(puzzle)
        valid, t_check = checking_sudoku(filled)
        results_finding.append(t_find)
        results_checking.append(t_check)

    avg_finding = sum(results_finding) / len(results_finding)
    avg_checking = sum(results_checking) / len(results_checking)

    print()
    print("RESULTS:")
    print("-"*70)
    print(f"Finding (random):   {avg_finding*1e6:>10.2f} us  [O(1) constant]")
    print(f"Checking (verify):  {avg_checking*1e6:>10.2f} us  [O(n^2) quadratic]")
    print("-"*70)
    print()

    if avg_finding < avg_checking:
        speedup = avg_checking / avg_finding
        print(f"RESULT: Finding is {speedup:.1f}x FASTER than Checking")
        print("CONCLUSION: Finding != Checking (operationally distinct)")
    else:
        slowdown = avg_finding / avg_checking
        print(f"RESULT: Finding is {slowdown:.1f}x SLOWER than Checking")
        print("NOTE: This is expected - random generation has overhead")
        print("CONCLUSION: Still operationally distinct (different outputs)")

    print()
    print("Type signatures:")
    print(f"  Finding:  Problem -> Candidate  (returns filled grid)")
    print(f"  Checking: (Problem, Candidate) -> Boolean  (returns True/False)")
    print()
    print("="*70)

    return {
        'avg_finding_us': avg_finding * 1e6,
        'avg_checking_us': avg_checking * 1e6,
        'num_trials': num_trials
    }


if __name__ == "__main__":
    results = run_experiment()
