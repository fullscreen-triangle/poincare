"""
Generate visualization panels for Poincaré Computing paper.
Each panel contains 4 charts in a row with at least one 3D chart.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyBboxPatch
import matplotlib.colors as mcolors
from pathlib import Path

# Set publication-quality defaults
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 8,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.linewidth': 0.8,
})

# Load data
data_path = Path(__file__).parent.parent.parent.parent / "examples" / "program_synthesis" / "results" / "extended_results_20260227_050058.json"
with open(data_path, 'r') as f:
    data = json.load(f)

results = data['results']

# Extract data
programs = [r['expected_program'] for r in results]
s_k = np.array([r['s_coords']['s_k'] for r in results])
s_t = np.array([r['s_coords']['s_t'] for r in results])
s_e = np.array([r['s_coords']['s_e'] for r in results])
operation_types = [r['operation_type'] for r in results]
correct = np.array([r['correct'] for r in results])
distances = np.array([r['distance'] for r in results])

# Color map for operation types
type_colors = {
    'aggregation': '#2ecc71',
    'access': '#3498db',
    'transformation': '#9b59b6',
    'arithmetic': '#e74c3c',
    'conditional': '#f39c12',
    'composition': '#1abc9c',
    'recursive': '#e91e63'
}

colors = [type_colors[t] for t in operation_types]

# ==============================================================================
# PANEL 1: S-Entropy Space Structure
# ==============================================================================
def create_panel_1():
    fig = plt.figure(figsize=(16, 4))

    # Chart 1: 3D S-Space scatter (all programs)
    ax1 = fig.add_subplot(141, projection='3d')
    for op_type in type_colors:
        mask = np.array([t == op_type for t in operation_types])
        if mask.any():
            ax1.scatter(s_k[mask], s_t[mask], s_e[mask],
                       c=type_colors[op_type], s=60, alpha=0.8,
                       edgecolors='white', linewidth=0.5, label=op_type)
    ax1.set_xlabel('$S_k$', labelpad=8)
    ax1.set_ylabel('$S_t$', labelpad=8)
    ax1.set_zlabel('$S_e$', labelpad=8)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_zlim(0, 1)
    ax1.view_init(elev=20, azim=45)
    ax1.set_title('(a)', fontweight='bold', loc='left')

    # Chart 2: S_k vs S_t projection
    ax2 = fig.add_subplot(142)
    for op_type in type_colors:
        mask = np.array([t == op_type for t in operation_types])
        if mask.any():
            ax2.scatter(s_k[mask], s_t[mask], c=type_colors[op_type],
                       s=80, alpha=0.8, edgecolors='white', linewidth=0.5)
    ax2.set_xlabel('$S_k$ (Knowledge)')
    ax2.set_ylabel('$S_t$ (Temporal)')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 0.8)
    ax2.grid(True, alpha=0.3)
    ax2.set_title('(b)', fontweight='bold', loc='left')

    # Chart 3: S_k vs S_e projection
    ax3 = fig.add_subplot(143)
    for op_type in type_colors:
        mask = np.array([t == op_type for t in operation_types])
        if mask.any():
            ax3.scatter(s_k[mask], s_e[mask], c=type_colors[op_type],
                       s=80, alpha=0.8, edgecolors='white', linewidth=0.5)
    ax3.set_xlabel('$S_k$ (Knowledge)')
    ax3.set_ylabel('$S_e$ (Evolution)')
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 0.9)
    ax3.grid(True, alpha=0.3)
    ax3.set_title('(c)', fontweight='bold', loc='left')

    # Chart 4: S_t vs S_e projection
    ax4 = fig.add_subplot(144)
    for op_type in type_colors:
        mask = np.array([t == op_type for t in operation_types])
        if mask.any():
            ax4.scatter(s_t[mask], s_e[mask], c=type_colors[op_type],
                       s=80, alpha=0.8, edgecolors='white', linewidth=0.5,
                       label=op_type.capitalize())
    ax4.set_xlabel('$S_t$ (Temporal)')
    ax4.set_ylabel('$S_e$ (Evolution)')
    ax4.set_xlim(0, 0.8)
    ax4.set_ylim(0, 0.9)
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='upper left', framealpha=0.9, ncol=2)
    ax4.set_title('(d)', fontweight='bold', loc='left')

    plt.tight_layout()
    fig.savefig('panel_1_s_entropy_space.pdf')
    fig.savefig('panel_1_s_entropy_space.png', dpi=300)
    plt.close()
    print("Panel 1 saved: S-Entropy Space Structure")

# ==============================================================================
# PANEL 2: Clustering & Synthesis Accuracy
# ==============================================================================
def create_panel_2():
    fig = plt.figure(figsize=(16, 4))

    # Chart 1: 3D with correct/incorrect highlighting
    ax1 = fig.add_subplot(141, projection='3d')
    # Plot correct ones
    correct_mask = correct
    ax1.scatter(s_k[correct_mask], s_t[correct_mask], s_e[correct_mask],
               c=[type_colors[t] for i, t in enumerate(operation_types) if correct[i]],
               s=60, alpha=0.8, edgecolors='white', linewidth=0.5, marker='o')
    # Plot incorrect ones
    incorrect_mask = ~correct
    if incorrect_mask.any():
        ax1.scatter(s_k[incorrect_mask], s_t[incorrect_mask], s_e[incorrect_mask],
                   c='black', s=120, alpha=1.0, marker='X', label='Incorrect')
    ax1.set_xlabel('$S_k$', labelpad=8)
    ax1.set_ylabel('$S_t$', labelpad=8)
    ax1.set_zlabel('$S_e$', labelpad=8)
    ax1.view_init(elev=25, azim=135)
    ax1.set_title('(a)', fontweight='bold', loc='left')

    # Chart 2: Cluster separation - S_k ranges by operation type
    ax2 = fig.add_subplot(142)
    op_types_unique = list(type_colors.keys())
    s_k_ranges = []
    for op in op_types_unique:
        mask = np.array([t == op for t in operation_types])
        if mask.any():
            s_k_ranges.append((s_k[mask].min(), s_k[mask].max(), s_k[mask].mean()))
        else:
            s_k_ranges.append((0, 0, 0))

    y_pos = np.arange(len(op_types_unique))
    for i, (op, (lo, hi, mean)) in enumerate(zip(op_types_unique, s_k_ranges)):
        ax2.barh(i, hi - lo, left=lo, height=0.6, color=type_colors[op], alpha=0.8)
        ax2.plot([mean], [i], 'k|', markersize=15, markeredgewidth=2)
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels([op.capitalize() for op in op_types_unique])
    ax2.set_xlabel('$S_k$ Range')
    ax2.set_xlim(0, 1)
    ax2.set_title('(b)', fontweight='bold', loc='left')

    # Chart 3: Distance histogram
    ax3 = fig.add_subplot(143)
    ax3.hist(distances[distances == 0], bins=1, color='#2ecc71', alpha=0.8,
             edgecolor='white', label=f'd=0 (n={np.sum(distances==0)})')
    if np.any(distances > 0):
        ax3.hist(distances[distances > 0], bins=10, color='#e74c3c', alpha=0.8,
                edgecolor='white', label=f'd>0 (n={np.sum(distances>0)})')
    ax3.set_xlabel('S-Space Distance')
    ax3.set_ylabel('Count')
    ax3.set_xlim(-0.1, 1.3)
    ax3.legend()
    ax3.set_title('(c)', fontweight='bold', loc='left')

    # Chart 4: Inter vs Intra cluster distance
    ax4 = fig.add_subplot(144)
    # Calculate intra-cluster distances
    intra_dists = []
    inter_dists = []
    for i in range(len(s_k)):
        for j in range(i+1, len(s_k)):
            d = np.sqrt((s_k[i]-s_k[j])**2 + (s_t[i]-s_t[j])**2 + (s_e[i]-s_e[j])**2)
            if operation_types[i] == operation_types[j]:
                intra_dists.append(d)
            else:
                inter_dists.append(d)

    bp = ax4.boxplot([intra_dists, inter_dists],
                     labels=['Intra-cluster', 'Inter-cluster'],
                     patch_artist=True)
    bp['boxes'][0].set_facecolor('#3498db')
    bp['boxes'][1].set_facecolor('#e74c3c')
    for box in bp['boxes']:
        box.set_alpha(0.7)
    ax4.set_ylabel('S-Space Distance')
    ratio = np.mean(inter_dists) / np.mean(intra_dists)
    ax4.axhline(np.mean(inter_dists), color='#e74c3c', linestyle='--', alpha=0.5)
    ax4.axhline(np.mean(intra_dists), color='#3498db', linestyle='--', alpha=0.5)
    ax4.text(1.5, np.mean(inter_dists)+0.02, f'Ratio: {ratio:.1f}×', ha='center', fontsize=9)
    ax4.set_title('(d)', fontweight='bold', loc='left')

    plt.tight_layout()
    fig.savefig('panel_2_clustering_accuracy.pdf')
    fig.savefig('panel_2_clustering_accuracy.png', dpi=300)
    plt.close()
    print("Panel 2 saved: Clustering & Synthesis Accuracy")

# ==============================================================================
# PANEL 3: Backward Navigation & Complexity
# ==============================================================================
def create_panel_3():
    fig = plt.figure(figsize=(16, 4))

    # Chart 1: 3D backward trajectory visualization
    ax1 = fig.add_subplot(141, projection='3d')

    # Create k-d tree partition visualization
    # Draw ternary partition grid at different depths
    for depth in [1, 2]:
        step = 1.0 / (3 ** depth)
        for i in np.arange(0, 1+step, step):
            ax1.plot([i, i], [0, 1], [0, 0], 'gray', alpha=0.2, linewidth=0.5)
            ax1.plot([0, 1], [i, i], [0, 0], 'gray', alpha=0.2, linewidth=0.5)

    # Plot programs as points
    ax1.scatter(s_k, s_t, s_e, c=colors, s=50, alpha=0.8, edgecolors='white', linewidth=0.5)

    # Draw example trajectory arrow (from query point to nearest)
    query = [0.52, 0.12, 0.16]  # Example query near 'add'
    target_idx = 10  # 'add' program
    ax1.plot([query[0], s_k[target_idx]],
             [query[1], s_t[target_idx]],
             [query[2], s_e[target_idx]],
             'k-', linewidth=2, alpha=0.8)
    ax1.scatter([query[0]], [query[1]], [query[2]], c='red', s=100, marker='*', zorder=10)

    ax1.set_xlabel('$S_k$', labelpad=8)
    ax1.set_ylabel('$S_t$', labelpad=8)
    ax1.set_zlabel('$S_e$', labelpad=8)
    ax1.view_init(elev=20, azim=60)
    ax1.set_title('(a)', fontweight='bold', loc='left')

    # Chart 2: Complexity scaling O(log M)
    ax2 = fig.add_subplot(142)
    M_values = np.array([10, 48, 100, 1000, 10000, 100000, 1e6, 1e7, 1e8, 1e9, 1e10])
    forward_time = M_values  # O(M)
    backward_time = np.log2(M_values)  # O(log M)

    ax2.semilogy(np.log10(M_values), forward_time, 'r-o', linewidth=2,
                 markersize=6, label='Forward $O(M)$')
    ax2.semilogy(np.log10(M_values), backward_time, 'g-s', linewidth=2,
                 markersize=6, label='Backward $O(\\log M)$')
    ax2.fill_between(np.log10(M_values), backward_time, forward_time,
                     color='green', alpha=0.1)
    ax2.axvline(np.log10(48), color='blue', linestyle='--', alpha=0.5)
    ax2.text(np.log10(48)+0.2, 1e6, 'M=48', fontsize=9, color='blue')
    ax2.set_xlabel('$\\log_{10}(M)$')
    ax2.set_ylabel('Operations')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_title('(b)', fontweight='bold', loc='left')

    # Chart 3: K-d tree depth visualization
    ax3 = fig.add_subplot(143)
    depths = np.arange(1, 8)
    nodes_per_depth = 2 ** depths
    cumulative_nodes = np.cumsum(nodes_per_depth)

    ax3.bar(depths, nodes_per_depth, color='#3498db', alpha=0.8,
            edgecolor='white', label='Nodes at depth')
    ax3.plot(depths, cumulative_nodes, 'ro-', linewidth=2, markersize=6,
             label='Cumulative')
    ax3.axhline(48, color='green', linestyle='--', alpha=0.7, label='M=48')
    ax3.fill_between(depths, 0, nodes_per_depth, where=cumulative_nodes <= 48,
                     color='green', alpha=0.2)
    ax3.set_xlabel('Tree Depth')
    ax3.set_ylabel('Nodes')
    ax3.set_xticks(depths)
    ax3.legend(loc='upper left')
    ax3.set_title('(c)', fontweight='bold', loc='left')

    # Chart 4: Speedup factor
    ax4 = fig.add_subplot(144)
    speedup = M_values / np.log2(M_values)
    ax4.loglog(M_values, speedup, 'b-o', linewidth=2, markersize=6)
    ax4.axvline(48, color='green', linestyle='--', alpha=0.5)
    ax4.axhline(48/np.log2(48), color='green', linestyle='--', alpha=0.5)
    ax4.scatter([48], [48/np.log2(48)], c='green', s=100, zorder=10)
    ax4.text(48*2, 48/np.log2(48), f'{48/np.log2(48):.1f}×', fontsize=10, color='green')
    ax4.axhline(3e8, color='red', linestyle=':', alpha=0.5)
    ax4.text(1e8, 5e8, '$3×10^8$× at $M=10^{10}$', fontsize=9, color='red')
    ax4.set_xlabel('Library Size $M$')
    ax4.set_ylabel('Speedup $(M / \\log M)$')
    ax4.grid(True, alpha=0.3, which='both')
    ax4.set_title('(d)', fontweight='bold', loc='left')

    plt.tight_layout()
    fig.savefig('panel_3_complexity_navigation.pdf')
    fig.savefig('panel_3_complexity_navigation.png', dpi=300)
    plt.close()
    print("Panel 3 saved: Backward Navigation & Complexity")

# ==============================================================================
# PANEL 4: Partition Structure & Capacity
# ==============================================================================
def create_panel_4():
    fig = plt.figure(figsize=(16, 4))

    # Chart 1: 3D ternary partition hierarchy
    ax1 = fig.add_subplot(141, projection='3d')

    # Create hierarchical ternary grid visualization
    # Level 0: full cube
    # Level 1: subdivide into 27 cells
    colors_ternary = plt.cm.viridis(np.linspace(0.2, 0.9, 27))

    # Draw ternary cells at depth 1
    cell_idx = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                x = i / 3
                y = j / 3
                z = k / 3
                # Draw cell corners
                ax1.scatter([x + 1/6], [y + 1/6], [z + 1/6],
                           c=[colors_ternary[cell_idx]], s=30, alpha=0.6)
                cell_idx += 1

    # Overlay programs
    ax1.scatter(s_k, s_t, s_e, c='red', s=80, alpha=0.9,
               edgecolors='white', linewidth=1, marker='o')

    # Draw partition lines
    for val in [1/3, 2/3]:
        ax1.plot([val, val], [0, 1], [0, 0], 'k-', alpha=0.3, linewidth=1)
        ax1.plot([0, 1], [val, val], [0, 0], 'k-', alpha=0.3, linewidth=1)
        ax1.plot([val, val], [0, 0], [0, 1], 'k-', alpha=0.3, linewidth=1)
        ax1.plot([0, 0], [val, val], [0, 1], 'k-', alpha=0.3, linewidth=1)

    ax1.set_xlabel('$S_k$', labelpad=8)
    ax1.set_ylabel('$S_t$', labelpad=8)
    ax1.set_zlabel('$S_e$', labelpad=8)
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_zlim(0, 1)
    ax1.view_init(elev=25, azim=30)
    ax1.set_title('(a)', fontweight='bold', loc='left')

    # Chart 2: C(n) = 2n² capacity formula
    ax2 = fig.add_subplot(142)
    n_values = np.arange(1, 11)
    capacity = 2 * n_values ** 2
    cumulative = np.cumsum(capacity)

    ax2.bar(n_values - 0.2, capacity, width=0.4, color='#3498db',
            alpha=0.8, label='$C(n) = 2n^2$')
    ax2.plot(n_values, cumulative, 'ro-', linewidth=2, markersize=8,
             label='Cumulative')

    # Mark validation points
    ax2.axhline(32, color='green', linestyle='--', alpha=0.5)
    ax2.axhline(50, color='green', linestyle='--', alpha=0.5)
    ax2.axhline(72, color='green', linestyle='--', alpha=0.5)

    ax2.set_xlabel('Principal Quantum Number $n$')
    ax2.set_ylabel('States')
    ax2.legend(loc='upper left')
    ax2.set_xticks(n_values)
    ax2.set_title('(b)', fontweight='bold', loc='left')

    # Chart 3: Ternary address distribution
    ax3 = fig.add_subplot(143)

    # Convert S-coordinates to ternary addresses (depth 2)
    def to_ternary(val, depth=2):
        address = []
        for d in range(depth):
            digit = int(val * 3)
            if digit > 2:
                digit = 2
            address.append(digit)
            val = val * 3 - digit
        return tuple(address)

    # Count programs per ternary cell
    ternary_counts = {}
    for i in range(len(s_k)):
        addr = (to_ternary(s_k[i])[0], to_ternary(s_t[i])[0], to_ternary(s_e[i])[0])
        ternary_counts[addr] = ternary_counts.get(addr, 0) + 1

    # Create heatmap data
    heatmap = np.zeros((3, 3))
    for (i, j, k), count in ternary_counts.items():
        heatmap[i, j] += count

    im = ax3.imshow(heatmap, cmap='YlOrRd', aspect='equal')
    ax3.set_xlabel('$t_{t,1}$ (Temporal trit)')
    ax3.set_ylabel('$t_{k,1}$ (Knowledge trit)')
    ax3.set_xticks([0, 1, 2])
    ax3.set_yticks([0, 1, 2])
    ax3.set_xticklabels(['0', '1', '2'])
    ax3.set_yticklabels(['0', '1', '2'])

    # Add count annotations
    for i in range(3):
        for j in range(3):
            ax3.text(j, i, f'{int(heatmap[i, j])}', ha='center', va='center',
                    color='white' if heatmap[i, j] > 5 else 'black', fontsize=11, fontweight='bold')

    ax3.set_title('(c)', fontweight='bold', loc='left')

    # Chart 4: Validation accuracy by platform (mass spec + program synthesis)
    ax4 = fig.add_subplot(144)

    domains = ['HMDB\nMetab.', 'LIPID\nMAPS', 'Mass\nBank', 'Program\nSynth.']
    accuracies = [99.4, 99.1, 98.7, 96.875]
    compounds = [2847, 892, 532, 32]

    bars = ax4.bar(domains, accuracies, color=['#3498db', '#2ecc71', '#e74c3c', '#9b59b6'],
                   alpha=0.8, edgecolor='white')

    # Add compound counts
    for bar, count in zip(bars, compounds):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2, height - 3,
                f'n={count}', ha='center', va='top', color='white', fontsize=9, fontweight='bold')

    ax4.set_ylabel('Accuracy (%)')
    ax4.set_ylim(90, 102)
    ax4.axhline(96.3, color='black', linestyle='--', alpha=0.5)
    ax4.text(3.5, 96.8, 'Mean: 96.3%', fontsize=9)
    ax4.set_title('(d)', fontweight='bold', loc='left')

    plt.tight_layout()
    fig.savefig('panel_4_partition_structure.pdf')
    fig.savefig('panel_4_partition_structure.png', dpi=300)
    plt.close()
    print("Panel 4 saved: Partition Structure & Capacity")

# ==============================================================================
# Generate all panels
# ==============================================================================
if __name__ == "__main__":
    print("Generating visualization panels for Poincaré Computing paper...")
    print("=" * 60)

    create_panel_1()
    create_panel_2()
    create_panel_3()
    create_panel_4()

    print("=" * 60)
    print("All panels generated successfully!")
    print("\nOutput files:")
    print("  - panel_1_s_entropy_space.pdf/png")
    print("  - panel_2_clustering_accuracy.pdf/png")
    print("  - panel_3_complexity_navigation.pdf/png")
    print("  - panel_4_partition_structure.pdf/png")
