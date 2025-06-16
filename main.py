# wechat_daily_bot/main.py

import os
from stock_provider import get_stock_summary
from fitness_provider import get_fitness_tip
from wechat_sender import send_wecom_message
from weather_provider import get_weather
from tianapi_provider import get_tianapi_data

def run_bot():
    # 获取各项内容
    weather = get_weather()
    fitness = get_fitness_tip()
    stock = get_stock_summary()

    # 天行 API 内容（附带 Emoji）
    caipu_data = get_tianapi_data('caipu')
    if isinstance(caipu_data, dict):
        caipu = f"🥗 美食推荐：{caipu_data.get('cp_name', '暂无')}，{caipu_data.get('texing', '')}"
    else:
        caipu = f"🥗 美食推荐：{caipu_data}"

    zaoan = f"📖 每日一句：{get_tianapi_data('zaoan')}"

    health_raw = get_tianapi_data('health')
    if isinstance(health_raw, list):
        health_items = [f"- {item['title']}" for item in health_raw if isinstance(item, dict) and 'title' in item]
        health = "🧘 健康养生：\n" + "\n".join(health_items[:3])
    else:
        health = f"🧘 健康养生：{health_raw}"

    chengyu = f"📚 每日成语：{get_tianapi_data('chengyu')}"
    lishi = f"📅 历史上的今天：{get_tianapi_data('lishi')}"

    news_raw = get_tianapi_data('guonei')
    if isinstance(news_raw, list):
        news_items = [f"- {item['title']}" for item in news_raw if isinstance(item, dict) and 'title' in item]
        news = "📰 国内新闻：\n" + "\n".join(news_items[:3])
    else:
        news = f"📰 国内新闻：{news_raw}"

    # 拼接消息
    content = f"""
📅 今日早报

☀️ 天气：{weather}

{caipu}
{zaoan}
{health}
{chengyu}
{lishi}
{news}

🏋️ 健身饮食：{fitness}

📈 股市概览：{stock}
    """

    send_wecom_message(content.strip())

if __name__ == "__main__":
    run_bot()
