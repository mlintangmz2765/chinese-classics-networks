# Character Network Analysis of China's Four Great Classical Novels

This repository contains the dataset and Python source code for the academic paper:
**Mapping Narrative Structures Through Character Networks: A Comparative Computational Analysis of China's Four Great Classical Novels**
*(Submitted to Sinolingua: Journal of Chinese Studies)*

## Overview
This project applies Social Network Analysis (SNA) to mathematically map and compare the character interaction networks of the Four Great Classical Novels of Chinese literature (四大名著):
1. *Romance of the Three Kingdoms* (三国演义)
2. *Water Margin* (水浒传)
3. *Journey to the West* (西游记)
4. *Dream of the Red Chamber* (红楼梦)

Using paragraph-based co-occurrence extraction, this study measures Degree, Betweenness, and Eigenvector centralities, and employs the Louvain algorithm for community detection to reveal structural "fingerprints" of each genre.

## Repository Structure

### 1. Data Collection & Preprocessing
- `01a_scrape_three_kingdoms.py`, `01b_scrape_water_margin.py`, `01c_scrape_journey_west.py`, `01d_scrape_red_chamber.py`: Web scrapers to pull raw Chinese text chapters from Wikisource.
- `02*_extract_*.py`: Scripts that utilize `jieba` POS-tagging (`nr`) and custom alias dictionaries to extract named entities.
- `entities_*_verified.csv`: The manually verified alias dictionaries mapping various character aliases to their canonical names.

### 2. Network Construction & Metrics
- `03_build_network.py`: Constructs the edge list by scanning for paragraph-based co-occurrences of verified characters (minimum threshold weight ≥ 3).
- `04_calculate_centrality.py`: Computes network centralities and Louvain communities, outputting the `centrality_metrics_summary.csv`.
- `05a_generate_graphs.py` & `05b_generate_pngs.py`: Visualization scripts to generate initial graph layouts before manual polishing in Gephi.

### 3. Generated Datasets
- `network_*.gexf`: The complete mathematical network graphs for each novel, ready to be opened in Gephi or NetworkX.
- `edgelist_*.csv`: Raw interaction edges and weights.
- `centrality_metrics_summary.csv`: The final computed centrality metrics for the top characters in each novel.

## Reproducibility
To reproduce the findings in the paper:
1. Ensure you have Python 3.9+ installed.
2. Install dependencies: `pip install requests beautifulsoup4 jieba networkx python-louvain pandas matplotlib`
3. (Optional) Run the `01*_scrape_*.py` scripts to fetch the latest raw texts. Note: Raw texts are not included in this repository due to their large file sizes.
4. Run `03_build_network.py` followed by `04_calculate_centrality.py`.
5. Open the resulting `.gexf` files in [Gephi](https://gephi.org/) for advanced visualization.

## License & Citation
If you use this code or dataset in your research, please cite our paper published in *Sinolingua*. The code in this repository is open-sourced under the MIT License.
