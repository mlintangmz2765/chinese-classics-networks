"""
06_global_network_analysis.py
Computes global network properties, degree distribution analysis,
null model comparison, and small-world coefficients for all four novels.
Outputs results to CSV and generates degree distribution plots.
"""

import networkx as nx
import numpy as np
import csv
import os
import warnings
warnings.filterwarnings('ignore')


try:
    import powerlaw
    HAS_POWERLAW = True
except ImportError:
    HAS_POWERLAW = False
    print("WARNING: 'powerlaw' package not found. Install with: pip install powerlaw")
    print("Skipping power-law distribution fitting.\n")

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import LogLocator
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not found. Skipping plot generation.\n")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOVELS = {
    "Three Kingdoms": "network_three_kingdoms.gexf",
    "Water Margin": "network_water_margin.gexf",
    "Journey to the West": "network_journey_west.gexf",
    "Dream of the Red Chamber": "network_red_chamber.gexf",
}

NUM_RANDOM_TRIALS = 100


def load_network(filepath):
    """Load a GEXF network file."""
    G = nx.read_gexf(filepath)

    if G.is_directed():
        G = G.to_undirected()

    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G_connected = G.subgraph(largest_cc).copy()
        print(f"  Network not fully connected. Largest component: {len(G_connected)}/{len(G)} nodes")
    else:
        G_connected = G
    return G, G_connected


def compute_global_properties(G, G_connected):
    """Compute global network properties."""
    n = G.number_of_nodes()
    m = G.number_of_edges()
    density = nx.density(G)
    avg_degree = 2 * m / n if n > 0 else 0
    

    avg_clustering = nx.average_clustering(G)
    transitivity = nx.transitivity(G)
    

    avg_path_length = nx.average_shortest_path_length(G_connected)
    diameter = nx.diameter(G_connected)
    

    assortativity = nx.degree_assortativity_coefficient(G)
    
    return {
        "Nodes": n,
        "Edges": m,
        "Density": round(density, 4),
        "Average Degree": round(avg_degree, 2),
        "Avg. Clustering Coefficient": round(avg_clustering, 4),
        "Transitivity": round(transitivity, 4),
        "Avg. Path Length": round(avg_path_length, 4),
        "Diameter": diameter,
        "Assortativity": round(assortativity, 4),
    }


def compute_null_models(G, G_connected, num_trials=100):
    """Compare with Erdős-Rényi and Barabási-Albert random graph models."""
    n = G.number_of_nodes()
    m = G.number_of_edges()
    
    C_real = nx.average_clustering(G)
    L_real = nx.average_shortest_path_length(G_connected)
    

    p = 2 * m / (n * (n - 1)) if n > 1 else 0
    er_clustering = []
    er_path_length = []
    
    for _ in range(num_trials):
        G_er = nx.erdos_renyi_graph(n, p)
        if nx.is_connected(G_er):
            er_clustering.append(nx.average_clustering(G_er))
            er_path_length.append(nx.average_shortest_path_length(G_er))
    
    C_random = np.mean(er_clustering) if er_clustering else p
    L_random = np.mean(er_path_length) if er_path_length else np.log(n) / np.log(n * p) if n * p > 1 else float('inf')
    

    gamma = C_real / C_random if C_random > 0 else float('inf')
    lam = L_real / L_random if L_random > 0 else float('inf')
    sigma = gamma / lam if lam > 0 else float('inf')
    
    m_ba = max(1, round(m / n))
    ba_clustering = []
    ba_path_length = []
    
    for _ in range(num_trials):
        try:
            G_ba = nx.barabasi_albert_graph(n, min(m_ba, n-1))
            if nx.is_connected(G_ba):
                ba_clustering.append(nx.average_clustering(G_ba))
                ba_path_length.append(nx.average_shortest_path_length(G_ba))
        except:
            pass
    
    C_ba = np.mean(ba_clustering) if ba_clustering else 0
    L_ba = np.mean(ba_path_length) if ba_path_length else 0
    
    return {
        "C_real": round(C_real, 4),
        "C_ER": round(C_random, 4),
        "C_BA": round(C_ba, 4),
        "L_real": round(L_real, 4),
        "L_ER": round(L_random, 4),
        "L_BA": round(L_ba, 4),
        "gamma (C_real/C_ER)": round(gamma, 4),
        "lambda (L_real/L_ER)": round(lam, 4),
        "sigma (small-world)": round(sigma, 4),
    }


def compute_degree_distribution(G):
    """Compute degree distribution and fit power-law if available."""
    degrees = [d for _, d in G.degree()]
    degree_seq = sorted(degrees, reverse=True)
    
    result = {
        "min_degree": min(degrees),
        "max_degree": max(degrees),
        "mean_degree": round(np.mean(degrees), 2),
        "std_degree": round(np.std(degrees), 2),
        "median_degree": round(np.median(degrees), 2),
    }
    
    if HAS_POWERLAW and len(degrees) > 10:
        fit = powerlaw.Fit(degrees, discrete=True, verbose=False)
        result["power_law_alpha"] = round(fit.power_law.alpha, 4)
        result["power_law_xmin"] = fit.power_law.xmin
        

        R_exp, p_exp = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
        R_ln, p_ln = fit.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
        
        result["pl_vs_exp_R"] = round(R_exp, 4)
        result["pl_vs_exp_p"] = round(p_exp, 4)
        result["pl_vs_lognormal_R"] = round(R_ln, 4)
        result["pl_vs_lognormal_p"] = round(p_ln, 4)
    
    return result, degrees


def compute_robustness(G):
    """Compute network robustness under targeted and random node removal."""
    n = G.number_of_nodes()
    
    G_targeted = G.copy()
    targeted_sizes = [1.0]
    
    nodes_by_degree = sorted(G.degree(), key=lambda x: x[1], reverse=True)
    removal_steps = max(1, n // 10)
    
    for i in range(0, min(n - 1, n // 2), max(1, removal_steps)):
        if i < len(nodes_by_degree):
            node_to_remove = nodes_by_degree[i][0]
            if node_to_remove in G_targeted:
                G_targeted.remove_node(node_to_remove)
                if len(G_targeted) > 0:
                    largest_cc = max(nx.connected_components(G_targeted), key=len)
                    targeted_sizes.append(len(largest_cc) / n)
                else:
                    targeted_sizes.append(0)
    

    random_sizes = [1.0]
    G_random = G.copy()
    nodes_list = list(G_random.nodes())
    np.random.shuffle(nodes_list)
    
    for i in range(0, min(n - 1, n // 2), max(1, removal_steps)):
        if i < len(nodes_list):
            if nodes_list[i] in G_random:
                G_random.remove_node(nodes_list[i])
                if len(G_random) > 0:
                    largest_cc = max(nx.connected_components(G_random), key=len)
                    random_sizes.append(len(largest_cc) / n)
                else:
                    random_sizes.append(0)
    

    targeted_robustness = round(np.trapz(targeted_sizes) / len(targeted_sizes), 4) if targeted_sizes else 0
    random_robustness = round(np.trapz(random_sizes) / len(random_sizes), 4) if random_sizes else 0
    
    return {
        "Targeted Robustness (AUC)": targeted_robustness,
        "Random Robustness (AUC)": random_robustness,
        "Robustness Ratio (T/R)": round(targeted_robustness / random_robustness, 4) if random_robustness > 0 else 0,
    }


def plot_degree_distributions(all_degrees, output_path):
    """Generate 4-panel degree distribution plot."""
    if not HAS_MATPLOTLIB:
        print("Skipping plot generation (matplotlib not available)")
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    novel_names = list(all_degrees.keys())
    colors = ['#2166ac', '#b2182b', '#1b7837', '#762a83']
    
    for idx, (ax, novel) in enumerate(zip(axes.flatten(), novel_names)):
        degrees = all_degrees[novel]
        

        unique, counts = np.unique(degrees, return_counts=True)
        freq = counts / counts.sum()
        

        sorted_degrees = np.sort(degrees)[::-1]
        ccdf = np.arange(1, len(sorted_degrees) + 1) / len(sorted_degrees)
        
        ax.loglog(sorted_degrees, ccdf, 'o', color=colors[idx], markersize=5, alpha=0.7, label='Empirical CCDF')
        

        if HAS_POWERLAW and len(degrees) > 10:
            fit = powerlaw.Fit(degrees, discrete=True, verbose=False)
            alpha = fit.power_law.alpha
            xmin = fit.power_law.xmin
            

            x_fit = np.linspace(xmin, max(degrees), 100)
            y_fit = (x_fit / xmin) ** (1 - alpha)
            ax.loglog(x_fit, y_fit, '--', color='black', linewidth=1.5, 
                     label=f'Power-law fit (α={alpha:.2f})')
        
        ax.set_xlabel('Degree (k)', fontsize=11)
        ax.set_ylabel('P(K ≥ k)', fontsize=11)
        ax.set_title(novel, fontsize=12, fontweight='bold')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  Saved degree distribution plot to: {output_path}")


def main():
    print("=" * 70)
    print("GLOBAL NETWORK ANALYSIS FOR DSH PAPER")
    print("=" * 70)
    
    all_global = {}
    all_null = {}
    all_degree = {}
    all_degree_raw = {}
    all_robustness = {}
    
    for novel, filename in NOVELS.items():
        filepath = os.path.join(BASE_DIR, filename)
        print(f"\n{'─' * 60}")
        print(f"Processing: {novel}")
        print(f"{'─' * 60}")
        
        if not os.path.exists(filepath):
            print(f"  ERROR: File not found: {filepath}")
            continue
        
        G, G_connected = load_network(filepath)
        print(f"  Loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        

        print("  Computing global properties...")
        global_props = compute_global_properties(G, G_connected)
        all_global[novel] = global_props
        for k, v in global_props.items():
            print(f"    {k}: {v}")
        

        print(f"  Computing null models ({NUM_RANDOM_TRIALS} trials)...")
        null_props = compute_null_models(G, G_connected, NUM_RANDOM_TRIALS)
        all_null[novel] = null_props
        for k, v in null_props.items():
            print(f"    {k}: {v}")
        

        print("  Computing degree distribution...")
        degree_props, degrees = compute_degree_distribution(G)
        all_degree[novel] = degree_props
        all_degree_raw[novel] = degrees
        for k, v in degree_props.items():
            print(f"    {k}: {v}")
        

        print("  Computing robustness...")
        robustness = compute_robustness(G)
        all_robustness[novel] = robustness
        for k, v in robustness.items():
            print(f"    {k}: {v}")
    

    print(f"\n{'=' * 70}")
    print("SAVING RESULTS")
    print(f"{'=' * 70}")
    

    csv_path = os.path.join(BASE_DIR, "global_network_properties.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        headers = ["Novel"] + list(list(all_global.values())[0].keys())
        writer.writerow(headers)
        for novel, props in all_global.items():
            writer.writerow([novel] + list(props.values()))
    print(f"  Saved: {csv_path}")
    

    csv_path = os.path.join(BASE_DIR, "null_model_comparison.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        headers = ["Novel"] + list(list(all_null.values())[0].keys())
        writer.writerow(headers)
        for novel, props in all_null.items():
            writer.writerow([novel] + list(props.values()))
    print(f"  Saved: {csv_path}")
    

    csv_path = os.path.join(BASE_DIR, "degree_distribution_analysis.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        headers = ["Novel"] + list(list(all_degree.values())[0].keys())
        writer.writerow(headers)
        for novel, props in all_degree.items():
            writer.writerow([novel] + list(props.values()))
    print(f"  Saved: {csv_path}")
    

    csv_path = os.path.join(BASE_DIR, "robustness_analysis.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        headers = ["Novel"] + list(list(all_robustness.values())[0].keys())
        writer.writerow(headers)
        for novel, props in all_robustness.items():
            writer.writerow([novel] + list(props.values()))
    print(f"  Saved: {csv_path}")
    

    plot_path = os.path.join(BASE_DIR, "degree_distribution_plot.png")
    plot_degree_distributions(all_degree_raw, plot_path)
    

    print(f"\n{'=' * 70}")
    print("SUMMARY TABLE FOR PAPER")
    print(f"{'=' * 70}")
    print(f"\n{'Property':<35} {'Three Kingdoms':>15} {'Water Margin':>15} {'Journey West':>15} {'Red Chamber':>15}")
    print("─" * 95)
    
    all_props = ["Nodes", "Edges", "Density", "Average Degree", 
                 "Avg. Clustering Coefficient", "Transitivity",
                 "Avg. Path Length", "Diameter", "Assortativity"]
    
    for prop in all_props:
        vals = []
        for novel in NOVELS:
            if novel in all_global:
                vals.append(str(all_global[novel].get(prop, "N/A")))
            else:
                vals.append("N/A")
        print(f"{prop:<35} {vals[0]:>15} {vals[1]:>15} {vals[2]:>15} {vals[3]:>15}")
    
    print("\nSmall-World Analysis:")
    print(f"{'Property':<35} {'Three Kingdoms':>15} {'Water Margin':>15} {'Journey West':>15} {'Red Chamber':>15}")
    print("─" * 95)
    
    sw_props = ["sigma (small-world)", "gamma (C_real/C_ER)", "lambda (L_real/L_ER)"]
    for prop in sw_props:
        vals = []
        for novel in NOVELS:
            if novel in all_null:
                vals.append(str(all_null[novel].get(prop, "N/A")))
            else:
                vals.append("N/A")
        print(f"{prop:<35} {vals[0]:>15} {vals[1]:>15} {vals[2]:>15} {vals[3]:>15}")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
