# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather_summary():
    key = os.environ.get("QWEATHER_API_KEY")
    base_url = "https://n749vgt7bu.re.qweatherapi.com/v7"

    # 定义请求地址
    now_url = f"{base_url}/weather/now?location=101190104&key={key}"
    air_url = f"{base_url}/air/now?location=101190104&key={key}"
    indices_url = f"{base_url}/indices/1d?location=101190104&type=5&key={key}"  # 紫外线指数 type=5

    try:
        # 实况天气
        now_resp = requests.get(now_url).json()
        weather = now_resp.get("now", {})
        desc = weather.get("text", "未知")
        temp = weather.get("temp", "未知")
        feels_like = weather.get("feelsLike", "未知")
        humidity = weather.get("humidity", "未知")
        wind_dir = weather.get("windDir", "未知")

        # 空气质量
        air_resp = requests.get(air_url).json()
        air = air_resp.get("now", {})
        aqi = air.get("aqi", "未知")
        category = air.get("category", "未知")

        # 紫外线指数
        indices_resp = requests.get(indices_url).json()
        uv_level = "未知"
        if indices_resp.get("code") == "200":
            uv_data = indices_resp.get("daily", [{}])[0]
            uv_level = uv_data.get("level", "未知") + "（" + uv_data.get("name", "") + "）"

        summary = (
            f"天气：{desc}，气温 {temp}°C（体感 {feels_like}°C），湿度 {humidity}%，风向 {wind_dir}。\n"
            f"空气质量：{category}（AQI {aqi}）。\n"
            f"紫外线指数：{uv_level}"
        )

        return summary

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
