# wechat_daily_bot/weather_provider.py
import requests
import os

def get_weather(city_code="320115"):  # 江宁区行政代码
    key = os.environ.get("GAODE_API_KEY")
    base_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    params = {
        "key": key,
        "city": city_code,
        "extensions": "all",  # 获取未来3天天气 + 当天预报
        "output": "JSON"
    }

    try:
        resp = requests.get(base_url, params=params)
        resp.raise_for_status()
        data = resp.json()
        forecasts = data.get("forecasts", [{}])[0]

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

        summary.append(f"更新时间：{report_time}")
        return "\n".join(summary)
    except Exception as e:
        return f"天气信息获取失败：{str(e)}"
