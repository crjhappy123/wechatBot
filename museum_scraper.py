# wechat_daily_bot/museum_scraper.py

import requests
from bs4 import BeautifulSoup

def get_latest_museum_notices(max_pages=10):
    base_url = "https://njggzy.nanjing.gov.cn/njweb/column/38257?pageNo={}"
    keyword = "博物馆"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    results = []
    
    for page in range(1, max_pages + 1):
        url = base_url.format(page)
        resp = requests.get(url, headers=headers, timeout=8)
        if resp.status_code != 200:
            continue
        soup = BeautifulSoup(resp.text, 'html.parser')
        items = soup.select('div.article-list ul li')  # 根据网页结构调整
        
        for item in items:
            a = item.find('a')
            if a and keyword in a.text:
                title = a.text.strip()
                href = a['href']
                full_url = href if href.startswith('http') else f"https://njggzy.nanjing.gov.cn{href}"
                results.append(f"{title} 👉 {full_url}")
        
        if len(results) >= 3:
            break
    
    return results[:3] if results else ["暂无博物馆相关公告"]


