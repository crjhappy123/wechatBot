# wechat_daily_bot/weather_provider.py
import os
import requests


def get_weather():
    try:
        api_key = os.environ.get("QWEATHER_API_KEY")
        if not api_key:
            return "⚠️ 缺少和风天气 API Key 环境变量 QWEATHER_API_KEY"

        base_url = "https://n749vgt7bu.re.qweatherapi.com/v7/weather/now"
        location = "101190104"  # 南京市江宁区
        now_url = f"{base_url}?location={location}&key={api_key}"

        air_url = f"https://n749vgt7bu.re.qweatherapi.com/v7/air/now?location={location}&key={api_key}"
        indices_url = f"https://n749vgt7bu.re.qweatherapi.com/v7/indices/1d?location={location}&type=5&key={api_key}"  # 紫外线指数类型=5

        now_resp = requests.get(now_url)
        air_resp = requests.get(air_url)
        indices_resp = requests.get(indices_url)

        if now_resp.status_code != 200 or "code" in now_resp.json() and now_resp.json().get("code") != "200":
            return f"⚠️ 获取天气失败：{now_resp.json()}"
        if air_resp.status_code != 200 or "code" in air_resp.json() and air_resp.json().get("code") != "200":
            return f"⚠️ 获取空气质量失败：{air_resp.json()}"
        if indices_resp.status_code != 200 or "code" in indices_resp.json() and indices_resp.json().get("code") != "200":
            return f"⚠️ 获取紫外线指数失败：{indices_resp.json()}"

        now_data = now_resp.json().get("now", {})
        air_data = air_resp.json().get("now", {})
        uv_data = indices_resp.json().get("daily", [{}])[0]

        summary = (
            f"{now_data.get('text', '未知')}，气温 {now_data.get('temp', '?')}℃，"
            f"湿度 {now_data.get('humidity', '?')}%，风力 {now_data.get('windScale', '?')}级；\n"
            f"空气质量：{air_data.get('category', '未知')}，PM2.5：{air_data.get('pm2p5', '?')}；\n"
            f"紫外线强度：{uv_data.get('category', '未知')}"
        )

        return summary

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"
