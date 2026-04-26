# Character Network Analysis of China's Four Great Classical Novels

[English](#english) | [中文](#zhongwen)

<a id="english"></a>

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

<p align="center">
  <img src="plot_three_kingdoms.png" width="45%" alt="Romance of the Three Kingdoms Network">
  <img src="plot_water_margin.png" width="45%" alt="Water Margin Network">
</p>
<p align="center">
  <img src="plot_journey_west.png" width="45%" alt="Journey to the West Network">
  <img src="plot_red_chamber.png" width="45%" alt="Dream of the Red Chamber Network">
</p>

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
2. Install dependencies: `pip install requests beautifulsoup4 jieba networkx python-louvain pandas matplotlib adjustText pypinyin`
3. (Optional) Run the `01*_scrape_*.py` scripts to fetch the latest raw texts. Note: Raw texts are not included in this repository due to their large file sizes.
4. Run `03_build_network.py` followed by `04_calculate_centrality.py`.
5. Open the resulting `.gexf` files in [Gephi](https://gephi.org/) for advanced visualization.

## License & Citation
If you use this code or dataset in your research, please cite our paper published in *Sinolingua*. The code in this repository is open-sourced under the MIT License.

---

<a id="zhongwen"></a>

# 中国四大名著的人物网络分析

[English](#english) | [中文](#zhongwen)

本仓库包含以下学术论文的数据集和 Python 源代码：
**Mapping Narrative Structures Through Character Networks: A Comparative Computational Analysis of China's Four Great Classical Novels** (通过人物网络绘制叙事结构：中国四大名著的比较计算分析)
*(已提交至 Sinolingua: Journal of Chinese Studies)*

## 概述
本项目应用社会网络分析 (SNA) 对中国文学四大名著的人物交互网络进行数学映射和比较：
1. *Romance of the Three Kingdoms* (三国演义)
2. *Water Margin* (水浒传)
3. *Journey to the West* (西游记)
4. *Dream of the Red Chamber* (红楼梦)

本研究采用基于段落的共现提取方法，测量了度中心性 (Degree)、中介中心性 (Betweenness) 和特征向量中心性 (Eigenvector)，并使用 Louvain 算法进行社区发现，从而揭示每种文学体裁的结构“指纹”。

<p align="center">
  <img src="plot_three_kingdoms.png" width="45%" alt="三国演义网络图">
  <img src="plot_water_margin.png" width="45%" alt="水浒传网络图">
</p>
<p align="center">
  <img src="plot_journey_west.png" width="45%" alt="西游记网络图">
  <img src="plot_red_chamber.png" width="45%" alt="红楼梦网络图">
</p>

## 仓库结构

### 1. 数据收集与预处理
- `01a_scrape_three_kingdoms.py`, `01b_scrape_water_margin.py`, `01c_scrape_journey_west.py`, `01d_scrape_red_chamber.py`: 用于从维基文库 (Wikisource) 抓取原始中文文本章节的网络爬虫。
- `02*_extract_*.py`: 利用 `jieba` 词性标注 (`nr`) 和自定义别名词典提取命名实体的脚本。
- `entities_*_verified.csv`: 经过人工验证的别名词典，将各种角色别名映射到其标准名称。

### 2. 网络构建与指标计算
- `03_build_network.py`: 通过扫描已验证角色在段落内的共现来构建边列表（最低阈值权重 ≥ 3）。
- `04_calculate_centrality.py`: 计算网络中心性和 Louvain 社区，输出 `centrality_metrics_summary.csv`。
- `05a_generate_graphs.py` & `05b_generate_pngs.py`: 可视化脚本，用于在 Gephi 中进行人工优化前生成初始图形布局。

### 3. 生成的数据集
- `network_*.gexf`: 每部小说的完整数学网络图，可直接在 Gephi 或 NetworkX 中打开。
- `edgelist_*.csv`: 原始交互边和权重。
- `centrality_metrics_summary.csv`: 每部小说中主要人物的最终中心性指标计算结果。

## 可重复性
复现论文中的研究结果：
1. 确保已安装 Python 3.9+。
2. 安装依赖项：`pip install requests beautifulsoup4 jieba networkx python-louvain pandas matplotlib adjustText pypinyin`
3. (可选) 运行 `01*_scrape_*.py` 脚本获取最新的原始文本。注意：由于文件较大，本仓库不包含原始文本。
4. 运行 `03_build_network.py`，然后运行 `04_calculate_centrality.py`。
5. 在 [Gephi](https://gephi.org/) 中打开生成的 `.gexf` 文件以进行高级可视化。

## 许可与引用
如果您在研究中使用了本代码或数据集，请引用发表在 *Sinolingua* 上的论文。本仓库中的代码遵循 MIT 许可证开源。
