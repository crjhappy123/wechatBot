import requests
import os

def get_weather():
    key = os.environ.get("QWEATHER_API_KEY")
    location = "101190104"  # 南京江宁区，使用和风城市ID
    try:
        weather = requests.get(
            f"https://devapi.qweather.com/v7/weather/now?location={location}&key={key}"
        ).json()
        air = requests.get(
            f"https://devapi.qweather.com/v7/air/now?location={location}&key={key}"
        ).json()
        now = weather["now"]
        air_now = air["now"]
        return (
            f"天气：{now['text']}，气温：{now['temp']}℃，湿度：{now['humidity']}%，"
            f"空气质量：{air_now['category']}（AQI: {air_now['aqi']}，PM2.5: {air_now['pm2p5']}）"
        )
    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
