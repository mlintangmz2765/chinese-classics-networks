import networkx as nx
import csv

novels = ['three_kingdoms', 'water_margin', 'journey_west', 'red_chamber']
all_results = []

for novel in novels:
    gexf_file = f"network_{novel}.gexf"
    try:
        G = nx.read_gexf(gexf_file)
        print(f"Calculating metrics for {novel.upper()}...")
    except FileNotFoundError:
        print(f"File {gexf_file} not found, skipping...")
        continue
    
    deg = nx.degree_centrality(G)
    
    bet = nx.betweenness_centrality(G)
    
    try:
        eig = nx.eigenvector_centrality(G, max_iter=2000, weight='weight')
    except (nx.PowerIterationFailedConvergence, ValueError):
        eig = nx.eigenvector_centrality(G, max_iter=2000)

    sorted_chars = sorted(deg.keys(), key=lambda x: deg[x], reverse=True)
    
    top_15 = sorted_chars[:15]
    for rank, char in enumerate(top_15):
        all_results.append({
            'Novel': novel.upper(),
            'Rank': rank + 1,
            'Character': char,
            'Degree_Centrality': round(deg[char], 4),
            'Betweenness_Centrality': round(bet[char], 4),
            'Eigenvector_Centrality': round(eig[char], 4)
        })

csv_out = 'centrality_metrics_summary.csv'
with open(csv_out, 'w', encoding='utf-8', newline='') as f:
    fields = ['Novel', 'Rank', 'Character', 'Degree_Centrality', 'Betweenness_Centrality', 'Eigenvector_Centrality']
    writer = csv.DictWriter(f, fieldnames=fields)
    writer.writeheader()
    writer.writerows(all_results)

print(f"\nDone! Metrics table exported to: {csv_out}")
