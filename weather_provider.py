# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather():
    try:
        base_url = "https://n749vgt7bu.re.qweatherapi.com/v7/weather/now"
        location = "101190104"  # 南京江宁区
        key = os.environ.get("QWEATHER_API_KEY")

        if not key:
            return "⚠️ 缺少和风天气API Key"

        url = f"{base_url}?location={location}&key={key}"
        response = requests.get(url)
        data = response.json()

        if "code" in data and data["code"] != "200":
            return f"⚠️ 获取和风天气失败：{data.get('code', '未知错误')}"

        now = data["now"]
        weather_text = now["text"]
        temp = now["temp"]
        humidity = now.get("humidity", "?")
        wind_dir = now.get("windDir", "?")
        wind_scale = now.get("windScale", "?")

        return f"{weather_text}，气温 {temp}℃，湿度 {humidity}% ，{wind_dir}风 {wind_scale}级"

    except Exception as e:
        return f"⚠️ 获取和风天气失败：天气接口返回异常：{str(e)}"
