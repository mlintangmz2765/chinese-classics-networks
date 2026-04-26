import networkx as nx
import community.community_louvain as community_louvain
import os

novels = ['three_kingdoms', 'water_margin', 'journey_west', 'red_chamber']
BACKBONE_THRESHOLD = 15

for novel in novels:
    file_name = f"network_{novel}.gexf"
    if not os.path.exists(file_name):
        continue
        
    print(f"\nProcessing Publication Graphs for {novel.upper()}...")
    
    G = nx.read_gexf(file_name)
    
    degree_dict = nx.degree_centrality(G)
    nx.set_node_attributes(G, degree_dict, 'degree_centrality')
    
    print(f"  -> Extracting Top 30 Characters...")
    sorted_nodes = sorted(degree_dict.keys(), key=lambda x: degree_dict[x], reverse=True)
    top_30_nodes = sorted_nodes[:30]
    
    G_top30 = G.subgraph(top_30_nodes).copy()
    
    partition_top30 = community_louvain.best_partition(G_top30, weight='weight')
    nx.set_node_attributes(G_top30, partition_top30, 'modularity_class')
    
    out_top30 = f"{novel}_top30_focus.gexf"
    nx.write_gexf(G_top30, out_top30)
    print(f"     Saved: {out_top30} (Nodes: {G_top30.number_of_nodes()}, Edges: {G_top30.number_of_edges()})")
    
    print(f"  -> Extracting Community Backbone (Threshold > {BACKBONE_THRESHOLD})...")
    G_backbone = G.copy()
    
    weak_edges = [(u, v) for u, v, d in G_backbone.edges(data=True) if d['weight'] < BACKBONE_THRESHOLD]
    G_backbone.remove_edges_from(weak_edges)
    
    isolated_nodes = list(nx.isolates(G_backbone))
    G_backbone.remove_nodes_from(isolated_nodes)
    
    if G_backbone.number_of_nodes() > 0:
        partition_backbone = community_louvain.best_partition(G_backbone, weight='weight')
        nx.set_node_attributes(G_backbone, partition_backbone, 'modularity_class')
    
    out_backbone = f"{novel}_community_backbone.gexf"
    nx.write_gexf(G_backbone, out_backbone)
    print(f"     Saved: {out_backbone} (Nodes: {G_backbone.number_of_nodes()}, Edges: {G_backbone.number_of_edges()})")

print("\n=== ALL PROCESSING COMPLETE ===")
print("These files are noise-free and include automatic color attributes (modularity_class).")
print("Ready for Gephi import and layouting.")
