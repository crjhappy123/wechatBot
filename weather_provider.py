# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather():
    try:
        api_key = os.environ.get("QWEATHER_API_KEY")
        location = "101190107"  # 江宁区的Location ID（或使用经纬度）
        base_url = "https://n749vgt7bu.re.qweatherapi.com"

        # 获取实况天气
        weather_resp = requests.get(
            f"{base_url}/v7/weather/now",
            params={"location": location, "key": api_key},
            timeout=10
        )
        weather_data = weather_resp.json()

        # 获取空气质量
        air_resp = requests.get(
            f"{base_url}/v7/air/now",
            params={"location": location, "key": api_key},
            timeout=10
        )
        air_data = air_resp.json()

        # 获取生活指数（紫外线）
        uv_resp = requests.get(
            f"{base_url}/v7/indices/1d",
            params={"location": location, "type": "5", "key": api_key},
            timeout=10
        )
        uv_data = uv_resp.json()

        if weather_data.get("code") != "200":
            raise Exception(f"天气接口返回异常：{weather_data}")
        if air_data.get("code") != "200":
            raise Exception(f"空气接口返回异常：{air_data}")
        if uv_data.get("code") != "200":
            raise Exception(f"紫外线接口返回异常：{uv_data}")

        now = weather_data["now"]
        air = air_data["now"]
        uv = uv_data["daily"][0]

        return (
            f"江宁区现在是{now['text']}，温度{now['temp']}℃，湿度{now['humidity']}%。"
            f"空气质量：{air['category']}（{air['aqi']}），主要污染物：{air['primary'] if air['primary'] else '无'}。"
            f"紫外线强度：{uv['category']}。"
        )

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
