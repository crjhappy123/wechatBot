# wechat_daily_bot/main.py

import os
from weather_provider import get_weather
from stock_provider import get_stock_summary
from fitness_provider import get_fitness_tip
from wechat_sender import send_wecom_message

def run_bot():
    weather = get_weather()
    fitness = get_fitness_tip()
    stock = get_stock_summary()

    content = f"""
    📅 今日早报

    ☀️ 天气：{weather}

    🏋️健身饮食：{fitness}

    📈 股市概览：{stock}
    """
    send_wecom_message(content.strip())

if __name__ == "__main__":
    run_bot()
