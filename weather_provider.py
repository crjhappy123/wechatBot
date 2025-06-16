import os
import requests

def get_weather():
    key = os.environ.get("QWEATHER_API_KEY")
    location = "101190104"  # 南京江宁区 Location ID

    try:
        resp = requests.get(
            f"https://devapi.qweather.com/v7/weather/now?location={location}&key={key}"
        )
        weather = resp.json()

        if "now" not in weather:
            raise ValueError(f"接口返回异常：{weather}")

        now = weather["now"]

        air_resp = requests.get(
            f"https://devapi.qweather.com/v7/air/now?location={location}&key={key}"
        )
        air_data = air_resp.json()
        air_now = air_data.get("now", {})

        return (
            f"天气：{now.get('text')}，气温：{now.get('temp')}℃，湿度：{now.get('humidity')}%，"
            f"空气质量：{air_now.get('category', '未知')}（AQI: {air_now.get('aqi', '?')}，"
            f"PM2.5: {air_now.get('pm2p5', '?')}）"
        )

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
