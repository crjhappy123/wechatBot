# wechat_daily_bot/museum_scraper.py

import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def get_latest_museum_notices():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    url = "https://njggzy.nanjing.gov.cn/njweb/search/fullsearch.html?wd=博物馆"
    driver.get(url)
    time.sleep(3)  # 等待页面加载完成

    elements = driver.find_elements(By.CSS_SELECTOR, "div.search-cont-box > ul > li")
    results = []

    for el in elements[:5]:
        title = el.text.strip()
        if title:
            results.append(title)

    driver.quit()
    return results if results else ["暂无博物馆相关公告"]
