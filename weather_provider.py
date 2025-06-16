# wechat_daily_bot/weather_provider.py
import os
import requests
from openai import OpenAI, RateLimitError
import time


def get_weather():
    try:
        api_key = os.environ.get("QWEATHER_API_KEY")
        if not api_key:
            return "⚠️ 缺少和风天气 API Key 环境变量 QWEATHER_API_KEY"

        location = "101190104"  # 南京市江宁区
        base_host = "https://n749vgt7bu.re.qweatherapi.com"

        now_url = f"{base_host}/v7/weather/now?location={location}&key={api_key}"
        air_url = f"{base_host}/v7/air/now?location={location}&key={api_key}"
        uv_url = f"{base_host}/v7/indices/1d?location={location}&type=5&key={api_key}"
        forecast_url = f"{base_host}/v7/weather/3d?location={location}&key={api_key}"

        now_resp = requests.get(now_url)
        air_resp = requests.get(air_url)
        uv_resp = requests.get(uv_url)
        forecast_resp = requests.get(forecast_url)

        if now_resp.status_code != 200 or now_resp.json().get("code") != "200":
            return f"⚠️ 获取天气失败：{now_resp.json()}"
        if air_resp.status_code != 200 or air_resp.json().get("code") != "200":
            return f"⚠️ 获取空气质量失败：{air_resp.json()}"
        if uv_resp.status_code != 200 or uv_resp.json().get("code") != "200":
            return f"⚠️ 获取紫外线指数失败：{uv_resp.json()}"
        if forecast_resp.status_code != 200 or forecast_resp.json().get("code") != "200":
            return f"⚠️ 获取天气预报失败：{forecast_resp.json()}"

        now_data = now_resp.json().get("now", {})
        air_data = air_resp.json().get("now", {})
        uv_data = uv_resp.json().get("daily", [{}])[0]
        forecast = forecast_resp.json().get("daily", [{}])[0]

        weather_text = now_data.get("text", "未知")
        temp = now_data.get("temp", "?")
        humidity = now_data.get("humidity", "?")
        wind = now_data.get("windScale", "?")
        air_quality = air_data.get("category", "未知")
        pm25 = air_data.get("pm2p5", "?")
        uv_index = uv_data.get("category", "未知")
        forecast_text = forecast.get("textDay", "晴") + "转" + forecast.get("textNight", "晴")
        temp_max = forecast.get("tempMax", "?")
        temp_min = forecast.get("tempMin", "?")

        base_summary = (
            f"{weather_text}，气温 {temp}℃，湿度 {humidity}%，风力 {wind}级；\n"
            f"空气质量：{air_quality}，PM2.5：{pm25}；\n"
            f"紫外线强度：{uv_index}；\n"
            f"今日预报：{forecast_text}，最高 {temp_max}℃，最低 {temp_min}℃；"
        )

        # ChatGPT 推荐衣着运动建议
        suggestion = get_gpt_suggestion(
            f"南京今天天气：{weather_text}，最高温 {temp_max}℃，最低温 {temp_min}℃，空气质量 {air_quality}，紫外线 {uv_index}。请给出穿衣建议和运动建议，不超过40字。"
        )

        return base_summary + "\n👕 穿衣建议与运动建议：" + suggestion

    except Exception as e:
        return f"⚠️ 获取和风天气失败：{str(e)}"


def get_gpt_suggestion(prompt):
    try:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return "❌ 缺少 OpenAI API Key"

        client = OpenAI(api_key=api_key)
        models = ["gpt-4o", "gpt-3.5-turbo"]

        for model in models:
            for attempt in range(2):
                try:
                    resp = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    return resp.choices[0].message.content.strip()
                except RateLimitError:
                    if model == "gpt-4o" and attempt == 1:
                        break
                    time.sleep(8)
                except Exception:
                    break

        return "❌ 建议生成失败：请稍后再试"

    except Exception as e:
        return f"❌ ChatGPT调用失败：{str(e)}"
