
# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather(city_code="101190101"):
    key = os.environ.get("HEFENG_API_KEY")
    url = f"https://devapi.qweather.com/v7/weather/now?location={city_code}&key={key}"
    resp = requests.get(url).json()
    now = resp.get("now", {})
    return f"{now.get('text', '未知')}, {now.get('temp', '?')}℃, 湿度 {now.get('humidity', '?')}%"
