# wechat_daily_bot/museum_scraper.py

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://njggzy.nanjing.gov.cn"
SEARCH_URL = "https://njggzy.nanjing.gov.cn/njweb/search/fullsearch.html"
KEYWORDS = ['博物馆', '展览馆', '文物']

def get_latest_museum_notices():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    notices = []

    for page in range(1, 11):  # 抓取前10页
        params = {
            "wd": "博物馆",
            "page": page
        }

        try:
            resp = requests.get(SEARCH_URL, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            for a in soup.find_all("a", href=True):
                title = a.get_text(strip=True)
                href = a["href"]

                if any(kw in title for kw in KEYWORDS):
                    full_url = href if href.startswith("http") else BASE_URL + href
                    notice = f"{title} 👉 {full_url}"
                    if notice not in notices:
                        notices.append(notice)
                        if len(notices) >= 3:
                            return notices

        except Exception as e:
            return [f"❌ 博物馆信息抓取失败：{str(e)}"]

    return ["暂无博物馆相关公告"]

