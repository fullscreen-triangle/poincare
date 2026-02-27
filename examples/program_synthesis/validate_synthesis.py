"""
Validation Script for Poincaré Program Synthesis

This script validates backward trajectory completion for program synthesis
against known benchmarks and baseline methods.

Results are saved in JSON and CSV format for analysis.
"""

import time
import json
import csv
from typing import List, Tuple, Any, Dict
from datetime import datetime
from pathlib import Path

from synthesis_core import (
    ProgramNavigator,
    ProgramObserver,
    format_examples
)


class SynthesisBenchmark:
    """Benchmark suite for program synthesis validation"""

    def __init__(self):
        self.navigator = ProgramNavigator()
        self.observer = ProgramObserver()
        self.results = []

    def get_test_cases(self) -> Dict[str, List[Tuple[List, Any]]]:
        """
        Standard test cases for program synthesis.

        Each test case is a set of I/O examples that uniquely identify a program.
        """
        return {
            'sum': [
                ([1, 2, 3], 6),
                ([4, 5, 6], 15),
                ([10], 10),
                ([2, 3], 5),
            ],
            'product': [
                ([2, 3], 6),
                ([4, 5], 20),
                ([2, 2, 2], 8),
                ([1, 5], 5),
            ],
            'max': [
                ([1, 5, 3], 5),
                ([2, 9, 4], 9),
                ([10, 1], 10),
                ([7, 7, 3], 7),
            ],
            'min': [
                ([1, 5, 3], 1),
                ([2, 9, 4], 2),
                ([10, 1], 1),
                ([7, 7, 3], 3),
            ],
            'length': [
                ([1, 2, 3], 3),
                ([4], 1),
                ([1, 2, 3, 4, 5], 5),
                ([], 0),
            ],
            'first': [
                ([1, 2, 3], 1),
                ([10, 20], 10),
                ([5], 5),
                ([99, 1, 2], 99),
            ],
            'last': [
                ([1, 2, 3], 3),
                ([10, 20], 20),
                ([5], 5),
                ([99, 1, 2], 2),
            ],
        }

    def run_validation(self) -> List[Dict]:
        """
        Run complete validation suite.

        Returns:
            List of result dictionaries
        """
        print("=" * 80)
        print("POINCARÉ PROGRAM SYNTHESIS VALIDATION")
        print("Backward Trajectory Completion in Program Space")
        print("=" * 80)
        print()

        test_cases = self.get_test_cases()
        results = []

        for program_name, examples in test_cases.items():
            print(f"Testing: {program_name}")
            print(f"Examples:\n{format_examples(examples)}")

            # Run synthesis
            result = self._test_synthesis(program_name, examples)
            results.append(result)

            # Print result
            self._print_result(result)
            print()

        return results

    def _test_synthesis(
        self,
        expected_program: str,
        examples: List[Tuple[List, Any]]
    ) -> Dict:
        """
        Test program synthesis for single case.

        Returns:
            Dictionary with test results
        """
        # Observe examples to get S-coordinates
        start_observe = time.time()
        s_coords = self.observer.observe(examples)
        observe_time = time.time() - start_observe

        # Navigate backward to synthesize program
        start_synthesis = time.time()
        result = self.navigator.synthesize(examples)
        synthesis_time = time.time() - start_synthesis

        # Check correctness
        if result is None:
            synthesized_program, function = None, None
            correct = False
            match = False
        else:
            synthesized_program, function = result
            correct = synthesized_program == expected_program
            match = self._validate_match(function, examples)

        # Get partition coordinates
        partition_coords = self.observer.to_partition(s_coords)

        return {
            'timestamp': datetime.now().isoformat(),
            'expected_program': expected_program,
            'synthesized_program': synthesized_program,
            'correct': correct,
            'examples_validated': match,
            'num_examples': len(examples),
            's_coords': s_coords.to_dict(),
            'partition_coords': partition_coords.to_dict(),
            'observe_time_ms': observe_time * 1000,
            'synthesis_time_ms': synthesis_time * 1000,
            'total_time_ms': (observe_time + synthesis_time) * 1000,
            'examples': [{'input': inp, 'output': out} for inp, out in examples]
        }

    def _validate_match(
        self,
        function,
        examples: List[Tuple[List, Any]]
    ) -> bool:
        """Validate synthesized function matches all examples"""
        try:
            for inp, expected_out in examples:
                actual_out = function(inp)
                if actual_out != expected_out:
                    return False
            return True
        except:
            return False

    def _print_result(self, result: Dict):
        """Pretty print single test result"""
        status = "[PASS]" if result['correct'] else "[FAIL]"
        print(f"Status: {status}")
        print(f"Expected: {result['expected_program']}")
        print(f"Synthesized: {result['synthesized_program']}")
        print(f"S-coordinates: {result['s_coords']}")
        print(f"Partition: {result['partition_coords']['operation_type']}")
        print(f"Time: {result['total_time_ms']:.2f}ms "
              f"(observe: {result['observe_time_ms']:.2f}ms, "
              f"synthesis: {result['synthesis_time_ms']:.2f}ms)")

    def compute_statistics(self, results: List[Dict]) -> Dict:
        """Compute aggregate statistics"""
        total = len(results)
        correct = sum(1 for r in results if r['correct'])
        validated = sum(1 for r in results if r['examples_validated'])

        avg_time = sum(r['total_time_ms'] for r in results) / total
        avg_observe_time = sum(r['observe_time_ms'] for r in results) / total
        avg_synthesis_time = sum(r['synthesis_time_ms'] for r in results) / total

        return {
            'total_tests': total,
            'correct_syntheses': correct,
            'validated_programs': validated,
            'accuracy': correct / total,
            'validation_rate': validated / total,
            'avg_total_time_ms': avg_time,
            'avg_observe_time_ms': avg_observe_time,
            'avg_synthesis_time_ms': avg_synthesis_time,
        }

    def save_results(
        self,
        results: List[Dict],
        statistics: Dict,
        output_dir: str = "results"
    ):
        """Save results to JSON and CSV files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save detailed results as JSON
        json_file = output_path / f"synthesis_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump({
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'framework': 'Poincaré Computing',
                    'method': 'Backward Trajectory Completion',
                    'partition_depth': self.navigator.partition_depth,
                    'branching_factor': self.navigator.branching_factor,
                },
                'statistics': statistics,
                'results': results
            }, f, indent=2)

        print(f"Detailed results saved to: {json_file}")

        # Save summary as CSV
        csv_file = output_path / f"synthesis_summary_{timestamp}.csv"
        with open(csv_file, 'w', newline='') as f:
            fieldnames = [
                'expected_program',
                'synthesized_program',
                'correct',
                'examples_validated',
                'num_examples',
                's_k',
                's_t',
                's_e',
                'operation_type',
                'total_time_ms',
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for r in results:
                writer.writerow({
                    'expected_program': r['expected_program'],
                    'synthesized_program': r['synthesized_program'],
                    'correct': r['correct'],
                    'examples_validated': r['examples_validated'],
                    'num_examples': r['num_examples'],
                    's_k': r['s_coords']['s_k'],
                    's_t': r['s_coords']['s_t'],
                    's_e': r['s_coords']['s_e'],
                    'operation_type': r['partition_coords']['operation_type'],
                    'total_time_ms': r['total_time_ms'],
                })

        print(f"Summary CSV saved to: {csv_file}")

        # Save statistics separately
        stats_file = output_path / f"statistics_{timestamp}.json"
        with open(stats_file, 'w') as f:
            json.dump(statistics, f, indent=2)

        print(f"Statistics saved to: {stats_file}")


def main():
    """Run validation and save results"""
    benchmark = SynthesisBenchmark()

    # Run validation
    results = benchmark.run_validation()

    # Compute statistics
    print("=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    statistics = benchmark.compute_statistics(results)

    print(f"Total tests: {statistics['total_tests']}")
    print(f"Correct syntheses: {statistics['correct_syntheses']}")
    print(f"Accuracy: {statistics['accuracy']:.1%}")
    print(f"Validation rate: {statistics['validation_rate']:.1%}")
    print(f"Average time: {statistics['avg_total_time_ms']:.2f}ms")
    print(f"  - Observe: {statistics['avg_observe_time_ms']:.2f}ms")
    print(f"  - Synthesis: {statistics['avg_synthesis_time_ms']:.2f}ms")
    print()

    # Save results
    benchmark.save_results(results, statistics)

    print("=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)

    return results, statistics


if __name__ == "__main__":
    main()
