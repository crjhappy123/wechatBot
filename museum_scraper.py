# wechat_daily_bot/museum_scraper.py

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_latest_museum_notices():
    options = Options()
    options.add_argument("--headless=new")  # 建议使用新 headless 模式
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(options=options)
        url = "https://njggzy.nanjing.gov.cn/njweb/search/fullsearch.html?wd=博物馆"
        driver.get(url)

        # 等待列表元素加载
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-cont-box > ul > li"))
        )

        elements = driver.find_elements(By.CSS_SELECTOR, "div.search-cont-box > ul > li")
        results = []

        for el in elements[:5]:
            title = el.text.strip()
            if title:
                results.append(title)

        return results if results else ["暂无博物馆相关公告"]

    except Exception as e:
        return [f"❌ 抓取失败：{str(e)}"]

    finally:
        driver.quit()
