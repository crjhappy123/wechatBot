
# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather(city_code="320100"):
    key = os.environ.get("GAODE_API_KEY")
    url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={key}&extensions=base&output=JSON"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        lives = data.get("lives", [{}])[0]
        weather = lives.get("weather", "未知")
        temperature = lives.get("temperature", "?")
        humidity = lives.get("humidity", "?")
        report_time = lives.get("reporttime", "")
        return f"{weather}, {temperature}℃, 湿度 {humidity}%, 更新于 {report_time}"
    except Exception as e:
        return "天气信息获取失败"
