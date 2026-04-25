import csv
import sys
import itertools
from collections import Counter
import networkx as nx

def main():
    if len(sys.argv) < 2:
        print("Usage: python 03_build_network.py [novel_name]")
        print("Example: python 03_build_network.py sanguo")
        return

    novel_arg = sys.argv[1].lower()
    
    if novel_arg == 'three_kingdoms':
        raw_file = "Sanguo_Yanyi_Raw.txt"
        csv_file = "entities_three_kingdoms_verified.csv"
        out_prefix = "three_kingdoms"
    elif novel_arg == 'water_margin':
        raw_file = "Shuihu_Zhuan_Raw.txt"
        csv_file = "entities_water_margin_verified.csv"
        out_prefix = "water_margin"
    elif novel_arg == 'journey_west':
        raw_file = "Xiyou_Ji_Raw.txt"
        csv_file = "entities_journey_west_verified.csv"
        out_prefix = "journey_west"
    elif novel_arg == 'red_chamber':
        raw_file = "Honglou_Meng_Raw.txt"
        csv_file = "entities_red_chamber_verified.csv"
        out_prefix = "red_chamber"
    else:
        print(f"Novel '{novel_arg}' not recognized. Choose: three_kingdoms, water_margin, journey_west, red_chamber")
        return

    print(f"=== Starting Network Build for {novel_arg.upper()} ===")
    
    print(f"Loading alias dictionary from {csv_file}...")
    alias_dict = {}
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) < 3: continue
                ext_name, freq, main_name = row[0], row[1], row[2]
                if main_name and main_name != 'NOISE':
                    alias_dict[ext_name] = main_name
    except FileNotFoundError:
        print(f"Error: {csv_file} not found!")
        return
        
    print(f"Successfully loaded {len(alias_dict)} valid entities.")

    print(f"Reading raw text {raw_file}...")
    with open(raw_file, 'r', encoding='utf-8') as f:
        paragraphs = f.read().split('\n')

    print(f"Processing {len(paragraphs)} paragraphs to find co-occurrences...")
    
    edge_weights = Counter()
    node_weights = Counter()

    search_keys = sorted(alias_dict.keys(), key=len, reverse=True)

    for para in paragraphs:
        if len(para.strip()) == 0:
            continue
            
        found_main_names = set()
        
        for ext_name in search_keys:
            if ext_name in para:
                found_main_names.add(alias_dict[ext_name])
                
        for name in found_main_names:
            node_weights[name] += 1
            
        if len(found_main_names) >= 2:
            pairs = itertools.combinations(list(found_main_names), 2)
            for pair in pairs:
                edge = tuple(sorted(pair))
                edge_weights[edge] += 1

    EDGE_WEIGHT_THRESHOLD = 3
    print(f"\nBuilding Network Graph (Removing interactions < {EDGE_WEIGHT_THRESHOLD} times)...")
    
    G = nx.Graph()
    
    for node, weight in node_weights.items():
        G.add_node(node, weight=weight)
        
    edge_count = 0
    for edge, weight in edge_weights.items():
        if weight >= EDGE_WEIGHT_THRESHOLD:
            G.add_edge(edge[0], edge[1], weight=weight)
            edge_count += 1
            
    isolated_nodes = list(nx.isolates(G))
    G.remove_nodes_from(isolated_nodes)
    
    print(f"Network Formed: {G.number_of_nodes()} Characters (Nodes) and {G.number_of_edges()} Connections (Edges).")

    csv_out = f"edgelist_{out_prefix}.csv"
    gexf_out = f"network_{out_prefix}.gexf"
    
    print(f"Saving to {csv_out}...")
    with open(csv_out, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Source', 'Target', 'Weight', 'Type'])
        for u, v, d in G.edges(data=True):
            writer.writerow([u, v, d['weight'], 'Undirected'])
            
    print(f"Saving to {gexf_out} (For Gephi)...")
    nx.write_gexf(G, gexf_out)
    
    print("=== PROCESS COMPLETE ===")
    
    print("\n[VERIFICATION] Top 5 Strongest Connections:")
    top_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:5]
    for i, (u, v, d) in enumerate(top_edges):
        try:
            print(f"{i+1}. {u} <---> {v} (Weight: {d['weight']})")
        except UnicodeEncodeError:
            print(f"{i+1}. [Hanzi Character] <---> [Hanzi Character] (Weight: {d['weight']})")

if __name__ == "__main__":
    main()
