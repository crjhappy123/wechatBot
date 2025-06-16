# wechat_daily_bot/main.py

import os
from weather_provider import get_weather, get_tianapi_data
from stock_provider import get_stock_summary
from fitness_provider import get_fitness_tip
from wechat_sender import send_wecom_message

def run_bot():
    # 获取各项内容
    weather = get_weather()
    fitness = get_fitness_tip()
    stock = get_stock_summary()

    # 天行 API 内容（附带 Emoji）
    caipu = f"🥗 美食推荐：{get_tianapi_data('caipu')}"
    zaoan = f"📖 每日一句：{get_tianapi_data('zaoan')}"
    health = f"🧘 健康养生：{get_tianapi_data('health')}"
    chengyu = f"📚 每日成语：{get_tianapi_data('chengyu')}"
    lishi = f"📅 历史上的今天：{get_tianapi_data('lishi')}"
    news = f"📰 国内新闻：{get_tianapi_data('guonei')}"

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
