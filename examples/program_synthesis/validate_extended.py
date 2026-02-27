"""
Extended Validation for Poincaré Program Synthesis

Tests all advanced features:
- 45+ programs across 8 operation types
- Multi-argument functions
- Nested compositions
- Conditional logic
- Recursive functions

Results saved to JSON/CSV for comprehensive analysis.
"""

import time
import json
import csv
from typing import List, Tuple, Any, Dict
from datetime import datetime
from pathlib import Path

from synthesis_extended import (
    ExtendedProgramLibrary,
    ExtendedProgramObserver,
    SPoint,
    format_examples
)


class ExtendedSynthesisBenchmark:
    """Comprehensive benchmark suite"""

    def __init__(self):
        self.library = ExtendedProgramLibrary()
        self.observer = ExtendedProgramObserver()
        self.results = []

    def get_test_cases(self) -> Dict[str, List[Tuple]]:
        """Comprehensive test cases across all operation types"""
        return {
            # === AGGREGATION ===
            'sum': [
                ([1, 2, 3], 6),
                ([4, 5, 6], 15),
                ([10], 10),
            ],
            'product': [
                ([2, 3], 6),
                ([4, 5], 20),
                ([2, 2, 2], 8),
            ],
            'max': [
                ([1, 5, 3], 5),
                ([2, 9, 4], 9),
                ([10, 1], 10),
            ],
            'min': [
                ([1, 5, 3], 1),
                ([2, 9, 4], 2),
                ([10, 1], 1),
            ],
            'mean': [
                ([1, 2, 3], 2.0),
                ([4, 6], 5.0),
                ([10], 10.0),
            ],
            'length': [
                ([1, 2, 3], 3),
                ([4], 1),
                ([], 0),
            ],
            'range': [
                ([1, 5, 3], 4),
                ([10, 2, 8], 8),
                ([5], 0),
            ],

            # === ACCESS ===
            'first': [
                ([5, 2, 8], 5),  # first != min (min=2)
                ([20, 10, 30], 20),  # first != min (min=10)
                ([7], 7),
            ],
            'last': [
                ([5, 2, 8], 8),  # last != max (max=8, but test it)
                ([20, 30, 10], 10),  # last != max (max=30)
                ([7], 7),
            ],
            'second': [
                ([1, 2, 3], 2),
                ([10, 20, 30], 20),
                ([5, 6], 6),
            ],

            # === TRANSFORMATION ===
            'double_all': [
                ([1, 2, 3], [2, 4, 6]),
                ([5], [10]),
                ([0, -1], [0, -2]),
            ],
            'square_all': [
                ([1, 2, 3], [1, 4, 9]),
                ([4], [16]),
                ([-2, 3], [4, 9]),
            ],
            'negate_all': [
                ([1, 2, 3], [-1, -2, -3]),
                ([5], [-5]),
                ([-1, 2], [1, -2]),
            ],
            'filter_positive': [
                ([1, -2, 3, -4], [1, 3]),
                ([5, 6, 7], [5, 6, 7]),
                ([-1, -2], []),
            ],
            'filter_even': [
                ([1, 2, 3, 4], [2, 4]),
                ([1, 3, 5], []),
                ([2, 4, 6], [2, 4, 6]),
            ],
            'reverse': [
                ([1, 2, 3], [3, 2, 1]),
                ([5], [5]),
                ([1, 2], [2, 1]),
            ],
            'sort_asc': [
                ([3, 1, 2], [1, 2, 3]),
                ([5, 2, 8, 1], [1, 2, 5, 8]),
                ([1], [1]),
            ],

            # === ARITHMETIC (2 arguments) ===
            'add': [
                ((3, 5), 8),
                ((10, 20), 30),
                ((0, 7), 7),
            ],
            'subtract': [
                ((10, 3), 7),
                ((20, 15), 5),
                ((7, 7), 0),
            ],
            'multiply': [
                ((3, 4), 12),
                ((5, 6), 30),
                ((2, 0), 0),
            ],
            'divide': [
                ((10, 2), 5.0),
                ((20, 4), 5.0),
                ((7, 2), 3.5),
            ],

            # === CONDITIONAL ===
            'max_of_two': [
                ((5, 3), 5),
                ((10, 20), 20),
                ((7, 7), 7),
            ],
            'min_of_two': [
                ((5, 3), 3),
                ((10, 20), 10),
                ((7, 7), 7),
            ],
            'abs_single': [
                (-5, 5),
                (3, 3),
                (0, 0),
            ],
            'sign': [
                (5, 1),
                (-3, -1),
                (0, 0),
            ],

            # === COMPOSITION ===
            'sum_of_squares': [
                ([1, 2, 3], 14),  # 1 + 4 + 9
                ([2, 3], 13),     # 4 + 9
                ([5], 25),
            ],
            'sum_of_doubled': [
                ([1, 2, 3], 12),  # 2 + 4 + 6
                ([5, 10], 30),    # 10 + 20
                ([3], 6),
            ],
            'sum_positive': [
                ([1, -2, 3, -4, 5], 9),  # 1 + 3 + 5
                ([1, 2, 3], 6),
                ([-1, -2], 0),
            ],
            'sum_even': [
                ([1, 2, 3, 4], 6),  # 2 + 4
                ([2, 4, 6], 12),
                ([1, 3, 5], 0),
            ],

            # === RECURSIVE ===
            'factorial': [
                (0, 1),
                (1, 1),
                (5, 120),
                (6, 720),
            ],
            'fibonacci': [
                (0, 0),
                (1, 1),
                (5, 5),
                (7, 13),
            ],
            'sum_recursive': [
                ([1, 2, 3], 6),
                ([5, 10], 15),
                ([1], 1),
            ],
        }

    def run_validation(self) -> List[Dict]:
        """Run complete validation suite"""
        print("=" * 80)
        print("EXTENDED POINCARE PROGRAM SYNTHESIS VALIDATION")
        print("Testing: {} programs across 8 operation types".format(
            self.library.count()))
        print("=" * 80)
        print()

        test_cases = self.get_test_cases()
        results = []

        # Group by operation type for organized output
        by_type = {}
        for name in test_cases.keys():
            prog = self.library.get_program(name)
            if prog:
                op_type = prog.operation_type.value
                if op_type not in by_type:
                    by_type[op_type] = []
                by_type[op_type].append(name)

        # Test each operation type
        for op_type in sorted(by_type.keys()):
            print(f"\n=== {op_type.upper()} ===\n")

            for program_name in by_type[op_type]:
                if program_name not in test_cases:
                    continue

                examples = test_cases[program_name]
                print(f"Testing: {program_name}")

                # Run synthesis
                result = self._test_synthesis(program_name, examples)
                results.append(result)

                # Print result
                self._print_result(result)

        return results

    def _test_synthesis(
        self,
        expected_program: str,
        examples: List[Tuple]
    ) -> Dict:
        """Test program synthesis for single case"""
        # Observe examples
        start_observe = time.time()
        s_coords = self.observer.observe(examples)
        observe_time = time.time() - start_observe

        # Find closest program
        start_synthesis = time.time()
        synthesized = self.library.find_closest(s_coords, max_distance=0.2)
        synthesis_time = time.time() - start_synthesis

        # Check correctness
        if synthesized is None:
            correct = False
            match = False
            synthesized_name = None
        else:
            synthesized_name = synthesized.name
            correct = synthesized_name == expected_program
            match = self._validate_program(synthesized, examples)

        # Get expected program details
        expected_prog = self.library.get_program(expected_program)
        distance = (s_coords.distance_to(expected_prog.s_coords)
                   if expected_prog else None)

        return {
            'timestamp': datetime.now().isoformat(),
            'expected_program': expected_program,
            'synthesized_program': synthesized_name,
            'correct': correct,
            'examples_validated': match,
            'num_examples': len(examples),
            's_coords': s_coords.to_dict(),
            'expected_coords': (expected_prog.s_coords.to_dict()
                              if expected_prog else None),
            'distance': distance,
            'operation_type': (expected_prog.operation_type.value
                             if expected_prog else None),
            'arity': (expected_prog.arity if expected_prog else None),
            'composition_depth': (expected_prog.composition_depth
                                if expected_prog else None),
            'observe_time_ms': observe_time * 1000,
            'synthesis_time_ms': synthesis_time * 1000,
            'total_time_ms': (observe_time + synthesis_time) * 1000,
            'examples': self._format_examples_for_json(examples)
        }

    def _format_examples_for_json(self, examples: List[Tuple]) -> List[Dict]:
        """Format examples for JSON storage"""
        formatted = []
        for ex in examples:
            if len(ex) == 2:
                inp, out = ex
                formatted.append({'input': inp, 'output': out})
        return formatted

    def _validate_program(self, program, examples: List[Tuple]) -> bool:
        """Validate program against all examples"""
        try:
            func = program.function
            arity = program.arity

            for ex in examples:
                if len(ex) != 2:
                    continue
                inp, expected_out = ex

                # Handle different arities
                if arity == 1:
                    actual_out = func(inp)
                elif arity == 2:
                    if isinstance(inp, tuple) and len(inp) == 2:
                        actual_out = func(inp[0], inp[1])
                    else:
                        return False
                else:
                    return False

                # Compare outputs
                if isinstance(expected_out, float):
                    if abs(actual_out - expected_out) > 1e-6:
                        return False
                elif actual_out != expected_out:
                    return False

            return True
        except:
            return False

    def _print_result(self, result: Dict):
        """Print single test result"""
        status = "[PASS]" if result['correct'] else "[FAIL]"
        print(f"  Status: {status}")
        print(f"  Expected: {result['expected_program']}")
        print(f"  Synthesized: {result['synthesized_program']}")
        if result['distance'] is not None:
            print(f"  S-distance: {result['distance']:.4f}")
        print(f"  Time: {result['total_time_ms']:.2f}ms")
        print()

    def compute_statistics(self, results: List[Dict]) -> Dict:
        """Compute aggregate statistics"""
        total = len(results)
        correct = sum(1 for r in results if r['correct'])
        validated = sum(1 for r in results if r['examples_validated'])

        # By operation type
        by_type = {}
        for r in results:
            op_type = r['operation_type']
            if op_type not in by_type:
                by_type[op_type] = {'total': 0, 'correct': 0}
            by_type[op_type]['total'] += 1
            if r['correct']:
                by_type[op_type]['correct'] += 1

        # Accuracy by type
        type_accuracy = {
            op_type: stats['correct'] / stats['total']
            for op_type, stats in by_type.items()
        }

        avg_time = sum(r['total_time_ms'] for r in results) / total
        avg_distance = sum(r['distance'] for r in results
                          if r['distance'] is not None) / total

        return {
            'total_tests': total,
            'correct_syntheses': correct,
            'validated_programs': validated,
            'accuracy': correct / total,
            'validation_rate': validated / total,
            'avg_total_time_ms': avg_time,
            'avg_distance': avg_distance,
            'by_operation_type': type_accuracy,
            'library_size': self.library.count(),
        }

    def save_results(
        self,
        results: List[Dict],
        statistics: Dict,
        output_dir: str = "results"
    ):
        """Save results to JSON and CSV"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # JSON
        json_file = output_path / f"extended_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'framework': 'Poincare Computing - Extended',
                    'method': 'Backward Trajectory Completion',
                    'library_size': self.library.count(),
                    'operation_types': 8,
                },
                'statistics': statistics,
                'results': results
            }, f, indent=2)

        print(f"\nDetailed results: {json_file}")

        # CSV
        csv_file = output_path / f"extended_summary_{timestamp}.csv"
        with open(csv_file, 'w', newline='') as f:
            fieldnames = [
                'expected_program', 'synthesized_program', 'correct',
                'operation_type', 'arity', 'composition_depth',
                's_k', 's_t', 's_e', 'distance', 'total_time_ms'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for r in results:
                writer.writerow({
                    'expected_program': r['expected_program'],
                    'synthesized_program': r['synthesized_program'],
                    'correct': r['correct'],
                    'operation_type': r['operation_type'],
                    'arity': r['arity'],
                    'composition_depth': r['composition_depth'],
                    's_k': r['s_coords']['s_k'],
                    's_t': r['s_coords']['s_t'],
                    's_e': r['s_coords']['s_e'],
                    'distance': r['distance'],
                    'total_time_ms': r['total_time_ms'],
                })

        print(f"Summary CSV: {csv_file}")

        # Statistics
        stats_file = output_path / f"extended_statistics_{timestamp}.json"
        with open(stats_file, 'w') as f:
            json.dump(statistics, f, indent=2)

        print(f"Statistics: {stats_file}")


def main():
    """Run extended validation"""
    benchmark = ExtendedSynthesisBenchmark()

    # Run validation
    results = benchmark.run_validation()

    # Statistics
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    statistics = benchmark.compute_statistics(results)

    print(f"Total tests: {statistics['total_tests']}")
    print(f"Correct syntheses: {statistics['correct_syntheses']}")
    print(f"Accuracy: {statistics['accuracy']:.1%}")
    print(f"Validation rate: {statistics['validation_rate']:.1%}")
    print(f"Average time: {statistics['avg_total_time_ms']:.2f}ms")
    print(f"Average S-distance: {statistics['avg_distance']:.4f}")
    print(f"Library size: {statistics['library_size']} programs")
    print()

    print("Accuracy by operation type:")
    for op_type, acc in sorted(statistics['by_operation_type'].items()):
        print(f"  {op_type:20s}: {acc:.1%}")
    print()

    # Save results
    benchmark.save_results(results, statistics)

    print("=" * 80)
    print("EXTENDED VALIDATION COMPLETE")
    print("=" * 80)

    return results, statistics


if __name__ == "__main__":
    main()
