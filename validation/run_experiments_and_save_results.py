"""
Master script to run all experiments and save results with proper encoding
"""

import sys
import io
import subprocess

# Set UTF-8 encoding for output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def run_and_save(script_name, output_file):
    """Run experiment script and save output"""
    print(f"\n{'='*70}")
    print(f"Running {script_name}...")
    print(f"{'='*70}\n")

    try:
        # Run with UTF-8 encoding
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=120
        )

        # Save output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\nSTDERR:\n")
                f.write(result.stderr)

        print(f"Results saved to: {output_file}")

        # Also print to console
        print(result.stdout)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"ERROR: {script_name} timed out")
        return False
    except Exception as e:
        print(f"ERROR running {script_name}: {e}")
        return False

def main():
    """Run all validation experiments"""
    print("="*70)
    print("RUNNING ALL VALIDATION EXPERIMENTS")
    print("="*70)

    experiments = [
        ("experiment_1_random_guess_paradox.py", "results_experiment_1.txt"),
        ("experiment_2_type_theory.py", "results_experiment_2.txt"),
        ("experiment_3_complexity_scaling.py", "results_experiment_3.txt"),
    ]

    results = []

    for script, output in experiments:
        success = run_and_save(script, output)
        results.append((script, success))

    # Summary
    print("\n" + "="*70)
    print("EXPERIMENT RESULTS SUMMARY")
    print("="*70)

    for script, success in results:
        status = "SUCCESS" if success else "FAILED"
        print(f"  {status:<10} {script}")

    all_success = all(success for _, success in results)

    if all_success:
        print("\nAll experiments completed successfully!")
        print("Results saved in:")
        for _, output in experiments:
            print(f"  - {output}")
    else:
        print("\nSome experiments failed. Check error messages above.")

    print("="*70)

if __name__ == "__main__":
    main()
