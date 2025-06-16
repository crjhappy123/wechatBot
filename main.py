# wechat_daily_bot/main.py

import os
import random
from weather_provider import get_weather
from stock_provider import get_stock_summary
from fitness_provider import get_fitness_tip
from wechat_sender import send_wecom_message
from tianapi_provider import get_tianapi_data

def run_bot():
    # 获取各项内容
    weather = get_weather()
    fitness = get_fitness_tip()
    stock = get_stock_summary()

    # 天行 API 内容（附带 Emoji）
    caipu_data = get_tianapi_data('caipu')
    if isinstance(caipu_data, list) and len(caipu_data) > 0:
        cp = random.choice(caipu_data)
        caipu = (
            f"🥗 美食推荐：{cp.get('cp_name', '未知')}\n"
            f"特性：{cp.get('texing', '无')}\n"
            f"原料：{cp.get('yuanliao', '无')}\n"
            f"调料：{cp.get('tiaoliao', '无')}\n"
            f"做法：{cp.get('zuofa', '无')}"
        )
    else:
        caipu = f"🥗 美食推荐：{caipu_data}"

    zaoan = f"📖 每日一句：{get_tianapi_data('zaoan')}"

    health_data = get_tianapi_data('health')
    if isinstance(health_data, list) and len(health_data) > 0:
        health = f"🧘 健康养生：{health_data[0]}"
    else:
        health = f"🧘 健康养生：{health_data}"

    chengyu = f"📚 每日成语：{get_tianapi_data('chengyu')}"
    lishi = f"📅 历史上的今天：{get_tianapi_data('lishi')}"

    news_data = get_tianapi_data('guonei')
    if isinstance(news_data, list) and len(news_data) > 0:
        news = "📰 国内新闻：\n- " + "\n- ".join(news_data)
    else:
        news = f"📰 国内新闻：{news_data}"

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
