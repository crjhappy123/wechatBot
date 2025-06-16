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
    caipu_raw = get_tianapi_data('caipu')
    if isinstance(caipu_raw, list) and len(caipu_raw) > 0:
        cp = random.choice(caipu_raw)
        caipu = (
            f"🥗 美食推荐：{cp.get('cp_name')}\n"
            f"特性：{cp.get('texing', '无')}\n"
            f"原料：{cp.get('yuanliao', '无')}\n"
            f"调料：{cp.get('tiaoliao', '无')}\n"
            f"做法：{cp.get('zuofa')}"
        )
    else:
        caipu = f"🥗 美食推荐：{caipu_raw}"

    zaoan = f"📖 每日一句：{get_tianapi_data('zaoan')}"

    health_raw = get_tianapi_data('health')
    if isinstance(health_raw, list) and len(health_raw) > 0:
        health = f"🧘 健康养生：{health_raw[0]}"
    else:
        health = f"🧘 健康养生：{health_raw}"

    chengyu = f"📚 每日成语：{get_tianapi_data('chengyu')}"
    lishi = f"📅 历史上的今天：{get_tianapi_data('lishi')}"

    news_raw = get_tianapi_data('guonei')
    if isinstance(news_raw, list) and len(news_raw) > 0:
        news = "📰 国内新闻：\n- " + "\n- ".join(news_raw)
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
