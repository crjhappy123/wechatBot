# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather(city_code="320100"):  # 江宁区行政代码
    key = os.environ.get("GAODE_API_KEY")
    base_url_weather = "https://restapi.amap.com/v3/weather/weatherInfo"
    base_url_air = "https://restapi.amap.com/v3/air/now"

    try:
        # 获取天气预报
        weather_resp = requests.get(base_url_weather, params={
            "key": key,
            "city": city_code,
            "extensions": "all",
            "output": "JSON"
        })
        weather_resp.raise_for_status()
        forecasts = weather_resp.json().get("forecasts", [{}])[0]

        city = forecasts.get("city", "未知地区")
        report_time = forecasts.get("reporttime", "未知时间")
        casts = forecasts.get("casts", [])

        summary = [f"{city}（江宁区）天气预报："]
        for day in casts[:1]:  # 只展示今天
            date = day.get("date", "")
            week = day.get("week", "")
            day_weather = day.get("dayweather", "")
            night_weather = day.get("nightweather", "")
            day_temp = day.get("daytemp", "")
            night_temp = day.get("nighttemp", "")
            wind = day.get("daywind", "")
            power = day.get("daypower", "")

            summary.append(f"{date}（周{week}）：白天{day_weather}，夜间{night_weather}，气温{night_temp}~{day_temp}℃，{wind}风 {power}级")

        # 获取实况湿度信息
        live_resp = requests.get(base_url_weather, params={
            "key": key,
            "city": city_code,
            "extensions": "base",
            "output": "JSON"
        })
        live_resp.raise_for_status()
        live_data = live_resp.json().get("lives", [{}])[0]
        humidity = live_data.get("humidity", "?")
        summary.append(f"当前湿度：{humidity}%")

        # 获取空气质量
        air_resp = requests.get(base_url_air, params={
            "key": key,
            "city": city_code,
            "output": "JSON"
        })
        air_resp.raise_for_status()
        air_data = air_resp.json().get("lives", [{}])[0]
        aqi = air_data.get("aqi", "?")
        quality = air_data.get("quality", "?")
        pm25 = air_data.get("pm2.5", "?")
        pm10 = air_data.get("pm10", "?")
        summary.append(f"空气质量：{quality}（AQI: {aqi}，PM2.5: {pm25}，PM10: {pm10}）")

        summary.append(f"更新时间：{report_time}")
        return "\n".join(summary)

    except Exception as e:
        return f"天气信息获取失败：{str(e)}"
