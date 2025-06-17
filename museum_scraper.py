# wechat_daily_bot/museum_scraper.py

import requests
from bs4 import BeautifulSoup

def get_latest_museum_notices():
    url = "https://njggzy.nanjing.gov.cn/njweb/search/fullsearch.html?wd=博物馆"
    try:
        response = requests.get(url, timeout=8)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='list-item')

        museum_news = []
        for item in items:
            title_tag = item.find('a', title=True)
            if title_tag and "博物馆" in title_tag['title']:
                title = title_tag['title']
                museum_news.append(title)
            if len(museum_news) >= 3:
                break

        if not museum_news:
            return ["暂无博物馆相关公告"]

        return museum_news

    except Exception as e:
        return [f"❌ 获取失败：{str(e)}"]
