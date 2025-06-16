# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather():
    try:
        api_host = "https://n749vgt7bu.re.qweatherapi.com"
        location = "101190104"  # 南京市江宁区
        url = f"{api_host}/v7/weather/now?location={location}"

        headers = {
            "X-QW-Api-Key": os.environ.get("QWEATHER_API_KEY")
        }

        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if "now" not in data:
            return f"⚠️ 获取和风天气失败：天气接口返回异常：{data}"

        now = data["now"]
        return f"{now['text']}，气温{now['temp']}℃，湿度{now['humidity']}%，风力{now['windScale']}级，风向{now['windDir']}。"

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
