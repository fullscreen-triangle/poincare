"""
Generate Panel Figures for Backward Trajectory Completion Paper
Each panel contains 4 charts in a row with minimal text
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.patches import Patch
from matplotlib.colors import LinearSegmentedColormap

# Set publication-quality defaults
plt.rcParams.update({
    'font.size': 9,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 7,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'font.family': 'serif',
})

# Paths
BASE_DIR = Path(__file__).parent.parent.parent
SYNTHESIS_RESULTS = BASE_DIR / "examples/program_synthesis/results/extended_results_20260227_050058.json"
COMPLEXITY_RESULTS = BASE_DIR / "docs/scattering-puzzle/experiments/results/computational_complexity.json"
ABERRATION_RESULTS = BASE_DIR / "docs/scattering-puzzle/experiments/results/aberration_invariance.json"
VALIDATION_RESULTS = BASE_DIR / "docs/scattering-puzzle/experiments/results/validation_results.json"
OUTPUT_DIR = Path(__file__).parent / "figures"

# Color palette
COLORS = {
    'access': '#1f77b4',
    'aggregation': '#ff7f0e',
    'arithmetic': '#2ca02c',
    'composition': '#d62728',
    'conditional': '#9467bd',
    'recursive': '#8c564b',
    'transformation': '#e377c2',
}


def load_json(path):
    """Load JSON file"""
    with open(path, 'r') as f:
        return json.load(f)


def create_panel_1_synthesis():
    """Panel 1: Program Synthesis Results - 4 charts in a row"""
    data = load_json(SYNTHESIS_RESULTS)
    results = data['results']

    fig, axes = plt.subplots(1, 4, figsize=(14, 3))
    fig.suptitle('Panel 1: Program Synthesis in S-Entropy Space', fontsize=11, y=1.02)

    # Extract data
    s_k = [r['s_coords']['s_k'] for r in results]
    s_t = [r['s_coords']['s_t'] for r in results]
    s_e = [r['s_coords']['s_e'] for r in results]
    op_types = [r['operation_type'] for r in results]
    correct = [r['correct'] for r in results]
    distances = [r['distance'] for r in results]

    # Chart 1: S_k vs S_t scatter by operation type
    ax = axes[0]
    for op_type in COLORS:
        mask = [t == op_type for t in op_types]
        if any(mask):
            x = [s_k[i] for i in range(len(s_k)) if mask[i]]
            y = [s_t[i] for i in range(len(s_t)) if mask[i]]
            ax.scatter(x, y, c=COLORS[op_type], label=op_type, s=40, alpha=0.8, edgecolors='white', linewidth=0.5)
    ax.set_xlabel('$S_k$ (Knowledge)')
    ax.set_ylabel('$S_t$ (Temporal)')
    ax.set_xlim(-0.05, 1.0)
    ax.set_ylim(0, 0.8)
    ax.legend(loc='upper left', ncol=2, framealpha=0.9, fontsize=6)
    ax.set_title('(a) $S_k$ vs $S_t$')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 2: S_k vs S_e scatter
    ax = axes[1]
    for op_type in COLORS:
        mask = [t == op_type for t in op_types]
        if any(mask):
            x = [s_k[i] for i in range(len(s_k)) if mask[i]]
            y = [s_e[i] for i in range(len(s_e)) if mask[i]]
            ax.scatter(x, y, c=COLORS[op_type], s=40, alpha=0.8, edgecolors='white', linewidth=0.5)
    ax.set_xlabel('$S_k$ (Knowledge)')
    ax.set_ylabel('$S_e$ (Evolution)')
    ax.set_xlim(-0.05, 1.0)
    ax.set_ylim(0, 0.9)
    ax.set_title('(b) $S_k$ vs $S_e$')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 3: Accuracy by operation type
    ax = axes[2]
    stats = data['statistics']['by_operation_type']
    op_names = list(stats.keys())
    accuracies = [stats[op] * 100 for op in op_names]
    colors = [COLORS.get(op, '#888888') for op in op_names]
    bars = ax.bar(range(len(op_names)), accuracies, color=colors, edgecolor='white', linewidth=0.5)
    ax.set_xticks(range(len(op_names)))
    ax.set_xticklabels([op[:4] for op in op_names], rotation=45, ha='right')
    ax.set_ylabel('Accuracy (%)')
    ax.set_ylim(0, 105)
    ax.axhline(y=96.9, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_title('(c) Accuracy by Type')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    # Add value labels
    for bar, acc in zip(bars, accuracies):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{acc:.0f}', ha='center', va='bottom', fontsize=7)

    # Chart 4: Distance distribution histogram
    ax = axes[3]
    # Separate correct and incorrect
    dist_correct = [d for d, c in zip(distances, correct) if c and d < 0.5]
    dist_incorrect = [d for d, c in zip(distances, correct) if not c]

    ax.hist(dist_correct, bins=15, alpha=0.7, color='#2ca02c', label='Correct', edgecolor='white')
    if dist_incorrect:
        ax.hist(dist_incorrect, bins=5, alpha=0.7, color='#d62728', label='Incorrect', edgecolor='white')
    ax.set_xlabel('Euclidean Distance')
    ax.set_ylabel('Count')
    ax.set_title('(d) Navigation Distance')
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    plt.tight_layout()
    return fig


def create_panel_2_complexity():
    """Panel 2: Computational Complexity - 4 charts in a row"""
    data = load_json(COMPLEXITY_RESULTS)
    results = data['data']['results']

    fig, axes = plt.subplots(1, 4, figsize=(14, 3))
    fig.suptitle('Panel 2: Computational Complexity Scaling', fontsize=11, y=1.02)

    # Extract data
    sizes = [r['size'] for r in results]
    n_pixels = [r['n_pixels'] for r in results]
    matrix_elements = [r['matrix_elements'] for r in results]
    time_build = [r['time_build'] * 1000 for r in results]  # to ms
    time_svd = [r['time_svd'] * 1000 for r in results]
    time_recon = [r['time_reconstruction'] * 1000 for r in results]
    total_time = [r['total_time'] * 1000 for r in results]

    # Chart 1: Total time vs matrix size
    ax = axes[0]
    ax.plot(sizes, total_time, 'o-', color='#1f77b4', linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
    ax.set_xlabel('Matrix Size')
    ax.set_ylabel('Total Time (ms)')
    ax.set_title('(a) Scaling: Size vs Time')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 2: Log-log scaling plot
    ax = axes[1]
    log_sizes = np.log10(sizes)
    log_times = np.log10(total_time)
    ax.plot(log_sizes, log_times, 'o-', color='#ff7f0e', linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
    # Fit line
    coeffs = np.polyfit(log_sizes, log_times, 1)
    fit_line = np.poly1d(coeffs)
    ax.plot(log_sizes, fit_line(log_sizes), '--', color='red', linewidth=1.5, alpha=0.7)
    ax.set_xlabel('log$_{10}$(Size)')
    ax.set_ylabel('log$_{10}$(Time)')
    ax.set_title(f'(b) Log-Log: $O(n^{{{coeffs[0]:.2f}}})$')
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 3: Time breakdown stacked bar
    ax = axes[2]
    x = np.arange(len(sizes))
    width = 0.6
    ax.bar(x, time_build, width, label='Build', color='#2ca02c', edgecolor='white')
    ax.bar(x, time_svd, width, bottom=time_build, label='SVD', color='#d62728', edgecolor='white')
    ax.bar(x, time_recon, width, bottom=[b+s for b,s in zip(time_build, time_svd)], label='Reconstruct', color='#9467bd', edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_xlabel('Matrix Size')
    ax.set_ylabel('Time (ms)')
    ax.set_title('(c) Time Breakdown')
    ax.legend(loc='upper left', framealpha=0.9, fontsize=7)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Chart 4: Matrix elements vs time
    ax = axes[3]
    elements_millions = [e / 1e6 for e in matrix_elements]
    ax.plot(elements_millions, total_time, 's-', color='#8c564b', linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
    ax.set_xlabel('Matrix Elements (millions)')
    ax.set_ylabel('Time (ms)')
    ax.set_title('(d) Elements vs Time')
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    return fig


def create_panel_3_aberration():
    """Panel 3: Aberration Invariance - 4 charts in a row"""
    data = load_json(ABERRATION_RESULTS)
    results = data['data']['results']

    fig, axes = plt.subplots(1, 4, figsize=(14, 3))
    fig.suptitle('Panel 3: Aberration Invariance Analysis', fontsize=11, y=1.02)

    # Get unique aberrations and average across images
    aberrations = ['Perfect', 'Defocus', 'Astigmatism', 'Coma', 'Spherical', 'Mixed_mild', 'Mixed_strong', 'Extreme']
    aberration_colors = plt.cm.viridis(np.linspace(0, 0.9, len(aberrations)))

    # Aggregate by aberration type
    agg_data = {ab: {'psnr_ab': [], 'psnr_rec': [], 'mse_ab': [], 'mse_rec': [], 'psf': [], 'strength': []} for ab in aberrations}
    for r in results:
        ab = r['aberration']
        agg_data[ab]['psnr_ab'].append(r['psnr_aberrated'])
        agg_data[ab]['psnr_rec'].append(r['psnr_reconstructed'])
        agg_data[ab]['mse_ab'].append(r['mse_aberrated'])
        agg_data[ab]['mse_rec'].append(r['mse_reconstructed'])
        agg_data[ab]['psf'].append(r['psf_spread'])
        agg_data[ab]['strength'].append(r['aberration_strength'])

    # Chart 1: PSNR aberrated vs reconstructed
    ax = axes[0]
    x = np.arange(len(aberrations))
    width = 0.35
    psnr_ab_mean = [np.mean(agg_data[ab]['psnr_ab']) for ab in aberrations]
    psnr_rec_mean = [np.mean(agg_data[ab]['psnr_rec']) for ab in aberrations]
    ax.bar(x - width/2, psnr_ab_mean, width, label='Aberrated', color='#d62728', alpha=0.8, edgecolor='white')
    ax.bar(x + width/2, psnr_rec_mean, width, label='Reconstructed', color='#2ca02c', alpha=0.8, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels([ab[:4] for ab in aberrations], rotation=45, ha='right')
    ax.set_ylabel('PSNR (dB)')
    ax.set_title('(a) PSNR Comparison')
    ax.legend(loc='upper right', framealpha=0.9, fontsize=7)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Chart 2: Aberration strength vs PSNR improvement
    ax = axes[1]
    strengths = [np.mean(agg_data[ab]['strength']) for ab in aberrations]
    psnr_improvement = [np.mean(agg_data[ab]['psnr_rec']) - np.mean(agg_data[ab]['psnr_ab']) for ab in aberrations]
    for i, ab in enumerate(aberrations):
        ax.scatter(strengths[i], psnr_improvement[i], c=[aberration_colors[i]], s=100, label=ab[:4], edgecolors='white', linewidth=1)
    ax.set_xlabel('Aberration Strength')
    ax.set_ylabel('PSNR Change (dB)')
    ax.set_title('(b) Strength vs PSNR Change')
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 3: PSF spread by aberration type
    ax = axes[2]
    psf_means = [np.mean(agg_data[ab]['psf']) for ab in aberrations]
    bars = ax.bar(range(len(aberrations)), psf_means, color=aberration_colors, edgecolor='white', linewidth=0.5)
    ax.set_xticks(range(len(aberrations)))
    ax.set_xticklabels([ab[:4] for ab in aberrations], rotation=45, ha='right')
    ax.set_ylabel('PSF Spread')
    ax.set_title('(c) PSF Spread')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Chart 4: MSE comparison (log scale)
    ax = axes[3]
    mse_ab_mean = [np.mean(agg_data[ab]['mse_ab']) for ab in aberrations]
    mse_rec_mean = [np.mean(agg_data[ab]['mse_rec']) for ab in aberrations]
    ax.semilogy(range(len(aberrations)), mse_ab_mean, 'o-', color='#d62728', label='Aberrated', linewidth=2, markersize=6)
    ax.semilogy(range(len(aberrations)), mse_rec_mean, 's-', color='#2ca02c', label='Reconstructed', linewidth=2, markersize=6)
    ax.set_xticks(range(len(aberrations)))
    ax.set_xticklabels([ab[:4] for ab in aberrations], rotation=45, ha='right')
    ax.set_ylabel('MSE (log scale)')
    ax.set_title('(d) MSE Comparison')
    ax.legend(loc='upper left', framealpha=0.9, fontsize=7)
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    return fig


def create_panel_4_validation():
    """Panel 4: Validation & Algorithm Comparison - 4 charts in a row"""
    fig, axes = plt.subplots(1, 4, figsize=(14, 3))
    fig.suptitle('Panel 4: Backward vs Forward Complexity', fontsize=11, y=1.02)

    # Data from experiment 3
    sizes = [10, 50, 100, 500, 1000]
    forward_us = [8.00, 6.00, 4.40, 14.00, 9.70]
    backward_us = [54.60, 41.90, 41.20, 83.10, 83.20]
    theoretical_comparisons = [3.3, 5.6, 6.6, 9.0, 10.0]
    backward_comparisons = [6, 8, 9, 11, 12]

    # Chart 1: Forward vs Backward time
    ax = axes[0]
    x = np.arange(len(sizes))
    width = 0.35
    ax.bar(x - width/2, forward_us, width, label='Forward', color='#d62728', alpha=0.8, edgecolor='white')
    ax.bar(x + width/2, backward_us, width, label='Backward', color='#2ca02c', alpha=0.8, edgecolor='white')
    ax.set_xticks(x)
    ax.set_xticklabels(sizes)
    ax.set_xlabel('Library Size M')
    ax.set_ylabel(r'Time ($\mu$s)')
    ax.set_title('(a) Execution Time')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')

    # Chart 2: Scaling comparison
    ax = axes[1]
    ax.semilogx(sizes, forward_us, 'o-', color='#d62728', label='Forward', linewidth=2, markersize=8)
    ax.semilogx(sizes, backward_us, 's-', color='#2ca02c', label='Backward', linewidth=2, markersize=8)
    ax.set_xlabel('Library Size M (log)')
    ax.set_ylabel(r'Time ($\mu$s)')
    ax.set_title('(b) Log-Scale Scaling')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 3: Number of comparisons
    ax = axes[2]
    ax.plot(sizes, backward_comparisons, 'o-', color='#1f77b4', label='Measured', linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
    ax.plot(sizes, theoretical_comparisons, 's--', color='#ff7f0e', label='Theoretical log$_2$(M)', linewidth=2, markersize=8, alpha=0.7)
    # Add O(M) reference line (scaled)
    linear_ref = [s/100 for s in sizes]  # scaled for visibility
    ax.plot(sizes, linear_ref, ':', color='gray', label='O(M) ref', linewidth=1.5, alpha=0.5)
    ax.set_xlabel('Library Size M')
    ax.set_ylabel('Comparisons')
    ax.set_title('(c) Comparisons Count')
    ax.legend(loc='upper left', framealpha=0.9, fontsize=7)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Chart 4: Speedup potential at scale
    ax = axes[3]
    # Theoretical speedup: M / log2(M)
    large_sizes = [10, 100, 1000, 10000, 100000, 1000000]
    speedups = [m / np.log2(m) for m in large_sizes]
    ax.loglog(large_sizes, speedups, 'o-', color='#9467bd', linewidth=2, markersize=8, markerfacecolor='white', markeredgewidth=2)
    ax.set_xlabel('Library Size M')
    ax.set_ylabel('Theoretical Speedup')
    ax.set_title('(d) Speedup: $M / \\log_2 M$')
    ax.grid(True, alpha=0.3, linestyle='--')
    # Add annotation for key point
    ax.annotate(f'{speedups[-1]:.0f}x', xy=(large_sizes[-1], speedups[-1]),
                xytext=(large_sizes[-1]/5, speedups[-1]*1.5),
                arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7),
                fontsize=9, color='#9467bd')

    plt.tight_layout()
    return fig


def main():
    """Generate all panel figures"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating Panel 1: Program Synthesis...")
    fig1 = create_panel_1_synthesis()
    fig1.savefig(OUTPUT_DIR / "panel_1_synthesis.png", dpi=300, bbox_inches='tight', facecolor='white')
    fig1.savefig(OUTPUT_DIR / "panel_1_synthesis.pdf", bbox_inches='tight', facecolor='white')
    plt.close(fig1)

    print("Generating Panel 2: Computational Complexity...")
    fig2 = create_panel_2_complexity()
    fig2.savefig(OUTPUT_DIR / "panel_2_complexity.png", dpi=300, bbox_inches='tight', facecolor='white')
    fig2.savefig(OUTPUT_DIR / "panel_2_complexity.pdf", bbox_inches='tight', facecolor='white')
    plt.close(fig2)

    print("Generating Panel 3: Aberration Invariance...")
    fig3 = create_panel_3_aberration()
    fig3.savefig(OUTPUT_DIR / "panel_3_aberration.png", dpi=300, bbox_inches='tight', facecolor='white')
    fig3.savefig(OUTPUT_DIR / "panel_3_aberration.pdf", bbox_inches='tight', facecolor='white')
    plt.close(fig3)

    print("Generating Panel 4: Validation & Scaling...")
    fig4 = create_panel_4_validation()
    fig4.savefig(OUTPUT_DIR / "panel_4_validation.png", dpi=300, bbox_inches='tight', facecolor='white')
    fig4.savefig(OUTPUT_DIR / "panel_4_validation.pdf", bbox_inches='tight', facecolor='white')
    plt.close(fig4)

    print(f"\nAll panels saved to: {OUTPUT_DIR}")
    print("Files generated:")
    for f in OUTPUT_DIR.glob("panel_*.png"):
        print(f"  - {f.name}")


if __name__ == "__main__":
    main()
