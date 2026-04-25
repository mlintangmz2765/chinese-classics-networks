import requests
from bs4 import BeautifulSoup
import time
import os

TOTAL_CHAPTERS = 120
BASE_URL = "https://zh.wikisource.org/wiki/水滸傳_(120回本)/第{:03d}回"
OUTPUT_FILE = "Shuihu_Zhuan_Raw.txt"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
}

def scrape_chapter(chapter_num):
    url = BASE_URL.format(chapter_num)
    print(f"Fetching Chapter {chapter_num:03d}: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find('div', class_='mw-parser-output')
        if not content_div:
            return None
            
        paragraphs = content_div.find_all('p')
        
        chapter_text = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                chapter_text.append(text)
                
        return "\n".join(chapter_text)
        
    except Exception as e:
        print(f"Error fetching Chapter {chapter_num}: {e}")
        return None

def main():
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"Old file {OUTPUT_FILE} deleted, starting fresh download...")
        
    print(f"Starting scraping {TOTAL_CHAPTERS} chapters of Shui Hu Zhuan (Batas Air) from Wikisource...")
    
    for i in range(1, TOTAL_CHAPTERS + 1):
        content = scrape_chapter(i)
        
        if content:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n\n=== CHAPTER {i} ===\n\n")
                f.write(content)
            print(f"Chapter {i:03d} successfully saved.")
        else:
            print(f"Failed to process Chapter {i:03d}.")
            
        time.sleep(2)
        
    print(f"Done! All text for Shui Hu Zhuan saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
