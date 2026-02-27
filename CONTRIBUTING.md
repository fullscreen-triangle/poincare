# Contributing to Poincaré Computing

Thank you for your interest in contributing to Poincaré computing! This is foundational work that bridges mathematics, physics, computer science, and epistemology. All contributions are welcome.

## Areas of Contribution

### 1. **Mathematical Foundations**

- Rigorous proofs of theorems
- Complexity analysis
- Partition theory extensions
- Category theory formalization
- New theoretical results

**Skills needed**: Advanced mathematics, proof writing, formal logic

### 2. **Core Implementation**

- Rust core library (`core/rust/`)
- Python bindings (`core/python/`)
- Performance optimization
- Memory management
- Ternary arithmetic primitives

**Skills needed**: Rust, Python, systems programming, algorithms

### 3. **Domain Adapters**

- Vision observer implementation
- Genomics observer implementation
- Mass spectrometry observer implementation
- Processor state observer implementation
- New domain mappings

**Skills needed**: Domain expertise + programming

### 4. **Validation & Testing**

- Unit tests for core primitives
- Integration tests across domains
- Benchmark implementations
- Consistency checks
- Accuracy validation against known results

**Skills needed**: Testing frameworks, numerical analysis

### 5. **Documentation**

- API documentation
- Tutorials and guides
- Examples and demonstrations
- Mathematical exposition
- Domain-specific documentation

**Skills needed**: Technical writing, pedagogy

### 6. **Applications**

- New use cases
- Performance comparisons
- Real-world problem solving
- Interdisciplinary connections

**Skills needed**: Domain expertise, problem-solving

## Getting Started

### 1. Understand the Framework

Read in this order:

1. **README.md** - High-level overview
2. **publication/poincare-trajectory-computing.tex** - Rigorous mathematical treatment
3. **docs/** - Theoretical papers on specific aspects

Key concepts to grasp:

- Bounded phase space and Poincaré recurrence
- Partition theory and hierarchical refinement
- Triple equivalence (oscillatory ≡ categorical ≡ entropic)
- Backward trajectory completion
- S-entropy space [0,1]³
- Ternary addressing

### 2. Set Up Development Environment

**For Rust development**:

```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Clone repository
git clone https://github.com/fullscreen-triangle/poincare.git
cd poincare/core/rust

# Build and test
cargo build
cargo test
```

**For Python development**:

```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
cd core/python
pip install -e ".[dev]"

# Run tests
pytest
```

### 3. Find an Issue

Check [GitHub Issues](https://github.com/fullscreen-triangle/poincare/issues) for:

- `good first issue` - Suitable for newcomers
- `help wanted` - Need community contribution
- `mathematics` - Theoretical work
- `implementation` - Coding work
- `documentation` - Writing work

Or propose new work via [GitHub Discussions](https://github.com/fullscreen-triangle/poincare/discussions).

## Development Workflow

### 1. Fork and Branch

```bash
# Fork the repository on GitHub

# Clone your fork
git clone https://github.com/YOUR_USERNAME/poincare.git
cd poincare

# Add upstream remote
git remote add upstream https://github.com/fullscreen-triangle/poincare.git

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Make Changes

**Code style**:

- Rust: Follow standard `rustfmt` formatting
- Python: Follow PEP 8, use `black` formatter
- LaTeX: Consistent mathematical notation

**Commit messages**:

```text
type(scope): Brief description

Detailed explanation if needed.

Closes #123
```

Types: `feat`, `fix`, `docs`, `test`, `refactor`, `perf`

**Testing**:

- Add tests for all new functionality
- Ensure existing tests pass
- Run benchmarks for performance-critical code

```bash
# Rust
cargo test
cargo bench

# Python
pytest
pytest --benchmark-only
```

### 3. Submit Pull Request

```bash
# Update your branch
git fetch upstream
git rebase upstream/main

# Push to your fork
git push origin feature/your-feature-name
```

Create PR on GitHub with:

- **Clear title**: What does this PR do?
- **Description**: Why is this change needed?
- **Testing**: How was it tested?
- **Documentation**: Updated as needed?
- **References**: Related issues/discussions

### 4. Code Review

Expect feedback on:

- Correctness (mathematical and computational)
- Performance implications
- Code clarity and documentation
- Test coverage
- Alignment with framework principles

Be responsive to feedback. This is collaborative work.

## Contribution Standards

### Mathematical Rigor

All theoretical contributions must be:

- **Formally stated**: Definitions, theorems, proofs
- **Logically sound**: Valid mathematical reasoning
- **Well-referenced**: Citations to prior work
- **Clearly written**: Accessible to target audience

Example:

```latex
\begin{theorem}[Partition Inversion]
\label{thm:partition_inversion}
In a partition hierarchy with depth $M$ and branching factor $b$,
the penultimate state can be found in $O(\log_b M)$ operations.
\end{theorem}

\begin{proof}
[Clear, step-by-step proof...]
\end{proof}
```

### Code Quality

All code contributions must:

- **Compile/run without errors**
- **Pass all existing tests**
- **Include new tests** for added functionality
- **Be documented** (doc comments for public APIs)
- **Follow style guidelines** (rustfmt, black)
- **Have no compiler warnings** (in release mode)

Example (Rust):

```rust
/// Find the penultimate state that transitions to the given state.
///
/// # Arguments
/// * `state` - The final state to work backward from
///
/// # Returns
/// * `Some(SPoint)` - The penultimate state if found
/// * `None` - If no predecessor exists or trajectory is complete
///
/// # Complexity
/// O(b) where b is the branching factor
pub fn find_penultimate(&self, state: &SPoint) -> Option<SPoint> {
    // Implementation with inline comments for complex logic
}
```

### Documentation Standards

All documentation must:

- **Be technically accurate**
- **Use consistent terminology**
- **Provide examples**
- **Explain *why*, not just *what***
- **Be accessible to intended audience**

Use this hierarchy:

- **README.md**: High-level overview for all audiences
- **API docs**: Technical reference for users
- **Tutorials**: Step-by-step guides for learners
- **Papers**: Rigorous mathematical treatment for researchers

### Performance Considerations

Poincaré computing achieves exponential speedup through backward navigation. Contributions must:

- **Preserve asymptotic complexity**: O(log N) is the goal
- **Avoid unnecessary allocations**: Especially in hot paths
- **Use memoization judiciously**: Balance memory vs computation
- **Benchmark performance-critical code**
- **Document complexity in comments**

## Specific Contribution Areas

### Core Primitives (High Priority)

**Needed**:

- `core/rust/src/space.rs` - S-entropy space implementation
- `core/rust/src/address.rs` - Ternary addressing
- `core/rust/src/partition.rs` - Partition coordinates
- `core/rust/src/trajectory.rs` - Trajectory structure
- `core/rust/src/navigator.rs` - Backward navigation engine
- `core/rust/src/observer.rs` - Observer trait and utilities

**Requirements**:

- Zero unsafe code (unless absolutely necessary with clear justification)
- Comprehensive doc comments
- 90%+ test coverage
- Benchmarks for key operations

### Domain Adapters (Medium Priority)

**Needed**:

- Vision observer (following `helicopter` patterns)
- Genomics observer (following `gospel` patterns)
- Mass spectrometry observer (following `lavoisier` patterns)
- Processor observer (following `maxwell` patterns)

**Requirements**:

- Implement `Observer` trait
- Validate against known results
- Document domain-specific mapping
- Provide usage examples

### Validation Suite (High Priority)

**Needed**:

- Harmonic oscillator validation
- N-body problem validation
- Lorenz attractor validation
- Cross-domain consistency checks
- Complexity benchmarks

**Requirements**:

- Compare against analytical solutions
- Measure accuracy metrics
- Profile performance
- Document methodology

### Examples & Tutorials (Medium Priority)

**Needed**:

- "Hello World" of Poincaré computing
- Stone trajectory example (classic mechanics)
- Protein folding demonstration
- Real-world problem solving

**Requirements**:

- Clear pedagogical progression
- Well-commented code
- Expected output shown
- Runtime/complexity discussed

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests
- **GitHub Discussions**: Questions, ideas, general discussion
- **Pull Requests**: Code review and technical discussion

### Code of Conduct

Be:

- **Respectful**: Treat all contributors with respect
- **Constructive**: Provide helpful feedback
- **Collaborative**: Work together toward common goals
- **Rigorous**: Maintain high standards
- **Patient**: This is complex, foundational work

We do not tolerate:

- Harassment or discrimination
- Unconstructive criticism
- Plagiarism or academic dishonesty
- Intentional misinformation

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

### Recognition

All contributors will be:

- Listed in CONTRIBUTORS.md
- Credited in relevant documentation
- Acknowledged in papers citing their work
- Given authorship credit for significant theoretical contributions

## Questions?

- **General questions**: [GitHub Discussions](https://github.com/fullscreen-triangle/poincare/discussions)
- **Bug reports**: [GitHub Issues](https://github.com/fullscreen-triangle/poincare/issues)
- **Security issues**: See SECURITY.md

---

Thank you for contributing to Poincaré computing!

**The stone has landed. Help us find its trajectory.**
