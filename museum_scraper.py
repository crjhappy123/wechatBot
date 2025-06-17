# wechat_daily_bot/museum_scraper.py

import requests
from bs4 import BeautifulSoup

def get_latest_museum_notices(limit=3):
    url = "https://njggzy.nanjing.gov.cn/njweb/search/fullsearch.html?wd=博物馆"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        result_list = soup.select("ul.searchList li")

        results = []
        for item in result_list:
            title_tag = item.select_one("a")
            date_tag = item.select_one("span")
            if title_tag and date_tag:
                title = title_tag.get_text(strip=True)
                href = title_tag["href"]
                date = date_tag.get_text(strip=True)
                if href.startswith("/"):
                    href = "https://njggzy.nanjing.gov.cn" + href
                results.append(f"{title} ({date})\n{href}")
                if len(results) >= limit:
                    break

        return results if results else ["暂无博物馆相关公告"]

    except Exception as e:
        return [f"获取失败：{e}"]
