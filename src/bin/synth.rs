//! CLI for program synthesis

use poincare::{Example, Navigator};

fn main() {
    let sep = "=".repeat(80);
    println!("{}", sep);
    println!("POINCARÉ PROGRAM SYNTHESIS - RUST IMPLEMENTATION");
    println!("{}", sep);
    println!();

    let navigator = Navigator::new();

    // Test cases from validation
    let test_cases = vec![
        (
            "sum",
            vec![
                Example::new_scalar_list(vec![1, 2, 3], 6),
                Example::new_scalar_list(vec![4, 5, 6], 15),
                Example::new_scalar_list(vec![10], 10),
            ],
        ),
        (
            "product",
            vec![
                Example::new_scalar_list(vec![2, 3], 6),
                Example::new_scalar_list(vec![4, 5], 20),
            ],
        ),
        (
            "max",
            vec![
                Example::new_scalar_list(vec![1, 5, 3], 5),
                Example::new_scalar_list(vec![2, 9, 4], 9),
            ],
        ),
        (
            "min",
            vec![
                Example::new_scalar_list(vec![1, 5, 3], 1),
                Example::new_scalar_list(vec![2, 9, 4], 2),
            ],
        ),
        (
            "first",
            vec![
                Example::new_scalar_list(vec![5, 2, 8], 5),
                Example::new_scalar_list(vec![20, 10, 30], 20),
            ],
        ),
        (
            "last",
            vec![
                Example::new_scalar_list(vec![5, 2, 8], 8),
                Example::new_scalar_list(vec![20, 30, 10], 10),
            ],
        ),
        (
            "double_all",
            vec![
                Example::new_list_list(vec![1, 2, 3], vec![2, 4, 6]),
                Example::new_list_list(vec![5], vec![10]),
            ],
        ),
        (
            "square_all",
            vec![
                Example::new_list_list(vec![1, 2, 3], vec![1, 4, 9]),
                Example::new_list_list(vec![4], vec![16]),
            ],
        ),
    ];

    let mut correct = 0;
    let mut total = 0;

    for (expected, examples) in test_cases {
        print!("Testing {:<15} ... ", expected);

        match navigator.synthesize(&examples) {
            Ok(program) => {
                let s_coords = navigator.observe(&examples).unwrap();
                let success = program.name() == expected;

                if success {
                    correct += 1;
                    println!("[PASS] {} {}", program.name(), s_coords);
                } else {
                    println!(
                        "[FAIL] Expected: {}, Got: {} {}",
                        expected,
                        program.name(),
                        s_coords
                    );
                }
                total += 1;
            }
            Err(e) => {
                println!("[ERROR] {}", e);
                total += 1;
            }
        }
    }

    println!();
    println!("{}", sep);
    println!("RESULTS");
    println!("{}", sep);
    println!("Total tests: {}", total);
    println!("Correct: {}", correct);
    println!(
        "Accuracy: {:.1}%",
        (correct as f64 / total as f64) * 100.0
    );
    println!("Library size: {} programs", navigator.library().len());
    println!("{}", sep);
}
