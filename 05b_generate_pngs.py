import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text
from matplotlib.lines import Line2D
import os
from pypinyin import pinyin, Style

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

novels = ['three_kingdoms', 'water_margin', 'journey_west', 'red_chamber']

NOVEL_DISPLAY_NAMES = {
    'three_kingdoms': 'Romance of the Three Kingdoms',
    'water_margin': 'Water Margin',
    'journey_west': 'Journey to the West',
    'red_chamber': 'Dream of the Red Chamber',
}

for novel in novels:
    gexf_file = f"{novel}_top30_focus.gexf"
    if not os.path.exists(gexf_file):
        continue
        
    print(f"Plotting publication graph for {novel.upper()}...")
    G = nx.read_gexf(gexf_file)
    
    k_value = 1.8 if novel == 'journey_west' else 0.8
    pos = nx.spring_layout(G, k=k_value, iterations=200, seed=42)
    
    plt.figure(figsize=(14, 9), dpi=300)
    
    try:
        node_sizes = [float(G.nodes[n].get('degree_centrality', 0.1)) * 1200 for n in G.nodes()]
    except:
        node_sizes = [dict(G.degree())[n] * 30 for n in G.nodes()]
        
    node_sizes = [max(size, 100) for size in node_sizes]
    
    try:
        communities = [int(float(G.nodes[n].get('modularity_class', 0))) for n in G.nodes()]
    except:
        communities = [0 for n in G.nodes()]
        
    unique_comms = list(set(communities))
    cmap = plt.colormaps.get_cmap('tab10') 
    colors = [cmap(unique_comms.index(c) % 10) for c in communities]
    
    edges = G.edges(data=True)
    try:
        weights = [float(d.get('weight', 1)) for u, v, d in edges]
    except:
        weights = [1 for u, v, d in edges]
        
    edge_widths = [np.log1p(w) * 0.4 for w in weights]
    
    nx.draw_networkx_edges(G, pos, 
                           width=edge_widths, 
                           alpha=0.25, 
                           edge_color='#888888',
                           connectionstyle='arc3,rad=0.15',
                           arrows=True,
                           arrowstyle='-') 
                           
    nodes = nx.draw_networkx_nodes(G, pos, 
                                   node_size=node_sizes, 
                                   node_color=colors, 
                                   alpha=0.9, 
                                   edgecolors='white', 
                                   linewidths=1.5)
                                   
    PINYIN_OVERRIDES = {
        '铁扇公主': 'Tie Shan Gongzhu',
        '玉皇大帝': 'Yu Huang Dadi',
        '托塔李天王': 'Tuo Tali Tianwang',
        '九曜星君': 'Jiu Yao Xingjun',
        '王母娘娘': 'Wangmu Niangniang',
        '太上老君': 'Taishang Laojun',
        '二郎神': 'Erlang Shen',
        '红孩儿': 'Hong Hai Er',
        '镇元大仙': 'Zhen Yuan Daxian',
        '菩提祖师': 'Puti Zushi'
    }

    texts = []
    for node, (x, y) in pos.items():
        node_str = str(node)
        
        if node_str in PINYIN_OVERRIDES:
            pinyin_str = PINYIN_OVERRIDES[node_str]
        else:
            pinyin_list = pinyin(node_str, style=Style.NORMAL)
            raw_pinyin = [p[0].lower() for p in pinyin_list]
            
            COMPOUND_SURNAMES = ['zhuge', 'sima', 'xiahou', 'taishi', 'gongsun', 'xue', 'jia']
            if len(raw_pinyin) >= 3 and (raw_pinyin[0] + raw_pinyin[1]) in COMPOUND_SURNAMES:
                surname = (raw_pinyin[0] + raw_pinyin[1]).capitalize()
                given = "".join(raw_pinyin[2:]).capitalize()
                pinyin_str = f"{surname} {given}"
            elif len(raw_pinyin) >= 2:
                surname = raw_pinyin[0].capitalize()
                given = "".join(raw_pinyin[1:]).capitalize()
                pinyin_str = f"{surname} {given}"
            else:
                pinyin_str = raw_pinyin[0].capitalize()
        
        texts.append(plt.text(x, y, pinyin_str, fontsize=12, fontweight='bold', 
                              ha='center', va='center',
                              bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.15')))
                              
    adjust_text(texts, lim=1000, expand_points=(1.5, 1.5), expand_text=(1.5, 1.5), 
                force_text=(0.8, 0.8), force_points=(0.8, 0.8),
                arrowprops=dict(arrowstyle="-", color='gray', lw=0.5, alpha=0.6))
    

    plt.axis('off')
    plt.tight_layout()
    
    out_file = f"plot_{novel}.png"
    plt.savefig(out_file, bbox_inches='tight', dpi=300)
    
    out_file_pdf = f"{novel}_academic_plot.pdf"
    plt.savefig(out_file_pdf, bbox_inches='tight')
    
    plt.close()
    
    print(f"Image successfully saved: {out_file}")

print("\nProcess complete. All PNG images generated.")
