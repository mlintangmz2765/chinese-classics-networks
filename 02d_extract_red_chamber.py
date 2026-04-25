import jieba.posseg as pseg
from collections import Counter
import csv
import re
import time

INPUT_FILE = "Honglou_Meng_Raw.txt"
OUTPUT_FILE = "entities_red_chamber.csv"

def is_valid_name(word):
    if len(word) < 2 or len(word) > 4:
        return False
    invalid_words = {
        '今日', '太守', '将军', '主公', '不可', '如何', '丞相', '都督', '大王', '陛下', 
        '先生', '左右', '商议', '天下', '一面', '大喜', '于是', '不能', '今日', '不敢',
        '太太', '老爷', '奶奶', '姑娘', '丫头'
    }
    if word in invalid_words:
        return False
    return True

def main():
    print(f"Reading raw text from {INPUT_FILE}...")
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File {INPUT_FILE} not found. Ensure scraping is complete.")
        return

    print("Cleaning text...")
    text = re.sub(r'[^\u4e00-\u9fa5]+', '', text)
    
    print("Starting entity extraction for Dream of the Red Chamber...")
    start_time = time.time()
    words = pseg.cut(text)
    name_counter = Counter()
    
    count = 0
    for word, flag in words:
        if flag == 'nr' and is_valid_name(word):
            name_counter[word] += 1
        count += 1
        if count % 100000 == 0:
            print(f"Processed {count} words...")

    top_names = name_counter.most_common(400)
    print(f"\nSaving {len(top_names)} top entities to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Extracted_Name', 'Frequency', 'Main_Name_Mapping'])
        for name, freq in top_names:
            writer.writerow([name, freq, ''])
            
    elapsed_time = time.time() - start_time
    print(f"Finished in {elapsed_time:.2f} seconds!")

if __name__ == "__main__":
    main()
